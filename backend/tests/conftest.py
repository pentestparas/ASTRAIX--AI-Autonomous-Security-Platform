"""Pytest configuration and fixtures."""
import pytest
import asyncio
from typing import AsyncGenerator
import os
import sys

# Add app directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def mock_settings():
    """Mock settings for tests."""
    from app.config import settings as app_settings
    app_settings.APP_ENV = "test"
    app_settings.DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    return app_settings


@pytest.fixture
def mock_registry():
    """Mock plugin registry."""
    from app.plugins import PluginRegistry
    return PluginRegistry(plugins_dir="/tmp/nonexistent")


@pytest.fixture
def mock_orchestrator():
    """Mock orchestrator."""
    from app.orchestrator import Orchestrator
    return Orchestrator(plugin_registry=None)