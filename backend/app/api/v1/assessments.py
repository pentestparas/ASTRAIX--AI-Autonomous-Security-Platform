from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from app.database.session import get_session
from app.repositories import assessment_repo
from app.schemas.base import ResponseSchema, PaginatedResponse
from app.domain.models.assessment import Assessment as AssessmentModel
from app.domain.schemas.assessment import (
    AssessmentRead,
    AssessmentCreate,
)
from app.orchestrator.service import Orchestrator, AssessmentStatus, get_orchestrator
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("", response_model=ResponseSchema[PaginatedResponse[AssessmentRead]])
async def list_assessments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200, description="Page size (alias: limit)"),
    limit: int = Query(None, ge=1, le=200, description="Page size (alias for page_size)"),
    status: Optional[str] = None,
    type: Optional[str] = None,
    project_id: Optional[UUID] = None,
    organization_id: Optional[str] = None,
    db: AsyncSession = Depends(get_session),
):
    """List assessments with pagination."""
    effective_limit = limit if limit is not None else page_size
    filters = {}
    if status:
        filters["status"] = status
    if type:
        filters["type"] = type
    if project_id:
        filters["project_id"] = project_id
    if organization_id:
        filters["organization_id"] = organization_id
    items = await assessment_repo.list(db, skip=(page - 1) * effective_limit, limit=effective_limit, **filters)
    total = await assessment_repo.count(db, **filters)
    result_items = []
    for i in items:
        d = AssessmentRead.model_validate(i)
        d.asset_name = i.asset.name if hasattr(i, 'asset') and i.asset else None
        result_items.append(d)
    return ResponseSchema(
        data=PaginatedResponse(
            items=result_items,
            total=total,
            page=page,
            page_size=effective_limit,
            total_pages=(total + effective_limit - 1) // effective_limit,
        )
    )


@router.post("", response_model=ResponseSchema[AssessmentRead])
async def create_assessment(
    payload: AssessmentCreate,
    db: AsyncSession = Depends(get_session),
    orchestrator: Orchestrator = Depends(get_orchestrator),
):
    """Create and queue an assessment for execution."""
    assessment = AssessmentModel(**payload.model_dump())
    assessment.status = AssessmentStatus.PENDING.value
    assessment = await assessment_repo.create(db, assessment)
    logger.info("assessment.queued", id=str(assessment.id))

    # Execute
    try:
        result = await orchestrator.run_assessment(db, assessment.id)
        return ResponseSchema(data=AssessmentRead.model_validate(result))
    except Exception as exc:
        logger.error("assessment.error", id=str(assessment.id), exc=str(exc))
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/{assessment_id}", response_model=ResponseSchema[AssessmentRead])
async def get_assessment(
    assessment_id: UUID,
    db: AsyncSession = Depends(get_session),
):
    """Get an assessment by ID."""
    assessment = await assessment_repo.get(db, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    d = AssessmentRead.model_validate(assessment)
    d.asset_name = assessment.asset.name if hasattr(assessment, 'asset') and assessment.asset else None
    return ResponseSchema(data=d)


@router.post("/{assessment_id}/start", response_model=ResponseSchema[AssessmentRead])
async def start_assessment(
    assessment_id: UUID,
    db: AsyncSession = Depends(get_session),
    orchestrator: Orchestrator = Depends(get_orchestrator),
):
    """Start an assessment by ID."""
    assessment = await assessment_repo.get(db, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    result = await orchestrator.run_assessment(db, assessment_id)
    return ResponseSchema(data=AssessmentRead.model_validate(result))


@router.delete("/{assessment_id}")
async def cancel_assessment(
    assessment_id: UUID,
    db: AsyncSession = Depends(get_session),
):
    """Cancel an assessment (mark as cancelled)."""
    assessment = await assessment_repo.get(db, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    assessment.status = AssessmentStatus.CANCELLED.value
    await assessment_repo.update(db, assessment)
    return ResponseSchema(message="Assessment cancelled")