from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from app.database.session import get_session
from app.repositories import finding_repo
from app.schemas.base import ResponseSchema, PaginatedResponse
from app.domain.models.finding import Finding as FindingModel
from app.domain.schemas.finding import (
    FindingRead,
    FindingUpdate,
)
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/", response_model=ResponseSchema[PaginatedResponse[FindingRead]])
async def list_findings(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    severity: Optional[str] = None,
    assessment_id: Optional[UUID] = None,
    asset_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_session),
):
    """List findings with pagination."""
    filters = {}
    if severity:
        filters["severity"] = severity
    if assessment_id:
        filters["assessment_id"] = assessment_id
    if asset_id:
        filters["asset_id"] = asset_id
    items = await finding_repo.list(db, skip=(page - 1) * page_size, limit=page_size, **filters)
    total = await finding_repo.count(db, **filters)
    return ResponseSchema(
        data=PaginatedResponse(
            items=[FindingRead.from_orm(i) for i in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size,
        )
    )


@router.get("/{finding_id}", response_model=ResponseSchema[FindingRead])
async def get_finding(
    finding_id: UUID,
    db: AsyncSession = Depends(get_session),
):
    """Get a finding by ID."""
    finding = await finding_repo.get(db, finding_id)
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    return ResponseSchema(data=FindingRead.from_orm(finding))


@router.patch("/{finding_id}", response_model=ResponseSchema[FindingRead])
async def update_finding(
    finding_id: UUID,
    payload: FindingUpdate,
    db: AsyncSession = Depends(get_session),
):
    """Update finding status / fields."""
    finding = await finding_repo.get(db, finding_id)
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(finding, k, v)
    finding = await finding_repo.update(db, finding)
    return ResponseSchema(data=FindingRead.from_orm(finding))


@router.delete("/{finding_id}")
async def delete_finding(
    finding_id: UUID,
    db: AsyncSession = Depends(get_session),
):
    """Delete a finding."""
    deleted = await finding_repo.delete(db, finding_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Finding not found")
    return ResponseSchema(message="Finding deleted")