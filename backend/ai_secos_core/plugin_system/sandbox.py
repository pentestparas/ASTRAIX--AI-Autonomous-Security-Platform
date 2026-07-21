"""Plugin Sandbox: isolation boundary.

Responsibilities split (one-sentence each):
  - Executor: *how* a plugin runs (transport, I/O loop).
  - Sandbox:  *what is allowed* during execution (resource limits, FS,
              network, command allow-list).

The Sandbox produces a `SandboxDecision`. Enforcement is the Executor's
job — the Sandbox only decides what is allowed. A later milestone can
swap this to `bubblewrap`, `firejail`, or `nsjail` without disturbing
the Executor's contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from ai_secos_core.config.settings import PluginSystemSettings
from ai_secos_core.plugin_system.manifest import PluginManifest
from ai_secos_core.shared.errors import PluginError


class SandboxViolation(PluginError):
    code = "sandbox_violation"


@dataclass(frozen=True)
class SandboxDecision:
    """A grant of execution rights.

    The Executor consumes this to configure the subprocess environment
    (args, env, resource limits).
    """

    plugin_id: str
    allowed_executables: tuple[str, ...]
    network_mode: str
    filesystem_mode: str
    cpu_cores: float
    memory_mb: int
    timeout_seconds: int
    max_output_bytes: int

    def subprocess_argv(self, plugin_dir: Path, manifest: PluginManifest) -> list[str]:
        """Translate the decision + manifest into a safe subprocess argv.

        The intermediate executable is the first token; the binary
        is the second; the entrypoint is the third when applicable.
        Anything after is unsafe (variable interpolation) — see policy.
        """
        runtime = manifest.runtime
        entry = str(plugin_dir / manifest.entrypoint)
        if runtime == "python3":
            return ["python3", entry]
        if runtime == "node":
            return ["node", entry]
        if runtime == "go":
            return [entry]
        if runtime in ("sh", "bash"):
            return ["/bin/sh", entry]
        raise SandboxViolation(f"unknown runtime: {runtime}")


class PluginSandbox:
    """Decides what is allowed for a given plugin.

    The decision is deterministic and auditable; it does not require
    a subprocess.
    """

    def __init__(self, settings: PluginSystemSettings) -> None:
        self._settings = settings

    def decide(
        self,
        manifest: PluginManifest,
        *,
        argv_tokens: Iterable[str] | None = None,
    ) -> SandboxDecision:
        cmd_allowlist = tuple(self._settings.allow_command_allowlist)

        # If a caller provides argv tokens, they must all be in the
        # allowlist. The actual subprocess invocation never interpolates
        # free-form input — see Executor.
        if argv_tokens:
            for tok in argv_tokens:
                if tok not in cmd_allowlist:
                    raise SandboxViolation(
                        f"argv token not in allowlist: {tok!r}",
                        details={
                            "plugin_id": manifest.id,
                            "token": tok,
                            "allowlist": list(cmd_allowlist),
                        },
                    )

        extras = tuple(manifest.sandbox.allowed_executables or ())
        if any(tok not in cmd_allowlist for tok in extras):
            raise SandboxViolation(
                "manifest allowed_executables must be a subset of platform allowlist",
                details={"plugin_id": manifest.id},
            )

        allowed = tuple(sorted(set(cmd_allowlist) | set(extras)))

        return SandboxDecision(
            plugin_id=manifest.id,
            allowed_executables=allowed,
            network_mode=manifest.sandbox.network,
            filesystem_mode=manifest.sandbox.filesystem,
            cpu_cores=float(manifest.limits.cpu_cores),
            memory_mb=int(manifest.limits.memory_mb),
            timeout_seconds=int(manifest.limits.timeout_seconds),
            max_output_bytes=int(manifest.limits.max_output_bytes),
        )


__all__ = [
    "PluginSandbox",
    "SandboxDecision",
    "SandboxViolation",
]
