"""Task Executor — runs a Task.

A planner produces Tasks; the executor is what runs a single Task.
At Milestone 1 the `NoopTaskExecutor` is the only implementation. The
real Executor (which calls into plugin_system, finding_engine, etc.)
will override this in later milestones.

Why a port at M1?

  - Allows the planner to be exercised end-to-end (task state machine,
    parallelism, retries) before any plugin exists.
  - Forces the interface to be designed even before the implementations
    arrive, reducing architectural drift.

The contract:

  - `run(task, cancellation, context)` produces an Awaitable result.
  - `context` is a typed map for executor-specific data.
"""

from __future__ import annotations

import abc
import asyncio
from dataclasses import dataclass
from typing import Any, Mapping

from ai_secos_core.runtime.cancellation import CancellationToken
from ai_secos_core.runtime.task import Task


@dataclass(frozen=True)
class TaskRunResult:
    task: Task
    output: Any
    success: bool
    error: str | None = None


class TaskExecutor(abc.ABC):
    """Run a single Task and emit a result."""

    @abc.abstractmethod
    async def run(
        self,
        task: Task,
        *,
        cancellation: CancellationToken,
        context: Mapping[str, Any],
    ) -> TaskRunResult:
        raise NotImplementedError


class NoopTaskExecutor:
    """Default at Milestone 1.

    The executor performs the bare minimum: a `result`-only step
    identity that records the params it received. Useful for
    end-to-end scheduler tests without any plugin installed.
    """

    async def run(
        self,
        task: Task,
        *,
        cancellation: CancellationToken,
        context: Mapping[str, Any],
    ) -> TaskRunResult:
        if cancellation.is_cancelled():
            return TaskRunResult(
                task=task,
                output=None,
                success=False,
                error="cancelled",
            )
        # Simulate work; in real executors this dispatches to a plugin,
        # an AI Gateway call, a report renderer, etc.
        await asyncio.sleep(0)
        return TaskRunResult(
            task=task,
            output={"params": task.params, "kind": task.kind.value},
            success=True,
        )


__all__ = [
    "TaskExecutor",
    "NoopTaskExecutor",
    "TaskRunResult",
]
