"""FastAPI transport: health, ready, version.

All other API routes beyond these three belong to the Application
layer (Astrix Security Analyst), not AI-SecOS Core.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from ai_secos_core.api_platform.container import Container
from ai_secos_core.api_platform.dependencies import get_container

router = APIRouter(tags=["platform"])


@router.get("/health")
async def health() -> dict[str, Any]:
    """Endpoint health; always 200."""
    _not_used = await get_container()  # ensure container wired
    return {"status": "ok", "service": "ai-secos", "detail": "live"}


@router.get("/ready")
async def ready() -> dict[str, Any]:
    """Ready — fail if plugins unload or config invalid."""
    try:
        container = await get_container()
        # Invoke a marker that throws on failed discovery.
        _ = container.plugins.ids()
        return {"status": "ok", "service": "ai-secos", "detail": "ready"}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.get("/version")
async def version() -> dict[str, Any]:
    """Runtime identity."""
    container = await get_container()
    return {
        "service": "ai-secos-core",
        "version": container.settings.platform.app_version,
    }


__all__ = ["router"]
