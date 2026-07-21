from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.database.session import get_session
from app.core.auth import (
    create_access_token,
    get_current_active_user,
    get_current_user,
    get_password_hash,
    verify_password,
    Permission,
    RequiresPermission,
)
from app.config import settings
from app.domain.models.organization import User, Organization, Project, Membership, ApiKey, RoleName
from app.repositories.organization import (
    UserRepository,
    OrganizationRepository,
    ProjectRepository,
    MembershipRepository,
    ApiKeyRepository,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


# --- Request/Response Models ---

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    sub: str
    exp: int


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: Optional[str] = None
    organization_name: Optional[str] = None
    organization_slug: Optional[str] = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    full_name: Optional[str]
    is_active: bool
    is_superuser: bool
    last_login: Optional[datetime]
    created_at: datetime


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    slug: str = Field(min_length=2, max_length=100, pattern=r"^[a-z0-9-]+$")
    description: Optional[str] = None


class OrganizationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    slug: str
    description: Optional[str]
    logo_url: Optional[str]
    settings: dict
    subscription_tier: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    logo_url: Optional[str] = None
    settings: Optional[dict] = None


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    slug: str = Field(min_length=2, max_length=100, pattern=r"^[a-z0-9-]+$")
    description: Optional[str] = None
    settings: Optional[dict] = None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    name: str
    slug: str
    description: Optional[str]
    settings: dict
    is_active: bool
    created_at: datetime
    updated_at: datetime


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    settings: Optional[dict] = None
    is_active: Optional[bool] = None


class MembershipCreate(BaseModel):
    email: EmailStr
    role: RoleName = RoleName.VIEWER
    project_id: Optional[UUID] = None


class MembershipResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    organization_id: UUID
    project_id: Optional[UUID]
    role: RoleName
    is_default: bool
    created_at: datetime
    user: UserResponse


class MembershipUpdate(BaseModel):
    role: Optional[RoleName] = None
    is_default: Optional[bool] = None


class ApiKeyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    scopes: list[str] = Field(default_factory=list)
    expires_in_days: Optional[int] = Field(default=None, ge=1, le=3650)


class ApiKeyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    key_prefix: str
    scopes: list[str]
    expires_at: Optional[datetime]
    last_used_at: Optional[datetime]
    is_active: bool
    created_at: datetime


class ApiKeyCreateResponse(BaseModel):
    api_key: ApiKeyResponse
    key: str  # Only returned once!


# --- Dependencies ---

def get_user_repo(db: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(db)


def get_org_repo(db: AsyncSession = Depends(get_session)) -> OrganizationRepository:
    return OrganizationRepository(db)


def get_project_repo(db: AsyncSession = Depends(get_session)) -> ProjectRepository:
    return ProjectRepository(db)


def get_membership_repo(db: AsyncSession = Depends(get_session)) -> MembershipRepository:
    return MembershipRepository(db)


def get_api_key_repo(db: AsyncSession = Depends(get_session)) -> ApiKeyRepository:
    return ApiKeyRepository(db)


# --- Auth Endpoints ---

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repo: UserRepository = Depends(get_user_repo),
):
    """OAuth2 compatible login for Swagger UI."""
    user = await user_repo.get_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    await user_repo.update_last_login(user.id)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )
    return Token(
        access_token=access_token,
        expires_in=int(access_token_expires.total_seconds()),
    )


@router.post("/login/json", response_model=Token)
async def login_json(
    login_data: UserLogin,
    user_repo: UserRepository = Depends(get_user_repo),
):
    """JSON-based login for frontend applications."""
    user = await user_repo.get_by_email(login_data.email)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    await user_repo.update_last_login(user.id)

    expires_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES if not login_data.remember_me else settings.ACCESS_TOKEN_EXPIRE_MINUTES * 24 * 7
    access_token_expires = timedelta(minutes=expires_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )
    return Token(
        access_token=access_token,
        expires_in=int(access_token_expires.total_seconds()),
    )


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    user_repo: UserRepository = Depends(get_user_repo),
    org_repo: OrganizationRepository = Depends(get_org_repo),
    membership_repo: MembershipRepository = Depends(get_membership_repo),
):
    """Register a new user and optionally create an organization."""
    existing = await user_repo.get_by_email(user_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
    )
    user = await user_repo.create(user)

    # Create organization if provided
    if user_data.organization_name:
        slug = user_data.organization_slug or user_data.organization_name.lower().replace(" ", "-")
        # Check slug uniqueness
        existing_org = await org_repo.get_by_slug(slug)
        if existing_org:
            slug = f"{slug}-{user.id.hex[:8]}"

        org = Organization(
            name=user_data.organization_name,
            slug=slug,
        )
        org = await org_repo.create(org)

        # Create owner membership
        membership = Membership(
            user_id=user.id,
            organization_id=org.id,
            role=RoleName.OWNER,
            is_default=True,
        )
        await membership_repo.create(membership)
        
        # Commit all changes
        await membership_repo.db.commit()

    return user


@router.post("/refresh", response_model=Token)
async def refresh_token(
    current_user: User = Depends(get_current_active_user),
):
    """Refresh access token."""
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(current_user.id)},
        expires_delta=access_token_expires,
    )
    return Token(
        access_token=access_token,
        expires_in=int(access_token_expires.total_seconds()),
    )


@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_current_active_user)):
    """Get current user profile."""
    return current_user


# --- Organization Endpoints ---

org_router = APIRouter(prefix="/organizations", tags=["Organizations"])


@org_router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    org_data: OrganizationCreate,
    current_user: User = Depends(get_current_active_user),
    org_repo: OrganizationRepository = Depends(get_org_repo),
    membership_repo: MembershipRepository = Depends(get_membership_repo),
):
    """Create a new organization."""
    existing = await org_repo.get_by_slug(org_data.slug)
    if existing:
        raise HTTPException(status_code=400, detail="Organization slug already taken")

    org = Organization(
        name=org_data.name,
        slug=org_data.slug,
        description=org_data.description,
    )
    org = await org_repo.create(org)

    # Create owner membership
    membership = Membership(
        user_id=current_user.id,
        organization_id=org.id,
        role=RoleName.OWNER,
        is_default=True,
    )
    await membership_repo.create(membership)

    return org


@org_router.get("", response_model=list[OrganizationResponse])
async def list_organizations(
    current_user: User = Depends(get_current_active_user),
    org_repo: OrganizationRepository = Depends(get_org_repo),
    membership_repo: MembershipRepository = Depends(get_membership_repo),
):
    """List organizations the current user is a member of."""
    memberships = await membership_repo.get_user_memberships(current_user.id)
    org_ids = [m.organization_id for m in memberships]
    return await org_repo.get_by_ids(org_ids)


@org_router.get("/{organization_id}", response_model=OrganizationResponse)
async def get_organization(
    organization_id: UUID,
    current_user: User = Depends(RequiresPermission(Permission.ORG_VIEW)),
    org_repo: OrganizationRepository = Depends(get_org_repo),
):
    """Get organization details."""
    org = await org_repo.get(organization_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@org_router.patch("/{organization_id}", response_model=OrganizationResponse)
async def update_organization(
    organization_id: UUID,
    org_data: OrganizationUpdate,
    current_user: User = Depends(RequiresPermission(Permission.ORG_UPDATE)),
    org_repo: OrganizationRepository = Depends(get_org_repo),
):
    """Update organization."""
    org = await org_repo.get(organization_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    for field, value in org_data.model_dump(exclude_unset=True).items():
        setattr(org, field, value)

    return await org_repo.update(org)


@org_router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    organization_id: UUID,
    current_user: User = Depends(RequiresPermission(Permission.ORG_DELETE)),
    org_repo: OrganizationRepository = Depends(get_org_repo),
):
    """Delete organization (owner only)."""
    org = await org_repo.get(organization_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    # Check if user is owner
    membership_repo = MembershipRepository(org_repo.db)
    membership = await membership_repo.get_user_membership(current_user.id, organization_id)
    if not membership or membership.role != RoleName.OWNER:
        raise HTTPException(status_code=403, detail="Only organization owners can delete")

    await org_repo.delete(organization_id)


# --- Project Endpoints ---

project_router = APIRouter(prefix="/projects", tags=["Projects"])


@project_router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    organization_id: UUID,
    current_user: User = Depends(RequiresPermission(Permission.PROJECT_CREATE)),
    project_repo: ProjectRepository = Depends(get_project_repo),
):
    """Create a new project in an organization."""
    existing = await project_repo.get_by_slug(organization_id, project_data.slug)
    if existing:
        raise HTTPException(status_code=400, detail="Project slug already taken in this organization")

    project = Project(
        organization_id=organization_id,
        name=project_data.name,
        slug=project_data.slug,
        description=project_data.description,
        settings=project_data.settings or {},
    )
    return await project_repo.create(project)


@project_router.get("", response_model=list[ProjectResponse])
async def list_projects(
    organization_id: UUID,
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    current_user: User = Depends(RequiresPermission(Permission.PROJECT_VIEW)),
    project_repo: ProjectRepository = Depends(get_project_repo),
):
    """List projects in an organization."""
    return await project_repo.list(organization_id, skip, limit, active_only)


@project_router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: UUID,
    current_user: User = Depends(RequiresPermission(Permission.PROJECT_VIEW)),
    project_repo: ProjectRepository = Depends(get_project_repo),
):
    """Get project details."""
    project = await project_repo.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@project_router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: UUID,
    project_data: ProjectUpdate,
    current_user: User = Depends(RequiresPermission(Permission.PROJECT_UPDATE)),
    project_repo: ProjectRepository = Depends(get_project_repo),
):
    """Update project."""
    project = await project_repo.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    for field, value in project_data.model_dump(exclude_unset=True).items():
        setattr(project, field, value)

    return await project_repo.update(project)


@project_router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: UUID,
    organization_id: UUID = None,
    current_user: User = Depends(RequiresPermission(Permission.PROJECT_DELETE)),
    project_repo: ProjectRepository = Depends(get_project_repo),
):
    """Delete project."""
    await project_repo.delete(project_id)


# --- Membership Endpoints ---

membership_router = APIRouter(prefix="/memberships", tags=["Memberships"])


@membership_router.get("", response_model=list[MembershipResponse])
async def list_memberships(
    organization_id: UUID,
    project_id: Optional[UUID] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(RequiresPermission(Permission.ORG_VIEW)),
    membership_repo: MembershipRepository = Depends(get_membership_repo),
):
    """List organization or project memberships."""
    if project_id:
        return await membership_repo.get_project_memberships(project_id)
    return await membership_repo.get_organization_memberships(organization_id, skip, limit)


@membership_router.post("", response_model=MembershipResponse, status_code=status.HTTP_201_CREATED)
async def invite_member(
    membership_data: MembershipCreate,
    organization_id: UUID,
    current_user: User = Depends(RequiresPermission(Permission.ORG_MANAGE_MEMBERS)),
    user_repo: UserRepository = Depends(get_user_repo),
    membership_repo: MembershipRepository = Depends(get_membership_repo),
):
    """Invite a user to organization or project."""
    user = await user_repo.get_by_email(membership_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if already a member
    existing = await membership_repo.get_user_membership(user.id, organization_id)
    if existing and not membership_data.project_id:
        raise HTTPException(status_code=400, detail="User is already a member of this organization")

    if membership_data.project_id:
        existing = await membership_repo.get_user_membership(user.id, organization_id, membership_data.project_id)
        if existing:
            raise HTTPException(status_code=400, detail="User is already a member of this project")

    membership = Membership(
        user_id=user.id,
        organization_id=organization_id,
        project_id=membership_data.project_id,
        role=membership_data.role,
    )
    return await membership_repo.create(membership)


@membership_router.patch("/{membership_id}", response_model=MembershipResponse)
async def update_membership(
    membership_id: UUID,
    membership_data: MembershipUpdate,
    current_user: User = Depends(RequiresPermission(Permission.ORG_MANAGE_MEMBERS)),
    membership_repo: MembershipRepository = Depends(get_membership_repo),
):
    """Update membership role."""
    membership = await membership_repo.get(membership_id)
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")

    # Prevent demoting the last owner
    if membership_data.role and membership_data.role != RoleName.OWNER:
        if membership.role == RoleName.OWNER:
            # Check if there are other owners
            org_memberships = await membership_repo.get_organization_memberships(membership.organization_id)
            owner_count = sum(1 for m in org_memberships if m.role == RoleName.OWNER)
            if owner_count <= 1:
                raise HTTPException(status_code=400, detail="Cannot demote the last owner")

    for field, value in membership_data.model_dump(exclude_unset=True).items():
        setattr(membership, field, value)

    return await membership_repo.update(membership)


@membership_router.delete("/{membership_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    membership_id: UUID,
    current_user: User = Depends(RequiresPermission(Permission.ORG_MANAGE_MEMBERS)),
    membership_repo: MembershipRepository = Depends(get_membership_repo),
):
    """Remove a member from organization or project."""
    membership = await membership_repo.get(membership_id)
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")

    # Prevent removing the last owner
    if membership.role == RoleName.OWNER:
        org_memberships = await membership_repo.get_organization_memberships(membership.organization_id)
        owner_count = sum(1 for m in org_memberships if m.role == RoleName.OWNER)
        if owner_count <= 1:
            raise HTTPException(status_code=400, detail="Cannot remove the last owner")

    await membership_repo.delete(membership.user_id, membership.organization_id, membership.project_id)


# --- API Key Endpoints ---

apikey_router = APIRouter(prefix="/api-keys", tags=["API Keys"])


@apikey_router.post("", response_model=ApiKeyCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    key_data: ApiKeyCreate,
    organization_id: UUID,
    current_user: User = Depends(RequiresPermission(Permission.ORG_MANAGE_API_KEYS)),
    api_key_repo: ApiKeyRepository = Depends(get_api_key_repo),
):
    """Create a new API key."""
    expires_at = None
    if key_data.expires_in_days:
        expires_at = datetime.utcnow() + timedelta(days=key_data.expires_in_days)

    api_key, full_key = await api_key_repo.create(
        organization_id=organization_id,
        user_id=current_user.id,
        name=key_data.name,
        scopes=key_data.scopes,
        expires_at=expires_at,
    )

    return ApiKeyCreateResponse(
        api_key=ApiKeyResponse.model_validate(api_key),
        key=full_key,  # Only returned once!
    )


@apikey_router.get("", response_model=list[ApiKeyResponse])
async def list_api_keys(
    organization_id: UUID,
    current_user: User = Depends(RequiresPermission(Permission.ORG_MANAGE_API_KEYS)),
    api_key_repo: ApiKeyRepository = Depends(get_api_key_repo),
):
    """List API keys for organization."""
    return await api_key_repo.get_by_organization(organization_id)


@apikey_router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_api_key(
    key_id: UUID,
    current_user: User = Depends(RequiresPermission(Permission.ORG_MANAGE_API_KEYS)),
    api_key_repo: ApiKeyRepository = Depends(get_api_key_repo),
):
    """Revoke an API key."""
    await api_key_repo.delete(key_id)


@apikey_router.patch("/{key_id}/toggle", response_model=ApiKeyResponse)
async def toggle_api_key(
    key_id: UUID,
    current_user: User = Depends(RequiresPermission(Permission.ORG_MANAGE_API_KEYS)),
    api_key_repo: ApiKeyRepository = Depends(get_api_key_repo),
):
    """Enable/disable an API key."""
    api_key = await api_key_repo.get(key_id)
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")

    api_key.is_active = not api_key.is_active
    return await api_key_repo.update(api_key)