"""
AI Planner Agent

Decides the VAPT plan: which tools to run, in which phase, and why.

Grounded in the AstraIX knowledge base (360+ sources, FAISS semantic search)
so every tool decision carries explainable AI reasoning. The LLM provider
(NVIDIA NIM, falling back to local Ollama) refines the selection; otherwise
the knowledge-base heuristics stand on their own.
"""

import asyncio
import json
import os
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple

from app.core.logging import get_logger
from app.vapt.agents.kb import kb_snippets
from app.vapt.models import VAPTScanType
from app.vapt.tools import TOOLS_REGISTRY, get_available_tools

logger = get_logger(__name__)

KB_PATH = "/app/knowledge-base"

PHASE_DEFS: List[Dict[str, Any]] = [
    {
        "id": "recon",
        "name": "Reconnaissance",
        "description": "Discover live hosts, open ports and running services to map the attack surface.",
        "tools": ["nmap", "masscan", "dnsrecon", "subfinder"],
        "kb_query": "network reconnaissance port scanning service discovery nmap masscan dnsrecon subfinder",
    },
    {
        "id": "enumeration",
        "name": "Web Enumeration",
        "description": "Enumerate web paths, directories, server headers and technologies to find exposed surface.",
        "tools": ["gobuster", "ffuf", "whatweb", "httpx", "wafw00f", "arjun"],
        "kb_query": "web directory enumeration gobuster ffuf whatweb httpx wafw00f server misconfiguration",
    },
    {
        "id": "vuln_scan",
        "name": "Vulnerability Detection & Exploitation",
        "description": "Actively probe for known vulnerabilities AND exploit them with injection engines, metasploit modules and session abuse: sqlmap --level/--risk, commix, dalfox, metasploit, jwt, dom-xss, flows.",
        "tools": ["nuclei", "sqlmap", "commix", "dalfox", "metasploit", "flows", "dom-xss", "jwt"],
        "kb_query": "vulnerability scanning exploitation sqlmap commix dalfox metasploit OWASP top 10 injection session abuse",
    },
    {
        "id": "brute_force",
        "name": "Credential Testing",
        "description": "Test for weak credentials on exposed authentication services.",
        "tools": ["hydra"],
        "kb_query": "brute force weak credentials hydra password policy authentication",
    },
    {
        "id": "crypto",
        "name": "SSL/TLS Deep Dive",
        "description": "Audit SSL/TLS configuration, weak ciphers and protocol issues.",
        "tools": ["sslscan", "testssl"],
        "kb_query": "SSL TLS certificate weak ciphers protocol audit testssl",
    },
    {
        "id": "ai_security",
        "name": "AI / LLM Security",
        "description": "Probe AI/LLM endpoints for OWASP LLM Top 10: prompt injection, jailbreaks, data leakage.",
        "tools": ["garak", "promptfoo", "forms"],
        "kb_query": "AI LLM security prompt injection jailbreak OWASP LLM top 10 garak",
    },
]

TOOL_KB_QUERIES: Dict[str, str] = {
    "nmap": "nmap port scanning service fingerprinting techniques",
    "nikto": "nikto web server vulnerability scanning",
    "nuclei": "nuclei template vulnerability scanning CVE detection",
    "sqlmap": "sqlmap SQL injection automated testing",
    "gobuster": "gobuster directory brute force web enumeration",
    "ffuf": "ffuf fuzzing web content discovery",
    "sslscan": "sslscan SSL TLS protocol cipher audit",
    "masscan": "masscan high speed port scanning",
    "dnsrecon": "dnsrecon DNS enumeration records brute force",
    "subfinder": "subfinder passive subdomain discovery",
    "httpx": "httpx http probing technology fingerprinting",
    "whatweb": "whatweb web technology fingerprinting",
    "wafw00f": "wafw00f web application firewall detection",
    "arjun": "arjun hidden parameter discovery",
    "commix": "commix command injection detection exploitation",
    "dalfox": "dalfox XSS scanning parameter based",
    "hydra": "hydra brute force weak credentials ssh http",
    "testssl": "testssl TLS SSL configuration audit cipher suite",
    "garak": "garak LLM security prompt injection jailbreak data leakage probe",
    "promptfoo": "promptfoo LLM red-team scan OWASP LLM top 10 jailbreak strategies chat endpoint",
    "metasploit": "metasploit exploit modules payloads vulnerability exploitation",
    "flows": "API business logic flows BOLA JWT session abuse price tampering OWASP API top 10",
    "dom-xss": "DOM based XSS client side JavaScript sinks headless browser detection",
    "jwt": "JWT token security algorithm confusion none algorithm secret brute force session integrity",
    "forms": "web form API chatbot scanner prompt injection SQL injection XSS",
}
class PlannerAgent:
    """Knowledge-base-grounded plan generator for VAPT scans."""

    def _kb_search(self, query: str, top_k: int = 3) -> List[str]:
        return kb_snippets(query, top_k=top_k)

    def _parse_json(self, text: str) -> Optional[Dict[str, Any]]:
        if not text:
            return None
        text = text.strip()
        text = text[text.find("{"): text.rfind("}") + 1]
        try:
            return json.loads(text)
        except Exception:
            return None

    async def _nvidia_refine(self, messages: List[Dict[str, str]]) -> Optional[str]:
        from app.core.config import settings

        if not settings.NVIDIA_API_KEY:
            return None
        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(
                base_url=settings.NVIDIA_BASE_URL,
                api_key=settings.NVIDIA_API_KEY,
                timeout=settings.LLM_TIMEOUT,
                max_retries=0,
            )
            last_error: Optional[Exception] = None
            for model in (settings.AI_MODEL, settings.AI_MODEL_FALLBACK):
                for attempt in range(2):
                    try:
                        response = await client.chat.completions.create(
                            model=model,
                            messages=messages,
                            temperature=0.2,
                            max_tokens=600,
                        )
                        return (response.choices[0].message.content or "").strip()
                    except Exception as e:  # 529/429 overloads, 5xx
                        last_error = e
                        retryable = getattr(e, "status_code", None) in (429, 500, 502, 503, 529)
                        logger.warning(
                            "NVIDIA attempt %d failed on %s (%s): %s",
                            attempt + 1,
                            model,
                            "retryable" if retryable else "non-retryable",
                            e,
                        )
                        if not retryable:
                            break
                        await asyncio.sleep(2 * (attempt + 1))
            logger.warning("NVIDIA NIM failed after retries: %s", last_error)
            return None
        except Exception as e:
            logger.warning("NVIDIA NIM refinement failed: %s", e)
            return None

    async def _ollama_refine(self, messages: List[Dict[str, str]]) -> Optional[str]:
        from app.core.config import settings

        try:
            import httpx

            async with httpx.AsyncClient(timeout=settings.LLM_TIMEOUT) as client:
                resp = await client.post(
                    f"{settings.OLLAMA_BASE_URL.rstrip('/')}/api/chat",
                    json={
                        "model": settings.OLLAMA_MODEL,
                        "messages": messages,
                        "stream": False,
                        "format": "json",
                        "keep_alive": "30m",
                    },
                )
                resp.raise_for_status()
                return (resp.json().get("message", {}).get("content") or "").strip()
        except Exception as e:
            logger.warning("Ollama refinement failed: %s", e)
            return None

    async def _llm_refine(self, prompt: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Ask the LLM (NVIDIA NIM, falling back to Ollama) to refine tool selection.

        Returns (parsed_json, provider_name). provider_name is None if no LLM available.
        """
        from app.core.config import settings

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a senior penetration testing planner. "
                    "You decide the exact Kali tools and phases for a VAPT engagement. "
                    "Prioritize EXPLOITATION over passive recon: include deep "
                    "exploitation tools (sqlmap --level/--risk, metasploit, commix, "
                    "hydra, dalfox, zap, flows, jwt, dom-xss) as soon as web "
                    "endpoints exist. Respond ONLY with valid JSON."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        providers: List[Tuple[str, Callable[[List[Dict[str, str]]], Awaitable[Optional[str]]]]] = []
        if settings.LLM_PROVIDER in ("auto", "ollama", "nvidia"):
            if settings.LLM_PROVIDER != "nvidia":
                # Ollama (qwen3) is the PRIMARY planner LLM; NVIDIA is secondary.
                providers.append(("Ollama", self._ollama_refine))
            providers.append(("NVIDIA", self._nvidia_refine))

        for name, call in providers:
            try:
                text = await call(messages)
            except Exception as e:
                logger.warning("%s refinement raised: %s", name, e)
                text = None
            if text:
                parsed = self._parse_json(text)
                if parsed is not None:
                    return parsed, name
        return None, None

    async def plan_scan(
        self,
        target: str,
        scan_type: VAPTScanType,
        target_info: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate the full phased VAPT plan with KB-grounded reasoning."""
        available = set(get_available_tools())

        phases: List[Dict[str, Any]] = []
        for phase_def in PHASE_DEFS:
            if phase_def["id"] == "ai_security" and scan_type not in (
                VAPTScanType.FULL, VAPTScanType.LLM,
            ):
                continue
            if scan_type == VAPTScanType.SSL and phase_def["id"] not in ("recon", "crypto"):
                continue
            if scan_type == VAPTScanType.NETWORK and phase_def["id"] not in ("recon", "crypto"):
                continue
            if scan_type == VAPTScanType.WEB and phase_def["id"] == "crypto":
                continue

            kb_snippets = await asyncio.to_thread(self._kb_search, phase_def["kb_query"])
            tools = []
            reason_futs = []
            for tool_id in phase_def["tools"]:
                if tool_id not in TOOLS_REGISTRY:
                    continue
                if tool_id not in available:
                    continue
                tool = TOOLS_REGISTRY[tool_id]
                reason_futs.append(
                    asyncio.to_thread(self._kb_search, TOOL_KB_QUERIES[tool_id], top_k=1)
                )
            reasons = await asyncio.gather(*reason_futs) if reason_futs else []
            for tool_id, reason in zip(
                [tid for tid in phase_def["tools"] if tid in available and tid in TOOLS_REGISTRY],
                reasons,
            ):
                tool = TOOLS_REGISTRY[tool_id]
                tools.append({
                    "id": tool_id,
                    "name": tool.name,
                    "description": tool.description,
                    "reason": reason[0] if reason else f"Standard {phase_def['name'].lower()} tool",
                })
            if not tools:
                continue
            phases.append({
                "id": phase_def["id"],
                "name": phase_def["name"],
                "description": phase_def["description"],
                "tools": tools,
                "kb_context": kb_snippets[:2],
            })

        plan = {
            "target": target,
            "scan_type": scan_type.value if scan_type else "auto",
            "target_type": target_info.get("type", "unknown"),
            "phases": phases,
            "tool_count": sum(len(p["tools"]) for p in phases),
            "strategy": "AI knowledge-base driven: tools selected per phase using 360-source semantic search",
        }

        llm_plan, provider = await self._llm_refine(
            "You are a senior penetration testing planner. Given the target "
            f"{target!r} (type {target_info.get('type')}), select the best Kali tools "
            "per VAPT phase from: nmap, masscan, dnsrecon, subfinder, nikto, nuclei, "
            "sqlmap, gobuster, ffuf, httpx, whatweb, wafw00f, arjun, commix, dalfox, "
            "hydra, sslscan, testssl, garak, api-surface, code-review, flows, dom-xss. "
            "For FULL scans include ALL scan types (network, web, API, SSL/TLS, "
            "container, AI/LLM security - garak) plus deeper application coverage "
            "with api-surface, code-review (static source review), flows (API "
            "business logic: BOLA, JWT, SQLi login, price tampering) and dom-xss "
            "(client-side DOM XSS). "
            "Return JSON {\"phases\":[{\"id\":\"recon|enumeration|vuln_scan|brute_force|crypto|ai_security\","
            "\"tools\":[\"nmap\",...]}]}. Only include tools above and phases relevant to the target type."
        )
        if llm_plan and isinstance(llm_plan, dict) and llm_plan.get("phases"):
            llm_order: Dict[str, List[str]] = {}
            for p in llm_plan["phases"]:
                pid = str(p.get("id", ""))
                tools = [t for t in p.get("tools", []) if t in TOOLS_REGISTRY and t in available]
                if pid:
                    llm_order.setdefault(pid, []).extend(tools)
            for phase in phases:
                preferred: List[str] = []
                for pid, tools in llm_order.items():
                    if pid == phase["id"] or phase["id"] in pid.split("|"):
                        preferred.extend(tools)
                if preferred:
                    tool_map = {t["id"]: t for t in phase["tools"]}
                    seen = set()
                    ordered = []
                    for tid in preferred:
                        if tid in tool_map and tid not in seen:
                            ordered.append(tool_map[tid])
                            seen.add(tid)
                    ordered += [t for t in phase["tools"] if t["id"] not in seen]
                    phase["tools"] = ordered
            plan["strategy"] = (
                f"AI/LLM refined plan ({provider or 'LLM'}) grounded in knowledge base"
            )

        return plan


_planner: Optional[PlannerAgent] = None


def get_planner() -> PlannerAgent:
    global _planner
    if _planner is None:
        _planner = PlannerAgent()
    return _planner
