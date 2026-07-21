# AstraIX Security Analyst - Knowledge Base

> **Authoritative Source for AI Development Assistance**
> 
> This document provides the single source of truth for understanding the AstraIX Security Analyst codebase. 
> AI assistants should consult this document before providing development assistance to prevent hallucinations 
> and ensure alignment with the project's architecture, design decisions, and roadmap.

---

## 🎯 Project Overview

### Mission
Build the world's most extensible AI-native cybersecurity platform.

### Vision
**AI-SecOS** is the runtime. **AstraIX Security Analyst** is the first application.

### Architecture
```
AstraIX Platform
├── AI-SecOS Core         (reusable runtime; zero product knowledge)
├── Applications
│   └── Security Analyst  (first product)
└── Plugins               (isolated subprocesses; live outside applications)
```

---

## 🏗️ Core Architectural Principles

### Five Non-Negotiable Platform Principles

1. **AI reasons. Tools execute.**
   - The AI selects workflows, interprets results, prioritizes, explains, and reports.
   - It does not perform scanning, parsing, or execution.

2. **Capabilities orchestrate plugins.**
   - Applications request a **Capability**. The platform resolves it to a Workflow, which fans out to one or more **Plugins**.
   - Applications never bind to specific tools.

3. **Plugins return structured data only.**
   - Plugins receive a typed input and return a typed result (JSON, validated against the plugin manifest schema).
   - No side channels, no free-form stdout, no in-memory state shared with the AI.

4. **All plugin output must normalize into a Canonical Security Finding.**
   - Every plugin's output — regardless of native format — flows through the Normalizer.
   - Emerges as a `SecurityFinding` (the system's universal language).
   - This is the schema that AI, Risk Engine, and Report Engine consume.

5. **Applications never call plugins directly; all execution flows through AI-SecOS Core.**
   - The capability/workflow/plugin hierarchy is owned entirely by AI-SecOS.
   - Applications compose capabilities; the platform composes plugins.

---

## 📁 Repository Structure

```
astraix-security-analyst/
├── backend/                          # FastAPI backend
│   ├── ai_secos_core/                # Reusable platform runtime
│   │   ├── capabilities/             # Capability manifests, loader, resolver, registry
│   │   ├── finding_engine/            # Normalize → Dedupe → Enrich → Correlate
│   │   ├── infrastructure/           # DB, logging, metrics, error handling
│   │   ├── runtime/                   # Workflow engine
│   │   ├── plugin_system/             # Plugin management
│   │   └── shared/                    # Value objects, errors, events
│   ├── app/                           # Security Analyst application
│   │   ├── api/v1/                    # REST endpoints
│   │   ├── domain/                    # DDD aggregates (assets, assessments, findings)
│   │   ├── orchestrator/              # Workflow coordination
│   │   ├── repositories/             # Data access layer
│   │   └── services/                 # Business logic
│   └── tests/
│
├── frontend/                         # Next.js 15 frontend
│   ├── src/
│   │   ├── app/                      # Pages (dashboard, assessments, findings)
│   │   ├── components/               # UI components
│   │   ├── services/                 # API clients
│   │   ├── types/                    # TypeScript types
│   │   └── hooks/                    # React hooks
│
├── engineering/                      # CRITICAL DOCUMENTATION
│   ├── PROJECT_MANIFEST.md          # Constitution - loaded FIRST by AI
│   ├── VISION.md                    # 10-year product vision
│   ├── ARCHITECTURE.md              # System architecture
│   ├── MVP_SCOPE.md                 # Build now/later/never
│   ├── ROADMAP.md                   # Milestone sequence
│   ├── TECH_STACK.md                # Technology decisions
│   ├── CODING_STANDARDS.md          # Coding conventions
│   └── rules/00_MASTER_RULES.md     # AI engineer behavioral rules
│
├── plugins/                          # Plugin directory
│   ├── core/                        # Plugin SDK
│   └── community/                   # Community plugins
│
├── docker/                          # Docker configurations
├── docker-compose.yml              # Full stack orchestration
├── requirements.txt               # Python dependencies (updated)
└── Makefile                       # Convenience commands
```

---

## 🔑 Key Abstraction Levels

These are the ONLY levels an Application interacts with:

```
Application         (e.g. Security Analyst)
       ↓ requests
Capability          (e.g. Web Security Assessment, Prompt Injection Assessment)
       ↓ resolved by
Workflow            (declarative YAML; e.g. Discovery, LLM Assessment)
       ↓ executed by
Plugin              (isolated subprocess; e.g. Subfinder, Nuclei, Garak)
```

### Examples

| Application | Capability | Workflow | Plugins |
|---|---|---|---|
| Security Analyst | Web Security Assessment | Discovery | Subfinder, Katana, httpx, Nuclei |
| AI Security | Prompt Injection Assessment | LLM Assessment | Garak, PyRIT, Promptfoo |
| Cloud Security | Cloud Posture Assessment | Cloud Audit | Prowler, ScoutSuite |

---

## 📊 Canonical Security Finding Schema

This is the **universal language** of the platform:

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

### Hard Rules

- `evidence` and `metadata` are **opaque payloads** from the plugin. They are stored but **never trusted** for downstream logic.
- Downstream logic reads only declared fields.
- **AI is fed canonical findings**; it never sees raw plugin output.
- Two findings with the same `(asset, cwe, cve, plugin)` collapse to one canonical record via a deterministic fingerprint; `first_seen` is preserved, `last_seen` updated.

---

## 🔌 Plugin Development Kit (PDK)

### Interface (First Stable Contract)

```python
class SecurityPlugin(ABC):
    @property
    def metadata(self) -> PluginMetadata: ...
    
    async def validate(self, context: PluginContext) -> None: ...
    
    async def execute(self, context: PluginContext) -> PluginResult: ...
    
    async def cleanup(self) -> None: ...
```

### Plugin Characteristics

- **Isolated subprocesses** that exchange typed JSON
- Plugins do not import AI-SecOS code
- Plugins do not call the AI
- Plugins do not see other plugins
- Plugins have a `manifest.yml` defining inputs/outputs

### Plugin Locations

```
plugins/
├── core/                  # Plugin SDK
├── community/            # Community plugins
└── [capability]/         # e.g. network_vapt, web_vapt, cloud_posture
```

---

## 🚀 Finding Engine Pipeline

The Finding Engine owns the truth about findings after a plugin runs:

```
Plugin Output
    ↓
1. Normalize (raw → Canonical SecurityFinding)
    ↓
2. Deduplicate (by deterministic fingerprint)
    ↓
3. Enrich (asset context, historical data)
    ↓
4. Correlate (cross-plugin, cross-asset)
    ↓
5. Tag & Map (MITRE / OWASP / CWE)
    ↓
Canonical SecurityFindings (consumed by AI, Risk Engine, Report Engine)
```

---

## 📈 Risk Engine

The Risk Engine composes:

- **Likelihood** — probability of exploitation, given context
- **Impact** — what happens if exploited
- **Exploitability** — concrete attack feasibility (public exploit, prerequisites)
- **Business Context** — asset criticality, exposure, compliance weight
- → **Risk Score (0–100)**

---

## 🤖 AI Gateway

Decomposed into six sub-modules:

1. **Provider Manager** — which providers exist; lifecycle (OpenAI, Anthropic, MiniMax, Ollama, Gemini, Nemotron, …)
2. **Prompt Manager** — versioned, parameter-rendered prompt templates
3. **Context Builder** — assembles normalized findings + asset + history + policy into a context window
4. **Model Router** — selects provider/model per request (cost, capability, latency)
5. **Token Manager** — budgets, accounting, retries, compression
6. **Response Parser** — safe parsing of model output back to typed structures

### Adding a New Provider

Implement an adapter under `providers/` and register it with `Provider Manager`. All other AI Gateway modules are untouched.

---

## 🎯 AI Philosophy

- **AI never executes scanning work**
- **AI reasons about findings, not raw plugin output**
- **AI receives normalized, risk-scored `SecurityFinding` objects** — not raw payloads
- **AI is an analyst. Plugins are operators.**

---

## 🛤️ Execution Flow

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

---

## 📋 API Endpoints (28 Total)

### Core
- `GET /` - Service info
- `GET /health` - Health check
- `GET /ready` - Readiness check

### API v1
- **Assessments:** `GET /api/v1/assessments/`, `POST /api/v1/assessments/{id}/start`
- **Assets:** `GET /api/v1/assets/`, `GET /api/v1/assets/{id}`
- **Findings:** `GET /api/v1/findings/`, `GET /api/v1/findings/{id}`
- **Plugins:** `GET /api/v1/plugins/`, `POST /api/v1/plugins/{id}/run`
- **Organizations:** `GET /api/v1/organizations`, `GET /api/v1/organizations/{id}`
- **Auth:** `POST /api/v1/auth/login`, `POST /api/v1/auth/register`, `GET /api/v1/auth/me`
- **Projects:** `POST /api/v1/projects`, `GET /api/v1/projects/{id}`
- **API Keys:** `POST /api/v1/api-keys`, `GET /api/v1/api-keys/{id}`
- **Memberships:** `POST /api/v1/memberships`, `PATCH /api/v1/memberships/{id}`

---

## 🗺️ Current Milestone Status

Per `engineering/ROADMAP.md`:

### Completed
- ✅ M0: Engineering Foundation
- ✅ M1-M4: Backend core infrastructure (mostly)

### In Progress / Next
- 🔄 M5: Security Analyst UI
- 🔄 Plugin implementations (httpx, nuclei, etc.)

### Deferred
- ⏳ M6+: Cloud Security, Container Security, SAST, AI Security, etc.

---

## 🔒 Non-Goals (Explicitly Out of Scope)

- ❌ EDR (Endpoint Detection & Response)
- ❌ SIEM (Security Information & Event Management)
- ❌ SOAR (Security Orchestration, Automation & Response)
- ❌ SOC-as-a-Service
- ❌ Active exploitation (running real exploits against customers)
- ❌ Credential attacks (password spraying, brute force, stuffing)
- ❌ Lateral movement automation
- ❌ C2 (Command & Control)
- ❌ Malware generation or delivery

---

## 📚 Critical Documentation Loading Order

When providing development assistance, AI assistants MUST load documents in this order:

1. **`engineering/PROJECT_MANIFEST.md`** (this file) — Loaded FIRST
2. **`engineering/rules/00_MASTER_RULES.md`** — Behavioral rules
3. **Relevant supporting doc:**
   - Architecture question → `engineering/ARCHITECTURE.md`
   - Scope/deferral question → `engineering/MVP_SCOPE.md`
   - Sequencing question → `engineering/ROADMAP.md`
   - Coding question → `engineering/CODING_STANDARDS.md`
4. Then state the task

**If there is a conflict between documents, this file wins, then `00_MASTER_RULES.md`, then the relevant doc.**

---

## ⚙️ Technology Stack

### Backend
- **Framework:** FastAPI 0.110+
- **Language:** Python 3.12
- **Database:** PostgreSQL + SQLAlchemy 2.0 (async)
- **Cache:** Redis
- **Validation:** Pydantic v2
- **Migrations:** Alembic

### Frontend
- **Framework:** Next.js 15 (App Router)
- **Language:** TypeScript (strict)
- **Styling:** Tailwind CSS + Radix UI
- **State:** React Query / Zustand

### Infrastructure
- **Containerization:** Docker + Docker Compose
- **Monitoring:** Prometheus + Grafana (planned)

---

## 🎓 Development Principles

1. **Simplicity over complexity**
2. **Extensibility over shortcuts**
3. **Composition over inheritance**
4. **Convention over configuration**
5. **Security by default**
6. **Performance after correctness**
7. **Production quality over prototype hacks**

---

## 🚀 Quick Start Commands

### Backend
```bash
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm run dev
```

### Docker (All-in-one)
```bash
docker-compose up -d
```

---

## 📝 Maintenance Notes

### Requirements Management
- **Use `requirements.txt`** with minimum versions (>=)
- **DON'T use `requirements-core.txt`** (has conflicting pinned versions)
- After adding packages: `pip freeze > requirements.lock.txt` for production

### Python Version
- **Python 3.12** is the standard
- Backend venv is configured for 3.12
- Set system default to 3.12 in `~/.zshrc`

### Frontend Status
- MVP/placeholder quality (M5 not started)
- Backend is primary focus
- Use Swagger UI (`/docs`) for testing APIs

---

**Last Updated:** July 2026  
**Status:** Active Development  
**Version:** PoC (T0)
