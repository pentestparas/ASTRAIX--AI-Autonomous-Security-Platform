"""
AstraIX Security Analyst - Main Application

Entry point for the FastAPI application.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from app.config import get_settings
from app.api.v1 import api_router
from app.core.logging import get_logger, setup_logging
from app.database.session import init_db, close_db
from app.plugins import get_plugin_registry

settings = get_settings()
setup_logging()
logger = get_logger(__name__)


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