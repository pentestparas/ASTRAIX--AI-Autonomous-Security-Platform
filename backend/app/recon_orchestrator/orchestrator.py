import asyncio
import time
from collections import defaultdict
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from uuid import uuid4

from app.core.logging import get_logger
from app.recon_orchestrator.graph_db import get_knowledge_graph, KnowledgeGraph
from app.vapt.control import get_scan_controller
from app.vapt.executor import VAPTExecutor
from app.vapt.models import (
    VAPTFinding,
    VAPTScanRequest,
    VAPTScanResult,
    VAPTSeverity,
    VAPTTool,
)
from app.vapt.tools import get_tool, get_tools_for_scan_type

logger = get_logger(__name__)

TOOL_PHASES: Dict[str, List[str]] = {
    "recon": ["nmap"],
    "web": ["nikto", "nuclei", "gobuster"],
    "deep": ["sqlmap", "sslscan"],
}

PHASE_ORDER = ["recon", "web", "deep"]


class ReconOrchestrator:
    def __init__(self, executor: VAPTExecutor):
        self._executor = executor
        self._graph: KnowledgeGraph = get_knowledge_graph()
        self._publish: Optional[Callable[[str, str, dict], Any]] = None

    def set_progress_publisher(self, publish: Callable[[str, str, dict], Any]) -> None:
        """Attach a callback for live progress events (scan_id, event_type, data)."""
        self._publish = publish

    async def _emit(self, scan_id: str, event_type: str, data: dict = None) -> None:
        if self._publish:
            try:
                await self._publish(scan_id, event_type, data or {})
            except Exception as e:
                logger.warning("progress publish failed: %s", e)

    async def execute_scan(self, request: VAPTScanRequest, scan_id: Optional[str] = None) -> VAPTScanResult:
        result = VAPTScanResult(request=request, status="running", started_at=datetime.utcnow())
        if scan_id:
            from uuid import UUID as _UUID
            result.id = _UUID(scan_id)

        tools = self._resolve_tools(request)
        result.tool_results = {t: {"status": "queued"} for t in tools}

        target_id = request.target.value
        await self._graph.upsert_target(
            target_id=target_id,
            name=target_id,
            scan_id=str(result.id),
            scan_type=request.scan_type.value if request.scan_type else "",
        )

        phases = self._assign_phases(tools)
        all_findings: List[VAPTFinding] = []

        for phase_name in PHASE_ORDER:
            phase_tools = phases.get(phase_name, [])
            if not phase_tools:
                continue

            # Pause / stop gate: engages between phases so an in-flight
            # docker tool is allowed to finish before the scan blocks.
            await get_scan_controller().checkpoint(str(result.id))

            logger.info("Orchestrator phase=%s tools=%s", phase_name, phase_tools)
            await self._emit(str(result.id), "phase_started", {
                "phase": phase_name,
                "tools": phase_tools,
            })

            phase_results = await asyncio.gather(
                *[
                    self._run_tool_phase(tool_id, request, result, str(result.id))
                    for tool_id in phase_tools
                ],
                return_exceptions=True,
            )

            for r in phase_results:
                if isinstance(r, BaseException):
                    result.errors.append(f"phase:{phase_name} error={r}")
                elif isinstance(r, list):
                    all_findings.extend(r)
                    for f in r:
                        result.add_finding(f)
                        await self._emit(str(result.id), "finding_found", f.to_dict())
                        await self._write_finding_to_graph(target_id, f, str(result.id))

            await self._emit(str(result.id), "phase_completed", {
                "phase": phase_name,
                "findings": len(all_findings),
            })

        if result.findings:
            result.status = "completed"
            result.message = f"Found {len(result.findings)} vulnerabilities across {len(tools)} tools"
        else:
            result.status = "completed"
            result.message = "Scan completed, no vulnerabilities found"

        result.finalize(result.status, result.message)
        await self._emit(str(result.id), "scan_completed", {
            "status": result.status,
            "findings_count": len(result.findings),
            "duration": result.duration,
            "message": result.message,
        })
        return result

    async def _run_tool_phase(self, tool_id: str, request: VAPTScanRequest, result: VAPTScanResult, scan_id: str) -> list:
        tool = get_tool(tool_id)
        if not tool:
            return []

        target = request.target.value
        if tool.requires_url and not target.startswith(("http://", "https://")):
            target = f"http://{target}"

        cmd = self._executor._build_docker_command(tool, target, quick=getattr(request, "quick", False))
        if not cmd:
            await self._emit(scan_id, "tool_failed", {"tool": tool_id, "reason": "no command"})
            return []

        self._executor._check_rate_limit(tool_id)

        container_name = f"astraix-vapt-{uuid4().hex[:8]}"
        await self._emit(scan_id, "tool_started", {
            "tool": tool_id,
            "name": tool.name,
            "description": tool.description,
            "command": cmd,
        })
        output = ""
        started = time.time()
        try:
            task = asyncio.ensure_future(
                asyncio.to_thread(
                    self._executor._run_container_sync,
                    self._executor.KALI_IMAGE,
                    cmd,
                    container_name,
                    tool.timeout,
                )
            )
            while True:
                try:
                    output = await asyncio.wait_for(asyncio.shield(task), timeout=30)
                    if not isinstance(output, str):
                        output = str(output)
                    break
                except asyncio.TimeoutError:
                    await self._emit(scan_id, "tool_ping", {
                        "tool": tool_id,
                        "name": tool.name,
                        "elapsed": round(time.time() - started, 1),
                    })

            duration = round(time.time() - started, 1)
            result.tool_results[tool_id] = {
                "duration": duration,
                "return_code": 0,
                "success": True,
            }

            findings = self._executor._parse_output(output, tool, request.target.value)
            await self._emit(scan_id, "tool_finished", {
                "tool": tool_id,
                "name": tool.name,
                "duration": duration,
                "findings_count": len(findings),
            })
            for f in findings:
                result.add_finding(f)
                await self._emit(scan_id, "finding_found", f.to_dict())
            return findings

        except asyncio.TimeoutError:
            self._executor._kill_container(container_name)
            result.errors.append(f"{tool_id}: timeout")
            await self._emit(scan_id, "tool_failed", {"tool": tool_id, "reason": "timeout"})
        except Exception as e:
            result.errors.append(f"{tool_id}: {str(e)}")
            await self._emit(scan_id, "tool_failed", {"tool": tool_id, "reason": str(e)})
        return []

    async def _write_finding_to_graph(self, target_id: str, finding: VAPTFinding, scan_id: str) -> None:
        port_id = ""
        if finding.port:
            port_id = await self._graph.upsert_port(
                target_id=target_id,
                port=finding.port,
                protocol=finding.protocol or "tcp",
                state="open",
            )

        service_id = ""
        if finding.service:
            service_id = await self._graph.upsert_service(
                port_id=port_id or target_id,
                name=finding.service,
                version="",
            )

        await self._graph.add_finding(
            target_id=target_id,
            title=finding.title,
            severity=finding.severity.value,
            description=finding.description,
            remediation=finding.remediation or "",
            tool_name=finding.tool_name or "",
            port_id=port_id,
            service_id=service_id,
        )

    def _resolve_tools(self, request: VAPTScanRequest) -> List[str]:
        if request.tools:
            return request.tools
        return get_tools_for_scan_type(request.scan_type)

    def _assign_phases(self, tools: List[str]) -> Dict[str, List[str]]:
        assigned: Dict[str, List[str]] = defaultdict(list)
        for t in tools:
            placed = False
            for phase, phase_tools in TOOL_PHASES.items():
                if t in phase_tools:
                    assigned[phase].append(t)
                    placed = True
                    break
            if not placed:
                assigned["recon"].append(t)
        return assigned
