"""Dependency providers for FastAPI routes."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, Request

from ai_secos_core.api_platform.container import Container


async def get_container(request: Request) -> Container:
    """FastAPI dependency: immutable container wired to pathOps."""
    return request.app.state.container


async def get_settings(container: Container = Depends(get_container)):
    """Shortcut: typed settings."""
    return container.settings


__all__ = ["get_container", "get_settings"]
