"""Finding Enricher — the contract and the no-op default.

Enrichers attach additional context to findings: asset criticality,
intel-feed matches, threat-model tilt, etc. Real implementations
land in a later milestone; here we ship the contract + a no-op so the
pipeline compiles.
"""

from __future__ import annotations

import abc

from ai_secos_core.shared.value_objects import SecurityFinding


class FindingEnricher(abc.ABC):
    """Augments a single canonical SecurityFinding with external context."""

    @abc.abstractmethod
    async def enrich(self, finding: SecurityFinding) -> SecurityFinding:
        """Return a new (or in-place enriched) finding."""
        raise NotImplementedError


class NoopFindingEnricher:
    """Identity enricher. The default at Milestone 1."""

    async def enrich(self, finding: SecurityFinding) -> SecurityFinding:
        return finding


__all__ = [
    "FindingEnricher",
    "NoopFindingEnricher",
]
