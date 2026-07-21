from typing import Optional
from uuid import UUID
from datetime import datetime, timedelta
from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.domain.models.organization import (
    User,
    Organization,
    Project,
    Membership,
    ApiKey,
    RoleName,
    AuditLog,
)


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def get(self, user_id: UUID) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == str(user_id)))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_ids(self, user_ids: list[UUID]) -> list[User]:
        if not user_ids:
            return []
        result = await self.db.execute(select(User).where(User.id.in_(user_ids)))
        return list(result.scalars().all())

    async def list(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> list[User]:
        query = select(User)
        if active_only:
            query = query.where(User.is_active == True)
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update(self, user: User) -> User:
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def update_last_login(self, user_id: UUID) -> bool:
        user = await self.get(user_id)
        if user:
            user.last_login_at = datetime.utcnow()
            await self.db.flush()
            return True
        return False


class OrganizationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, org: Organization) -> Organization:
        self.db.add(org)
        await self.db.flush()
        await self.db.refresh(org)
        return org

    async def get(self, org_id: UUID) -> Optional[Organization]:
        result = await self.db.execute(select(Organization).where(Organization.id == str(org_id)))
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Optional[Organization]:
        result = await self.db.execute(select(Organization).where(Organization.slug == slug))
        return result.scalar_one_or_none()

    async def get_by_ids(self, org_ids: list[UUID]) -> list[Organization]:
        if not org_ids:
            return []
        result = await self.db.execute(select(Organization).where(Organization.id.in_(org_ids)))
        return list(result.scalars().all())

    async def list(self, skip: int = 0, limit: int = 100) -> list[Organization]:
        result = await self.db.execute(
            select(Organization).where(Organization.is_active == True).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def update(self, org: Organization) -> Organization:
        await self.db.flush()
        await self.db.refresh(org)
        return org

    async def delete(self, org_id: UUID) -> bool:
        org = await self.get(org_id)
        if org:
            await self.db.delete(org)
            return True
        return False


class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, project: Project) -> Project:
        # Convert UUIDs to strings for SQLite compatibility
        project.organization_id = str(project.organization_id) if project.organization_id else None
        if project.id:
            project.id = str(project.id)
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def get(self, project_id: UUID) -> Optional[Project]:
        result = await self.db.execute(select(Project).where(Project.id == str(project_id)))
        return result.scalar_one_or_none()

    async def get_by_slug(self, organization_id: UUID, slug: str) -> Optional[Project]:
        result = await self.db.execute(
            select(Project).where(Project.organization_id == str(organization_id), Project.slug == slug)
        )
        return result.scalar_one_or_none()

    async def get_by_organization(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Project]:
        result = await self.db.execute(
            select(Project)
            .where(Project.organization_id == str(organization_id), Project.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_ids(self, project_ids: list[UUID]) -> list[Project]:
        if not project_ids:
            return []
        result = await self.db.execute(select(Project).where(Project.id.in_(project_ids)))
        return list(result.scalars().all())

    async def list(
        self, organization_id: UUID, skip: int = 0, limit: int = 100, active_only: bool = True
    ) -> list[Project]:
        query = select(Project).where(Project.organization_id == str(organization_id))
        if active_only:
            query = query.where(Project.is_active == True)
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count(self, organization_id: UUID, active_only: bool = True) -> int:
        query = select(func.count(Project.id)).where(Project.organization_id == str(organization_id))
        if active_only:
            query = query.where(Project.is_active == True)
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def update(self, project: Project) -> Project:
        await self.db.flush()
        await self.db.refresh(project)
        return project

    async def delete(self, project_id: UUID) -> bool:
        project = await self.get(project_id)
        if project:
            await self.db.delete(project)
            return True
        return False


class MembershipRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, membership: Membership) -> Membership:
        self.db.add(membership)
        await self.db.commit()
        await self.db.refresh(membership)
        return membership

    async def get(self, membership_id: UUID) -> Optional[Membership]:
        result = await self.db.execute(select(Membership).where(Membership.id == str(membership_id)))
        return result.scalar_one_or_none()

    async def get_user_membership(
        self, user_id: UUID, organization_id: UUID, project_id: UUID | None = None
    ) -> Optional[Membership]:
        query = select(Membership).where(
            Membership.user_id == user_id, Membership.organization_id == organization_id
        )
        if project_id:
            query = query.where(Membership.project_id == project_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_organization_memberships(
        self, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Membership]:
        result = await self.db.execute(
            select(Membership)
            .where(Membership.organization_id == organization_id, Membership.project_id.is_(None))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_project_memberships(self, project_id: UUID) -> list[Membership]:
        result = await self.db.execute(
            select(Membership).where(Membership.project_id == project_id)
        )
        return list(result.scalars().all())

    async def get_user_memberships(self, user_id: UUID) -> list[Membership]:
        result = await self.db.execute(
            select(Membership).where(Membership.user_id == user_id)
        )
        return list(result.scalars().all())

    async def get_user_project_memberships(
        self, user_id: UUID, organization_id: UUID
    ) -> list[Membership]:
        result = await self.db.execute(
            select(Membership).where(
                Membership.user_id == user_id,
                Membership.organization_id == organization_id,
                Membership.project_id.is_not(None),
            )
        )
        return list(result.scalars().all())

    async def update(self, membership: Membership) -> Membership:
        await self.db.flush()
        await self.db.refresh(membership)
        return membership

    async def delete(self, user_id: UUID, organization_id: UUID, project_id: UUID | None = None) -> bool:
        query = select(Membership).where(
            Membership.user_id == user_id, Membership.organization_id == organization_id
        )
        if project_id:
            query = query.where(Membership.project_id == project_id)
        else:
            query = query.where(Membership.project_id.is_(None))
        result = await self.db.execute(query)
        membership = result.scalar_one_or_none()
        if membership:
            await self.db.delete(membership)
            return True
        return False


class ApiKeyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def hash_key(key: str) -> str:
        import hashlib
        return hashlib.sha256(key.encode()).hexdigest()

    @staticmethod
    def generate_key() -> tuple[str, str]:
        import secrets
        prefix = "astraix_"
        random_part = secrets.token_urlsafe(32)
        full_key = f"{prefix}{random_part}"
        key_hash = ApiKeyRepository.hash_key(full_key)
        key_prefix = full_key[:20]
        return full_key, key_hash, key_prefix

    async def create(
        self,
        organization_id: UUID,
        user_id: UUID | None,
        name: str,
        scopes: list[str],
        expires_at: datetime | None = None,
    ) -> tuple[ApiKey, str]:
        full_key, key_hash, key_prefix = self.generate_key()

        api_key = ApiKey(
            organization_id=organization_id,
            user_id=user_id,
            name=name,
            key_hash=key_hash,
            key_prefix=key_prefix,
            scopes=scopes,
            expires_at=expires_at,
        )
        self.db.add(api_key)
        await self.db.flush()
        await self.db.refresh(api_key)
        return api_key, full_key

    async def get(self, key_id: UUID) -> Optional[ApiKey]:
        result = await self.db.execute(select(ApiKey).where(ApiKey.id == str(key_id)))
        return result.scalar_one_or_none()

    async def get_by_hash(self, key_hash: str) -> Optional[ApiKey]:
        result = await self.db.execute(select(ApiKey).where(ApiKey.key_hash == key_hash))
        return result.scalar_one_or_none()

    async def get_by_organization(self, organization_id: UUID) -> list[ApiKey]:
        result = await self.db.execute(
            select(ApiKey).where(ApiKey.organization_id == organization_id)
        )
        return list(result.scalars().all())

    async def get_by_user(self, user_id: UUID) -> list[ApiKey]:
        result = await self.db.execute(select(ApiKey).where(ApiKey.user_id == user_id))
        return list(result.scalars().all())

    async def update_last_used(self, key_id: UUID) -> bool:
        api_key = await self.get(key_id)
        if api_key:
            api_key.last_used_at = datetime.utcnow()
            await self.db.flush()
            return True
        return False

    async def update(self, api_key: ApiKey) -> ApiKey:
        await self.db.flush()
        await self.db.refresh(api_key)
        return api_key

    async def delete(self, key_id: UUID) -> bool:
        api_key = await self.get(key_id)
        if api_key:
            await self.db.delete(api_key)
            return True
        return False


# Repository dependencies
async def get_user_repo(db: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(db)


async def get_organization_repo(db: AsyncSession = Depends(get_session)) -> OrganizationRepository:
    return OrganizationRepository(db)


async def get_project_repo(db: AsyncSession = Depends(get_session)) -> ProjectRepository:
    return ProjectRepository(db)


async def get_membership_repo(db: AsyncSession = Depends(get_session)) -> MembershipRepository:
    return MembershipRepository(db)


async def get_api_key_repo(db: AsyncSession = Depends(get_session)) -> ApiKeyRepository:
    return ApiKeyRepository(db)