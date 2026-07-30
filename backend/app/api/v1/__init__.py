from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session
from app.schemas.base import ResponseSchema
from app.api.v1.assessments import router as assessments_router
from app.api.v1.assets import router as assets_router
from app.api.v1.findings import router as findings_router
from app.api.v1.plugins import router as plugins_router
from app.api.v1.reports import router as reports_router
from app.api.v1.graph import router as graph_router
from app.api.v1.knowledge import router as knowledge_router
from app.api.v1.auth import router as auth_router
from app.vapt.routes import router as vapt_router
from app.api.v1.organizations import (
    org_router,
    project_router,
    membership_router,
    apikey_router,
)

api_router = APIRouter()


@api_router.get("/health")
async def ping():
    from app.config import get_settings
    s = get_settings()
    return {"status": "healthy", "service": s.APP_NAME, "version": s.APP_VERSION}


@api_router.get("/ready")
async def ready():
    return {"status": "ready"}


@api_router.get("/capabilities")
async def list_capabilities():
    """List available security scan capabilities."""
    return {
        "success": True,
        "data": [
            {"capability": "network_vapt", "name": "Network VAPT", "status": "available"},
            {"capability": "web_vapt", "name": "Web Application VAPT", "status": "available"},
            {"capability": "cloud_posture", "name": "Cloud Configuration Audit", "status": "available"},
            {"capability": "code_audit", "name": "Code Security Audit", "status": "available"},
        ]
    }


@api_router.get("/dashboard/activity")
async def get_dashboard_activity(organization_id: UUID = None, limit: int = 10):
    """Get recent activity for dashboard."""
    return []


@api_router.get("/dashboard/stats")
async def get_dashboard_stats(organization_id: UUID = None):
    """Get dashboard statistics for an organization."""
    base = {
        "total_projects": 0,
        "active_scans": 0,
        "critical_findings": 0,
        "high_findings": 0,
        "medium_findings": 0,
        "low_findings": 0,
        "open_findings": 0,
        "resolved_findings": 0,
        "assets_discovered": 0,
        "total_findings": 0,
        "scans_this_week": 0,
        "scans_this_month": 0,
    }
    if not organization_id:
        return base

    try:
        from app.repositories import finding_repo, assessment_repo, asset_repo
        from app.database.session import async_session_maker
        async with async_session_maker() as session:
            findings = await finding_repo.count(session, organization_id=str(organization_id))
            assessments = await assessment_repo.count(session, organization_id=str(organization_id))
            assets = await asset_repo.count(session, organization_id=str(organization_id))
            critical = await finding_repo.count(session, organization_id=str(organization_id), severity="critical")
            high = await finding_repo.count(session, organization_id=str(organization_id), severity="high")
            medium = await finding_repo.count(session, organization_id=str(organization_id), severity="medium")
            low = await finding_repo.count(session, organization_id=str(organization_id), severity="low")
            open_f = await finding_repo.count(session, organization_id=str(organization_id), status="open")
            resolved = await finding_repo.count(session, organization_id=str(organization_id), status="resolved")

            return {
                "total_projects": 0,
                "active_scans": 0,
                "critical_findings": critical,
                "high_findings": high,
                "medium_findings": medium,
                "low_findings": low,
                "open_findings": open_f,
                "resolved_findings": resolved,
                "assets_discovered": assets,
                "total_findings": findings,
                "scans_this_week": 0,
                "scans_this_month": assessments,
            }
    except Exception:
        return base


@api_router.post("/assess")
async def run_assessment(data: dict, session: AsyncSession = Depends(get_session)):
    """Run a security assessment scan."""
    from uuid import uuid4, UUID as UUIDType
    from datetime import datetime
    from app.domain.models.asset import Asset
    from app.domain.models.assessment import Assessment

    target = data.get("target", "")
    capability_id = data.get("capability_id", "web_vapt")
    config = data.get("config", {})
    org_id_str = config.get("organization_id")

    if not org_id_str:
        raise HTTPException(status_code=400, detail="organization_id is required")

    proj_id_str = config.get("project_id")

    try:
        organization_id = UUIDType(org_id_str) if isinstance(org_id_str, str) else org_id_str
        project_id = UUIDType(proj_id_str) if isinstance(proj_id_str, str) and proj_id_str else None
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid organization_id or project_id format")

    asset_uuid = uuid4()
    assessment_uuid = uuid4()
    correlation_id = str(uuid4())

    asset = Asset(
        id=asset_uuid,
        organization_id=organization_id,
        project_id=project_id,
        name=target,
        type=capability_id,
        identifier=target,
        criticality="medium",
        tags=[],
        metadata_json={},
    )
    session.add(asset)

    assessment = Assessment(
        id=assessment_uuid,
        organization_id=organization_id,
        project_id=project_id,
        asset_id=asset_uuid,
        status="pending",
        type=capability_id,
        config=config,
        findings_count=0,
    )
    session.add(assessment)
    await session.flush()

    return ResponseSchema(
        data={
            "assessment_id": str(assessment_uuid),
            "correlation_id": correlation_id,
            "capability": capability_id,
            "status": "pending",
            "finding_count": 0,
            "findings": [],
            "risk_score_min": 0,
            "risk_score_max": 0,
            "risk_score_avg": 0,
        }
    )


api_router.include_router(auth_router, tags=["Authentication"])
api_router.include_router(org_router, tags=["Organizations"])
api_router.include_router(project_router, tags=["Projects"])
api_router.include_router(membership_router, tags=["Memberships"])
api_router.include_router(apikey_router, tags=["API Keys"])
api_router.include_router(assessments_router, prefix="/assessments", tags=["Assessments"])
api_router.include_router(assets_router, prefix="/assets", tags=["Assets"])
api_router.include_router(findings_router, prefix="/findings", tags=["Findings"])
api_router.include_router(plugins_router, prefix="/plugins", tags=["Plugins"])
api_router.include_router(reports_router, prefix="/reports", tags=["Reports"])
api_router.include_router(vapt_router, prefix="/vapt", tags=["VAPT"])
api_router.include_router(graph_router, tags=["Attack Surface Graph"])
api_router.include_router(knowledge_router, tags=["Knowledge Base"])