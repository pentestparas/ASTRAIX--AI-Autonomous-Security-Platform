"""Finding Engine — the pipeline orchestrator.

Pipeline order (matches ARCHITECTURE.md):

  1. **Normalize** (plugin-specific output → canonical `SecurityFinding`)
  2. **Deduplicate** (fingerprint-based collapse)
  3. **Enrich** (asset context, intel)
  4. **Correlate** (cross-plugin / cross-asset)

Each stage is an injectable. The engine is trivially testable, and
swapping the default stage implementations is a one-line change.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass

from ai_secos_core.finding_engine.correlator import (
    FindingCorrelator,
    NoopFindingCorrelator,
)
from ai_secos_core.finding_engine.deduplicator import FindingDeduplicator
from ai_secos_core.finding_engine.enricher import FindingEnricher, NoopFindingEnricher
from ai_secos_core.finding_engine.normalizer import (
    FindingNormalizer,
    NormalizerRegistry,
)
from ai_secos_core.shared.value_objects import (
    AssessmentId,
    CapabilityId,
    SecurityFinding,
)


@dataclass(frozen=True)
class FindingEngineConfig:
    """Toggles that do not require a new class."""

    normalized_required: bool = True
    dedupe_enabled: bool = True


@dataclass(frozen=True)
class FindingEngineContext:
    """The context fields a Finding needs to exist at all."""

    assessment_id: AssessmentId
    capability_id: CapabilityId
    asset_id: str


class FindingEngine(abc.ABC):
    """Orchestrates the pipeline for one or more raw plugin results."""

    @abc.abstractmethod
    async def process(
        self,
        plugin_id: str,
        raw_output: dict[str, object],
        context: FindingEngineContext,
    ) -> list[SecurityFinding]:
        """Run the full pipeline on one plugin's raw output.

        Returns deduplicated canonical findings.
        """
        raise NotImplementedError


@dataclass
class DefaultFindingEngine:
    """Default pipeline implementation. All collaborators are injectable."""

    normalizers: NormalizerRegistry
    deduplicator: FindingDeduplicator
    enricher: FindingEnricher | None = None
    correlator: FindingCorrelator | None = None
    config: FindingEngineConfig | None = None

    def __post_init__(self) -> None:
        # Rebind dataclass-style to avoid overriding freezed defaults.
        # We deliberately keep these public so callers can introspect.
        self.enricher = self.enricher or NoopFindingEnricher()
        self.correlator = self.correlator or NoopFindingCorrelator()
        self.config = self.config or FindingEngineConfig()

    async def process(
        self,
        plugin_id: str,
        raw_output: dict[str, object],
        context: FindingEngineContext,
    ) -> list[SecurityFinding]:
        normalizer: FindingNormalizer = self.normalizers.get(plugin_id)
        raw_findings = list(
            normalizer.normalize(
                raw_output,
                assessment_id=context.assessment_id,
                capability_id=context.capability_id,
                asset_id=context.asset_id,
            )
        )
        if self.config.normalized_required and not raw_findings:
            return []

        if self.config.dedupe_enabled:
            merged: list[SecurityFinding] = []
            for finding in raw_findings:
                stored, _ = self.deduplicator.ingest(finding)
                merged.append(stored)
        else:
            merged = raw_findings

        enriched: list[SecurityFinding] = []
        for finding in merged:
            enriched.append(await self.enricher.enrich(finding))

        return await self.correlator.correlate(enriched)


__all__ = [
    "FindingEngine",
    "DefaultFindingEngine",
    "FindingEngineConfig",
    "FindingEngineContext",
]
