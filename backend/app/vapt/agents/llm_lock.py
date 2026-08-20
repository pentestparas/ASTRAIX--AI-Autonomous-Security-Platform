"""
Global LLM call serializer.

The agent loop and the test-matrix phase run concurrently in one scan and
both hammer the same providers (NVIDIA NIM rate limits, Ollama single
model). A per-event-loop asyncio lock serializes provider round-trips so
bursts a) don't 429 the NIM endpoint and b) don't time out the phase budget.

The lock is cached per running event loop: asyncio.Lock binds to the loop
that creates it, and a stray lock from a dead throwaway loop (e.g. a CLI
reproduction) would otherwise hang every waiter on the server loop.
"""

import asyncio
import threading

_locks: dict = {}
_guard = threading.Lock()


def get_llm_lock() -> asyncio.Lock:
    loop = asyncio.get_running_loop()
    with _guard:
        lock = _locks.get(loop)
        if lock is None:
            lock = asyncio.Lock()
            _locks[loop] = lock
        return lock