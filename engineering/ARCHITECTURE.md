# ARCHITECTURE.md

> The shape of the system.
> Loaded when an architecture question arises.

---

## 1. Layered Model

```
AstraIX Platform
├── AI-SecOS Core         (reusable runtime; zero product knowledge)
├── Applications
│   ├── Security Analyst  (first product)
│   └── <future>
└── Plugins               (isolated subprocesses; live outside Applications)
```

The repository is named `astraix-security-analyst/` for now. Renaming is **deferred** — see `MVP_SCOPE.md`.

Inside the repository, the canonical backend layout is:

```
backend/
├── ai_secos_core/
│   ├── platform/                 (bootstrap, DI container, lifespan, CORS, error handlers)
│   ├── runtime/                  (orchestrator, workflow engine)
│   ├── plugin_system/            (manifest, registry, executor, lifecycle, transport)
│   ├── ai_gateway/               (gateway, provider interface, providers/{openai,anthropic,minimax,ollama,gemini,nemotron})
│   ├── normalizer/               (raw plugin output → Canonical Security Finding)
│   ├── risk_engine/              (0–100 risk scoring)
│   ├── report_engine/            (template-driven report generation)
│   ├── shared/                   (events, errors, cqrs-lite, results)
│   ├── infrastructure/           (db, cache-in-process, observability, config)
│   └── models/                   (Canonical Security Finding, Capability, Workflow)
└── applications/
    └── security_analyst/
        ├── domain/               (DDD aggregates: assets, assessments, findings)
        ├── workflows/            (product-specific workflow definitions)
        ├── interfaces/           (REST endpoints, request/response schemas)
        └── ui_bindings/          (data shapes consumed by the frontend)
```

---

## 2. AI-SecOS Core Responsibilities

AI-SecOS Core owns:

- Workflow orchestration
- Capability resolution
- Plugin lifecycle management
- Plugin execution
- Result normalization
- Risk scoring
- AI provider routing
- Report generation
- Configuration management
- Logging
- Metrics
- Event dispatching

AI-SecOS Core **must contain zero application-specific business logic.**

## 3. Application Responsibilities

Applications own:

- User experience
- Domain models
- API endpoints
- Business workflows (composition of Capabilities)
- Dashboard presentation
- Authentication (future)
- Authorization (future)

Applications **must never**:

- Execute plugins directly
- Communicate with AI providers directly
- Normalize plugin output
- Perform risk scoring

The boundary is enforced by import rules and reviewed in code review.

---

## 4. The Four Abstraction Levels

```
Application      (e.g. Security Analyst)
       ↓ requests
Capability       (e.g. Web Security Assessment)
       ↓ resolved by
Workflow         (declarative YAML; ordered Steps)
       ↓ executed by
Plugin           (isolated subprocess; returns typed JSON)
       ↓ normalized into
SecurityFinding  (canonical schema; the system's universal language)
```

Applications request a Capability. The platform decides the Workflow. The Workflow composes Plugins. **Applications never know which tools are running.**

---

## 5. Canonical Security Finding

This is the universal language of the platform. Every plugin's native output — regardless of vendor format — must be normalized into this schema before any downstream consumption.

```yaml
SecurityFinding:
  id              # stable UUID, dedup key
  assessment_id   # owning assessment/run
  asset           # asset identifier (host, domain, repo, container, etc.)
  capability      # capability that produced it (e.g. web_security)
  plugin          # plugin id that produced it
  category        # normalized category (e.g. injection, misconfig, supply_chain)

  title           # human-readable one-liner
  description     # markdown; 1–3 sentences

  severity        # one of: info | low | medium | high | critical
  confidence      # 0.0–1.0
  risk_score      # 0–100 from Risk Engine (post-normalization)

  cvss            # optional float
  cwe             # optional list[str]
  cve             # optional list[str]
  owasp           # optional list[str] (e.g. "A03:2021 - Injection")

  evidence        # raw artifact reference; opaque to AI
  references      # list[str] (URLs)
  remediation     # markdown remediation guidance
  tags            # free-form labels, normalized per capability

  metadata        # plugin-specific extension; opaque to AI

  first_seen      # ISO 8601 UTC
  last_seen       # ISO 8601 UTC
  timestamp       # ISO 8601 UTC (current observation)
```

**Hard rules**

- `evidence` and `metadata` are opaque payloads from the plugin. They are stored but **never trusted** for downstream logic. Downstream logic reads only declared fields.
- AI is fed canonical findings; it never sees raw plugin output.
- Two findings with the same `(asset, cwe, cve, plugin)` collapse to one canonical record via a deterministic fingerprint; `first_seen` is preserved, `last_seen` updated.

---

## 6. Plugin Development Kit (PDK) — Stable Contract

This interface is **the first stable contract** of the platform. Implementations and Consumers are expected to evolve, but `SecurityPlugin` itself should rarely change.

```python
class SecurityPlugin(ABC):

    @property
    def metadata(self) -> PluginMetadata: ...

    async def validate(self, context: PluginContext) -> None: ...

    async def execute(self, context: PluginContext) -> PluginResult: ...

    async def cleanup(self) -> None: ...
```

- `PluginMetadata`: id, version, capabilities supported, required inputs, declared outputs.
- `PluginContext`: typed input parameters + capability manifest.
- `PluginResult`: raw structured payload to be passed to the Normalizer.

**Naming note:** "SDK" is reserved for the general concept. The Plugin SDK is officially called the **Plugin Development Kit (PDK)** to avoid name collisions with future agent/capability/workflow SDKs.

Plugins are **isolated subprocesses** that exchange typed JSON. They do not import AI-SecOS code; they do not call the AI; they do not see other plugins.

---

## 7. AI Gateway Contract

```
ai_gateway/
├── gateway.py            # single entrypoint; selects provider
├── provider.py           # interface: send/receive, retries, streaming
└── providers/
    ├── openai.py
    ├── anthropic.py
    ├── minimax.py
    ├── ollama.py
    ├── gemini.py
    └── nemotron.py
```

Every provider implements the same interface. Adding or swapping providers must not require changes elsewhere.

---

## 8. Platform Lifecycle (Execution Flow)

```
Assessment Request
        ↓
Capability Selected
        ↓
Workflow Loaded (declarative YAML; *what*, not *how*)
        ↓
Task Planner                 (translates Workflow into a DAG of Tasks; parallelism, retries, conditional execution, cancellation)
        ↓
Plugin Manager               (resolve plugin candidates for the DAG)
        ↓
Plugin Validator             (manifest + input schema check, sandbox policy check)
        ↓
Plugin Sandbox               (resource limits; allowlist; isolation boundary)
        ↓
Plugin Executor              (subprocess exec + structured log + correlation id + output collection)
        ↓
Plugin(s)                    (isolated subprocess; typed JSON in/out)
        ↓
Finding Engine               (normalize + dedupe + fingerprint + enrich + correlate + map to MITRE/OWASP/CWE + confidence adjust + tag)
        ↓
Risk Engine                  (likelihood + impact + exploitability + business context → 0–100 score)
        ↓
AI Gateway                   (Provider Manager → Prompt Manager → Context Builder → Model Router → Token Manager → Response Parser)
        ↓
Report Engine                (template → executive report)
        ↓
Dashboard                    (Application-level presentation)
```

**Separation of concerns:**

- **Workflow** is *declarative* and *static*. It names capabilities and steps.
- **Task Planner** is *dynamic*. It owns execution topology: parallelism, dependency graph, retries, batching, scheduling, conditional execution, cancellation.
- **Plugin Executor** is a *reusable service* that owns subprocess mechanics.
- **Plugin Sandbox** is the *isolation* boundary; distinct from Executor so policies can evolve without touching transport.

This is **the mental model** every contributor is expected to internalize.

---

## 9. Declarative Workflows (Not Hardcoded)

Workflows are defined as YAML, not embedded in Python:

```yaml
workflow:
  id: discovery
  steps:
    - subfinder
    - katana
    - httpx
```

```yaml
workflow:
  id: web_assessment
  steps:
    - discovery
    - technology_detection
    - nuclei
    - normalize
    - risk
    - ai_analysis
    - report
```

The orchestrator interprets the YAML. Adding a new assessment type (Cloud, AI Security, Compliance) means authoring a new workflow file — **not editing orchestrator code**.

---

## 9.1 Capabilities as First-Class Objects

Capabilities are not just concepts; they are **versioned, declarative objects** that the Workflow Engine resolves into one or more workflows.

```yaml
capability:
  id: web_security
  version: "1.0.0"
  display_name: Web Security Assessment
  description: Black-box assessment of web applications and APIs

  workflows:
    - discovery
    - web_assessment

  supported_assets:
    - domain
    - url
    - ip

  input_schema:
    target:
      type: string
      required: true
    scope:
      type: array
      required: false

  required_plugins:
    - id: subfinder
      min_version: "1.0.0"
    - id: nuclei
      min_version: "3.0.0"

  compliance:
    owasp_asvs: ["V1", "V2", "V4"]
```

```yaml
capability:
  id: ai_security
  version: "1.0.0"
  display_name: AI Security Assessment
  workflows:
    - llm_assessment
  supported_assets:
    - prompt
    - model_endpoint
```

**Why this is required:** Applications request `capability_id`. The platform resolves it to a Workflow, which fans out to Plugins. Future applications add new Capability manifests — never change Workflow Engine code.

---

## 10. Frontend Architecture

The frontend mirrors the backend split:

```
frontend/
├── core/                          (domain-agnostic primitives)
│   ├── components/                (Card, DataTable, Badge, Button, Progress, Modal, Chart)
│   ├── hooks/                     (useFetch, useResource, useStream)
│   ├── services/                  (typed HTTP client; one base class)
│   └── tokens/                    (design tokens; Tailwind preset)
└── applications/
    └── security_analyst/
        ├── pages/                 (Dashboard, Assessment Detail, Findings, Reports)
        ├── sections/              (composed from core/ primitives)
        ├── mocks/                 (test data lives here, never in core/)
        └── adapters/              (maps backend → typed shapes for core/)
```

**Rule:** `core/` must not know the words "asset", "finding", "cve", "severity". It accepts typed objects and renders them.

---

## 11. Cross-Cutting Concerns

| Concern | Owner | Notes |
|---|---|---|
| Configuration | AI-SecOS Core (`config/`) | 12-factor; env-first; never hardcoded |
| Logging | AI-SecOS Core (`infrastructure/observability/`) | Structured (JSON); correlation id per assessment |
| Metrics | AI-SecOS Core (`infrastructure/observability/`) | Prometheus format; per-workflow, per-plugin, per-ai-call |
| Tracing | AI-SecOS Core (`infrastructure/observability/`) | OTel; spans across plugin subprocess |
| Errors | AI-SecOS Core (`shared/errors.py`) | Hierarchy: `PlatformError` → `PluginError`\|`AIError`\|`WorkflowError` |
| Events | AI-SecOS Core (`shared/events.py`) | In-process dispatcher; Kafka deferred |
| Storage | AI-SecOS Core (`infrastructure/db/`) | Async SQLAlchemy + Alembic |
| Cache | AI-SecOS Core (`infrastructure/cache/`) | In-process; Redis deferred |

---

## 12. Extension Model (The Fast Path for New Products)

To add a new Application (e.g. AI Security):

1. Add new Capability manifests under `ai_secos_core/capabilities/`.
2. Add new Workflow YAML under `ai_secos_core/workflows/`.
3. Add new Plugins under `plugins/` if needed.
4. Add new DDD aggregates under `applications/<new_product>/domain/`.
5. Add new Pages under `frontend/applications/<new_product>/pages/`.

**No changes** required to the Workflow Engine, Plugin Executor, Normalizer, Risk Engine, AI Gateway, or Report Engine.

## 13. What This Document Does Not Cover

- Deployment topology (Docker files are under `docker/`; covered there).
- Coding style (see `CODING_STANDARDS.md`).
- Behavioral rules for AI engineer sessions (see `rules/00_MASTER_RULES.md`).
- Sequence of milestones (see `ROADMAP.md`).
- Build-now / build-later / never (see `MVP_SCOPE.md`).