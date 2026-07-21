"""Cancellation token for running tasks/plans.

The platform-wide cancellation contract: every running Plan owns a
token, and (eventually) HTTP handlers or supervisors may request
cancellation by call site.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Callable


class CancelledError(asyncio.CancelledError):
    """A typed alias for cancellation that originates from the platform."""


@dataclass
class CancellationToken:
    """Lightweight, async-friendly cancellation."""

    cancelled: bool = False
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    _future: asyncio.Future[None] | None = None

    def is_cancelled(self) -> bool:
        return self.cancelled

    async def cancel(self) -> None:
        async with self._lock:
            if self.cancelled:
                return
            self.cancelled = True
            if self._future is None:
                self._future = asyncio.get_event_loop().create_future()
            self._future.set_result(None)

    async def wait(self) -> None:
        if self._future is None:
            self._future = asyncio.get_event_loop().create_future()
            if self.cancelled:
                self._future.set_result(None)
        await self._future


__all__ = ["CancellationToken", "CancelledError"]
