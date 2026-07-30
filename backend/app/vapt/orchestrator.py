"""
VAPT AI Orchestrator

AI-powered tool selection and scan coordination.
Analyzes target and selects appropriate tools.
"""

import hashlib
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from app.vapt.models import VAPTFinding, VAPTSeverity, VAPTScanRequest, VAPTScanResult, VAPTScanType, VAPTTarget
from app.vapt.executor import get_vapt_executor
from app.vapt.agents import ResearcherAgent, VerifierAgent
from app.recon_orchestrator.orchestrator import ReconOrchestrator


class AIOrchestrator:
    """
    AI orchestrator for VAPT.
    
    Multi-agent pipeline:
    1. Recon → 2. Scan Tools → 3. Researcher Enrich → 4. Verifier Confirm
    """

    def __init__(self):
        self.executor = get_vapt_executor()
        self.recon = ReconOrchestrator(self.executor)
        self.researcher = ResearcherAgent()
        self.verifier = VerifierAgent()

    async def analyze_and_scan(self, target: str, scan_type: str = "auto") -> VAPTScanResult:
        """Analyze target and run appropriate scan."""
        target_info = self._analyze_target(target)
        scan_type = self._determine_scan_type(scan_type, target_info)
        tools = self._select_tools(scan_type, target_info)

        request = VAPTScanRequest(
            target=VAPTTarget(value=target, type=target_info["type"]),
            scan_type=scan_type,
            tools=tools,
        )

        result = await self.recon.execute_scan(request)

        result.findings = await self.researcher.enrich_findings(result.findings)

        result.findings = await self.verifier.verify_findings(result.findings)

        return result

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