import asyncio
import json
import logging
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field

from app.plugins.manifest import PluginManifest, load_manifest
from app.domain.models.plugin import (
    PluginOutput,
    PluginError,
    FindingOut,
)

logger = logging.getLogger(__name__)


class PluginInstance(BaseModel):
    """Loaded plugin: metadata + path."""

    manifest: PluginManifest
    path: Path
    enabled: bool = True


class PluginRunResult(BaseModel):
    """Result of running a plugin."""

    success: bool
    manifest: PluginManifest
    output: Optional[PluginOutput] = None
    error: Optional[PluginError] = None
    duration: float
    started_at: datetime
    completed_at: datetime


class PluginRegistry:
    """Lifecycle: discover → load → run → results.

    Plugins are subprocesses:
      - Discovery: filesystem crawler
      - Load: validate plugin.yml
      - Run: spawn process; stdin/stdout pipes
      - Timeout & cancellation: enforcement
    """

    PLUGINS_DIR: str = "plugins"
    PLUGIN_TIMEOUT_DEFAULT: int = 300

    def __init__(self, plugins_dir: Optional[str] = None):
        self.plugins_dir = Path(plugins_dir or self.PLUGINS_DIR)
        self.plugins: Dict[str, PluginInstance] = {}

    async def load_plugins(self) -> List[str]:
        """Discover plugins and validate manifests.

        Returns: list of plugin IDs.
        """
        if not self.plugins_dir.exists():
            logger.warning("Plugin dir not found: %s", self.plugins_dir)
            return []

        loaded = []
        for plugin_dir in sorted(self.plugins_dir.glob("*")):
            if not plugin_dir.is_dir():
                continue
            try:
                manifest = load_manifest(plugin_dir)
                self.plugins[manifest.id] = PluginInstance(
                    manifest=manifest,
                    path=plugin_dir,
                )
                logger.info("Loaded plugin: %s", manifest.id)
                loaded.append(manifest.id)
            except Exception as exc:
                logger.error("Failed to load plugin: %s — %s", plugin_dir.name, exc)

        return loaded

    def get_plugin(self, plugin_id: str) -> Optional[PluginInstance]:
        """Get plugin by ID."""
        return self.plugins.get(plugin_id)

    async def run_plugin(
        self,
        plugin_id: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> PluginRunResult:
        """Run plugin as subprocess.

        Args:
            plugin_id: Plugin identifier
            params: Plugin input parameters

        Returns: PluginRunResult (success + output/error)
        """
        if plugin_id not in self.plugins:
            return PluginRunResult(
                success=False,
                manifest=PluginManifest(id=plugin_id, name="", description="", entrypoint=""),
                error=PluginError(error=f"Plugin not found: {plugin_id}"),
                duration=0,
                started_at=datetime.utcnow(),
                completed_at=datetime.utcnow(),
            )

        instance = self.plugins[plugin_id]
        start = datetime.utcnow()
        try:
            output, error = await self._execute(instance, params)
            return PluginRunResult(
                success=error is None,
                manifest=instance.manifest,
                output=output,
                error=error,
                duration=(datetime.utcnow() - start).total_seconds(),
                started_at=start,
                completed_at=datetime.utcnow(),
            )
        except Exception as exc:
            return PluginRunResult(
                success=False,
                manifest=instance.manifest,
                error=PluginError(error=str(exc)),
                duration=(datetime.utcnow() - start).total_seconds(),
                started_at=start,
                completed_at=datetime.utcnow(),
            )

    async def _execute(
        self,
        instance: PluginInstance,
        params: Optional[Dict[str, Any]],
    ) -> tuple:
        """Execute plugin subprocess. Returns (output, error)."""
        manifest = instance.manifest
        entry = manifest.entrypoint
        script_path = instance.path / entry

        if not script_path.exists():
            raise FileNotFoundError(f"Plugin entrypoint not found: {script_path}")

        # Determine runtime command based on language
        if manifest.runtime.startswith("python"):
            cmd = ["python", str(script_path)]
        elif manifest.runtime.startswith("node"):
            cmd = ["node", str(script_path)]
        elif manifest.runtime.startswith("go"):
            cmd = [str(script_path)]
        else:
            cmd = ["sh", str(script_path)]

        input_data = json.dumps(params or {})

        # Run in executor
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            self._run_subprocess,
            cmd,
            input_data,
            manifest.limits.timeout,
        )

        if result is None:
            return None, PluginError(error="Subprocess raised exception")

        stdout, stderr = result

        if stderr:
            logger.warning("Plugin stderr: %s", stderr)

        try:
            parsed = json.loads(stdout.strip())
            if "error" in parsed:
                return None, PluginError(**parsed)
            return PluginOutput(**parsed), None
        except json.JSONDecodeError as exc:
            return None, PluginError(error=f"Invalid JSON output: {exc}")

    def _run_subprocess(self, cmd: list, input_data: str, timeout: int) -> Optional[tuple]:
        """Run subprocess synchronously. Returns (stdout, stderr)."""
        try:
            result = subprocess.run(
                cmd,
                input=input_data.encode("utf-8"),
                capture_output=True,
                timeout=timeout,
                check=False,
            )
            return (
                result.stdout.decode("utf-8"),
                result.stderr.decode("utf-8"),
            )
        except subprocess.TimeoutExpired:
            return None
        except Exception:
            return None

    def enable_plugin(self, plugin_id: str) -> bool:
        """Enable a plugin by ID. Returns True if found."""
        if plugin_id not in self.plugins:
            return False
        self.plugins[plugin_id].enabled = True
        return True

    def disable_plugin(self, plugin_id: str) -> bool:
        """Disable a plugin by ID. Returns True if found."""
        if plugin_id not in self.plugins:
            return False
        self.plugins[plugin_id].enabled = False
        return True

    def list_plugins(self) -> List[PluginManifest]:
        """Get manifests of all registered plugins."""
        return [p.manifest for p in self.plugins.values()]


_plugin_registry: Optional[PluginRegistry] = None


async def get_plugin_registry() -> PluginRegistry:
    """Singleton plugin registry."""
    global _plugin_registry
    if _plugin_registry is None:
        _plugin_registry = PluginRegistry()
        await _plugin_registry.load_plugins()
    return _plugin_registry