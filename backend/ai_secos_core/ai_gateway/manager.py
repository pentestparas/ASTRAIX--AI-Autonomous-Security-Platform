"""Provider Manager.

The Manager owns the lifecycle of providers. Applications never name a
provider; the Model Router decides which (`provider_id`, `model`) to
use, and the Manager resolves it to a real `AIProvider`.
"""

from __future__ import annotations

import threading
from collections.abc import Iterable

from ai_secos_core.ai_gateway.provider import AIProvider
from ai_secos_core.shared.errors import AIError


class ProviderAlreadyRegisteredError(AIError):
    code = "provider_already_registered"


class ProviderNotFoundError(AIError):
    code = "provider_not_found"


class ProviderManager:
    """Thread-safe registry of providers.

    The Manager is the *only* place providers are added. Removing them
    (de-registration) is reserved for tests.
    """

    def __init__(self, providers: Iterable[AIProvider] | None = None) -> None:
        self._providers: dict[str, AIProvider] = {}
        self._lock = threading.RLock()
        if providers:
            for p in providers:
                self.register(p)

    def register(self, provider: AIProvider) -> None:
        pid = provider.provider_id
        if not pid:
            raise AIError("provider_id must be set", details={"provider": type(provider).__name__})
        with self._lock:
            if pid in self._providers:
                raise ProviderAlreadyRegisteredError(
                    f"provider already registered: {pid}",
                    details={"provider_id": pid},
                )
            self._providers[pid] = provider

    def unregister(self, provider_id: str) -> None:
        with self._lock:
            self._providers.pop(provider_id, None)

    def get(self, provider_id: str) -> AIProvider:
        try:
            return self._providers[provider_id]
        except KeyError as exc:
            raise ProviderNotFoundError(
                f"provider not found: {provider_id}",
                details={"provider_id": provider_id},
            ) from exc

    def has(self, provider_id: str) -> bool:
        with self._lock:
            return provider_id in self._providers

    def ids(self) -> list[str]:
        with self._lock:
            return sorted(self._providers.keys())

    def clear(self) -> None:
        with self._lock:
            self._providers.clear()


__all__ = [
    "ProviderManager",
    "ProviderAlreadyRegisteredError",
    "ProviderNotFoundError",
]
