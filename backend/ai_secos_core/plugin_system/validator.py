"""Plugin Validator: schema, capability, and permission checks.

The Validator is the gate between "manifest exists" and "platform
may execute this plugin". It does NOT execute anything.

What it checks:
  1. Manifest schema (already enforced by Pydantic; double-checked here).
  2. Input parameters conform to `input_schema` (against a minimal
     subset of JSON Schema — does not require metadata files).
  3. Required Capabilities are satisfied by the platform registry.
  4. Resource limits are within platform-wide maximums.
  5. Sandbox policy is allowed by the platform's allow-list.

The Validator runs on the platform side; plugins cannot validate
themselves.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from ai_secos_core.plugin_system.manifest import PluginManifest
from ai_secos_core.shared.errors import PluginError


class PluginValidationError(PluginError):
    code = "plugin_validation_error"


@dataclass(frozen=True)
class ValidationResult:
    plugin_id: str
    ok: bool
    issues: tuple[str, ...] = ()

    def __bool__(self) -> bool:  # noqa: D401
        return self.ok


class PluginValidator:
    """Validates a manifest + proposed invocation parameters.

    Stateless aside from injectables. Exposed methods:
      - validate_manifest(manifest): static structural check.
      - validate_invocation(manifest, params): input against schema;
        capability satisfaction checked against `installed_capabilities`.
    """

    PLATFORM_MAX_CPU: float = 16.0
    PLATFORM_MAX_MEMORY_MB: int = 16384
    PLATFORM_MAX_TIMEOUT: int = 24 * 3600

    def __init__(
        self,
        *,
        installed_capabilities: Iterable[str] = (),
        allowed_sandbox_filesystems: Iterable[str] = ("ephemeral",),
        allowed_sandbox_networks: Iterable[str] = ("none", "outbound"),
    ) -> None:
        self._caps: frozenset[str] = frozenset(installed_capabilities)
        self._fs: frozenset[str] = frozenset(allowed_sandbox_filesystems)
        self._net: frozenset[str] = frozenset(allowed_sandbox_networks)

    def validate_manifest(self, manifest: PluginManifest) -> ValidationResult:
        issues: list[str] = []
        limits = manifest.limits
        if limits.cpu_cores > self.PLATFORM_MAX_CPU:
            issues.append(
                f"cpu_cores={limits.cpu_cores} exceeds platform max "
                f"{self.PLATFORM_MAX_CPU}"
            )
        if limits.memory_mb > self.PLATFORM_MAX_MEMORY_MB:
            issues.append(
                f"memory_mb={limits.memory_mb} exceeds platform max "
                f"{self.PLATFORM_MAX_MEMORY_MB}"
            )
        if limits.timeout_seconds > self.PLATFORM_MAX_TIMEOUT:
            issues.append(
                f"timeout_seconds={limits.timeout_seconds} exceeds "
                f"platform max {self.PLATFORM_MAX_TIMEOUT}"
            )
        if manifest.sandbox.filesystem not in self._fs:
            issues.append(
                f"sandbox.filesystem={manifest.sandbox.filesystem!r} not "
                f"in platform allow-list {sorted(self._fs)}"
            )
        if manifest.sandbox.network not in self._net:
            issues.append(
                f"sandbox.network={manifest.sandbox.network!r} not "
                f"in platform allow-list {sorted(self._net)}"
            )
        if manifest.sandbox.allow_command_substitution:
            issues.append("sandbox.allow_command_substitution must be false")
        return ValidationResult(
            plugin_id=manifest.id,
            ok=not issues,
            issues=tuple(issues),
        )

    def validate_invocation(
        self,
        manifest: PluginManifest,
        params: dict[str, Any],
    ) -> ValidationResult:
        issues: list[str] = []

        for req in manifest.capabilities:
            if req.capability_id not in self._caps:
                issues.append(
                    f"required capability {req.capability_id!r} not available"
                )

        # Minimal input validation against the manifest's input_schema.
        required = manifest.input_schema.required or []
        for name in required:
            if name not in params:
                issues.append(f"missing required input parameter: {name!r}")

        properties = manifest.input_schema.properties or {}
        for name, value in params.items():
            spec = properties.get(name)
            if spec is None:
                # Allow extra parameters; many real tools accept them.
                continue
            t = spec.get("type") if isinstance(spec, dict) else None
            if t is None:
                continue
            if not _type_match(value, t):
                issues.append(
                    f"input parameter {name!r}: expected {t}, got {type(value).__name__}"
                )
        return ValidationResult(
            plugin_id=manifest.id,
            ok=not issues,
            issues=tuple(issues),
        )


def _type_match(value: Any, expected_type: str) -> bool:
    """Tiny subset of JSON Schema type matching for type-checking most params."""
    match expected_type:
        case "string":
            return isinstance(value, str)
        case "integer":
            return isinstance(value, int) and not isinstance(value, bool)
        case "number":
            return isinstance(value, (int, float)) and not isinstance(value, bool)
        case "boolean":
            return isinstance(value, bool)
        case "array":
            return isinstance(value, list)
        case "object":
            return isinstance(value, dict)
        case "null":
            return value is None
        case _:
            return True  # unknown types pass (forward-compatible)


__all__ = [
    "PluginValidator",
    "PluginValidationError",
    "ValidationResult",
]
