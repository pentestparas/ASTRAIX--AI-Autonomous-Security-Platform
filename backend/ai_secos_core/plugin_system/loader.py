"""Plugin Loader: read manifests from disk → PluginRecords.

The Loader is the *only* component that knows the filesystem layout.
A future iteration could load from a marketplace API; the Loader's
shape stays the same.

Behavior contract:
  - `discover()` walks the plugins root and yields manifest-bearing
    directories.
  - `load_one()` parses exactly one `plugin.yml`.
  - Failure to parse stops at that plugin — other plugins are unaffected.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml

from ai_secos_core.plugin_system.manifest import PluginManifest
from ai_secos_core.plugin_system.registry import PluginRecord
from ai_secos_core.shared.errors import PluginError


class PluginLoaderError(PluginError):
    code = "plugin_loader_error"


@dataclass(frozen=True)
class LoadedPlugin:
    """A loader-level result wrapping a successfully parsed manifest."""

    record: PluginRecord


class PluginLoader:
    """Filesystem-based plugin loader.

    The exact YAML layout is opaque outside this class.
    """

    MANIFEST_FILENAME: str = "plugin.yml"

    def __init__(self, plugins_root: Path | str) -> None:
        self._root = Path(plugins_root)

    @property
    def plugins_root(self) -> Path:
        return self._root

    def discover(self) -> list[PluginRecord]:
        """Walk the plugins root; return all parseable plugin records.

        Directories without a `plugin.yml` are skipped silently.
        Parse failures raise `PluginLoaderError`.
        """
        if not self._root.exists():
            return []
        records: list[PluginRecord] = []
        for manifest_path in sorted(self._root.rglob(self.MANIFEST_FILENAME)):
            try:
                manifest = self._parse_one(manifest_path)
            except PluginLoaderError:
                # Skip broken plugins; one failure doesn't poison others.
                continue
            records.append(
                PluginRecord(
                    manifest=manifest,
                    location=manifest_path.parent,
                )
            )
        return records

    def load_one(self, plugin_dir: Path | str) -> PluginRecord:
        """Load a single plugin by directory path.

        Raises PluginLoaderError on missing manifest or parse failure.
        """
        plugin_dir = Path(plugin_dir)
        manifest_path = plugin_dir / self.MANIFEST_FILENAME
        if not manifest_path.is_file():
            raise PluginLoaderError(
                f"manifest not found: {manifest_path}",
                details={"path": str(manifest_path)},
            )
        manifest = self._parse_one(manifest_path)
        return PluginRecord(manifest=manifest, location=plugin_dir)

    def _parse_one(self, manifest_path: Path) -> PluginManifest:
        try:
            raw = yaml.safe_load(manifest_path.read_text())
        except yaml.YAMLError as exc:
            raise PluginLoaderError(
                f"invalid YAML: {manifest_path}",
                details={"path": str(manifest_path)},
            ) from exc
        if not isinstance(raw, dict):
            raise PluginLoaderError(
                f"manifest must be a mapping: {manifest_path}",
                details={"path": str(manifest_path)},
            )
        try:
            manifest = PluginManifest.model_validate(raw)
        except Exception as exc:  # pydantic.ValidationError
            raise PluginLoaderError(
                f"invalid manifest: {manifest_path}: {exc}",
                details={"path": str(manifest_path)},
            ) from exc
        # Catch entrypoint format problems early.
        try:
            manifest.validate_entrypoint_format()
        except ValueError as exc:
            raise PluginLoaderError(
                f"invalid entrypoint: {exc}",
                details={"path": str(manifest_path)},
            ) from exc
        return manifest


__all__ = [
    "PluginLoader",
    "PluginLoaderError",
    "LoadedPlugin",
]
