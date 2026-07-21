"""Task Planner — the dynamic heart of the platform.

Per ARCHITECTURE.md:

  - Workflow is *static* — declares intent.
  - Task Planner is *dynamic* — owns execution topology:
      - builds a dependency DAG from `WorkflowStep.depends_on`
      - schedules ready tasks in parallel
      - enforces retries with backoff
      - enforces timeouts per task
      - cooperatively cancels running tasks
      - emits structured events on every transition

At Milestone 1 we ship:

  - A complete, deterministic DAG scheduler.
  - `NoopTaskExecutor`-driven execution, so the planner compiles and
    tests pass before any plugin exists.
  - Topology-level cancellation and timeout.
  - Optional per-step retry policy applied uniformly.

The Executor port (TaskExecutor) is overridden in later milestones to
call plugin execution, finding engine, risk engine, AI gateway, and
report engine.
"""

from __future__ import annotations

import abc
import asyncio
import contextlib
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

from ai_secos_core.infrastructure.logging import get_logger
from ai_secos_core.infrastructure.metrics import Counter, Histogram, MetricsRegistry
from ai_secos_core.runtime.cancellation import CancelledError, CancellationToken
from ai_secos_core.runtime.executor import TaskExecutor, TaskRunResult
from ai_secos_core.runtime.task import Task, TaskId, TaskState
from ai_secos_core.shared.events import EventDispatcher, make_event
from ai_secos_core.shared.value_objects import Workflow

_logger = get_logger(__name__)


@dataclass(frozen=True)
class TaskPlannerConfig:
    """Top-level knobs for the planner."""

    max_parallel: int = 4
    per_task_timeout_seconds: float | None = None
    max_retries: int = 0
    retry_backoff_seconds: float = 0.5


@dataclass(frozen=True)
class PlannedExecution:
    """Outcome of one full plan run."""

    plan_id: str
    succeeded: bool
    tasks: tuple[Task, ...]


class TaskPlanner(abc.ABC):
    """Schedule and execute a Workflow as a DAG."""

    @abc.abstractmethod
    async def run(
        self,
        workflow: Workflow,
        *,
        context: Mapping[str, Any] | None = None,
        cancellation: CancellationToken | None = None,
    ) -> PlannedExecution:
        raise NotImplementedError


@dataclass
class DefaultTaskPlanner:
    """Default planner: DAG scheduler with retries + parallel workers."""

    executor: TaskExecutor
    event_dispatcher: EventDispatcher
    metrics: MetricsRegistry
    config: TaskPlannerConfig = field(default_factory=TaskPlannerConfig)

    _semaphore: asyncio.Semaphore | None = field(default=None, init=False)
    _exec_counter: Counter | None = field(default=None, init=False)
    _plan_hist: Histogram | None = field(default=None, init=False)

    async def run(
        self,
        workflow: Workflow,
        *,
        context: Mapping[str, Any] | None = None,
        cancellation: CancellationToken | None = None,
    ) -> PlannedExecution:
        self._ensure_wired()
        ctx = dict(context or {})
        token = cancellation or CancellationToken()
        plan_id = ctx.get("plan_id") or f"plan-{id(workflow):x}"
        ctx.setdefault("plan_id", plan_id)

        tasks: list[Task] = [self._decode(step, i) for i, step in enumerate(workflow.steps)]
        task_index: dict[str, Task] = {t.id: t for t in tasks}
        # Validate deps.
        for t in tasks:
            for dep in t.depends_on:
                if dep not in task_index:
                    raise ValueError(
                        f"unknown dependency {dep!r} on task {t.name!r}"
                    )

        children: dict[str, list[str]] = {t.id: [] for t in tasks}
        for t in tasks:
            for dep in t.depends_on:
                children[dep].append(t.id)

        self._record_plan_start(plan_id)
        try:
            await self._drive(tasks, task_index, children, token, ctx)
        except CancelledError:
            for t in tasks:
                if t.state not in (
                    TaskState.SUCCEEDED,
                    TaskState.FAILED,
                    TaskState.CANCELLED,
                    TaskState.SKIPPED,
                ):
                    t.state = TaskState.CANCELLED
                    await self._emit_event("task.cancelled", plan_id, t)

        failed = [t for t in tasks if t.state is TaskState.FAILED]
        cancelled = [t for t in tasks if t.state is TaskState.CANCELLED]
        succeeded = not failed and not cancelled
        self._record_plan_end(plan_id, succeeded)
        return PlannedExecution(plan_id=plan_id, succeeded=succeeded, tasks=tuple(tasks))

    # --- internals ------------------------------------------------------------

    def _ensure_wired(self) -> None:
        if self._semaphore is None:
            self._semaphore = asyncio.Semaphore(self.config.max_parallel)
        if self._exec_counter is None:
            self._exec_counter = self.metrics.counter(
                "task_planner_executions_total",
                unit="executions",
                description="Number of tasks executed by status",
                label_names=("status",),
            )
        if self._plan_hist is None:
            self._plan_hist = self.metrics.histogram(
                "task_planner_plan_duration_ms",
                unit="ms",
                description="Plan execution wall-clock duration",
            )

    def _decode(self, step, index: int) -> Task:
        return Task.from_step(
            step_index=index,
            step_name=step.name,
            kind=step.kind,
            target=step.target,
            params=step.params,
            depends_on=step.depends_on,
        )

    async def _drive(
        self,
        tasks: list[Task],
        index: dict[TaskId, Task],
        children: dict[TaskId, list[TaskId]],
        token: CancellationToken,
        ctx: dict[str, Any],
    ) -> None:
        in_flight: set[asyncio.Task[None]] = set()
        try:
            while not self._all_done(tasks):
                if token.is_cancelled():
                    raise CancelledError
                ready = self._ready(tasks, index)
                spawned_this_round = 0
                for t in ready:
                    if t.state is not TaskState.PENDING:
                        continue
                    if token.is_cancelled():
                        raise CancelledError
                    t.state = TaskState.READY
                    spawned_this_round += 1
                    in_flight.add(
                        asyncio.create_task(
                            self._run_with_retries(t, token, ctx),
                            name=f"{t.name}-{t.id}",
                        )
                    )
                if spawned_this_round == 0 and not in_flight:
                    # No progress possible: remaining tasks are unreachable.
                    for t in tasks:
                        if t.state is TaskState.PENDING:
                            t.state = TaskState.SKIPPED
                            await self._emit_event("task.skipped", ctx["plan_id"], t)
                    break
                if in_flight:
                    done, _ = await asyncio.wait(
                        in_flight,
                        return_when=asyncio.FIRST_COMPLETED,
                    )
                    in_flight.difference_update(done)
                    if token.is_cancelled():
                        raise CancelledError
        finally:
            for coro in in_flight:
                coro.cancel()
            for coro in in_flight:
                with contextlib.suppress(BaseException):
                    await coro

    @staticmethod
    def _ready(
        tasks: list[Task],
        _index: dict[TaskId, Task],
    ) -> list[Task]:
        out: list[Task] = []
        for t in tasks:
            if t.state is not TaskState.PENDING:
                continue
            deps_satisfied = True
            for dep in t.depends_on:
                d = next((x for x in tasks if x.id == dep), None)
                if d is None:
                    deps_satisfied = False
                    break
                if d.state not in (TaskState.SUCCEEDED, TaskState.SKIPPED):
                    deps_satisfied = False
                    break
            if deps_satisfied:
                out.append(t)
        return out

    @staticmethod
    def _all_done(tasks: list[Task]) -> bool:
        return all(
            t.state in (
                TaskState.SUCCEEDED,
                TaskState.FAILED,
                TaskState.CANCELLED,
                TaskState.SKIPPED,
            )
            for t in tasks
        )

    async def _run_with_retries(
        self,
        task: Task,
        token: CancellationToken,
        ctx: dict[str, Any],
    ) -> None:
        attempts = self.config.max_retries + 1
        backoff = self.config.retry_backoff_seconds
        last_error: str | None = None
        async with self._semaphore:  # type: ignore[union-attr]
            for attempt in range(attempts):
                if token.is_cancelled():
                    task.state = TaskState.CANCELLED
                    await self._emit_event("task.cancelled", ctx["plan_id"], task)
                    return
                task.state = TaskState.RUNNING
                await self._emit_event("task.started", ctx["plan_id"], task)
                try:
                    result = await self._invoke(task, token, ctx)
                except asyncio.CancelledError:
                    task.state = TaskState.CANCELLED
                    await self._emit_event("task.cancelled", ctx["plan_id"], task)
                    raise CancelledError from None
                except Exception as exc:  # noqa: BLE001
                    last_error = str(exc)
                    self._record_task_status("failed")
                    await self._emit_event(
                        "task.error",
                        ctx["plan_id"],
                        task,
                        extra={"attempt": attempt + 1, "error": last_error},
                    )
                    if attempt < attempts - 1:
                        await asyncio.sleep(backoff * (2 ** attempt))
                        continue
                    task.state = TaskState.FAILED
                    task.error = last_error
                    await self._emit_event("task.failed", ctx["plan_id"], task)
                    return
                if result.success:
                    task.state = TaskState.SUCCEEDED
                    task.output = result.output
                    self._record_task_status("succeeded")
                    await self._emit_event("task.succeeded", ctx["plan_id"], task)
                    return
                last_error = result.error or "task reported failure"
                if attempt < attempts - 1:
                    await self._emit_event(
                        "task.retry",
                        ctx["plan_id"],
                        task,
                        extra={"attempt": attempt + 1, "error": last_error},
                    )
                    await asyncio.sleep(backoff * (2 ** attempt))
                    continue
                task.state = TaskState.FAILED
                task.error = last_error
                self._record_task_status("failed")
                await self._emit_event("task.failed", ctx["plan_id"], task)

    async def _invoke(
        self,
        task: Task,
        token: CancellationToken,
        ctx: dict[str, Any],
    ) -> TaskRunResult:
        timeout = self.config.per_task_timeout_seconds
        if timeout is None:
            return await self.executor.run(task, cancellation=token, context=ctx)
        try:
            return await asyncio.wait_for(
                self.executor.run(task, cancellation=token, context=ctx),
                timeout=timeout,
            )
        except asyncio.TimeoutError as exc:
            raise TimeoutError(f"task {task.name!r} timed out") from exc

    # --- observability --------------------------------------------------------

    def _record_task_status(self, status: str) -> None:
        if self._exec_counter is None:
            return
        try:
            self._exec_counter.inc(labels={"status": status})
        except Exception:
            pass

    def _record_plan_start(self, plan_id: str) -> None:
        self._plan_start_ns = asyncio.get_event_loop().time()

    def _record_plan_end(self, plan_id: str, success: bool) -> None:
        if self._plan_hist is None or not hasattr(self, "_plan_start_ns"):
            return
        try:
            self._plan_hist.observe(
                max(0.0, (asyncio.get_event_loop().time() - self._plan_start_ns) * 1000.0)
            )
        except Exception:
            pass

    async def _emit_event(
        self,
        event_type: str,
        plan_id: str,
        task: Task,
        *,
        extra: dict[str, Any] | None = None,
    ) -> None:
        payload: dict[str, Any] = {
            "plan_id": plan_id,
            "task_id": task.id,
            "task_name": task.name,
            "state": task.state.value,
        }
        if extra:
            payload.update(extra)
        await self.event_dispatcher.publish(
            make_event(event_type, correlation_id=plan_id, payload=payload)
        )


__all__ = [
    "TaskPlanner",
    "DefaultTaskPlanner",
    "TaskPlannerConfig",
    "PlannedExecution",
]
