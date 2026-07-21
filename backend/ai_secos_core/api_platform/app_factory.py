"""FastAPI app factory.

Binds the DI container to the web transport.

- Health/ready endpoints.
- Lifespan hooks.
- CORS middleware.
- Exception handlers.
"""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ai_secos_core.api_platform.container import Container, build_default_container


@asynccontextmanager
async def lifespan(app: FastAPI, container: Container) -> AsyncIterator[None]:
    """Start/stop lifetime management."""
    container.logger.info("platform.startup")
    yield
    container.logger.info("platform.shutdown")
    await container.events.publish(
        container.shared.events.make_event("platform.shutdown")
    )


def build_app(container: Container | None = None) -> FastAPI:
    """Create the FastAPI application.

    Mostly configures routing + middleware; DI container is wired
    separately.
    """
    container = container or build_default_container()

    app = FastAPI(
        title=container.settings.platform.app_name,
        version=container.settings.platform.app_version,
        description=(
            "AI-SecOS Core — Reusable AI-native cybersecurity runtime. "
            "See: PROJECT_MANIFEST.md"
        ),
        docs_url="/docs" if container.settings.platform.debug else None,
        lifespan=lambda app: lifespan(app, container),
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=container.settings.platform.cors_origins,
        allow_credentials=container.settings.platform.cors_allow_credentials,
        allow_methods=container.settings.platform.cors_allow_methods,
        allow_headers=container.settings.platform.cors_allow_headers,
    )

    # Wire routers
    from ai_secos_core.api_platform.routes import router
    app.include_router(router, prefix="/api/v1")

    # Error handlers are registered in `error_handlers.py`.

    app.state.container = container
    return app


__all__ = ["build_app"]
