from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session
from app.api.v1.assessments import router as assessments_router
from app.api.v1.assets import router as assets_router
from app.api.v1.findings import router as findings_router
from app.api.v1.plugins import router as plugins_router
from app.api.v1.reports import router as reports_router
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
    return {"status": "healthy"}


@api_router.get("/ready")
async def ready():
    return {"status": "ready"}


@api_router.get("/capabilities")
async def list_capabilities():
    """List available security scan capabilities."""
    return {
        "success": True,
        "data": [
            {"id": "network_vapt", "name": "Network VAPT", "status": "available"},
            {"id": "web_vapt", "name": "Web Application VAPT", "status": "available"},
            {"id": "cloud_posture", "name": "Cloud Configuration Audit", "status": "available"},
            {"id": "code_audit", "name": "Code Security Audit", "status": "available"},
        ]
    }


@api_router.get("/dashboard/stats")
async def get_dashboard_stats(organization_id: UUID = None):
    """Get dashboard statistics for an organization."""
    if not organization_id:
        return {
            "total_projects": 0,
            "active_scans": 0,
            "critical_findings": 0,
            "open_findings": 0,
            "resolved_findings": 0,
            "assets_discovered": 0,
            "total_findings": 0,
        }
    return {
        "total_projects": 1,
        "active_scans": 0,
        "critical_findings": 0,
        "open_findings": 0,
        "resolved_findings": 0,
        "assets_discovered": 0,
        "total_findings": 0,
    }


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
    proj_id_str = config.get("project_id")

    if not org_id_str or not proj_id_str:
        raise HTTPException(status_code=400, detail="organization_id and project_id are required")

    try:
        organization_id = UUIDType(org_id_str) if isinstance(org_id_str, str) else org_id_str
        project_id = UUIDType(proj_id_str) if isinstance(proj_id_str, str) else proj_id_str
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid organization_id or project_id format")

    asset_uuid = uuid4()
    assessment_uuid = uuid4()

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

    return {
        "id": str(assessment_uuid),
        "name": f"Scan of {target}",
        "type": capability_id,
        "status": "pending",
        "target": target,
        "organization_id": str(organization_id),
        "project_id": str(project_id),
        "asset": {"id": str(asset_uuid), "name": target},
        "findings_count": 0,
        "started_at": None,
    }


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