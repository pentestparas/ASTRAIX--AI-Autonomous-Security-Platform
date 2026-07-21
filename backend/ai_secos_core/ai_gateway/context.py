"""Context Builder — assembles what's fed into a prompt.

Pre-AI responsibilities:

  - Bundle canonical findings + asset context + capabilities + relevant
    Risk Engine output into a typed payload.
  - Decide what fits in the model's window (compress/truncate/select).

At Milestone 1 we ship:

  - The typed `FindingContextPayload` shape.
  - The `ContextBuilder` port.
  - A `NullContextBuilder` that returns the payload unchanged (no
    compression / windowing) — enough for tests and the empty default.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from typing import Any, Mapping

from ai_secos_core.risk_engine.types import RiskScore
from ai_secos_core.shared.value_objects import SecurityFinding


@dataclass(frozen=True)
class FindingContextPayload:
    """What the AI sees. Pre-serialization.

    The AI Gateway *never* receives the raw plugin output directly; it
    sees only this. `risk_summary` carries the Risk Engine's reasoning
    trace, not raw weights.
    """

    findings: tuple[SecurityFinding, ...]
    risk_summary: tuple[RiskScore, ...]
    asset: str
    capability: str
    extras: Mapping[str, Any] = field(default_factory=dict)

    def to_template_params(self) -> dict[str, Any]:
        """Convenience: flatten to a dict for string substitution."""
        return {
            "asset": self.asset,
            "capability": self.capability,
            "findings": [f.model_dump(mode="json") for f in self.findings],
            "risk_summary": [
                {"value": s.value, "factors": [f.source.value for f in s.factors]}
                for s in self.risk_summary
            ],
            **{k: v for k, v in self.extras.items()},
        }


class ContextBuilder(abc.ABC):
    """Build a `FindingContextPayload` from typed inputs."""

    @abc.abstractmethod
    async def build(
        self,
        *,
        findings: list[SecurityFinding],
        risk_scores: list[RiskScore],
        asset: str,
        capability: str,
        extras: Mapping[str, Any] | None = None,
    ) -> FindingContextPayload:
        raise NotImplementedError


class NullContextBuilder:
    """Default at Milestone 1.

    Performs no compression or redaction. A future milestone may add
    ones that respect model context windows and redaction policy.
    """

    async def build(
        self,
        *,
        findings: list[SecurityFinding],
        risk_scores: list[RiskScore],
        asset: str,
        capability: str,
        extras: Mapping[str, Any] | None = None,
    ) -> FindingContextPayload:
        return FindingContextPayload(
            findings=tuple(findings),
            risk_summary=tuple(risk_scores),
            asset=asset,
            capability=capability,
            extras=extras or {},
        )


__all__ = [
    "ContextBuilder",
    "NullContextBuilder",
    "FindingContextPayload",
]
