"""Report Engine — contract-only at Milestone 1.

The Engine produces a `ReportArtifact` per requested `format`. Each
artifact composes `ReportSection`s: summary, findings, optional AI
comment, etc.

At Milestone 1 we ship:

  - The typed contract `ReportEngine` and the JSON-only default.
  - `ReportTemplate` and a registry.
"""

from ai_secos_core.report_engine.types import (
    ReportArtifact,
    ReportFormat,
    ReportSection,
    ReportTemplate,
    ReportRequest,
)
from ai_secos_core.report_engine.engine import ReportEngine, NullReportEngine

__all__ = [
    "ReportArtifact",
    "ReportFormat",
    "ReportSection",
    "ReportTemplate",
    "ReportRequest",
    "ReportEngine",
    "NullReportEngine",
]
