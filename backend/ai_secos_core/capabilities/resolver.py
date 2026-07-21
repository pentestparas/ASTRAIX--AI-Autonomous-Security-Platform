"""Capability Resolver.

Resolves a `Capability` request into a concrete execution plan:
  - Capability
  - Capability Version
  - Input Parameters
  - Underlying Workflows (one or more)
  - Required plugins
  - Compliance mapping
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from ai_secos_core.capabilities.errors import CapabilityResolverError
from ai_secos_core.capabilities.models import Capability, RequiredPlugin
from ai_secos_core.runtime.workflow_engine import DefaultWorkflowEngine, WorkflowRecord
from ai_secos_core.shared.errors import PlatformError
from ai_secos_core.shared.value_objects import Workflow


class ResolutionError(PlatformError):
    """Raised when capability resolution fails."""

    code = "capability_resolution_error"
    http_status = 422


@dataclass(frozen=True)
class ResolvedCapability:
    """A Capability fully resolved to executable Workflows."""

    capability: Capability
    workflows: tuple[WorkflowRecord, ...]
    inputs: Dict[str, Any]
    missing_plugins: tuple[RequiredPlugin, ...]

    @property
    def is_executable(self) -> bool:
        return len(self.missing_plugins) == 0 and len(self.workflows) > 0


class CapabilityResolver:
    """Resolves Capabilities to WorkflowRecords ready for the Task Planner."""

    def __init__(
        self,
        capability_registry: "CapabilityRegistry",
        workflow_engine: DefaultWorkflowEngine,
        installed_plugins: Optional[frozenset[str]] = None,
    ) -> None:
        self._capabilities = capability_registry
        self._workflows = workflow_engine
        self._installed_plugins = installed_plugins or frozenset()

    def resolve(
        self,
        capability_id: str,
        inputs: Dict[str, Any],
        version: Optional[str] = None,
    ) -> ResolvedCapability:
        try:
            capability = self._capabilities.get(capability_id, version)
        except Exception as exc:  # CapabilityNotFoundError
            raise ResolutionError(
                f"capability not resolvable: {capability_id}",
            ) from exc

        workflows: list[WorkflowRecord] = []
        missing_workflow_ids: list[str] = []
        for wf_id in capability.workflows:
            try:
                record = self._workflows.get(wf_id)
            except Exception:
                missing_workflow_ids.append(str(wf_id))
                continue
            workflows.append(record)

        if missing_workflow_ids:
            raise ResolutionError(
                f"missing workflows for capability {capability_id}: "
                f"{missing_workflow_ids}",
                details={
                    "capability_id": capability_id,
                    "missing_workflows": missing_workflow_ids,
                },
            )

        missing_plugins: tuple[RequiredPlugin, ...] = tuple(
            req
            for req in capability.required_plugins
            if req.plugin_id not in self._installed_plugins
        )

        normalized_inputs = self._validate_inputs(capability, inputs)

        return ResolvedCapability(
            capability=capability,
            workflows=tuple(workflows),
            inputs=normalized_inputs,
            missing_plugins=missing_plugins,
        )

    def _validate_inputs(
        self, capability: Capability, inputs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate inputs against the capability's input schema (lightweight).

        Performs only `required` checks at M2; richer JSON Schema
        validation arrives later.
        """
        if not capability.inputs.required:
            return inputs
        missing = [
            key for key in capability.inputs.required if key not in inputs
        ]
        if missing:
            raise ResolutionError(
                f"missing required inputs: {missing}",
                details={"capability_id": capability.id, "missing": missing},
            )
        return inputs


from ai_secos_core.capabilities.registry import CapabilityRegistry