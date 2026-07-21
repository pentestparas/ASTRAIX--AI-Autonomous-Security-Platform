"""
Scanner Executor Service

Enterprise-grade scanner execution with:
- Async tool execution
- Resource management
- Docker container isolation
- Result aggregation
- Retry logic
"""

import asyncio
import hashlib
import json
import logging
import os
import re
import subprocess
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from app.scanner.models import (
    Finding,
    ScanRequest,
    ScanResult,
    ScanStatus,
    Severity,
    ToolCapability,
    ToolResult,
)
from app.scanner.vapt_platforms import (
    KALI_TOOLS,
    PlatformConfig,
    PlatformType,
    ScanOrchestrator,
    VAPTExecutor,
    VAPTOutputParser,
    create_dark_moon_executor,
    create_kali_executor,
    create_pentagi_executor,
)

logger = logging.getLogger(__name__)


class ScannerExecutor:
    """
    Main scanner execution service.

    Features:
    - Multi-tool execution with Docker isolation
    - Output parsing for 15+ security tools
    - Result deduplication
    - Async execution
    """

    def __init__(self):
        self._tool_registry = KALI_TOOLS.copy()
        self._parsers = VAPTOutputParser()

    async def run_scan(self, scan_request: ScanRequest) -> ScanResult:
        """Execute a complete security scan."""
        logger.info(f"Starting scan for target: {scan_request.target}")

        result = ScanResult(
            id=uuid4(),
            status=ScanStatus.RUNNING,
            target=scan_request.target,
            capability=scan_request.capability,
            started_at=datetime.utcnow(),
        )

        # Create executor based on request
        executor = self._create_executor(scan_request)

        # Get tools for this scan
        tools = self._get_tools(scan_request)

        if not tools:
            result.finalize(ScanStatus.FAILED, "No suitable tools found")
            return result

        # Execute tools
        try:
            tool_results = await executor.execute_tools_parallel(
                tools,
                scan_request.target,
                context=self._build_context(scan_request)
            )

            # Aggregate findings
            for tr in tool_results:
                result.add_tool_result(tr)

            # Deduplicate findings
            result.findings = self._deduplicate_findings(result.findings)

            # Determine status
            if result.findings_count > 0:
                result.finalize(ScanStatus.COMPLETED, f"Scan completed with {result.findings_count} findings")
            elif result.errors:
                result.finalize(ScanStatus.PARTIAL, f"Completed with {len(result.errors)} errors")
            else:
                result.finalize(ScanStatus.COMPLETED, "Scan completed, no findings")

        except Exception as e:
            logger.error(f"Scan failed: {e}")
            result.errors.append(str(e))
            result.finalize(ScanStatus.FAILED, str(e))

        return result

    async def run_single_tool(
        self,
        tool_id: str,
        target: str,
        deep: bool = False,
        **kwargs
    ) -> ToolResult:
        """Execute a single tool."""
        if tool_id not in self._tool_registry:
            raise ValueError(f"Unknown tool: {tool_id}")

        tool = self._tool_registry[tool_id]
        executor = create_kali_executor()

        return await executor.execute_tool(tool, target, {"deep": deep, **kwargs})

    def _create_executor(self, scan_request: ScanRequest) -> VAPTExecutor:
        """Create appropriate executor for scan request."""
        # Check for external platform integration
        platform = os.environ.get("VAPT_PLATFORM", "kali")

        if platform == "dark-moon":
            base_url = os.environ.get("DARK_MOON_URL", "http://localhost:8080")
            api_key = os.environ.get("DARK_MOON_API_KEY", "")
            return create_dark_moon_executor(base_url, api_key)
        elif platform == "pentagi":
            base_url = os.environ.get("PENTAGI_URL", "http://localhost:8443")
            api_key = os.environ.get("PENTAGI_API_KEY", "")
            return create_pentagi_executor(base_url, api_key)
        else:
            return create_kali_executor()

    def _get_tools(self, scan_request: ScanRequest) -> List[Any]:
        """Get tools for a scan request."""
        from app.scanner.vapt_platforms import ExternalTool

        tools: List[ExternalTool] = []

        # Add explicitly requested tools
        for tool_id in scan_request.tools:
            if tool_id in self._tool_registry:
                tools.append(self._tool_registry[tool_id])

        # If no tools specified, use defaults for capability
        if not tools:
            defaults = self._get_default_tools(scan_request.capability)
            for tool_id in defaults:
                if tool_id in self._tool_registry:
                    tools.append(self._tool_registry[tool_id])

        # Apply deep/aggressive flags to tool configs
        for tool in tools:
            if scan_request.deep:
                tool.args.extend(["-Tuning", "1,2,3,4,5,6,7,8,9"])
            if scan_request.aggressive and tool.name == "nmap":
                tool.args.append("-A")

        return tools

    def _get_default_tools(self, capability: ToolCapability) -> List[str]:
        """Get default tools for a capability."""
        defaults = {
            ToolCapability.NETWORK_VAPT: ["nmap", "masscan", "dnsrecon"],
            ToolCapability.WEB_VAPT: ["nikto", "sqlmap", "nuclei", "gobuster", "ffuf"],
            ToolCapability.CLOUD_SECURITY: ["prowler", "scoutsuite"],
            ToolCapability.CODE_AUDIT: ["semgrep", "bandit"],
            ToolCapability.CONTAINER_SECURITY: ["trivy"],
            ToolCapability.API_SECURITY: ["sqlmap", "nuclei", "ffuf"],
            ToolCapability.SSL_SECURITY: ["sslscan", "testssl"],
            ToolCapability.DNS_RECON: ["dnsrecon", "theHarvester"],
        }
        return defaults.get(capability, ["nmap"])

    def _build_context(self, scan_request: ScanRequest) -> Dict[str, Any]:
        """Build execution context for tools."""
        return {
            "deep": scan_request.deep,
            "aggressive": scan_request.aggressive,
            "organization_id": str(scan_request.organization_id) if scan_request.organization_id else None,
            "project_id": str(scan_request.project_id) if scan_request.project_id else None,
            "assessment_id": str(scan_request.assessment_id) if scan_request.assessment_id else None,
        }

    def _deduplicate_findings(self, findings: List[Finding]) -> List[Finding]:
        """Remove duplicate findings based on fingerprint."""
        seen = set()
        unique = []

        for finding in findings:
            fingerprint = self._compute_fingerprint(finding)
            if fingerprint not in seen:
                seen.add(fingerprint)
                unique.append(finding)

        return unique

    def _compute_fingerprint(self, finding: Finding) -> str:
        """Compute unique fingerprint for a finding."""
        key = f"{finding.target}:{finding.title}:{finding.severity}:{finding.tool_name}"
        if finding.port:
            key += f":{finding.port}"
        if finding.parameter:
            key += f":{finding.parameter}"
        return hashlib.sha256(key.encode()).hexdigest()[:32]


class ToolAvailabilityChecker:
    """Check which tools are available in the environment."""

    @staticmethod
    def check_tool(tool_id: str) -> bool:
        """Check if a specific tool is available."""
        if tool_id not in KALI_TOOLS:
            return False

        tool = KALI_TOOLS[tool_id]
        try:
            result = subprocess.run(
                ["which", tool.command],
                capture_output=True,
                timeout=5,
            )
            return result.returncode == 0
        except Exception:
            return False

    @staticmethod
    def check_docker() -> bool:
        """Check if Docker is available."""
        try:
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                timeout=5,
            )
            return result.returncode == 0
        except Exception:
            return False

    @staticmethod
    def get_available_tools() -> Dict[str, bool]:
        """Get availability status of all tools."""
        return {
            tool_id: ToolAvailabilityChecker.check_tool(tool_id)
            for tool_id in KALI_TOOLS
        }

    @staticmethod
    def get_health_status() -> Dict[str, Any]:
        """Get overall health status of the scanner."""
        docker_available = ToolAvailabilityChecker.check_docker()
        tools_available = sum(
            1 for tid in KALI_TOOLS
            if ToolAvailabilityChecker.check_tool(tid)
        )
        total_tools = len(KALI_TOOLS)

        return {
            "docker_available": docker_available,
            "tools_available": tools_available,
            "total_tools": total_tools,
            "health": "healthy" if docker_available and tools_available > 0 else "degraded",
            "missing_tools": [
                tid for tid in KALI_TOOLS
                if not ToolAvailabilityChecker.check_tool(tid)
            ],
        }


# Singleton instance
_scanner_executor: Optional[ScannerExecutor] = None


def get_scanner_executor() -> ScannerExecutor:
    """Get the global scanner executor instance."""
    global _scanner_executor
    if _scanner_executor is None:
        _scanner_executor = ScannerExecutor()
    return _scanner_executor