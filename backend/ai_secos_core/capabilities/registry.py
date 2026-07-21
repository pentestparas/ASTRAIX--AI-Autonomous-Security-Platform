"""Capability Registry — typed lookup and lifecycle.

Thread-safe in-memory registry of `Capability` instances.
Future iterations can persist to PostgreSQL.
"""

from __future__ import annotations

import threading
from typing import Dict, Iterable, List, Optional

from ai_secos_core.capabilities.errors import (
    CapabilityNotFoundError,
    CapabilityAlreadyRegisteredError,
)
from ai_secos_core.capabilities.models import Capability, CapabilityManifest, CapabilityVersion


class CapabilityRegistry:
    """Thread-safe registry of `Capability` instances keyed by id+version.

    Capabilities are versioned; multiple versions may coexist.
    Registering the same (id, version) twice raises an error.
    """

    def __init__(self, capabilities: Iterable[Capability] | None = None) -> None:
        self._by_id_version: Dict[str, Dict[str, Capability]] = {}
        self._lock = threading.RLock()
        if capabilities:
            for cap in capabilities:
                self.register(cap)

    def register(self, capability: Capability) -> None:
        with self._lock:
            store = self._by_id_version.setdefault(capability.id, {})
            version_key = str(capability.version)
            if version_key in store:
                raise CapabilityAlreadyRegisteredError(
                    f"capability already registered: {capability.id}@{version_key}",
                    details={"capability_id": capability.id, "version": version_key},
                )
            store[version_key] = capability

    def register_from_manifest(self, manifest: CapabilityManifest) -> Capability:
        capability = manifest.to_capability()
        self.register(capability)
        return capability

    def get(self, capability_id: str, version: Optional[str] = None) -> Capability:
        with self._lock:
            store = self._by_id_version.get(capability_id)
            if not store:
                raise CapabilityNotFoundError(
                    f"capability not found: {capability_id}",
                    details={"capability_id": capability_id},
                )
            if version is None:
                latest = max(
                    (CapabilityVersion.parse(v) for v in store),
                    key=lambda ver: (ver.major, ver.minor, ver.patch),
                )
                return store[str(latest)]
            if version not in store:
                raise CapabilityNotFoundError(
                    f"capability version not found: {capability_id}@{version}",
                    details={"capability_id": capability_id, "version": version},
                )
            return store[version]

    def has(self, capability_id: str, version: Optional[str] = None) -> bool:
        with self._lock:
            if capability_id not in self._by_id_version:
                return False
            if version is None:
                return True
            return version in self._by_id_version[capability_id]

    def list(self, capability_id: Optional[str] = None) -> List[Capability]:
        with self._lock:
            if capability_id is not None:
                return list(self._by_id_version.get(capability_id, {}).values())
            return [
                cap
                for versions in self._by_id_version.values()
                for cap in versions.values()
            ]

    def ids(self) -> List[str]:
        with self._lock:
            return sorted(self._by_id_version.keys())

    def clear(self) -> None:
        with self._lock:
            self._by_id_version.clear()