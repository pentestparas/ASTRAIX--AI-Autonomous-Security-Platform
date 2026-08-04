"""
Scan Progress Bus

Redis-backed event stream for live scan progress. Each scan publishes
structured events (plan decisions, phase transitions, tool lifecycle,
findings) that the frontend polls and renders as a live console.
"""

import json
import os
import time
from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.core.logging import get_logger

logger = get_logger(__name__)

EVENT_TTL_SECONDS = int(os.environ.get("SCAN_PROGRESS_TTL", "3600"))
_SCAN_KEY_PREFIX = "scan:progress:{scan_id}:events"
_STATUS_KEY_PREFIX = "scan:progress:{scan_id}:status"


class ScanProgressBus:
    """Publishes and reads scan progress events (Redis-backed, in-memory fallback)."""

    def __init__(self):
        self._redis = None
        self._memory: Dict[str, List[Dict[str, Any]]] = {}
        self._memory_status: Dict[str, Dict[str, Any]] = {}
        self._use_redis = os.environ.get("VAPT_USE_REDIS_PROGRESS", "true").lower() == "true"
        self._init_redis()

    def _init_redis(self) -> None:
        if not self._use_redis:
            return
        try:
            import redis.asyncio as aioredis
            from app.core.config import settings

            self._redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
            logger.info("ScanProgressBus connected to Redis")
        except Exception as e:
            self._redis = None
            logger.warning("ScanProgressBus falling back to in-memory: %s", e)

    def _key(self, scan_id: str, prefix: str) -> str:
        return prefix.format(scan_id=scan_id)

    async def publish(self, scan_id: str, event_type: str, data: Dict[str, Any] = None) -> None:
        event = {
            "ts": time.time(),
            "type": event_type,
            "data": data or {},
        }
        if self._redis is not None:
            try:
                key = self._key(scan_id, _SCAN_KEY_PREFIX)
                await self._redis.rpush(key, json.dumps(event))
                await self._redis.expire(key, EVENT_TTL_SECONDS)
                status_key = self._key(scan_id, _STATUS_KEY_PREFIX)
                await self._redis.hset(status_key, "last_active", event["ts"])
                await self._redis.expire(status_key, EVENT_TTL_SECONDS)
                return
            except Exception as e:
                logger.warning("Redis publish failed, using memory: %s", e)
        self._memory.setdefault(scan_id, []).append(event)
        st = self._memory_status.setdefault(scan_id, {})
        st["last_active"] = event["ts"]

    async def set_status(self, scan_id: str, status: str, **extra: Any) -> None:
        payload = {"status": status, "ts": time.time(), "last_active": time.time(), **extra}
        if self._redis is not None:
            try:
                key = self._key(scan_id, _STATUS_KEY_PREFIX)
                await self._redis.hset(key, mapping=payload)
                await self._redis.expire(key, EVENT_TTL_SECONDS)
                return
            except Exception as e:
                logger.warning("Redis status failed, using memory: %s", e)
        self._memory_status[scan_id] = payload

    async def events(self, scan_id: str, since: int = 0) -> List[Dict[str, Any]]:
        if self._redis is not None:
            try:
                key = self._key(scan_id, _SCAN_KEY_PREFIX)
                raw = await self._redis.lrange(key, since, -1)
                events = [json.loads(e) for e in raw]
                total = await self._redis.llen(key)
                return events, total
            except Exception as e:
                logger.warning("Redis read failed, using memory: %s", e)
        items = self._memory.get(scan_id, [])
        return items[since:], len(items)

    async def status(self, scan_id: str) -> Optional[Dict[str, Any]]:
        if self._redis is not None:
            try:
                key = self._key(scan_id, _STATUS_KEY_PREFIX)
                data = await self._redis.hgetall(key)
                if data:
                    return dict(data)
            except Exception as e:
                logger.warning("Redis status read failed, using memory: %s", e)
        return self._memory_status.get(scan_id)

    async def active_scans(self) -> List[Dict[str, Any]]:
        """List scans that are still running (non-terminal status)."""
        terminal = {"completed", "failed", "cancelled", "error", "scan_completed"}
        scans: List[Dict[str, Any]] = []
        if self._redis is not None:
            try:
                pattern = _STATUS_KEY_PREFIX.format(scan_id="*")
                async for key in self._redis.scan_iter(match=pattern, count=100):
                    data = await self._redis.hgetall(key)
                    if not data:
                        continue
                    if data.get("status", "running") in terminal:
                        continue
                    parts = key.split(":")
                    scan_id = parts[2] if len(parts) >= 3 else key
                    scans.append({
                        "scan_id": scan_id,
                        "status": data.get("status", "running"),
                        "ts": float(data.get("ts", 0) or 0),
                        "last_active": float(data.get("last_active", 0) or 0),
                        "target": data.get("target"),
                        "scan_type": data.get("scan_type"),
                    })
                return scans
            except Exception as e:
                logger.warning("Redis active_scans failed, using memory: %s", e)
        for scan_id, st in self._memory_status.items():
            if st.get("status") in terminal:
                continue
            scans.append({
                "scan_id": scan_id,
                "status": st.get("status", "running"),
                "ts": float(st.get("ts", 0) or 0),
                "last_active": float(st.get("last_active", 0) or 0),
                "target": st.get("target"),
                "scan_type": st.get("scan_type"),
            })
        return scans


_bus: Optional[ScanProgressBus] = None


def get_progress_bus() -> ScanProgressBus:
    global _bus
    if _bus is None:
        _bus = ScanProgressBus()
    return _bus


async def publish_scan_event(
    scan_id: str,
    event_type: str,
    data: Dict[str, Any] = None,
) -> None:
    try:
        await get_progress_bus().publish(scan_id, event_type, data)
    except Exception as e:
        logger.warning("publish_scan_event failed: %s", e)
