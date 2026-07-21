"""Reusable value objects (the platform's vocabulary).

These are the typed shapes that flow between AI-SecOS Core modules and
between the Core and Applications. Nothing in this module raises or
performs I/O; it only defines data.
"""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, NewType

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
)
from typing_extensions import Annotated

# --- Type brands ---------------------------------------------------------

CapabilityId = NewType("CapabilityId", str)
PluginId = NewType("PluginId", str)
WorkflowId = NewType("WorkflowId", str)
AssetId = NewType("AssetId", str)
AssessmentId = NewType("AssessmentId", str)
CorrelationId = NewType("CorrelationId", str)

_ID_PATTERN = r"^[a-z][a-z0-9_]*(/[a-z][a-z0-9_]*)?$"
_LOWERCASE = Annotated[str, StringConstraints(pattern=_ID_PATTERN, max_length=128)]


# --- Enumerations --------------------------------------------------------

class Severity(str, Enum):
    """Severity levels, ordered from informational to critical."""

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    @classmethod
    def _missing_(cls, value: object) -> "Severity | None":  # type: ignore[override]
        # Tolerate mixed-case input.
        if isinstance(value, str):
            v = value.lower()
            for member in cls:
                if member.value == v:
                    return member
        return None


class WorkflowStepKind(str, Enum):
    """The kinds of step a Workflow may declare."""

    CAPABILITY = "capability"
    SCAN = "scan"
    NORMALIZE = "normalize"
    RISK = "risk"
    AI_ANALYZE = "ai_analyze"
    REPORT = "report"


# --- Capability ----------------------------------------------------------

class CapabilityVersion(BaseModel):
    """SemVer-style version (integer triple)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    major: int = Field(ge=0)
    minor: int = Field(ge=0)
    patch: int = Field(ge=0)

    def __str__(self) -> str:  # noqa: D401
        return f"{self.major}.{self.minor}.{self.patch}"


class SupportedAssetType(BaseModel):
    """An asset type a Capability can handle (e.g. 'domain', 'ip')."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    type: Annotated[str, StringConstraints(pattern=r"^[a-z][a-z0-9_]*$", max_length=64)]


class RequiredPlugin(BaseModel):
    """A Plugin a Capability depends on."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: PluginId
    min_version: CapabilityVersion


class ComplianceTag(BaseModel):
    """A compliance framework mapping."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    framework: str = Field(min_length=2, max_length=64)
    control: str = Field(min_length=1, max_length=64)


class Capability(BaseModel):
    """A first-class declaration of a security capability.

    Capabilities are *resolved* by the Workflow Engine into concrete
    Workflows at runtime. Applications request a Capability by id; they
    never reference a Plugin by name directly.
    """

    model_config = ConfigDict(extra="forbid", frozen=False)

    id: _LOWERCASE
    version: CapabilityVersion
    display_name: str = Field(min_length=1, max_length=128)
    description: str = ""

    workflows: list[WorkflowId] = Field(default_factory=list)
    supported_assets: list[SupportedAssetType] = Field(default_factory=list)
    required_plugins: list[RequiredPlugin] = Field(default_factory=list)
    compliance: list[ComplianceTag] = Field(default_factory=list)


# --- Workflow ------------------------------------------------------------

class WorkflowStep(BaseModel):
    """Single step inside a Workflow declaration.

    `kind` selects how the Task Planner should interpret this step.
    """

    model_config = ConfigDict(extra="forbid")

    name: Annotated[str, StringConstraints(min_length=1, max_length=128)]
    kind: WorkflowStepKind
    target: str | None = None           # identifier of capability/step
    depends_on: list[str] = Field(default_factory=list)  # local-names within workflow
    params: dict[str, Any] = Field(default_factory=dict)


class Workflow(BaseModel):
    """Declarative Workflow (YAML-loadable).

    Pure data. Interpretation happens in `runtime/` (Task Planner).
    """

    model_config = ConfigDict(extra="forbid")

    id: _LOWERCASE
    description: str = ""
    steps: list[WorkflowStep] = Field(min_length=1)

    @field_validator("steps")
    @classmethod
    def _step_names_unique(cls, value: list[WorkflowStep]) -> list[WorkflowStep]:
        names = [s.name for s in value]
        if len(set(names)) != len(names):
            raise ValueError("workflow step names must be unique")
        return value


# --- Canonical Security Finding -----------------------------------------

class FindingEvidence(BaseModel):
    """Opaque evidence payload attached to a SecurityFinding.

    Downstream code reads only declared fields of SecurityFinding;
    `evidence` is opaque and treated as untrusted. The AI Gateway
    never sees it directly; only summary text derived from it.
    """

    model_config = ConfigDict(extra="allow", frozen=False)

    schema_name: str = Field(default="unknown", max_length=64)
    raw: Any = None


FindingFingerprint = NewType("FindingFingerprint", str)


class Confidence(float):
    """Validated confidence score: 0.0–1.0."""

    def __new__(cls, value: float) -> "Confidence":
        if not 0.0 <= float(value) <= 1.0:
            raise ValueError(f"confidence must be 0.0–1.0, got {value}")
        return super().__new__(cls, float(value))


def _default_fingerprint_key() -> str:
    return uuid.uuid4().hex


class SecurityFinding(BaseModel):
    """Universal language of the platform.

    Two findings with identical `(asset, cwe, cve, plugin)` collapse to one
    canonical record via the fingerprint.
    """

    model_config = ConfigDict(extra="forbid", frozen=False)

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    assessment_id: AssessmentId
    asset: _LOWERCASE
    capability: _LOWERCASE
    plugin: PluginId
    category: Annotated[str, StringConstraints(min_length=1, max_length=64)] = "uncategorized"

    title: str = Field(min_length=1, max_length=512)
    description: str = ""

    severity: Severity
    confidence: float = Field(ge=0.0, le=1.0)
    risk_score: float | None = Field(default=None, ge=0.0, le=100.0)

    cvss: float | None = Field(default=None, ge=0.0, le=10.0)
    cwe: list[str] = Field(default_factory=list)
    cve: list[str] = Field(default_factory=list)
    owasp: list[str] = Field(default_factory=list)

    evidence: FindingEvidence | None = None
    references: list[str] = Field(default_factory=list)
    remediation: str = ""
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    fingerprint: FindingFingerprint = Field(default_factory=FindingFingerprint)
    first_seen: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_seen: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("references")
    @classmethod
    def _validate_urls(cls, value: list[str]) -> list[str]:
        url_re = re.compile(r"^https?://[^\s]+$")
        for u in value:
            if not url_re.match(u):
                raise ValueError(f"invalid reference url: {u!r}")
        return value


# --- Public re-exports --------------------------------------------------

__all__ = [
    # type brands
    "CapabilityId",
    "PluginId",
    "WorkflowId",
    "AssetId",
    "AssessmentId",
    "CorrelationId",
    # enums
    "Severity",
    "WorkflowStepKind",
    # capability
    "Capability",
    "CapabilityVersion",
    "SupportedAssetType",
    "RequiredPlugin",
    "ComplianceTag",
    # workflow
    "Workflow",
    "WorkflowStep",
    # finding
    "SecurityFinding",
    "FindingEvidence",
    "FindingFingerprint",
]
