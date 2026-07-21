"""Shared cross-cutting primitives.

Exports:
  - Platform error hierarchy.
  - Event dispatcher (in-process, swappable later).
  - Correlation id context.
  - Reusable value objects (Capability, Workflow, SecurityFinding).
"""

from ai_secos_core.shared.errors import (
    PlatformError,
    PluginError,
    WorkflowError,
    AIError,
    FindingEngineError,
    RiskEngineError,
    ReportEngineError,
    ConfigurationError,
)
from ai_secos_core.shared.events import (
    DomainEvent,
    EventDispatcher,
    InProcessEventDispatcher,
)
from ai_secos_core.shared.correlation import (
    CorrelationId,
    correlation_id_var,
    new_correlation_id,
)
from ai_secos_core.shared.value_objects import (
    Capability,
    CapabilityVersion,
    Workflow,
    WorkflowStep,
    WorkflowStepKind,
    Severity,
    Confidence,
    SecurityFinding,
    FindingEvidence,
    FindingFingerprint,
)
from ai_secos_core.shared.results import (
    Result,
    Success,
    Failure,
    ok,
    fail,
    is_ok,
    is_failure,
)

__all__ = [
    # errors
    "PlatformError",
    "PluginError",
    "WorkflowError",
    "AIError",
    "FindingEngineError",
    "RiskEngineError",
    "ReportEngineError",
    "ConfigurationError",
    # events
    "DomainEvent",
    "EventDispatcher",
    "InProcessEventDispatcher",
    # correlation ids
    "CorrelationId",
    "correlation_id_var",
    "new_correlation_id",
    # value objects
    "Capability",
    "CapabilityVersion",
    "Workflow",
    "WorkflowStep",
    "WorkflowStepKind",
    "Severity",
    "Confidence",
    "SecurityFinding",
    "FindingEvidence",
    "FindingFingerprint",
    # results
    "Result",
    "Success",
    "Failure",
    "ok",
    "fail",
    "is_ok",
    "is_failure",
]
