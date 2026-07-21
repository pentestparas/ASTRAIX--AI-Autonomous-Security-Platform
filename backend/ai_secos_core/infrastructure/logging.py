"""Correlation-aware structured logging.

Default backend is `logging` to avoid hard-pinning a dependency on
`structlog`; a future milestone may swap to richer processors.

Every log line carries the active correlation id, so the AI engineer's
"log every critical action" rule is enforceable.
"""

from __future__ import annotations

import logging
import sys
from typing import Any

from ai_secos_core.config.settings import ObservabilitySettings, load_settings
from ai_secos_core.shared.correlation import (
    CorrelationId,
    correlation_id_var,
    get_correlation_id,
)

_LOG_RECORD_FORMAT = (
    "%(asctime)s %(levelname)s [%(correlation_id)s] %(name)s — %(message)s"
)
_RESERVED_LOG_KEYS = {
    "name", "msg", "args", "levelname", "levelno", "pathname", "filename",
    "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName",
    "created", "msecs", "relativeCreated", "thread", "threadName",
    "processName", "process", "message",
}


class _CorrelationIdFilter(logging.Filter):
    """Inject the active correlation id into every record."""

    def filter(self, record: logging.LogRecord) -> bool:  # noqa: D401
        cid = get_correlation_id()
        record.correlation_id = str(cid)
        return True


def _json_formatter() -> logging.Formatter:
    """Minimal JSON formatter using only stdlib."""

    import json

    class JsonFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:  # noqa: D401
            payload: dict[str, Any] = {
                "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
                "level": record.levelname,
                "logger": record.name,
                "correlation_id": getattr(record, "correlation_id", "-"),
                "message": record.getMessage(),
            }
            extras = {
                k: v for k, v in record.__dict__.items()
                if k not in _RESERVED_LOG_KEYS and k != "correlation_id"
            }
            if extras:
                payload["extra"] = extras
            if record.exc_info:
                payload["exception"] = self.formatException(record.exc_info)
            return json.dumps(payload, default=str)

    return JsonFormatter()


def _console_formatter() -> logging.Formatter:
    return logging.Formatter(_LOG_RECORD_FORMAT)


def configure_logging(
    settings: ObservabilitySettings | None = None,
) -> None:
    """Configure the root logger.

    Idempotent: safe to call multiple times.
    """
    settings = settings or load_settings().observability

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.addFilter(_CorrelationIdFilter())
    handler.setFormatter(
        _json_formatter() if settings.log_format == "json" else _console_formatter()
    )

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(getattr(logging, settings.log_level.upper()))


def get_logger(name: str) -> logging.Logger:
    """Return a logger; configure on first use."""
    if not logging.getLogger().handlers:
        configure_logging()
    return logging.getLogger(name)


def bind_correlation_id(cid: CorrelationId | str) -> None:
    """Set the active correlation id for subsequent logs."""
    correlation_id_var.set(
        cid if isinstance(cid, CorrelationId) else CorrelationId(cid)
    )


__all__ = [
    "configure_logging",
    "get_logger",
    "bind_correlation_id",
]
