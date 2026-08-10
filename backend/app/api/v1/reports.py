import uuid as uuid_lib
from datetime import datetime, timezone
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
from app.report_engine.engine import Jinja2ReportEngine
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
        version="2.0",
        description="Executive Summary - high-level overview for leadership",
        section_order=("summary",),
        requires_ai_comment=True,
    ),
    "technical": ReportTemplate(
        id="technical",
        version="2.0",
        description="Technical Report - detailed findings and remediation steps",
        section_order=("summary", "findings"),
        requires_ai_comment=False,
    ),
    "compliance": ReportTemplate(
        id="compliance",
        version="2.0",
        description="Compliance Report - audit-ready compliance documentation",
        section_order=("summary", "findings", "ai_comment"),
        requires_ai_comment=True,
    ),
}

FORMAT_MAP = {
    "json": ReportFormat.JSON,
    "html": ReportFormat.HTML,
    "pdf": ReportFormat.PDF,
}

FORMAT_MIME = {
    "json": "application/json",
    "html": "text/html",
    "pdf": "application/pdf",
}

TEMPLATE_FRAMEWORKS = {
    "executive": ["OWASP", "CIS"],
    "technical": ["OWASP ASVS", "NIST CSF"],
    "compliance": ["SOC2", "PCI DSS", "ISO 27001"],
}

# SOC 2 Trust Services Criteria relevant to VAPT findings
SOC2_CONTROLS = [
    ("CC7.1", "Vulnerability management — continuous monitoring and detection of security vulnerabilities"),
    ("CC7.2", "Incident detection — procedures to identify and respond to security incidents"),
    ("CC7.3", "Incident response — response activities and communication"),
    ("CC7.4", "Incident recovery — restoration of systems and business continuity"),
    ("CC7.5", "System monitoring — anomalous activity detection"),
    ("CC8.1", "Change management — changes to data, software and configurations authorized and tested"),
    ("CC6.1", "Logical access — access restricted to authorized users"),
    ("CC6.2", "Access provisioning and removal — user access managed through lifecycle"),
    ("CC6.3", "Access revocation — access removed upon termination/role change"),
    ("CC6.6", "Cryptographic controls — encryption of sensitive data in transit and at rest"),
    ("CC9.1", "Risk mitigation — system design aligned with risk assessment"),
]

# ISO 27001 Annex A controls relevant to VAPT findings
ISO27001_CONTROLS = [
    ("A.5.25", "Learning from information security incidents"),
    ("A.5.23", "Cloud services security"),
    ("A.5.21", "Managing information security in the ICT supply chain"),
    ("A.8.20", "Networks security"),
    ("A.8.21", "Security of network services"),
    ("A.8.22", "Segregation of networks"),
    ("A.8.28", "Secure coding"),
    ("A.8.24", "Use of cryptography"),
    ("A.8.25", "Secure development life cycle"),
    ("A.8.26", "Application security requirements"),
    ("A.8.27", "Secure system architecture and engineering principles"),
    ("A.8.29", "Security testing in development and acceptance"),
    ("A.5.14", "Information transfer"),
    ("A.8.9", "Management of technical vulnerabilities"),
    ("A.8.10", "Information deletion"),
    ("A.5.33", "Protecting records"),
    ("A.8.19", "Installation of software on operational systems"),
    ("A.8.1", "User endpoint devices"),
]

# Keyword -> control mapping for SOC 2 / ISO 27001
_DEFAULT_SOC2 = "CC7.1"
_DEFAULT_ISO = "A.8.28"


def _finding_to_security_finding(f: FindingModel) -> SecurityFinding:
    import re
    asset = f.asset.name.lower() if hasattr(f, 'asset') and f.asset else "unknown"
    asset = re.sub(r'[^a-z0-9_]', '_', asset)

    details = f.details or {}
    cves = details.get("cve") or details.get("cves") or []
    cwes = details.get("cwe") or details.get("cwes") or []
    if isinstance(cves, str):
        cves = [cves]
    if isinstance(cwes, str):
        cwes = [cwes]

    risk_score = details.get("risk_score") or details.get("cvss")

    evidence = details.get("evidence") or details.get("payload")
    kb_sources = [r for r in (details.get("kb_sources") or []) if isinstance(r, str)]
    references = [r for r in kb_sources if r.startswith(("http://", "https://"))]
    kb_non_urls = [r for r in kb_sources if not r.startswith(("http://", "https://"))]
    metadata = {
        "host": details.get("host"),
        "port": details.get("port"),
        "path": details.get("path"),
        "protocol": details.get("protocol"),
        "service": details.get("service"),
        "vulnerability_type": details.get("vulnerability_type"),
        "tool": details.get("tool"),
        "confidence": details.get("confidence"),
        "kb_sources": kb_non_urls or None,
    }
    metadata = {k: v for k, v in metadata.items() if v is not None}

    try:
        confidence = float(details.get("confidence") or 1.0)
    except (TypeError, ValueError):
        confidence = 1.0

    return SecurityFinding(
        id=uuid_lib.UUID(f.id) if isinstance(f.id, str) else f.id,
        assessment_id=str(f.assessment_id),
        asset=asset,
        capability="vapt",
        plugin=f.plugin_id,
        title=f.title,
        description=f.description or "",
        severity=Severity(f.severity.lower()) if f.severity else Severity.INFO,
        confidence=confidence,
        remediation=f.remediation or "",
        cvss=f.cvss_score,
        risk_score=risk_score,
        cwe=cwes,
        cve=cves,
        evidence=evidence if isinstance(evidence, str) else None,
        references=references,
        metadata=metadata,
        fingerprint=str(f.id),
    )


class GenerateReportRequest(BaseModel):
    assessment_id: str
    template: str = "executive"
    format: str = "json"


def _dict_to_security_finding(item: dict, assessment_id: str) -> SecurityFinding:
    """Build a SecurityFinding from a scan snapshot row (assessment.config)."""
    cves = item.get("cve") or []
    cwes = item.get("cwe") or []
    if isinstance(cves, str):
        cves = [cves]
    if isinstance(cwes, str):
        cwes = [cwes]
    kb_sources = [r for r in (item.get("kb_sources") or []) if isinstance(r, str)]
    references = [r for r in kb_sources if r.startswith(("http://", "https://"))]
    kb_non_urls = [r for r in kb_sources if not r.startswith(("http://", "https://"))]
    metadata = {
        "host": item.get("host"),
        "port": item.get("port"),
        "path": item.get("path"),
        "protocol": item.get("protocol"),
        "service": item.get("service"),
        "vulnerability_type": item.get("vulnerability_type"),
        "tool": item.get("tool"),
        "confidence": item.get("confidence"),
        "kb_sources": kb_non_urls or None,
    }
    metadata = {k: v for k, v in metadata.items() if v is not None}
    try:
        confidence = float(item.get("confidence") or 1.0)
    except (TypeError, ValueError):
        confidence = 1.0
    evidence = item.get("evidence")
    try:
        severity = Severity(str(item.get("severity", "info")).lower())
    except ValueError:
        severity = Severity.INFO
    return SecurityFinding(
        id=uuid_lib.uuid4(),
        assessment_id=assessment_id,
        asset="target",
        capability="vapt",
        plugin="vapt",
        title=str(item.get("title"))[:512] or "Finding",
        description=item.get("description") or "",
        severity=severity,
        confidence=confidence,
        remediation=item.get("remediation") or "",
        cvss=None,
        risk_score=None,
        cwe=cwes,
        cve=cves,
        evidence=evidence if isinstance(evidence, str) else None,
        references=references,
        metadata=metadata,
        fingerprint=str(uuid_lib.uuid4()),
    )


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

    # Prefer the scan's own finding snapshot (assessment.config) so the report
    # shows the full scan result even when cross-scan fingerprint dedup kept
    # most findings attached to earlier assessments. Falls back to DB rows.
    snapshot = (dict(assessment.config or {}).get("finding_snapshot")) or []
    if snapshot:
        sec_findings = [_dict_to_security_finding(item, str(assessment.id)) for item in snapshot]
        findings_count = len(sec_findings)
    else:
        sec_findings = [_finding_to_security_finding(f) for f in findings]
        findings_count = len(findings)

    project = assessment.project if hasattr(assessment, "project") else None
    org_name = None
    if project is not None and getattr(project, "organization", None) is not None:
        org_name = project.organization.name
    elif project is not None:
        try:
            org_name = project.organization.name
        except Exception:
            org_name = None

    client_name = org_name or (project.name if project else None) or "AstraIX Client"
    asset_name = assessment.asset.name if hasattr(assessment, "asset") and assessment.asset else "Unknown Asset"
    started = assessment.started_at or assessment.created_at
    completed = assessment.completed_at
    now = datetime.now(timezone.utc)

    # Real AI insights (Gemini executive summary / recommendations) captured
    # by the VAPT orchestrator at scan time are stored in assessment.config.
    cfg = dict(assessment.config or {})
    insights = cfg.get("insights") or {}
    if isinstance(insights, str):
        try:
            import json as _json
            insights = _json.loads(insights)
        except Exception:
            insights = {}

    extras = {
        "client_name": client_name,
        "asset_name": asset_name,
        "assessment_type": assessment.type,
        "assessment_status": assessment.status,
        "started_at": started.strftime("%Y-%m-%d") if started else "N/A",
        "completed_at": completed.strftime("%Y-%m-%d") if completed else now.strftime("%Y-%m-%d"),
        "report_date": now.strftime("%Y-%m-%d"),
        "report_version": "2.0 (Final)",
        "engagement_ref": f"{assessment.id[:8].upper()}",
        "environment": details_env(assessment),
        "soc2_controls": SOC2_CONTROLS,
        "iso27001_controls": ISO27001_CONTROLS,
        "ai_comment": insights.get("executive_summary") or "",
        "risk_level": insights.get("risk_level") or "",
        "recommendations": insights.get("recommendations") or [],
        "tools_used": insights.get("tools_used") or [],
        "scan_duration": insights.get("scan_duration") or "",
    }

    request = ReportRequest(
        template=tmpl,
        findings=sec_findings,
        correlation_id=body.assessment_id,
        extras=extras,
    )

    engine = Jinja2ReportEngine()
    artifacts = await engine.render(request, formats=(fmt,))

    if not artifacts:
        raise HTTPException(status_code=500, detail="Report generation failed")

    artifact = artifacts[0]

    report_content = artifact.serialize()
    ext = {"json": "json", "html": "html", "pdf": "pdf"}.get(body.format, "json")
    filename = f"report_{body.assessment_id[:8]}_{body.template}.{ext}"
    return ResponseSchema(
        data={
            "download_url": None,
            "report": report_content,
            "filename": filename,
            "title": artifact.title,
            "format": artifact.format.value,
            "mime": FORMAT_MIME.get(body.format, "application/octet-stream"),
            "assessment_id": body.assessment_id,
            "findings_count": findings_count,
        }
    )


def details_env(assessment: AssessmentModel) -> str:
    try:
        cfg = assessment.config or {}
        env = cfg.get("environment")
        if env:
            return env
    except Exception:
        pass
    return "Production"


@router.get("/templates")
async def list_templates():
    return ResponseSchema(
        data=[
            {
                "id": tid,
                "name": t.description.split(" - ")[0],
                "description": t.description,
                "version": t.version,
                "frameworks": TEMPLATE_FRAMEWORKS.get(tid, []),
            }
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
