"""Risk Signal Providers.

A provider is a single sub-axis of risk scoring:
  - Likelihood
  - Impact
  - Exploitability
  - Business Context

Each is its own port. Multiple providers per axis can exist at once;
the engine aggregates them. At Milestone 1 we ship a `Static...`
implementation that uses the canonical Severity as input. Real intel-
backed providers are a later milestone.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass

from ai_secos_core.risk_engine.types import (
    RiskFactor,
    RiskFactorSource,
    RiskSignals,
    Severity,
)

# Map severity → per-axis numeric estimates.
_SEVERITY_LIKELIHOOD = {
    Severity.INFO: 0.10,
    Severity.LOW: 0.25,
    Severity.MEDIUM: 0.50,
    Severity.HIGH: 0.75,
    Severity.CRITICAL: 0.95,
}
_SEVERITY_IMPACT = {
    Severity.INFO: 0.05,
    Severity.LOW: 0.20,
    Severity.MEDIUM: 0.45,
    Severity.HIGH: 0.75,
    Severity.CRITICAL: 0.95,
}


class RiskSignalProvider(abc.ABC):
    """A single sub-axis of risk scoring.

    Concrete providers are pure functions from `RiskSignals` to
    `RiskFactor`. They MUST be deterministic and side-effect free
    (intel lookups are cached or stubbed at the provider's edge).
    """

    source: RiskFactorSource
    default_weight: float

    @abc.abstractmethod
    def evaluate(self, signals: RiskSignals) -> RiskFactor:
        """Return the factor for one set of signals."""
        raise NotImplementedError


class StaticRiskSignalProvider:
    """A static, deterministic provider.

    Likelihood and Impact use the severity table; Exploitability uses
    CVE/Known-exploit data; Business Context uses injected asset
    criticality.
    """

    def __init__(
        self,
        source: RiskFactorSource,
        default_weight: float,
    ) -> None:
        self.source = source
        self.default_weight = default_weight
        self._specific: dict[RiskFactorSource, _ProviderFn] = {
            RiskFactorSource.LIKELIHOOD: self._likelihood,
            RiskFactorSource.IMPACT: self._impact,
            RiskFactorSource.EXPLOITABILITY: self._exploitability,
            RiskFactorSource.BUSINESS_CONTEXT: self._business_context,
        }

    def evaluate(self, signals: RiskSignals) -> RiskFactor:
        fn = self._specific[self.source]
        value, rationale = fn(signals)
        return RiskFactor(
            source=self.source,
            value=max(0.0, min(1.0, value)),
            weight=self.default_weight,
            rationale=rationale,
        )

    # ----- axis implementations ------------------------------------------------

    def _likelihood(self, signals: RiskSignals) -> tuple[float, str]:
        base = _SEVERITY_LIKELIHOOD[signals.severity]
        if signals.cve:
            base = max(base, base + 0.05)
            return base, f"severity={signals.severity.value}, cve cues"
        return base, f"severity={signals.severity.value}"

    def _impact(self, signals: RiskSignals) -> tuple[float, str]:
        base = _SEVERITY_IMPACT[signals.severity]
        if signals.cvss is not None:
            # CVSS already maps impact 0–10; bring into 0–1.
            base = max(base, signals.cvss / 10.0)
            return base, f"severity={signals.severity.value}, cvss={signals.cvss}"
        return base, f"severity={signals.severity.value}"

    def _exploitability(self, signals: RiskSignals) -> tuple[float, str]:
        if signals.public_exploit_known:
            return 0.95, "public exploit known"
        if signals.cve:
            return 0.65, "cve id(s) present, no public exploit check"
        if signals.cwe:
            return 0.40, "cwe class known"
        return 0.20, "no exploit signal"

    def _business_context(self, signals: RiskSignals) -> tuple[float, str]:
        return (
            max(0.0, min(1.0, signals.business_criticality)),
            f"asset criticality={signals.business_criticality:.2f}",
        )


# Internal: per-axis functions return (value, rationale).
_ProviderFn = "object"  # helper typing — handled at runtime
