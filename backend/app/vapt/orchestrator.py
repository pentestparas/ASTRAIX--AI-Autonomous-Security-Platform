"""
VAPT AI Orchestrator

AI-powered tool selection and scan coordination.
Analyzes target and selects appropriate tools.
"""

import asyncio
import hashlib
import os
import time
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from app.vapt.models import VAPTFinding, VAPTSeverity, VAPTScanRequest, VAPTScanResult, VAPTScanType, VAPTTarget
from app.vapt.executor import get_vapt_executor
from app.vapt.adapters.registry import get_enabled_adapters
from app.vapt.agents import ResearcherAgent, VerifierAgent
from app.vapt.agents.planner import get_planner
from app.vapt.progress import publish_scan_event, get_progress_bus
from app.recon_orchestrator.orchestrator import ReconOrchestrator
from app.core.logging import get_logger

logger = get_logger(__name__)


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

        await publish_scan_event(scan_id, "scan_started", {"target": target, "scan_type": scan_type})

        target_info = self._analyze_target(target)
        scan_type_enum = self._determine_scan_type(scan_type, target_info)

        await publish_scan_event(scan_id, "ai_analyzing", {
            "target": target,
            "target_type": target_info["type"],
            "message": f"Analyzing target: {target} ({target_info['type']})",
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

            tools = [t["id"] for p in plan["phases"] for t in p["tools"]]
            tools = list(dict.fromkeys(tools))

            await publish_scan_event(scan_id, "ai_decision", {
                "message": f"AI selected {len(tools)} tools across {len(plan['phases'])} phases from knowledge base",
                "tools": tools,
                "strategy": plan["strategy"],
            })

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

            result = await self.recon.execute_scan(request, scan_id=scan_id)

            adapter_results = await self._run_adapters(target, scan_type_enum, scan_id, target_info)
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

            await publish_scan_event(scan_id, "ai_research", {
                "message": "Researcher agent enriching findings from knowledge base",
            })
            t0 = time.time()
            result.findings = await asyncio.wait_for(
                self.researcher.enrich_findings(result.findings),
                timeout=int(os.environ.get("VAPT_RESEARCH_TIMEOUT", "90")),
            )
            await publish_scan_event(scan_id, "ai_research_done", {
                "duration": round(time.time() - t0, 1),
                "enriched_count": len(result.findings),
            })

            await publish_scan_event(scan_id, "ai_verification", {
                "message": "Verifier agent re-confirming findings to eliminate false positives",
            })
            t0 = time.time()
            result.findings = await asyncio.wait_for(
                self.verifier.verify_findings(result.findings),
                timeout=int(os.environ.get("VAPT_VERIFY_ALL_TIMEOUT", "240")),
            )
            await publish_scan_event(scan_id, "ai_verification_done", {
                "duration": round(time.time() - t0, 1),
                "confirmed_count": len(result.findings),
            })

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

            return result
        finally:
            watchdog.cancel()

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
            VAPTScanType.FULL: ["nmap", "nikto", "nuclei", "gobuster", "sslscan"],
        }
        return tool_selection.get(scan_type, ["nmap"])

    def generate_insights(self, result: VAPTScanResult) -> Dict[str, Any]:
        """Generate AI insights on scan results."""
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

        return {
            "risk_level": risk_level,
            "total_findings": len(result.findings),
            "severity_breakdown": {k.value: v for k, v in severity_counts.items()},
            "tools_used": list(result.tool_results.keys()),
            "scan_duration": f"{result.duration:.1f}s",
            "recommendations": self._generate_recommendations(result, risk_level),
            "executive_summary": self._generate_summary(result, risk_level),
        }

    def _generate_recommendations(self, result: VAPTScanResult, risk_level: str) -> List[str]:
        recommendations = []
        severity_counts = result.get_severity_counts()

        kb_recommendations = set()
        for f in result.findings:
            if f.details.get("kb_context"):
                for source in f.details.get("kb_sources", []):
                    kb_recommendations.add(f"See {source} for remediation guidance")
        recommendations.extend(sorted(kb_recommendations)[:3])

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

        return recommendations

    def _generate_summary(self, result: VAPTScanResult, risk_level: str) -> str:
        target = result.request.target.value
        count = len(result.findings)

        if risk_level == "CRITICAL":
            return f"Critical security posture on {target}. {count} vulnerabilities detected requiring immediate attention."
        elif risk_level == "HIGH":
            return f"High-risk security posture on {target}. {count} vulnerabilities found - remediation recommended urgently."
        elif risk_level == "MEDIUM":
            return f"Medium security posture on {target}. {count} findings identified - address in planned timeline."
        else:
            return f"Acceptable security posture on {target}. {count} informational findings - continue monitoring."


_orchestrator: Optional[AIOrchestrator] = None


def get_vapt_orchestrator() -> AIOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AIOrchestrator()
    return _orchestrator