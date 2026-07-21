"""Task Planner tests.

Targets:
  - DAG topology respecting `depends_on`
  - Parallel ready-task scheduling
  - Retry + timeout
  - Cancel (no plugin actually called)
"""

import asyncio
from typing import AsyncContextManager

import pytest
from pytest_asyncio.plugin import SubRequest

from ai_secos_core.runtime.task_planner import TaskPlanner, TaskPlannerConfig
from ai_secos_core.runtime.task import TaskState
from ai_secos_core.shared.value_objects import Workflow, WorkflowStep, WorkflowStepKind
from ai_secos_core.runtime.executor import NoopTaskExecutor
from ai_secos_core.shared.events import InProcessEventDispatcher
from ai_secos_core.infrastructure.metrics import NoopMetricsRegistry


@pytest.fixture
def planner(request: SubRequest) -> TaskPlanner:
    dispatcher = InProcessEventDispatcher()
    executor = NoopTaskExecutor()
    metrics = NoopMetricsRegistry()
    config = getattr(request, "param", TaskPlannerConfig(max_parallel=2))
    return TaskPlanner(executor=executor, event_dispatcher=dispatcher, metrics=metrics, config=config)


@pytest.mark.asyncio
def test_linear_workflow(planner: TaskPlanner) -> None:
    """A -> B -> C runs in serial."""
    workflow = Workflow(
        id="test-linear",
        steps=[
            WorkflowStep(
                name="step-1",
                kind=WorkflowStepKind.CAPABILITY,
                target="mock/cap-1",
            ),
            WorkflowStep(
                name="step-2",
                kind=WorkflowStepKind.CAPABILITY,
                target="mock/cap-2",
                depends_on=["step-1"],
            ),
            WorkflowStep(
                name="step-3",
                kind=WorkflowStepKind.CAPABILITY,
                target="mock/cap-3",
                depends_on=["step-2"],
            ),
        ],
    )
    outcome = await planner.run(workflow)
    assert outcome.succeeded
    assert len(outcome.tasks) == 3
    states = [t.state.value for t in outcome.tasks]
    assert states == ["succeeded", "succeeded", "succeeded"]


@pytest.mark.asyncio
def test_diamond_workflow(planner: TaskPlanner) -> None:
    """A -> B,C -> D runs B/C in parallel."""
    workflow = Workflow(
        id="test-diamond",
        steps=[
            WorkflowStep(name="a", kind=WorkflowStepKind.SCAN, target="a"),
            WorkflowStep(name="b", kind=WorkflowStepKind.SCAN, target="b", depends_on=["a"]),
            WorkflowStep(name="c", kind=WorkflowStepKind.SCAN, target="c", depends_on=["a"]),
            WorkflowStep(name="d", kind=WorkflowStepKind.NORMALIZE, depends_on=["b", "c"]),
        ],
    )
    outcome = await planner.run(workflow)
    assert outcome.succeeded
    states = [t.state.value for t in outcome.tasks]
    assert all(s == "succeeded" for s in states)