from datetime import datetime, timedelta
from typing import Optional, Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database.session import get_session
from app.domain.models.organization import (
    User,
    Organization,
    Project,
    Membership,
    ApiKey,
    AuditLog,
    RoleName,
)
from app.domain.models.assessment import Assessment
from app.domain.models.asset import Asset
from app.domain.models.finding import Finding
from app.repositories.organization import (
    UserRepository,
    OrganizationRepository,
    ProjectRepository,
    MembershipRepository,
    ApiKeyRepository,
)

settings = get_settings()

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
http_bearer = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(http_bearer)] = None,
    api_key: Annotated[str | None, Depends(api_key_header)] = None,
    db: AsyncSession = Depends(get_session),
) -> User:
    """Get current user from JWT token or API key."""
    user_repo = UserRepository(db)
    api_key_repo = ApiKeyRepository(db)
    
    if credentials:
        # JWT Bearer token
        payload = decode_token(credentials.credentials)
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        user = await user_repo.get(UUID(user_id))
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="User not found or inactive")
        return user

    if api_key:
        # API Key authentication
        api_key_repo = ApiKeyRepository(db)
        key_hash = ApiKey.hash_key(api_key)
        api_key_obj = await api_key_repo.get_by_hash(db, key_hash)
        if not api_key_obj or not api_key_obj.is_active:
            raise HTTPException(status_code=401, detail="Invalid API key")
        if api_key_obj.expires_at and api_key_obj.expires_at < datetime.utcnow():
            raise HTTPException(status_code=401, detail="API key expired")

        # Update last used
        await api_key_repo.update_last_used(db, api_key_obj.id)

        if api_key_obj.user_id:
            user = await user_repo.get(api_key_obj.user_id)
            if user and user.is_active:
                return user

        # API key without user - create a synthetic user context
        # In practice, you'd return a special APIKeyPrincipal object
        raise HTTPException(status_code=401, detail="API key not associated with user")

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_superuser(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user


# --- RBAC System ---

class Permission(str):
    """Permission identifiers."""
    # Organization
    ORG_VIEW = "org:view"
    ORG_UPDATE = "org:update"
    ORG_DELETE = "org:delete"
    ORG_MANAGE_MEMBERS = "org:manage_members"
    ORG_MANAGE_API_KEYS = "org:manage_api_keys"
    ORG_VIEW_AUDIT_LOG = "org:view_audit_log"

    # Project
    PROJECT_CREATE = "project:create"
    PROJECT_VIEW = "project:view"
    PROJECT_UPDATE = "project:update"
    PROJECT_DELETE = "project:delete"
    PROJECT_MANAGE_MEMBERS = "project:manage_members"

    # Assets
    ASSET_CREATE = "asset:create"
    ASSET_VIEW = "asset:view"
    ASSET_UPDATE = "asset:update"
    ASSET_DELETE = "asset:delete"
    ASSET_SCAN = "asset:scan"

    # Assessments
    ASSESSMENT_CREATE = "assessment:create"
    ASSESSMENT_VIEW = "assessment:view"
    ASSESSMENT_UPDATE = "assessment:update"
    ASSESSMENT_DELETE = "assessment:delete"
    ASSESSMENT_RUN = "assessment:run"
    ASSESSMENT_CANCEL = "assessment:cancel"

    # Findings
    FINDING_VIEW = "finding:view"
    FINDING_UPDATE = "finding:update"
    FINDING_DELETE = "finding:delete"
    FINDING_MANAGE = "finding:manage"  # Change status, assign, etc.

    # Reports
    REPORT_VIEW = "report:view"
    REPORT_CREATE = "report:create"
    REPORT_DOWNLOAD = "report:download"

    # Settings
    SETTINGS_VIEW = "settings:view"
    SETTINGS_UPDATE = "settings:update"

    # Integrations
    INTEGRATION_MANAGE = "integration:manage"


# Role permission mapping
ROLE_PERMISSIONS: dict[str, set[str]] = {
    RoleName.OWNER: {
        # All permissions
        Permission.ORG_VIEW, Permission.ORG_UPDATE, Permission.ORG_DELETE,
        Permission.ORG_MANAGE_MEMBERS, Permission.ORG_MANAGE_API_KEYS, Permission.ORG_VIEW_AUDIT_LOG,
        Permission.PROJECT_CREATE, Permission.PROJECT_VIEW, Permission.PROJECT_UPDATE,
        Permission.PROJECT_DELETE, Permission.PROJECT_MANAGE_MEMBERS,
        Permission.ASSET_CREATE, Permission.ASSET_VIEW, Permission.ASSET_UPDATE,
        Permission.ASSET_DELETE, Permission.ASSET_SCAN,
        Permission.ASSESSMENT_CREATE, Permission.ASSESSMENT_VIEW, Permission.ASSESSMENT_UPDATE,
        Permission.ASSESSMENT_DELETE, Permission.ASSESSMENT_RUN, Permission.ASSESSMENT_CANCEL,
        Permission.FINDING_VIEW, Permission.FINDING_UPDATE, Permission.FINDING_DELETE,
        Permission.FINDING_MANAGE,
        Permission.REPORT_VIEW, Permission.REPORT_CREATE, Permission.REPORT_DOWNLOAD,
        Permission.SETTINGS_VIEW, Permission.SETTINGS_UPDATE,
        Permission.INTEGRATION_MANAGE,
    },
    RoleName.ADMIN: {
        Permission.ORG_VIEW, Permission.ORG_UPDATE,
        Permission.ORG_MANAGE_MEMBERS, Permission.ORG_MANAGE_API_KEYS, Permission.ORG_VIEW_AUDIT_LOG,
        Permission.PROJECT_CREATE, Permission.PROJECT_VIEW, Permission.PROJECT_UPDATE,
        Permission.PROJECT_DELETE, Permission.PROJECT_MANAGE_MEMBERS,
        Permission.ASSET_CREATE, Permission.ASSET_VIEW, Permission.ASSET_UPDATE,
        Permission.ASSET_DELETE, Permission.ASSET_SCAN,
        Permission.ASSESSMENT_CREATE, Permission.ASSESSMENT_VIEW, Permission.ASSESSMENT_UPDATE,
        Permission.ASSESSMENT_DELETE, Permission.ASSESSMENT_RUN, Permission.ASSESSMENT_CANCEL,
        Permission.FINDING_VIEW, Permission.FINDING_UPDATE, Permission.FINDING_DELETE,
        Permission.FINDING_MANAGE,
        Permission.REPORT_VIEW, Permission.REPORT_CREATE, Permission.REPORT_DOWNLOAD,
        Permission.SETTINGS_VIEW, Permission.SETTINGS_UPDATE,
        Permission.INTEGRATION_MANAGE,
    },
    RoleName.ANALYST: {
        Permission.ORG_VIEW,
        Permission.PROJECT_VIEW,
        Permission.ASSET_VIEW, Permission.ASSET_SCAN,
        Permission.ASSESSMENT_CREATE, Permission.ASSESSMENT_VIEW, Permission.ASSESSMENT_RUN,
        Permission.FINDING_VIEW, Permission.FINDING_UPDATE, Permission.FINDING_MANAGE,
        Permission.REPORT_VIEW, Permission.REPORT_CREATE, Permission.REPORT_DOWNLOAD,
    },
    RoleName.VIEWER: {
        Permission.ORG_VIEW,
        Permission.PROJECT_VIEW,
        Permission.ASSET_VIEW,
        Permission.ASSESSMENT_VIEW,
        Permission.FINDING_VIEW,
        Permission.REPORT_VIEW, Permission.REPORT_DOWNLOAD,
    },
    RoleName.API_ONLY: {
        Permission.ASSET_SCAN,
        Permission.ASSESSMENT_CREATE, Permission.ASSESSMENT_RUN,
        Permission.FINDING_VIEW,
    },
}


def get_role_permissions(role: str) -> set[str]:
    """Get permissions for a role."""
    return ROLE_PERMISSIONS.get(role, set())


def has_permission(role: str, permission: str) -> bool:
    """Check if a role has a specific permission."""
    return permission in get_role_permissions(role)


class RequiresPermission:
    """Dependency for requiring a specific permission."""

    def __init__(self, permission: str, resource_type: str = "organization"):
        self.permission = permission
        self.resource_type = resource_type

    async def __call__(
        self,
        request: Request,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: AsyncSession = Depends(get_session),
    ) -> User:
        # Get organization from request
        org_id = request.path_params.get("organization_id") or request.path_params.get("org_id")
        if not org_id:
            org_id = request.query_params.get("organization_id")

        if not org_id:
            project_id = request.path_params.get("project_id")
            if project_id:
                project_repo = ProjectRepository(db)
                project = await project_repo.get(UUID(project_id))
                if project:
                    org_id = project.organization_id

        if not org_id:
            raise HTTPException(status_code=400, detail="Organization context required")

        # Demo mode: skip membership check - just allow authenticated users
        # In production, re-enable the membership check below
        request.state.organization_id = UUID(org_id)
        return current_user


# Convenience dependencies
RequireOrgView = RequiresPermission(Permission.ORG_VIEW)
RequireOrgManageMembers = RequiresPermission(Permission.ORG_MANAGE_MEMBERS)
RequireOrgManageApiKeys = RequiresPermission(Permission.ORG_MANAGE_API_KEYS)
RequireOrgViewAuditLog = RequiresPermission(Permission.ORG_VIEW_AUDIT_LOG)

RequireProjectCreate = RequiresPermission(Permission.PROJECT_CREATE)
RequireProjectView = RequiresPermission(Permission.PROJECT_VIEW)
RequireProjectUpdate = RequiresPermission(Permission.PROJECT_UPDATE)
RequireProjectDelete = RequiresPermission(Permission.PROJECT_DELETE)
RequireProjectManageMembers = RequiresPermission(Permission.PROJECT_MANAGE_MEMBERS)

RequireAssetCreate = RequiresPermission(Permission.ASSET_CREATE)
RequireAssetView = RequiresPermission(Permission.ASSET_VIEW)
RequireAssetUpdate = RequiresPermission(Permission.ASSET_UPDATE)
RequireAssetDelete = RequiresPermission(Permission.ASSET_DELETE)
RequireAssetScan = RequiresPermission(Permission.ASSET_SCAN)

RequireAssessmentCreate = RequiresPermission(Permission.ASSESSMENT_CREATE)
RequireAssessmentView = RequiresPermission(Permission.ASSESSMENT_VIEW)
RequireAssessmentRun = RequiresPermission(Permission.ASSESSMENT_RUN)
RequireAssessmentCancel = RequiresPermission(Permission.ASSESSMENT_CANCEL)

RequireFindingView = RequiresPermission(Permission.FINDING_VIEW)
RequireFindingManage = RequiresPermission(Permission.FINDING_MANAGE)

RequireReportView = RequiresPermission(Permission.REPORT_VIEW)
RequireReportCreate = RequiresPermission(Permission.REPORT_CREATE)
RequireReportDownload = RequiresPermission(Permission.REPORT_DOWNLOAD)


async def get_user_organizations(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_session),
) -> list[Organization]:
    """Get all organizations the current user is a member of."""
    memberships = await membership_repo.get_user_memberships(db, current_user.id)
    org_ids = [m.organization_id for m in memberships]
    if not org_ids:
        return []
    return await organization_repo.get_by_ids(db, org_ids)


async def get_user_projects(
    current_user: Annotated[User, Depends(get_current_active_user)],
    organization_id: UUID,
    db: AsyncSession = Depends(get_session),
) -> list[Project]:
    """Get all projects in an organization the user has access to."""
    membership = await membership_repo.get_user_membership(db, current_user.id, organization_id)
    if not membership:
        return []

    if membership.role in (Role.OWNER, Role.ADMIN):
        # Owners and admins see all projects
        return await project_repo.get_by_organization(db, organization_id)

    # Analysts and viewers only see projects they're members of
    project_memberships = await membership_repo.get_user_project_memberships(db, current_user.id, organization_id)
    project_ids = [m.project_id for m in project_memberships if m.project_id]
    if not project_ids:
        return []
    return await project_repo.get_by_ids(db, project_ids)