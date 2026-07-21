"""Report Engine — implementation.

At Milestone 1, only the JSON/Markdown default renderer is shipped.
HTML rendering and template-driven themes arrive later.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from threading import RLock
from typing import Any, Iterable, Sequence

from ai_secos_core.report_engine.types import (
    ReportArtifact,
    ReportFormat,
    ReportRequest,
    ReportSection,
    ReportTemplate,
)


class ReportEngine(abc.ABC):
    """Render reports from findings + risk scores."""

    @abc.abstractmethod
    async def render(
        self,
        request: ReportRequest,
        *,
        formats: Iterable[ReportFormat] = (ReportFormat.JSON,),
    ) -> list[ReportArtifact]:
        raise NotImplementedError


@dataclass
class NullReportEngine:
    """JSON/Markdown default at Milestone 1.

    Produces deterministic artefacts using the template's
    `section_order`. Template registry lives elsewhere.
    """

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
            artifact = ReportArtifact(
                format=fmt,
                title=f"{request.template.id}@{request.template.version}",
                sections=tuple(sections),
                correlation_id=request.correlation_id,
            )
            out.append(artifact)
        return out


# ---------------------------------------------------------------------------
# Section builders — replaceable per draft milestone.


def _build_section(
    kind: str,
    request: ReportRequest,
) -> ReportSection | None:
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
    severity_counts: dict[str, int] = {}
    for f in findings:
        severity_counts[f.severity.value] = severity_counts.get(f.severity.value, 0) + 1
    risky: list[dict[str, Any]] = []
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


__all__ = ["ReportEngine", "NullReportEngine"]
