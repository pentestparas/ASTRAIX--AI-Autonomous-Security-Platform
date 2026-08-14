"""
VAPT AI Orchestrator

AI-powered tool selection and scan coordination.
Analyzes target and selects appropriate tools.
"""

import asyncio
import hashlib
import os
import re
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from app.vapt.models import VAPTFinding, VAPTSeverity, VAPTScanRequest, VAPTScanResult, VAPTScanType, VAPTTarget
from app.vapt.executor import get_vapt_executor
from app.vapt.adapters.registry import get_enabled_adapters
from app.vapt.agents import ResearcherAgent, VerifierAgent
from app.vapt.agents.kb import kb_snippets, kb_context_for_finding, kb_ready
from app.vapt.agents.planner import get_planner
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
    ) -> VAPTScanResult:
        """Analyze target and run the AI-planned scan with live progress events."""
        scan_id = scan_id or str(uuid4())

        controller = get_scan_controller()
        controller.register(scan_id, meta={"target": target, "scan_type": scan_type})

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
            try:
                plan = await asyncio.wait_for(
                    self.planner.plan_scan(target, scan_type_enum, target_info),
                    timeout=int(os.environ.get("VAPT_PLAN_TIMEOUT", "60")),
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

            await publish_scan_event(scan_id, "plan_ready", plan)

            if not plan["phases"]:
                fallback = self._select_tools(scan_type_enum, target_info)
                plan["phases"] = [{
                    "id": "recon",
                    "name": "Reconnaissance",
                    "description": "Fallback tool set",
                    "tools": [{"id": t, "name": t, "description": "", "reason": "fallback"} for t in fallback],
                }]

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
            # automatic fallback. External platform adapters fan out alongside.
            # Adapters are best-effort: a failing adapter never aborts the scan.
            result, adapter_results = await asyncio.gather(
                self._run_agent_or_recon(request, scan_id, target_info, publish),
                self._run_adapters(target, scan_type_enum, scan_id, target_info),
                return_exceptions=True,
            )
            if isinstance(result, BaseException):
                raise result
            if isinstance(adapter_results, BaseException):
                logger.warning("Adapters failed for %s: %s", target, adapter_results)
                adapter_results = []

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
                    self.verifier.verify_findings(result.findings),
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
        if agent_mode:
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

    def _select_tools(self, scan_type: VAPTScanType, target_info: Dict) -> List[str]:
        """Select tools based on scan type and target."""
        tool_selection = {
            VAPTScanType.NETWORK: ["nmap"],
            VAPTScanType.WEB: ["nmap", "nikto", "nuclei", "gobuster"],
            VAPTScanType.API: ["nuclei", "nmap"],
            VAPTScanType.SSL: ["sslscan", "nmap"],
            VAPTScanType.CONTAINER: ["trivy"],
            VAPTScanType.LLM: ["garak"],
            VAPTScanType.FULL: ["nmap", "nikto", "nuclei", "gobuster", "sslscan"],
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