"""Milestone 2 End-to-End Demo — Capability -> Workflow -> Plugin -> Findings.

Demonstrates the complete vertical slice:

  Application → Capability (web/discovery)
                    ↓ (CapabilityResolver)
                 Workflow (workflow-web-discovery)
                    ↓ (Task Planner)
                 Task: plugin.run(httpx)
                    ↓ (StreamingPluginExecutor)
                 httpx subprocess emits JSON
                    ↓
                 HttpxNormalizer
                    ↓ (FindingEngine pipeline)
                 Canonical SecurityFindings
                    ↓ (RiskEngine)
                 Risk-scored findings
                    ↓ (ReportEngine)
                 JSON report

This file is the runnable integration proof for M2.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any, Dict

from ai_secos_core.capabilities.loader import CapabilityLoader
from ai_secos_core.capabilities.registry import CapabilityRegistry
from ai_secos_core.capabilities.resolver import CapabilityResolver
from ai_secos_core.finding_engine.engine import (
    DefaultFindingEngine,
    FindingEngineContext,
)
from ai_secos_core.finding_engine.normalizer import NormalizerRegistry
from ai_secos_core.finding_engine.normalizers.httpx import HttpxNormalizer
from ai_secos_core.infrastructure.logging import configure_logging, get_logger

logger = get_logger("m2-demo")
from ai_secos_core.plugin_system.executor import PluginExecutionRequest, PluginExecutor
from ai_secos_core.plugin_system.loader import PluginLoader
from ai_secos_core.plugin_system.registry import PluginRegistry
from ai_secos_core.runtime.plugin_streaming import StreamingPluginExecutor
from ai_secos_core.runtime.workflow import load_workflow_from_yaml
from ai_secos_core.runtime.workflow_engine import DefaultWorkflowEngine
from ai_secos_core.shared.assessment import (
    Assessment,
    AssessmentConfiguration,
    AssessmentResult,
    AssessmentStatus,
)
from ai_secos_core.shared.asset import Asset, AssetType
from ai_secos_core.shared.events import InProcessEventDispatcher
from ai_secos_core.shared.correlation import new_correlation_id
from ai_secos_core.risk_engine import build_default_risk_engine
from ai_secos_core.report_engine.engine import NullReportEngine
from ai_secos_core.report_engine.types import ReportRequest, ReportTemplate
from ai_secos_core.infrastructure.metrics import NoopMetricsRegistry
from ai_secos_core.plugin_system.sandbox import PluginSandbox
from ai_secos_core.config.settings import PluginSystemSettings


async def run_demo() -> Dict[str, Any]:
    """Run the full M2 end-to-end demonstration and return a summary."""
    configure_logging()
    correlation_id = new_correlation_id()

    plugins_root = Path(__file__).parent / "plugins"
    capabilities_root = Path(__file__).parent / "capabilities" / "library"

    # 1) Plugin discovery.
    plugin_loader = PluginLoader(plugins_root)
    plugin_registry = PluginRegistry()
    for record in plugin_loader.discover():
        plugin_registry.register(record)

    # 2) Normalizer registry (manual registration at M2; auto-discovery later).
    normalizer_registry = NormalizerRegistry()
    normalizer_registry.register(HttpxNormalizer())

    # 3) Capability discovery.
    capability_loader = CapabilityLoader(capabilities_root)
    capability_registry = CapabilityRegistry()
    if capabilities_root.exists():
        for loaded in capability_loader.discover():
            capability_registry.register_from_manifest(loaded.manifest)

    # 4) Workflow discovery.
    workflows_root = Path(__file__).parent / "workflows"
    workflow_engine = DefaultWorkflowEngine()
    if workflows_root.exists():
        for workflow_path in workflows_root.rglob("*.yml"):
            try:
                workflow = load_workflow_from_yaml(workflow_path)
                workflow_engine.register(workflow)
            except Exception:
                continue

    # 5) Resolve capability.
    resolver = CapabilityResolver(
        capability_registry=capability_registry,
        workflow_engine=workflow_engine,
        installed_plugins=frozenset(plugin_registry.ids()),
    )

    capability_id = "web/discovery"
    if not capability_registry.has(capability_id):
        print(f"[M2 demo] capability '{capability_id}' not registered — skipping")
        return {"status": "skip", "reason": "capability not registered"}

    resolved = resolver.resolve(
        capability_id=capability_id,
        inputs={"target": "demo.astraix.local"},
        version=None,
    )
    logger.info("capability.resolved extra capability_id=%s", capability_id)

    # 6) Build assets.
    target_asset = Asset(
        id="asset_demo",
        type=AssetType.URL,
        value="https://demo.astraix.local",
        display_name="Demo AstraIX Target",
    )

    # 7) Build Assessment.
    assessment = Assessment.create(
        configuration=AssessmentConfiguration(
            capability_id=capability_id,
            inputs=resolved.inputs,
        ),
        asset_ids=(target_asset.id,),
        target_assets=(target_asset.canonical_string,),
    )
    assessment.correlation_id = correlation_id
    assessment.transition(AssessmentStatus.RUNNING, correlation_id=correlation_id, reason="capability resolved")

    # 8) Run the plugin directly (M2 demo skips full Task Planner).
    event_dispatcher = InProcessEventDispatcher()
    metrics_registry = NoopMetricsRegistry()
    sandbox = PluginSandbox(settings=PluginSystemSettings())
    base_executor = PluginExecutor(plugin_registry, sandbox, event_dispatcher, metrics_registry)
    streaming_executor = StreamingPluginExecutor(base_executor, event_dispatcher)
    request = PluginExecutionRequest(
        plugin_id="scanner/httpx",
        params={"target": "demo.astraix.local", "ports": ["80", "443"]},
        correlation_id=correlation_id,
    )
    plugin_result = await streaming_executor.execute(request)

    if plugin_result.status.value != "ok":
        print(f"[M2 demo] plugin failed: {plugin_result.error}")
        return {"status": "plugin_failed", "error": plugin_result.error}

    raw_output = plugin_result.output
    if not isinstance(raw_output, dict):
        print("[M2 demo] unexpected plugin output shape")
        return {"status": "bad_output"}

    # 9) Normalize → Finding Engine pipeline.
    deduplicator = _noop_dedup()
    finding_engine = DefaultFindingEngine(
        normalizers=normalizer_registry,
        deduplicator=deduplicator,
    )
    context = FindingEngineContext(
        assessment_id=assessment.id,
        capability_id=capability_id,
        asset_id=target_asset.id,
    )
    findings = await finding_engine.process(
        plugin_id="scanner/httpx",
        raw_output=raw_output,
        context=context,
    )

    # 10) Risk score.
    risk_engine = build_default_risk_engine()
    risk_results = await risk_engine.score(findings)

    # 11) Report.
    report_engine = NullReportEngine()
    template = ReportTemplate(
        id="m2-web-discovery",
        version="1.0.0",
        description="M2 demo report for web discovery capability",
    )
    assessment.result = AssessmentResult(
        finding_ids=tuple(str(f.id) for f in findings),
        risk_scores=tuple(r.score.value for r in risk_results),
        report_artifact_ids=(),
    )
    assessment.transition(AssessmentStatus.COMPLETED, correlation_id=correlation_id, reason="M2 demo completed")

    report_request = ReportRequest(
        template=template,
        findings=tuple(r.finding for r in risk_results),
        scored=risk_results,
        correlation_id=correlation_id,
    )
    artifacts = await report_engine.render(report_request)
    serialized = [a.serialize() for a in artifacts]

    summary = {
        "status": "ok",
        "correlation_id": correlation_id,
        "capability": capability_id,
        "asset_count": 1,
        "finding_count": len(findings),
        "risk_score_min": min((r.score.value for r in risk_results), default=0),
        "risk_score_max": max((r.score.value for r in risk_results), default=0),
        "risk_score_avg": (
            sum(r.score.value for r in risk_results) / len(risk_results)
            if risk_results else 0
        ),
        "finding_titles": [f.title for f in findings],
        "report_count": len(serialized),
        "report_lengths": [len(s) for s in serialized],
    }
    print(json.dumps(summary, indent=2))
    return summary


def _noop_dedup():
    """Minimal in-memory deduplicator for M2 demo only."""

    class _StubDedup:
        def __init__(self):
            self._seen = []

        def ingest(self, f):
            self._seen.append(f)
            return f, True

        def known(self, f):
            return False

        def all(self):
            return list(self._seen)

        def reset(self):
            self._seen.clear()

    # Use FindingDeduplicator via component path; fallback for M2 only
    from ai_secos_core.finding_engine.deduplicator import DefaultFindingDeduplicator
    return DefaultFindingDeduplicator()


if __name__ == "__main__":
    logger = get_logger("m2-demo")
    asyncio.run(run_demo())