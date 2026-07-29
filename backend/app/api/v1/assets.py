from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from app.database.session import get_session
from app.repositories import asset_repo
from app.schemas.base import ResponseSchema, PaginatedResponse
from app.domain.models.asset import Asset as AssetModel
from app.domain.schemas.asset import (
    AssetRead,
    AssetCreate,
    AssetUpdate,
)
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("", response_model=ResponseSchema[PaginatedResponse[AssetRead]])
async def list_assets(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    type: Optional[str] = None,
    db: AsyncSession = Depends(get_session),
):
    """List assets with pagination."""
    filters = {}
    if type:
        filters["type"] = type
    items = await asset_repo.list(db, skip=(page - 1) * page_size, limit=page_size, **filters)
    total = await asset_repo.count(db, **filters)
    return ResponseSchema(
        data=PaginatedResponse(
            items=[AssetRead.from_orm(i) for i in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size,
        )
    )


@router.post("", response_model=ResponseSchema[AssetRead])
async def create_asset(
    payload: AssetCreate,
    db: AsyncSession = Depends(get_session),
):
    """Create a new asset."""
    asset = AssetModel(**payload.dict())
    asset = await asset_repo.create(db, asset)
    logger.info("asset.created", id=str(asset.id))
    return ResponseSchema(data=AssetRead.from_orm(asset))


@router.get("/{asset_id}", response_model=ResponseSchema[AssetRead])
async def get_asset(
    asset_id: UUID,
    db: AsyncSession = Depends(get_session),
):
    """Get an asset by ID."""
    asset = await asset_repo.get(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return ResponseSchema(data=AssetRead.from_orm(asset))


@router.patch("/{asset_id}", response_model=ResponseSchema[AssetRead])
async def update_asset(
    asset_id: UUID,
    payload: AssetUpdate,
    db: AsyncSession = Depends(get_session),
):
    """Update asset fields."""
    asset = await asset_repo.get(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(asset, k, v)
    asset = await asset_repo.update(db, asset)
    return ResponseSchema(data=AssetRead.from_orm(asset))


@router.delete("/{asset_id}")
async def delete_asset(
    asset_id: UUID,
    db: AsyncSession = Depends(get_session),
):
    """Delete an asset."""
    deleted = await asset_repo.delete(db, asset_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Asset not found")
    return ResponseSchema(message="Asset deleted")