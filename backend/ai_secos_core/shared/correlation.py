"""Correlation id context.

Every critical action (workflow, plugin exec, AI call) carries a correlation id
that is propagated via `contextvars`, written to logs, and emitted on the
event bus. Application code may set it; the platform never invents one outside
of entrypoints.
"""

from __future__ import annotations

import uuid
from contextvars import ContextVar
from typing import NewType

CorrelationId = NewType("CorrelationId", str)

correlation_id_var: ContextVar[CorrelationId | None] = ContextVar(
    "ai_secos_correlation_id",
    default=None,
)


def new_correlation_id() -> CorrelationId:
    """Produce a new opaque correlation id (UUID4 hex)."""
    return CorrelationId(uuid.uuid4().hex)


def get_correlation_id() -> CorrelationId:
    """Return the current correlation id, creating one if absent.

    Use only at entrypoints (HTTP handler, worker message, plugin runner).
    """
    cid = correlation_id_var.get()
    if cid is None:
        cid = new_correlation_id()
        correlation_id_var.set(cid)
    return cid


def set_correlation_id(cid: CorrelationId | str) -> CorrelationId:
    typed = cid if isinstance(cid, CorrelationId) else CorrelationId(cid)
    correlation_id_var.set(typed)
    return typed


__all__ = [
    "CorrelationId",
    "correlation_id_var",
    "new_correlation_id",
    "get_correlation_id",
    "set_correlation_id",
]
