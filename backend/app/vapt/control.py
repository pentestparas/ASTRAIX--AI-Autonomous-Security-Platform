"""
Scan Control Channel

In-process control plane for active scans: pause, resume, stop and
cooperative checkpoints. The orchestrator and recon engine call
``checkpoint(scan_id)`` at phase and tool boundaries; a paused scan
blocks at the next checkpoint until resumed, and a stopped scan raises
``ScanStoppedError`` so callers can mark the assessment as stopped.
"""

import asyncio
from typing import Any, Dict, Optional

from app.core.logging import get_logger
from app.vapt.progress import get_progress_bus, publish_scan_event

logger = get_logger(__name__)


class ScanStoppedError(Exception):
    """Raised at a checkpoint when the scan was stopped by the user."""

    def __init__(self, scan_id: str):
        super().__init__(f"Scan {scan_id} stopped by user")
        self.scan_id = scan_id


class ScanController:
    """Registry + control flags for scans currently executing in-process."""

    def __init__(self) -> None:
        self._tasks: Dict[str, asyncio.Task] = {}
        self._state: Dict[str, Dict[str, Any]] = {}
        self._meta: Dict[str, Dict[str, Any]] = {}

    def register(
        self,
        scan_id: str,
        task: Optional[asyncio.Task] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Track a running scan so control endpoints can reach its task."""
        self._tasks[scan_id] = task or asyncio.current_task()
        st = self._state.setdefault(scan_id, {})
        st["paused"] = False
        st["stop_requested"] = False
        st["paused_event_sent"] = False
        if meta:
            self._meta[scan_id] = meta

    def finish(self, scan_id: str) -> None:
        """Drop runtime state when the scan ends (meta is kept for restart)."""
        self._tasks.pop(scan_id, None)
        self._state.pop(scan_id, None)

    def is_active(self, scan_id: str) -> bool:
        return scan_id in self._tasks

    def status(self, scan_id: str) -> Optional[str]:
        st = self._state.get(scan_id)
        if not st:
            return None
        if st.get("stop_requested"):
            return "stopping"
        return "paused" if st.get("paused") else "running"

    def meta(self, scan_id: str) -> Optional[Dict[str, Any]]:
        return self._meta.get(scan_id)

    async def checkpoint(self, scan_id: str) -> None:
        """Cooperative pause/stop gate.

        No-op for scans that are not registered. While paused, blocks at
        the checkpoint (publishing scan_paused once) until resumed or
        stopped; raises ScanStoppedError when the scan was stopped.
        """
        st = self._state.get(scan_id)
        if not st:
            return
        if st.get("stop_requested"):
            raise ScanStoppedError(scan_id)
        while st.get("paused"):
            if not st.get("paused_event_sent"):
                st["paused_event_sent"] = True
                await publish_scan_event(scan_id, "scan_paused", {
                    "message": "Scan paused by user",
                })
                await get_progress_bus().set_status(scan_id, "paused")
                logger.info("scan.paused", scan_id=scan_id)
            await asyncio.sleep(1)
            if st.get("stop_requested"):
                raise ScanStoppedError(scan_id)
        if st.get("paused_event_sent"):
            st["paused_event_sent"] = False
            await publish_scan_event(scan_id, "scan_resumed", {
                "message": "Scan resumed",
            })
            await get_progress_bus().set_status(scan_id, "running")
            logger.info("scan.resumed", scan_id=scan_id)

    def pause(self, scan_id: str) -> bool:
        st = self._state.get(scan_id)
        if not st or not self.is_active(scan_id) or st.get("stop_requested"):
            return False
        st["paused"] = True
        logger.info("scan.pause_requested", scan_id=scan_id)
        return True

    def resume(self, scan_id: str) -> bool:
        st = self._state.get(scan_id)
        if not st or st.get("stop_requested"):
            return False
        st["paused"] = False
        logger.info("scan.resume_requested", scan_id=scan_id)
        return True

    async def stop(self, scan_id: str) -> bool:
        st = self._state.get(scan_id)
        task = self._tasks.get(scan_id)
        if not st or task is None:
            return False
        st["stop_requested"] = True
        st["paused"] = False
        logger.info("scan.stop_requested", scan_id=scan_id)
        task.cancel()
        return True


_controller: Optional[ScanController] = None


def get_scan_controller() -> ScanController:
    global _controller
    if _controller is None:
        _controller = ScanController()
    return _controller