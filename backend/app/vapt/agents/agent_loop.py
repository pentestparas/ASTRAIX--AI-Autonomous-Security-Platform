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
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple

from app.core.logging import get_logger
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

MAX_STEPS = int(os.environ.get("VAPT_AGENT_MAX_STEPS", "20"))
MIN_STEPS = int(os.environ.get("VAPT_AGENT_MIN_STEPS", "8"))
APPROVAL_TIMEOUT = int(os.environ.get("VAPT_APPROVAL_TIMEOUT", "300"))
OBSERVATION_LIMIT = int(os.environ.get("VAPT_AGENT_OBSERVATION_LIMIT", "12000"))

SYSTEM_PROMPT = """You are the autonomous VAPT (Vulnerability Assessment & Penetration Testing) agent for AstraIX.
You are conducting an authorized security engagement against the provided target.

Rules:
1. Pick ONE security tool per turn using the provided functions. The tools are
   phase-gated: recon tools (nmap, masscan, dnsrecon, subfinder) are available
   now. After a recon step completes, web tools unlock (httpx, nikto, gobuster,
   ffuf, nuclei...). After a web step, deep tools unlock (sqlmap, hydra, sslscan...).
2. Use the target as-is; do not invent targets. extra_args must be plain
   command-line flags, never shell metacharacters.
3. Tools marked [REQUIRES OPERATOR APPROVAL] will pause for a human decision.
   That is expected - proceed normally and describe why each is needed.
4. If no more testing is meaningful or you have sufficient evidence, reply with
   a FINAL REPORT as plain text starting with the line FINAL REPORT: followed by
   a concise summary (key findings by severity, confidence, and recommended
   next steps for the client). You may ONLY conclude once you have run at least
   MIN_STEPS distinct tools, attempted the deep phase (zap, sqlmap, metasploit,
   hydra...), and covered every unlocked phase. Early final reports will be
   rejected.
5. Never call a tool twice in a row with identical arguments.
6. Do not test unrelated targets or expand scope beyond the given target."""


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

    # ------------------------------------------------------- KB grounding

    def _kb_search(self, query: str, top_k: int = 3) -> List[str]:
        try:
            import sys

            sys.path.insert(0, "/app/knowledge-base")
            from search import get_knowledge_base

            kb = get_knowledge_base()
            results = kb.search(query, top_k=top_k)
            return [
                f"[{r['source']}] {r['text'][:300]}"
                for r in results
                if r.get("text")
            ]
        except Exception:
            return []

    async def _load_kb_context(
        self,
        target: str,
        target_info: Dict[str, Any],
    ) -> None:
        """Ground the agent with knowledge-base methodology snippets."""
        ttype = target_info.get("type", "web")
        query = (
            f"autonomous penetration testing methodology {ttype} web application "
            "SQL injection XSS API endpoint enumeration exploitation best practice"
        )
        try:
            snippets = await asyncio.to_thread(self._kb_search, query, 4)
            if snippets:
                self._kb_context = (
                    "Knowledge base guidance (use it to choose the most effective tools "
                    "and payload strategies):\n" + "\n".join(snippets[:4])
                )
        except Exception:
            self._kb_context = ""

    def _can_conclude(
        self,
        step_index: int,
        steps: List[StepRecord],
        completed_phases: set,
        pool: List[Any],
    ) -> Tuple[bool, str]:
        """Return (rejected, reason) when the model may NOT write a final
        report yet - enforces minimum tool diversity and deep-phase coverage."""
        distinct = len({s.tool_id for s in steps if s.decision == "ran"})
        if step_index < MIN_STEPS:
            return True, (
                f"You have only completed {step_index} steps. Run at least "
                f"{MIN_STEPS} steps before concluding."
            )
        if distinct < 3:
            return True, (
                f"You have only used {distinct} distinct tools. Use at least "
                f"3 different tools before concluding."
            )
        if "deep" not in completed_phases and any(
            t.phase == "deep" for t in pool
        ):
            return True, (
                "You have not attempted the deep phase yet (sqlmap, hydra, "
                "metasploit, zap, dalfox...). Run at least one deep-phase "
                "tool before concluding."
            )
        return False, ""

    # ------------------------------------------------------------- LLM calls

    async def _llm_turn(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
    ) -> Tuple[Optional[str], List[Dict[str, Any]]]:
        """Call the LLM with function tools; return (text, tool_calls).

        Prefers NVIDIA NIM (OpenAI-compatible), falls back to Ollama.
        Returns (None, []) when no provider is reachable.
        """
        from app.core.config import settings

        text: Optional[str] = None
        calls: List[Dict[str, Any]] = []

        if settings.LLM_PROVIDER in ("auto", "nvidia") and settings.NVIDIA_API_KEY:
            try:
                from openai import AsyncOpenAI

                client = AsyncOpenAI(
                    base_url=settings.NVIDIA_BASE_URL,
                    api_key=settings.NVIDIA_API_KEY,
                    timeout=settings.LLM_TIMEOUT,
                    max_retries=1,
                )
                response = await client.chat.completions.create(
                    model=settings.AI_MODEL,
                    messages=messages,
                    temperature=0.2,
                    max_tokens=900,
                    tools=tools or None,
                )
                msg = response.choices[0].message
                text = (msg.content or "").strip() or None
                for call in msg.tool_calls or []:
                    try:
                        arguments = json.loads(call.function.arguments or "{}")
                    except json.JSONDecodeError:
                        arguments = {}
                    calls.append({
                        "name": call.function.name,
                        "arguments": arguments,
                    })
                return text, calls
            except Exception as exc:
                logger.warning("Agent loop NVIDIA turn failed: %s", exc)

        if settings.LLM_PROVIDER in ("auto", "ollama"):
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
                    return text, calls
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

        await self._load_kb_context(target, target_info)

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
                        text, calls = await self._llm_turn(messages, _current_schemas())
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