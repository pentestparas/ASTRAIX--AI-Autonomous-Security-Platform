"""
Orchestrator Service

The orchestrator runs assessments via the plugin system:
  1. Load asset → assessment context
  2. Resolve plugins (e.g., network, web, cloud)
  3. Run plugins in parallel/sequence
  4. Process findings (deduplication, scoring)
  5. Persist findings
"""

import asyncio
import uuid
from datetime import datetime
from typing import List, Optional, Union, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.assessment import Assessment
from app.domain.models.finding import Finding
from app.plugins.registry import PluginRegistry
from app.domain.models.plugin import PluginOutput, PluginError
from app.database import repositories as repos
from app.core.logging import get_logger

logger = get_logger(__name__)


class AssessmentStatus:
    """Assessment lifecycle states."""
    PENDING = "pending"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Orchestrator:
    """Sequences assessment execution: plugins → findings."""

    def __init__(self, plugin_registry: PluginRegistry):
        self.registry = plugin_registry

    async def run_assessment(
        self,
        db: AsyncSession,
        assessment_id: uuid.UUID,
    ) -> Optional[Assessment]:
        """Execute an assessment by ID."""
        assessment = await repos.assessment.get(db, assessment_id)
        if not assessment:
            logger.warn("assessment.not_found", id=str(assessment_id))
            return None

        # Update: scheduled → running
        assessment.status = AssessmentStatus.RUNNING
        assessment.started_at = datetime.utcnow()
        await repos.assessment.update(db, assessment)

        try:
            # Resolve plugins → run
            plugin_ids = self._resolve_plugins(assessment)
            tasks = [
                self._run_plugin(plugin, assessment)
                for plugin in plugin_ids
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process findings: dedup, persist
            findings_count = await self._process_results(db, assessment, results)

            assessment.status = AssessmentStatus.COMPLETED
            assessment.completed_at = datetime.utcnow()
            assessment.findings_count = findings_count
            await repos.assessment.update(db, assessment)

            logger.info("orchestrator.completed", id=str(assessment_id), findings=findings_count)
            return assessment

        except Exception as exc:
            logger.error("orchestrator.failed", id=str(assessment_id), exc=exc)
            assessment.status = AssessmentStatus.FAILED
            assessment.error = str(exc)
            await repos.assessment.update(db, assessment)
            return assessment

    def _resolve_plugins(self, assessment: Assessment) -> List[str]:
        """Resolve plugins based on assessment metadata."""
        explicit = assessment.config.get("plugins") if assessment.config else None
        if explicit:
            return explicit
        # Default: plugins matching asset/assessment type
        return self._auto_select_plugins(assessment)

    def _auto_select_plugins(self, assessment: Assessment) -> List[str]:
        """Default plugin selection."""
        asset_type = assessment.asset.type if assessment.asset else "unknown"
        rule_map = {
            "ipv4": ["scanners/nmap-ipv4"],
            "application": ["scanners/nmap-ipv4", "scanners/nuclei-templates"],
            "cloud": ["scanners/cloud-config"],
            "container": ["scanners/trivy-image"],
        }
        return rule_map.get(asset_type, [])

    async def _run_plugin(
        self,
        plugin_id: str,
        assessment: Assessment,
    ) -> Union[PluginOutput, PluginError, Exception]:
        """Run a single plugin."""
        params = self._build_params(assessment)
        return await self.registry.run_plugin(plugin_id, params)

    def _build_params(self, assessment: Assessment) -> dict:
        """Build plugin invocation params from assessment."""
        return {
            "asset": assessment.asset.identifier if assessment.asset else "",
            "deep": assessment.config.get("deep", False) if assessment.config else False,
            "flags": assessment.config.get("flags", "") if assessment.config else "",
        }

    async def _process_results(
        self,
        db: AsyncSession,
        assessment: Assessment,
        results: List[Union[PluginOutput, PluginError, Exception]],
    ) -> int:
        """Persist plugins' findings."""
        findings = []
        for result in results:
            if isinstance(result, Exception):
                continue
            if isinstance(result, PluginError):
                continue
            for fo in result.findings:
                fingerprint = self._fingerprint_finding(assessment, fo)
                existing = await repos.finding.find_by_fingerprint(db, fingerprint)
                if existing:
                    continue
                f = Finding(
                    id=uuid.uuid4(),
                    assessment_id=assessment.id,
                    plugin_id=result.plugin_id,
                    severity=fo.severity,
                    title=fo.title,
                    asset_id=assessment.asset_id,
                    details=fo.details,
                    remediation=fo.remediation,
                    reference=fo.reference,
                    fingerprint=fingerprint,
                    created_at=datetime.utcnow(),
                )
                findings.append(f)
        if findings:
            await repos.finding.create_many(db, findings)
        return len(findings)

    def _fingerprint_finding(self, assessment: Assessment, finding: Finding) -> str:
        """Generate fingerprint: title + asset + plugin + severity."""
        content = (
            f"{assessment.id}:{assessment.asset_id}:"
            f"{finding.title}:{finding.severity}"
        )
        return uuid.uuid5(uuid.NAMESPACE_DNS, content).hex