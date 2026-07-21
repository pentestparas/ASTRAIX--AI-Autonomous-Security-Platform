"""
Orchestrator Service

Coordinates plugins, assessments, and findings.

Responsibilities:
  - Load plugins via PluginRegistry
  - Run assessments (sync + async)
  - Process & persist findings
  - Schedule (future)
  - Execute VAPT tools (Kali Linux, Dark-Moon, PentAGI)
"""

from __future__ import annotations

import asyncio
import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.plugins import PluginRegistry
from app.plugins.registry import PluginRunResult
from app.domain.models.finding import Finding
from app.domain.models.assessment import Assessment
from app.domain.models.asset import Asset
from app.repositories import assessment_repo, asset_repo, finding_repo
from app.core.logging import get_logger
from app.scanner.executor import get_scanner_executor, ScannerExecutor
from app.scanner.models import ToolCapability

logger = get_logger(__name__)


class AssessmentStatus(str, Enum):
    """Assessment lifecycle."""

    PENDING = "pending"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Orchestrator:
    """Coordinator: schedules + runs assessments."""

    def __init__(self, plugin_registry: PluginRegistry, scanner_executor: ScannerExecutor = None):
        self.plugins = plugin_registry
        self.scanner = scanner_executor or get_scanner_executor()
        self._use_vapt_executor = True  # Use real VAPT tools when available

    async def run_assessment(
        self,
        db: AsyncSession,
        assessment_id: UUID,
    ) -> Assessment:
        """Run an assessment by ID. Updates state as we progress."""
        assessment = await assessment_repo.get(db, assessment_id)
        if not assessment:
            raise ValueError(f"Assessment not found: {assessment_id}")

        # PENDING → RUNNING
        assessment.status = AssessmentStatus.RUNNING.value
        assessment.started_at = datetime.utcnow()
        await assessment_repo.update(db, assessment)

        try:
            asset = await asset_repo.get(db, assessment.asset_id)
            if not asset:
                raise ValueError(f"Asset not found: {assessment.asset_id}")

            # Use VAPT scanner if enabled and available
            if self._use_vapt_executor:
                findings_count = await self._run_vapt_scan(db, assessment, asset)
            else:
                # Fall back to plugin system
                findings_count = await self._run_plugin_scan(db, assessment, asset)

            assessment.findings_count = findings_count

            # RUNNING → COMPLETED
            assessment.status = AssessmentStatus.COMPLETED.value
            assessment.completed_at = datetime.utcnow()
            await assessment_repo.update(db, assessment)

            logger.info(
                "assessment.completed",
                id=str(assessment_id),
                findings=findings_count,
            )
            return assessment

        except Exception as exc:
            logger.error("assessment.failed", id=str(assessment_id), exc=str(exc))
            assessment.status = AssessmentStatus.FAILED.value
            assessment.error = str(exc)
            assessment.completed_at = datetime.utcnow()
            await assessment_repo.update(db, assessment)
            raise

    async def _run_vapt_scan(
        self,
        db: AsyncSession,
        assessment: Assessment,
        asset: Asset,
    ) -> int:
        """
        Run real VAPT scan using Kali Linux tools.
        This is the enterprise-grade implementation that actually executes tools.
        """
        from app.scanner.models import ScanRequest, ToolCapability

        # Map asset type to capability
        capability_map = {
            "ipv4": ToolCapability.NETWORK_VAPT,
            "ipv6": ToolCapability.NETWORK_VAPT,
            "domain": ToolCapability.WEB_VAPT,
            "url": ToolCapability.WEB_VAPT,
            "web": ToolCapability.WEB_VAPT,
            "application": ToolCapability.WEB_VAPT,
            "cloud": ToolCapability.CLOUD_SECURITY,
            "aws": ToolCapability.CLOUD_SECURITY,
            "azure": ToolCapability.CLOUD_SECURITY,
            "gcp": ToolCapability.CLOUD_SECURITY,
            "container": ToolCapability.CONTAINER_SECURITY,
            "docker": ToolCapability.CONTAINER_SECURITY,
            "code": ToolCapability.CODE_AUDIT,
            "api": ToolCapability.API_SECURITY,
            "ssl": ToolCapability.SSL_SECURITY,
        }

        # Map assessment type to tools
        tool_map = {
            "network_vapt": ["nmap", "masscan", "dnsrecon"],
            "web_vapt": ["nikto", "sqlmap", "nuclei", "gobuster", "ffuf"],
            "cloud_posture": ["prowler", "scoutsuite"],
            "code_audit": ["semgrep", "bandit"],
            "container_scan": ["trivy"],
            "ssl_audit": ["sslscan", "testssl"],
        }

        # Get capability and tools
        capability = capability_map.get(asset.type, ToolCapability.NETWORK_VAPT)
        config = assessment.config or {}
        tools = config.get("tools", tool_map.get(assessment.type, ["nmap"]))

        # Create scan request
        scan_request = ScanRequest(
            target=asset.identifier,
            tools=tools,
            capability=capability,
            deep=config.get("deep", False),
            aggressive=config.get("aggressive", False),
            organization_id=assessment.organization_id,
            project_id=assessment.project_id,
            assessment_id=assessment.id,
        )

        # Execute scan
        logger.info(f"Executing VAPT scan: {len(tools)} tools on {asset.identifier}")
        scan_result = await self.scanner.run_scan(scan_request)

        # Persist findings
        count = 0
        for finding in scan_result.findings:
            # Convert to domain finding model
            domain_finding = Finding(
                id=uuid.uuid4(),
                organization_id=assessment.organization_id,
                project_id=assessment.project_id,
                assessment_id=assessment.id,
                asset_id=asset.id,
                plugin_id=f"vapt/{finding.tool_name}",
                severity=finding.severity.value,
                title=finding.title,
                description=finding.description,
                details=finding.details,
                cvss_score=finding.cvss_score,
                remediation=finding.remediation,
                reference=finding.reference,
                fingerprint=finding.id.hex,  # Use the Finding's UUID as fingerprint
                status="open",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            await finding_repo.create(db, domain_finding)
            count += 1

        logger.info(f"VAPT scan completed: {count} findings from {len(scan_result.tool_results)} tools")
        return count

    async def _run_plugin_scan(
        self,
        db: AsyncSession,
        assessment: Assessment,
        asset: Asset,
    ) -> int:
        """Run scan using the plugin system (fallback)."""
        plugin_ids = self._resolve_plugins(assessment, asset)
        results = await self._run_plugins(plugin_ids, asset, assessment)
        return await self._persist_findings(db, assessment, results)

    async def _persist_findings(
        self,
        db: AsyncSession,
        assessment: Assessment,
        results: List[PluginRunResult],
    ) -> int:
        """Process plugin findings, dedupe, persist."""
        count = 0
        for result in results:
            if not result.success or not result.output:
                continue
            for fo in result.output.findings:
                fingerprint = self._fingerprint(assessment, fo)
                exists = await finding_repo.find_by_fingerprint(db, fingerprint)
                if exists:
                    continue
                finding = Finding(
                    id=uuid.uuid4(),
                    assessment_id=assessment.id,
                    asset_id=assessment.asset_id,
                    plugin_id=result.manifest.id,
                    severity=fo.severity,
                    title=fo.title,
                    description=fo.description,
                    details=fo.details,
                    remediation=fo.remediation,
                    reference=fo.reference,
                    fingerprint=fingerprint,
                    status="open",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                await finding_repo.create(db, finding)
                count += 1
        return count

    def _fingerprint(self, assessment: Assessment, finding) -> str:
        """Stable identifier: title + asset."""
        key = f"{assessment.asset_id}:{finding.title}:{finding.severity}"
        return uuid.uuid5(uuid.NAMESPACE_DNS, key).hex


_orchestrator: Optional[Orchestrator] = None


async def get_orchestrator() -> Orchestrator:
    """Singleton orchestrator."""
    global _orchestrator
    if _orchestrator is None:
        registry = await get_plugin_registry()
        _orchestrator = Orchestrator(registry)
    return _orchestrator