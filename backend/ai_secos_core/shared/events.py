"""In-process event dispatcher protocol.

Application code (Workflow Engine, Plugin Executor, Finding Engine, Risk
Engine, AI Gateway, Report Engine) emits `DomainEvent`s via this
dispatcher. The default implementation is in-process; later milestones can
swap to a Kafka/Redis-backed dispatcher without changing callers.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Protocol


@dataclass(frozen=True)
class DomainEvent:
    """Base shape of every platform event.

    Concrete events extend this with module-specific fields.
    """

    type: str
    occurred_at: datetime
    correlation_id: str
    payload: dict[str, Any]


class EventDispatcher(Protocol):
    """Protocol for an in-process pub-sub dispatcher.

    Implementations must be safe to call from async code.
    """

    async def publish(self, event: DomainEvent) -> None: ...

    def subscribe(
        self, event_type: str, handler: Callable[[DomainEvent], "asyncio.Future[None]"]
    ) -> None: ...


class InProcessEventDispatcher:
    """Default in-process dispatcher.

    - The handlers list per event type is the simple list of callables.
    - Handlers are called sequentially within the publishing task.
    - On error, handlers raise; the dispatcher logs via the event bus
      logger if available, and continues with the next handler (best-effort).
    """

    def __init__(self) -> None:
        self._handlers: dict[str, list[Callable[[DomainEvent], "asyncio.Future[None]"]]] = {}

    async def publish(self, event: DomainEvent) -> None:
        handlers = list(self._handlers.get(event.type, []))
        for handler in handlers:
            try:
                await handler(event)
            except Exception:  # noqa: BLE001
                # Best-effort delivery: a failing handler must not break
                # the publishing path. Production observability layer
                # (added in later milestones) handles logging.
                continue

    def subscribe(
        self,
        event_type: str,
        handler: Callable[[DomainEvent], "asyncio.Future[None]"],
    ) -> None:
        self._handlers.setdefault(event_type, []).append(handler)


def make_event(
    event_type: str,
    *,
    correlation_id: str,
    payload: dict[str, Any] | None = None,
) -> DomainEvent:
    """Factory that stamps occurred_at and correlation id automatically."""
    return DomainEvent(
        type=event_type,
        occurred_at=datetime.now(timezone.utc),
        correlation_id=correlation_id,
        payload=payload or {},
    )


__all__ = [
    "DomainEvent",
    "EventDispatcher",
    "InProcessEventDispatcher",
    "make_event",
]
