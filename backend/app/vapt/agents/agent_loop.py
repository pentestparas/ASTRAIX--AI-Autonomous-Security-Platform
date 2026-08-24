"""
Autonomous VAPT Agent Loop (Phase 1)

RedAmon-inspired agentic workflow: instead of running a fixed tool script,
the LLM observes each tool's output and decides the next tool - phase-gated
(``recon`` -> ``web`` -> ``deep``) and operator-approved for dangerous tools.

Design:
  * Provider-agnostic tool calling - NVIDIA NIM (OpenAI-compatible) with an
    Ollama fallback, mirroring the PlannerAgent provider chain.
  * Phase gating enforced backend-side: recon tools available immediately,
    web unlocks after the first recon step, deep after the first web step.
  * Dangerous tools pause at an operator approval gate (ScanController) and
    publish ``tool_approval_requested`` events the UI renders.
  * Every step is recorded into the Neo4j attack graph as a ChainStep node
    (target --HAS_CHAIN_STEP--> step) so the agent's path is visual.
  * Falls back to the classic pipeline when no LLM is configured/reachable.
"""

import asyncio
import json
import os
import time
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple

from app.core.logging import get_logger
from app.vapt.agents.llm_usage import estimate_tokens, record_llm_call, time_tracked
from app.vapt.models import (
    VAPTFinding,
    VAPTScanResult,
    VAPTScanType,
    VAPTSeverity,
)
from app.vapt.tools import (
    AGENT_LOOP_CATEGORIES,
    PHASE_LABELS,
    PHASE_ORDER,
    get_agent_pool,
    get_tool,
    tool_openai_schema,
    validate_extra_args,
)

logger = get_logger(__name__)

# Tool IDs that count as real exploitation effort - the loop refuses to
# conclude until at least two of these have been executed (maximum exploitation).
_EXPLOIT_TOOLS = {
    "sqlmap",
    "metasploit",
    "commix",
    "hydra",
    "zap",
    "dalfox",
    "flows",
    "dom-xss",
    "nikto",
    "nuclei",
}

MAX_STEPS = int(os.environ.get("VAPT_AGENT_MAX_STEPS", "40"))
MIN_STEPS = int(os.environ.get("VAPT_AGENT_MIN_STEPS", "12"))
APPROVAL_TIMEOUT = int(os.environ.get("VAPT_APPROVAL_TIMEOUT", "300"))
OBSERVATION_LIMIT = int(os.environ.get("VAPT_AGENT_OBSERVATION_LIMIT", "16000"))

SYSTEM_PROMPT = """You are the autonomous VAPT (Vulnerability Assessment & Penetration Testing) agent for AstraIX.
You are conducting an authorized security engagement against the provided target. Your mission is MAXIMUM EXPLOITATION:
discover every exploitable vulnerability and prove impact. Verify everything you find.

Rules:
1. Pick ONE security tool per turn using the provided functions. The tools are
   phase-gated: recon tools (nmap, masscan, dnsrecon, subfinder) are available
   now. After a recon step completes, web tools unlock (httpx, nikto, gobuster,
   ffuf, nuclei...). After a web step, deep tools unlock (sqlmap, hydra, sslscan...).
2. Use the target as-is; do not invent targets. extra_args must be plain
   command-line flags, never shell metacharacters. Pass deep flags that increase
   thoroughness: sqlmap --level/--risk, gobuster larger wordlists, nuclei default
   templates, hydra with the default wordlists.
3. Ground every decision in the Knowledge Base guidance and KB observations in
   the context: cite them when choosing a tool or payload strategy. When the KB
   supplies payloads (SQLi, XSS, auth bypass, RCE), feed them through the tools'
   extra_args or the verifier's payload field to actively exploit targets.
3. Tools marked [REQUIRES OPERATOR APPROVAL] will pause for a human decision.
   That is expected - proceed normally and describe why each is needed.
4. EXPLOIT, DO NOT JUST RECON. Once you have web endpoints, go straight for the
   deep exploitation tools: metasploit, sqlmap, commix, hydra, zap, dalfox,
   flows (OAuth/flow abuse), jwt, dom-xss, nikto, nuclei. Prefer exploiting
   findings over re-running recon. If a tool finds nothing, move to the next
   exploitation tool - do not repeat tools with identical arguments.
5. Conclude with a FINAL REPORT as plain text starting with the line
   FINAL REPORT: followed by a concise summary (key findings by severity,
   confidence, exploit evidence, and recommended next steps for the client).
   You may ONLY conclude once you have run at least MIN_STEPS distinct tools,
   attempted the deep phase (zap, sqlmap, metasploit, hydra...), covered every
   unlocked phase, AND run every exploitation tool that could apply. Early
   final reports will be rejected.
6. Never call a tool twice in a row with identical arguments.
7. Do not test unrelated targets or expand scope beyond the given target."""


@dataclass
class StepRecord:
    """One agent-loop step (one tool execution attempt)."""

    index: int
    tool_id: str = ""
    tool_name: str = ""
    reason: str = ""
    decision: str = "skipped"  # ran | rejected | skipped | error
    findings_count: int = 0
    summary: str = ""
    error: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step": self.index,
            "tool": self.tool_id,
            "tool_name": self.tool_name,
            "reason": self.reason,
            "decision": self.decision,
            "findings_count": self.findings_count,
            "summary": self.summary[:400],
            "error": self.error[:200],
        }


class AgentLoop:
    """The autonomous tool-calling loop with phase + approval gating."""

    def __init__(
        self,
        executor: Any,
        controller: Any,
        publish: Callable[[str, str, Dict[str, Any]], Awaitable[None]],
        graph: Optional[Any] = None,
    ) -> None:
        self._executor = executor
        self._controller = controller
        self._publish = publish
        self._graph = graph
        self._kb_context: str = ""
        self._kb_observations: List[str] = []

    # ------------------------------------------------------- KB grounding

    TARGET_TYPE_QUERIES = {
        "url": (
            "web application penetration testing methodology OWASP top 10 "
            "enumeration injection XSS broken access control exploitation"
        ),
        "api": (
            "API security testing methodology OWASP API top 10 authentication "
            "authorization injection enumeration"
        ),
        "ip": (
            "network penetration testing methodology reconnaissance port scanning "
            "service enumeration exploitation"
        ),
        "domain": (
            "web application penetration testing methodology subdomain enumeration "
            "DNS recon attack surface mapping"
        ),
        "hostname": (
            "web application penetration testing methodology subdomain enumeration "
            "DNS recon attack surface mapping"
        ),
        "unknown": (
            "penetration testing methodology reconnaissance attack surface "
            "enumeration exploitation"
        ),
    }

    SCAN_TYPE_QUERIES = {
        VAPTScanType.LLM: (
            "AI LLM security testing OWASP LLM top 10 prompt injection "
            "jailbreak data poisoning model security"
        ),
        VAPTScanType.API: (
            "API security testing OWASP API top 10 methodology"
        ),
        VAPTScanType.SSL: (
            "SSL TLS penetration testing certificate cipher configuration audit"
        ),
        VAPTScanType.CONTAINER: (
            "container security scanning image vulnerabilities kubernetes"
        ),
    }

    def _kb_search(self, query: str, top_k: int = 3) -> List[str]:
        from app.vapt.agents.kb import kb_snippets

        return kb_snippets(query, top_k=top_k)

    async def _load_kb_context(
        self,
        target: str,
        target_info: Dict[str, Any],
        scan_type: VAPTScanType,
    ) -> None:
        """Ground the agent with methodology guidance from the knowledge base,
        specific to the detected target type and chosen scan type."""
        ttype = target_info.get("type", "unknown")
        queries = []
        queries.append(self.TARGET_TYPE_QUERIES.get(ttype, self.TARGET_TYPE_QUERIES["unknown"]))
        extra = self.SCAN_TYPE_QUERIES.get(scan_type)
        if extra:
            queries.append(extra)
        for query in queries:
            try:
                snippets = await asyncio.to_thread(self._kb_search, query, 3)
                if snippets:
                    self._kb_context += (
                        "Knowledge base guidance (use it to choose the most effective "
                        "tools and payload strategies):\n"
                        + "\n".join(snippets[:3])
                        + "\n"
                    )
            except Exception:
                continue

    async def _ground_observations(self, findings: List[VAPTFinding]) -> None:
        """Ground newly observed vuln classes in KB so the next tool decision
        exploits them (e.g. KB says deepen SQLi with sqlmap, not gobuster)."""
        if not findings:
            return
        seen = set()
        for f in findings[-3:]:
            key = (f.title or "")[:80]
            if key in seen:
                continue
            seen.add(key)
            query = f"{f.title} {f.vulnerability_type or ''} exploitation technique"
            try:
                snippets = await asyncio.to_thread(self._kb_search, query, 2)
            except Exception:
                continue
            for s in snippets[:2]:
                obs = f"KB guidance on observed '{f.title[:60]}': {s[:260]}"
                if obs not in self._kb_observations:
                    self._kb_observations.append(obs)

    def _can_conclude(
        self,
        step_index: int,
        steps: List[StepRecord],
        completed_phases: set,
        pool: List[Any],
    ) -> Tuple[bool, str]:
        """Return (rejected, reason) when the model may NOT write a final
        report yet - enforces minimum tool diversity, deep-phase coverage and
        exploitation coverage (maximum exploitation)."""
        distinct = len({s.tool_id for s in steps if s.decision == "ran"})
        if step_index < MIN_STEPS:
            return True, (
                f"You have only completed {step_index} steps. Run at least "
                f"{MIN_STEPS} steps before concluding."
            )
        if distinct < 5:
            return True, (
                f"You have only used {distinct} distinct tools. Use at least "
                f"5 different tools before concluding."
            )
        if "deep" not in completed_phases and any(
            t.phase == "deep" for t in pool
        ):
            return True, (
                "You have not attempted the deep phase yet (sqlmap, hydra, "
                "metasploit, zap, dalfox...). Run at least one deep-phase "
                "tool before concluding."
            )
        deep_ran = {
            s.tool_id for s in steps if s.decision == "ran" and s.tool_id in _EXPLOIT_TOOLS
        }
        if len(deep_ran) < 2:
            missing = sorted(_EXPLOIT_TOOLS - deep_ran)
            return True, (
                "Maximum exploitation is required: run at least 2 exploitation "
                "tools (sqlmap, metasploit, commix, hydra, zap, dalfox, flows, "
                f"jwt, dom-xss, nikto, nuclei). You have used {len(deep_ran)}. "
                f"Unused: {', '.join(missing)}."
            )
        return False, ""

    # ------------------------------------------------------------- LLM calls

    async def _llm_turn(
        self,
        scan_id: str,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
    ) -> Tuple[Optional[str], List[Dict[str, Any]]]:
        """Serialize against the matrix phase's LLM calls.

        The matrix phase and the agent loop run concurrently within a scan
        and share the same providers; a global asyncio lock keeps bursts from
        rate-limiting the NVIDIA NIM endpoint or starving the phase budget.
        """
        from app.vapt.agents.llm_lock import get_llm_lock

        async with get_llm_lock():
            return await self._llm_turn_locked(scan_id, messages, tools)

    async def _llm_turn_locked(
        self,
        scan_id: str,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
    ) -> Tuple[Optional[str], List[Dict[str, Any]]]:
        """Call the LLM with function tools; return (text, tool_calls).

        Provider order honors LLM_PROVIDER: ``ollama`` makes the local model
        primary with NVIDIA NIM as backup; ``auto``/``nvidia`` keep NVIDIA
        primary with Ollama as fallback. Each provider is tried at most once
        with no internal client retries, so a rate-limited or down provider
        fails fast and the agent degrades to the deterministic rotation
        instead of stalling a step for minutes.
        Returns (None, []) when no provider is reachable.
        """
        from app.core.config import settings

        nvidia_allowed = bool(settings.NVIDIA_API_KEY) and settings.LLM_PROVIDER != "ollama"
        ollama_allowed = bool(settings.OLLAMA_BASE_URL)

        for which in ("ollama", "nvidia") if settings.LLM_PROVIDER == "ollama" else ("nvidia", "ollama"):
            if which == "nvidia" and not nvidia_allowed:
                continue
            if which == "ollama" and not ollama_allowed:
                continue
            if which == "nvidia":
                text, calls = await self._llm_nvidia(scan_id, messages, tools)
            else:
                text, calls = await self._llm_ollama(scan_id, messages, tools)
            if text or calls:
                return text, calls
        return None, []

    async def _llm_nvidia(
        self,
        scan_id: str,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
    ) -> Tuple[Optional[str], List[Dict[str, Any]]]:
        from app.core.config import settings

        t0 = time.time()
        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(
                base_url=settings.NVIDIA_BASE_URL,
                api_key=settings.NVIDIA_API_KEY,
                timeout=settings.LLM_TIMEOUT,
                max_retries=0,
            )
            last_err: Optional[Exception] = None
            for model in (settings.AI_MODEL, settings.AI_MODEL_FALLBACK):
                try:
                    response = await client.chat.completions.create(
                        model=model,
                        messages=messages,
                        temperature=0.2,
                        max_tokens=900,
                        tools=tools or None,
                    )
                    break
                except Exception as exc:
                    last_err = exc
                    logger.warning(
                        "Agent loop NVIDIA turn failed on %s: %s", model, exc
                    )
            else:
                raise last_err  # type: ignore[misc]
            msg = response.choices[0].message
            text = (msg.content or "").strip() or None
            calls: List[Dict[str, Any]] = []
            for call in msg.tool_calls or []:
                try:
                    arguments = json.loads(call.function.arguments or "{}")
                except json.JSONDecodeError:
                    arguments = {}
                calls.append({
                    "name": call.function.name,
                    "arguments": arguments,
                })
            usage = response.usage
            tokens_in = int(usage.prompt_tokens) if usage else 0
            tokens_out = int(usage.completion_tokens) if usage else estimate_tokens(text)
            ok = bool(text or calls)
            record_llm_call(
                scan_id=scan_id,
                provider="NVIDIA",
                model=model,
                purpose="agent",
                tokens_in=tokens_in,
                tokens_out=tokens_out,
                ms=time_tracked(t0),
                ok=ok,
            )
            await self._publish(scan_id, "llm_call", {
                "provider": "NVIDIA",
                "model": model,
                "purpose": "agent",
                "ms": time_tracked(t0),
                "ok": ok,
            })
            if ok:
                return text, calls
            logger.warning("Agent loop NVIDIA returned empty - falling through")
        except Exception as exc:
            logger.warning("Agent loop NVIDIA turn failed: %s", exc)
        return None, []

    async def _llm_ollama(
        self,
        scan_id: str,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
    ) -> Tuple[Optional[str], List[Dict[str, Any]]]:
        from app.core.config import settings

        t0 = time.time()
        try:
            import httpx

            payload: Dict[str, Any] = {
                "model": settings.OLLAMA_MODEL,
                "messages": messages,
                "stream": False,
                "think": False,
            }
            if tools:
                # Ollama expects the full OpenAI-style tool wrapper,
                # and "format": "json" would serialize the tool call
                # into content instead of structured tool_calls.
                payload["tools"] = tools
            calls: List[Dict[str, Any]] = []
            async with httpx.AsyncClient(timeout=settings.LLM_TIMEOUT) as client:
                resp = await client.post(
                    f"{settings.OLLAMA_BASE_URL.rstrip('/')}/api/chat",
                    json=payload,
                )
                resp.raise_for_status()
                data = resp.json()
                msg = data.get("message", {})
                text = (msg.get("content") or "").strip() or None
                for call in msg.get("tool_calls") or []:
                    fn = call.get("function", {})
                    calls.append({
                        "name": fn.get("name", ""),
                        "arguments": json.loads(fn.get("arguments") or "{}")
                        if isinstance(fn.get("arguments"), str)
                        else (fn.get("arguments") or {}),
                    })
                usage = data.get("prompt_eval_count") or 0, data.get("eval_count") or 0
                ok = bool(text or calls)
                record_llm_call(
                    scan_id=scan_id,
                    provider="Ollama",
                    model=settings.OLLAMA_MODEL or "ollama",
                    purpose="agent",
                    tokens_in=usage[0],
                    tokens_out=estimate_tokens(text),
                    ms=time_tracked(t0),
                    ok=ok,
                )
                await self._publish(scan_id, "llm_call", {
                    "provider": "Ollama",
                    "model": settings.OLLAMA_MODEL or "ollama",
                    "purpose": "agent",
                    "ms": time_tracked(t0),
                    "ok": ok,
                })
                if ok:
                    return text, calls
                logger.warning(
                    "Agent loop Ollama returned empty"
                )
        except Exception as exc:
            logger.warning("Agent loop Ollama turn failed: %s", exc)
        return None, []

    # ------------------------------------------------------- context builder

    def _build_context(
        self,
        target: str,
        target_info: Dict[str, Any],
        steps: List[StepRecord],
        findings: List[VAPTFinding],
        allowed_phases: List[str],
    ) -> str:
        lines = [
            f"Target: {target} (type: {target_info.get('type', 'unknown')})",
            f"Unlocked phases: {', '.join(PHASE_LABELS[p] for p in allowed_phases)}",
            "",
        ]
        if self._kb_context:
            lines.append(self._kb_context)
            lines.append("")
        if self._kb_observations:
            lines.append("KB observations on findings so far:")
            lines.extend(self._kb_observations[-4:])
            lines.append("")
        lines.append("Steps so far:")
        for s in steps[-10:]:
            lines.append(
                f"  {s.index}. {s.tool_name or s.tool_id} [{s.decision}] "
                f"({s.findings_count} findings) - {s.summary[:120]}"
            )
        tool_uses: Dict[str, int] = {}
        for s in steps:
            if s.decision == "ran":
                tool_uses[s.tool_id or s.tool_name] = (
                    tool_uses.get(s.tool_id or s.tool_name, 0) + 1
                )
        if tool_uses:
            lines.append(
                "Tool usage so far: "
                + ", ".join(f"{k} x{v}" for k, v in tool_uses.items())
            )
            repeats = [k for k, v in tool_uses.items() if v >= 2]
            if repeats:
                lines.append(
                    f"Note: you already ran {', '.join(repeats)} more than once "
                    "without yielding findings - choose a DIFFERENT tool next."
                )
        if steps:
            lines.append("")

        sev_counts: Dict[str, int] = {}
        for f in findings:
            sev = f.severity.value
            sev_counts[sev] = sev_counts.get(sev, 0) + 1
        lines.append(
            f"Findings so far: {len(findings)} "
            f"({', '.join(f'{k}={v}' for k, v in sorted(sev_counts.items()))})"
        )
        lines.append("Recent findings (top 12, title | severity | target | port):")
        for f in findings[-12:]:
            lines.append(
                f"  - {f.title[:110]} | {f.severity.value} | {f.host or f.target} | {f.port or ''}"
            )

        ctx = "\n".join(lines)
        return ctx[:OBSERVATION_LIMIT]

    # ------------------------------------------------------------- execution

    async def _record_step(
        self,
        scan_id: str,
        target_id: str,
        step: StepRecord,
        args: Dict[str, Any],
    ) -> None:
        """Persist the step into the Neo4j attack graph (best-effort)."""
        if not self._graph:
            return
        try:
            await self._graph.add_chain_step(
                target_id=target_id,
                scan_id=scan_id,
                step_index=step.index,
                tool_name=step.tool_name or step.tool_id,
                args=args,
                decision=step.decision,
                success=step.decision == "ran" and not step.error,
                summary=step.summary,
            )
        except Exception as exc:
            logger.warning("Agent step graph record failed: %s", exc)

    async def run(
        self,
        scan_id: str,
        target: str,
        target_info: Dict[str, Any],
        scan_type: VAPTScanType,
    ) -> Optional[Tuple[List[StepRecord], List[VAPTFinding]]]:
        """Run the autonomous loop. Returns ``(steps, findings)``, or None on
        LLM failure (the orchestrator then falls back to the classic pipeline)."""
        pool = get_agent_pool(scan_type)
        # Git-repo secret scanners are useless against live web apps (they
        # clone the target URL); keep them only for repo-style targets.
        if target.startswith(("http://", "https://")):
            pool = [
                t for t in pool
                if t.id not in {"gitleaks", "trufflehog", "semgrep", "bandit"}
            ]
        pool_tools: Dict[str, Any] = {}
        for tool in pool:
            pool_tools[tool.id] = tool
        if not pool_tools:
            logger.info("Agent loop: empty tool pool for %s", scan_type)
            return None

        target_id = f"target:{target}"
        findings: List[VAPTFinding] = []
        steps: List[StepRecord] = []
        allowed_phases = ["recon"]
        # Scan types with no recon tools (e.g. code review) must not wait for
        # a recon step to unlock their phases.
        if not any(t.phase == "recon" for t in pool):
            allowed_phases = sorted({t.phase for t in pool})
        completed_phases: set[str] = set()

        def _current_schemas() -> List[Dict[str, Any]]:
            return [
                tool_openai_schema(t)
                for t in pool
                if t.phase in allowed_phases
            ]

        await self._publish(scan_id, "agent_loop_started", {
            "target": target,
            "scan_type": scan_type.value,
            "max_steps": MAX_STEPS,
            "tools": [t.id for t in pool],
        })

        await self._load_kb_context(target, target_info, scan_type)

        # When the LLM stays down across steps, switch to a pure deterministic
        # rotation instead of burning 3 retry attempts (and ~2min of sleeps)
        # on EVERY step. Keeps a flaky Ollama from starving the scan budget.
        llm_down_streak = 0

        def _rotate_tool() -> Tuple[Optional[str], Dict[str, Any]]:
            """Pick the next unused tool from the unlocked phases."""
            fallback = [
                t for t in pool
                if t.phase in allowed_phases
                and t.id != "sqlmap"
            ]
            ran = {s.tool_id for s in steps}
            unused = [t for t in fallback if t.id not in ran]
            pick = (unused or fallback)[0] if fallback else None
            if pick is None:
                return None, {}
            return pick.id, {}

        try:
            for step_index in range(1, MAX_STEPS + 1):
                try:
                    await self._controller.checkpoint(scan_id)
                except Exception:
                    raise

                await self._publish(scan_id, "agent_step_started", {
                    "step": step_index,
                    "message": "Agent deciding next tool",
                })

                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": self._build_context(
                            target, target_info, steps, findings, allowed_phases
                        ),
                    },
                ]
                step = StepRecord(index=step_index)

                # Resolve the tool choice, retrying with backoff when the model
                # is briefly unavailable, then falling back to a deterministic
                # tool rotation so a flaky LLM never starves the scan.
                tool_id = ""
                args: Dict[str, Any] = {}
                final_report = False
                if llm_down_streak >= 2:
                    # LLM has been down for consecutive steps - rotate directly.
                    tool_id, args = _rotate_tool()
                    if tool_id:
                        logger.warning(
                            "Agent loop: LLM down streak %d - rotating to %s",
                            llm_down_streak, tool_id,
                        )
                    else:
                        logger.warning(
                            "Agent loop: no fallback tool available in rotation"
                        )
                    final_report = not tool_id
                else:
                    tool_id = ""
                    args = {}
                    for attempt in range(3):
                        text, calls = await self._llm_turn(scan_id, messages, _current_schemas())
                        if not text and not calls:
                            llm_down_streak += 1
                            logger.warning(
                                "Agent loop: LLM unavailable (attempt %d/3) - retrying",
                                attempt + 1,
                            )
                            if attempt < 2:
                                await asyncio.sleep(5 * (attempt + 1))
                                continue
                            # Deterministic fallback: rotate through the unlocked pool
                            # (prefer tools not run yet) so the scan still executes.
                            tool_id, args = _rotate_tool()
                            if tool_id:
                                logger.warning(
                                    "Agent loop: using deterministic fallback tool %s",
                                    tool_id,
                                )
                            break

                    if calls:
                        llm_down_streak = 0
                        tool_id = str(calls[0].get("name", ""))
                        args = calls[0].get("arguments") or {}
                    else:
                        # Plain-text response - look for a JSON decision or FINAL REPORT.
                        body = (text or "").strip()
                        if body.upper().startswith("FINAL REPORT"):
                            rejected, reason = self._can_conclude(
                                step_index, steps, completed_phases, pool
                            )
                            if rejected:
                                messages.append({
                                    "role": "assistant",
                                    "content": body[:400],
                                })
                                messages.append({
                                    "role": "user",
                                    "content": (
                                        f"Final report rejected: {reason} "
                                        "Continue the engagement by choosing "
                                        "another tool."
                                    ),
                                })
                                continue
                            await self._publish(scan_id, "agent_final_report", {
                                "step": step_index,
                                "summary": body[:2000],
                            })
                            final_report = True
                            break
                        try:
                            decision = json.loads(body[body.find("{"): body.rfind("}") + 1])
                            tool_id = str(
                                decision.get("next_tool")
                                or decision.get("tool")
                                or decision.get("tool_id")
                                or decision.get("tool_name")
                                or ""
                            )
                            args = decision.get("args") or {}
                        except (json.JSONDecodeError, ValueError):
                            rejected, reason = self._can_conclude(
                                step_index, steps, completed_phases, pool
                            )
                            if rejected:
                                messages.append({
                                    "role": "assistant",
                                    "content": body[:400],
                                })
                                messages.append({
                                    "role": "user",
                                    "content": (
                                        f"Unparseable reply; final report rejected: "
                                        f"{reason} Continue the engagement by "
                                        "choosing another tool."
                                    ),
                                })
                                continue
                            await self._publish(scan_id, "agent_final_report", {
                                "step": step_index,
                                "summary": body[:2000],
                            })
                            final_report = True
                            break

                    if tool_id not in pool_tools:
                        messages.append({
                            "role": "assistant",
                            "content": text or (
                                json.dumps({"next_tool": tool_id, "args": args})
                                if tool_id else "No tool selected"
                            ),
                        })
                        messages.append({
                            "role": "user",
                            "content": (
                                f"Your previous turn did not select a valid tool "
                                f"(got: '{tool_id}'). The available tools are: "
                                f"{', '.join(sorted(pool_tools))}. Choose exactly one "
                                f"from that list now."
                            ),
                        })

                if final_report:
                    break

                tool = pool_tools.get(tool_id)
                if not tool:
                    step.decision = "skipped"
                    step.reason = f"Unknown or unavailable tool: {tool_id}"
                    steps.append(step)
                    await self._publish(scan_id, "agent_step", step.to_dict())
                    continue

                target_arg = str(args.get("target") or target)
                extra_args = str(args.get("extra_args") or "")
                if not validate_extra_args(extra_args):
                    step.tool_id = tool_id
                    step.tool_name = tool.name
                    step.decision = "skipped"
                    step.reason = "Rejected unsafe extra_args"
                    steps.append(step)
                    await self._publish(scan_id, "agent_step", step.to_dict())
                    continue

                step.tool_id = tool_id
                step.tool_name = tool.name
                step.reason = str(args.get("reason", ""))

                # ---- phase gate (backend-enforced)
                if tool.phase not in allowed_phases:
                    step.decision = "skipped"
                    step.reason = f"Phase {tool.phase} not unlocked"
                    steps.append(step)
                    await self._publish(scan_id, "agent_step", step.to_dict())
                    continue

                # ---- dangerous-tool approval gate
                if tool.dangerous:
                    approval_id = await self._controller.request_tool_approval(
                        scan_id,
                        tool_id,
                        tool.name,
                        {"target": target_arg, "extra_args": extra_args},
                        reason=step.reason or f"Agent requested {tool.name}",
                    )
                    decision = await self._controller.await_approval(
                        scan_id, approval_id, timeout=float(APPROVAL_TIMEOUT)
                    )
                    if decision is None:
                        step.decision = "skipped"
                        step.reason = "Approval timed out or scan stopped"
                        steps.append(step)
                        await self._publish(scan_id, "agent_step", step.to_dict())
                        continue
                    if not decision:
                        step.decision = "rejected"
                        step.reason = "Operator rejected execution"
                        steps.append(step)
                        await self._publish(scan_id, "agent_step", step.to_dict())
                        continue

                await self._publish(scan_id, "tool_started", {
                    "tool": tool_id,
                    "command": tool.command,
                })

                tool_findings, output, error = await self._executor.run_agent_tool(
                    tool_id, target_arg, extra_args
                )

                if error:
                    step.decision = "error"
                    step.error = error
                    step.summary = f"{tool.name} failed: {error}"
                else:
                    step.decision = "ran"
                    step.findings_count = len(tool_findings)
                    sev_high = sum(
                        1 for f in tool_findings if f.severity in (VAPTSeverity.CRITICAL, VAPTSeverity.HIGH)
                    )
                    if tool_findings:
                        step.summary = (
                            f"{tool.name} returned {len(tool_findings)} findings"
                            f" ({sev_high} critical/high)"
                        )
                    else:
                        # Include a short raw-output excerpt so the next decision
                        # is grounded in the actual tool output.
                        excerpt = (output or "").strip().replace("\n", " ")[:260]
                        step.summary = (
                            f"{tool.name} completed with no parsed findings. "
                            f"Output: {excerpt}" if excerpt
                            else f"{tool.name} completed with no findings"
                        )
                    findings.extend(tool_findings)
                    await self._ground_observations(tool_findings)
                    # Re-running a tool (or repeated scans) can yield duplicate
                    # findings - keep a single canonical copy per (title, desc,
                    # target) so the report stays clean.
                    seen_f = {}
                    for f in findings:
                        seen_f[(f.title, f.description, f.target)] = f
                    findings = list(seen_f.values())
                    completed_phases.add(tool.phase)

                await self._publish(scan_id, "tool_finished", {
                    "tool": tool_id,
                    "findings_count": len(tool_findings) if not error else 0,
                })
                for f in tool_findings[:25]:
                    await self._publish(scan_id, "finding_found", f.to_dict())

                steps.append(step)
                await self._publish(scan_id, "agent_step", step.to_dict())
                await self._record_step(scan_id, target_id, step, args)

                # ---- phase unlock
                next_unlock = None
                if "recon" in completed_phases and "web" not in allowed_phases:
                    next_unlock = "web"
                elif "web" in completed_phases and "deep" not in allowed_phases:
                    next_unlock = "deep"
                if next_unlock:
                    allowed_phases.append(next_unlock)
                    await self._publish(scan_id, "agent_phase_unlocked", {
                        "phase": next_unlock,
                        "label": PHASE_LABELS[next_unlock],
                        "tools": [
                            t.id for t in pool
                            if t.phase == next_unlock and t.agent_visible
                        ],
                    })

        finally:
            # Preserve partial results so a timed-out/aborted loop still
            # contributes findings to the final report (merged by the
            # orchestrator when it falls back to the classic pipeline).
            try:
                self._controller.set_agent_partial(scan_id, steps, findings)
            except Exception:
                pass

        await self._publish(scan_id, "agent_loop_done", {
            "steps": len(steps),
            "findings": len(findings),
            "phases_completed": sorted(completed_phases),
        })
        return steps, findings

    async def run_result(
        self,
        scan_id: str,
        target: str,
        target_info: Dict[str, Any],
        scan_type: VAPTScanType,
        request: Any,
    ) -> VAPTScanResult:
        """Full-run entry point returning a VAPTScanResult."""
        from datetime import datetime

        from app.vapt.models import VAPTScanResult

        result = VAPTScanResult(
            request=request,
            status="completed",
            started_at=datetime.utcnow(),
        )
        try:
            steps, findings = await self.run(scan_id, target, target_info, scan_type)
            result.findings = findings or []
            result.tool_results["agent_loop"] = {
                "steps": [s.to_dict() for s in (steps or [])],
                "steps_count": len(steps or []),
                "findings": len(result.findings),
                "status": "ok",
            }
        except Exception as exc:
            logger.error("Agent loop failed: %s", exc)
            result.status = "failed"
            result.errors.append(str(exc))
        result.finalize(result.status)
        return result


_loop: Optional[AgentLoop] = None


def get_agent_loop(
    executor: Any,
    controller: Any,
    publish: Callable[[str, str, Dict[str, Any]], Awaitable[None]],
    graph: Optional[Any] = None,
) -> AgentLoop:
    return AgentLoop(executor, controller, publish, graph)


def agent_loop_supported(scan_type: VAPTScanType) -> bool:
    return scan_type in AGENT_LOOP_CATEGORIES and bool(get_agent_pool(scan_type))