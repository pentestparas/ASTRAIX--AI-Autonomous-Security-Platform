"""Workflow — declarative YAML-loadable structure.

Reuse of the canonical `Workflow` value object from `shared/`, plus
a YAML loader that turns workflows on disk into typed objects.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from ai_secos_core.shared.errors import WorkflowError
from ai_secos_core.shared.value_objects import Workflow, WorkflowStep


class WorkflowLoaderError(WorkflowError):
    code = "workflow_loader_error"


@dataclass(frozen=True)
class _YamlBundle:
    path: Path
    data: dict[str, object]


def load_workflow_from_yaml(path: Path | str) -> Workflow:
    """Read a YAML workflow file and return a typed `Workflow`.

    Raises `WorkflowLoaderError` on missing/invalid files.
    """
    p = Path(path)
    if not p.is_file():
        raise WorkflowLoaderError(
            f"workflow file missing: {p}",
            details={"path": str(p)},
        )
    try:
        raw = yaml.safe_load(p.read_text())
    except yaml.YAMLError as exc:
        raise WorkflowLoaderError(
            f"invalid YAML: {p}", details={"path": str(p)}
        ) from exc
    if not isinstance(raw, dict):
        raise WorkflowLoaderError(
            f"workflow must be a mapping: {p}", details={"path": str(p)}
        )
    steps_raw = raw.get("steps", [])
    if not isinstance(steps_raw, list) or not steps_raw:
        raise WorkflowLoaderError(
            f"workflow requires non-empty 'steps' list: {p}",
            details={"path": str(p)},
        )
    steps: list[WorkflowStep] = []
    for i, item in enumerate(steps_raw):
        if not isinstance(item, dict):
            raise WorkflowLoaderError(
                f"step #{i} must be a mapping: {p}",
                details={"path": str(p)},
            )
        try:
            steps.append(WorkflowStep(**item))
        except Exception as exc:  # pydantic.ValidationError
            raise WorkflowLoaderError(
                f"step #{i} invalid: {exc}",
                details={"path": str(p)},
            ) from exc
    try:
        return Workflow(
            id=str(raw.get("id", p.stem)),
            description=str(raw.get("description", "")),
            steps=steps,
        )
    except Exception as exc:
        raise WorkflowLoaderError(
            f"workflow invalid: {p}: {exc}",
            details={"path": str(p)},
        ) from exc


__all__ = [
    "load_workflow_from_yaml",
    "WorkflowLoaderError",
]
