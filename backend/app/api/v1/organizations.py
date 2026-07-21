from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.core.auth import (
    get_current_active_user,
    RequiresPermission,
    Permission,
    RoleName,
)
from app.domain.models.organization import User, Organization, Project, Membership
from app.domain.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationRead,
    OrganizationReadWithProjects,
    ProjectCreate,
    ProjectUpdate,
    ProjectRead,
    ProjectReadWithStats,
    MembershipCreate,
    MembershipUpdate,
    MembershipRead,
    MembershipReadWithUser,
    ApiKeyCreate,
    ApiKeyRead,
    ApiKeyCreateResponse,
)
from app.repositories import (
    get_organization_repo,
    get_project_repo,
    get_membership_repo,
    get_api_key_repo,
    get_user_repo,
)
from app.repositories.organization import (
    OrganizationRepository,
    ProjectRepository,
    MembershipRepository,
    ApiKeyRepository,
    UserRepository,
)

# --- Organizations Router ---
org_router = APIRouter(prefix="/organizations", tags=["Organizations"])


@org_router.post("", response_model=OrganizationRead, status_code=status.HTTP_201_CREATED)
async def create_organization(
    org_data: OrganizationCreate,
    current_user: User = Depends(get_current_active_user),
    org_repo: OrganizationRepository = Depends(get_organization_repo),
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


@org_router.get("", response_model=list[OrganizationRead])
async def list_organizations(
    current_user: User = Depends(get_current_active_user),
    org_repo: OrganizationRepository = Depends(get_organization_repo),
    membership_repo: MembershipRepository = Depends(get_membership_repo),
):
    """List organizations the current user is a member of."""
    memberships = await membership_repo.get_user_memberships(current_user.id)
    org_ids = [m.organization_id for m in memberships]
    return await org_repo.get_by_ids(org_ids)


@org_router.get("/{organization_id}", response_model=OrganizationReadWithProjects)
async def get_organization(
    organization_id: UUID,
    current_user: User = Depends(RequiresPermission(Permission.ORG_VIEW)),
    org_repo: OrganizationRepository = Depends(get_organization_repo),
    project_repo: ProjectRepository = Depends(get_project_repo),
):
    """Get organization with projects."""
    org = await org_repo.get(organization_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    projects = await project_repo.get_by_organization(organization_id)
    org.projects = projects
    return org


@org_router.patch("/{organization_id}", response_model=OrganizationRead)
async def update_organization(
    organization_id: UUID,
    org_data: OrganizationUpdate,
    current_user: User = Depends(RequiresPermission(Permission.ORG_UPDATE)),
    org_repo: OrganizationRepository = Depends(get_organization_repo),
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
    org_repo: OrganizationRepository = Depends(get_organization_repo),
    membership_repo: MembershipRepository = Depends(get_membership_repo),
):
    """Delete organization (owner only)."""
    org = await org_repo.get(organization_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    # Verify owner
    membership = await membership_repo.get_user_membership(current_user.id, organization_id)
    if not membership or membership.role != RoleName.OWNER:
        raise HTTPException(status_code=403, detail="Only organization owners can delete")

    await org_repo.delete(organization_id)


# --- Projects Router ---
project_router = APIRouter(prefix="/projects", tags=["Projects"])


@project_router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    organization_id: UUID = Query(...),
    project_data: ProjectCreate = None,
    current_user: User = Depends(RequiresPermission(Permission.PROJECT_CREATE)),
    project_repo: ProjectRepository = Depends(get_project_repo),
):
    """Create a new project in an organization."""
    if not project_data:
        raise HTTPException(status_code=400, detail="project_data is required")
    existing = await project_repo.get_by_slug(organization_id, project_data.slug)
    if existing:
        raise HTTPException(status_code=400, detail="Project slug already taken in this organization")

    project = Project(
        organization_id=organization_id,
        name=project_data.name,
        slug=project_data.slug,
        description=project_data.description,
    )
    if hasattr(project_data, 'settings') and project_data.settings:
        project.settings = project_data.settings
    return await project_repo.create(project)


@project_router.get("", response_model=list[ProjectReadWithStats])
async def list_projects(
    organization_id: UUID = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    active_only: bool = Query(True),
    current_user: User = Depends(RequiresPermission(Permission.PROJECT_VIEW)),
    project_repo: ProjectRepository = Depends(get_project_repo),
):
    """List projects in an organization."""
    if not organization_id:
        return []
    projects = await project_repo.list(organization_id, skip, limit, active_only)
    return projects


@project_router.get("/{project_id}", response_model=ProjectReadWithStats)
async def get_project(
    project_id: UUID,
    current_user: User = Depends(RequiresPermission(Permission.PROJECT_VIEW)),
    project_repo: ProjectRepository = Depends(get_project_repo),
):
    """Get project details with stats."""
    project = await project_repo.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@project_router.patch("/{project_id}", response_model=ProjectRead)
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
    current_user: User = Depends(RequiresPermission(Permission.PROJECT_DELETE)),
    project_repo: ProjectRepository = Depends(get_project_repo),
):
    """Delete project."""
    project = await project_repo.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    await project_repo.delete(project_id)


# --- Memberships Router ---
membership_router = APIRouter(prefix="/memberships", tags=["Memberships"])


@membership_router.post("", response_model=MembershipReadWithUser, status_code=status.HTTP_201_CREATED)
async def invite_member(
    organization_id: UUID,
    membership_data: MembershipCreate,
    current_user: User = Depends(RequiresPermission(Permission.ORG_MANAGE_MEMBERS)),
    membership_repo: MembershipRepository = Depends(get_membership_repo),
    user_repo: UserRepository = Depends(get_user_repo),
):
    """Invite a user to an organization or project."""
    # Find user by email
    user = await user_repo.get_by_email(membership_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if already a member
    existing = await membership_repo.get_user_membership(user.id, organization_id)
    if existing:
        raise HTTPException(status_code=400, detail="User is already a member of this organization")

    # Check project membership if provided
    if membership_data.project_id:
        existing_project = await membership_repo.get_user_membership(user.id, organization_id, membership_data.project_id)
        if existing_project:
            raise HTTPException(status_code=400, detail="User is already a member of this project")

    membership = Membership(
        user_id=user.id,
        organization_id=organization_id,
        project_id=membership_data.project_id,
        role=membership_data.role,
    )
    membership = await membership_repo.create(membership)

    return MembershipReadWithUser.model_validate(membership, from_attributes=True)


@membership_router.get("", response_model=list[MembershipReadWithUser])
async def list_members(
    organization_id: UUID,
    project_id: Optional[UUID] = Query(None),
    current_user: User = Depends(RequiresPermission(Permission.ORG_VIEW)),
    membership_repo: MembershipRepository = Depends(get_membership_repo),
):
    """List members of an organization or project."""
    if project_id:
        memberships = await membership_repo.get_project_memberships(project_id)
    else:
        memberships = await membership_repo.get_organization_memberships(organization_id)
    return memberships


@membership_router.patch("/{membership_id}", response_model=MembershipRead)
async def update_membership(
    membership_id: UUID,
    membership_data: MembershipUpdate,
    current_user: User = Depends(RequiresPermission(Permission.ORG_MANAGE_MEMBERS)),
    membership_repo: MembershipRepository = Depends(get_membership_repo),
):
    """Update member role."""
    # Get membership
    result = await membership_repo.db.execute(
        select(Membership).where(Membership.id == membership_id)
    )
    membership = result.scalar_one_or_none()
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")

    # Prevent demoting the last owner
    if membership_data.role and membership_data.role != RoleName.OWNER and membership.role == RoleName.OWNER:
        owners = await membership_repo.get_organization_memberships(membership.organization_id)
        owner_count = sum(1 for m in owners if m.role == RoleName.OWNER)
        if owner_count <= 1:
            raise HTTPException(status_code=400, detail="Cannot remove the last owner")

    if membership_data.role:
        membership.role = membership_data.role
    if membership_data.is_default is not None:
        membership.is_default = membership_data.is_default

    return await membership_repo.update(membership)


@membership_router.delete("/{membership_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    membership_id: UUID,
    current_user: User = Depends(RequiresPermission(Permission.ORG_MANAGE_MEMBERS)),
    membership_repo: MembershipRepository = Depends(get_membership_repo),
):
    """Remove a member from organization/project."""
    result = await membership_repo.db.execute(
        select(Membership).where(Membership.id == membership_id)
    )
    membership = result.scalar_one_or_none()
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")

    # Prevent removing the last owner
    if membership.role == RoleName.OWNER:
        owners = await membership_repo.get_organization_memberships(membership.organization_id)
        owner_count = sum(1 for m in owners if m.role == RoleName.OWNER)
        if owner_count <= 1:
            raise HTTPException(status_code=400, detail="Cannot remove the last owner")

    # Prevent self-removal if owner
    if membership.user_id == current_user.id and membership.role == RoleName.OWNER:
        raise HTTPException(status_code=400, detail="Owners cannot remove themselves")

    await membership_repo.db.delete(membership)
    await membership_repo.db.commit()


# --- API Keys Router ---
apikey_router = APIRouter(prefix="/api-keys", tags=["API Keys"])


@apikey_router.post("", response_model=ApiKeyCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    organization_id: UUID,
    api_key_data: ApiKeyCreate,
    current_user: User = Depends(RequiresPermission(Permission.ORG_MANAGE_API_KEYS)),
    api_key_repo: ApiKeyRepository = Depends(get_api_key_repo),
):
    """Create a new API key."""
    expires_at = None
    if api_key_data.expires_in_days:
        expires_at = datetime.utcnow() + timedelta(days=api_key_data.expires_in_days)

    api_key, plain_key = await api_key_repo.create(
        organization_id=organization_id,
        user_id=current_user.id,
        name=api_key_data.name,
        scopes=api_key_data.scopes,
        expires_at=expires_at,
    )

    response = ApiKeyCreateResponse.model_validate(api_key, from_attributes=True)
    response.key = plain_key  # Only returned once!
    return response


@apikey_router.get("", response_model=list[ApiKeyRead])
async def list_api_keys(
    organization_id: UUID,
    current_user: User = Depends(RequiresPermission(Permission.ORG_MANAGE_API_KEYS)),
    api_key_repo: ApiKeyRepository = Depends(get_api_key_repo),
):
    """List API keys for an organization."""
    return await api_key_repo.get_by_organization(organization_id)


@apikey_router.get("/{key_id}", response_model=ApiKeyRead)
async def get_api_key(
    key_id: UUID,
    current_user: User = Depends(RequiresPermission(Permission.ORG_MANAGE_API_KEYS)),
    api_key_repo: ApiKeyRepository = Depends(get_api_key_repo),
):
    """Get API key details (without the actual key)."""
    api_key = await api_key_repo.get(key_id)
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    return api_key


@apikey_router.patch("/{key_id}", response_model=ApiKeyRead)
async def update_api_key(
    key_id: UUID,
    is_active: bool,
    current_user: User = Depends(RequiresPermission(Permission.ORG_MANAGE_API_KEYS)),
    api_key_repo: ApiKeyRepository = Depends(get_api_key_repo),
):
    """Activate/deactivate an API key."""
    api_key = await api_key_repo.get(key_id)
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")

    api_key.is_active = is_active
    return await api_key_repo.update(api_key)


@apikey_router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_api_key(
    key_id: UUID,
    current_user: User = Depends(RequiresPermission(Permission.ORG_MANAGE_API_KEYS)),
    api_key_repo: ApiKeyRepository = Depends(get_api_key_repo),
):
    """Delete an API key."""
    deleted = await api_key_repo.delete(key_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="API key not found")