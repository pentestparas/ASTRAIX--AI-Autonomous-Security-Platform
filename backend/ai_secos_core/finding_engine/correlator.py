"""Finding Correlator — the contract + the no-op default.

Correlators detect patterns across findings: chained exploits, repeated
attack-path components, MITRE technique sequences. Real implementations
land in a later milestone.
"""

from __future__ import annotations

import abc
from typing import Iterable

from ai_secos_core.shared.value_objects import SecurityFinding


class FindingCorrelator(abc.ABC):
    """Adds correlation metadata to findings."""

    @abc.abstractmethod
    async def correlate(
        self, findings: Iterable[SecurityFinding]
    ) -> list[SecurityFinding]:
        """Return the same set of findings, possibly tagged with correlation."""
        raise NotImplementedError


class NoopFindingCorrelator:
    """Identity correlator. The default at Milestone 1."""

    async def correlate(
        self, findings: Iterable[SecurityFinding]
    ) -> list[SecurityFinding]:
        return list(findings)


__all__ = [
    "FindingCorrelator",
    "NoopFindingCorrelator",
]
