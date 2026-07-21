# MVP_SCOPE.md

> The guardrail.
> Loaded when a scope/deferral question arises.

---

## Mission of this document

A single, durable answer to: *"Should we build this now, later, or never?"*

If a candidate feature falls outside the lists below, the AI engineer must **stop and ask**, not implement.

---

## Build Now (Required for VP Demo)

The VP demo proves three things:

1. **A Capability can be requested** end-to-end (request → workflow → plugins → canonical findings → risk score → AI summary → report).
2. **The platform is reusable** (a second Application could be added without rewriting core).
3. **The AI is reasoning, not scanning** (Risk Engine + AI Gateway together).

### Required for the demo

| # | Item | Why |
|---|---|---|
| 1 | Three-layer repo layout (`ai_secos_core` + `applications/security_analyst`) | Architectural foundation |
| 2 | Plugin SDK contract (`SecurityPlugin` ABC) | First stable contract |
| 3 | Plugin Manager + Plugin Executor (isolated subprocesses) | Reusable execution machinery |
| 4 | Workflow Engine (declarative YAML) | Heart of the platform |
| 5 | Capability manifests (declarative YAML) | Resolution target for Applications |
| 6 | Result Normalizer → Canonical Security Finding | Universal schema |
| 7 | Risk Engine (0–100 score) | Pre-AI prioritization |
| 8 | AI Gateway (provider interface + provider stubs) | Model-agnostic reasoning |
| 9 | Report Engine (template-driven) | Executive output |
| 10 | First plugin: httpx | Proves the SDK end-to-end |
| 11 | Discovery Capability (Subfinder, Katana, httpx) | Proves workflow composition for recon-only |
| 12 | Web Security Assessment Capability (Nuclei) | Proves a second capability on the same core |
| 13 | Security Analyst UI (Dashboard + assessment detail + findings + report) | Proves frontend layering |
| 13 | In-process cache (no Redis) | Keeps MVP small |
| 14 | In-process event dispatcher (no Kafka) | Keeps MVP small |
| 15 | Async SQLAlchemy + Alembic | Persistence layer |
| 16 | Structured logging + correlation ids | Observability |
| 17 | OpenAPI docs | API surface |
| 18 | Docker Compose | Local run |

### Optional for the demo (only if it doesn't slow the core path)

- Prometheus `/metrics` endpoint
- Health/readiness endpoints
- Per-plugin retry policy
- Capability versioning

---

## Build Later (Post-Demo Roadmap)

These are real, valuable, and **deliberately deferred** until after the demo is validated with leadership.

| Area | Examples | Earliest milestone |
|---|---|---|
| **Cloud Security** | Prowler, ScoutSuite, Wiz-like capabilities | M6 |
| **Container / K8s Security** | Trivy, Kubescape, Falco integration | M7 |
| **SAST / Code Review** | Semgrep, CodeQL, Gitleaks | M8 |
| **AI Security** | Garak, PyRIT, Promptfoo + dedicated Capability | M9 |
| **Compliance Reporting** | ISO 27001, SOC 2, PCI, HIPAA, NIST 800-53, CIS | M10 |
| **Threat Modeling** | STRIDE, MITRE mapping, AI-generated DFDs | M11 |
| **Mobile Security** | Android/iOS static + dynamic analysis | M12 |
| **Network Security** | Nmap, Masscan, SMB, SNMP, AD enumeration | M13 |
| **AI Risk Engine enrichment** | Threat intelligence feeds, business context | M14 |
| **Remediation Automation** | PR creation, Jira tickets, developer nudge | M15 |
| **Continuous Monitoring** | Scheduled scans, drift detection | M16 |
| **Multi-tenancy** | Org separation, RBAC | M17 |
| **SDK for plugin authors** | `astraix plugin new` scaffold | M18 |

These will gain concrete sub-documents when approached.

---

## Never Build Unless Needed

These are **anti-features**. They do not align with the AI-assisted security assessment mission. Building any of them requires a **separate, approved initiative**.

- **No EDR** (Endpoint Detection & Response)
- **No SIEM** (Security Information & Event Management)
- **No SOAR** (Security Orchestration, Automation & Response)
- **No SOC-as-a-Service**
- **No active exploitation** (running real exploits against customers)
- **No credential attacks** (password spraying, brute force, stuffing)
- **No lateral movement automation**
- **No C2** (Command & Control)
- **No malware generation or delivery**
- **No persistence mechanism tooling**
- **No privilege escalation tooling**
- **No Active Directory attack framework**
- **No autonomous exploitation engine**

If a prompt requests any of these, the AI engineer must **stop and ask the human sponsor**, not proceed.

---

## Infrastructure deferred beyond MVP

Each item below was considered. Each was deferred because it adds operational complexity proportional to scale we don't have yet.

| Deferred | Use later when |
|---|---|
| Redis | Multi-process workers; > ~10 assessments/hour sustained |
| Kafka / pub-sub | > 1 backend process tier |
| gRPC plugin transport | Plugins need to be on remote hosts |
| Full CQRS | Tens of millions of findings; need separate read models |
| Event sourcing for assessments | Need audit-grade replays / regulatory traceability |
| Plugin marketplace | Have external plugin authors |
| Plugin signing / supply chain | Distributing plugins to untrusted parties |
| Multi-tenancy (row-level security) | Selling SaaS to multiple orgs |
| Distributed orchestrator (Temporal / Argo) | Assessments need to span minutes-to-hours with retry across crashes |

---

## What this document does NOT cover

- **Architecture** — see `ARCHITECTURE.md`
- **Coding style** — see `CODING_STANDARDS.md`
- **Sequence** — see `ROADMAP.md`
- **Behavioral rules** — see `rules/00_MASTER_RULES.md`