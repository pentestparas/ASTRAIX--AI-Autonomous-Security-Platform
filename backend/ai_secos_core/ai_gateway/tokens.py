"""Token Manager — budgets, accounting, retries, compression.

At Milestone 1 we ship the typed contracts and a no-op default. Real
token-budget enforcement lands when concrete providers arrive.

The manager has three contracts:

  1. Plan — pre-call estimate; if the request would exceed the budget,
     refuse before it reaches the model.
  2. Record — post-call accounting.
  3. Compress — reduce the prompt footprint when `compress=True`.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass

from ai_secos_core.ai_gateway.provider import AITokenUsage


@dataclass(frozen=True)
class TokenBudget:
    """Hard limits for a call. `None` = no limit on that field."""

    max_prompt_tokens: int | None
    max_total_tokens: int | None

    @classmethod
    def unlimited(cls) -> "TokenBudget":
        return cls(max_prompt_tokens=None, max_total_tokens=None)


class TokenManager(abc.ABC):
    """Pre-call planning + post-call accounting."""

    @abc.abstractmethod
    def plan(
        self,
        prompt: str,
        budget: TokenBudget,
    ) -> int:
        """Estimate prompt tokens; raise `PlanningError` if over budget."""
        raise NotImplementedError

    @abc.abstractmethod
    def record(self, usage: AITokenUsage, *, correlation_id: str | None) -> None:
        """Persist a usage line for accounting."""
        raise NotImplementedError


class _PlanningError(Exception):
    """Raised when a planned request would exceed its budget."""


class NoopTokenManager:
    """Default at Milestone 1.

    Plan = approximate character length / 4.
    Record = swallowed.
    """

    def plan(self, prompt: str, budget: TokenBudget) -> int:
        estimate = max(1, len(prompt) // 4)
        if budget.max_prompt_tokens is not None and estimate > budget.max_prompt_tokens:
            raise _PlanningError(
                f"prompt over budget: {estimate} > {budget.max_prompt_tokens}"
            )
        if budget.max_total_tokens is not None and estimate > budget.max_total_tokens:
            raise _PlanningError(
                f"prompt over total budget: {estimate} > {budget.max_total_tokens}"
            )
        return estimate

    def record(self, usage: AITokenUsage, *, correlation_id: str | None) -> None:
        # Accounting persistence arrives with concrete providers.
        return None


__all__ = [
    "TokenManager",
    "NoopTokenManager",
    "TokenBudget",
]
