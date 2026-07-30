from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID
from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


class AssessmentBase(BaseModel):
    asset_id: UUID
    type: str
    config: dict = {}
    status: str = "pending"


class AssessmentCreate(AssessmentBase):
    pass


class AssessmentRead(AssessmentBase, BaseSchema):
    id: UUID
    organization_id: Optional[str] = None
    project_id: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    findings_count: int = 0
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    asset_name: Optional[str] = None


class AssessmentSummary(BaseSchema):
    """Lightweight assessment summary."""

    id: UUID
    asset_id: UUID
    type: str
    status: str
    findings_count: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None