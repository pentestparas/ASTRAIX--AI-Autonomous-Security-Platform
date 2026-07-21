"""AI-SecOS Core test entrypoint."""
import pytest

pytest_plugins = [
    "ai_secos_core.tests.platform.conftest",
    "ai_secos_core.tests.runtime.conftest",
    "ai_secos_core.tests.plugin_system.conftest",
    "ai_secos_core.tests.finding_engine.conftest",
    "ai_secos_core.tests.risk_engine.conftest",
    "ai_secos_core.tests.ai_gateway.conftest",
]


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "integration: cross-module or subprocess integration"
    )
    config.addinivalue_line("markers", "slow: > 1 second")


@pytest.fixture(scope="session")
def event_loop():
    import asyncio

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()