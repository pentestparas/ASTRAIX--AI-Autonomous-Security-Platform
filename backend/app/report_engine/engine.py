from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

from jinja2 import Environment, FileSystemLoader, select_autoescape

from ai_secos_core.report_engine.types import (
    ReportArtifact,
    ReportFormat,
    ReportRequest,
    ReportSection,
    ReportTemplate,
)
from ai_secos_core.shared.value_objects import SecurityFinding


TEMPLATE_DIR = Path(__file__).parent / "templates"

_jinja_env = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=select_autoescape(["html", "xml"]),
)


class ReportEngine:
    async def render(
        self,
        request: ReportRequest,
        *,
        formats: Iterable[ReportFormat] = (ReportFormat.JSON,),
    ) -> list[ReportArtifact]:
        raise NotImplementedError


@dataclass(frozen=True)
class RenderedArtifact(ReportArtifact):
    serialized_content: str = ""

    def serialize(self) -> str:
        if self.serialized_content:
            return self.serialized_content
        return super().serialize()


@dataclass
class Jinja2ReportEngine:
    async def render(
        self,
        request: ReportRequest,
        *,
        formats: Iterable[ReportFormat] = (ReportFormat.JSON,),
    ) -> list[ReportArtifact]:
        sections: list[ReportSection] = []
        for kind in request.template.section_order:
            section = _build_section(kind, request)
            if section is not None:
                sections.append(section)

        out: list[ReportArtifact] = []
        for fmt in formats:
            if fmt in (ReportFormat.HTML, ReportFormat.MARKDOWN):
                artifact = self._render_html(request, sections, fmt)
            else:
                artifact = ReportArtifact(
                    format=fmt,
                    title=f"{request.template.id}@{request.template.version}",
                    sections=tuple(sections),
                    correlation_id=request.correlation_id,
                )
            out.append(artifact)
        return out

    def _render_html(
        self,
        request: ReportRequest,
        sections: list[ReportSection],
        fmt: ReportFormat,
    ) -> RenderedArtifact:
        template_name = f"{request.template.id}.html"

        severity_counts = {}
        for f in request.findings:
            severity_counts[f.severity.value] = severity_counts.get(f.severity.value, 0) + 1

        risky = []
        for r in request.scored:
            risky.append({"score": r.score.value, "asset": r.finding.asset})
        risky.sort(key=lambda d: -d["score"])

        ai_comment = ""
        for s in sections:
            if s.kind == "ai_comment":
                ai_comment = s.body

        extras = request.extras or {}

        ctx = {
            "title": f"{request.template.id}@{request.template.version}",
            "assessment_id": request.correlation_id,
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            "template_name": request.template.id,
            "total_findings": len(request.findings),
            "severity_counts": severity_counts,
            "top_risks": risky[:5],
            "ai_comment": ai_comment,
            "client_name": extras.get("client_name", "AstraIX Client"),
            "asset_name": extras.get("asset_name", "Unknown Asset"),
            "assessment_type": extras.get("assessment_type", "VAPT"),
            "assessment_status": extras.get("assessment_status", ""),
            "started_at": extras.get("started_at", ""),
            "completed_at": extras.get("completed_at", ""),
            "report_date": extras.get("report_date", ""),
            "report_version": extras.get("report_version", "1.0"),
            "engagement_ref": extras.get("engagement_ref", ""),
            "environment": extras.get("environment", "Production"),
            "soc2_controls": extras.get("soc2_controls", []),
            "iso27001_controls": extras.get("iso27001_controls", []),
            "findings": [
                {
                    "id": str(f.id),
                    "asset": f.asset,
                    "severity": f.severity.value,
                    "title": f.title,
                    "description": f.description,
                    "remediation": f.remediation,
                    "plugin": f.plugin,
                    "cvss": f.cvss,
                    "risk_score": f.risk_score,
                    "cwe": f.cwe or [],
                    "cve": f.cve or [],
                    "confidence": f.confidence,
                }
                for f in request.findings
            ],
        }

        try:
            tmpl = _jinja_env.get_template(template_name)
        except Exception:
            tmpl = _jinja_env.get_template("executive.html")

        body = tmpl.render(**ctx)

        if fmt is ReportFormat.HTML:
            try:
                from weasyprint import HTML as WeasyHTML
                pdf_bytes = WeasyHTML(string=body).write_pdf()
                serialized = pdf_bytes.decode("latin-1")
            except Exception:
                serialized = body
        else:
            serialized = body

        return RenderedArtifact(
            format=fmt,
            title=ctx["title"],
            sections=tuple(sections),
            correlation_id=request.correlation_id,
            serialized_content=serialized,
        )


def _build_section(kind: str, request: ReportRequest) -> ReportSection | None:
    if kind == "summary":
        return _summary_section(request)
    if kind == "findings":
        return _findings_section(request)
    if kind == "ai_comment":
        if request.template.requires_ai_comment:
            return _ai_comment_placeholder(request)
        return None
    return None


def _summary_section(request: ReportRequest) -> ReportSection:
    findings = request.findings
    severity_counts = {}
    for f in findings:
        severity_counts[f.severity.value] = severity_counts.get(f.severity.value, 0) + 1
    risky = []
    for r in request.scored:
        risky.append({"value": r.score.value, "asset": r.finding.asset})
    risky.sort(key=lambda d: -d["value"])
    return ReportSection(
        title="Executive Summary",
        kind="summary",
        body=f"{len(findings)} findings; severity histogram: {severity_counts}",
        data={
            "total_findings": len(findings),
            "severity_counts": severity_counts,
            "top_risks": risky[:5],
        },
    )


def _findings_section(request: ReportRequest) -> ReportSection:
    serialized = [
        {
            "id": str(f.id),
            "asset": f.asset,
            "severity": f.severity.value,
            "title": f.title,
            "risk_score": f.risk_score,
            "cwe": f.cwe,
            "cve": f.cve,
        }
        for f in request.findings
    ]
    return ReportSection(
        title="Findings",
        kind="findings",
        body=f"{len(serialized)} finding(s) attached.",
        data={"findings": serialized},
    )


def _ai_comment_placeholder(request: ReportRequest) -> ReportSection:
    return ReportSection(
        title="AI Analyst Comment",
        kind="ai_comment",
        body="(placeholder — AI Gateway integration arrives post M1)",
        data={"requires_ai_gateway": True},
    )
