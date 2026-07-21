"""Plugin manifest (the typed shape of a `plugin.yml`).

Schema is intentionally strict — invalid manifests must reject at load
time, not at execute time.

A manifest is *data*, not behavior. It declares:
  - identity (id, name, version)
  - capabilities supported
  - input/output schemas (validated as JSON Schema later)
  - resource limits and sandbox policy (interpreted by Sandbox)
  - executable entrypoint
"""

from __future__ import annotations

import re
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from typing_extensions import Annotated

_PLUGIN_ID = Annotated[
    str,
    StringConstraints(pattern=r"^[a-z][a-z0-9_]*/[a-z][a-z0-9_]*$", max_length=128),
]
_VERSION = Annotated[
    str,
    StringConstraints(pattern=r"^\d+\.\d+\.\d+$", max_length=16),
]
_RUNTIME = Annotated[
    str,
    StringConstraints(pattern=r"^(python3|node|go|sh|bash)$", max_length=16),
]


class PluginCapabilityRequirement(BaseModel):
    """A Capability the Plugin requires from the platform."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    capability_id: _PLUGIN_ID
    role: str = Field(pattern=r"^primary$|^secondary$", default="primary")


class PluginResourceLimits(BaseModel):
    """Hard limits applied by the Sandbox."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    cpu_cores: float = Field(ge=0.0, le=64.0, default=1.0)
    memory_mb: int = Field(ge=0, le=65536, default=512)
    timeout_seconds: int = Field(ge=1, le=24 * 3600, default=300)
    max_output_bytes: int = Field(ge=1024, le=256 * 1024 * 1024, default=16 * 1024 * 1024)


class PluginSandboxPolicy(BaseModel):
    """Sandbox behavior policy."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    network: str = Field(pattern=r"^(none|outbound|any)$", default="outbound")
    filesystem: str = Field(pattern=r"^(read_only|read_write|ephemeral)$", default="ephemeral")
    allowed_executables: list[str] = Field(default_factory=list)
    allow_command_substitution: bool = False


class PluginInputSchema(BaseModel):
    """JSON Schema fragment describing a plugin's expected input."""

    model_config = ConfigDict(extra="allow", frozen=True)

    type: str = Field(default="object", pattern=r"^object$")
    required: list[str] = Field(default_factory=list)
    properties: dict[str, Any] = Field(default_factory=dict)


class PluginOutputSchema(BaseModel):
    """JSON Schema fragment describing a plugin's output."""

    model_config = ConfigDict(extra="allow", frozen=True)

    type: str = Field(default="object", pattern=r"^object$")
    required: list[str] = Field(default_factory=list)
    properties: dict[str, Any] = Field(default_factory=dict)


class PluginManifest(BaseModel):
    """Typed representation of a `plugin.yml` declaration."""

    model_config = ConfigDict(extra="forbid", frozen=False)

    id: _PLUGIN_ID
    name: str = Field(min_length=1, max_length=128)
    version: _VERSION
    description: str = ""
    author: str = "unknown"
    runtime: _RUNTIME
    entrypoint: str = Field(min_length=1, max_length=512)

    capabilities: list[PluginCapabilityRequirement] = Field(default_factory=list)
    input_schema: PluginInputSchema = Field(default_factory=PluginInputSchema)
    output_schema: PluginOutputSchema = Field(default_factory=PluginOutputSchema)
    limits: PluginResourceLimits = Field(default_factory=PluginResourceLimits)
    sandbox: PluginSandboxPolicy = Field(default_factory=PluginSandboxPolicy)
    requirements: dict[str, list[str]] = Field(default_factory=dict)
    icon: str | None = None

    def validate_entrypoint_format(self) -> None:
        """Validate entrypoint format for the declared runtime.

        Examples:
          python3: "main.py"               -> ok
          node:    "main.js"               -> ok
          go:      "bin/scanner"           -> ok
          sh:      "scan.sh"               -> ok
        """
        ep = self.entrypoint
        if self.runtime == "python3":
            if not re.match(r"^[a-zA-Z0-9_\-./]+\.py$", ep):
                raise ValueError(f"invalid python entrypoint: {ep}")
        elif self.runtime == "node":
            if not re.match(r"^[a-zA-Z0-9_\-./]+\.js$", ep):
                raise ValueError(f"invalid node entrypoint: {ep}")
        elif self.runtime == "go":
            if "/" in ep and (".." in ep):
                raise ValueError(f"invalid go entrypoint: {ep}")
        elif self.runtime in ("sh", "bash"):
            if not re.match(r"^[a-zA-Z0-9_\-./]+\.sh$", ep):
                raise ValueError(f"invalid shell entrypoint: {ep}")


__all__ = [
    "PluginManifest",
    "PluginCapabilityRequirement",
    "PluginResourceLimits",
    "PluginSandboxPolicy",
    "PluginInputSchema",
    "PluginOutputSchema",
]
