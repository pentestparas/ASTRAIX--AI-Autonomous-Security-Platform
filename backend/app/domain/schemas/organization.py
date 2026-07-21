from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.domain.schemas.asset import AssetRead
from app.domain.models.organization import RoleName


# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    preferences: Optional[dict] = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    is_active: bool
    is_superuser: bool
    last_login: Optional[datetime]
    avatar_url: Optional[str]
    preferences: dict
    created_at: datetime
    updated_at: datetime


class UserReadWithMemberships(UserRead):
    memberships: list["MembershipRead"] = []


# --- Organization Schemas ---
class OrganizationBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    slug: str = Field(min_length=1, max_length=100, pattern=r"^[a-z0-9-]+$")
    description: Optional[str] = None


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    logo_url: Optional[str] = None
    settings: Optional[dict] = None


class OrganizationRead(OrganizationBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    logo_url: Optional[str]
    settings: dict
    subscription_tier: str
    subscription_expires_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class OrganizationReadWithProjects(OrganizationRead):
    projects: list["ProjectRead"] = []


# --- Project Schemas ---
class ProjectBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    slug: str = Field(min_length=1, max_length=100, pattern=r"^[a-z0-9-]+$")
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    settings: Optional[dict] = None
    is_active: Optional[bool] = None


class ProjectRead(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    settings: dict
    is_active: bool
    created_at: datetime
    updated_at: datetime


class ProjectReadWithAssets(ProjectRead):
    assets: list["AssetRead"] = []


class ProjectReadWithStats(ProjectRead):
    assets_count: int = 0
    assessments_count: int = 0
    open_findings_count: int = 0
    critical_findings_count: int = 0


# --- Membership Schemas ---
class MembershipBase(BaseModel):
    role: str = Field(pattern=r"^(owner|admin|analyst|viewer)$")


class MembershipCreate(MembershipBase):
    user_id: UUID
    project_id: Optional[UUID] = None


class MembershipUpdate(BaseModel):
    role: Optional[str] = Field(default=None, pattern=r"^(owner|admin|analyst|viewer)$")


class MembershipRead(MembershipBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    organization_id: UUID
    project_id: Optional[UUID]
    is_default: bool
    created_at: datetime
    updated_at: datetime


class MembershipReadWithUser(MembershipRead):
    user: UserRead


# --- API Key Schemas ---
class ApiKeyBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    scopes: list[str] = Field(default_factory=list)
    expires_at: Optional[datetime] = None


class ApiKeyCreate(ApiKeyBase):
    pass


class ApiKeyRead(ApiKeyBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    key_prefix: str
    organization_id: UUID
    last_used_at: Optional[datetime]
    is_active: bool
    created_at: datetime
    updated_at: datetime


class ApiKeyCreateResponse(ApiKeyRead):
    """Response when creating an API key - includes the plain key only once."""
    plain_key: str


# --- Forward references ---
UserReadWithMemberships.model_rebuild()
OrganizationReadWithProjects.model_rebuild()
ProjectReadWithAssets.model_rebuild()
ProjectReadWithStats.model_rebuild()