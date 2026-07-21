# Assessment API

> 67 nodes · cohesion 0.06

## Key Concepts

- **AssessRequest** (30 connections) — `backend/ai_secos_core/api.py`
- **AssessResponse** (30 connections) — `backend/ai_secos_core/api.py`
- **FindingSummary** (30 connections) — `backend/ai_secos_core/api.py`
- **run_demo()** (29 connections) — `backend/ai_secos_core/m2_demo.py`
- **DefaultWorkflowEngine** (21 connections) — `backend/ai_secos_core/runtime/workflow_engine.py`
- **assess()** (20 connections) — `backend/ai_secos_core/api.py`
- **FindingEvidence** (19 connections) — `backend/ai_secos_core/shared/value_objects.py`
- **CapabilityResolver** (17 connections) — `backend/ai_secos_core/capabilities/resolver.py`
- **Assessment** (15 connections) — `backend/ai_secos_core/shared/assessment.py`
- **_bootstrap()** (14 connections) — `backend/ai_secos_core/api.py`
- **InProcessEventDispatcher** (14 connections) — `backend/ai_secos_core/shared/events.py`
- **NoopMetricsRegistry** (13 connections) — `backend/ai_secos_core/infrastructure/metrics.py`
- **PluginSystemSettings** (12 connections) — `backend/ai_secos_core/config/settings.py`
- **HttpxNormalizer** (12 connections) — `backend/ai_secos_core/finding_engine/normalizers/httpx.py`
- **api.py** (11 connections) — `backend/ai_secos_core/api.py`
- **NmapNormalizer** (11 connections) — `backend/ai_secos_core/finding_engine/normalizers/nmap.py`
- **NucleiNormalizer** (11 connections) — `backend/ai_secos_core/finding_engine/normalizers/nuclei.py`
- **SemgrepNormalizer** (11 connections) — `backend/ai_secos_core/finding_engine/normalizers/semgrep.py`
- **SubfinderNormalizer** (11 connections) — `backend/ai_secos_core/finding_engine/normalizers/subfinder.py`
- **TrivyNormalizer** (11 connections) — `backend/ai_secos_core/finding_engine/normalizers/trivy.py`
- **assessment.py** (9 connections) — `backend/ai_secos_core/shared/assessment.py`
- **ReportRequest** (8 connections) — `backend/ai_secos_core/report_engine/types.py`
- **ReportTemplate** (8 connections) — `backend/ai_secos_core/report_engine/types.py`
- **AssessmentConfiguration** (8 connections) — `backend/ai_secos_core/shared/assessment.py`
- **AssessmentStatus** (8 connections) — `backend/ai_secos_core/shared/assessment.py`
- *... and 42 more nodes in this community*

## Relationships

- [[App Factory & Null Providers]] (26 shared connections)
- [[Metrics System]] (25 shared connections)
- [[Context Building]] (23 shared connections)
- [[Workflow Engine]] (14 shared connections)
- [[Community 45]] (13 shared connections)
- [[Task & Risk Types]] (11 shared connections)
- [[Plugin Schemas]] (8 shared connections)
- [[Community 28]] (8 shared connections)
- [[Community 33]] (7 shared connections)
- [[Community 42]] (7 shared connections)
- [[Community 31]] (6 shared connections)
- [[Capability Loader]] (5 shared connections)

## Source Files

- `backend/ai_secos_core/api.py`
- `backend/ai_secos_core/capabilities/resolver.py`
- `backend/ai_secos_core/config/settings.py`
- `backend/ai_secos_core/finding_engine/normalizers/httpx.py`
- `backend/ai_secos_core/finding_engine/normalizers/nmap.py`
- `backend/ai_secos_core/finding_engine/normalizers/nuclei.py`
- `backend/ai_secos_core/finding_engine/normalizers/semgrep.py`
- `backend/ai_secos_core/finding_engine/normalizers/subfinder.py`
- `backend/ai_secos_core/finding_engine/normalizers/trivy.py`
- `backend/ai_secos_core/infrastructure/metrics.py`
- `backend/ai_secos_core/m2_demo.py`
- `backend/ai_secos_core/report_engine/types.py`
- `backend/ai_secos_core/risk_engine/engine.py`
- `backend/ai_secos_core/runtime/workflow_engine.py`
- `backend/ai_secos_core/shared/assessment.py`
- `backend/ai_secos_core/shared/events.py`
- `backend/ai_secos_core/shared/value_objects.py`
- `backend/ai_secos_core/tests/runtime/test_task_planner.py`

## Audit Trail

- EXTRACTED: 175 (38%)
- INFERRED: 282 (62%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*