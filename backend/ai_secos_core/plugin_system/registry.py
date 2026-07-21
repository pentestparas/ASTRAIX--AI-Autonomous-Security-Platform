"""Plugin Registry: what exists and how it is looked up.

The Registry owns *records* (manifest + resolved filesystem location),
not behavior. Permission to execute is the Executor's responsibility.

Operations:
  - register():   add a PluginRecord.
  - get():        lookup by id.
  - list():       list all registered plugins.
  - has():        membership test.

The Registry is populated by the Loader and consumed by the Executor
and Workflow Engine.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from threading import RLock
from typing import Iterable

from ai_secos_core.plugin_system.manifest import PluginManifest
from ai_secos_core.shared.errors import PluginError


class PluginAlreadyRegisteredError(PluginError):
    code = "plugin_already_registered"


class PluginNotFoundError(PluginError):
    code = "plugin_not_found"


@dataclass(frozen=True)
class PluginRecord:
    """Pairing of manifest with its resolved filesystem location."""

    manifest: PluginManifest
    location: Path  # directory containing the plugin


class PluginRegistry:
    """In-memory registry. Thread-safe.

    Persistence (saving registered plugin state to a database) is
    deferred per MVP_SCOPE.md — out of scope at Milestone 1.
    """

    def __init__(self) -> None:
        self._records: dict[str, PluginRecord] = {}
        self._lock = RLock()

    def register(self, record: PluginRecord) -> None:
        with self._lock:
            pid = record.manifest.id
            if pid in self._records:
                raise PluginAlreadyRegisteredError(
                    f"plugin already registered: {pid}",
                    details={"plugin_id": pid},
                )
            self._records[pid] = record

    def unregister(self, plugin_id: str) -> None:
        with self._lock:
            self._records.pop(plugin_id, None)

    def get(self, plugin_id: str) -> PluginRecord:
        try:
            return self._records[plugin_id]
        except KeyError as exc:
            raise PluginNotFoundError(
                f"plugin not found: {plugin_id}",
                details={"plugin_id": plugin_id},
            ) from exc

    def has(self, plugin_id: str) -> bool:
        with self._lock:
            return plugin_id in self._records

    def list(self) -> list[PluginRecord]:
        with self._lock:
            return list(self._records.values())

    def ids(self) -> list[str]:
        with self._lock:
            return sorted(self._records.keys())

    def clear(self) -> None:
        with self._lock:
            self._records.clear()


__all__ = [
    "PluginRegistry",
    "PluginRecord",
    "PluginAlreadyRegisteredError",
    "PluginNotFoundError",
]
