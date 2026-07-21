"""Runtime — Workflow Engine + Task Planner.

The Runtime is the *executable* heart of the platform.

Sub-modules:

  - `task.py`         typed `Task` + `TaskState` (the planner's unit).
  - `workflow.py`     a `Workflow`, parsed from YAML.
  - `workflow_engine.py`  resolves Capabilities → Workflows (declarative).
  - `task_planner.py` builds a DAG, schedules tasks, executes them.
  - `executor.py`     thin wrapper around plugin/engine execution.
  - `cancellation.py` cancellation token type.
  - `runtime.py`      end-to-end compositor; entry points.

At Milestone 1:

  - All steps are NO-OPS by default. No plugin is ever invoked here.
  - The Task Planner runs a DAG and reports state transitions via
    `EventDispatcher`. It's hot-swappable with plugin execution.

This module compiles and tests even with zero plugins.
"""

from ai_secos_core.runtime.task import (
    Task,
    TaskState,
    TaskId,
)
from ai_secos_core.runtime.workflow import (
    Workflow,
    WorkflowLoaderError,
)
from ai_secos_core.runtime.workflow_engine import (
    WorkflowEngine,
    WorkflowResolutionError,
    DefaultWorkflowEngine,
)
from ai_secos_core.runtime.task_planner import (
    TaskPlanner,
    TaskPlannerConfig,
    PlannedExecution,
    DefaultTaskPlanner,
)
from ai_secos_core.runtime.cancellation import (
    CancellationToken,
    CancelledError,
)
from ai_secos_core.runtime.executor import (
    TaskExecutor,
    NoopTaskExecutor,
)

__all__ = [
    "Task",
    "TaskState",
    "TaskId",
    "Workflow",
    "WorkflowLoaderError",
    "WorkflowEngine",
    "WorkflowResolutionError",
    "DefaultWorkflowEngine",
    "TaskPlanner",
    "TaskPlannerConfig",
    "PlannedExecution",
    "DefaultTaskPlanner",
    "CancellationToken",
    "CancelledError",
    "TaskExecutor",
    "NoopTaskExecutor",
]
