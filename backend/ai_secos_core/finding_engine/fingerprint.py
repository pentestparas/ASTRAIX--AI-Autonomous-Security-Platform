"""Deterministic fingerprinting contract.

Two findings with identical `(asset, cwe, cve, plugin)` collapse to one
canonical record. Fingerprints are stable across processes, machines,
and languages so the deduplicator can dedupe across the platform.
"""

from __future__ import annotations

import abc
import hashlib
from dataclasses import dataclass
from typing import Iterable

from ai_secos_core.config.constants import DEFAULT_DEDUPE_HASH_BYTES
from ai_secos_core.shared.value_objects import FindingFingerprint, SecurityFinding


class FindingFingerprinter(abc.ABC):
    """Computes fingerprints for findings."""

    @abc.abstractmethod
    def fingerprint(self, finding: SecurityFinding) -> FindingFingerprint: ...


@dataclass(frozen=True)
class DefaultFindingFingerprinter:
    """Default deterministic fingerprinter.

    The hash is built from fields that uniquely identify the same
    underlying finding. Free-form metadata is deliberately excluded.
    """

    hash_bytes: int = DEFAULT_DEDUPE_HASH_BYTES

    def fingerprint(self, finding: SecurityFinding) -> FindingFingerprint:
        ident = {
            "asset": str(finding.asset),
            "plugin": str(finding.plugin),
            "cwe": self._sorted(finding.cwe),
            "cve": self._sorted(finding.cve),
            "category": finding.category,
        }
        digest = hashlib.sha256(
            self._canonical_bytes(ident)
        ).digest()[: self.hash_bytes]
        return FindingFingerprint(digest.hex())

    @staticmethod
    def _sorted(values: Iterable[str]) -> list[str]:
        return sorted(values)

    @staticmethod
    def _canonical_bytes(payload: dict[str, object]) -> bytes:
        """Stable byte representation (sorted keys, list-of-tuples)."""
        import json

        return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


__all__ = [
    "FindingFingerprinter",
    "DefaultFindingFingerprinter",
]
