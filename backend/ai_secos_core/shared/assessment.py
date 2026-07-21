"""Assessment Model — central intent of a security run.

An `Assessment` ties together:
  - The asset(s) being assessed
  - The capability invoked
  - The workflows executed
  - The findings produced
  - The state (running/completed/failed/cancelled)
  - The history (state transitions)

This is the model that Applications submit and that the platform
tracks over time.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
import uuid


class AssessmentStatus(str, Enum):
    """Discrete lifecycle states."""

    PENDING = "pending"        # not yet started
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


@dataclass(frozen=True)
class AssessmentConfiguration:
    """User-supplied knobs at assessment submission time."""

    capability_id: str
    capability_version: Optional[str] = None
    inputs: Dict[str, Any] = field(default_factory=dict)
    timeout_seconds: Optional[int] = None
    max_parallel_tasks: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AssessmentResult:
    """The persisted output of an assessment."""

    finding_ids: Tuple[str, ...] = ()
    risk_scores: Tuple[float, ...] = ()
    report_artifact_ids: Tuple[str, ...] = ()
    error: Optional[str] = None


@dataclass(frozen=True)
class AssessmentTransition:
    """A single lifecycle event on an Assessment."""

    from_state: AssessmentStatus
    to_state: AssessmentStatus
    at: datetime
    correlation_id: str = ""
    reason: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Assessment:
    """A full security-assessment intent.

    Lifecycle:
      1. Application submits → Assessment (PENDING)
      2. Capability resolved → status = RUNNING
      3. Workflow tasks execute → produce findings
      4. Result persisted → status = COMPLETED | FAILED | CANCELLED
    """

    id: str
    configuration: AssessmentConfiguration
    asset_ids: Tuple[str, ...]
    target_assets: Tuple[str, ...] = ()  # serialized asset identifiers (string form)
    status: AssessmentStatus = AssessmentStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[AssessmentResult] = None
    history: List[AssessmentTransition] = field(default_factory=list)
    correlation_id: str = ""

    @classmethod
    def create(
        cls,
        configuration: AssessmentConfiguration,
        asset_ids: Tuple[str, ...],
        target_assets: Optional[Tuple[str, ...]] = None,
    ) -> "Assessment":
        return cls(
            id=str(uuid.uuid4()),
            configuration=configuration,
            asset_ids=asset_ids,
            target_assets=target_assets or (),
        )

    def transition(
        self,
        to_state: AssessmentStatus,
        *,
        reason: str = "",
        correlation_id: str = "",
        metadata: Optional[Dict[str, Any]] = None,
        at: Optional[datetime] = None,
    ) -> "Assessment":
        """Record a state transition. Returns self (for fluent use)."""
        self.history.append(
            AssessmentTransition(
                from_state=self.status,
                to_state=to_state,
                at=at or datetime.utcnow(),
                correlation_id=correlation_id or self.correlation_id,
                reason=reason,
                metadata=metadata or {},
            )
        )
        self.status = to_state
        if to_state in (
            AssessmentStatus.COMPLETED,
            AssessmentStatus.FAILED,
            AssessmentStatus.CANCELLED,
            AssessmentStatus.TIMEOUT,
        ):
            self.completed_at = datetime.utcnow()
        elif to_state is AssessmentStatus.RUNNING and self.started_at is None:
            self.started_at = datetime.utcnow()
        return self

    def is_terminal(self) -> bool:
        return self.status in (
            AssessmentStatus.COMPLETED,
            AssessmentStatus.FAILED,
            AssessmentStatus.CANCELLED,
            AssessmentStatus.TIMEOUT,
        )