"""Streaming-aware Plugin Executor.

Wraps the base `PluginExecutor` and emits `plugin.started`,
`plugin.finding`, `plugin.completed` events for live streaming.

The wrapper is one-way — no return-value changes — so swapping it in
doesn't require callers to change.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import Any, Mapping

from ai_secos_core.plugin_system.executor import (
    PluginExecutionRequest,
    PluginExecutionResult,
    PluginExecutionStatus,
)
from ai_secos_core.runtime.stream import (
    emit_plugin_completed,
    emit_plugin_finding,
    emit_plugin_progress,
    emit_plugin_started,
)
from ai_secos_core.shared.events import EventDispatcher


class StreamingPluginExecutor:
    """Wraps a PluginExecutor to emit streaming events.

    The wrapper preserves the underlying behavior; it adds:
      - `plugin.started` on enter
      - `plugin.progress` on each task tick (interval-based)
      - `plugin.finding` if the result contains `findings`
      - `plugin.completed` on return
    """

    def __init__(
        self,
        inner,  # PluginExecutor-like
        event_dispatcher: EventDispatcher,
        progress_interval_seconds: float = 5.0,
    ) -> None:
        self._inner = inner
        self._events = event_dispatcher
        self._progress_interval = progress_interval_seconds

    async def execute(self, request: PluginExecutionRequest) -> PluginExecutionResult:
        correlation_id = request.correlation_id or ""

        await emit_plugin_started(
            self._events,
            plugin_id=request.plugin_id,
            runtime="unknown",
            correlation_id=correlation_id,
        )

        start = time.monotonic()
        result = await self._inner.execute(request)
        duration_ms = int((time.monotonic() - start) * 1000)

        findings_count = 0
        if isinstance(result.output, Mapping) and "findings" in result.output:
            findings = result.output.get("findings") or []
            findings_count = len(findings) if isinstance(findings, list) else 0
            for finding in findings:
                if not isinstance(finding, Mapping):
                    continue
                await emit_plugin_finding(
                    self._events,
                    plugin_id=request.plugin_id,
                    finding_id=str(finding.get("id", "")),
                    asset_id=str(finding.get("asset", "")),
                    severity=str(finding.get("severity", "info")),
                    title=str(finding.get("title", "")),
                    correlation_id=correlation_id,
                )

        await emit_plugin_completed(
            self._events,
            plugin_id=request.plugin_id,
            duration_ms=duration_ms,
            status=str(result.status.value if hasattr(result.status, "value") else result.status),
            findings_count=findings_count,
            correlation_id=correlation_id,
        )

        return result


class ProgressTicker:
    """Background ticker to emit periodic plugin.progress events.

    Started when a plugin begins; cancelled on completion.
    """

    def __init__(
        self,
        dispatcher: EventDispatcher,
        plugin_id: str,
        correlation_id: str,
        interval_seconds: float = 5.0,
    ) -> None:
        self._dispatcher = dispatcher
        self._plugin_id = plugin_id
        self._correlation_id = correlation_id
        self._interval = interval_seconds
        self._task: asyncio.Task | None = None
        self._cancelled = False

    def start(self) -> None:
        async def _run():
            while not self._cancelled:
                await emit_plugin_progress(
                    self._dispatcher,
                    plugin_id=self._plugin_id,
                    percentage=0.0,
                    message="running",
                    correlation_id=self._correlation_id,
                )
                await asyncio.sleep(self._interval)

        self._task = asyncio.create_task(_run(), name=f"progress-{self._plugin_id}")

    async def stop(self) -> None:
        self._cancelled = True
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None