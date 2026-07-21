# PROJECT_MANIFEST.md

> **The constitution of AstraIX.**
> Loaded by every AI engineer session before any other document.

---

## Mission

Build the world's most extensible AI-native cybersecurity platform.

## Vision

**AI-SecOS** is the runtime.
**AstraIX Security Analyst** is the first application.

Future applications include:

- Cloud Security
- AI Security
- Threat Modeling
- Secure Code Review
- Runtime Defense
- Compliance
- Executive Risk Intelligence

Every application reuses the same AI-SecOS Core.

## Product Structure

```
AstraIX Platform
├── AI-SecOS Core           (reusable runtime — zero product knowledge)
├── Applications
│   ├── Security Analyst    (first product)
│   └── <future>           (Cloud, AI Security, Threat Modeling, …)
└── Plugins                (isolated subprocesses; live outside applications)

### Naming

- **Plugin Development Kit (PDK)** — the Plugin SDK. Distinct from any future Agent SDK / Capability SDK / Workflow SDK.
- **AI-SecOS Core** — the runtime.
- **Applications** — products that request Capabilities.
```

The repository is named `astraix-security-analyst/` for now.
Renaming is **explicitly deferred** — see `MVP_SCOPE.md`.

Inside the repository, the canonical backend layout is:

```
backend/
├── ai_secos_core/                 (reusable platform primitives)
└── applications/
    └── security_analyst/          (first product; DDD aggregates live here)
```

---

## The Five Non-Negotiable Platform Principles

1. **AI reasons. Tools execute.**
   The AI selects workflows, interprets results, prioritizes, explains, and reports.
   It does not perform scanning, parsing, or execution.
2. **Capabilities orchestrate plugins.**
   Applications request a **Capability**. The platform resolves it to a Workflow, which fans out to one or more **Plugins**. Applications never bind to specific tools.
3. **Plugins return structured data only.**
   Plugins receive a typed input and return a typed result (JSON, validated against the plugin manifest schema). No side channels, no free-form stdout, no in-memory state shared with the AI.
4. **All plugin output must normalize into a Canonical Security Finding.**
   Every plugin's output — regardless of native format — flows through the Normalizer and emerges as a `SecurityFinding` (the system's universal language). This is the schema that AI, Risk Engine, and Report Engine consume.
5. **Applications never call plugins directly; all execution flows through AI-SecOS Core.**
   The capability/workflow/plugin hierarchy is owned entirely by AI-SecOS. Applications compose capabilities; the platform composes plugins.

---

## Design Priorities

Order matters. Earlier items override later ones when they conflict.

1. **Simplicity over complexity**
2. **Extensibility over shortcuts**
3. **Composition over inheritance**
4. **Convention over configuration**
5. **Security by default**
6. **Performance after correctness**
7. **Production quality over prototype hacks**

---

## The Four Abstraction Levels

These are the only levels an Application interacts with:

```
Application         (e.g. Security Analyst)
       ↓
Capability          (e.g. Web Security Assessment, Prompt Injection Assessment)
       ↓
Workflow            (declarative YAML; e.g. Discovery, LLM Assessment)
       ↓
Plugin              (isolated subprocess; e.g. Subfinder, Nuclei, Garak)
```

**Examples**

| Application | Capability | Workflow | Plugins |
|---|---|---|---|
| Security Analyst | Web Security Assessment | Discovery | Subfinder, Katana, httpx, Nuclei |
| AI Security | Prompt Injection Assessment | LLM Assessment | Garak, PyRIT, Promptfoo |
| Cloud Security | Cloud Posture Assessment | Cloud Audit | Prowler, ScoutSuite |

**Why this matters:** Applications request a Capability. The platform decides the Workflow. The Workflow composes Plugins. Applications never know — or need to know — which tools are running.

---

## Plugin Philosophy

- Every security capability is implemented as a plugin.
- Plugins are **isolated subprocesses** that exchange typed JSON.
- Plugins never communicate directly with each other or with the AI.
- Plugins do not know about Applications; they receive a Capability manifest and produce a structured result.
- The Plugin Development Kit (PDK) is one of the first stable contracts.

The platform exposes five distinct concerns for plugins; each is its own module:

- **Plugin Registry** — what exists.
- **Plugin Loader** — how code becomes a registered plugin.
- **Plugin Validator** — inputs, permissions, manifest are sound.
- **Plugin Executor** — the subprocess mechanics.
- **Plugin Sandbox** — the isolation boundary (resource limits, allowlists).

## Finding Engine (formerly "Result Normalizer")

The Finding Engine owns the *truth* about findings after a plugin runs. It performs:

- normalization (raw → canonical `SecurityFinding`)
- deduplication (by deterministic fingerprint)
- enrichment (asset context, historical data)
- correlation (cross-plugin, cross-asset)
- confidence adjustment
- tagging
- MITRE / OWASP / CWE mapping
- CVE enrichment
- merging of equivalent findings

Normalization is the first 10% of this responsibility; the module takes the name of the whole concern.

## Risk Engine

The Risk Engine does not produce a single number in a vacuum. It composes:

- **Likelihood** — probability of exploitation, given context.
- **Impact** — what happens if exploited.
- **Exploitability** — concrete attack feasibility (public exploit, prerequisites).
- **Business Context** — asset criticality, exposure, compliance weight.
- → **Risk Score (0–100)**

The AI Gateway summarizes the resulting, already-prioritized findings.

## AI Gateway

The AI Gateway is decomposed into six sub-modules so each can evolve independently:

- **Provider Manager** — which providers exist; lifecycle (OpenAI, Anthropic, MiniMax, Ollama, Gemini, Nemotron, …).
- **Prompt Manager** — versioned, parameter-rendered prompt templates.
- **Context Builder** — assembles normalized findings + asset + history + policy into a context window.
- **Model Router** — selects provider/model per request (cost, capability, latency).
- **Token Manager** — budgets, accounting, retries, compression.
- **Response Parser** — safe parsing of model output back to typed structures.

Adding a new provider only requires implementing its adapter under `providers/` and registering it with `Provider Manager`. **All other AI Gateway modules are untouched.**

## AI Philosophy

- AI never executes scanning work.
- AI reasons about findings, not raw plugin output.
- AI receives normalized, risk-scored `SecurityFinding` objects — not raw payloads.
- AI is an analyst. Plugins are operators.

## Engineering Principles

- Every module independently testable.
- Every component has a single responsibility.
- Composition over inheritance.
- Dependency injection everywhere.
- Strong typing everywhere.
- No duplicated logic.
- No hardcoded values.
- Configuration first.
- Production-ready code only.
- Observability built in (structured logging, traces, metrics).

---

## Prompt Discipline (Authoritative for Every AI Session)

Every prompt — including this one — must, in order:

1. **Load `engineering/PROJECT_MANIFEST.md`** (this file).
2. **Load `engineering/rules/00_MASTER_RULES.md`.**
3. **Load the relevant supporting doc:**
   - Architecture question → `ARCHITECTURE.md`
   - Scope/deferral question → `MVP_SCOPE.md`
   - Sequencing question → `ROADMAP.md`
   - Coding question → `CODING_STANDARDS.md`
4. Then state the task.

If there is a conflict between documents, **this file wins**, then `00_MASTER_RULES.md`, then the relevant doc.

If a task is unclear, an AI engineer must **stop and ask**, not invent architecture.

---

## Non-Goals (for the current platform)

These are **explicitly out of scope** for the MVP and the immediate roadmap. Building any of them requires a separate, approved initiative.

- No EDR
- No SIEM
- No SOAR
- No SOC
- No active exploitation
- No credential attacks
- No lateral movement
- No C2
- No malware
- No persistence mechanisms
- No privilege escalation tooling
- No Active Directory attack framework
- No autonomous exploitation

This is an **AI-assisted security assessment platform**, not an offensive toolkit.

---

## Future Application Inventory (non-binding)

When the platform can support them, these applications reuse AI-SecOS Core without change:

- Cloud Security
- AI Security
- Threat Modeling
- Secure Code Review
- Runtime Defense
- Compliance
- Executive Risk Intelligence