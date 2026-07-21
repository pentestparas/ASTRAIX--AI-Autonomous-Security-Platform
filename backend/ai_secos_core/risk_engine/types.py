"""Typed outputs of the Risk Engine.

A `RiskScore` is a 0–100 value clipped and bounding-checked at the
domain boundary. A `RiskSignals` bundle carries the per-axis values
that produced it (so the AI and reporting layers can explain *why*).

Two ways to model the underlying severity used at the entry side:

  - `Severity` is re-exported from the shared `value_objects` module
    so callers do not need to import from two places.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from ai_secos_core.shared.value_objects import Severity

# Re-export the canonical severity enum here for ergonomic imports.
__all__ = ["Severity", "RiskScore", "RiskFactorSource", "RiskFactor", "RiskSignals"]


class RiskFactorSource(str, Enum):
    """Where a risk axis got its number."""

    LIKELIHOOD = "likelihood"
    IMPACT = "impact"
    EXPLOITABILITY = "exploitability"
    BUSINESS_CONTEXT = "business_context"


@dataclass(frozen=True)
class RiskFactor:
    """One contribution to the total risk score."""

    source: RiskFactorSource
    value: float    # 0.0 – 1.0 (each axis's individual score)
    weight: float   # configuration-driven
    rationale: str = ""

    @property
    def weighted(self) -> float:
        return self.value * self.weight


@dataclass(frozen=True)
class RiskScore:
    """Numeric, bounded 0–100 risk.

    Use `.factors` to display *why* the score is what it is.
    """

    value: int
    factors: tuple[RiskFactor, ...] = ()

    @classmethod
    def build(cls, factors: Iterable[RiskFactor]) -> "RiskScore":
        raw = sum(f.weighted for f in factors)
        bounded = int(max(0, min(100, round(raw * 100))))
        return cls(value=bounded, factors=tuple(factors))


@dataclass(frozen=True)
class RiskSignals:
    """The bundle the Risk Engine asks of each provider."""

    asset: str
    severity: Severity
    confidence: float
    cvss: float | None
    cve: tuple[str, ...]
    cwe: tuple[str, ...]
    owasp: tuple[str, ...]
    public_exploit_known: bool = False
    business_criticality: float = 0.5   # 0.0…1.0 — injected by Application
