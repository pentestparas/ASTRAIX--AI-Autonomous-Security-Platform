"""Capability data models.

A `Capability` is a versioned, first-class object that the Workflow Engine
resolves into one or more workflows at runtime. Applications request
`Capability` by id and version; they never reference plugins or tools
directly.

The model follows the architecture spec (capabilities are declarative,
typed, versioned; resolve to workflows, support asset types, declare
required plugins, map to compliance frameworks).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, FrozenSet, List, Optional, Tuple

from pydantic import BaseModel, ConfigDict, Field as PField, StringConstraints
from typing_extensions import Annotated

from ai_secos_core.shared.value_objects import CapabilityId, WorkflowId


class ComplianceFramework(str, Enum):
    """Compliance frameworks a capability may map to."""

    OWASP_ASVS = "owasp_asvs"
    OWASP_TOP10 = "owasp_top10"
    SOC2 = "soc2"
    ISO_27001 = "iso_27001"
    PCI_DSS = "pci_dss"
    HIPAA = "hipaa"
    NIST_CSF = "nist_csf"
    NIST_800_53 = "nist_800_53"
    CIS = "cis"


class AssetCategory(str, Enum):
    """Asset categories a capability can scan."""

    DOMAIN = "domain"
    HOST = "host"
    URL = "url"
    API = "api"
    REPOSITORY = "repository"
    MOBILE_APP = "mobile_app"
    CONTAINER = "container"
    KUBERNETES_CLUSTER = "kubernetes_cluster"
    AI_AGENT = "ai_agent"
    LLM_ENDPOINT = "llm_endpoint"
    CLOUD_ACCOUNT = "cloud_account"
    S3_BUCKET = "s3_bucket"
    IAM_ROLE = "iam_role"
    DATABASE = "database"


@dataclass(frozen=True)
class ComplianceTag:
    """A compliance framework mapping (one capability can map to many)."""

    framework: ComplianceFramework
    control: str
    rationale: str = ""


@dataclass(frozen=True)
class RequiredPlugin:
    """A Plugin required by the capability (plugin_id, min_version)."""

    plugin_id: str
    min_version: str
    role: str = "primary"  # primary | secondary


@dataclass(frozen=True)
class SupportedAssetType:
    """An asset type the capability operates on."""

    category: AssetCategory
    description: str = ""


@dataclass(frozen=True)
class CapabilityInputSchema:
    """Schema describing capability inputs (JSON Schema-like)."""

    type: str = "object"
    required: Tuple[str, ...] = ()
    properties: Tuple[Tuple[str, dict[str, Any]], ...] = ()
    additional_properties: bool = True


@dataclass(frozen=True)
class CapabilityOutputSchema:
    """Schema describing capability outputs (one or more finding types)."""

    finding_kinds: Tuple[str, ...] = ()  # e.g. "open_port", "exposed_endpoint"
    asset_types: Tuple[AssetCategory, ...] = ()


@dataclass(frozen=True)
class CapabilityVersion:
    """Semantic version (major.minor.patch)."""

    major: int
    minor: int
    patch: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    @classmethod
    def parse(cls, version_str: str) -> "CapabilityVersion":
        parts = version_str.split(".")
        if len(parts) != 3:
            raise ValueError(f"invalid version: {version_str}")
        return cls(
            major=int(parts[0]),
            minor=int(parts[1]),
            patch=int(parts[2]),
        )

    def __lt__(self, other: "CapabilityVersion") -> bool:
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)


@dataclass(frozen=True)
class CapabilityManifest:
    """Declarative manifest of a Capability (YAML-loadable).

    Imports-cap: this is *data*, not behavior. The CapabilityResolver
    reads it and resolves to workflows.
    """

    id: str = PField(...)
    version: str = PField(...)
    display_name: str = PField(...)
    description: str = PField(default="")
    inputs: CapabilityInputSchema = PField(default_factory=CapabilityInputSchema)
    outputs: CapabilityOutputSchema = PField(default_factory=CapabilityOutputSchema)
    supported_assets: Tuple[SupportedAssetType, ...] = PField(default_factory=tuple)
    workflows: Tuple[WorkflowId, ...] = PField(default_factory=tuple)
    required_plugins: Tuple[RequiredPlugin, ...] = PField(default_factory=tuple)
    compliance: Tuple[ComplianceTag, ...] = PField(default_factory=tuple)

    def to_capability(self) -> "Capability":
        """Promote this manifest to an executable Capability."""
        return Capability(
            id=self.id,
            version=CapabilityVersion.parse(self.version),
            display_name=self.display_name,
            description=self.description,
            inputs=self.inputs,
            outputs=self.outputs,
            supported_assets=self.supported_assets,
            workflows=self.workflows,
            required_plugins=self.required_plugins,
            compliance=self.compliance,
        )


@dataclass(frozen=True)
class Capability:
    """Executable Capability.

    This is what Applications interact with. Capabilities are resolved to
    Workflows via the CapabilityResolver.
    """

    id: str
    version: CapabilityVersion
    display_name: str
    description: str
    inputs: CapabilityInputSchema
    outputs: CapabilityOutputSchema
    supported_assets: Tuple[SupportedAssetType, ...]
    workflows: Tuple[WorkflowId, ...]
    required_plugins: Tuple[RequiredPlugin, ...]
    compliance: Tuple[ComplianceTag, ...]

    def supports_asset(self, category: AssetCategory) -> bool:
        return any(s.category == category for s in self.supported_assets)

    def requires_plugin(self, plugin_id: str) -> bool:
        return any(r.plugin_id == plugin_id for r in self.required_plugins)

    def compliance_mappings(self) -> Tuple[ComplianceTag, ...]:
        return self.compliance