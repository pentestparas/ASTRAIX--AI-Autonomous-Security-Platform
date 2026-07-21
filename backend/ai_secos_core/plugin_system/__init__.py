"""Plugin System (PDK-facing contracts + platform internals).

Public surface for plugin authors is the PDK (`SecurityPlugin`).
Platform internals (this package) split into five concerns:

  - **Registry**:   what plugins exist; lookup by id.
  - **Loader**:     reads plugin manifests from disk; produces PluginRecords.
  - **Validator**:  schema, capability, and permission checks.
  - **Executor**:   drives subprocess execution and output collection.
  - **Sandbox**:    isolation boundary; resource limits and allow-lists.

This file exports only the public names. Each sub-module may import from
this package's primitives.
"""

from ai_secos_core.plugin_system.manifest import (
    PluginManifest,
    PluginCapabilityRequirement,
    PluginResourceLimits,
    PluginSandboxPolicy,
    PluginInputSchema,
    PluginOutputSchema,
)
from ai_secos_core.plugin_system.registry import (
    PluginRegistry,
    PluginRecord,
    PluginAlreadyRegisteredError,
    PluginNotFoundError,
)
from ai_secos_core.plugin_system.loader import (
    PluginLoader,
    PluginLoaderError,
)
from ai_secos_core.plugin_system.validator import (
    PluginValidator,
    PluginValidationError,
)
from ai_secos_core.plugin_system.executor import (
    PluginExecutor,
    PluginExecutionRequest,
    PluginExecutionResult,
    PluginExecutionStatus,
)
from ai_secos_core.plugin_system.sandbox import (
    PluginSandbox,
    SandboxDecision,
    SandboxViolation,
)

__all__ = [
    # manifest
    "PluginManifest",
    "PluginCapabilityRequirement",
    "PluginResourceLimits",
    "PluginSandboxPolicy",
    "PluginInputSchema",
    "PluginOutputSchema",
    # registry
    "PluginRegistry",
    "PluginRecord",
    "PluginAlreadyRegisteredError",
    "PluginNotFoundError",
    # loader
    "PluginLoader",
    "PluginLoaderError",
    # validator
    "PluginValidator",
    "PluginValidationError",
    # executor
    "PluginExecutor",
    "PluginExecutionRequest",
    "PluginExecutionResult",
    "PluginExecutionStatus",
    # sandbox
    "PluginSandbox",
    "SandboxDecision",
    "SandboxViolation",
]
