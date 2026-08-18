# AstraIX — Architecture Report

*Generated from the automated knowledge-graph analysis of the AstraIX codebase (4,038 files analyzed).*

**Snapshot:** commit `8bd4966` · analyzed `2026-08-18` · methodology: full-project static analysis (scan → import map → batch analysis → graph merge → layering → validation)

---

## 1. Graph Summary

| Metric | Value |
|--------|-------|
| Files analyzed | 4,038 |
| Graph nodes | 4,669 |
| Graph edges | 4,307 |
| Edge kinds | 9 (`related` 2,371 · `contains` 675 · `exports` 613 · `imports` 553 · `depends_on` 47 · `configures` 36 · `documents` 9 · `routes` 2 · `deploys` 1) |
| Architecture layers | 10 |
| Guided tour steps | 12 |
| Validation issues | 0 |
| Orphan warnings | 687 (pre-dominantly isolated knowledge-base documents) |

**Node type mix:** `document` 3,549 · `function` 416 · `file` 260 · `config` 223 · `class` 215 · `service` 4 · `pipeline` 2

**Complexity profile:** 2,145 simple · 1,677 moderate · 847 complex — a healthy distribution, with the complexity concentrated in the API layer, VAPT engine, and AI core (not in glue code).

---

## 2. Architectural Layers

| # | Layer | Nodes | Role |
|---|-------|-------:|------|
| 1 | Backend API Application | 96 | FastAPI application in `backend/app`: API v1 routers, domain models, repositories, report engine |
| 2 | AI Security Core Engine | 104 | `ai_secos_core` engine: AI gateway/provider routing, capability manifests, plugin system, risk engine |
| 3 | Database | 3 | Alembic migration environment and versioned schema |
| 4 | Frontend Application | 50 | Next.js App Router frontend: pages, dashboard/settings components, UI kit, API client |
| 5 | Knowledge Base | 3,584 | Vendored security knowledge sources (skill/runbook markdown, payload libraries) |
| 6 | Training Data | 7 | Dataset builders and SFT dataset files (Kaggle, vulnerability corpora) |
| 7 | Plugins | 3 | Top-level plugin SDK and example plugins |
| 8 | Infrastructure & Deployment | 22 | Docker images and compose, nginx config, env/ignore files, dev scripts |
| 9 | Engineering Process | 16 | Engineering standards, project manifests, ADRs, rules/checklists |
| 10 | Documentation | 153 | README, `docs/`, changelogs/worklogs, graph artifacts |

The knowledge base dominates node count by design (vendored content); the *code* footprint is comparatively small and focused — the platform is an integration of orchestration logic around real tooling.

---

## 3. God Nodes (Highest Coupling)

Nodes with the most relationships — the load-bearing architecture of the system:

| Degree | Type | Node | Path |
|-------:|------|------|------|
| 128 | document | index.md | knowledge-base index |
| 53 | file | auth.py | `backend/app/api/v1/auth.py` |
| 46 | file | routes.py | `backend/app/vapt/routes.py` (scan lifecycle) |
| 39 | file | organizations.py | `backend/app/api/v1/organizations.py` (multi-tenancy) |
| 35 | function | build_default_container | Docker exec bootstrap |
| 31 | function | setup_logging | cross-cutting logging |
| 29 | function | assess | capability evaluation entry |
| 28 | class | SecurityFinding | canonical finding model |
| 28 | file | code_review_scanner.py | `docker/scripts/` |
| 26 | file | build.py | image build tooling |
| 25 | file | card.tsx | frontend UI kit |
| 24 | file | value_objects.py | `backend/ai_secos_core/shared/` |
| 22 | function | init_db | schema bootstrap |
| 22 | file | vapt_platforms.py | `backend/app/scanner/` |

---

## 4. Module Coupling — Backend

The backend is a **two-tier design**: a thin operational FastAPI layer (`app/`) orchestrating a declarative engine (`ai_secos_core`).

**API layer (`backend/app`)** — highest coupling:
- `api/v1/auth.py` — JWT auth, OAuth2 + JSON login (53 relationships)
- `api/v1/organizations.py` — org-scoped multi-tenancy (39)
- `api/v1/plugins.py` — plugin management endpoints (17)
- `vapt/routes.py` — the scan lifecycle: quick scan → orchestration → findings (46)
- `vapt/agents/kb.py` — the bridge between agents and the knowledge base (21)
- `vapt/models.py` + `scanner/models.py` — domain models (18 / 16)
- `report_engine/engine.py` — Jinja2 HTML pentest report rendering (17)
- `repositories/organization.py` — repository pattern (20)
- `vapt/tools.py` — tool registry (16)

**AI core (`backend/ai_secos_core`)** — the declarative engine:
- `shared/value_objects.py` — shared domain primitives (24)
- `runtime/stream.py` — declarative scan workflow runtime (16)
- `plugins/{nmap,httpx,nuclei,subfinder}/main.py` — plugin instances (13 / 9 / 9 / 9)
- `capabilities/loader.py` + `plugin_system/loader.py` — capability & plugin discovery (10 / 8)
- `risk_engine/engine.py` — deterministic 0–100 risk scoring (10)
- `shared/assessment.py`, `shared/asset.py` — core domain objects (10 / 10)
- `finding_engine/normalizers/trivy.py` — tool-output normalization (8)

**Import coupling between layers** (553 import edges): the dominant flows are `ai-security-core → (capabilities, plugins)` and `backend-api → (repositories, engine)`; cross-layer imports are shallow and one-directional — `app/` consumes `ai_secos_core`, never the reverse.

---

## 5. Module Coupling — Frontend

A compact, component-driven Next.js app (50 nodes) with three reuse centers:

- `components/ui/*` — design-system primitives: `card.tsx` (25), `button.tsx` (20), `dialog.tsx` (18), `input.tsx` (14), `table.tsx` (11)
- `hooks/useApi.ts` (22) + `services/api.ts` (13) — the typed API client shared by every page
- `types/index.ts` (14) — shared domain types

Key surfaces: `app/(main)/scans/page.tsx` (15) — quick scan + history + live console; `app/(main)/graph/page.tsx` (10) — attack-surface graph; dashboard components `RecentAssessments.tsx` (10), `QuickActions.tsx` (9).

---

## 6. Infrastructure & Engineering

- `docker-compose.yml` (6 services: postgres, redis, neo4j, ZAP, backend, frontend, nginx) is the deployment hub
- `docker/Dockerfile.backend` + `docker/fetch-kb.sh` + `docker/kb-repos.txt` — knowledge base is **baked into the image at build time** (AV-immune, never staged on host)
- `docker/scripts/*` — a secondary LLM-security product family inside the repo: `code_review_scanner.py` (28), `garak_scanner.py` (24, LLM red-teaming), `promptfoo_scanner.py` (22), `flows_engine.py` (20), `dom_xss_scanner.py` (16), `web_form_scanner.py` (16), `api_surface_scanner.py` (10)
- `engineering/` — ADRs, rules/checklists, manifests documenting process decisions

---

## 7. Guided Tour (12 Steps)

The graph encodes a canonical walkthrough of the platform: **README → FastAPI entry (`main.py`) → v1 router aggregation → VAPT scan lifecycle (`vapt/routes.py`) → AI core runtime (`ai_secos_core/runtime`) → declarative YAML scan workflows → data layer (async SQLAlchemy) → report engine → frontend root layout → scans console UI → AI agents + knowledge base (`agents/kb.py`) → containerization**.

---

## 8. Validation & Caveats

- **0 validation issues** across the full graph.
- **687 orphan warnings** are overwhelmingly vendored knowledge-base markdown documents with no code references — not an architectural defect.
- `imports` edges reflect **static import analysis only**; dynamic dispatch (plugin loading by name, Docker exec of tools, AI-gateway provider selection at runtime) is deliberately not modeled, so the `??`-layer import destinations are dynamic-runtime boundaries, partially captured by the 47 `depends_on` + 36 `configures` edges.
- The graph snapshot is pinned to commit `8bd4966`; rerun the pipeline after major refactors to refresh the topology and this report.