"""AI-SecOS Core configuration package.

Single point of access to typed settings. All values are loaded from
environment variables (12-factor) with validation at startup.
"""

from ai_secos_core.config.settings import (
    Settings,
    PlatformSettings,
    ObservabilitySettings,
    PluginSystemSettings,
    FindingEngineSettings,
    RiskEngineSettings,
    AIGatewaySettings,
    load_settings,
)
from ai_secos_core.config.constants import (
    DEFAULT_HTTP_TIMEOUT_SECONDS,
    DEFAULT_PLUGIN_TIMEOUT_SECONDS,
    DEFAULT_PLUGIN_CPU_QUOTA,
    DEFAULT_PLUGIN_MEMORY_MB,
    DEFAULT_RISK_SCORE_MIN,
    DEFAULT_RISK_SCORE_MAX,
)

__all__ = [
    "Settings",
    "PlatformSettings",
    "ObservabilitySettings",
    "PluginSystemSettings",
    "FindingEngineSettings",
    "RiskEngineSettings",
    "AIGatewaySettings",
    "load_settings",
    "DEFAULT_HTTP_TIMEOUT_SECONDS",
    "DEFAULT_PLUGIN_TIMEOUT_SECONDS",
    "DEFAULT_PLUGIN_CPU_QUOTA",
    "DEFAULT_PLUGIN_MEMORY_MB",
    "DEFAULT_RISK_SCORE_MIN",
    "DEFAULT_RISK_SCORE_MAX",
]
