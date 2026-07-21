"""Asset Model — universal asset representation.

An `Asset` is anything that can be scanned or assessed: a domain, URL,
API, repository, mobile app, container, Kubernetes cluster, AI agent,
LLM endpoint, cloud account, etc.

Assets are the *center of gravity* in security assessments. Findings
are attached to assets, risk scores are tied to assets, reports roll
up by asset.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
import uuid


class AssetType(str, Enum):
    """All asset types the platform understands."""

    DOMAIN = "domain"
    HOST = "host"
    URL = "url"
    API = "api"
    REPOSITORY = "repository"
    MOBILE_APP = "mobile_app"
    CONTAINER_IMAGE = "container_image"
    KUBERNETES_CLUSTER = "kubernetes_cluster"
    AI_AGENT = "ai_agent"
    LLM_ENDPOINT = "llm_endpoint"
    CLOUD_ACCOUNT = "cloud_account"
    S3_BUCKET = "s3_bucket"
    IAM_ROLE = "iam_role"
    DATABASE = "database"
    NETWORK = "network"


class AssetCriticality(str, Enum):
    """How critical this asset is to the business."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class AssetIdentifier:
    """Type-safe identifier for an asset (the `value` is asset-type-specific)."""

    type: AssetType
    value: str

    def __str__(self) -> str:
        return f"{self.type.value}:{self.value}"


@dataclass(frozen=True)
class Asset:
    """A scanned or assessable target.

    Findings reference `asset_id`; the canonical `SecurityFinding.asset`
    field stores the string form of `AssetIdentifier`.
    """

    id: str
    type: AssetType
    value: str

    display_name: str = ""
    description: str = ""
    criticality: AssetCriticality = AssetCriticality.MEDIUM
    tags: Tuple[str, ...] = ()
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Discovery & ecosystem context
    discovered_at: Optional[datetime] = None
    last_scanned_at: Optional[datetime] = None
    parent_asset_id: Optional[str] = None  # hierarchy (e.g. cloud account contains S3 bucket)

    # Graph relationships (filled by the knowledge graph module in M3+)
    related_assets: Tuple[str, ...] = ()
    technologies: Tuple[str, ...] = ()  # detected tech (Wappalyzer-style)

    @property
    def identifier(self) -> AssetIdentifier:
        return AssetIdentifier(type=self.type, value=self.value)

    @property
    def canonical_string(self) -> str:
        """The string used in `SecurityFinding.asset`."""
        return str(self.identifier)

    def child_asset(
        self,
        asset_type: AssetType,
        value: str,
        **kwargs: Any,
    ) -> "Asset":
        """Create a child asset under this one."""
        return Asset(
            id=str(uuid.uuid4()),
            type=asset_type,
            value=value,
            parent_asset_id=self.id,
            **kwargs,
        )


@dataclass(frozen=True)
class AssetInventory:
    """A bounded universe of assets derived from a Discovery capability."""

    assets: Tuple[Asset, ...] = ()
    roots: Tuple[str, ...] = ()  # asset ids that were "entry points"
    discovered_at: Optional[datetime] = None

    def by_id(self, asset_id: str) -> Optional[Asset]:
        for a in self.assets:
            if a.id == asset_id:
                return a
        return None

    def by_type(self, asset_type: AssetType) -> Tuple[Asset, ...]:
        return tuple(a for a in self.assets if a.type == asset_type)

    def roots(self) -> Tuple[Asset, ...]:
        return tuple(a for a in self.assets if a.id in self.roots)