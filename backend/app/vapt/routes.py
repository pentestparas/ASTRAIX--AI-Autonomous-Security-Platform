"""
VAPT API Routes

Fast API endpoints for VAPT operations with database persistence.
"""

from datetime import datetime
from sqlalchemy import select
from typing import Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.core.auth import get_current_active_user
from app.domain.models.organization import User
from app.vapt.models import VAPTScanType, VAPTTarget
from app.vapt.orchestrator import get_vapt_orchestrator
from app.vapt.progress import get_progress_bus
from app.vapt.tools import check_tool_availability, get_available_tools, TOOLS_REGISTRY
from app.core.logging import get_logger
from app.domain.models.asset import Asset
from app.domain.models.assessment import Assessment
from app.domain.models.finding import Finding
from app.repositories import asset_repo, assessment_repo, finding_repo

logger = get_logger(__name__)
router = APIRouter(tags=["VAPT"])


class ScanRequest(BaseModel):
    target: str
    scan_type: str = "auto"
    tools: list[str] = []
    deep: bool = False
    organization_id: Optional[str] = None
    project_id: Optional[str] = None
    client_scan_id: Optional[str] = None


class ScanResponse(BaseModel):
    scan_id: str
    assessment_id: Optional[str] = None
    status: str
    target: str
    findings_count: int
    findings: list = []
    severity_breakdown: dict
    insights: dict


class ToolStatusResponse(BaseModel):
    tools: dict
    available: list
    total_installed: int


@router.post("/scan", response_model=ScanResponse)
async def run_scan(
    request: ScanRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> ScanResponse:
    """
    Run a VAPT scan on target with database persistence.

    - **target**: IP, URL, domain, or hostname
    - **scan_type**: auto, network, web, api, ssl, full
    - **tools**: specific tool IDs (empty = auto-select)
    - **deep**: enable deep scanning mode
    - **organization_id**: UUID of the organization (required for persistence)
    - **project_id**: UUID of the project (required for persistence)
    """
    orchestrator = get_vapt_orchestrator()

    logger.info(f"Starting VAPT scan on {request.target}")

    scan_id = None
    if request.client_scan_id:
        try:
            scan_id = str(UUID(request.client_scan_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid client_scan_id format")

    result = await orchestrator.analyze_and_scan(
        target=request.target,
        scan_type=request.scan_type,
        scan_id=scan_id,
    )

    insights = orchestrator.generate_insights(result)

    assessment_id = None
    org_id = None
    proj_id = None

    if request.organization_id and request.project_id:
        try:
            org_id = request.organization_id
            proj_id = request.project_id

            asset_uuid = uuid4()
            assessment_uuid = uuid4()

            existing_asset = await session.execute(
                select(Asset).where(
                    Asset.identifier == request.target,
                    Asset.type == "vapt"
                ).limit(1)
            )
            existing_asset = existing_asset.scalar_one_or_none()

            if existing_asset:
                asset_uuid = existing_asset.id
            else:
                asset = Asset(
                    id=str(asset_uuid),
                    organization_id=str(org_id),
                    project_id=str(proj_id),
                    name=request.target,
                    type="vapt",
                    identifier=request.target,
                    criticality="medium",
                    tags=[],
                    metadata_json={"scan_type": request.scan_type},
                )
                session.add(asset)

            assessment = Assessment(
                id=str(assessment_uuid),
                organization_id=str(org_id),
                project_id=str(proj_id),
                asset_id=str(asset_uuid),
                status=result.status,
                type="vapt",
                config={"scan_type": request.scan_type, "tools": request.tools},
                started_at=result.started_at,
                completed_at=result.completed_at,
                findings_count=len(result.findings),
            )
            session.add(assessment)

            for finding in result.findings:
                fingerprint = f"{finding.title}:{request.target}:{finding.severity.value}"

                existing_finding = await session.execute(
                    select(Finding).where(Finding.fingerprint == fingerprint[:64]).limit(1)
                )
                existing_finding = existing_finding.scalar_one_or_none()
                if existing_finding:
                    continue

                domain_finding = Finding(
                    id=str(uuid4()),
                    organization_id=str(org_id),
                    project_id=str(proj_id),
                    asset_id=str(asset_uuid),
                    assessment_id=str(assessment_uuid),
                    plugin_id=f"vapt/{finding.tool_name}",
                    severity=finding.severity.value,
                    title=finding.title,
                    description=finding.description,
                    details=finding.details or {},
                    cvss_score=finding.cvss_score,
                    remediation=finding.remediation or "",
                    reference=finding.reference or "",
                    fingerprint=fingerprint[:64],
                    status="open",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                session.add(domain_finding)

            await session.commit()
            assessment_id = str(assessment_uuid)
            logger.info(f"VAPT scan persisted: {assessment_id}")

        except Exception as e:
            logger.error(f"Failed to persist VAPT scan: {e}")
            await session.rollback()

    return ScanResponse(
        scan_id=str(result.id),
        assessment_id=assessment_id,
        status=result.status,
        target=request.target,
        findings_count=len(result.findings),
        findings=[f.to_dict() for f in result.findings],
        severity_breakdown=insights["severity_breakdown"],
        insights=insights,
    )


@router.get("/tools")
async def list_tools() -> ToolStatusResponse:
    """Get status of all VAPT tools."""
    all_tools = {tid: {"name": t.name, "description": t.description, "category": t.category.value} for tid, t in TOOLS_REGISTRY.items()}
    available = get_available_tools()
    installed = check_tool_availability()

    return ToolStatusResponse(
        tools={tid: {"installed": installed.get(tid, False)} for tid in TOOLS_REGISTRY},
        available=available,
        total_installed=len(available),
    )


@router.get("/tools/health")
async def tools_health():
    """Check VAPT tools health."""
    available = get_available_tools()
    return {
        "status": "healthy" if len(available) > 0 else "degraded",
        "tools_available": len(available),
        "missing_tools": [tid for tid in TOOLS_REGISTRY if tid not in available],
    }


@router.post("/scan/quick")
async def quick_scan(
    request: ScanRequest,
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """Quick scan with essential tools (no persistence)."""
    orchestrator = get_vapt_orchestrator()
    scan_id = str(uuid4())
    result = await orchestrator.analyze_and_scan(request.target, request.scan_type or "auto", scan_id=scan_id)
    return {
        "scan_id": str(result.id),
        "target": request.target,
        "status": result.status,
        "findings": [f.to_dict() for f in result.findings],
        "duration": result.duration,
    }


@router.get("/scan/{scan_id}/progress")
async def get_scan_progress(
    scan_id: str,
    since: int = Query(0, ge=0, description="Event index to fetch from"),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """Get live scan progress events since an index."""
    bus = get_progress_bus()
    events, total = await bus.events(scan_id, since=since)
    status = await bus.status(scan_id)
    return {
        "scan_id": scan_id,
        "events": events,
        "total": total,
        "status": status or {"status": "running"},
    }


@router.get("/assessments/{assessment_id}")
async def get_assessment(assessment_id: UUID, session: AsyncSession = Depends(get_session)):
    """Get assessment details with findings."""
    from app.repositories import assessment_repo, finding_repo

    assessment = await assessment_repo.get(session, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    findings = await finding_repo.list(session, assessment_id=assessment_id)
    return {
        "assessment": {
            "id": str(assessment.id),
            "status": assessment.status,
            "type": assessment.type,
            "findings_count": assessment.findings_count,
            "started_at": assessment.started_at.isoformat() if assessment.started_at else None,
            "completed_at": assessment.completed_at.isoformat() if assessment.completed_at else None,
        },
        "findings": [
            {
                "id": str(f.id),
                "title": f.title,
                "severity": f.severity,
                "status": f.status,
                "description": f.description,
            }
            for f in findings
        ],
    }