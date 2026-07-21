"""Container / DI tests.

Targets:
  - Roundtrip build + freeze
  - Settings typing
  - Plugin discovery at boot
"""

import pytest
from pydantic_settings import BaseSettings
import tempfile

from ai_secos_core.api_platform.container import build_default_container, Container


def test_container_freeze() -> None:
    container = build_default_container()
    assert isinstance(container, Container)


def test_settings_values() -> None:
    container = build_default_container()
    settings = container.settings
  
    # Settings come from `Settings` pydantic base class.
    assert isinstance(settings, BaseSettings)
    assert settings.platform.app_name == "AI-SecOS Core"


def test_plugin_loader_discovery(tmp_path) -> None:
    from ai_secos_core.plugin_system.manifest import PluginManifest
    from ai_secos_core.plugin_system.loader import PluginLoader
    
    discovery_root = tmp_path / "plugins"
    discovery_root.mkdir()
    
    (discovery_root / "test_plugin").mkdir()
    (discovery_root / "test_plugin" / "plugin.yml").write_text(
        """id: test/plugin
name: Test Plugin
version: 1.0.0
runtime: python3
entrypoint: main.py
"""
    )
    
    # Rebuild container → drop into DI.
    container = build_default_container()
    # Override loader at DI for this test.
    # DI container _MutableContainer().mutate() → override
    from ai_secos_core.api_platform.container import _MutableContainer
    
    mutable = _MutableContainer()
    mutable.settings = container.settings
    mutable.loader = PluginLoader(str(discovery_root))
    mutable.freeze = lambda: container
    merged = mutable.freeze()
    
    records = merged.loader.discover()
    assert len(records) == 1
    assert records[0].manifest.id == "test/plugin"