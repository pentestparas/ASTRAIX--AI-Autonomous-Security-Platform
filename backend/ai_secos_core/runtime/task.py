"""Task — the unit the Task Planner reasons about.

A `Task` is a step decoded from a `Workflow`. It carries:

  - `id`: opaque, planner-local identifier.
  - `name`: human-readable label.
  - `kind`: declaration of what this step is (Capability/Plugin/etc).
  - `depends_on`: edge dependencies (other task ids in the same plan).
  - `params`: opaque payload for the executor.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Sequence

from ai_secos_core.shared.value_objects import WorkflowStepKind


TaskId = str


class TaskState(str, Enum):
    """Discrete lifecycle states of a Task."""

    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SKIPPED = "skipped"


@dataclass
class Task:
    id: TaskId
    name: str
    kind: WorkflowStepKind
    target: str | None
    params: dict[str, Any]
    depends_on: tuple[TaskId, ...] = field(default_factory=tuple)
    state: TaskState = TaskState.PENDING
    error: str | None = None
    output: Any = None

    @classmethod
    def from_step(
        cls,
        step_index: int,
        step_name: str,
        kind: WorkflowStepKind,
        target: str | None,
        params: dict[str, Any],
        depends_on: Sequence[str] = (),
    ) -> "Task":
        return cls(
            id=f"t{step_index}",
            name=step_name,
            kind=kind,
            target=target,
            params=dict(params),
            depends_on=tuple(depends_on),
        )


__all__ = [
    "Task",
    "TaskId",
    "TaskState",
]
