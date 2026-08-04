from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from datetime import datetime
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


@api_router.get("/system/status")
async def system_status():
    """Real component health: postgres, redis, neo4j, docker/Kali, KB."""
    from app.core.logging import get_logger
    logger = get_logger(__name__)
    components = {}

    # Postgres
    try:
        from app.database.session import async_session_maker
        from sqlalchemy import text
        async with async_session_maker() as session:
            await session.execute(text("SELECT 1"))
        components["postgres"] = {"status": "operational", "details": "connected"}
    except Exception as e:
        components["postgres"] = {"status": "down", "details": str(e)[:200]}

    # Redis
    try:
        from app.vapt.progress import get_progress_bus
        bus = get_progress_bus()
        if hasattr(bus, "_redis") and bus._redis is not None:
            await bus._redis.ping()
            components["redis"] = {"status": "operational", "details": "connected"}
        else:
            components["redis"] = {"status": "operational", "details": "in-memory fallback (no redis configured)"}
    except Exception as e:
        components["redis"] = {"status": "degraded", "details": str(e)[:200]}

    # Neo4j knowledge graph
    try:
        from app.recon_orchestrator.graph_db import get_knowledge_graph
        graph = get_knowledge_graph()
        if graph._enabled:
            components["neo4j"] = {"status": "operational", "details": "knowledge graph connected"}
        else:
            components["neo4j"] = {"status": "unavailable", "details": "knowledge graph disabled"}
    except Exception as e:
        components["neo4j"] = {"status": "unavailable", "details": str(e)[:200]}

    # Docker + Kali image
    try:
        from app.vapt.tools import check_tool_availability
        from app.vapt.executor import VAPTExecutor
        import subprocess
        availability = check_tool_availability()
        image_check = subprocess.run(
            ["docker", "image", "inspect", VAPTExecutor.KALI_IMAGE],
            capture_output=True, timeout=10,
        )
        kali_ok = image_check.returncode == 0
        components["docker"] = {
            "status": "operational" if kali_ok or availability else "degraded",
            "details": {
                "kali_image_available": kali_ok,
                "tools": {k: bool(v) for k, v in availability.items()},
            },
        }
    except Exception as e:
        components["docker"] = {"status": "down", "details": str(e)[:200]}

    # Knowledge base
    try:
        from app.api.v1 import knowledge as kb_mod
        if getattr(kb_mod, "_loaded", False) and kb_mod._kb is not None:
            stats = kb_mod._kb.stats()
            components["knowledge_base"] = {
                "status": "operational",
                "details": {
                    "chunks": stats.get("total_chunks", stats.get("chunks", 0)),
                    "sources": stats.get("total_sources", stats.get("sources", 0)),
                    "vocab_size": stats.get("vocab_size", 0),
                    "semantic_search": stats.get("semantic_search", False),
                },
            }
        else:
            components["knowledge_base"] = {"status": "unavailable", "details": "not loaded"}
    except Exception as e:
        components["knowledge_base"] = {"status": "unavailable", "details": str(e)[:200]}

    all_ok = all(c.get("status") == "operational" for c in components.values())
    return {
        "success": True,
        "status": "operational" if all_ok else "degraded",
        "components": components,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


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
        return ResponseSchema(data=base)

    try:
        from app.repositories import finding_repo, assessment_repo, asset_repo
        from app.domain.models.organization import Project as ProjectModel
        from app.domain.models.assessment import Assessment as AssessmentModel
        from app.vapt.progress import get_progress_bus
        from sqlalchemy import func, select
        from datetime import datetime, timedelta
        from app.database.session import async_session_maker
        async with async_session_maker() as session:
            findings = await finding_repo.count(session, organization_id=str(organization_id))
            assessments = await assessment_repo.count(session, organization_id=str(organization_id))
            assets = await asset_repo.count(session, organization_id=str(organization_id))
            projects = await session.execute(
                select(func.count()).select_from(ProjectModel).where(
                    ProjectModel.organization_id == str(organization_id)
                )
            )
            total_projects = projects.scalar_one()
            critical = await finding_repo.count(session, organization_id=str(organization_id), severity="critical")
            high = await finding_repo.count(session, organization_id=str(organization_id), severity="high")
            medium = await finding_repo.count(session, organization_id=str(organization_id), severity="medium")
            low = await finding_repo.count(session, organization_id=str(organization_id), severity="low")
            open_f = await finding_repo.count(session, organization_id=str(organization_id), status="open")
            resolved = await finding_repo.count(session, organization_id=str(organization_id), status="resolved")

            now = datetime.utcnow()
            week_ago = now - timedelta(days=7)
            month_ago = now - timedelta(days=30)
            async def period_count(since):
                return (await session.execute(
                    select(func.count()).select_from(AssessmentModel).where(
                        AssessmentModel.organization_id == str(organization_id),
                        AssessmentModel.started_at >= since,
                    )
                )).scalar_one()
            scans_week = await period_count(week_ago)
            scans_month = await period_count(month_ago)

            active_scans = len(await get_progress_bus().active_scans())

            return ResponseSchema(
                data={
                    "total_projects": total_projects,
                    "active_scans": active_scans,
                    "critical_findings": critical,
                    "high_findings": high,
                    "medium_findings": medium,
                    "low_findings": low,
                    "open_findings": open_f,
                    "resolved_findings": resolved,
                    "assets_discovered": assets,
                    "total_findings": findings,
                    "scans_this_week": scans_week,
                    "scans_this_month": scans_month,
                }
            )
    except Exception:
        return ResponseSchema(data=base)


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