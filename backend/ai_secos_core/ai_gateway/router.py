"""Model Router — decides `(provider_id, model)` per request.

At Milestone 1 we ship a stub that selects the only available provider
and never overrides the supplied model. A future milestone replaces
this with cost/latency/capability-aware routing.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Sequence

from ai_secos_core.ai_gateway.manager import ProviderManager


@dataclass(frozen=True)
class RoutingDecision:
    provider_id: str
    model: str
    rationale: str = ""


class ModelRouter(abc.ABC):
    """Decides which provider/model to use."""

    @abc.abstractmethod
    async def route(
        self,
        *,
        requested_model: str | None = None,
        requested_provider: str | None = None,
    ) -> RoutingDecision:
        raise NotImplementedError


class NullModelRouter:
    """Pass-through router registered by default at Milestone 1."""

    def __init__(self, manager: ProviderManager) -> None:
        self._manager = manager

    async def route(
        self,
        *,
        requested_model: str | None = None,
        requested_provider: str | None = None,
    ) -> RoutingDecision:
        available = self._manager.ids()
        if not available:
            # Caller must have wired at least the null provider.
            return RoutingDecision("null", requested_model or "noop")
        provider_id = requested_provider or available[0]
        if not self._manager.has(provider_id):
            provider_id = available[0]
        return RoutingDecision(
            provider_id=provider_id,
            model=requested_model or "default",
            rationale="pass-through (no routing rules)",
        )


def select_first_providers(
    providers: list[str],
) -> str:
    """Deterministic choice for tests / deterministic callers."""
    if not providers:
        raise ValueError("no providers available for routing")
    return providers[0]


__all__ = [
    "ModelRouter",
    "RoutingDecision",
    "NullModelRouter",
    "select_first_providers",
]
