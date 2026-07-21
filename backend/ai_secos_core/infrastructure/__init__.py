"""Cross-cutting infrastructure components.

This package provides:
  - Structured logging (correlation-aware, JSON or console).
  - Standard error → HTTP mapping (used by the FastAPI layer).
  - Metrics/tracing hooks (stubs that accept config; metrics/tracing
    transports can be wired in a later milestone).

No database, no cache, no queue are wired here at Milestone 1.
Those are explicitly deferred per MVP_SCOPE.md.
"""

from ai_secos_core.infrastructure.logging import (
    configure_logging,
    get_logger,
    bind_correlation_id,
)
from ai_secos_core.infrastructure.error_mapping import (
    platform_error_to_http_response,
    PlatformErrorResponse,
)
from ai_secos_core.infrastructure.metrics import (
    MetricsRegistry,
    Counter,
    Histogram,
    NoopMetricsRegistry,
)

__all__ = [
    "configure_logging",
    "get_logger",
    "bind_correlation_id",
    "platform_error_to_http_response",
    "PlatformErrorResponse",
    "MetricsRegistry",
    "Counter",
    "Histogram",
    "NoopMetricsRegistry",
]
