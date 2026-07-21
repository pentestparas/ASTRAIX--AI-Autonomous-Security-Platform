# ROADMAP.md

> The sequence.
> Loaded when a sequencing/milestone question arises.

---

## How Milestone Boundaries Work

Each milestone below produces a **runnable, demonstrable increment**. A milestone is considered complete when:

1. Its deliverables are merged.
2. Its verification command passes.
3. Its docs are updated.
4. Its demo path is rehearsable.

Work that doesn't belong to the active milestone belongs to a later one.

---

## Milestone 0 — Engineering Foundation *(complete)*

- Repository skeleton.
- Docker Compose.
- Engineering documents:
  - `PROJECT_MANIFEST.md`
  - `ARCHITECTURE.md`
  - `MVP_SCOPE.md`
  - `ROADMAP.md` (this file)
  - `CODING_STANDARDS.md`
  - `rules/00_MASTER_RULES.md`
- Engineering docs are **frozen** at the end of this milestone. Future edits versioned with rationale.

---

## Milestone 1 — AI-SecOS Core (Reusable Platform Shell)

**Goal:** A runnable but plugin-less platform shell. Demonstrates the three-layer repo, the lifecycle flow, and an empty Workflow Engine.

**Scope (only these modules):**

```
backend/ai_secos_core/
├── platform/                     (bootstrap, DI container, lifespan, CORS, error handlers)
├── runtime/                      (orchestrator, workflow engine)
├── plugin_system/                (manifest schema, registry, executor, lifecycle)
├── normalizer/                   (raw → SecurityFinding)
├── risk_engine/                  (0–100 risk_score)
├── ai_gateway/                   (gateway, provider interface, provider stubs)
├── report_engine/                (template-driven report)
├── shared/                       (errors, events, results)
├── config/                       (settings, 12-factor)
└── infrastructure/               (async SQLAlchemy, in-process cache, observability)
```

Each module ships with:
- typed interfaces
- unit tests
- in-code docstrings
- entry point to be loaded by the application entrypoint

**Out of scope:** no plugins, no Nuclei/httpx/etc., no AI provider keys, no security-analyst business code, no UI.

**Verification:**
- `pytest backend/ai_secos_core/` passes.
- Boot the platform shell, return 200 on `/health`.
- An empty workflow definition can be loaded from YAML and interpreted.

**Demo path:**
- Show the repo layout.
- Show an empty workflow being registered.
- Show that a second application could be mounted with no change to `ai_secos_core`.

---

## Milestone 2 — First Plugin (httpx)

**Goal:** Validate the entire execution chain end-to-end with a single, real plugin. If this works, the architecture is sound.

**Scope:**
- `plugins/httpx/` containing `plugin.yml` + executable.
- httpx → Normalizer → Canonical Security Finding (probe-level: title, severity, asset).
- Risk Engine integration with one canonical finding.
- One test workflow that invokes the capability.

**Verification:**
- The plugin is discoverable via the registry.
- The plugin runs in an isolated subprocess and returns typed JSON.
- The Normalizer converts every httpx probe result into a `SecurityFinding`.
- The Risk Engine produces a 0–100 score.
- Tests cover subprocess isolation, retry on failure, timeout enforcement.

**Demo path:**
- Trigger httpx against a harmless target.
- Show the chain produce canonical findings, scanned across Network → Plugin → Normalizer → Risk Engine.

---

## Milestone 3 — Discovery Capability

**Goal:** Add Subfinder and Katana. Capability `discovery_dns_recon` is complete.

**Scope:**
- `plugins/subfinder/`, `plugins/katana/` with manifests and executables.
- A `discovery` capability that runs all three (Subfinder, Katana, httpx) and feeds into a unified asset inventory.
- Dashboard panel: "Target asset inventory."

**Verification:**
- All three plugins run end-to-end via the workflow.
- Asset graph: discovered subdomains → probes → canonical findings.
- Tests cover capability resolution from YAML.

**Demo path:**
- Receive a single target → discover subdomains → probe each → show dedup.

---

## Milestone 4 — Web Security Assessment Capability

**Goal:** The AI finally has meaningful, risk-scored findings to reason over.

**Scope:**
- `plugins/nuclei/` with manifest and executable.
- A `web_security_assessment` capability that invokes `discovery` and then Nuclei.
- Normalizer extended for Nuclei's native format.
- Risk Engine rolled up per asset and per assessment.
- AI Gateway integration — provider-agnostic, real provider selected via config.
- Report Engine produces an HTML executive report from a Jinja template.

**Verification:**
- A complete chain runs against a test target.
- Canonical findings are produced.
- Risk scores are stable.
- AI summary produces a reusable Markdown report.
- Report is rendered as HTML with no Jinja errors.

**Demo path:** *"Target → Discovery → Probing → Nuclei → Normalized Findings → Risk Scores → AI Summary → Executive Report."*

---

## Milestone 5 — Security Analyst UI

**Goal:** Make all of the above observable to a human.

**Scope:**
- `frontend/core/` — domain-agnostic primitives (Card, DataTable, Badge, Button, Progress, Modal, Chart).
- `frontend/applications/security_analyst/` — Dashboard, Assessment Detail, Findings, Report Viewer.
- Adapters map backend shapes into the typed objects the primitives expect.
- React Query hooks with typed contracts.
- One service base class for HTTP.

**Verification:**
- Dashboard renders an empty state, a running state, and a complete state.
- Findings page is filterable by severity, capability, asset.
- Report viewer renders the AI report.
- No "assessment"-specific words leak into `core/`.

**Demo path:** Run an end-to-end assessment from the dashboard; watch the platform progress; open the executive report.

---

## Milestones 6+ — Post-VP

Each post-VP milestone is gated on a separate proposal. Tracked in `engineering/adr/` (one ADR per milestone when started).

| # | Title | Earliest start |
|---|---|---|
| 6 | Cloud Security Capability | After M5 demo |
| 7 | Container & Kubernetes Capability | After M6 |
| 8 | SAST / Code Review Capability | After M7 |
| 9 | AI Security Capability | After M8 |
| 10 | Compliance Reporting | After M9 |
| 11 | Threat Modeling | After M10 |
| 12 | Mobile Security | After M11 |
| 13 | Network Security (incl. AD enumeration helpers) | After M12 |
| 14 | AI Risk Enrichment (intel, business context) | After M13 |
| 15 | Remediation Automation (PR bots, ticket ops) | After M14 |
| 16 | Continuous Monitoring (scheduling, drift) | After M15 |
| 17 | Multi-tenancy & RBAC | After M16 |
| 18 | PDK for plugin authors | After M17 |

---

## What this document does NOT cover

- The architecture itself — `ARCHITECTURE.md`.
- Build-now / build-later / never — `MVP_SCOPE.md`.
- Coding style — `CODING_STANDARDS.md`.
- AI engineer behavior — `rules/00_MASTER_RULES.md`.