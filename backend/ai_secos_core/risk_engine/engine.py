"""Risk Engine — pipeline orchestrator and entry points.

Two implementations are shipped at Milestone 1:

  - `NoopRiskEngine`: skips sub-axes; derives score directly from
    canonical `Severity`. Useful for tests and as a fallback.
  - `DefaultRiskEngine`: full likelihood/impact/exploitability/business
    pipeline with the four `StaticRiskSignalProvider`s.

Both are pluggable via the `RiskEngine` protocol.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Iterable, Sequence

from ai_secos_core.risk_engine.providers import (
    RiskSignalProvider,
    StaticRiskSignalProvider,
)
from ai_secos_core.risk_engine.types import (
    RiskFactor,
    RiskFactorSource,
    RiskScore,
    RiskSignals,
)
from ai_secos_core.shared.value_objects import SecurityFinding, Severity

# Severity → deterministic 0–100 midpoint for the noop path.
_NOOP_SEVERITY_MIDPOINT: dict[Severity, int] = {
    Severity.INFO: 5,
    Severity.LOW: 25,
    Severity.MEDIUM: 50,
    Severity.HIGH: 75,
    Severity.CRITICAL: 95,
}


def _noop_severity_to_score(severity: Severity) -> int:
    return _NOOP_SEVERITY_MIDPOINT[severity]


@dataclass(frozen=True)
class RiskEngineResult:
    """A scored finding (or a typed wrapper around a SecurityFinding)."""

    finding: SecurityFinding
    score: RiskScore


class RiskEngine(abc.ABC):
    """Engine port: score one or more canonical findings."""

    @abc.abstractmethod
    async def score(self, findings: Iterable[SecurityFinding]) -> list[RiskEngineResult]:
        """Score each canonical finding."""
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Default implementation


@dataclass
class DefaultRiskEngine:
    """Full Likelihood/Impact/Exploitability/Business pipeline.

    Providers are injectable. Weights are configuration-driven via the
    `weights` param — kept as a dict so the platform's `RiskEngineSettings`
    can plug in directly at the DI boundary.
    """

    providers: Sequence[RiskSignalProvider]
    # weights keyed by `RiskFactorSource.value`.
    weights: dict[str, float] | None = None

    def __post_init__(self) -> None:
        # Default weights from `RiskEngineSettings` (kept here for self-
        # containment); DI may override this dict at construction.
        if self.weights is None:
            self.weights = {
                "likelihood": 0.25,
                "impact": 0.35,
                "exploitability": 0.25,
                "business_context": 0.15,
            }

    async def score(
        self,
        findings: Iterable[SecurityFinding],
    ) -> list[RiskEngineResult]:
        out: list[RiskEngineResult] = []
        for finding in findings:
            signals = self._to_signals(finding)
            factors = self._evaluate(signals)
            score = RiskScore.build(factors)
            out.append(
                RiskEngineResult(
                    finding=finding.model_copy(update={"risk_score": float(score.value)}),
                    score=score,
                )
            )
        return out

    # ---- internals --------------------------------------------------------

    def _to_signals(self, finding: SecurityFinding) -> RiskSignals:
        return RiskSignals(
            asset=str(finding.asset),
            severity=finding.severity,
            confidence=finding.confidence,
            cvss=finding.cvss,
            cve=tuple(finding.cve),
            cwe=tuple(finding.cwe),
            owasp=tuple(finding.owasp),
            public_exploit_known=False,   # intel-coupling is post-M1
            business_criticality=0.5,     # overridden by Application context
        )

    def _evaluate(self, signals: RiskSignals) -> list[RiskFactor]:
        factors: list[RiskFactor] = []
        for provider in self.providers:
            f = provider.evaluate(signals)
            w = self.weights.get(f.source.value, f.weight)
            factors.append(
                RiskFactor(
                    source=f.source,
                    value=f.value,
                    weight=w,
                    rationale=f.rationale,
                )
            )
        # Ensure all four sources are present (filled with zero if absent).
        present = {f.source for f in factors}
        for source in RiskFactorSource:
            if source not in present:
                factors.append(
                    RiskFactor(
                        source=source,
                        value=0.0,
                        weight=self.weights.get(source.value, 0.0),
                        rationale="no provider registered",
                    )
                )
        return factors


# ---------------------------------------------------------------------------
# No-op implementation


class NoopRiskEngine:
    """Identity: score derived directly from canonical severity.

    Used in tests and as the fallback engine when no providers are
    configured.
    """

    async def score(
        self,
        findings: Iterable[SecurityFinding],
    ) -> list[RiskEngineResult]:
        out: list[RiskEngineResult] = []
        for finding in findings:
            value = _noop_severity_to_score(finding.severity)
            factor = RiskFactor(
                source=RiskFactorSource.IMPACT,
                value=value / 100.0,
                weight=1.0,
                rationale=f"severity={finding.severity.value}",
            )
            score = RiskScore.build([factor])
            out.append(
                RiskEngineResult(
                    finding=finding.model_copy(update={"risk_score": float(value)}),
                    score=score,
                )
            )
        return out


# ---------------------------------------------------------------------------
# Convenience factory


def build_default_risk_engine() -> DefaultRiskEngine:
    """Convenience factory used by the DI container at M1.

    Real DI wires `RiskEngineSettings` and overrides providers/weights if
    appropriate; this helper keeps the construction default-stable.
    """
    providers: list[RiskSignalProvider] = [
        StaticRiskSignalProvider(source=RiskFactorSource.LIKELIHOOD, default_weight=0.25),
        StaticRiskSignalProvider(source=RiskFactorSource.IMPACT, default_weight=0.35),
        StaticRiskSignalProvider(source=RiskFactorSource.EXPLOITABILITY, default_weight=0.25),
        StaticRiskSignalProvider(source=RiskFactorSource.BUSINESS_CONTEXT, default_weight=0.15),
    ]
    return DefaultRiskEngine(providers=providers, weights=None)


__all__ = [
    "RiskEngine",
    "DefaultRiskEngine",
    "NoopRiskEngine",
    "RiskEngineResult",
    "build_default_risk_engine",
]
