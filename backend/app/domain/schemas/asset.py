from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.base import BaseSchema


class AssetBase(BaseModel):
    name: str
    type: str
    identifier: str
    criticality: str = "medium"
    tags: List[str] = []
    metadata: dict = {}


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    identifier: Optional[str] = None
    criticality: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[dict] = None
    last_scanned: Optional[datetime] = None


class AssetRead(AssetBase, BaseSchema):
    id: UUID
    last_scanned: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime