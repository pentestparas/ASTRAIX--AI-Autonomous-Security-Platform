"""
Scan Control Channel

In-process control plane for active scans: pause, resume, stop and
cooperative checkpoints. The orchestrator and recon engine call
``checkpoint(scan_id)`` at phase and tool boundaries; a paused scan
blocks at the next checkpoint until resumed, and a stopped scan raises
``ScanStoppedError`` so callers can mark the assessment as stopped.
"""

import asyncio
import os
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from app.core.logging import get_logger
from app.vapt.progress import get_progress_bus, publish_scan_event

logger = get_logger(__name__)


class ScanStoppedError(Exception):
    """Raised at a checkpoint when the scan was stopped by the user."""

    def __init__(self, scan_id: str):
        super().__init__(f"Scan {scan_id} stopped by user")
        self.scan_id = scan_id


@dataclass
class ToolApprovalRequest:
    """A pending operator decision for a dangerous agent tool call."""

    approval_id: str
    scan_id: str
    tool_id: str
    tool_name: str
    args: Dict[str, Any]
    reason: str = ""
    decision: Optional[bool] = None
    created_at: float = field(default_factory=time.time)
    _event: asyncio.Event = field(default_factory=asyncio.Event)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "approval_id": self.approval_id,
            "scan_id": self.scan_id,
            "tool_id": self.tool_id,
            "tool_name": self.tool_name,
            "args": self.args,
            "reason": self.reason,
            "decision": self.decision,
            "created_at": self.created_at,
        }


class ScanController:
    """Registry + control flags for scans currently executing in-process."""

    def __init__(self) -> None:
        self._tasks: Dict[str, asyncio.Task] = {}
        self._state: Dict[str, Dict[str, Any]] = {}
        self._meta: Dict[str, Dict[str, Any]] = {}
        self._approvals: Dict[str, Dict[str, ToolApprovalRequest]] = {}

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
        self._approvals.pop(scan_id, None)

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

    def set_agent_partial(
        self, scan_id: str, steps: List[Any], findings: List[Any]
    ) -> None:
        """Store the agent loop's partial results so an aborted/timed-out
        loop can still contribute findings to the final report."""
        st = self._state.setdefault(scan_id, {})
        st["agent_partial"] = (steps, findings)

    def get_agent_partial(self, scan_id: str) -> Optional[Tuple[List[Any], List[Any]]]:
        st = self._state.get(scan_id)
        if not st:
            return None
        return st.get("agent_partial")

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

    # ------------------------------------------------------------------
    # Dangerous-tool approval gate (agent loop)
    # ------------------------------------------------------------------

    async def request_tool_approval(
        self,
        scan_id: str,
        tool_id: str,
        tool_name: str,
        args: Dict[str, Any],
        reason: str = "",
    ) -> str:
        """Register a pending operator decision for a dangerous tool call.

        Autonomous mode (VAPT_AUTO_APPROVE, default ON) settles the approval
        immediately so scans never stall on an invisible prompt. Operators
        can force manual gating by setting VAPT_AUTO_APPROVE=false - the
        approval panel then renders live in the scan console for the
        VAPT_APPROVAL_TIMEOUT window.
        """
        auto = os.environ.get("VAPT_AUTO_APPROVE", "true").lower() not in ("0", "false", "no")
        approval = ToolApprovalRequest(
            approval_id=str(uuid.uuid4().hex[:12]),
            scan_id=scan_id,
            tool_id=tool_id,
            tool_name=tool_name,
            args=args,
            reason=reason,
        )
        self._approvals.setdefault(scan_id, {})[approval.approval_id] = approval
        logger.info(
            "tool.approval_requested",
            scan_id=scan_id, tool=tool_id, approval_id=approval.approval_id,
            auto_approved=auto,
        )
        await publish_scan_event(scan_id, "tool_approval_requested", approval.to_dict())
        if auto:
            approval.decision = True
            approval._event.set()
            logger.info(
                "tool.approval_resolved",
                scan_id=scan_id, approval_id=approval.approval_id, approved=True,
                auto=True,
            )
            await publish_scan_event(
                scan_id,
                "tool_approval_resolved",
                {
                    "approval_id": approval.approval_id,
                    "scan_id": scan_id,
                    "tool_id": tool_id,
                    "tool_name": tool_name,
                    "approved": True,
                    "auto": True,
                },
            )
        return approval.approval_id

    def pending_approvals(self, scan_id: str) -> List[Dict[str, Any]]:
        now = time.time()
        ttl = float(os.environ.get("VAPT_APPROVAL_TIMEOUT", "300"))
        pending = [
            a.to_dict()
            for a in self._approvals.get(scan_id, {}).values()
            if a.decision is None and now - a.created_at < ttl
        ]
        return pending

    async def resolve_approval(self, scan_id: str, approval_id: str, approved: bool) -> bool:
        """Settle a pending approval. Returns False when unknown or already settled."""
        approval = self._approvals.get(scan_id, {}).get(approval_id)
        if not approval or approval.decision is not None:
            return False
        approval.decision = approved
        approval._event.set()
        logger.info(
            "tool.approval_resolved",
            scan_id=scan_id, approval_id=approval_id, approved=approved,
        )
        await publish_scan_event(
            scan_id,
            "tool_approval_resolved",
            {
                "approval_id": approval.approval_id,
                "scan_id": scan_id,
                "tool_id": approval.tool_id,
                "tool_name": approval.tool_name,
                "approved": approved,
            },
        )
        return True

    async def await_approval(
        self,
        scan_id: str,
        approval_id: str,
        timeout: float = 300,
    ) -> Optional[bool]:
        """Wait for the operator's decision. None = timed out / not resolved."""
        approval = self._approvals.get(scan_id, {}).get(approval_id)
        if not approval:
            return None
        st = self._state.get(scan_id, {})
        try:
            while True:
                if st.get("stop_requested"):
                    return None
                done, _ = await asyncio.wait(
                    [asyncio.create_task(approval._event.wait())],
                    timeout=min(timeout, 5),
                )
                if done:
                    return approval.decision
                timeout -= 5
                if timeout <= 0:
                    return None
        except asyncio.CancelledError:
            raise


_controller: Optional[ScanController] = None


def get_scan_controller() -> ScanController:
    global _controller
    if _controller is None:
        _controller = ScanController()
    return _controller