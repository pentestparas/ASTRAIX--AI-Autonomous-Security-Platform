"""
Repository pattern for data access.

Each repository:
  - Wraps SQLAlchemy queries for a model
  - Provides async CRUD operations
  - Returns Pydantic-validated objects
"""

from typing import Generic, Optional, Type, TypeVar, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete as sql_delete, update as sql_update
from uuid import UUID

from app.database.session import Base


T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """Generic repository for any model."""

    def __init__(self, model: Type[T]):
        self.model = model

    async def get(self, db: AsyncSession, id: UUID) -> Optional[T]:
        """Get by ID."""
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def list(self, db: AsyncSession, skip: int = 0, limit: int = 100, **filters) -> List[T]:
        """List with pagination and optional filters."""
        from sqlalchemy import String
        query = select(self.model)
        exclude_status = filters.pop("exclude_status", None)
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.where(getattr(self.model, key) == value)
        if exclude_status and hasattr(self.model, "status"):
            query = query.where(self.model.status != str(exclude_status))
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def count(self, db: AsyncSession, **filters) -> int:
        """Count records with optional filters."""
        from sqlalchemy import func
        query = select(func.count()).select_from(self.model)
        exclude_status = filters.pop("exclude_status", None)
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.where(getattr(self.model, key) == value)
        if exclude_status and hasattr(self.model, "status"):
            query = query.where(self.model.status != str(exclude_status))
        result = await db.execute(query)
        return result.scalar() or 0

    async def create(self, db: AsyncSession, obj: T) -> T:
        """Create a new instance."""
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def update(self, db: AsyncSession, obj: T) -> T:
        """Update instance."""
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def delete(self, db: AsyncSession, id: UUID) -> bool:
        """Delete by ID."""
        stmt = sql_delete(self.model).where(self.model.id == id)
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount > 0


# --- Domain repositories ---
from app.domain.models.assessment import Assessment
from app.domain.models.finding import Finding
from app.domain.models.asset import Asset

assessment = BaseRepository(Assessment)
finding = BaseRepository(Finding)
asset = BaseRepository(Asset)

# Aliases for backward compatibility
assessment_repo = assessment
finding_repo = finding
asset_repo = asset

# --- Organization repositories ---
from app.repositories.organization import (
    UserRepository,
    OrganizationRepository,
    ProjectRepository,
    MembershipRepository,
    ApiKeyRepository,
    get_user_repo,
    get_organization_repo,
    get_project_repo,
    get_membership_repo,
    get_api_key_repo,
)

__all__ = [
    "BaseRepository",
    "assessment",
    "finding",
    "asset",
    "UserRepository",
    "OrganizationRepository",
    "ProjectRepository",
    "MembershipRepository",
    "ApiKeyRepository",
    "get_user_repo",
    "get_organization_repo",
    "get_project_repo",
    "get_membership_repo",
    "get_api_key_repo",
]