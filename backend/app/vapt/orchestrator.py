"""
VAPT AI Orchestrator

AI-powered tool selection and scan coordination.
Analyzes target and selects appropriate tools.
"""

import asyncio
import hashlib
import json
import os
import re
import time
from datetime import datetime
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple
from uuid import UUID, uuid4

from app.vapt.models import VAPTFinding, VAPTSeverity, VAPTScanRequest, VAPTScanResult, VAPTScanType, VAPTTarget
from app.vapt.executor import get_vapt_executor
from app.vapt.adapters.registry import get_enabled_adapters
from app.vapt.agents import ResearcherAgent, VerifierAgent
from app.vapt.agents.kb import kb_snippets, kb_context_for_finding, kb_ready
from app.vapt.agents.planner import get_planner
from app.vapt.agents.recon import mine_web_surface
from app.vapt.agents.matrix import MatrixAgent, get_matrix_agent, build_curl_command, parse_probe_output
from app.vapt.agents.llm_usage import llm_usage_snapshot, reset_llm_usage
from app.vapt.control import ScanStoppedError, get_scan_controller
from app.vapt.progress import publish_scan_event, get_progress_bus
from app.recon_orchestrator.orchestrator import ReconOrchestrator
from app.core.logging import get_logger

logger = get_logger(__name__)

# KB grounding queries per target type - the whole workflow (planning, agent
# decisions, risk, summary) starts from these methodology snippets.
TARGET_KB_QUERIES: Dict[str, str] = {
    "url": (
        "web application penetration testing methodology OWASP top 10 "
        "enumeration injection XSS broken access control exploitation"
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

SCAN_TYPE_KB_QUERIES: Dict[str, str] = {
    "llm": (
        "AI LLM security testing OWASP LLM top 10 prompt injection "
        "jailbreak data poisoning model security"
    ),
    "api": (
        "API security testing OWASP API top 10 methodology"
    ),
    "ssl": (
        "SSL TLS penetration testing certificate cipher configuration audit"
    ),
    "container": (
        "container security scanning image vulnerabilities kubernetes"
    ),
}

KEV_MARKERS = (
    "known exploited", "kev", "cisa catalog", "cisa ",
    "actively exploited", "exploited in the wild", "weaponized",
)

RISK_LEVELS = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]


class AIOrchestrator:
    """
    AI orchestrator for VAPT.
    
    Full AI-first pipeline:
    1. Plan (AI planner + knowledge base) → 2. Recon → 3. Enumerate →
    4. Vulnerability Detect → 5. Verify → 6. Report
    """

    def __init__(self):
        self.executor = get_vapt_executor()
        self.recon = ReconOrchestrator(self.executor)
        self.researcher = ResearcherAgent()
        self.verifier = VerifierAgent()
        self.planner = get_planner()

    async def analyze_and_scan(
        self,
        target: str,
        scan_type: str = "auto",
        scan_id: Optional[str] = None,
        quick: bool = False,
    ) -> VAPTScanResult:
        """Analyze target and run the AI-planned scan with live progress events.

        ``quick=True`` skips the LLM planner and the autonomous agent loop,
        falling back to the deterministic tool set with a bounded port scope
        (see executor quick mode)."""
        scan_id = scan_id or str(uuid4())

        controller = get_scan_controller()
        controller.register(scan_id, meta={"target": target, "scan_type": scan_type})
        reset_llm_usage(scan_id)

        await publish_scan_event(scan_id, "scan_started", {"target": target, "scan_type": scan_type})

        target_info = self._analyze_target(target)
        scan_type_enum = self._determine_scan_type(scan_type, target_info)

        await publish_scan_event(scan_id, "ai_analyzing", {
            "target": target,
            "target_type": target_info["type"],
            "message": f"Analyzing target: {target} ({target_info['type']})",
        })

        # Ground the whole workflow in the knowledge base up front: the
        # methodology snippets retrieved here feed planning, the agent loop,
        # risk scoring and the executive summary.
        kb_guidance = await asyncio.to_thread(
            self._kb_ground_target, target_info, scan_type_enum
        )
        if kb_guidance:
            target_info["kb_guidance"] = kb_guidance
            target_info["kb_query"] = kb_guidance["query"]
            await publish_scan_event(scan_id, "ai_kb_grounding", {
                "target": target,
                "target_type": target_info["type"],
                "query": kb_guidance["query"],
                "snippets": kb_guidance["snippets"][:3],
                "message": (
                    f"Workflow grounded in knowledge base for {target} "
                    f"({target_info['type']} methodology)"
                ),
            })

        watchdog = asyncio.create_task(self._stall_watchdog(scan_id))
        try:
            if quick:
                plan = self._quick_plan(scan_type_enum, target_info)
                await publish_scan_event(scan_id, "plan_ready", plan)
            else:
                try:
                    plan = await asyncio.wait_for(
                        self.planner.plan_scan(target, scan_type_enum, target_info),
                        timeout=int(os.environ.get("VAPT_PLAN_TIMEOUT", "300")),
                    )
                except asyncio.TimeoutError:
                    logger.warning("Planner timed out for %s - using KB fallback plan", target)
                    plan = {
                        "target": target,
                        "scan_type": scan_type_enum.value,
                        "target_type": target_info["type"],
                        "phases": [],
                        "tool_count": 0,
                        "strategy": "Planner timed out - knowledge-base fallback",
                    }

                if not plan["phases"]:
                    plan = self._quick_plan(scan_type_enum, target_info)

                await publish_scan_event(scan_id, "plan_ready", plan)

            if scan_type_enum == VAPTScanType.LLM:
                llm_reason = "Dedicated LLM vulnerability scanner"
                if kb_guidance and kb_guidance["snippets"]:
                    llm_reason = (
                        f"{llm_reason} | KB: {kb_guidance['snippets'][0][:200]}"
                    )
                plan["phases"] = [{
                    "id": "llm",
                    "name": "AI / LLM Security Testing",
                    "description": "OWASP LLM Top 10 probes - prompt injection, jailbreaks, data leakage",
                    "tools": [{
                        "id": "garak",
                        "name": "Garak",
                        "description": "AI/LLM security scanner (OWASP LLM Top 10 probes)",
                        "reason": llm_reason,
                    }],
                }]

            if kb_guidance:
                plan["kb_guidance"] = kb_guidance["snippets"][:2]

            tools = [t["id"] for p in plan["phases"] for t in p["tools"]]
            tools = list(dict.fromkeys(tools))

            await publish_scan_event(scan_id, "ai_decision", {
                "message": f"AI selected {len(tools)} tools across {len(plan['phases'])} phases from knowledge base",
                "tools": tools,
                "strategy": plan["strategy"],
            })

            await controller.checkpoint(scan_id)

            request = VAPTScanRequest(
                target=VAPTTarget(value=target, type=target_info["type"]),
                scan_type=scan_type_enum,
                tools=tools,
                quick=quick,
            )

            async def publish(scan_id_: str, event_type: str, data: dict) -> None:
                await publish_scan_event(scan_id_, event_type, data)

            self.recon.set_progress_publisher(publish)

            await publish_scan_event(scan_id, "phase_started", {
                "phase": "execution",
                "tools": tools,
                "message": "Starting tool execution",
            })

            # Phase 1: the autonomous agent loop runs FIRST (when enabled and an
            # LLM is reachable); the classic phased recon pipeline is the
            # automatic fallback. External platform adapters fan out alongside,
            # as does the LLM test-matrix phase. All are best-effort: a failing
            # member never aborts the scan.
            result, adapter_results, matrix_out = await asyncio.gather(
                self._run_agent_or_recon(request, scan_id, target_info, publish),
                self._run_adapters(target, scan_type_enum, scan_id, target_info),
                self._run_matrix_phase(request, scan_id, target_info, publish),
                return_exceptions=True,
            )
            if isinstance(result, BaseException):
                raise result
            if isinstance(adapter_results, BaseException):
                logger.warning("Adapters failed for %s: %s", target, adapter_results)
                adapter_results = []
            if isinstance(matrix_out, BaseException):
                logger.warning("Matrix phase failed for %s: %s", target, matrix_out)
                matrix_out = {"findings": [], "entries": [], "suspicious": 0,
                              "provider": None, "surface": None}

            for ar in adapter_results:
                for finding in ar.findings:
                    result.add_finding(finding)
                if ar.adapter_id not in result.tool_results:
                    result.tool_results[ar.adapter_id] = {}
                result.tool_results[ar.adapter_id].update({
                    "findings": len(ar.findings),
                    "duration": ar.duration,
                    "errors": ar.errors,
                    "status": "ok" if not ar.errors else "error",
                })

            for finding in matrix_out.get("findings") or []:
                result.add_finding(finding)
            result.tool_results["matrix"] = {
                "entries": len(matrix_out.get("entries") or []),
                "suspicious": matrix_out.get("suspicious", 0),
                "findings": len(matrix_out.get("findings") or []),
                "provider": matrix_out.get("provider"),
                "surface": matrix_out.get("surface") or {},
            }

            await controller.checkpoint(scan_id)

            await publish_scan_event(scan_id, "ai_research", {
                "message": "Researcher agent enriching findings from knowledge base",
            })
            t0 = time.time()
            try:
                result.findings = await asyncio.wait_for(
                    self.researcher.enrich_findings(result.findings),
                    timeout=int(os.environ.get("VAPT_RESEARCH_TIMEOUT", "90")),
                )
            except (asyncio.TimeoutError, asyncio.CancelledError):
                # Research is best-effort: a slow/failed enrichment must never
                # fail the scan. Keep the raw findings and move on.
                logger.warning(
                    "Research enrichment timed out after %ss - keeping raw findings",
                    os.environ.get("VAPT_RESEARCH_TIMEOUT", "90"),
                )
            await publish_scan_event(scan_id, "ai_research_done", {
                "duration": round(time.time() - t0, 1),
                "enriched_count": len(result.findings),
            })

            await controller.checkpoint(scan_id)

            await publish_scan_event(scan_id, "ai_verification", {
                "message": "Verifier agent re-confirming findings to eliminate false positives",
            })
            t0 = time.time()
            try:
                result.findings = await asyncio.wait_for(
                    self.verifier.verify_findings(
                        result.findings, scan_id=scan_id, publish=publish_scan_event
                    ),
                    timeout=int(os.environ.get("VAPT_VERIFY_ALL_TIMEOUT", "240")),
                )
            except (asyncio.TimeoutError, asyncio.CancelledError):
                logger.warning(
                    "Verification timed out after %ss - keeping findings",
                    os.environ.get("VAPT_VERIFY_ALL_TIMEOUT", "240"),
                )
            await publish_scan_event(scan_id, "ai_verification_done", {
                "duration": round(time.time() - t0, 1),
                "confirmed_count": len(result.findings),
            })

            # Canonical vulnerability names + CVSS scores so reports and the
            # findings UI show standard titles instead of raw tool output.
            from app.vapt.normalizer import normalize_findings

            result.findings = normalize_findings(result.findings)

            await controller.checkpoint(scan_id)

            await publish_scan_event(scan_id, "report_generating", {
                "message": "Generating executive summary and remediation plan",
            })
            insights = await asyncio.wait_for(
                asyncio.to_thread(self.generate_insights, result),
                timeout=int(os.environ.get("VAPT_REPORT_TIMEOUT", "60")),
            )
            matrix_entries = matrix_out.get("entries") or []
            insights["test_matrix"] = {
                "provider": matrix_out.get("provider"),
                "suspicious": matrix_out.get("suspicious", 0),
                "entries": [
                    {
                        "id": e["id"], "endpoint": e["endpoint"], "method": e["method"],
                        "attack_type": e["attack_type"], "priority": e["priority"],
                        "expected_result": e.get("expected_result") or "",
                        "suspicious": bool(e.get("probe", {}).get("suspicious")),
                        "status": e.get("probe", {}).get("status"),
                    }
                    for e in matrix_entries
                ],
            }
            try:
                chain = await asyncio.wait_for(
                    get_matrix_agent().build_attack_chain(
                        result.findings, scan_id=scan_id, publish=publish_scan_event
                    ),
                    timeout=int(os.environ.get("VAPT_CHAIN_TIMEOUT", "120")),
                )
                insights["attack_chain"] = chain
                logger.info("Attack chain synthesized: %d steps",
                            len(chain.get("steps") or []))
            except (asyncio.TimeoutError, Exception) as e:
                logger.warning("Attack chain synthesis failed: %s", e)
                insights["attack_chain"] = {"summary": "", "steps": []}
            result.tool_results["ai_insights"] = insights
            usage = llm_usage_snapshot(scan_id)
            if usage and usage.get("calls"):
                await publish_scan_event(scan_id, "llm_stats", {
                    "phase": "total",
                    "calls": usage["calls"],
                    "ok_calls": usage["ok_calls"],
                    "total_tokens": usage["total_tokens"],
                    "elapsed_ms": usage["elapsed_ms"],
                    "providers": usage["providers"],
                    "purposes": usage["purposes"],
                    "message": (
                        f"Scan used {usage['calls']} LLM call(s) across "
                        f"{len(usage['providers'])} provider(s), "
                        f"{usage['total_tokens']} tokens in {usage['elapsed_ms'] / 1000:.1f}s"
                    ),
                })
            await publish_scan_event(scan_id, "report_ready", insights)
            await publish_scan_event(scan_id, "scan_completed", {
                "status": result.status,
                "findings_count": len(result.findings),
                "duration": round(result.duration, 1),
                "insights": insights,
            })

            bus = get_progress_bus()
            await bus.set_status(scan_id, result.status, findings_count=len(result.findings))

            await self._ingest_attack_graph(scan_id, target, result)

            return result
        except asyncio.CancelledError as exc:
            # Stop requested while the scan task was cancelled mid-await
            # (e.g. inside a docker worker). Convert to the cooperative stop
            # signal so callers mark the assessment as stopped.
            raise ScanStoppedError(scan_id) from exc
        except ScanStoppedError:
            await publish_scan_event(scan_id, "scan_stopped", {
                "message": "Scan stopped by user",
            })
            await get_progress_bus().set_status(scan_id, "stopped")
            raise
        finally:
            watchdog.cancel()
            controller.finish(scan_id)

    async def _run_agent_or_recon(
        self,
        request: VAPTScanRequest,
        scan_id: str,
        target_info: Dict[str, Any],
        publish: Any,
    ) -> VAPTScanResult:
        """Run the autonomous agent loop, falling back to the classic phased
        recon pipeline when the loop is disabled or no LLM is reachable."""
        agent_mode = os.environ.get("VAPT_AGENT_MODE", "true").lower() == "true"
        if agent_mode and not request.quick:
            from app.vapt.agents.agent_loop import agent_loop_supported, get_agent_loop
            from app.vapt.control import get_scan_controller
            from app.recon_orchestrator.graph_db import get_knowledge_graph

            if agent_loop_supported(request.scan_type):
                loop = get_agent_loop(
                    self.executor,
                    get_scan_controller(),
                    publish,
                    get_knowledge_graph(),
                )
                try:
                    loop_out = await asyncio.wait_for(
                        loop.run(
                            scan_id,
                            request.target.value,
                            target_info,
                            request.scan_type,
                        ),
                        timeout=int(os.environ.get("VAPT_AGENT_TIMEOUT", "1800")),
                    )
                except asyncio.TimeoutError:
                    logger.warning(
                        "Agent loop timed out for %s - using classic pipeline",
                        request.target.value,
                    )
                    loop_out = None
                except ScanStoppedError:
                    raise
                if loop_out is not None:
                    steps, findings = loop_out
                    result = VAPTScanResult(
                        id=uuid4(),
                        request=request,
                        status="completed",
                        started_at=datetime.utcnow(),
                    )
                    result.findings = findings
                    result.tool_results["agent_loop"] = {
                        "steps": [s.to_dict() for s in steps],
                        "steps_count": len(steps),
                        "findings": len(findings),
                        "status": "ok",
                    }
                    result.finalize(
                        "completed",
                        f"Autonomous agent completed {len(steps)} steps "
                        f"with {len(findings)} findings",
                    )
                    return result
                logger.info("Agent loop unavailable - falling back to classic pipeline")
            group_usage = llm_usage_snapshot(scan_id)
            if group_usage and group_usage.get("calls"):
                await publish(scan_id, "llm_stats", {
                    "phase": "agent_loop",
                    "calls": group_usage["calls"],
                    "ok_calls": group_usage["ok_calls"],
                    "total_tokens": group_usage["total_tokens"],
                    "elapsed_ms": group_usage["elapsed_ms"],
                    "providers": group_usage["providers"],
                    "purposes": group_usage["purposes"],
                    "message": (
                        f"Autonomous agent loop: {group_usage['calls']} LLM turn(s), "
                        f"{group_usage['total_tokens']} tokens, "
                        f"{group_usage['elapsed_ms'] / 1000:.1f}s"
                    ),
                })

        result = await self.recon.execute_scan(request, scan_id=scan_id)

        # A timed-out/aborted agent loop may still have produced findings -
        # merge them in so the classic pipeline result is enriched, never
        # replaced, by the partial agent work.
        try:
            from app.vapt.control import get_scan_controller

            partial = get_scan_controller().get_agent_partial(scan_id)
            if partial:
                p_steps, p_findings = partial
                merged = 0
                for f in p_findings:
                    if not any(
                        (x.title, x.description, x.target)
                        == (f.title, f.description, f.target)
                        for x in result.findings
                    ):
                        result.add_finding(f)
                        merged += 1
                result.tool_results["agent_loop_partial"] = {
                    "steps": len(p_steps),
                    "findings": len(p_findings),
                    "merged": merged,
                    "status": "partial",
                }
                logger.info(
                    "Merged %d findings from partial agent loop into classic result",
                    merged,
                )
        except Exception as e:
            logger.warning("Agent partial merge failed: %s", e)

        return result

    async def _run_adapters(
        self,
        target: str,
        scan_type: VAPTScanType,
        scan_id: str,
        target_info: Dict[str, Any],
    ) -> List[Any]:
        """Run all enabled external adapters in parallel against the target.

        Adapters run AFTER the built-in Kali toolchain and BEFORE agent
        enrichment, so their findings flow through the same researcher /
        verifier / risk-scoring pipeline. Each adapter is isolated - one
        failing adapter never aborts the scan.
        """
        adapters = [a for a in get_enabled_adapters() if a.allow_for(scan_type, target_info)]
        if not adapters:
            return []

        await publish_scan_event(scan_id, "adapters_started", {
            "adapters": [a.id for a in adapters],
            "message": f"Running {len(adapters)} external platform adapters",
        })

        results = await asyncio.gather(*[
            self._run_one_adapter(a, target, scan_id, scan_type, target_info)
            for a in adapters
        ])

        await publish_scan_event(scan_id, "adapters_completed", {
            "adapters": [
                {"id": r.adapter_id, "findings": len(r.findings), "errors": len(r.errors)}
                for r in results
            ],
            "message": f"External adapters finished: {sum(len(r.findings) for r in results)} findings",
        })
        return results

    async def _run_one_adapter(
        self,
        adapter: Any,
        target: str,
        scan_id: str,
        scan_type: VAPTScanType,
        target_info: Dict[str, Any],
    ):
        await publish_scan_event(scan_id, "adapter_started", {
            "adapter": adapter.id,
            "name": adapter.name,
            "message": f"{adapter.name} starting against {target}",
        })
        result = await adapter.run_scan(target, scan_id, scan_type, target_info)
        await publish_scan_event(scan_id, "adapter_completed", {
            "adapter": adapter.id,
            "name": adapter.name,
            "findings": len(result.findings),
            "errors": result.errors,
            "duration": result.duration,
            "message": (
                f"{adapter.name} found {len(result.findings)} findings in {result.duration:.0f}s"
                if not result.errors
                else f"{adapter.name} completed with errors: {'; '.join(result.errors)[:200]}"
            ),
        })
        return result

    async def _run_matrix_phase(
        self,
        request: VAPTScanRequest,
        scan_id: str,
        target_info: Dict[str, Any],
        publish: Callable[..., Awaitable[None]],
    ) -> Dict[str, Any]:
        """LLM test-matrix phase: mine surface -> generate matrix -> probe.

        Mirrors the validated engagement workflow: bundle/route mining,
        LLM-generated {endpoint, method, attack_type, payload, expected_result}
        entries executed as HTTP probes (Kali curl) or tool runs, with PoC
        evidence captured into findings. Runs in parallel with the agent loop
        and adapters; failures never abort the scan.
        """
        target = request.target.value
        scan_type = request.scan_type.value if request.scan_type else "auto"
        base = target if target.startswith(("http://", "https://")) else f"http://{target}"

        outcome: Dict[str, Any] = {
            "findings": [], "entries": [], "suspicious": 0,
            "provider": None, "surface": None,
        }

        await publish(scan_id, "matrix_generating", {
            "message": "Mining web surface (JS bundles) for test-matrix endpoints",
        })

        heartbeat_task: Optional[asyncio.Task] = None
        heartbeat_cancel = asyncio.Event()

        async def _heartbeat():
            try:
                while not heartbeat_cancel.is_set():
                    await asyncio.sleep(30)
                    if heartbeat_cancel.is_set():
                        break
                    await publish(scan_id, "matrix_heartbeat", {
                        "message": "Matrix phase running (mining surface, LLM generation)...",
                    })
            except asyncio.CancelledError:
                pass

        heartbeat_task = asyncio.create_task(_heartbeat())
        try:
            surface = await asyncio.wait_for(
                mine_web_surface(base, timeout=float(os.environ.get("VAPT_MATRIX_RECON_TIMEOUT", "25"))),
                timeout=40,
            )
            outcome["surface"] = {
                "endpoints": surface.get("endpoint_count", 0),
                "scripts": surface.get("scripts") or [],
                "hints": surface.get("hints") or [],
            }
        except Exception as e:
            logger.warning("Matrix surface mining failed for %s: %s", target, e)
            surface = {"endpoints": [], "hints": []}

        kb_query = (
            TARGET_KB_QUERIES.get(target_info.get("type"))
            or SCAN_TYPE_KB_QUERIES.get(scan_type)
            or "web application penetration testing methodology"
        )
        kb_ctx: List[str] = []
        try:
            kb_ctx = await asyncio.wait_for(
                asyncio.to_thread(kb_snippets, kb_query, 3),
                timeout=int(os.environ.get("VAPT_MATRIX_KB_TIMEOUT", "45")),
            )
        except (asyncio.TimeoutError, Exception) as e:
            logger.warning("Matrix KB grounding failed/timeout: %s", e)
            kb_ctx = []

        # Session acquisition: try default credentials on discovered login
        # endpoints so authenticated attack classes (XXE, IDOR, admin API,
        # CSRF) are testable. Bounded and best-effort.
        from app.vapt.agents.session import try_acquire_session

        session: Optional[Dict[str, Any]] = None
        try:
            session = await asyncio.wait_for(
                try_acquire_session(
                    base,
                    surface.get("endpoints") or [],
                    scan_id=scan_id,
                    timeout=float(os.environ.get("VAPT_SESSION_TIMEOUT", "20")),
                ),
                timeout=30,
            )
        except (asyncio.TimeoutError, Exception) as e:
            logger.warning("Session acquisition failed for %s: %s", target, e)
        if session:
            await publish(scan_id, "session_acquired", {
                "kind": session["kind"],
                "endpoint": session["endpoint"],
                "credential": session["credential"],
                "evidence": session["evidence"],
                "message": (
                    f"Session acquired via default credentials "
                    f"({session['credential']}) on {session['endpoint']} - "
                    "running authenticated probes"
                ),
            })
            outcome["findings"].append(VAPTFinding(
                title="Default Credentials - Weak Authentication",
                description=(
                    f"Login endpoint {session['endpoint']} accepts default/vendor "
                    f"credentials ({session['credential']}), granting a full session "
                    f"({session['evidence']}). Authenticated test probes were run "
                    "with this session."
                ),
                severity=VAPTSeverity.HIGH,
                tool_name="session-acquisition",
                target=target,
                path=session["endpoint"],
                vulnerability_type="Broken Authentication",
                remediation=(
                    "Disable default/vendor accounts, enforce password policies, "
                    "and implement account lockout / rate limiting."
                ),
            ))

        try:
            entries, provider = await asyncio.wait_for(
                get_matrix_agent().generate_matrix(
                    base, scan_type, target_info, surface, kb_ctx,
                    scan_id=scan_id, publish=publish, session=session,
                ),
                timeout=int(os.environ.get("VAPT_MATRIX_LLM_TIMEOUT", "240")),
            )
        except (asyncio.TimeoutError, Exception) as e:
            logger.warning("Matrix generation failed/timeout: %s", e)
            entries, provider = [], None
        outcome["provider"] = provider
        usage = llm_usage_snapshot(scan_id)
        if usage and usage.get("calls"):
            failure_calls = usage["calls"] - usage["ok_calls"]
            await publish(scan_id, "llm_stats", {
                "phase": "matrix",
                "calls": usage["calls"],
                "ok_calls": usage["ok_calls"],
                "total_tokens": usage["total_tokens"],
                "elapsed_ms": usage["elapsed_ms"],
                "providers": usage["providers"],
                "purposes": usage["purposes"],
                "message": (
                    f"LLM matrix generation: {usage['calls']} call(s), "
                    f"{usage['total_tokens']} tokens, {usage['elapsed_ms']:.0f}ms"
                    + (f" ({failure_calls} failed)" if failure_calls else "")
                ),
            })
        await publish(scan_id, "matrix_generated", {
            "entries": len(entries),
            "provider": provider,
            "endpoints": surface.get("endpoint_count", 0),
            "message": f"Test matrix ready: {len(entries)} exploitation probes ({provider or 'heuristic'})",
            "matrix": [
                {
                    "id": e["id"],
                    "endpoint": e["endpoint"],
                    "method": e["method"],
                    "attack_type": e["attack_type"],
                    "priority": e["priority"],
                    "expected_result": (e.get("expected_result") or "")[:200],
                    "params": {
                        k: str(v)[:120] for k, v in (e.get("params") or {}).items()
                    } or None,
                }
                for e in entries
            ],
        })
        if not entries:
            return outcome

        executor = get_vapt_executor()
        for entry in entries:
            await publish(scan_id, "matrix_entry_started", {
                "id": entry["id"],
                "endpoint": entry["endpoint"],
                "method": entry["method"],
                "attack_type": entry["attack_type"],
                "priority": entry["priority"],
            })
            probe: Dict[str, Any] = {}
            try:
                if entry.get("tool"):
                    tool_findings, output, err = await executor.run_agent_tool(
                        entry["tool"], base + entry["endpoint"], ""
                    )
                    outcome["findings"].extend(tool_findings)
                    probe = {"tool": entry["tool"], "error": err, "raw": (output or "")[-1500:]}
                else:
                    auth_header = (session or {}).get("header", "") if session else ""
                    cmd = build_curl_command(entry, base, auth_header)
                    output, err = await executor.run_arbitrary_command(
                        cmd, timeout=int(os.environ.get("VAPT_MATRIX_PROBE_TIMEOUT", "30"))
                    )
                    status, body = parse_probe_output(output)
                    payload_values = list((entry.get("params") or {}).values())
                    suspicious, reason = MatrixAgent.classify_entry(
                        entry, status, body, payload_values, output
                    )
                    probe = {"status": status, "body": body[:300], "body_len": len(body),
                             "error": err, "suspicious": suspicious, "reason": reason}
                    if suspicious:
                        outcome["findings"].append(self._matrix_probe_finding(
                            entry, base, status, body, output, reason
                        ))
            except Exception as e:
                logger.warning("Matrix entry %s (%s%s) failed: %s",
                               entry["id"], entry["method"], entry["endpoint"], e)
                probe["error"] = str(e)
            finally:
                entry["probe"] = probe
                outcome["entries"].append(entry)
                await publish(scan_id, "matrix_entry_done", {
                    "id": entry["id"],
                    "endpoint": entry["endpoint"],
                    "attack_type": entry["attack_type"],
                    "suspicious": bool(probe.get("suspicious")),
                    "status": probe.get("status"),
                    "reason": probe.get("reason") or "",
                    "poc_preview": (
                        str(probe.get("body") or "")[:300]
                        if not probe.get("tool") else ""
                    ),
                    "tool": probe.get("tool") or "",
                    "error": probe.get("error") or "",
                })

        outcome["suspicious"] = sum(
            1 for e in outcome["entries"] if e.get("probe", {}).get("suspicious")
        )
        heartbeat_cancel.set()
        if heartbeat_task:
            await asyncio.wait([heartbeat_task], timeout=2)
        return outcome

    def _matrix_probe_finding(
        self,
        entry: Dict[str, Any],
        base: str,
        status: int,
        body: str,
        output: str,
        reason: str,
    ) -> VAPTFinding:
        """Build a VAPTFinding carrying the full PoC trio for a matrix entry."""
        from urllib.parse import urlparse

        parsed = urlparse(base)
        return VAPTFinding(
            title=f"[Matrix] {entry['attack_type']} — {entry['method']} {entry['endpoint']}",
            description=(
                f"LLM test-matrix probe flagged: {reason}.\n"
                f"Expected result: {entry.get('expected_result') or 'n/a'}."
            ),
            severity=MatrixAgent.severity_for(entry["priority"]),
            tool_name="matrix-probe",
            target=base,
            host=parsed.hostname or base,
            path=entry["endpoint"],
            vulnerability_type=entry["attack_type"],
            payload=json.dumps({
                "params": entry.get("params") or {},
                "json_body": entry.get("json_body"),
            }, ensure_ascii=False)[:2000],
            details={
                "matrix_entry_id": entry["id"],
                "attack_type": entry["attack_type"],
                "priority": entry["priority"],
                "poc_request": {
                    "method": entry["method"],
                    "url": base.rstrip("/") + entry["endpoint"],
                    "params": entry.get("params") or {},
                    "json_body": entry.get("json_body"),
                },
                "poc_response": {
                    "status": status,
                    "body_preview": body[:2000],
                    "body_length": len(body),
                },
                "poc_evidence": (output or "")[-3000:],
                "expected_result": entry.get("expected_result") or "",
            },
        )

    async def _stall_watchdog(self, scan_id: str) -> None:
        """Detect when a running scan stops producing activity (stuck).

        If no event was published for STALL_SECONDS while the scan is still
        running, emit a scan_stalled event once so the UI can warn the user.
        """
        stall_seconds = int(os.environ.get("VAPT_STALL_SECONDS", "300"))
        await asyncio.sleep(stall_seconds)
        bus = get_progress_bus()
        while True:
            st = await bus.status(scan_id)
            if not st or st.get("status") not in ("running", "planning", "pending", "queued"):
                return
            last_active = st.get("last_active") or st.get("ts") or 0
            idle = time.time() - float(last_active)
            if idle > stall_seconds:
                logger.warning("Scan %s appears stalled (idle %.0fs)", scan_id, idle)
                await publish_scan_event(scan_id, "scan_stalled", {
                    "idle_for": round(idle, 1),
                    "message": "No activity detected - check network connectivity or target responsiveness",
                })
                return
            await asyncio.sleep(15)

    def _analyze_target(self, target: str) -> Dict[str, Any]:
        """Analyze target to understand what it is."""
        info = {
            "original": target,
            "type": "unknown",
            "has_port": False,
            "is_web": False,
            "is_ip": False,
            "is_domain": False,
        }

        if target.startswith(("http://", "https://")):
            info["type"] = "url"
            info["is_web"] = True
        elif ":" in target:
            parts = target.split(":")
            info["type"] = "url"
            info["is_web"] = True
            info["has_port"] = True
        elif self._is_valid_ip(target):
            info["type"] = "ip"
            info["is_ip"] = True
        elif "." in target and not target.startswith("http"):
            info["type"] = "domain"
            info["is_domain"] = True
        else:
            info["type"] = "hostname"
            info["is_domain"] = True

        return info

    def _is_valid_ip(self, target: str) -> bool:
        parts = target.split(".")
        if len(parts) != 4:
            return False
        return all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)

    def _kb_ground_target(
        self, target_info: Dict[str, Any], scan_type: VAPTScanType
    ) -> Optional[Dict[str, Any]]:
        """Retrieve KB methodology snippets for the target (sync, CPU-bound)."""
        try:
            if not kb_ready():
                return None
            query = SCAN_TYPE_KB_QUERIES.get(
                scan_type.value, TARGET_KB_QUERIES.get(target_info.get("type", "unknown"))
            ) or TARGET_KB_QUERIES["unknown"]
            return {
                "query": query,
                "snippets": kb_snippets(query, top_k=3, max_len=260),
            }
        except Exception as e:
            logger.warning("KB target grounding failed: %s", e)
            return None

    def _determine_scan_type(self, requested: str, target_info: Dict) -> VAPTScanType:
        if requested != "auto":
            try:
                return VAPTScanType(requested)
            except ValueError:
                pass

        if target_info["is_web"]:
            return VAPTScanType.WEB
        return VAPTScanType.NETWORK

    def _quick_plan(self, scan_type: VAPTScanType, target_info: Dict) -> Dict[str, Any]:
        """Deterministic fallback plan used for quick scans and planner
        timeouts - no LLM round-trip, bounded tool set."""
        tools = self._select_tools(scan_type, target_info)
        return {
            "target": target_info.get("value", ""),
            "scan_type": scan_type.value,
            "target_type": target_info["type"],
            "phases": [{
                "id": "recon",
                "name": "Reconnaissance",
                "description": "Fallback tool set",
                "tools": [{"id": t, "name": t, "description": "", "reason": "fallback"} for t in tools],
            }],
            "tool_count": len(tools),
            "strategy": "Quick scan - deterministic fallback tool set",
        }

    def _select_tools(self, scan_type: VAPTScanType, target_info: Dict) -> List[str]:
        """Select tools based on scan type and target."""
        tool_selection = {
            VAPTScanType.NETWORK: ["nmap"],
            VAPTScanType.WEB: ["nmap", "nikto", "nuclei", "gobuster"],
            VAPTScanType.API: ["nuclei", "nmap"],
            VAPTScanType.SSL: ["sslscan", "nmap"],
            VAPTScanType.CONTAINER: ["trivy"],
            VAPTScanType.LLM: ["garak", "promptfoo"],
            VAPTScanType.CODE_REVIEW: ["code-review", "gitleaks", "trufflehog", "semgrep", "bandit"],
            VAPTScanType.FULL: ["nmap", "masscan", "dnsrecon", "subfinder", "nikto", "nuclei", "gobuster", "ffuf", "whatweb", "httpx", "api-surface", "sslscan", "testssl", "trivy", "garak", "forms", "code-review", "flows", "dom-xss"],
        }
        return tool_selection.get(scan_type, ["nmap"])

    def generate_insights(self, result: VAPTScanResult) -> Dict[str, Any]:
        """Generate AI insights on scan results, grounded in the KB.

        Risk scoring is evidence-driven: findings are matched against the
        KB (CVEs, known-exploited references) and the risk level is adjusted
        when KB sources flag high-velocity exploitation.
        """
        severity_counts = result.get_severity_counts()
        critical = severity_counts.get(VAPTSeverity.CRITICAL, 0)
        high = severity_counts.get(VAPTSeverity.HIGH, 0)

        risk_level = "LOW"
        if critical > 0 or high > 3:
            risk_level = "CRITICAL"
        elif high > 0 or severity_counts.get(VAPTSeverity.MEDIUM, 0) > 5:
            risk_level = "HIGH"
        elif severity_counts.get(VAPTSeverity.MEDIUM, 0) > 0:
            risk_level = "MEDIUM"

        kb_risk = self._kb_risk_analysis(result)
        risk_level, justification = self._kb_adjust_risk(risk_level, kb_risk, severity_counts)

        insight_levels = {
            "risk_level": risk_level,
            "risk_justification": justification,
            "kb_evidence": kb_risk["evidence"][:12],
            "kb_cves": kb_risk["cves"][:15],
            "kb_status": kb_risk["status"],
            "total_findings": len(result.findings),
            "severity_breakdown": {k.value: v for k, v in severity_counts.items()},
            "tools_used": list(result.tool_results.keys()),
            "scan_duration": f"{result.duration:.1f}s",
            "recommendations": self._generate_recommendations(result, risk_level, kb_risk),
            "executive_summary": self._generate_summary(result, risk_level, kb_risk),
        }
        return insight_levels

    def _kb_risk_analysis(self, result: VAPTScanResult) -> Dict[str, Any]:
        """Match findings against the KB and collect CVEs / exploitation flags.

        Runs synchronously (bounded: top 10 findings, 2 hits each); callers
        wrap it in asyncio.to_thread when on the event loop.
        """
        evidence: List[Dict[str, Any]] = []
        cves: List[str] = []
        kev = False
        try:
            if not kb_ready():
                return {"evidence": [], "cves": [], "kev": kev, "status": "unavailable"}
            found_cves = set(f.cve for f in result.findings if f.cve)
            rank = {VAPTSeverity.CRITICAL: 0, VAPTSeverity.HIGH: 1,
                    VAPTSeverity.MEDIUM: 2, VAPTSeverity.LOW: 3,
                    VAPTSeverity.INFO: 4}
            top = sorted(result.findings, key=lambda f: rank.get(f.severity, 4))[:10]
            for f in top:
                hits = kb_context_for_finding(
                    f.title, f.description, f.vulnerability_type or "",
                    severity=f.severity.value,
                )
                for h in hits:
                    text = (h.get("text") or "")[:500].lower()
                    if any(m in text for m in KEV_MARKERS):
                        kev = True
                    hit_cves = re.findall(r"CVE-\d{4}-\d{4,7}",
                                          h.get("text") or "", re.IGNORECASE)
                    new_cves = [c for c in hit_cves if c not in found_cves and c not in cves]
                    cves.extend(new_cves[:3])
                    evidence.append({
                        "severity": f.severity.value,
                        "finding": f.title[:120],
                        "evidence": (h.get("text") or "")[:220],
                        "source": str(h.get("source", ""))[:180],
                        "title": str(h.get("title", ""))[:120],
                        "relevance": round(float(h.get("relevance", 0) or 0), 3),
                    })
                if len(evidence) >= 16:
                    break
        except Exception as e:
            logger.warning("KB risk analysis failed: %s", e)
            return {"evidence": [], "cves": [], "kev": False, "status": "error"}
        status = "ready" if evidence else "no_evidence"
        return {"evidence": evidence, "cves": cves, "kev": kev, "status": status}

    def _kb_adjust_risk(
        self, base: str, kb_risk: Dict[str, Any], severity_counts: Dict[str, int]
    ) -> tuple:
        """Elevate risk one notch when KB flags known-exploited activity."""
        if not kb_risk.get("kev") or kb_risk.get("status") != "ready":
            return base, ""
        idx = RISK_LEVELS.index(base)
        if idx < len(RISK_LEVELS) - 1:
            adjusted = RISK_LEVELS[idx + 1]
            justification = (
                f"Risk elevated from {base} to {adjusted}: KB sources flag "
                f"known-exploited (KEV) activity for {len(kb_risk['evidence'])} "
                "matched finding references."
            )
            return adjusted, justification
        return base, (
            f"CRITICAL posture confirmed: KB sources flag known-exploited "
            f"(KEV) activity across {len(kb_risk['evidence'])} finding references."
        )

    def _generate_recommendations(
        self, result: VAPTScanResult, risk_level: str, kb_risk: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        kb_risk = kb_risk or {}
        recommendations = []
        severity_counts = result.get_severity_counts()

        kb_recommendations = []
        for f in result.findings:
            if f.details.get("kb_context"):
                snippet = " ".join(str(f.details.get("kb_context", "")).split())[:200]
                if snippet:
                    source = (f.details.get("kb_sources") or [""])[0]
                    line = f"Remediation guidance ({source}): {snippet}"
                    if line not in kb_recommendations:
                        kb_recommendations.append(line)
        recommendations.extend(sorted(kb_recommendations)[:4])

        cves = kb_risk.get("cves") or []
        if cves:
            recommendations.append(
                f"KB references additional CVEs: {', '.join(cves[:6])} - "
                "review these advisories for known-exploited status"
            )

        if severity_counts.get(VAPTSeverity.CRITICAL, 0) > 0:
            recommendations.append("CRITICAL: Address critical vulnerabilities immediately")
        if severity_counts.get(VAPTSeverity.HIGH, 0) > 0:
            recommendations.append("HIGH: Plan remediation within 1 week")
        if severity_counts.get(VAPTSeverity.MEDIUM, 0) > 5:
            recommendations.append("MEDIUM: Schedule remediation within 30 days")
        if result.tool_results.get("nmap"):
            recommendations.append("Review open ports - close unnecessary services")
        if any("sql" in f.title.lower() for f in result.findings):
            recommendations.append("CRITICAL: Implement SQL injection prevention")
        if any("xss" in f.title.lower() for f in result.findings):
            recommendations.append("HIGH: Implement XSS filters and CSP headers")

        return recommendations[:8]

    def _generate_summary(
        self, result: VAPTScanResult, risk_level: str,
        kb_risk: Optional[Dict[str, Any]] = None,
    ) -> str:
        kb_risk = kb_risk or {}
        target = result.request.target.value
        count = len(result.findings)

        if risk_level == "CRITICAL":
            summary = f"Critical security posture on {target}. {count} vulnerabilities detected requiring immediate attention."
        elif risk_level == "HIGH":
            summary = f"High-risk security posture on {target}. {count} vulnerabilities found - remediation recommended urgently."
        elif risk_level == "MEDIUM":
            summary = f"Medium security posture on {target}. {count} findings identified - address in planned timeline."
        else:
            summary = f"Acceptable security posture on {target}. {count} informational findings - continue monitoring."

        evidence = kb_risk.get("evidence") or []
        if evidence:
            rank = {VAPTSeverity.CRITICAL: 0, VAPTSeverity.HIGH: 1,
                    VAPTSeverity.MEDIUM: 2, VAPTSeverity.LOW: 3,
                    VAPTSeverity.INFO: 4}
            top = sorted(result.findings, key=lambda f: rank.get(f.severity, 4))[:3]
            if top:
                lead = "Leading risks: " + "; ".join(
                    f"{f.title[:90]} ({f.severity.value})" for f in top
                )
                summary += f" {lead}."
            kb_findings = [e for e in evidence if e["severity"] in ("critical", "high")]
            shown = {e["source"] for e in evidence}
            if shown:
                summary += (
                    f" KB confirmations: {len(evidence)} evidence references "
                    f"({', '.join(sorted(shown)[:3])})."
                )
            cves = kb_risk.get("cves") or []
            if cves:
                summary += f" KB-linked CVEs: {', '.join(cves[:5])}."

        return summary

    async def _ingest_attack_graph(
        self,
        scan_id: str,
        target: str,
        result: VAPTScanResult,
    ) -> None:
        """Populate the Neo4j attack-surface graph with targets, ports,
        services, tools and findings from this scan (best-effort)."""
        try:
            from app.recon_orchestrator.graph_db import get_knowledge_graph

            kg = get_knowledge_graph()
            if not getattr(kg, "_enabled", False):
                logger.info("Attack graph disabled (Neo4j) - skipping ingestion")
                return

            await publish_scan_event(scan_id, "graph_ingesting", {
                "message": "Building attack surface graph (Neo4j)",
            })

            target_id = f"target:{target}"
            await kg.upsert_target(target_id, target, scan_id)

            port_ids: Dict[int, str] = {}
            service_ids: Dict[tuple, str] = {}
            for finding in result.findings:
                port = finding.port
                if port and port not in port_ids:
                    port_ids[port] = await kg.upsert_port(
                        target_id, port, finding.protocol or "tcp", "open"
                    )
                service_key = (finding.port, finding.service)
                if finding.service and service_key not in service_ids:
                    service_ids[service_key] = await kg.upsert_service(
                        port_ids.get(finding.port, ""), finding.service, ""
                    )

            for finding in result.findings:
                await kg.add_finding(
                    target_id=target_id,
                    title=finding.title,
                    severity=finding.severity.value,
                    description=finding.description,
                    remediation=finding.remediation or "",
                    tool_name=finding.tool_name,
                    port_id=port_ids.get(finding.port, ""),
                    service_id=service_ids.get((finding.port, finding.service), ""),
                )

            await publish_scan_event(scan_id, "graph_ready", {
                "targets": 1,
                "findings": len(result.findings),
                "message": f"Attack surface graph built: {len(result.findings)} findings",
            })
        except Exception as exc:
            logger.error("Attack graph ingestion failed: %s", exc)


_orchestrator: Optional[AIOrchestrator] = None


def get_vapt_orchestrator() -> AIOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AIOrchestrator()
    return _orchestrator