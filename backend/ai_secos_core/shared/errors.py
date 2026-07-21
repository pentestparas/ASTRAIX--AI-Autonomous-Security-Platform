"""Single error hierarchy for the entire AI-SecOS Core.

Public API (the only types an Application or Plugin may raise):
  PlatformError        base
  PluginError          plugin-related
  WorkflowError        workflow/task-planner errors
  AIError              AI Gateway errors
  FindingEngineError   Finding Engine errors
  RiskEngineError      Risk Engine errors
  ReportEngineError    Report Engine errors
  ConfigurationError   configuration loading/validation errors

The HTTP layer (in `platform/`) maps these to status codes.
"""

from __future__ import annotations

from typing import Any


class PlatformError(Exception):
    """Base error of the platform.

    Carries `code` (machine-readable, stable) and `details`
    (structured debug data, never secrets).
    """

    code: str = "platform_error"
    http_status: int = 500

    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.__class__.__name__,
            "code": self.code,
            "message": self.message,
            "details": self.details,
        }


class PluginError(PlatformError):
    code = "plugin_error"
    http_status = 502  # upstream issue


class WorkflowError(PlatformError):
    code = "workflow_error"
    http_status = 422


class AIError(PlatformError):
    code = "ai_error"
    http_status = 502


class FindingEngineError(PlatformError):
    code = "finding_engine_error"
    http_status = 422


class RiskEngineError(PlatformError):
    code = "risk_engine_error"
    http_status = 422


class ReportEngineError(PlatformError):
    code = "report_engine_error"
    http_status = 422


class ConfigurationError(PlatformError):
    code = "configuration_error"
    http_status = 500


__all__ = [
    "PlatformError",
    "PluginError",
    "WorkflowError",
    "AIError",
    "FindingEngineError",
    "RiskEngineError",
    "ReportEngineError",
    "ConfigurationError",
]
