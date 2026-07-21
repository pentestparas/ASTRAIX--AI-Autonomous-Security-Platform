"""Map platform errors → HTTP responses.

FastAPI exception handler in `platform/` delegates to this mapper.
Kept independent of FastAPI types for testability.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ai_secos_core.shared.correlation import get_correlation_id
from ai_secos_core.shared.errors import PlatformError


@dataclass(frozen=True)
class PlatformErrorResponse:
    status: int
    body: dict[str, Any]


def platform_error_to_http_response(error: PlatformError) -> PlatformErrorResponse:
    """Convert a PlatformError to a status/body pair.

    `correlation_id` is included so the client can reference it when
    seeking support.
    """
    body = {
        "ok": False,
        "error": {
            "type": type(error).__name__,
            "code": error.code,
            "message": error.message,
            "details": error.details,
            "correlation_id": str(get_correlation_id()),
        },
    }
    return PlatformErrorResponse(status=error.http_status, body=body)


__all__ = [
    "PlatformErrorResponse",
    "platform_error_to_http_response",
]
