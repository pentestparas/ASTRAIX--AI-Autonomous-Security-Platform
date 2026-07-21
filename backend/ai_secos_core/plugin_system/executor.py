"""Plugin Executor: drives the subprocess lifecycle.

Owns the *mechanics*:

  - Resolve a registered plugin's location.
  - Build argv via `Sandbox.subprocess_argv(...)` (no interpolation).
  - Spawn via `asyncio.create_subprocess_exec` with resource bounds.
  - Stream stdin (typed JSON) and collect stdout/stderr with size cap.
  - Enforce hard timeout.
  - Return a `PluginExecutionResult` (success/failure/timed-out).
  - Emit a structured `DomainEvent` on completion.

The Executor MUST be sandbox-decided; it does NOT inspect the manifest
beyond the Sandbox-resolved decision.
"""

from __future__ import annotations

import asyncio
import json
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Iterator

from ai_secos_core.infrastructure.logging import get_logger
from ai_secos_core.infrastructure.metrics import Counter, Histogram, MetricsRegistry
from ai_secos_core.plugin_system.manifest import PluginManifest
from ai_secos_core.plugin_system.registry import PluginRecord, PluginRegistry
from ai_secos_core.plugin_system.sandbox import (
    PluginSandbox,
    SandboxDecision,
    SandboxViolation,
)
from ai_secos_core.shared.events import EventDispatcher, make_event
from ai_secos_core.shared.correlation import CorrelationId, get_correlation_id

_logger = get_logger(__name__)


class PluginExecutionStatus(str, Enum):
    OK = "ok"
    FAILED = "failed"
    TIMED_OUT = "timed_out"
    CANCELLED = "cancelled"
    SANDBOX_REJECTED = "sandbox_rejected"
    NOT_FOUND = "not_found"
    INVALID_OUTPUT = "invalid_output"


@dataclass(frozen=True)
class PluginExecutionRequest:
    """Typed request to run a plugin once."""

    plugin_id: str
    params: dict[str, object]
    correlation_id: CorrelationId | None = None
    stdin_blob: bytes | None = None  # if None, params are JSON-encoded


@dataclass(frozen=True)
class PluginExecutionResult:
    status: PluginExecutionStatus
    plugin_id: str
    stdout: str = ""
    stderr: str = ""
    exit_code: int | None = None
    elapsed_ms: int = 0
    error: str | None = None
    output: object | None = None  # parsed JSON, when valid


class PluginExecutor:
    """Async-first plugin executor with deterministic safety."""

    def __init__(
        self,
        registry: PluginRegistry,
        sandbox: PluginSandbox,
        event_dispatcher: EventDispatcher,
        metrics: MetricsRegistry,
    ) -> None:
        self._registry = registry
        self._sandbox = sandbox
        self._events = event_dispatcher
        self._exec_counter: Counter = metrics.counter(
            "plugin_executions_total",
            unit="executions",
            description="Count of plugin invocations by status",
            label_names=("status",),
        )
        self._exec_hist: Histogram = metrics.histogram(
            "plugin_execution_duration_ms",
            unit="ms",
            description="Plugin execution wall-clock duration",
        )

    async def execute(self, request: PluginExecutionRequest) -> PluginExecutionResult:
        plugin_id = request.plugin_id
        cid = request.correlation_id or get_correlation_id()

        try:
            record = self._registry.get(plugin_id)
        except Exception as exc:  # PluginNotFoundError
            self._record_metric("not_found")
            await self._emit_event(
                event_type="plugin.execution.not_found",
                plugin_id=plugin_id,
                cid=cid,
                detail=str(exc),
            )
            return PluginExecutionResult(
                status=PluginExecutionStatus.NOT_FOUND,
                plugin_id=plugin_id,
                error="plugin not found",
            )

        decision: SandboxDecision
        try:
            decision = self._sandbox.decide(record.manifest)
        except SandboxViolation as exc:
            self._record_metric("sandbox_rejected")
            await self._emit_event(
                event_type="plugin.execution.sandbox_rejected",
                plugin_id=plugin_id,
                cid=cid,
                detail=str(exc),
            )
            return PluginExecutionResult(
                status=PluginExecutionStatus.SANDBOX_REJECTED,
                plugin_id=plugin_id,
                error=str(exc),
            )

        start_ns = time.monotonic_ns()
        result = await self._run_subprocess(record, decision, request)
        elapsed_ms = int((time.monotonic_ns() - start_ns) // 1_000_000)

        result_out = PluginExecutionResult(
            status=result.status,
            plugin_id=plugin_id,
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.exit_code,
            elapsed_ms=elapsed_ms,
            error=result.error,
            output=result.output,
        )

        self._record_metric(result_out.status.value)
        self._exec_hist.observe(float(elapsed_ms))
        await self._emit_event(
            event_type="plugin.execution.completed",
            plugin_id=plugin_id,
            cid=cid,
            detail={
                "status": result_out.status.value,
                "elapsed_ms": elapsed_ms,
            },
        )
        return result_out

    # ---- internals ------------------------------------------------------

    async def _run_subprocess(
        self,
        record: PluginRecord,
        decision: SandboxDecision,
        request: PluginExecutionRequest,
    ) -> PluginExecutionResult:
        """Drive asyncio's subprocess for one plugin invocation."""

        argv = decision.subprocess_argv(record.location, record.manifest)
        stdin_payload = (
            request.stdin_blob
            if request.stdin_blob is not None
            else json.dumps(request.params or {}).encode("utf-8")
        )

        env = {
            "ASTRAIX_CORRELATION_ID": str(request.correlation_id or get_correlation_id()),
            "PATH": "/usr/local/bin:/usr/bin:/bin",
        }

        try:
            proc = await asyncio.create_subprocess_exec(
                *argv,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,
            )
        except FileNotFoundError as exc:
            return PluginExecutionResult(
                status=PluginExecutionStatus.FAILED,
                plugin_id=request.plugin_id,
                error=f"entrypoint not found: {exc}",
            )

        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(stdin_payload),
                timeout=decision.timeout_seconds,
            )
        except asyncio.TimeoutError:
            try:
                proc.kill()
            except ProcessLookupError:
                pass
            return PluginExecutionResult(
                status=PluginExecutionStatus.TIMED_OUT,
                plugin_id=request.plugin_id,
                error=f"timeout after {decision.timeout_seconds}s",
            )

        # Cap output to prevent OOM (best-effort for Milestone 1).
        out_b = _truncate_bytes(stdout, decision.max_output_bytes)
        err_b = _truncate_bytes(stderr, decision.max_output_bytes)

        if proc.returncode != 0:
            return PluginExecutionResult(
                status=PluginExecutionStatus.FAILED,
                plugin_id=request.plugin_id,
                stdout=out_b.decode("utf-8", errors="replace"),
                stderr=err_b.decode("utf-8", errors="replace"),
                exit_code=proc.returncode,
                error="non-zero exit",
            )

        # Try to parse stdout as JSON; fall back to raw string.
        decoded_text = out_b.decode("utf-8", errors="replace").strip()
        parsed: object
        try:
            parsed = json.loads(decoded_text) if decoded_text else {}
        except json.JSONDecodeError:
            return PluginExecutionResult(
                status=PluginExecutionStatus.OK,
                plugin_id=request.plugin_id,
                stdout=decoded_text,
                stderr=err_b.decode("utf-8", errors="replace"),
                exit_code=0,
                output={"raw": decoded_text},
            )

        if not isinstance(parsed, dict):
            return PluginExecutionResult(
                status=PluginExecutionStatus.INVALID_OUTPUT,
                plugin_id=request.plugin_id,
                stderr=err_b.decode("utf-8", errors="replace"),
                exit_code=0,
                error="plugin output must be a JSON object",
            )

        return PluginExecutionResult(
            status=PluginExecutionStatus.OK,
            plugin_id=request.plugin_id,
            stdout=decoded_text,
            stderr=err_b.decode("utf-8", errors="replace"),
            exit_code=0,
            output=parsed,
        )

    def _record_metric(self, status: str) -> None:
        try:
            self._exec_counter.inc(labels={"status": status})
        except Exception:
            # metrics must never block execution
            pass

    async def _emit_event(
        self,
        event_type: str,
        plugin_id: str,
        cid: CorrelationId,
        detail: object,
    ) -> None:
        await self._events.publish(
            make_event(
                event_type,
                correlation_id=str(cid),
                payload={"plugin_id": plugin_id, "detail": _safe(detail)},
            )
        )


def _truncate_bytes(b: bytes, cap: int) -> bytes:
    if cap <= 0 or len(b) <= cap:
        return b
    return b[:cap]


def _safe(v: object) -> object:
    """Convert non-JSON values to strings, swallowing exceptions."""
    try:
        json.dumps(v)
        return v
    except TypeError:
        try:
            return str(v)
        except Exception:
            return "<unprintable>"


class NoopTaskExecutor:
    """Dummy executor for DI containers.
    
    M2 currently uses PluginExecutor for actual work.
    """
    async def execute(self, request: PluginExecutionRequest) -> PluginExecutionResult:
        return PluginExecutionResult(
            status=PluginExecutionStatus.FAILED,
            plugin_id=request.plugin_id,
            error="NoopTaskExecutor is a stub",
        )

class TaskExecutor(PluginExecutor):
    """High-level task executor wrapper."""
    pass

__all__ = [
    "PluginExecutor",
    "PluginExecutionRequest",
    "PluginExecutionResult",
    "PluginExecutionStatus",
    "NoopTaskExecutor",
    "TaskExecutor",
]
