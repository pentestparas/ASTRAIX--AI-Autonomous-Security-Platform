"""
Test Matrix Agent

The LLM-driven exploitation test matrix: given the mined web surface
(bundle endpoints), target info and KB grounding, the LLM generates a
prioritized list of {endpoint, method, attack_type, payload,
expected_result} probes. The orchestrator executes each entry (HTTP
probes via the Kali curl runner, tool entries via run_agent_tool) and
captures PoC evidence into findings - mirroring the validated engagement
workflow (recon -> matrix -> exploit -> PoC -> report).

Entries are validated server-side so the LLM cannot escape the target
scope or emit OS-destructive payloads.
"""

import asyncio
import json
import re
import shlex
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple

from app.core.logging import get_logger
from app.vapt.models import VAPTSeverity, VAPTFinding

logger = get_logger(__name__)

_STATUS_MARKER = "---HTTP_STATUS:"

ALLOWED_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"}
MAX_ENTRIES = 16
MAX_PAYLOAD_LEN = 500

# Block OS-destructive / out-of-scope payloads before they reach the runner.
_DENY_RE = re.compile(
    r"(rm\s+-\s*rf|mkfs\.[a-z]+|dd\s+if=|\bshutdown\b|\breboot\b|:\(\)\s*\{|fork\s*bomb|"
    r"\bwget\b.*\|\s*(?:bash|sh)\b|curl\s+.*\|\s*(?:bash|sh)\b|\bchmod\s+-R\s+777\s+/)",
    re.IGNORECASE,
)

# Positive signals keyed by attack-type keyword (title/type match).
_SIGNAL_PATTERNS: List[Tuple[str, re.Pattern]] = [
    (r"sqli|sql\s*injection", re.compile(r"SQL|sqlite|unterminated|syntax error|near \"|foreign key|constraint", re.I)),
    (r"xss", re.compile(r"<script|onerror=|onload=|javascript:|alert\(")),
    (r"prompt", re.compile(r"confidential|discount.*\d+|coupon|internal|system prompt|instructions", re.I)),
    (r"idor|access control|authorization", re.compile(r"\b200\b|\border\b|account|address", re.I)),
    (r"auth|login|brute", re.compile(r"token|jwt|session|200", re.I)),
    (r"path traversal|traversal", re.compile(r"root:|etc/passwd|\.\./", re.I)),
    (r"ssrf", re.compile(r"ECONNREFUSED|timed out|127\.0\.0\.1|internal", re.I)),
    (r"error|disclosure", re.compile(r"traceback|stack|exception|error", re.I)),
]

SCAN_TYPE_KB_QUERIES = {
    "web": "web application penetration testing OWASP top 10 injection XSS broken access control",
    "api": "API penetration testing REST endpoint attacks BOLA IDOR JWT SQL injection",
    "full": "full penetration test web API network AI LLM security test matrix exploitation",
    "llm": "LLM security prompt injection jailbreak OWASP LLM top 10 chatbot",
    "network": "network penetration test service exploitation",
    "ssl": "TLS SSL misconfiguration certificate audit",
    "container": "container security misconfiguration docker kubernetes",
}


class MatrixAgent:
    """LLM test-matrix generation and PoC execution support."""

    # ------------------------------------------------------------------ LLM

    async def _nvidia_llm(self, messages: List[Dict[str, str]]) -> Tuple[Optional[str], Optional[str]]:
        """NVIDIA NIM call; returns (text, model_name). Primary model for
        LLM-assisted analysis is AI_MATRIX_MODEL (deepseek-v4-flash), with
        minimax-m3 / fallback tried in order. Transport errors (no HTTP
        status) are retried like 429/5xx."""
        from app.core.config import settings

        if not settings.NVIDIA_API_KEY:
            return None, None
        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(
                base_url=settings.NVIDIA_BASE_URL,
                api_key=settings.NVIDIA_API_KEY,
                timeout=settings.LLM_TIMEOUT,
                max_retries=0,
            )
            models: List[str] = []
            for m in (settings.AI_MATRIX_MODEL, settings.AI_MODEL, settings.AI_MODEL_FALLBACK):
                if m and m not in models:
                    models.append(m)
            for model in models:
                for attempt in range(2):
                    try:
                        response = await client.chat.completions.create(
                            model=model,
                            messages=messages,
                            temperature=0.2,
                            max_tokens=1500,
                        )
                        return (response.choices[0].message.content or "").strip(), model
                    except Exception as e:
                        status = getattr(e, "status_code", None)
                        retryable = status in (429, 500, 502, 503, 529) or status is None
                        logger.warning(
                            "NVIDIA matrix attempt %d failed on %s (%s): %s",
                            attempt + 1, model,
                            "retryable" if retryable else "non-retryable",
                            e,
                        )
                        if not retryable:
                            break
                        await asyncio.sleep(2 * (attempt + 1))
            return None, None
        except Exception as e:
            logger.warning("NVIDIA matrix LLM failed: %s", e)
            return None, None

    async def _ollama_llm(self, messages: List[Dict[str, str]]) -> Optional[str]:
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
            logger.warning("Ollama matrix LLM failed: %s", e)
            return None

    async def _llm_json(self, prompt: str) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
        """Ask the LLM (Ollama primary, NVIDIA secondary) for a JSON array."""
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a senior penetration tester designing an exploitation test "
                    "matrix for an AUTHORIZED engagement. Generate precise, realistic "
                    "payloads targeting ONLY the given endpoints. Respond ONLY with a "
                    "JSON array, never markdown."
                ),
            },
            {"role": "user", "content": prompt},
        ]
        providers: List[Tuple[str, Callable[[List[Dict[str, str]]], Awaitable[Any]]]] = []
        from app.core.config import settings

        # For the LLM-assisted analysis (matrix) phase, NVIDIA (deepseek-v4)
        # is PRIMARY when a key exists - it produces sharper JSON payload
        # matrices - with Ollama qwen3 as the local fallback.
        if settings.LLM_PROVIDER in ("auto", "ollama", "nvidia"):
            if settings.NVIDIA_API_KEY:
                providers.append(("NVIDIA", self._nvidia_llm))
            if settings.LLM_PROVIDER != "nvidia":
                providers.append(("Ollama", self._ollama_llm))

        for name, call in providers:
            try:
                result = await call(messages)
            except Exception as e:
                logger.warning("%s matrix LLM raised: %s", name, e)
                result = None
            text: Optional[str] = None
            model: Optional[str] = None
            if isinstance(result, tuple):
                text, model = result
            elif isinstance(result, str):
                text = result
            if text:
                parsed = self._parse_json_list(text)
                if parsed is not None:
                    return parsed, f"{name}:{model}" if model else name
                logger.warning("%s matrix LLM returned unparseable content: %.200s",
                               name, text.replace("\n", " "))
        return None, None

    @staticmethod
    def _parse_json_list(text: str) -> Optional[List[Dict[str, Any]]]:
        if not text:
            return None
        text = text.strip()
        start, end = text.find("["), text.rfind("]")
        if start == -1 or end == -1:
            return None
        try:
            data = json.loads(text[start:end + 1])
        except Exception:
            return None
        if isinstance(data, dict):
            for key in ("matrix", "entries", "tests", "steps"):
                if isinstance(data.get(key), list):
                    data = data[key]
                    break
            else:
                return None
        return data if isinstance(data, list) else None

    # ------------------------------------------------------------ Validation

    def _validate_entry(self, raw: Dict[str, Any], base_url: str) -> Optional[Dict[str, Any]]:
        if not isinstance(raw, dict):
            return None
        endpoint = str(raw.get("endpoint") or "").strip()
        if not endpoint.startswith("/"):
            return None
        method = str(raw.get("method") or "GET").upper()
        if method not in ALLOWED_METHODS:
            return None
        attack_type = str(raw.get("attack_type") or "").strip()
        if not attack_type:
            return None

        params = raw.get("params") or {}
        json_body = raw.get("json_body")
        payload_text = json.dumps({"params": params, "json_body": json_body})
        if _DENY_RE.search(payload_text):
            logger.warning("Matrix entry dropped (destructive payload): %s", endpoint)
            return None
        if len(payload_text) > MAX_PAYLOAD_LEN * 2:
            return None

        priority = str(raw.get("priority") or "medium").lower()
        if priority not in ("high", "medium", "low"):
            priority = "medium"

        tool = str(raw.get("tool") or "").strip()

        return {
            "id": str(raw.get("id") or f"m{abs(hash(endpoint + attack_type + payload_text)) % 100000}"),
            "endpoint": endpoint,
            "method": method,
            "attack_type": attack_type,
            "params": params if isinstance(params, dict) else {},
            "json_body": json_body,
            "expected_result": str(raw.get("expected_result") or ""),
            "priority": priority,
            "tool": tool,
        }

    # ------------------------------------------------------------- Generation

    async def generate_matrix(
        self,
        target: str,
        scan_type: str,
        target_info: Dict[str, Any],
        surface: Dict[str, Any],
        kb_context: Optional[List[str]] = None,
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """Build the validated exploitation test matrix for the target."""
        base = target if target.startswith(("http://", "https://")) else f"http://{target}"
        endpoints = surface.get("endpoints") or []
        hints = ", ".join(surface.get("hints") or [])
        kb_text = "\n".join((kb_context or [])[:2]) or "no KB context"

        prompt = (
            f"Target: {base} (type {target_info.get('type')}, scan {scan_type}).\n"
            f"Tech hints: {hints or 'unknown'}.\n"
            f"Discovered endpoints:\n" + ("\n".join(f"- {e}" for e in endpoints[:40]) if endpoints else "- none (design own probes on likely paths)")
            + f"\n\nKnowledge base grounding:\n{kb_text}\n\n"
            "Design an exploitation test matrix for these endpoints. For each entry return: "
            '{"id": "m1", "endpoint": "/path", "method": "GET|POST|...", "attack_type": "SQLi|XSS|IDOR|...", '
            '"params": {"q": "payload"}, "json_body": {...} or null, '
            '"expected_result": "what indicates the vuln", "priority": "high|medium|low"}. '
            "Rules: params carry query/form values, json_body carries the JSON body for POST/PUT/PATCH. "
            "Use real payloads (SQL syntax errors, quote breaking, XSS script tags, IDOR ids, prompt-injection "
            "instructions for chatbot endpoints). Max 10 entries. Cover the most likely OWASP issues for "
            f"scan type {scan_type}."
        )

        raw_entries, provider = await self._llm_json(prompt)
        if not raw_entries:
            return [], provider

        entries: List[Dict[str, Any]] = []
        for raw in raw_entries:
            if len(entries) >= MAX_ENTRIES:
                break
            entry = self._validate_entry(raw, base)
            if entry:
                entries.append(entry)
        if not entries:
            logger.warning("Matrix LLM returned no valid entries (%s)", provider or "LLM")
        return entries, provider

    # ------------------------------------------------------------ Classification

    @staticmethod
    def classify_entry(
        entry: Dict[str, Any],
        status: int,
        body: str,
        payload_values: List[str],
        output: str = "",
    ) -> Tuple[bool, str]:
        """Heuristic positive-signal check for an HTTP matrix entry.

        Returns (suspicious, reason).
        """
        haystack = " ".join([entry.get("attack_type", ""), body[:4000], output[:4000]])
        for kind, pattern in _SIGNAL_PATTERNS:
            if re.search(kind, haystack) and pattern.search(haystack):
                return True, f"{kind} signal matched in response"
        if status >= 500:
            return True, f"server error status {status}"
        dangerous = ("<script", "onerror=", "javascript:", "'", '"')
        reflected = [p for p in payload_values if p and any(tok in p for tok in dangerous) and p in body]
        if reflected:
            return True, "payload reflected unescaped in response"
        return False, ""

    # --------------------------------------------------------------- Attack chain

    async def build_attack_chain(self, findings: List[VAPTFinding]) -> Dict[str, Any]:
        """LLM synthesis of the findings into an attack-chain narrative."""
        if not findings:
            return {"summary": "", "steps": []}

        lines = [
            f"- [{f.severity.value}] {f.title} ({f.vulnerability_type or 'unknown'}): {f.description[:180]}"
            for f in findings[:15]
        ]
        prompt = (
            "Given these confirmed findings from an authorized pentest, reconstruct the most plausible "
            "attack chain an attacker would use (e.g. recon -> weak auth -> admin -> data exfiltration):\n"
            + "\n".join(lines)
            + "\n\nReturn JSON {\"summary\": \"2-3 sentence executive narrative\", "
            '"steps": [{"order": 1, "from": "unauthenticated", "to": "admin", '
            '"via": "JWT alg:none forgery", "technique": "JWT bypass", "finding_ref": "title or n/a"}]}. '
            "Max 6 steps. Respond ONLY with JSON."
        )
        raw, provider = await self._llm_json(prompt)
        if not isinstance(raw, list):
            return {"summary": "", "steps": []}
        steps = [
            {
                "order": int(s.get("order", i + 1)),
                "from": str(s.get("from") or "attacker"),
                "to": str(s.get("to") or ""),
                "via": str(s.get("via") or ""),
                "technique": str(s.get("technique") or ""),
                "finding_ref": str(s.get("finding_ref") or ""),
            }
            for i, s in enumerate(raw[:6])
            if isinstance(s, dict) and s.get("to")
        ]
        summary = ""
        for i, s in enumerate(steps):
            summary += f"{s['order']}. {s['from']} -> {s['to']} via {s['via']} ({s['technique']}); "
        return {"summary": summary.rstrip("; ") or (steps[0]["via"] if steps else ""), "steps": steps}

    @staticmethod
    def severity_for(priority: str) -> VAPTSeverity:
        return {
            "high": VAPTSeverity.HIGH,
            "medium": VAPTSeverity.MEDIUM,
            "low": VAPTSeverity.LOW,
        }.get(priority, VAPTSeverity.MEDIUM)


_matrix_agent: Optional[MatrixAgent] = None


def get_matrix_agent() -> MatrixAgent:
    global _matrix_agent
    if _matrix_agent is None:
        _matrix_agent = MatrixAgent()
    return _matrix_agent


def build_curl_command(entry: Dict[str, Any], base_url: str) -> str:
    """Build the Kali curl probe for one matrix entry.

    GET entries encode params into the query string (-G --data-urlencode),
    others send form-encoded params (--data-urlencode) or a JSON body.
    Output ends with the status marker line so the probe can be parsed.
    """
    url = base_url.rstrip("/") + entry["endpoint"]
    method = entry.get("method", "GET")
    params = entry.get("params") or {}
    json_body = entry.get("json_body")

    cmd = ["curl", "-s", "-k", "-L", "-m", "15", "-w", "\\n" + _STATUS_MARKER + "%{http_code}"]
    if method == "GET":
        if params:
            cmd.append("-G")
            for k, v in params.items():
                cmd += ["--data-urlencode", f"{k}={v}"]
    else:
        cmd += ["-X", method]
        if json_body is not None:
            cmd += ["-H", "Content-Type: application/json",
                    "--data", json.dumps(json_body, separators=(",", ":"), ensure_ascii=False)]
        elif params:
            for k, v in params.items():
                cmd += ["--data-urlencode", f"{k}={v}"]
    cmd.append(shlex.quote(url))
    return " ".join(cmd)


def parse_probe_output(output: str) -> Tuple[int, str]:
    """Split a probe output into (http_status, body)."""
    if not output:
        return 0, ""
    marker_idx = output.rfind(_STATUS_MARKER)
    if marker_idx == -1:
        return 0, output[-4000:]
    status_str = output[marker_idx + len(_STATUS_MARKER):].strip()
    try:
        status = int(status_str.split()[0])
    except (ValueError, IndexError):
        status = 0
    return status, output[:marker_idx][-4000:]
