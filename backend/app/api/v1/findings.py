from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from app.database.session import get_session
from app.repositories import finding_repo, assessment_repo
from app.repositories.organization import MembershipRepository, ProjectRepository
from app.schemas.base import ResponseSchema, PaginatedResponse
from app.domain.models.finding import Finding as FindingModel
from app.domain.models.organization import User
from app.domain.models.asset import Asset
from app.domain.schemas.finding import (
    FindingRead,
    FindingUpdate,
)
from app.core.auth import get_current_user
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


async def _user_org_ids(db: AsyncSession, user: User) -> set[str]:
    memberships = await MembershipRepository(db).get_user_memberships(user.id)
    return {str(m.organization_id) for m in memberships}


async def _require_org_access(db: AsyncSession, user: User, org_id) -> None:
    if str(org_id) not in await _user_org_ids(db, user):
        raise HTTPException(status_code=403, detail="No access to this organization")


class BulkUpdateRequest(BaseModel):
    ids: list[str]
    status: Optional[str] = None
    severity: Optional[str] = None


@router.get("", response_model=ResponseSchema[PaginatedResponse[FindingRead]])
async def list_findings(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    severity: Optional[str] = None,
    status: Optional[str] = None,
    assessment_id: Optional[str] = None,
    asset_id: Optional[str] = None,
    organization_id: Optional[str] = None,
    project_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    """List findings with pagination. Only true positives by default.

    When no explicit ``status`` filter is given, ``false_positive`` findings
    are excluded so the list represents confirmed vulnerabilities.

    Results are scoped to the caller's organizations; foreign
    assessment/asset/project/org ids are rejected.
    """
    allowed_orgs = await _user_org_ids(db, current_user)
    if organization_id:
        if str(organization_id) not in allowed_orgs:
            raise HTTPException(status_code=403, detail="No access to this organization")
    if assessment_id:
        assessment = await assessment_repo.get(db, assessment_id)
        if not assessment or str(assessment.organization_id) not in allowed_orgs:
            raise HTTPException(status_code=403, detail="No access to this assessment")
    if asset_id:
        from sqlalchemy import select
        asset = (
            await db.execute(select(Asset).where(Asset.id == str(asset_id)))
        ).scalar_one_or_none()
        if not asset or str(asset.organization_id) not in allowed_orgs:
            raise HTTPException(status_code=403, detail="No access to this asset")
    if project_id:
        project = await ProjectRepository(db).get(project_id)
        if not project or str(project.organization_id) not in allowed_orgs:
            raise HTTPException(status_code=403, detail="No access to this project")
    filters = {}
    if severity:
        filters["severity"] = severity
    if status:
        filters["status"] = status
    elif not status:
        filters["exclude_status"] = "false_positive"
    if assessment_id:
        filters["assessment_id"] = assessment_id
    if asset_id:
        filters["asset_id"] = asset_id
    if organization_id:
        filters["organization_id"] = str(organization_id)
    elif allowed_orgs:
        filters["organization_id__in"] = allowed_orgs
    else:
        filters["organization_id__in"] = [""]
    if project_id:
        filters["project_id"] = project_id
    items = await finding_repo.list(db, skip=(page - 1) * page_size, limit=page_size, **filters)
    total = await finding_repo.count(db, **filters)
    return ResponseSchema(
        data=PaginatedResponse(
            items=[FindingRead.model_validate(i) for i in items],
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
    return ResponseSchema(data=FindingRead.model_validate(finding))


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
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(finding, k, v)
    finding = await finding_repo.update(db, finding)
    return ResponseSchema(data=FindingRead.model_validate(finding))


@router.post("/bulk-update", response_model=ResponseSchema[dict])
async def bulk_update_findings(
    payload: BulkUpdateRequest,
    db: AsyncSession = Depends(get_session),
):
    """Bulk update findings by IDs."""
    updated = 0
    for fid in payload.ids:
        try:
            finding = await finding_repo.get(db, UUID(fid))
            if not finding:
                continue
            if payload.status is not None:
                finding.status = payload.status
            if payload.severity is not None:
                finding.severity = payload.severity
            await finding_repo.update(db, finding)
            updated += 1
        except Exception:
            continue
    return ResponseSchema(data={"updated": updated}, message=f"Updated {updated} findings")


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