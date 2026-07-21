"""Typed platform settings (Pydantic v2, 12-factor).

Loading model:
  - All values are environment-driven (`.env` and process env).
  - Constructor performs startup-time validation.
  - Cache-friendly single factory: `load_settings()`.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from ai_secos_core.config.constants import (
    DEFAULT_AI_MAX_TOKENS,
    DEFAULT_AI_RETRY_ATTEMPTS,
    DEFAULT_AI_RETRY_BACKOFF_SECONDS,
    DEFAULT_AI_TIMEOUT_SECONDS,
    DEFAULT_PLUGIN_CPU_QUOTA,
    DEFAULT_PLUGIN_MEMORY_MB,
    DEFAULT_PLUGIN_TIMEOUT_SECONDS,
)


class PlatformSettings(BaseSettings):
    """Top-level runtime / identity settings."""

    model_config = SettingsConfigDict(
        env_prefix="ASTRAIX_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        frozen=False,
    )

    app_name: str = Field(default="AI-SecOS Core")
    app_version: str = Field(default="0.1.0")
    app_env: Literal["development", "test", "production"] = "development"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000

    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = Field(default_factory=lambda: ["*"])
    cors_allow_headers: list[str] = Field(default_factory=lambda: ["*"])


class ObservabilitySettings(BaseSettings):
    """Structured logging / tracing / metrics configuration."""

    model_config = SettingsConfigDict(
        env_prefix="ASTRAIX_OBS_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_format: Literal["json", "console"] = "json"
    log_correlation_id_header: str = "x-correlation-id"
    metrics_enabled: bool = False
    tracing_enabled: bool = False
    service_namespace: str = "ai_secos_core"


class PluginSystemSettings(BaseSettings):
    """Plugin execution / sandbox configuration."""

    model_config = SettingsConfigDict(
        env_prefix="ASTRAIX_PLUGIN_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    plugins_root: str = "plugins"
    timeout_seconds: int = DEFAULT_PLUGIN_TIMEOUT_SECONDS
    cpu_quota: float = DEFAULT_PLUGIN_CPU_QUOTA
    memory_mb: int = DEFAULT_PLUGIN_MEMORY_MB
    allow_command_allowlist: list[str] = Field(
        default_factory=lambda: ["python", "python3", "node", "go", "sh"]
    )


class FindingEngineSettings(BaseSettings):
    """Rules for normalization, dedup, and enrichment."""

    model_config = SettingsConfigDict(
        env_prefix="ASTRAIX_FINDING_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    deduplicate_enabled: bool = True
    enrich_with_intel: bool = False
    confidence_default: float = 0.5
    severity_levels: list[str] = Field(
        default_factory=lambda: ["info", "low", "medium", "high", "critical"]
    )


class RiskEngineSettings(BaseSettings):
    """Risk scoring configuration (interfaces only at Milestone 1)."""

    model_config = SettingsConfigDict(
        env_prefix="ASTRAIX_RISK_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    score_min: int = 0
    score_max: int = 100
    weights: dict[str, float] = Field(
        default_factory=lambda: {
            "likelihood": 0.25,
            "impact": 0.35,
            "exploitability": 0.25,
            "business_context": 0.15,
        }
    )


class AIGatewaySettings(BaseSettings):
    """AI Gateway configuration (provider-agnostic; no providers implemented yet)."""

    model_config = SettingsConfigDict(
        env_prefix="ASTRAIX_AI_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    timeout_seconds: float = DEFAULT_AI_TIMEOUT_SECONDS
    max_tokens: int = DEFAULT_AI_MAX_TOKENS
    retry_attempts: int = DEFAULT_AI_RETRY_ATTEMPTS
    retry_backoff_seconds: float = DEFAULT_AI_RETRY_BACKOFF_SECONDS
    cache_enabled: bool = False
    cache_ttl_seconds: int = 3600
    cost_aware_routing: bool = False


class Settings(BaseSettings):
    """Aggregate settings; the single value passed to the DI container."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    platform: PlatformSettings = Field(default_factory=PlatformSettings)
    observability: ObservabilitySettings = Field(default_factory=ObservabilitySettings)
    plugin_system: PluginSystemSettings = Field(default_factory=PluginSystemSettings)
    finding_engine: FindingEngineSettings = Field(default_factory=FindingEngineSettings)
    risk_engine: RiskEngineSettings = Field(default_factory=RiskEngineSettings)
    ai_gateway: AIGatewaySettings = Field(default_factory=AIGatewaySettings)


@lru_cache(maxsize=1)
def load_settings() -> Settings:
    """Single-entry factory. Cached for the process lifetime."""
    return Settings()
