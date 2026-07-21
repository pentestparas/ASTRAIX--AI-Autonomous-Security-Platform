import os
from pathlib import Path
from typing import Dict, Any, List, Optional

from pydantic import BaseModel, Field, model_validator
from yaml import safe_load


class PluginLimits(BaseModel):
    cpu: float = 1.0
    memory: int = 500
    timeout: int = 300


class PluginSchema(BaseModel):
    input: Dict[str, Any] = {}
    output: Dict[str, Any] = {}


class PluginManifest(BaseModel):
    id: str = Field(pattern=r"^[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+$")
    name: str
    description: str
    version: str = "0.1.0"
    author: str = "AstraIX"
    type: str = "scanner"
    runtime: str = "python3.12"
    entrypoint: str
    schema: PluginSchema = Field(default_factory=PluginSchema)
    limits: PluginLimits = Field(default_factory=PluginLimits)
    environment: List[str] = []
    requirements: Dict[str, List[str]] = {}
    capabilities: List[str] = []
    icon: Optional[str] = None


def load_manifest(plugin_dir: Path) -> PluginManifest:
    """Load a plugin.json from a directory."""
    manifest_path = plugin_dir / "plugin.yml"
    if not manifest_path.exists():
        raise FileNotFoundError(f"plugin.yml not found in {plugin_dir}")
    data = safe_load(manifest_path.read_text())
    return PluginManifest(**data)