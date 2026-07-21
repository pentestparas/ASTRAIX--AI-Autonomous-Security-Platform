"""Workflow Engine — declarative Workflow + Capability resolution.

A `Workflow` is data: an ordered list of `WorkflowStep` with
typography (`kind`) and dependencies (`depends_on`).

The Engine:

  - Loads `Workflow` declarations (from YAML or in-process builders).
  - Validates internal consistency.
  - DOES NOT plan/run. Planning is the Task Planner's responsibility.

At Milestone 1 we ship:

  - The typed contract `WorkflowEngine`.
  - The `DefaultWorkflowEngine`, an in-process implementation that
    resolves workflows and tracks them by id.
  - `WorkflowResolutionError` for invalid references / missing IDs.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from threading import RLock
from typing import Iterable

from ai_secos_core.shared.errors import WorkflowError
from ai_secos_core.shared.value_objects import (
    Capability,
    Workflow,
    WorkflowId,
)


class WorkflowResolutionError(WorkflowError):
    code = "workflow_resolution_error"


@dataclass(frozen=True)
class WorkflowRecord:
    """Workflow + the chain of references used to compile it."""

    workflow: Workflow
    capability: Capability | None


class WorkflowEngine(abc.ABC):
    """Declarative workflow repository.

    Engines do not *run* workflows; they resolve and validate them.
    The Task Planner turns a `Workflow` into ready-to-run Tasks.
    """

    @abc.abstractmethod
    def register(self, workflow: Workflow) -> None: ...

    @abc.abstractmethod
    def get(self, workflow_id: WorkflowId) -> WorkflowRecord: ...

    @abc.abstractmethod
    def list(self) -> list[WorkflowRecord]: ...


@dataclass
class DefaultWorkflowEngine:
    """Process-local default engine.

    Workflows are stored by id. Capabilities are optional references
    used to compile the workflow; missing ones produce a
    `WorkflowResolutionError` when the workflow is consumed.
    """

    capabilities: dict[WorkflowId, Capability] = field(default_factory=dict)
    _workflows: dict[WorkflowId, Workflow] = field(default_factory=dict)
    _lock: RLock = field(default_factory=RLock)

    def register(self, workflow: Workflow) -> None:
        with self._lock:
            self._workflows[WorkflowId(workflow.id)] = workflow

    def register_capability(self, capability: Capability) -> None:
        with self._lock:
            for wf_id in capability.workflows:
                self.capabilities[WorkflowId(wf_id)] = capability

    def get(self, workflow_id: WorkflowId) -> WorkflowRecord:
        with self._lock:
            wf = self._workflows.get(workflow_id)
            if wf is None:
                raise WorkflowResolutionError(
                    f"workflow not registered: {workflow_id}",
                    details={"workflow_id": workflow_id},
                )
            cap = self.capabilities.get(workflow_id)
            return WorkflowRecord(workflow=wf, capability=cap)

    def list(self) -> list[WorkflowRecord]:
        with self._lock:
            return [
                WorkflowRecord(workflow=wf, capability=self.capabilities.get(wid))
                for wid, wf in self._workflows.items()
            ]

    def ids(self) -> list[WorkflowId]:
        with self._lock:
            return sorted(self._workflows.keys())


__all__ = [
    "WorkflowEngine",
    "DefaultWorkflowEngine",
    "WorkflowResolutionError",
    "WorkflowRecord",
]
