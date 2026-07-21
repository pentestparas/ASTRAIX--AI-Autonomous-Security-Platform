"""YAML-based capability loader.

Loads capability manifests from filesystem into typed `Capability`s.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

import yaml

from ai_secos_core.capabilities.errors import (
    CapabilityAlreadyRegisteredError,
    CapabilityNotFoundError,
    CapabilityResolverError,
)
from ai_secos_core.capabilities.models import (
    AssetCategory,
    Capability,
    CapabilityInputSchema,
    CapabilityManifest,
    CapabilityOutputSchema,
    ComplianceFramework,
    ComplianceTag,
    RequiredPlugin,
    SupportedAssetType,
)
from ai_secos_core.shared.errors import PlatformError


class CapabilityLoaderError(PlatformError):
    """Raised on capability loader failures."""

    code = "capability_loader_error"
    http_status = 500


@dataclass(frozen=True)
class LoadedCapability:
    """A loader result wrapping a successfully parsed capability manifest."""

    manifest: CapabilityManifest
    capability: Capability
    path: Path


class CapabilityLoader:
    """Filesystem-based capability loader."""

    MANIFEST_FILENAME = "manifest.yml"
    MANIFEST_FILENAMES = ("manifest.yml", "capability.yml")

    def __init__(self, capabilities_root: Path | str) -> None:
        self._root = Path(capabilities_root)

    def discover(self) -> List[LoadedCapability]:
        """Discover all capabilities under the root."""
        if not self._root.exists():
            return []
        out: List[LoadedCapability] = []
        seen_paths: set[Path] = set()
        for filename in self.MANIFEST_FILENAMES:
            for path in sorted(self._root.rglob(filename)):
                if path in seen_paths:
                    continue
                seen_paths.add(path)
                try:
                    loaded = self.load_one(path.parent)
                except CapabilityLoaderError as exc:
                    continue  # bad manifests don't poison siblings
                out.append(loaded)
        return out

    def load_one(self, capability_dir: Path | str) -> LoadedCapability:
        capability_dir = Path(capability_dir)
        path = None
        for filename in self.MANIFEST_FILENAMES:
            candidate = capability_dir / filename
            if candidate.is_file():
                path = candidate
                break
        if path is None:
            raise CapabilityLoaderError(
                f"no manifest file in: {capability_dir}",
                details={"path": str(capability_dir)},
            )
        try:
            raw = yaml.safe_load(path.read_text())
        except yaml.YAMLError as exc:
            raise CapabilityLoaderError(
                f"invalid YAML in: {path}",
                details={"path": str(path)},
            ) from exc
        if not isinstance(raw, dict):
            raise CapabilityLoaderError(
                f"manifest must be a mapping: {path}",
                details={"path": str(path)},
            )
        manifest = _parse_manifest(raw, path)
        return LoadedCapability(
            manifest=manifest,
            capability=manifest.to_capability(),
            path=path,
        )


def _parse_manifest(raw: dict, path: Path) -> CapabilityManifest:
    """Parse a YAML mapping into a `CapabilityManifest`."""
    required_fields = ("id", "version", "display_name")
    for field in required_fields:
        if field not in raw:
            raise CapabilityLoaderError(
                f"missing required field {field!r} in {path}",
                details={"path": str(path), "field": field},
            )

    inputs_raw = raw.get("inputs", {})
    inputs = CapabilityInputSchema(
        type=inputs_raw.get("type", "object"),
        required=tuple(inputs_raw.get("required", []) or []),
        properties=tuple(sorted((inputs_raw.get("properties") or {}).items())),
        additional_properties=bool(inputs_raw.get("additional_properties", True)),
    )

    outputs_raw = raw.get("outputs", {})
    outputs = CapabilityOutputSchema(
        finding_kinds=tuple(outputs_raw.get("finding_kinds", []) or []),
        asset_types=tuple(
            _parse_asset_category(a)
            for a in (outputs_raw.get("asset_types", []) or [])
        ),
    )

    supported_assets = tuple(
        SupportedAssetType(
            category=_parse_asset_category(a["category"]),
            description=a.get("description", ""),
        )
        for a in raw.get("supported_assets", [])
    )

    required_plugins = tuple(
        RequiredPlugin(
            plugin_id=p["plugin_id"],
            min_version=p.get("min_version", "0.0.0"),
            role=p.get("role", "primary"),
        )
        for p in raw.get("required_plugins", [])
    )

    workflows = tuple(raw.get("workflows", []) or [])  # WorkflowId

    compliance = tuple(
        ComplianceTag(
            framework=_parse_framework(c["framework"]),
            control=c["control"],
            rationale=c.get("rationale", ""),
        )
        for c in raw.get("compliance", [])
    )

    return CapabilityManifest(
        id=raw["id"],
        version=raw["version"],
        display_name=raw["display_name"],
        description=raw.get("description", ""),
        inputs=inputs,
        outputs=outputs,
        supported_assets=supported_assets,
        workflows=workflows,
        required_plugins=required_plugins,
        compliance=compliance,
    )


def _parse_asset_category(value: str) -> AssetCategory:
    try:
        return AssetCategory(value)
    except ValueError as exc:
        raise CapabilityLoaderError(
            f"unknown asset category: {value}",
        ) from exc


def _parse_framework(value: str) -> ComplianceFramework:
    try:
        return ComplianceFramework(value)
    except ValueError as exc:
        raise CapabilityLoaderError(
            f"unknown compliance framework: {value}",
        ) from exc