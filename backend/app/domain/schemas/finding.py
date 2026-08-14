from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.schemas.base import BaseSchema
from app.domain.schemas.asset import AssetRead


class FindingBase(BaseModel):
    severity: str
    title: str
    description: Optional[str] = None
    details: Dict[str, Any] = {}
    remediation: Optional[str] = None
    reference: Optional[str] = None


class FindingRead(FindingBase, BaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    organization_id: Optional[str] = None
    project_id: Optional[str] = None
    asset_id: UUID
    assessment_id: UUID
    plugin_id: str
    cvss_score: Optional[float] = None
    status: str = "open"
    fingerprint: str
    created_at: datetime
    updated_at: datetime
    asset: Optional[AssetRead] = None


class FindingUpdate(BaseModel):
    status: Optional[str] = None
    remediation: Optional[str] = None
    severity: Optional[str] = None
