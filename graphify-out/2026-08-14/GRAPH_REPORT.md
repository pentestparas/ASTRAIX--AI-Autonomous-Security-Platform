# Graph Report - astraix-security-analyst  (2026-08-14)

## Corpus Check
- 258 files · ~180,997 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3197 nodes · 7705 edges · 165 communities (136 shown, 29 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 980 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5daafb02`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- _HttpAdapter
- api.py
- api.ts
- vapt_platforms.py
- plugin_system/executor.py
- risk_engine/engine.py
- PluginRegistry
- Container
- organizations.py
- CapabilityRegistry
- VAPTAdapter
- core/auth.py
- v1/auth.py
- _KaliToolAdapter
- SecurityFinding
- stream.py
- Orchestrator
- VAPTScanRequest
- [id]/page.tsx
- vapt/routes.py
- shared/__init__.py
- Workflow
- VAPTScanType
- MembershipRepository
- BaseModel
- ToolRegistry
- FastAPI Backend
- scans/page.tsx
- PluginManifest
- devDependencies
- RoleName
- ScannerExecutor
- LyrieAIAgent
- ReportFormat
- VAPTScanResult
- dependencies
- PlannerAgent
- Knowledge Base Corpus
- _MutableContainer
- VAPTExecutor
- VAPTFinding
- assessments.py
- v1/__init__.py
- RecentAssessments.tsx
- ScanController
- ProviderManager
- AstraIX Full-Spectrum Platform Vision
- assets.py
- BasePlugin
- AssetIdentifier
- compilerOptions
- Orchestrator
- SystemStatus.tsx
- Finding Engine
- VAPT Executor (executor.py)
- UserRepository
- .run
- Finding
- findings/page.tsx
- PromptManager
- metrics.py
- KnowledgeGraph
- kb.py
- Unified Security Hub
- kaggle-security-datasets/build.py
- ResponseSchema
- Auth API (auth.py)
- XalgorixAdapter
- ai_gateway/__init__.py
- garak_scanner.py
- infrastructure/__init__.py
- infrastructure/logging.py
- CSKB Sibling Docker Image
- Cybersecurity Knowledge Base
- ScanProgressBus
- Severity
- graph/page.tsx
- BaseRepository
- web_form_scanner.py
- AI-SecOS Core
- httpx/main.py
- PluginExecutor
- container.py
- PROJECT.md
- nmap/main.py
- PluginSandbox
- New batch (curated + API-verified — 22 datasets)
- NmapScanner
- OrganizationRepository
- results.py
- Release 0.1.0
- settings/page.tsx
- AdapterScanResult
- run_nuclei_scan
- run_semgrep_scan
- run_subfinder
- VerifierAgent
- run_trivy_scan
- to_severity
- scripts
- BaseSchema
- PluginRegistry
- .validate_invocation
- vapt/normalizer.py
- CHECKPOINT — AstraIX continuation point
- ASTRAIX Product Overview
- test_health.py
- System Architecture
- ToolAvailabilityChecker
- HTTPX Scanner Plugin
- Master AI Engineer Rules
- External VAPT Platform Adapters
- wordlists.py
- fetch-wordlists.sh
- ai_secos_core/tests/conftest.py
- Report Base Template (base.html)
- download.sh
- AstraIX Platform Constitution
- app/layout.tsx
- graphify.js
- eslint.config.mjs
- Project Roadmap
- AstraIX App Icon
- useActiveScansStore
- lucide-react
- @radix-ui/react-slot
- reactflow
- Technology Stack
- @types/dagre
- prettier-plugin-tailwindcss
- @types/node
- @types/react
- Trivy Security Scanner Plugin
- .get_tool_config
- astraix-backend
- Cloud Security Posture Assessment
- Static Application Security Testing
- entrypoint.sh
- next.config.js
- next-env.d.ts
- @hookform/resolvers
- @radix-ui/react-dropdown-menu
- zod
- start-dev.sh
- Product Vision
- Plugin SDK Schema
- Prompt Templates
- Operational Rules

## God Nodes (most connected - your core abstractions)
1. `SecurityFinding` - 99 edges
2. `BaseModel` - 87 edges
3. `VAPTFinding` - 65 edges
4. `RoleName` - 60 edges
5. `VAPTExecutor` - 58 edges
6. `Container` - 54 edges
7. `_MutableContainer` - 47 edges
8. `MembershipRepository` - 42 edges
9. `ResponseSchema` - 42 edges
10. `build_default_container()` - 41 edges

## Surprising Connections (you probably didn't know these)
- `AI Integration Architecture` --semantically_similar_to--> `AI Gateway`  [INFERRED] [semantically similar]
  docs/ARCHITECTURE_OVERVIEW.md → AGENTS.md
- `Custom Kali Image (astraix-kali)` --semantically_similar_to--> `astraix-kali Image`  [INFERRED] [semantically similar]
  CHANGELOG.md → AGENTS.md
- `Frontend Dashboard` --semantically_similar_to--> `Next.js Frontend`  [INFERRED] [semantically similar]
  CHANGELOG.md → AGENTS.md
- `Real VAPT Pipeline` --semantically_similar_to--> `VAPT Executor (executor.py)`  [INFERRED] [semantically similar]
  CHANGELOG.md → AGENTS.md
- `Phase 1 VAPT Module` --semantically_similar_to--> `VAPT Executor (executor.py)`  [INFERRED] [semantically similar]
  docs/PRODUCT_OVERVIEW.md → AGENTS.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Multi-Agent VAPT Scan Pipeline** — agents_scan_quick_api, agents_recon_orchestrator, agents_planner_agent, agents_researcher_agent, agents_verifier_agent, agents_risk_engine, agents_ai_gateway [EXTRACTED 1.00]
- **Report Template Set (Jinja extends)** — backend_app_report_engine_templates_base_report, backend_app_report_engine_templates_compliance_report, backend_app_report_engine_templates_executive_report, backend_app_report_engine_templates_technical_report [EXTRACTED 1.00]
- **Docker Compose Service Stack** — docker_compose_postgres_service, docker_compose_redis_service, docker_compose_backend_service, docker_compose_frontend_service, docker_compose_nginx_service, docker_compose_neo4j_service [EXTRACTED 1.00]
- **Icon Composition (Background + Shield + Check)** — frontend_src_app_icon_rounded_square_background, frontend_src_app_icon_shield_shape, frontend_src_app_icon_check_mark [INFERRED 0.95]
- **Three-Layer Platform Model** — engineering_architecture_ai_secos_core, engineering_architecture_applications, engineering_architecture_plugins [EXTRACTED 1.00]
- **Capability Resolution Chain** — engineering_architecture_applications, engineering_architecture_capability, engineering_architecture_workflow, engineering_architecture_plugins, engineering_architecture_security_finding [EXTRACTED 1.00]
- **Asset Discovery Workflow Plugin Composition** — workflows_asset_discovery, plugins_subfinder_plugin, plugins_httpx_plugin, finding_engine, report_engine [EXTRACTED 1.00]
- **Cloud Posture Workflow Plugin Composition** — workflows_cloud_posture, plugins_trivy_plugin, finding_engine, report_engine [EXTRACTED 1.00]
- **Network VAPT Workflow Plugin Composition** — workflows_network_vapt, plugins_nmap_plugin, plugins_nuclei_plugin, finding_engine, report_engine [EXTRACTED 1.00]
- **Web VAPT Workflow Plugin Composition** — workflows_web_vapt, plugins_httpx_plugin, plugins_nuclei_plugin, finding_engine, report_engine [EXTRACTED 1.00]
- **Shared Risk Scoring Component** — finding_engine, workflows_asset_discovery, workflows_cloud_posture, workflows_code_audit, workflows_discovery, workflows_network_vapt, workflows_web_vapt [EXTRACTED 1.00]
- **Shared Reporting Component** — report_engine, workflows_asset_discovery, workflows_cloud_posture, workflows_code_audit, workflows_discovery, workflows_network_vapt, workflows_web_vapt [EXTRACTED 1.00]
- **Plugin SDK Schema Defines Plugin Structure** — plugins_core_plugin_sdk_plugin_sdk, plugins_httpx_plugin, plugins_nmap_plugin, plugins_nuclei_plugin, plugins_semgrep_plugin, plugins_subfinder_plugin, plugins_trivy_plugin [EXTRACTED 1.00]

## Communities (165 total, 29 thin omitted)

### Community 0 - "_HttpAdapter"
Cohesion: 0.12
Nodes (10): _HttpAdapter, PentagiAdapter, Any, PentAGI - fully autonomous pentesting agent (Go backend, REST API)., RedAmon - agentic red team framework (graph-powered, webapp API)., Base for adapters that talk to an external HTTP API., zen-ai-pentest GitHub Action adapter (CI/CD). Requires a GitHub repo with the…, RedamonAdapter (+2 more)

### Community 1 - "api.py"
Cohesion: 0.04
Nodes (95): assess(), AssessRequest, AssessResponse, _bootstrap(), FindingSummary, index(), list_capabilities(), Any (+87 more)

### Community 2 - "api.ts"
Cohesion: 0.06
Nodes (41): formats, MIME_TYPES, templateIcons, apiKeysApi, assessmentsApi, assetsApi, findingsApi, graphApi (+33 more)

### Community 3 - "vapt_platforms.py"
Cohesion: 0.09
Nodes (41): get_scanner_executor(), Scanner Executor Service Enterprise-grade scanner execution with: - Async tool…, Get the global scanner executor instance., AstraIX Security Scanner Module Enterprise-grade security scanning engine that…, Finding, Enum, str, Scanner Models Enterprise-grade data models for security scanning operations.… (+33 more)

### Community 4 - "plugin_system/executor.py"
Cohesion: 0.11
Nodes (30): Counter, Histogram, MetricsRegistry, Protocol, Monotonically increasing value, optionally labelled., Distribution value, optionally labelled., NoopTaskExecutor, PluginExecutionRequest (+22 more)

### Community 5 - "risk_engine/engine.py"
Cohesion: 0.07
Nodes (34): FindingContextPayload, Any, What the AI sees. Pre-serialization. The AI Gateway *never* receives the raw…, Convenience: flatten to a dict for string substitution., DefaultRiskEngine, _noop_severity_to_score(), NoopRiskEngine, Severity (+26 more)

### Community 6 - "PluginRegistry"
Cohesion: 0.09
Nodes (30): FindingOut, PluginError, PluginOutput, PluginStatus, PluginType, Enum, str, load_manifest() (+22 more)

### Community 8 - "Container"
Cohesion: 0.09
Nodes (32): build_app(), lifespan(), FastAPI, FastAPI app factory. Binds the DI container to the web transport. -…, Start/stop lifetime management., Create the FastAPI application. Mostly configures routing + middleware; DI…, Container, At boot, walk the plugins root and populate: - plugin registry - normalizer… (+24 more)

### Community 9 - "organizations.py"
Cohesion: 0.09
Nodes (46): ApiKeyCreate, create_api_key(), create_organization(), create_project(), delete_api_key(), delete_organization(), delete_project(), get_api_key() (+38 more)

### Community 10 - "CapabilityRegistry"
Cohesion: 0.06
Nodes (61): CapabilityAlreadyRegisteredError, CapabilityNotFoundError, CapabilityResolverError, Capability-specific error types., Raised when attempting to register a duplicate capability., Raised when capability resolution fails (missing workflow, etc.)., Raised when a capability is not found in the registry., Capability Registry — first-class Capability abstraction. Applications request… (+53 more)

### Community 11 - "VAPTAdapter"
Cohesion: 0.13
Nodes (18): AdapterStatus, Base classes and contracts for VAPT external adapters., True when the environment contains everything needed to attempt a run., True when the adapter should participate in scans., Return current availability status (should not raise)., Health/availability status of an adapter., Contract implemented by every external VAPT integration. Lifecycle during a…, VAPTAdapter (+10 more)

### Community 12 - "core/auth.py"
Cohesion: 0.15
Nodes (23): api_key_header, decode_token(), get_current_active_user(), get_current_superuser(), get_current_user(), get_role_permissions(), get_user_organizations(), get_user_projects() (+15 more)

### Community 13 - "v1/auth.py"
Cohesion: 0.09
Nodes (48): create_api_key(), create_organization(), create_project(), delete_organization(), delete_project(), get_api_key_repo(), get_membership_repo(), get_org_repo() (+40 more)

### Community 14 - "_KaliToolAdapter"
Cohesion: 0.09
Nodes (10): _ContainerRunner, _KaliToolAdapter, LyrieAdapter, Any, RaccoonAdapter, Raccoon recon scanner (DNS/WHOIS/TLS/WAF/subdomains/dir-busting)., Minimal Docker-socket runner for one-shot commands in the Kali image., Filter crash/traceback/banner noise out of tool output before parsing. (+2 more)

### Community 15 - "SecurityFinding"
Cohesion: 0.04
Nodes (84): AssessmentId, FindingCorrelator, Finding Correlator — the contract + the no-op default. Correlators detect…, Adds correlation metadata to findings., Return the same set of findings, possibly tagged with correlation., FindingDeduplicator, _max_or_none(), _merge() (+76 more)

### Community 16 - "stream.py"
Cohesion: 0.17
Nodes (15): emit_plugin_completed(), emit_plugin_finding(), emit_plugin_progress(), emit_plugin_started(), PluginCompletedPayload, PluginFindingPayload, PluginProgressPayload, PluginStartedPayload (+7 more)

### Community 17 - "Orchestrator"
Cohesion: 0.12
Nodes (20): Asset, get_orchestrator(), Orchestrator, Assessment, AsyncSession, UUID, Run real VAPT scan using Kali Linux tools. This is the enterprise-grade…, Run scan using the plugin system (fallback). (+12 more)

### Community 18 - "VAPTScanRequest"
Cohesion: 0.13
Nodes (7): Any, VAPTExecutor, Attach a callback for live progress events (scan_id, event_type, data)., ReconOrchestrator, Run exactly one tool against the target for the autonomous agent. Returns…, Request for a VAPT scan., VAPTScanRequest

### Community 19 - "[id]/page.tsx"
Cohesion: 0.12
Nodes (27): react, cvssColor(), fmtLabel(), ProjectDetailPage(), registrableDomain(), severityConfig, statusOptions, QuickAction (+19 more)

### Community 20 - "vapt/routes.py"
Cohesion: 0.07
Nodes (57): get_scan_controller(), Exception, Raised at a checkpoint when the scan was stopped by the user., ScanStoppedError, get_vapt_orchestrator(), adapters_health(), ApprovalDecision, _finding_fingerprint() (+49 more)

### Community 21 - "shared/__init__.py"
Cohesion: 0.09
Nodes (20): Capability, Workflow Engine — declarative Workflow + Capability resolution. A `Workflow` is…, Workflow + the chain of references used to compile it., WorkflowRecord, WorkflowResolutionError, ConfigurationError, FindingEngineError, Single error hierarchy for the entire AI-SecOS Core. Public API (the only types… (+12 more)

### Community 22 - "Workflow"
Cohesion: 0.06
Nodes (51): CancellationToken, CancelledError, Cancellation token for running tasks/plans. The platform-wide cancellation…, A typed alias for cancellation that originates from the platform., Lightweight, async-friendly cancellation., NoopTaskExecutor, Any, Task Executor — runs a Task. A planner produces Tasks; the executor is what… (+43 more)

### Community 23 - "VAPTScanType"
Cohesion: 0.10
Nodes (31): agent_loop_supported(), Autonomous VAPT Agent Loop (Phase 1) RedAmon-inspired agentic workflow: instead…, AI Planner Agent Decides the VAPT plan: which tools to run, in which phase, and…, get_vapt_executor(), ASTRAIX VAPT Module AI-Orchestrated Vulnerability Assessment & Penetration…, Enum, field_validator, str (+23 more)

### Community 24 - "MembershipRepository"
Cohesion: 0.09
Nodes (15): ApiKey, ApiKeyRepository, get_api_key_repo(), get_membership_repo(), get_organization_repo(), get_project_repo(), get_user_repo(), MembershipRepository (+7 more)

### Community 25 - "BaseModel"
Cohesion: 0.17
Nodes (42): ComplianceTag, A compliance framework mapping., An asset type a Capability can handle (e.g. 'domain', 'ip')., A Plugin a Capability depends on., RequiredPlugin, SupportedAssetType, ApiKeyCreate, ApiKeyCreateResponse (+34 more)

### Community 26 - "ToolRegistry"
Cohesion: 0.09
Nodes (20): get_tool_registry(), Enum, str, Kali Linux Security Tool Registry Comprehensive registry of security tools…, Tool categories matching VAPT workflow., Metadata about a security tool., Default configuration for a tool., Registry for managing security tools. (+12 more)

### Community 27 - "FastAPI Backend"
Cohesion: 0.09
Nodes (32): FastAPI Backend, Neo4j Knowledge Graph, Next.js Frontend, PostgreSQL, Redis, Alembic Migrations Dependency, asyncpg Dependency, FastAPI Dependency (+24 more)

### Community 28 - "scans/page.tsx"
Cohesion: 0.09
Nodes (28): Finding, getSeverityBadge(), getTypeIcon(), getTypeLabel(), LiveScanConsole(), phaseIcons, PlanPhase, PlanTool (+20 more)

### Community 29 - "PluginManifest"
Cohesion: 0.07
Nodes (37): Plugin System (PDK-facing contracts + platform internals). Public surface for…, LoadedPlugin, PluginLoader, PluginLoaderError, Path, PluginError, PluginManifest, Plugin Loader: read manifests from disk → PluginRecords. The Loader is the… (+29 more)

### Community 30 - "devDependencies"
Cohesion: 0.06
Nodes (31): autoprefixer, eslint, eslint-config-next, devDependencies, autoprefixer, eslint, eslint-config-next, jsdom (+23 more)

### Community 31 - "RoleName"
Cohesion: 0.20
Nodes (29): str, RoleName, ApiKeyBase, ApiKeyCreate, ApiKeyCreateResponse, ApiKeyRead, MembershipBase, MembershipCreate (+21 more)

### Community 32 - "ScannerExecutor"
Cohesion: 0.06
Nodes (29): PluginRegistry, Any, Finding, ScanRequest, VAPTExecutor, Execute a single tool., Create appropriate executor for scan request., Get tools for a scan request. (+21 more)

### Community 33 - "LyrieAIAgent"
Cohesion: 0.08
Nodes (18): LyrieAIAgent, Severity, Lyrie AI Agent executor for autonomous security operations. Features: - 7-phase…, Run 7-phase autonomous pentest. Args: target: URL or local path to pentest…, Scan URL or file for security issues. Checks: - Security headers (CSP, HSTS,…, AI red-team an LLM endpoint. Strategies: - crescendo: gradual escalation - tap:…, Calculate CVSS v3.1 score from vector. Args: vector: CVSS vector string (e.g.,…, Verify agent identity using Agent Trust Protocol. Args: agent_id: Agent… (+10 more)

### Community 34 - "ReportFormat"
Cohesion: 0.14
Nodes (26): _ai_comment_placeholder(), _build_section(), _findings_section(), ReportRequest, Report Engine — implementation. At Milestone 1, only the JSON/Markdown default…, Render reports from findings + risk scores., ReportEngine, _summary_section() (+18 more)

### Community 35 - "VAPTScanResult"
Cohesion: 0.12
Nodes (15): Result from a VAPT scan., VAPTScanResult, AIOrchestrator, Any, Analyze target and run the AI-planned scan with live progress events., Run the autonomous agent loop, falling back to the classic phased recon…, Run all enabled external adapters in parallel against the target. Adapters run…, Analyze target to understand what it is. (+7 more)

### Community 36 - "dependencies"
Cohesion: 0.07
Nodes (29): axios, class-variance-authority, clsx, d3-force, dagre, date-fns, dependencies, axios (+21 more)

### Community 37 - "PlannerAgent"
Cohesion: 0.16
Nodes (7): get_planner(), PlannerAgent, Any, Ask the LLM (NVIDIA NIM, falling back to Ollama) to refine tool selection.…, Generate the full phased VAPT plan with KB-grounded reasoning., Knowledge-base-grounded plan generator for VAPT scans., ResearcherAgent

### Community 38 - "Knowledge Base Corpus"
Cohesion: 0.12
Nodes (19): OWASP Projects (ADR Tier 3), paulveillard/cybersecurity (ADR Tier 1), Anthropic Cybersecurity Skills Repo, awesome-soc Repo, Berkanktk/CyberSecurity Repo, CAI (Cybersecurity AI) Repo, cybersecurity-knowledge-base Repo, Cybersecurity-Resources Repo (+11 more)

### Community 39 - "_MutableContainer"
Cohesion: 0.13
Nodes (16): build_default_container(), _MutableContainer, Mutable (thread-safe) wiring harness., Safely edit mutable values., Return a frozen copy ready for consumption., Wire default implementations for production runtime., NoopFindingCorrelator, Identity correlator. The default at Milestone 1. (+8 more)

### Community 40 - "VAPTExecutor"
Cohesion: 0.11
Nodes (19): Add a tool result and update aggregated findings., Result from a single security tool execution., ToolResult, ExternalTool, Any, ScanRequest, Execute a complete security scan., Get tools for a given capability. (+11 more)

### Community 41 - "VAPTFinding"
Cohesion: 0.06
Nodes (11): Synthetic findings so the agent loop works in demo mode., Reduce a URL target to bare host[:port] for host-oriented tools., Extract an explicit port from a URL target, else the scheme default., Map loopback targets to the Docker gateway host. Tool containers run in…, Emit findings ONLY when sqlmap confirms an injection point. sqlmap…, VAPTExecutor, Any, A security finding from VAPT scan. (+3 more)

### Community 42 - "assessments.py"
Cohesion: 0.15
Nodes (23): AssessmentModel, cancel_assessment(), create_assessment(), get_assessment(), list_assessments(), AsyncSession, delete, get (+15 more)

### Community 43 - "v1/__init__.py"
Cohesion: 0.06
Nodes (47): get_graph(), get, get_dashboard_activity(), get_dashboard_stats(), list_capabilities(), ping(), get, UUID (+39 more)

### Community 44 - "RecentAssessments.tsx"
Cohesion: 0.11
Nodes (22): statusConfig, FindingDetail(), formatDetails(), severityStyles, Badge(), BadgeProps, CardDescription, CardFooter (+14 more)

### Community 45 - "ScanController"
Cohesion: 0.10
Nodes (11): Any, Store the agent loop's partial results so an aborted/timed-out loop can still…, Register a pending operator decision for a dangerous tool call., Settle a pending approval. Returns False when unknown or already settled., Wait for the operator's decision. None = timed out / not resolved., A pending operator decision for a dangerous agent tool call., Registry + control flags for scans currently executing in-process., Track a running scan so control endpoints can reach its task. (+3 more)

### Community 46 - "ProviderManager"
Cohesion: 0.12
Nodes (14): ProviderAlreadyRegisteredError, ProviderManager, ProviderNotFoundError, Provider Manager. The Manager owns the lifecycle of providers. Applications…, Thread-safe registry of providers. The Manager is the *only* place providers…, AIProvider, Concrete providers (OpenAI/Anthropic/...) implement this., NullModelRouter (+6 more)

### Community 47 - "AstraIX Full-Spectrum Platform Vision"
Cohesion: 0.08
Nodes (31): AstraIX Security Analyst Platform, AI Core Layer, AI Integration Architecture, Data Architecture (Hot/Warm/Cold), Deployment Options, Integration Ecosystem (100+ Native), AstraIX Full-Spectrum Platform Vision, Platform Roadmap (5 Phases to 2027) (+23 more)

### Community 48 - "assets.py"
Cohesion: 0.09
Nodes (41): create_asset(), delete_asset(), get_asset(), list_assets(), AsyncSession, delete, get, patch (+33 more)

### Community 49 - "BasePlugin"
Cohesion: 0.10
Nodes (17): BasePlugin, FindingOut, PluginError, PluginOutput, PluginSchema, Parse stdin: str → dict., Structured logging accessible to orchestrator., Schema for plugin I/O, described in plugin.yml. (+9 more)

### Community 51 - "compilerOptions"
Cohesion: 0.07
Nodes (29): compilerOptions, allowJs, baseUrl, esModuleInterop, forceConsistentCasingInFileNames, incremental, isolatedModules, jsx (+21 more)

### Community 52 - "Orchestrator"
Cohesion: 0.14
Nodes (16): Orchestrator, Assessment, AsyncSession, Exception, Finding, PluginError, PluginOutput, PluginRegistry (+8 more)

### Community 53 - "SystemStatus.tsx"
Cohesion: 0.13
Nodes (9): QuickActions(), RecentFindings(), StatCardProps, StatsCards(), ComponentRowProps, SystemStatus(), dashboardApi, systemApi (+1 more)

### Community 54 - "Finding Engine"
Cohesion: 0.17
Nodes (21): Finding Engine, web/discovery capability, network/recon capability, network/vuln-scan capability, api/security capability, web/vuln-scan capability, HTTP Probe (httpx) Plugin, Nmap Port Scanner Plugin (+13 more)

### Community 55 - "VAPT Executor (executor.py)"
Cohesion: 0.18
Nodes (20): Docker Socket, KALI_IMAGE Env Var, VAPT_DEMO_MODE Env Var, VAPT_USE_DOCKER Env Var, gobuster, astraix-kali Image, nikto, nmap (+12 more)

### Community 56 - "UserRepository"
Cohesion: 0.15
Nodes (13): login(), login_json(), OAuth2 compatible login for Swagger UI., JSON-based login for frontend applications., Refresh access token., refresh_token(), create_access_token(), create_refresh_token() (+5 more)

### Community 57 - ".run"
Cohesion: 0.17
Nodes (13): AgentLoop, get_agent_loop(), Any, The autonomous tool-calling loop with phase + approval gating., Ground the agent with methodology guidance from the knowledge base, specific to…, Ground newly observed vuln classes in KB so the next tool decision exploits…, Return (rejected, reason) when the model may NOT write a final report yet -…, Call the LLM with function tools; return (text, tool_calls). Prefers NVIDIA NIM… (+5 more)

### Community 58 - "Finding"
Cohesion: 0.07
Nodes (36): do_run_migrations(), run_async_migrations(), run_migrations_online(), AsyncSession, post, Run a security assessment scan., run_assessment(), get_session() (+28 more)

### Community 59 - "findings/page.tsx"
Cohesion: 0.20
Nodes (15): cvssColor(), FindingsPage(), severityConfig, statusOptions, roleConfig, Card, CardContent, Table (+7 more)

### Community 60 - "PromptManager"
Cohesion: 0.14
Nodes (11): _InMemoryPromptManager, PromptManager, PromptTemplate, PromptVersionError, Any, Exception, Prompt Manager — versioned prompt templates. A `PromptTemplate` is a…, Raised when a requested `prompt_id` / version combination is unknown. (+3 more)

### Community 61 - "metrics.py"
Cohesion: 0.25
Nodes (3): _NoopCounter, _NoopHistogram, Metrics primitives (stubs at Milestone 1). These are typed protocols so…

### Community 62 - "KnowledgeGraph"
Cohesion: 0.16
Nodes (5): KnowledgeGraph, _node_id(), _node_tooltip(), Any, Record one agent-loop step as a ChainStep node linked to the target (target…

### Community 63 - "kb.py"
Cohesion: 0.18
Nodes (14): get_kb(), kb_context_for_finding(), kb_ready(), kb_snippets(), kb_sources_for(), kb_stats(), Any, Shared knowledge-base client for the whole VAPT AI pipeline. The AstraIX… (+6 more)

### Community 64 - "Unified Security Hub"
Cohesion: 0.13
Nodes (19): Application Security Module, Cloud Security Module, Dark-Moon Platform, Data Security Module, Defensive Security Module, Email Security Module, GRC & Compliance Module, Identity Security Module (+11 more)

### Community 65 - "kaggle-security-datasets/build.py"
Cohesion: 0.23
Nodes (19): find_dataset_dir(), handle_ai_generic(), handle_cve_generic(), handle_ids_generic(), handle_phish_generic(), handle_siem_generic(), main(), Path (+11 more)

### Community 66 - "ResponseSchema"
Cohesion: 0.12
Nodes (31): get_kb_source(), knowledge_stats(), list_kb_sources(), get, post, Search the cybersecurity knowledge base., Get knowledge base statistics., Rebuild FAISS vector index from chunks.json. (+23 more)

### Community 67 - "Auth API (auth.py)"
Cohesion: 0.14
Nodes (14): Auth API (auth.py), Demo Credentials, Quick Scan API Endpoint, VAPT Routes (routes.py), VAPT Scan Route Handler (route.ts), passlib/bcrypt Dependency, python-jose Dependency, JWT Auth System (+6 more)

### Community 69 - "ai_gateway/__init__.py"
Cohesion: 0.08
Nodes (43): ABC, ContextBuilder, NullContextBuilder, Context Builder — assembles what's fed into a prompt. Pre-AI responsibilities:…, Build a `FindingContextPayload` from typed inputs., Default at Milestone 1. Performs no compression or redaction. A future…, AIGateway, DefaultAIGateway (+35 more)

### Community 70 - "garak_scanner.py"
Cohesion: 0.20
Nodes (16): add(), _attempt_prompt(), direct_probe(), find_chat_endpoint(), guess_response_field(), http(), main(), parse_garak_report() (+8 more)

### Community 71 - "infrastructure/__init__.py"
Cohesion: 0.19
Nodes (11): platform_error_to_http_response(), PlatformErrorResponse, Map platform errors → HTTP responses. FastAPI exception handler in `platform/`…, Convert a PlatformError to a status/body pair. `correlation_id` is included so…, Cross-cutting infrastructure components. This package provides: - Structured…, get_correlation_id(), CorrelationId, Correlation id context. Every critical action (workflow, plugin exec, AI call)… (+3 more)

### Community 72 - "infrastructure/logging.py"
Cohesion: 0.10
Nodes (30): Platform-wide constants. Pure values that have no dependency on environment…, AI-SecOS Core configuration package. Single point of access to typed settings.…, AIGatewaySettings, FindingEngineSettings, load_settings(), ObservabilitySettings, PlatformSettings, BaseSettings (+22 more)

### Community 73 - "CSKB Sibling Docker Image"
Cohesion: 0.11
Nodes (19): CSKB Alternatives Considered, cs kb CLI, CSKB Platform Principles Compliance, CSKB Sibling Docker Image, cybersec_kb Python Package, ADR-001 CSKB Document, Aif4thah Dojo-101, ElNiak awesome-ai-cybersecurity (+11 more)

### Community 74 - "Cybersecurity Knowledge Base"
Cohesion: 0.17
Nodes (17): Cybersecurity Knowledge Base, Planner Agent, ReconOrchestrator, Researcher Agent, Verifier Agent, faiss-cpu Dependency, fastembed Dependency, kb-data Named Volume (+9 more)

### Community 75 - "ScanProgressBus"
Cohesion: 0.25
Nodes (5): Any, Drop all stored events/status for a scan (used on restart)., List scans that are still running (non-terminal status)., Publishes and reads scan progress events (Redis-backed, in-memory fallback)., ScanProgressBus

### Community 76 - "Severity"
Cohesion: 0.21
Nodes (15): Enum, Severity levels, ordered from informational to critical., Severity, details_env(), _dict_to_security_finding(), _finding_to_security_finding(), generate_report(), GenerateReportRequest (+7 more)

### Community 77 - "graph/page.tsx"
Cohesion: 0.07
Nodes (22): bubbleSize(), BubbleView(), computeLayout(), edgeColor(), fetchAllFindings(), GraphNodeData, GraphPage(), GROUP_ANCHORS (+14 more)

### Community 78 - "BaseRepository"
Cohesion: 0.23
Nodes (8): BaseRepository, AsyncSession, T, UUID, Generic repository for any model., List with pagination and optional filters., Count records with optional filters., Create a new instance.

### Community 79 - "web_form_scanner.py"
Cohesion: 0.33
Nodes (12): add(), has_error_markers(), http(), main(), probe_chatbot(), probe_nosql_injection(), probe_sql_injection(), probe_xss_forms() (+4 more)

### Community 80 - "AI-SecOS Core"
Cohesion: 0.18
Nodes (14): AI Gateway Module, AI-SecOS Core, Infrastructure Module, Domain Models Module, Normalizer Module, Platform Bootstrap Module, Plugin System Module, Report Engine Module (+6 more)

### Community 81 - "httpx/main.py"
Cohesion: 0.20
Nodes (14): _add(), _detect_cdn(), _detect_technologies(), _extract_title(), main(), probe_target(), Any, Extract version from header like 'nginx/1.21.6'. (+6 more)

### Community 82 - "PluginExecutor"
Cohesion: 0.24
Nodes (7): PluginExecutor, CorrelationId, Drive asyncio's subprocess for one plugin invocation., Convert non-JSON values to strings, swallowing exceptions., Async-first plugin executor with deterministic safety., _safe(), _truncate_bytes()

### Community 83 - "container.py"
Cohesion: 0.13
Nodes (13): Dependency Injection container. Uses DI’y to wire the entire platform without…, # TODO: Lookup normalizer + register, DefaultFindingFingerprinter, FindingFingerprinter, Deterministic fingerprinting contract. Two findings with identical `(asset,…, Computes fingerprints for findings., Default deterministic fingerprinter. The hash is built from fields that…, Stable byte representation (sorted keys, list-of-tuples). (+5 more)

### Community 84 - "PROJECT.md"
Cohesion: 0.14
Nodes (12): Communication, In Scope (PoC), Mission, Out of Scope (PoC), Project Charter, Project Overview, Risks & Mitigations, Scope (+4 more)

### Community 85 - "nmap/main.py"
Cohesion: 0.24
Nodes (13): build_nmap_command(), main(), _parse_host(), parse_nmap_xml(), _parse_port(), Any, Parse a single host element., Parse a port element. (+5 more)

### Community 86 - "PluginSandbox"
Cohesion: 0.20
Nodes (6): PluginRegistry, PluginSandbox, Path, PluginManifest, Translate the decision + manifest into a safe subprocess argv. The intermediate…, Decides what is allowed for a given plugin. The decision is deterministic and…

### Community 87 - "New batch (curated + API-verified — 22 datasets)"
Cohesion: 0.17
Nodes (11): A. Vulnerabilities & CVE / exploit data, Already ingested (existing 3 — DO NOT re-download), B. Network intrusion & malware traffic, C. Malware, D. Phishing / URL / email security, E. Threat intel / SIEM / logs, Expected totals (rough estimate), F. AI / LLM security (+3 more)

### Community 88 - "NmapScanner"
Cohesion: 0.22
Nodes (6): NmapScanner, PluginError, PluginOutput, Run as process: stdin → scan → stdout, Run nmap, parse output, return findings., Parse Nmap XML/text → findings.

### Community 90 - "results.py"
Cohesion: 0.18
Nodes (12): fail(), Failure, is_failure(), is_ok(), ok(), Any, T, Result type (Rust/Python-port idiom) for explicit success/failure. Used by… (+4 more)

### Community 91 - "Release 0.1.0"
Cohesion: 0.12
Nodes (18): AI Gateway, Finding Normalizer (normalizer.py), Gemini AI, Kali Tools Dockerfile, Risk Scoring Engine, OpenAI SDK Dependency, Gemini AI Summaries, Custom Kali Image (astraix-kali) (+10 more)

### Community 92 - "settings/page.tsx"
Cohesion: 0.27
Nodes (5): Input, InputProps, authApi, organizationsApi, Organization

### Community 93 - "AdapterScanResult"
Cohesion: 0.29
Nodes (4): AdapterScanResult, Result of an adapter-run scan phase., DarkMoonAdapter, Dark-Moon autonomous pentest platform. Mode A (HTTP): DARKMOON_BASE_URL +…

### Community 94 - "run_nuclei_scan"
Cohesion: 0.33
Nodes (8): build_nuclei_command(), main(), parse_nuclei_json(), Any, Execute nuclei and return parsed results., Build nuclei command arguments., Parse nuclei JSON output lines., run_nuclei_scan()

### Community 95 - "run_semgrep_scan"
Cohesion: 0.33
Nodes (8): build_semgrep_command(), main(), parse_semgrep_results(), Any, Build semgrep command arguments., Parse semgrep JSON output., Execute semgrep and return parsed results., run_semgrep_scan()

### Community 96 - "run_subfinder"
Cohesion: 0.33
Nodes (8): build_subfinder_command(), main(), parse_subfinder_json(), Any, Build subfinder command arguments., Parse subfinder JSON output lines., Execute subfinder and return parsed results., run_subfinder()

### Community 97 - "VerifierAgent"
Cohesion: 0.27
Nodes (3): Best-effort lookup of exploitation/technique guidance in the knowledge base for…, Verify findings concurrently (bounded) so long-running re-exploits (e.g.…, VerifierAgent

### Community 98 - "run_trivy_scan"
Cohesion: 0.33
Nodes (8): build_trivy_command(), main(), parse_trivy_results(), Any, Build trivy command arguments., Parse trivy JSON output., Execute trivy and return parsed results., run_trivy_scan()

### Community 99 - "to_severity"
Cohesion: 0.22
Nodes (5): Any, Adapters are skipped for targets they cannot meaningfully test., Execute the adapter against ``target``. Must never raise - errors are captured…, Map arbitrary severity strings from external tools to VAPTSeverity., to_severity()

### Community 100 - "scripts"
Cohesion: 0.14
Nodes (13): name, private, scripts, build, dev, format, lint, start (+5 more)

### Community 101 - "BaseSchema"
Cohesion: 0.28
Nodes (6): BaseSchema, PaginatedResponse, Base schema with ORM mode enabled., Standard success response wrapper., Paginated results wrapper., ResponseSchema

### Community 103 - ".validate_invocation"
Cohesion: 0.32
Nodes (5): Any, PluginManifest, Tiny subset of JSON Schema type matching for type-checking most params., _type_match(), ValidationResult

### Community 104 - "vapt/normalizer.py"
Cohesion: 0.36
Nodes (7): canonical_vuln_name(), cvss_for_severity(), normalize_finding(), normalize_findings(), Finding normalization: canonical vulnerability names + CVSS scores. Raw tool…, Map a raw finding title/type onto a standard vulnerability name., Return the finding with a canonical title/type and a CVSS score.

### Community 105 - "CHECKPOINT — AstraIX continuation point"
Cohesion: 0.29
Nodes (6): 1. System state after restart, 2. Product features live right now, 3. Scan history (validated), 4. Known issues / gotchas, 5. Next steps (when resuming), CHECKPOINT — AstraIX continuation point

### Community 106 - "ASTRAIX Product Overview"
Cohesion: 0.33
Nodes (6): PostgreSQL Service (postgres:16-alpine), Database Schema (Core Tables), Product Deployment Architecture, ASTRAIX Product Overview, Target Market, Phase 1 VAPT Module

### Community 107 - "test_health.py"
Cohesion: 0.43
Nodes (6): AsyncClient, client(), asyncio, fixture, test_health_check(), test_root()

### Community 108 - "System Architecture"
Cohesion: 0.25
Nodes (9): System Architecture, Applications Layer, Plugin Executor, Plugin Manager, Plugin Sandbox, Plugin Validator, Plugins Layer, SecurityPlugin PDK (+1 more)

### Community 110 - "ToolAvailabilityChecker"
Cohesion: 0.27
Nodes (6): Check which tools are available in the environment., Check if a specific tool is available., Check if Docker is available., Get availability status of all tools., Get overall health status of the scanner., ToolAvailabilityChecker

### Community 111 - "HTTPX Scanner Plugin"
Cohesion: 0.25
Nodes (8): Network Vulnerability Assessment, External Asset Discovery, Web Discovery, Web Application Security Assessment, HTTPX Scanner Plugin, Nmap Scanner Plugin, Nuclei Scanner Plugin, Subfinder Scanner Plugin

### Community 112 - "Master AI Engineer Rules"
Cohesion: 0.25
Nodes (8): Coding Standards, Python Standards, TypeScript Standards, MVP Scope Definition, Build Later Items, Build Now Items, Never Build Items, Master AI Engineer Rules

### Community 114 - "External VAPT Platform Adapters"
Cohesion: 0.29
Nodes (6): Adapters, Configuration, Deploying an external platform, External VAPT Platform Adapters, Health, How it works

### Community 116 - "wordlists.py"
Cohesion: 0.40
Nodes (5): _probe_image(), Wordlist resolver — curated wordlists baked into the astraix-kali image. Lists…, Purpose -> {path, lines, present} verified inside the Kali image., Run one `wc -l` over every curated list inside the Kali image., wordlist_health()

### Community 117 - "fetch-wordlists.sh"
Cohesion: 0.67
Nodes (5): dedupe(), fetch(), fetch_soft(), log(), fetch-wordlists.sh script

### Community 119 - "ai_secos_core/tests/conftest.py"
Cohesion: 0.40
Nodes (3): event_loop(), fixture, AI-SecOS Core test entrypoint.

### Community 120 - "Report Base Template (base.html)"
Cohesion: 0.48
Nodes (7): Report Base Template (base.html), Severity Badge Styles, Compliance Report Template, Executive Report Template, Technical Report Template, Jinja2 Dependency, WeasyPrint Dependency

### Community 121 - "download.sh"
Cohesion: 0.60
Nodes (4): BATCH, download_one(), run_one(), download.sh script

### Community 122 - "AstraIX Platform Constitution"
Cohesion: 0.29
Nodes (7): Capability Abstraction, Workflow Abstraction, AstraIX Platform Constitution, AI-SecOS Core Runtime, Plugin System, Risk Engine, Security Analyst Application

### Community 130 - "Project Roadmap"
Cohesion: 0.33
Nodes (6): Project Roadmap, Milestone 1 - AI-SecOS Core, Milestone 2 - First Plugin httpx, Milestone 3 - Discovery Capability, Milestone 4 - Web Security Assessment, Milestone 5 - Security Analyst UI

### Community 131 - "AstraIX App Icon"
Cohesion: 0.47
Nodes (6): AstraIX App Icon, White Check Mark, Slate and Cyan Palette, Rounded Square Background, Security Branding Motif, Cyan Shield Glyph

### Community 132 - "useActiveScansStore"
Cohesion: 0.24
Nodes (7): RecentAssessments(), navigation, settingsNav, Sidebar(), ActiveScan, ActiveScansState, useActiveScansStore

### Community 136 - "Technology Stack"
Cohesion: 0.40
Nodes (5): Technology Stack, AI Tech Stack, Backend Tech Stack, DevOps Tech Stack, Frontend Tech Stack

### Community 148 - "Trivy Security Scanner Plugin"
Cohesion: 0.50
Nodes (4): Trivy Security Scanner Plugin, cloud/posture capability, container/security capability, iac/security capability

## Knowledge Gaps
- **314 isolated node(s):** `astraix-backend`, `entrypoint.sh script`, `eslintConfig`, `nextConfig`, `name` (+309 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BaseModel` connect `BaseModel` to `api.py`, `vapt_platforms.py`, `PluginRegistry`, `SecurityFinding`, `VAPTScanRequest`, `vapt/routes.py`, `shared/__init__.py`, `Workflow`, `VAPTScanType`, `PluginManifest`, `RoleName`, `VAPTScanResult`, `VAPTExecutor`, `VAPTFinding`, `assessments.py`, `assets.py`, `BasePlugin`, `Finding`, `Severity`, `BaseSchema`?**
  _High betweenness centrality (0.122) - this node is a cross-community bridge._
- **Why does `SecurityFinding` connect `SecurityFinding` to `api.py`, `ReportFormat`, `risk_engine/engine.py`, `ai_gateway/__init__.py`, `_MutableContainer`, `Severity`, `container.py`, `shared/__init__.py`, `Workflow`, `BaseModel`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Why does `Asset` connect `api.py` to `OrganizationRepository`, `UserRepository`, `BaseRepository`, `Orchestrator`, `AssetIdentifier`, `vapt/routes.py`, `MembershipRepository`, `BaseModel`, `Finding`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `SecurityFinding` (e.g. with `ContextBuilder` and `FindingContextPayload`) actually correct?**
  _`SecurityFinding` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Are the 52 inferred relationships involving `RoleName` (e.g. with `ApiKeyCreate` and `ApiKeyCreateResponse`) actually correct?**
  _`RoleName` has 52 INFERRED edges - model-reasoned connections that need verification._
- **What connects `astraix-backend`, `entrypoint.sh script`, `eslintConfig` to the rest of the system?**
  _314 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `_HttpAdapter` be split into smaller, more focused modules?**
  _Cohesion score 0.11931818181818182 - nodes in this community are weakly interconnected._