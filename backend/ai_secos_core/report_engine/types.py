"""Report Engine — typed shapes only at Milestone 1.

The Engine produces a `ReportArtifact` (one per requested `format`).
Each artifact is composed of `ReportSection`s: title, severity
summary, findings list, executive comment, etc.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Sequence

from ai_secos_core.risk_engine.engine import RiskEngineResult
from ai_secos_core.shared.value_objects import SecurityFinding


class ReportFormat(str, Enum):
    """Supported output formats."""

    JSON = "json"
    MARKDOWN = "markdown"
    HTML = "html"
    PDF = "pdf"


@dataclass(frozen=True)
class ReportSection:
    """One ordered block of the final report."""

    title: str
    kind: str          # e.g. "summary", "findings", "remediation"
    body: str = ""
    data: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ReportArtifact:
    """A rendered report, finalized."""

    format: ReportFormat
    title: str
    sections: tuple[ReportSection, ...] = ()
    correlation_id: str = ""

    def serialize(self) -> str:
        if self.format is ReportFormat.JSON:
            return json.dumps(
                {
                    "title": self.title,
                    "format": self.format.value,
                    "sections": [
                        {"title": s.title, "kind": s.kind, "body": s.body, "data": s.data}
                        for s in self.sections
                    ],
                },
                indent=2,
                default=str,
            )
        # Markdown fallback (HTML rendering arrives later).
        md: list[str] = [f"# {self.title}", ""]
        for s in self.sections:
            md.append(f"## {s.title}")
            md.append("")
            if s.body:
                md.append(s.body)
                md.append("")
        return "\n".join(md)


@dataclass(frozen=True)
class ReportTemplate:
    """A template declaring how to assemble a report."""

    id: str
    version: str
    description: str = ""
    section_order: tuple[str, ...] = ("summary", "findings", "ai_comment")
    requires_ai_comment: bool = False


@dataclass(frozen=True)
class ReportRequest:
    """Inputs to the engine."""

    template: ReportTemplate
    findings: Sequence[SecurityFinding]
    scored: Sequence[RiskEngineResult] = field(default_factory=tuple)
    correlation_id: str = ""
    extras: dict[str, Any] = field(default_factory=dict)


__all__ = [
    "ReportArtifact",
    "ReportFormat",
    "ReportSection",
    "ReportTemplate",
    "ReportRequest",
]
