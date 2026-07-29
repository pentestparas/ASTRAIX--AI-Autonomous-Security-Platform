import uuid as uuid_lib
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database.session import get_session
from app.repositories import assessment_repo, finding_repo
from app.schemas.base import ResponseSchema
from app.domain.models.assessment import Assessment as AssessmentModel
from app.domain.models.finding import Finding as FindingModel
from app.core.logging import get_logger
from ai_secos_core.report_engine.engine import NullReportEngine
from ai_secos_core.report_engine.types import (
    ReportRequest,
    ReportTemplate,
    ReportFormat,
)
from ai_secos_core.shared.value_objects import SecurityFinding, Severity

logger = get_logger(__name__)
router = APIRouter()

TEMPLATES = {
    "executive": ReportTemplate(
        id="executive",
        version="1.0",
        description="Executive Summary - high-level overview for leadership",
        section_order=("summary",),
        requires_ai_comment=True,
    ),
    "technical": ReportTemplate(
        id="technical",
        version="1.0",
        description="Technical Report - detailed findings and remediation",
        section_order=("summary", "findings"),
        requires_ai_comment=False,
    ),
    "compliance": ReportTemplate(
        id="compliance",
        version="1.0",
        description="Compliance Report - audit-ready documentation",
        section_order=("summary", "findings", "ai_comment"),
        requires_ai_comment=True,
    ),
}

FORMAT_MAP = {
    "json": ReportFormat.JSON,
    "html": ReportFormat.MARKDOWN,
    "pdf": ReportFormat.MARKDOWN,
}


def _finding_to_security_finding(f: FindingModel) -> SecurityFinding:
    import re
    asset = f.asset.name.lower() if hasattr(f, 'asset') and f.asset else "unknown"
    asset = re.sub(r'[^a-z0-9_]', '_', asset)
    return SecurityFinding(
        id=uuid_lib.UUID(f.id) if isinstance(f.id, str) else f.id,
        assessment_id=str(f.assessment_id),
        asset=asset,
        capability="vapt",
        plugin=f.plugin_id,
        title=f.title,
        description=f.description or "",
        severity=Severity(f.severity.lower()) if f.severity else Severity.INFO,
        confidence=1.0,
        remediation=f.remediation or "",
        cvss=f.cvss_score,
        fingerprint=str(f.id),
    )


class GenerateReportRequest(BaseModel):
    assessment_id: str
    template: str = "executive"
    format: str = "json"


@router.post("/generate")
async def generate_report(
    body: GenerateReportRequest,
    db: AsyncSession = Depends(get_session),
):
    assessment = await assessment_repo.get(db, body.assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    findings = await finding_repo.list(db, assessment_id=body.assessment_id)

    tmpl = TEMPLATES.get(body.template)
    if not tmpl:
        raise HTTPException(status_code=400, detail=f"Unknown template: {body.template}")

    fmt = FORMAT_MAP.get(body.format, ReportFormat.JSON)

    sec_findings = [_finding_to_security_finding(f) for f in findings]

    request = ReportRequest(
        template=tmpl,
        findings=sec_findings,
        correlation_id=body.assessment_id,
    )

    engine = NullReportEngine()
    artifacts = await engine.render(request, formats=(fmt,))

    if not artifacts:
        raise HTTPException(status_code=500, detail="Report generation failed")

    artifact = artifacts[0]

    report_content = artifact.serialize()
    ext = "json" if body.format == "json" else "md"
    filename = f"report_{body.assessment_id[:8]}_{body.template}.{ext}"
    return ResponseSchema(
        data={
            "download_url": None,
            "report": report_content,
            "filename": filename,
            "title": artifact.title,
            "format": artifact.format.value,
            "assessment_id": body.assessment_id,
            "findings_count": len(findings),
        }
    )


@router.get("/templates")
async def list_templates():
    return ResponseSchema(
        data=[
            {"id": tid, "name": t.description.split(" - ")[0], "description": t.description}
            for tid, t in TEMPLATES.items()
        ]
    )


@router.get("")
async def list_reports(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=200),
    db: AsyncSession = Depends(get_session),
):
    items = await assessment_repo.list(db, skip=(page - 1) * limit, limit=limit)
    return ResponseSchema(
        data={
            "items": [
                {
                    "id": str(a.id),
                    "assessment_id": str(a.id),
                    "template": "executive",
                    "created_at": str(a.created_at),
                }
                for a in items if a.status == "completed"
            ],
            "total": len(items),
            "page": page,
            "page_size": limit,
        }
    )
