"""
AstraIX Security Analyst - Main Application

Entry point for the FastAPI application.
"""

from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from sqlalchemy import select, update

from app.config import get_settings
from app.api.v1 import api_router
from app.core.logging import get_logger, setup_logging
from app.database.session import init_db, close_db, async_session_maker
from app.domain.models.assessment import Assessment
from app.plugins import get_plugin_registry

settings = get_settings()
setup_logging()
logger = get_logger(__name__)


async def _recover_orphaned_assessments():
    """Mark running assessments orphaned by a service restart as failed."""
    try:
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=2)
        async with async_session_maker() as session:
            orphaned = (
                await session.execute(
                    select(Assessment.id).where(
                        Assessment.status == "running",
                        Assessment.started_at.isnot(None),
                        Assessment.started_at < cutoff,
                    )
                )
            ).scalars().all()
            if orphaned:
                await session.execute(
                    update(Assessment)
                    .where(Assessment.id.in_(orphaned))
                    .values(
                        status="failed",
                        error="Interrupted by service restart",
                        completed_at=datetime.now(timezone.utc),
                    )
                )
                await session.commit()
                logger.warning(
                    "assessments.orphaned_recovered",
                    count=len(orphaned),
                    ids=[str(i) for i in orphaned],
                )
    except Exception as exc:
        logger.warning("assessments.orphan_recovery_failed", error=str(exc))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup/shutdown."""
    logger.info(
        "astraix.startup",
        name=settings.APP_NAME,
        version=settings.APP_VERSION,
        env=settings.APP_ENV,
    )

    # Initialize plugins
    try:
        registry = await get_plugin_registry()
        logger.info("plugins.loaded", count=len(registry.list_plugins()))
    except Exception as exc:
        logger.warning("plugins.load_failed", error=str(exc))

    # Initialize database
    await init_db()
    logger.info("database.initialized")

    # Recover assessments orphaned by a previous process exit
    await _recover_orphaned_assessments()

    # Warm the knowledge-base index in the background so the first scan's
    # planner does not blow the plan budget on the 2-3min index load.
    try:
        import threading

        from app.vapt.agents.kb import get_kb

        threading.Thread(target=get_kb, daemon=True, name="kb-warmup").start()
        logger.info("knowledge_base.warmup_started (background)")
    except Exception as exc:
        logger.warning("knowledge_base.warmup_failed", error=str(exc))

    yield

    await close_db()
    logger.info("astraix.shutdown")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Autonomous Security Assessment Platform",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    redirect_slashes=False,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# API routes
app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    """Root endpoint: health/status overview."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "docs": "/docs" if settings.DEBUG else "disabled",
        "api": settings.API_PREFIX,
        "status": "operational",
    }


@app.get("/health")
async def health_check():
    """Basic liveness check."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.get("/ready")
async def readiness_check():
    """Readiness check (validates dependencies)."""
    return {"status": "ready", "service": settings.APP_NAME}