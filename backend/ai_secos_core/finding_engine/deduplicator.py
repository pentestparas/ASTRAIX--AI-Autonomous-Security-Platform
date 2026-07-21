"""Deduplication: collapsing equivalent findings.

Two findings with the same fingerprint are considered the same finding
observed twice (or more times). The deduplicator retains the highest
severity, latest `last_seen`, and merges evidence.

The interface is small: callers pass findings one at a time; the
stateful deduplicator returns either a `SecurityFinding` (new) or
the merged `SecurityFinding` (existing).
"""

from __future__ import annotations

import abc
from datetime import datetime, timezone
from typing import Iterable

from ai_secos_core.finding_engine.fingerprint import (
    DefaultFindingFingerprinter,
    FindingFingerprinter,
)
from ai_secos_core.shared.value_objects import (
    FindingFingerprint,
    SecurityFinding,
    Severity,
)


class FindingDeduplicator(abc.ABC):
    """Stateful dedupe of findings by fingerprint."""

    @abc.abstractmethod
    def ingest(self, finding: SecurityFinding) -> tuple[SecurityFinding, bool]:
        """Insert one finding.

        Returns `(stored_finding, was_new)`. When `was_new=False`,
        `stored_finding` is the merged record (severity promoted where
        appropriate, `last_seen` updated, evidence new, etc.).
        """
        raise NotImplementedError

    @abc.abstractmethod
    def known(self, finding: SecurityFinding) -> bool: ...

    @abc.abstractmethod
    def all(self) -> list[SecurityFinding]: ...

    @abc.abstractmethod
    def reset(self) -> None: ...


_SEV_ORDER = {
    Severity.INFO: 0,
    Severity.LOW: 1,
    Severity.MEDIUM: 2,
    Severity.HIGH: 3,
    Severity.CRITICAL: 4,
}


def _promote_severity(a: Severity, b: Severity) -> Severity:
    return a if _SEV_ORDER[a] >= _SEV_ORDER[b] else b


class DefaultFindingDeduplicator:
    """In-memory implementation.

    Suitable for single-process Milestone 1 / Milestone 2 runs. A
    persistent (Postgres-backed) deduplicator is a later concern.
    """

    def __init__(self, fingerprinter: FindingFingerprinter | None = None) -> None:
        self._fingerprinter: FindingFingerprinter = (
            fingerprinter or DefaultFindingFingerprinter()
        )
        self._index: dict[FindingFingerprint, SecurityFinding] = {}

    def ingest(self, finding: SecurityFinding) -> tuple[SecurityFinding, bool]:
        fp = self._fingerprinter.fingerprint(finding)
        marked = finding.model_copy(update={"fingerprint": fp})
        existing = self._index.get(fp)
        if existing is None:
            self._index[fp] = marked
            return marked, True
        merged = _merge(existing, marked)
        self._index[fp] = merged
        return merged, False

    def known(self, finding: SecurityFinding) -> bool:
        fp = self._fingerprinter.fingerprint(finding)
        return fp in self._index

    def all(self) -> list[SecurityFinding]:
        return sorted(
            self._index.values(),
            key=lambda f: (f.last_seen, f.severity.value),
            reverse=True,
        )

    def reset(self) -> None:
        self._index.clear()


def _merge(prev: SecurityFinding, curr: SecurityFinding) -> SecurityFinding:
    """Merge a re-observed finding with its prior canonical record.

    Strategy:
      - Severity: promote to higher of the two.
      - Confidence: take max.
      - first_seen / last_seen: bracket.
      - evidence: prefer the current (most-recent) raw.
      - tags / metadata / cvss / cwe / cve / owasp: union, deduped.
    """
    promoted = _promote_severity(prev.severity, curr.severity)
    return prev.model_copy(
        update={
            "severity": promoted,
            "confidence": max(prev.confidence, curr.confidence),
            "first_seen": min(prev.first_seen, curr.first_seen),
            "last_seen": max(prev.last_seen, curr.last_seen)
            or datetime.now(timezone.utc),
            "evidence": curr.evidence or prev.evidence,
            "tags": sorted(set(prev.tags) | set(curr.tags)),
            "metadata": {**(prev.metadata or {}), **(curr.metadata or {})},
            "cvss": _max_or_none(prev.cvss, curr.cvss),
            "cwe": sorted(set(prev.cwe) | set(curr.cwe)),
            "cve": sorted(set(prev.cve) | set(curr.cve)),
            "owasp": sorted(set(prev.owasp) | set(curr.owasp)),
        }
    )


def _max_or_none(a: float | None, b: float | None) -> float | None:
    vals = [v for v in (a, b) if v is not None]
    if not vals:
        return None
    return max(vals)


__all__ = [
    "FindingDeduplicator",
    "DefaultFindingDeduplicator",
]
