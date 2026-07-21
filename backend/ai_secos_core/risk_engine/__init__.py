"""Risk Engine — likelihood × impact × exploitability × business context.

Per ARCHITECTURE.md, the Risk Engine does NOT produce a "0–100" from a
single signal. It composes multiple sub-scores:

  - likelihood
  - impact
  - exploitability
  - business_context

Each is a port (`RiskSignalProvider`). Weighting is configuration-driven
(`RiskEngineSettings.weights`). The pipeline sums them into a stable
0–100 `RiskScore`.

At Milestone 1 we provide:

  - The typed contract (signal, factor, score).
  - A `RiskEngine` orchestrator that takes injectable signals.
  - A `NoopRiskEngine` that returns a deterministic score derived
    directly from the canonical `severity`.

Real provider implementations (CVE exploit feeds, threat intel,
business-context lookups) arrive in later milestones. Here we pin
interfaces so M2 can plug in.
"""

from ai_secos_core.risk_engine.types import (
    RiskScore,
    RiskSignals,
    RiskFactor,
    RiskFactorSource,
    Severity,
)
from ai_secos_core.risk_engine.providers import (
    RiskSignalProvider,
    StaticRiskSignalProvider,
)
from ai_secos_core.risk_engine.engine import (
    RiskEngine,
    RiskEngineResult,
    NoopRiskEngine,
    DefaultRiskEngine,
    build_default_risk_engine,
)

__all__ = [
    "RiskScore",
    "RiskSignals",
    "RiskFactor",
    "RiskFactorSource",
    "Severity",
    "RiskSignalProvider",
    "StaticRiskSignalProvider",
    "RiskEngine",
    "RiskEngineResult",
    "NoopRiskEngine",
    "DefaultRiskEngine",
    "build_default_risk_engine",
]
