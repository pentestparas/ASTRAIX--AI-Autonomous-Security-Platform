"""FastAPI app for the AI-SecOS Core Web UI.

Run with: uvicorn api:app --reload --port 8000
"""

from __future__ import annotations

import asyncio
import json
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from ai_secos_core.capabilities.loader import CapabilityLoader
from ai_secos_core.capabilities.registry import CapabilityRegistry
from ai_secos_core.capabilities.resolver import CapabilityResolver
from ai_secos_core.finding_engine.engine import DefaultFindingEngine, FindingEngineContext
from ai_secos_core.finding_engine.normalizer import NormalizerRegistry
from ai_secos_core.finding_engine.normalizers.httpx import HttpxNormalizer
from ai_secos_core.finding_engine.normalizers.nmap import NmapNormalizer
from ai_secos_core.finding_engine.normalizers.nuclei import NucleiNormalizer
from ai_secos_core.finding_engine.normalizers.subfinder import SubfinderNormalizer
from ai_secos_core.finding_engine.normalizers.trivy import TrivyNormalizer
from ai_secos_core.finding_engine.normalizers.semgrep import SemgrepNormalizer
from ai_secos_core.infrastructure.logging import configure_logging, get_logger
from ai_secos_core.plugin_system.executor import PluginExecutor, PluginExecutionRequest
from ai_secos_core.plugin_system.loader import PluginLoader
from ai_secos_core.plugin_system.registry import PluginRegistry
from ai_secos_core.plugin_system.sandbox import PluginSandbox
from ai_secos_core.config.settings import PluginSystemSettings
from ai_secos_core.risk_engine import build_default_risk_engine
from ai_secos_core.shared.assessment import Assessment, AssessmentConfiguration, AssessmentStatus
from ai_secos_core.shared.asset import Asset, AssetType
from ai_secos_core.shared.correlation import new_correlation_id
from ai_secos_core.shared.events import InProcessEventDispatcher
from ai_secos_core.infrastructure.metrics import NoopMetricsRegistry
from ai_secos_core.report_engine.engine import NullReportEngine
from ai_secos_core.report_engine.types import ReportRequest, ReportTemplate
from ai_secos_core.runtime.workflow_engine import DefaultWorkflowEngine
from ai_secos_core.runtime.workflow import load_workflow_from_yaml

configure_logging()
logger = get_logger("api")

# ---------------------------------------------------------------------------
# App bootstrap
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent
PLUGINS_ROOT = BASE_DIR / "plugins"
CAPABILITIES_ROOT = BASE_DIR / "capabilities" / "library"
WORKFLOWS_ROOT = BASE_DIR / "workflows"


def _bootstrap() -> dict[str, Any]:
    plugin_loader = PluginLoader(PLUGINS_ROOT)
    plugin_registry = PluginRegistry()
    for record in plugin_loader.discover():
        plugin_registry.register(record)

    normalizer_registry = NormalizerRegistry()
    normalizer_registry.register(HttpxNormalizer())
    normalizer_registry.register(NmapNormalizer())
    normalizer_registry.register(NucleiNormalizer())
    normalizer_registry.register(SubfinderNormalizer())
    normalizer_registry.register(TrivyNormalizer())
    normalizer_registry.register(SemgrepNormalizer())

    capability_loader = CapabilityLoader(CAPABILITIES_ROOT)
    capability_registry = CapabilityRegistry()
    if CAPABILITIES_ROOT.exists():
        for loaded in capability_loader.discover():
            capability_registry.register_from_manifest(loaded.manifest)

    workflow_engine = DefaultWorkflowEngine()
    if WORKFLOWS_ROOT.exists():
        for workflow_path in WORKFLOWS_ROOT.rglob("*.yml"):
            try:
                workflow_engine.register(load_workflow_from_yaml(workflow_path))
            except Exception:
                pass

    return {
        "plugin_registry": plugin_registry,
        "normalizer_registry": normalizer_registry,
        "capability_registry": capability_registry,
        "workflow_engine": workflow_engine,
    }


_state = _bootstrap()


# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------


class AssessRequest(BaseModel):
    target: str = Field(..., description="Target URL or hostname to assess")
    ports: list[int] | None = Field(default=[80, 443], description="Ports to scan")
    follow_redirects: bool = Field(default=True)
    capability_id: str = Field(default="web/discovery")


class FindingSummary(BaseModel):
    id: str
    title: str
    description: str
    severity: str
    confidence: float
    risk_score: float | None
    category: str
    asset: str
    tags: list[str]
    plugin: str
    cwe: list[str]
    cve: list[str]
    metadata: dict[str, Any]


class AssessResponse(BaseModel):
    assessment_id: str
    correlation_id: str
    capability: str
    status: str
    finding_count: int
    findings: list[FindingSummary]
    risk_score_min: float
    risk_score_max: float
    risk_score_avg: float
    error: str | None = None


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="AI-SecOS Core API",
    description="HTTP probe + web discovery capability with risk scoring",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _sanitize_asset_id(target: str) -> str:
    """Convert 'https://example.com:443' to 'asset_example_com'."""
    import re
    # Remove protocol
    if "://" in target:
        target = target.split("://", 1)[1]
    # Remove port
    target = target.split(":")[0]
    # Replace non-alphanumeric with single underscore
    target = re.sub(r"[^a-z0-9]+", "_", target.lower())
    # Ensure starts with letter
    if not target[0].isalpha():
        target = "t_" + target
    return "asset_" + target


@app.post("/assess", response_model=AssessResponse)
async def assess(req: AssessRequest) -> AssessResponse:
    """Run a web discovery assessment against the given target."""
    target = req.target.strip()
    if not target:
        raise HTTPException(status_code=400, detail="target is required")

    # Resolve capability
    resolver = CapabilityResolver(
        capability_registry=_state["capability_registry"],
        workflow_engine=_state["workflow_engine"],
        installed_plugins=frozenset(_state["plugin_registry"].ids()),
    )

    if not _state["capability_registry"].has(req.capability_id):
        raise HTTPException(status_code=404, detail=f"capability '{req.capability_id}' not found")

    resolved = resolver.resolve(
        capability_id=req.capability_id,
        inputs={"target": target},
        version=None,
    )

    # Build asset + assessment
    asset_id = _sanitize_asset_id(target)
    asset = Asset(
        id=asset_id,
        type=AssetType.URL,
        value=f"https://{target}" if req.ports == [443] or (len(req.ports) == 1 and req.ports[0] == 443) else f"http://{target}",
        display_name=f"Assessment target: {target}",
    )
    correlation_id = new_correlation_id()
    assessment = Assessment.create(
        configuration=AssessmentConfiguration(
            capability_id=req.capability_id,
            inputs=resolved.inputs,
        ),
        asset_ids=(asset_id,),
        target_assets=(asset.canonical_string,),
    )
    assessment.correlation_id = correlation_id
    assessment.transition(AssessmentStatus.RUNNING, correlation_id=correlation_id, reason="assessment started")

    # Execute plugin
    sandbox = PluginSandbox(settings=PluginSystemSettings())
    executor = PluginExecutor(
        _state["plugin_registry"],
        sandbox,
        InProcessEventDispatcher(),
        NoopMetricsRegistry(),
    )

    plugin_id = resolved.inputs.get("plugin_id") or "scanner/httpx"

    plugin_result = await executor.execute(
        PluginExecutionRequest(
            plugin_id=plugin_id,
            params={"target": target, "ports": req.ports, "follow_redirects": req.follow_redirects},
            correlation_id=correlation_id,
        )
    )

    if plugin_result.status.value != "ok":
        assessment.transition(AssessmentStatus.FAILED, correlation_id=correlation_id, reason=plugin_result.error or "plugin failed")
        raise HTTPException(status_code=502, detail=f"plugin failed: {plugin_result.error}")

    raw_output = plugin_result.output
    if not isinstance(raw_output, dict):
        raise HTTPException(status_code=502, detail="unexpected plugin output shape")

    # Normalize → risk score
    from ai_secos_core.finding_engine.deduplicator import DefaultFindingDeduplicator
    finding_engine = DefaultFindingEngine(
        normalizers=_state["normalizer_registry"],
        deduplicator=DefaultFindingDeduplicator(),
    )
    context = FindingEngineContext(
        assessment_id=assessment.id,
        capability_id=req.capability_id,
        asset_id=asset_id,
    )
    findings = await finding_engine.process(
        plugin_id=plugin_id,
        raw_output=raw_output,
        context=context,
    )

    risk_engine = build_default_risk_engine()
    risk_results = await risk_engine.score(findings)

    assessment.result = ai_secos_core.shared.assessment.AssessmentResult(
        finding_ids=tuple(str(f.id) for f in findings),
        risk_scores=tuple(r.score.value for r in risk_results),
        report_artifact_ids=(),
    )
    assessment.transition(AssessmentStatus.COMPLETED, correlation_id=correlation_id, reason="assessment completed")

    summaries: list[FindingSummary] = []
    for r in risk_results:
        f = r.finding
        summaries.append(FindingSummary(
            id=str(f.id),
            title=f.title,
            description=f.description,
            severity=f.severity.value,
            confidence=f.confidence,
            risk_score=r.score.value,
            category=f.category,
            asset=f.asset,
            tags=list(f.tags),
            plugin=f.plugin,
            cwe=list(f.cwe),
            cve=list(f.cve),
            metadata=dict(f.metadata),
        ))

    return AssessResponse(
        assessment_id=assessment.id,
        correlation_id=str(correlation_id),
        capability=req.capability_id,
        status="completed",
        finding_count=len(findings),
        findings=summaries,
        risk_score_min=min((r.score.value for r in risk_results), default=0),
        risk_score_max=max((r.score.value for r in risk_results), default=0),
        risk_score_avg=sum(r.score.value for r in risk_results) / len(risk_results) if risk_results else 0,
        error=None,
    )


@app.get("/capabilities")
async def list_capabilities():
    """List available capabilities."""
    caps = []
    for cid in ["web/discovery", "port/scan", "cve/scan"]:
        if _state["capability_registry"].has(cid):
            caps.append({"id": cid, "status": "available"})
        else:
            caps.append({"id": cid, "status": "not_registered"})
    return {"capabilities": caps}


# ---------------------------------------------------------------------------
# Static files (frontend)
#   - Serve index.html at /
#   - Serve assets under /static/
# ---------------------------------------------------------------------------

STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def index():
    return (STATIC_DIR / "index.html").read_text()


if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", reload=True, port=8000)