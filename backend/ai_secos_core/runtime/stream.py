"""Streaming contracts — typed event types for live plugin output.

M2 only defines the contract; more events arrive in later milestones.
The platform's `EventDispatcher` consumes `DomainEvent`s; this module
adds concrete event type factories for streaming + lifecycle.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional, Tuple
import uuid

from ai_secos_core.shared.events import DomainEvent, make_event


PLUGIN_STARTED_EVENT = "plugin.started"
PLUGIN_PROGRESS_EVENT = "plugin.progress"
PLUGIN_FINDING_EVENT = "plugin.finding"
PLUGIN_COMPLETED_EVENT = "plugin.completed"


ASSESSMENT_CREATED_EVENT = "assessment.created"
ASSESSMENT_STARTED_EVENT = "assessment.started"
ASSESSMENT_COMPLETED_EVENT = "assessment.completed"
ASSESSMENT_FAILED_EVENT = "assessment.failed"


CAPABILITY_RESOLVED_EVENT = "capability.resolved"


@dataclass(frozen=True)
class PluginStartedPayload:
    plugin_id: str
    runtime: str
    correlation_id: str
    started_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass(frozen=True)
class PluginProgressPayload:
    plugin_id: str
    percentage: float  # 0.0 — 1.0
    message: str
    correlation_id: str
    at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass(frozen=True)
class PluginFindingPayload:
    plugin_id: str
    finding_id: str
    asset_id: str
    severity: str
    title: str
    at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass(frozen=True)
class PluginCompletedPayload:
    plugin_id: str
    duration_ms: int
    status: str
    findings_count: int
    correlation_id: str


def emit_plugin_started(
    dispatcher, *, plugin_id: str, runtime: str, correlation_id: str
) -> "asyncio.Future[None]":
    """Emit (and await the publish) for plugin.started."""
    payload = PluginStartedPayload(
        plugin_id=plugin_id, runtime=runtime, correlation_id=correlation_id
    ).__dict__
    return dispatcher.publish(make_event(PLUGIN_STARTED_EVENT, correlation_id=correlation_id, payload=payload))


def emit_plugin_completed(
    dispatcher, *, plugin_id: str, duration_ms: int, status: str, findings_count: int, correlation_id: str
):
    payload = PluginCompletedPayload(
        plugin_id=plugin_id,
        duration_ms=duration_ms,
        status=status,
        findings_count=findings_count,
        correlation_id=correlation_id,
    ).__dict__
    return dispatcher.publish(
        make_event(PLUGIN_COMPLETED_EVENT, correlation_id=correlation_id, payload=payload)
    )


def emit_plugin_finding(
    dispatcher, *, plugin_id: str, finding_id: str, asset_id: str, severity: str, title: str, correlation_id: str
):
    payload = PluginFindingPayload(
        plugin_id=plugin_id,
        finding_id=finding_id,
        asset_id=asset_id,
        severity=severity,
        title=title,
    ).__dict__
    return dispatcher.publish(
        make_event(PLUGIN_FINDING_EVENT, correlation_id=correlation_id, payload=payload)
    )


def emit_plugin_progress(
    dispatcher, *, plugin_id: str, percentage: float, message: str, correlation_id: str
):
    payload = PluginProgressPayload(
        plugin_id=plugin_id,
        percentage=percentage,
        message=message,
        correlation_id=correlation_id,
    ).__dict__
    return dispatcher.publish(
        make_event(PLUGIN_PROGRESS_EVENT, correlation_id=correlation_id, payload=payload)
    )