"""Convert platform errors → HTTP responses.

FastAPI exception handlers delegate to this module. Kept outside
FastAPI types for testability.
"""

from collections.abc import Mapping
from typing import Any

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse

from ai_secos_core.shared.errors import PlatformError


def register_exception_handlers(app: FastAPI) -> None:
    """Bind platform error handler."""
    from ai_secos_core.api_platform.dependencies import get_container

    @app.exception_handler(PlatformError)
    async def handle_platform_error(
        request: Request,
        exc: PlatformError,
    ) -> JSONResponse:
        container = await get_container(request)
        status_code = exc.http_status
        response = _map_error(exc, status_code, container)
        context = container.logger.bind(
            correlation_id=response["error"]["correlation_id"],
            error=exc.__class__.__name__,
        )
        if status_code >= 500:
            context.error("platform.error", message=exc.message)
        else:
            context.info("platform.error", message=exc.message)
        return JSONResponse(
            status_code=status_code,
            content=response,
        )


def _map_error(
    exc: PlatformError,
    code: int,
    container,
) -> dict[str, Any]:  # avoid raw dict typing
    """Shared mapping logic."""
    from ai_secos_core.shared.correlation import get_correlation_id

    response = {
        "ok": False,
        "error": {
            "type": exc.__class__.__name__,
            "code": exc.code,
            "message": exc.message,
            "details": _safe(exc.details),
            "correlation_id": str(get_correlation_id()),
        },
    }
    return response


def _safe(payload: Any) -> Any:
    """JSON-safe pinch."""
    try:
        import json
        json.dumps(payload)
        return payload
    except TypeError:
        try:
            return str(payload)
        except Exception:
            return repr(payload)


__all__ = ["register_exception_handlers"]
