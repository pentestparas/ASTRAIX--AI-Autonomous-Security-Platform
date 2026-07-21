"""Normalizer interface + registry.

The Normalizer is how raw plugin output becomes a `SecurityFinding`.
Each plugin ships with a Normalizer and registers it with the
registry; the registry resolves by `(plugin_id)` (or plugin_id +
output schema name).

At Milestone 1 we ship the contract and the registry; concrete plugin
normalizers (Nuclei, httpx, etc.) are out of scope per the directive
("no security business logic").
"""

from __future__ import annotations

import abc
import json
from dataclasses import dataclass
from typing import Any, Callable, Iterator, Mapping

from ai_secos_core.shared.errors import FindingEngineError
from ai_secos_core.shared.value_objects import (
    AssessmentId,
    PluginId,
    SecurityFinding,
    Severity,
)


class NormalizationError(FindingEngineError):
    code = "normalization_error"


class FindingNormalizer(abc.ABC):
    """Turns a plugin-specific raw output into a `SecurityFinding`.

    A single input may emit many findings (a Nuclei scan returns many
    matches); subclasses implement the iteration themselves.
    """

    plugin_id: PluginId

    @abc.abstractmethod
    def normalize(
        self,
        raw_output: Mapping[str, Any],
        *,
        assessment_id: AssessmentId,
        capability_id: str,
        asset_id: str,
    ) -> Iterator[SecurityFinding]:
        """Yield canonical findings from a raw plugin output.

        Implementations MUST yield fully-formed `SecurityFinding`
        objects. They SHOULD raise `NormalizationError` on
        irrecoverable shape mismatch.
        """
        raise NotImplementedError


class NormalizerRegistry:
    """Maps `(plugin_id)` → normalizer instance.

    A `NormalizerRegistry` produces no findings on its own; it is a
    pure lookup. The plugin author is responsible for shipping a
    `FindingNormalizer` alongside the plugin executable.
    """

    def __init__(self, normalizers: list[FindingNormalizer] | None = None) -> None:
        self._by_plugin: dict[str, FindingNormalizer] = {}
        if normalizers:
            for n in normalizers:
                self.register(n)

    def register(self, normalizer: FindingNormalizer) -> None:
        self._by_plugin[normalizer.plugin_id] = normalizer

    def get(self, plugin_id: str) -> FindingNormalizer:
        try:
            return self._by_plugin[plugin_id]
        except KeyError as exc:
            raise NormalizationError(
                f"normalizer not registered: {plugin_id}",
                details={"plugin_id": plugin_id},
            ) from exc

    def has(self, plugin_id: str) -> bool:
        return plugin_id in self._by_plugin

    def plugins(self) -> list[str]:
        return sorted(self._by_plugin.keys())


__all__ = [
    "FindingNormalizer",
    "NormalizerRegistry",
    "NormalizationError",
]
