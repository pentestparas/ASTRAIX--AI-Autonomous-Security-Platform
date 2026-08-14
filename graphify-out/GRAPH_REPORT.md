# Graph Report - astraix-security-analyst  (2026-08-14)

## Corpus Check
- 255 files · ~177,038 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3154 nodes · 7622 edges · 171 communities (144 shown, 27 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 981 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f1ed9147`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- VAPTAdapter
- api.py
- api.ts
- vapt_platforms.py
- plugin_system/executor.py
- Severity
- PluginRegistry
- Container
- organizations.py
- capabilities/loader.py
- health_check
- get_current_user
- OrganizationRepository
- _KaliToolAdapter
- FindingNormalizer
- EventDispatcher
- FindingEvidence
- Workflow
- [id]/page.tsx
- get_scan_controller
- DefaultWorkflowEngine
- DefaultTaskPlanner
- VAPTScanType
- MembershipRepository
- BaseModel
- ToolRegistry
- FastAPI Backend
- scans/page.tsx
- PluginRegistry
- devDependencies
- RoleName
- ScannerExecutor
- LyrieAIAgent
- ReportFormat
- AIOrchestrator
- dependencies
- PlannerAgent
- Knowledge Base Corpus
- ._create_executor
- VAPTExecutor
- VAPTFinding
- AssessmentRead
- vapt/routes.py
- RecentAssessments.tsx
- ScanController
- ProviderManager
- AstraIX Full-Spectrum Platform Vision
- findings.py
- BasePlugin
- Asset
- compilerOptions
- Orchestrator
- SystemStatus.tsx
- Finding Engine
- VAPT Executor (executor.py)
- assets.py
- .run
- domain/models/__init__.py
- findings/page.tsx
- PromptManager
- MetricsRegistry
- KnowledgeGraph
- Settings
- Unified Security Hub
- kaggle-security-datasets/build.py
- plugins.py
- PostgreSQL
- XalgorixAdapter
- container.py
- app/models/base.py
- CapabilityRegistry
- infrastructure/logging.py
- AI Gateway
- Cybersecurity Knowledge Base
- httpx.py
- value_objects.py
- graph/page.tsx
- BaseRepository
- ResponseSchema
- AI-SecOS Core
- httpx/main.py
- shared/assessment.py
- SecurityFinding
- PROJECT.md
- nmap/main.py
- TokenBudget
- New batch (curated + API-verified — 22 datasets)
- NmapScanner
- semgrep.py
- shared/__init__.py
- Release 0.1.0
- settings/page.tsx
- error_handlers.py
- run_nuclei_scan
- run_semgrep_scan
- run_subfinder
- VerifierAgent
- run_trivy_scan
- workflow.py
- scripts
- BaseSchema
- nuclei.py
- .validate_invocation
- vapt/normalizer.py
- KB Source List (Tier 1-3)
- Network VAPT Workflow
- test_health.py
- System Architecture
- FindingContextPayload
- ToolAvailabilityChecker
- HTTPX Scanner Plugin
- Master AI Engineer Rules
- ToolResult
- External VAPT Platform Adapters
- schemas/base.py
- wordlists.py
- fetch-wordlists.sh
- Auth API (auth.py)
- ai_secos_core/tests/conftest.py
- Report Base Template (base.html)
- download.sh
- AstraIX Platform Constitution
- app/layout.tsx
- graphify.js
- select_first_providers
- env.py
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
3. `VAPTFinding` - 63 edges
4. `RoleName` - 60 edges
5. `VAPTExecutor` - 57 edges
6. `Container` - 54 edges
7. `_MutableContainer` - 47 edges
8. `MembershipRepository` - 42 edges
9. `ResponseSchema` - 42 edges
10. `build_default_container()` - 41 edges

## Surprising Connections (you probably didn't know these)
- `Custom Kali Image (astraix-kali)` --semantically_similar_to--> `astraix-kali Image`  [INFERRED] [semantically similar]
  CHANGELOG.md → AGENTS.md
- `Frontend Dashboard` --semantically_similar_to--> `Next.js Frontend`  [INFERRED] [semantically similar]
  CHANGELOG.md → AGENTS.md
- `Real VAPT Pipeline` --semantically_similar_to--> `VAPT Executor (executor.py)`  [INFERRED] [semantically similar]
  CHANGELOG.md → AGENTS.md
- `Phase 1 VAPT Module` --semantically_similar_to--> `VAPT Executor (executor.py)`  [INFERRED] [semantically similar]
  docs/PRODUCT_OVERVIEW.md → AGENTS.md
- `CSKB Sibling Docker Image` --semantically_similar_to--> `Cybersecurity Knowledge Base`  [INFERRED] [semantically similar]
  engineering/adr/001-cskb.md → AGENTS.md

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

## Communities (171 total, 27 thin omitted)

### Community 0 - "VAPTAdapter"
Cohesion: 0.05
Nodes (39): AdapterScanResult, AdapterStatus, Any, Base classes and contracts for VAPT external adapters., True when the environment contains everything needed to attempt a run., True when the adapter should participate in scans., Adapters are skipped for targets they cannot meaningfully test., Return current availability status (should not raise). (+31 more)

### Community 1 - "api.py"
Cohesion: 0.08
Nodes (55): assess(), AssessRequest, AssessResponse, _bootstrap(), FindingSummary, index(), list_capabilities(), Any (+47 more)

### Community 2 - "api.ts"
Cohesion: 0.06
Nodes (41): formats, MIME_TYPES, templateIcons, apiKeysApi, assessmentsApi, assetsApi, findingsApi, graphApi (+33 more)

### Community 3 - "vapt_platforms.py"
Cohesion: 0.09
Nodes (41): get_scanner_executor(), Scanner Executor Service Enterprise-grade scanner execution with: - Async tool…, Get the global scanner executor instance., AstraIX Security Scanner Module Enterprise-grade security scanning engine that…, Finding, Enum, str, Scanner Models Enterprise-grade data models for security scanning operations.… (+33 more)

### Community 4 - "plugin_system/executor.py"
Cohesion: 0.07
Nodes (41): NoopTaskExecutor, PluginExecutionRequest, PluginExecutionResult, PluginExecutionStatus, Enum, str, Plugin Executor: drives the subprocess lifecycle. Owns the *mechanics*: -…, Drive asyncio's subprocess for one plugin invocation. (+33 more)

### Community 5 - "Severity"
Cohesion: 0.09
Nodes (32): DefaultRiskEngine, _noop_severity_to_score(), NoopRiskEngine, Severity, Risk Engine — pipeline orchestrator and entry points. Two implementations are…, Identity: score derived directly from canonical severity. Used in tests and as…, A scored finding (or a typed wrapper around a SecurityFinding)., Engine port: score one or more canonical findings. (+24 more)

### Community 6 - "PluginRegistry"
Cohesion: 0.06
Nodes (41): Asset, Orchestrator, Assessment, AsyncSession, UUID, Run real VAPT scan using Kali Linux tools. This is the enterprise-grade…, Run scan using the plugin system (fallback)., Process plugin findings, dedupe, persist. (+33 more)

### Community 8 - "Container"
Cohesion: 0.08
Nodes (38): build_app(), lifespan(), FastAPI, FastAPI app factory. Binds the DI container to the web transport. -…, Start/stop lifetime management., Create the FastAPI application. Mostly configures routing + middleware; DI…, build_default_container(), Container (+30 more)

### Community 9 - "organizations.py"
Cohesion: 0.09
Nodes (46): ApiKeyCreate, create_api_key(), create_organization(), create_project(), delete_api_key(), delete_organization(), delete_project(), get_api_key() (+38 more)

### Community 10 - "capabilities/loader.py"
Cohesion: 0.11
Nodes (36): Capability Registry — first-class Capability abstraction. Applications request…, CapabilityLoader, CapabilityLoaderError, LoadedCapability, _parse_asset_category(), _parse_framework(), _parse_manifest(), Path (+28 more)

### Community 11 - "health_check"
Cohesion: 0.29
Nodes (7): health_check(), get, Root endpoint: health/status overview., Basic liveness check., Readiness check (validates dependencies)., readiness_check(), root()

### Community 12 - "get_current_user"
Cohesion: 0.17
Nodes (19): api_key_header, decode_token(), get_current_active_user(), get_current_superuser(), get_current_user(), get_user_organizations(), get_user_projects(), AsyncSession (+11 more)

### Community 13 - "OrganizationRepository"
Cohesion: 0.09
Nodes (34): delete_organization(), delete_project(), get_organization(), get_project(), invite_member(), list_api_keys(), list_memberships(), list_organizations() (+26 more)

### Community 14 - "_KaliToolAdapter"
Cohesion: 0.07
Nodes (20): _ContainerRunner, _KaliToolAdapter, Any, RaccoonAdapter, Raccoon recon scanner (DNS/WHOIS/TLS/WAF/subdomains/dir-busting)., Minimal Docker-socket runner for one-shot commands in the Kali image., Filter crash/traceback/banner noise out of tool output before parsing., Base for tools installed inside the Kali image. (+12 more)

### Community 15 - "FindingNormalizer"
Cohesion: 0.12
Nodes (27): FindingCorrelator, NoopFindingCorrelator, Finding Correlator — the contract + the no-op default. Correlators detect…, Adds correlation metadata to findings., Identity correlator. The default at Milestone 1., DefaultFindingEngine, FindingEngine, FindingEngineConfig (+19 more)

### Community 16 - "EventDispatcher"
Cohesion: 0.10
Nodes (24): ProgressTicker, Streaming-aware Plugin Executor. Wraps the base `PluginExecutor` and emits…, Wraps a PluginExecutor to emit streaming events. The wrapper preserves the…, Background ticker to emit periodic plugin.progress events. Started when a…, StreamingPluginExecutor, emit_plugin_completed(), emit_plugin_finding(), emit_plugin_progress() (+16 more)

### Community 17 - "FindingEvidence"
Cohesion: 0.13
Nodes (21): _create_os_finding(), _normalize_host(), Any, Nmap Plugin — normalizer. Converts raw `nmap` output into canonical…, Create a finding for detected OS., Normalize all open ports from a host into findings., _normalize_one(), Any (+13 more)

### Community 18 - "Workflow"
Cohesion: 0.11
Nodes (28): CancelledError, A typed alias for cancellation that originates from the platform., PlannedExecution, Task Planner — the dynamic heart of the platform. Per ARCHITECTURE.md: -…, Top-level knobs for the planner., Outcome of one full plan run., Schedule and execute a Workflow as a DAG., TaskPlanner (+20 more)

### Community 19 - "[id]/page.tsx"
Cohesion: 0.12
Nodes (27): react, cvssColor(), fmtLabel(), ProjectDetailPage(), registrableDomain(), severityConfig, statusOptions, QuickAction (+19 more)

### Community 20 - "get_scan_controller"
Cohesion: 0.08
Nodes (44): get_scan_controller(), get_vapt_orchestrator(), adapters_health(), _finding_fingerprint(), get_assessment(), get_scan_progress(), list_approvals(), _mark_assessment_stopped() (+36 more)

### Community 21 - "DefaultWorkflowEngine"
Cohesion: 0.11
Nodes (19): CapabilityResolver, Any, Capability, Validate inputs against the capability's input schema (lightweight). Performs…, Raised when capability resolution fails., A Capability fully resolved to executable Workflows., Resolves Capabilities to WorkflowRecords ready for the Task Planner., ResolutionError (+11 more)

### Community 22 - "DefaultTaskPlanner"
Cohesion: 0.13
Nodes (17): CancellationToken, Cancellation token for running tasks/plans. The platform-wide cancellation…, Lightweight, async-friendly cancellation., NoopTaskExecutor, Any, Task Executor — runs a Task. A planner produces Tasks; the executor is what…, Run a single Task and emit a result., Default at Milestone 1. The executor performs the bare minimum: a `result`-only… (+9 more)

### Community 23 - "VAPTScanType"
Cohesion: 0.09
Nodes (36): agent_loop_supported(), Autonomous VAPT Agent Loop (Phase 1) RedAmon-inspired agentic workflow: instead…, get_planner(), AI Planner Agent Decides the VAPT plan: which tools to run, in which phase, and…, get_vapt_executor(), ASTRAIX VAPT Module AI-Orchestrated Vulnerability Assessment & Penetration…, Enum, field_validator (+28 more)

### Community 24 - "MembershipRepository"
Cohesion: 0.07
Nodes (23): ApiKey, get_api_key_repo(), get_membership_repo(), get_org_repo(), get_project_repo(), get_user_repo(), AsyncSession, ApiKeyRepository (+15 more)

### Community 25 - "BaseModel"
Cohesion: 0.14
Nodes (52): ApiKeyCreate, ApiKeyCreateResponse, ApiKeyResponse, create_api_key(), create_organization(), create_project(), login(), login_json() (+44 more)

### Community 26 - "ToolRegistry"
Cohesion: 0.09
Nodes (22): get_tool_registry(), Enum, str, Kali Linux Security Tool Registry Comprehensive registry of security tools…, Tool categories matching VAPT workflow., Metadata about a security tool., Default configuration for a tool., Registry for managing security tools. (+14 more)

### Community 27 - "FastAPI Backend"
Cohesion: 0.10
Nodes (28): FastAPI Backend, Neo4j Knowledge Graph, Next.js Frontend, Redis, FastAPI Dependency, Neo4j Driver Dependency, Pydantic v2 Dependency, redis Python Client Dependency (+20 more)

### Community 28 - "scans/page.tsx"
Cohesion: 0.09
Nodes (28): Finding, getSeverityBadge(), getTypeIcon(), getTypeLabel(), LiveScanConsole(), phaseIcons, PlanPhase, PlanTool (+20 more)

### Community 29 - "PluginRegistry"
Cohesion: 0.09
Nodes (20): LoadedPlugin, PluginLoader, PluginLoaderError, Path, PluginError, PluginManifest, Plugin Loader: read manifests from disk → PluginRecords. The Loader is the…, A loader-level result wrapping a successfully parsed manifest. (+12 more)

### Community 30 - "devDependencies"
Cohesion: 0.06
Nodes (31): autoprefixer, eslint, eslint-config-next, devDependencies, autoprefixer, eslint, eslint-config-next, jsdom (+23 more)

### Community 31 - "RoleName"
Cohesion: 0.20
Nodes (29): str, RoleName, ApiKeyBase, ApiKeyCreate, ApiKeyCreateResponse, ApiKeyRead, MembershipBase, MembershipCreate (+21 more)

### Community 32 - "ScannerExecutor"
Cohesion: 0.08
Nodes (22): PluginRegistry, Finding, Remove duplicate findings based on fingerprint., Compute unique fingerprint for a finding., Main scanner execution service. Features: - Multi-tool execution with Docker…, ScannerExecutor, Finding, Parse Nmap text output as fallback. (+14 more)

### Community 33 - "LyrieAIAgent"
Cohesion: 0.09
Nodes (16): LyrieAIAgent, Severity, Lyrie AI Agent executor for autonomous security operations. Features: - 7-phase…, Run 7-phase autonomous pentest. Args: target: URL or local path to pentest…, Scan URL or file for security issues. Checks: - Security headers (CSP, HSTS,…, AI red-team an LLM endpoint. Strategies: - crescendo: gradual escalation - tap:…, Calculate CVSS v3.1 score from vector. Args: vector: CVSS vector string (e.g.,…, Verify agent identity using Agent Trust Protocol. Args: agent_id: Agent… (+8 more)

### Community 34 - "ReportFormat"
Cohesion: 0.10
Nodes (44): _ai_comment_placeholder(), _build_section(), _findings_section(), NullReportEngine, ReportRequest, Report Engine — implementation. At Milestone 1, only the JSON/Markdown default…, Render reports from findings + risk scores., JSON/Markdown default at Milestone 1. Produces deterministic artefacts using… (+36 more)

### Community 35 - "AIOrchestrator"
Cohesion: 0.08
Nodes (25): get_knowledge_graph(), Exception, Scan Control Channel In-process control plane for active scans: pause, resume,…, Cooperative pause/stop gate. No-op for scans that are not registered. While…, Raised at a checkpoint when the scan was stopped by the user., ScanStoppedError, AIOrchestrator, Any (+17 more)

### Community 36 - "dependencies"
Cohesion: 0.07
Nodes (29): axios, class-variance-authority, clsx, d3-force, dagre, date-fns, dependencies, axios (+21 more)

### Community 37 - "PlannerAgent"
Cohesion: 0.23
Nodes (5): PlannerAgent, Any, Ask the LLM (NVIDIA NIM, falling back to Ollama) to refine tool selection.…, Generate the full phased VAPT plan with KB-grounded reasoning., Knowledge-base-grounded plan generator for VAPT scans.

### Community 38 - "Knowledge Base Corpus"
Cohesion: 0.12
Nodes (19): OWASP Projects (ADR Tier 3), paulveillard/cybersecurity (ADR Tier 1), Anthropic Cybersecurity Skills Repo, awesome-soc Repo, Berkanktk/CyberSecurity Repo, CAI (Cybersecurity AI) Repo, cybersecurity-knowledge-base Repo, Cybersecurity-Resources Repo (+11 more)

### Community 39 - "._create_executor"
Cohesion: 0.21
Nodes (8): Any, ScanRequest, VAPTExecutor, Create appropriate executor for scan request., Get tools for a scan request., Get default tools for a capability., Build execution context for tools., Execute a complete security scan.

### Community 40 - "VAPTExecutor"
Cohesion: 0.14
Nodes (16): ExternalTool, Any, ScanRequest, Execute a complete security scan., Get tools for a given capability., Enterprise VAPT Execution Engine Features: - Multi-platform support (Kali,…, Execute a single tool and return parsed findings., Execute multiple tools in parallel. (+8 more)

### Community 41 - "VAPTFinding"
Cohesion: 0.06
Nodes (10): Run exactly one tool against the target for the autonomous agent. Returns…, Synthetic findings so the agent loop works in demo mode., Reduce a URL target to bare host[:port] for host-oriented tools., Extract an explicit port from a URL target, else the scheme default., Map loopback targets to the Docker gateway host. Tool containers run in…, Emit findings ONLY when sqlmap confirms an injection point. sqlmap…, VAPTExecutor, Any (+2 more)

### Community 42 - "AssessmentRead"
Cohesion: 0.13
Nodes (23): AssessmentModel, cancel_assessment(), create_assessment(), get_assessment(), list_assessments(), AsyncSession, delete, get (+15 more)

### Community 43 - "vapt/routes.py"
Cohesion: 0.06
Nodes (69): get_dashboard_activity(), get_dashboard_stats(), list_capabilities(), ping(), AsyncSession, get, post, UUID (+61 more)

### Community 44 - "RecentAssessments.tsx"
Cohesion: 0.11
Nodes (22): statusConfig, FindingDetail(), formatDetails(), severityStyles, Badge(), BadgeProps, CardDescription, CardFooter (+14 more)

### Community 45 - "ScanController"
Cohesion: 0.10
Nodes (11): Any, Store the agent loop's partial results so an aborted/timed-out loop can still…, Register a pending operator decision for a dangerous tool call., Settle a pending approval. Returns False when unknown or already settled., Wait for the operator's decision. None = timed out / not resolved., A pending operator decision for a dangerous agent tool call., Registry + control flags for scans currently executing in-process., Track a running scan so control endpoints can reach its task. (+3 more)

### Community 46 - "ProviderManager"
Cohesion: 0.12
Nodes (13): ProviderAlreadyRegisteredError, ProviderManager, ProviderNotFoundError, Provider Manager. The Manager owns the lifecycle of providers. Applications…, Thread-safe registry of providers. The Manager is the *only* place providers…, AIProvider, AIRequest, NullProvider (+5 more)

### Community 47 - "AstraIX Full-Spectrum Platform Vision"
Cohesion: 0.09
Nodes (29): AstraIX Security Analyst Platform, Data Architecture (Hot/Warm/Cold), Deployment Options, Integration Ecosystem (100+ Native), AstraIX Full-Spectrum Platform Vision, Platform Roadmap (5 Phases to 2027), VAPT Capability, ASTRAIX AI Modules (+21 more)

### Community 48 - "findings.py"
Cohesion: 0.19
Nodes (19): bulk_update_findings(), BulkUpdateRequest, delete_finding(), get_finding(), list_findings(), AsyncSession, delete, get (+11 more)

### Community 49 - "BasePlugin"
Cohesion: 0.10
Nodes (17): BasePlugin, FindingOut, PluginError, PluginOutput, PluginSchema, Parse stdin: str → dict., Structured logging accessible to orchestrator., Schema for plugin I/O, described in plugin.yml. (+9 more)

### Community 50 - "Asset"
Cohesion: 0.12
Nodes (16): Asset, AssetCriticality, AssetIdentifier, AssetInventory, AssetType, Any, Enum, str (+8 more)

### Community 51 - "compilerOptions"
Cohesion: 0.07
Nodes (29): compilerOptions, allowJs, baseUrl, esModuleInterop, forceConsistentCasingInFileNames, incremental, isolatedModules, jsx (+21 more)

### Community 52 - "Orchestrator"
Cohesion: 0.14
Nodes (16): Orchestrator, Assessment, AsyncSession, Exception, Finding, PluginError, PluginOutput, PluginRegistry (+8 more)

### Community 53 - "SystemStatus.tsx"
Cohesion: 0.14
Nodes (9): QuickActions(), RecentFindings(), StatCardProps, StatsCards(), ComponentRowProps, SystemStatus(), dashboardApi, systemApi (+1 more)

### Community 54 - "Finding Engine"
Cohesion: 0.23
Nodes (13): Finding Engine, web/discovery capability, HTTP Probe (httpx) Plugin, Semgrep SAST Scanner Plugin, Subfinder Subdomain Enumeration Plugin, Report Engine, code/audit capability, sast/security capability (+5 more)

### Community 55 - "VAPT Executor (executor.py)"
Cohesion: 0.18
Nodes (20): Docker Socket, KALI_IMAGE Env Var, VAPT_DEMO_MODE Env Var, VAPT_USE_DOCKER Env Var, gobuster, astraix-kali Image, nikto, nmap (+12 more)

### Community 56 - "assets.py"
Cohesion: 0.22
Nodes (17): create_asset(), delete_asset(), get_asset(), list_assets(), AsyncSession, delete, get, patch (+9 more)

### Community 57 - ".run"
Cohesion: 0.18
Nodes (12): AgentLoop, get_agent_loop(), Any, The autonomous tool-calling loop with phase + approval gating., Ground the agent with knowledge-base methodology snippets., Return (rejected, reason) when the model may NOT write a final report yet -…, Call the LLM with function tools; return (text, tool_calls). Prefers NVIDIA NIM…, Persist the step into the Neo4j attack graph (best-effort). (+4 more)

### Community 58 - "domain/models/__init__.py"
Cohesion: 0.16
Nodes (15): get_session(), AsyncSession, Database session dependency., FindingOut, PluginError, PluginManifest, PluginOutput, PluginStatus (+7 more)

### Community 59 - "findings/page.tsx"
Cohesion: 0.20
Nodes (15): cvssColor(), FindingsPage(), severityConfig, statusOptions, roleConfig, Card, CardContent, Table (+7 more)

### Community 60 - "PromptManager"
Cohesion: 0.14
Nodes (11): _InMemoryPromptManager, PromptManager, PromptTemplate, PromptVersionError, Any, Exception, Prompt Manager — versioned prompt templates. A `PromptTemplate` is a…, Raised when a requested `prompt_id` / version combination is unknown. (+3 more)

### Community 61 - "MetricsRegistry"
Cohesion: 0.13
Nodes (10): Counter, Histogram, MetricsRegistry, _NoopCounter, _NoopHistogram, Protocol, Metrics primitives (stubs at Milestone 1). These are typed protocols so…, Monotonically increasing value, optionally labelled. (+2 more)

### Community 62 - "KnowledgeGraph"
Cohesion: 0.11
Nodes (9): KnowledgeGraph, _node_id(), _node_tooltip(), Any, Record one agent-loop step as a ChainStep node linked to the target (target…, Any, VAPTExecutor, Attach a callback for live progress events (scan_id, event_type, data). (+1 more)

### Community 63 - "Settings"
Cohesion: 0.50
Nodes (4): get_settings(), BaseSettings, Application settings. Loaded from `.env` or process-level env vars., Settings

### Community 64 - "Unified Security Hub"
Cohesion: 0.13
Nodes (19): Application Security Module, Cloud Security Module, Dark-Moon Platform, Data Security Module, Defensive Security Module, Email Security Module, GRC & Compliance Module, Identity Security Module (+11 more)

### Community 65 - "kaggle-security-datasets/build.py"
Cohesion: 0.23
Nodes (19): find_dataset_dir(), handle_ai_generic(), handle_cve_generic(), handle_ids_generic(), handle_phish_generic(), handle_siem_generic(), main(), Path (+11 more)

### Community 66 - "plugins.py"
Cohesion: 0.19
Nodes (18): _count_by_capability(), _count_by_type(), disable_plugin(), enable_plugin(), get_plugin(), list_plugins(), plugins_info(), Any (+10 more)

### Community 67 - "PostgreSQL"
Cohesion: 0.13
Nodes (17): PostgreSQL, Quick Scan API Endpoint, VAPT Routes (routes.py), VAPT Scan Route Handler (route.ts), Alembic Migrations Dependency, asyncpg Dependency, SQLAlchemy 2.0 Dependency, VAPT API (+9 more)

### Community 69 - "container.py"
Cohesion: 0.10
Nodes (37): ABC, ContextBuilder, NullContextBuilder, Context Builder — assembles what's fed into a prompt. Pre-AI responsibilities:…, Build a `FindingContextPayload` from typed inputs., Default at Milestone 1. Performs no compression or redaction. A future…, AIGateway, DefaultAIGateway (+29 more)

### Community 70 - "app/models/base.py"
Cohesion: 0.33
Nodes (5): UUID, TimestampMixin, UUIDMixin, declared_attr, Mapped

### Community 71 - "CapabilityRegistry"
Cohesion: 0.18
Nodes (5): CapabilityVersion, Semantic version (major.minor.patch)., CapabilityRegistry, Capability, Thread-safe registry of `Capability` instances keyed by id+version.…

### Community 72 - "infrastructure/logging.py"
Cohesion: 0.07
Nodes (44): Platform-wide constants. Pure values that have no dependency on environment…, AI-SecOS Core configuration package. Single point of access to typed settings.…, AIGatewaySettings, FindingEngineSettings, load_settings(), ObservabilitySettings, PlatformSettings, BaseSettings (+36 more)

### Community 73 - "AI Gateway"
Cohesion: 0.12
Nodes (18): AI Gateway, Gemini AI, OpenAI SDK Dependency, Gemini AI Summaries, AI Core Layer, AI Integration Architecture, CSKB Alternatives Considered, cs kb CLI (+10 more)

### Community 74 - "Cybersecurity Knowledge Base"
Cohesion: 0.17
Nodes (17): Cybersecurity Knowledge Base, Planner Agent, ReconOrchestrator, Researcher Agent, Verifier Agent, faiss-cpu Dependency, fastembed Dependency, kb-data Named Volume (+9 more)

### Community 75 - "httpx.py"
Cohesion: 0.23
Nodes (13): _confidence(), _extract_items(), HttpxPluginId, make_httpx_input(), _normalize_one(), _normalize_tech(), Any, HTTP Probe (httpx) Plugin — normalizer. Converts raw `httpx` output into… (+5 more)

### Community 76 - "value_objects.py"
Cohesion: 0.12
Nodes (13): CapabilityVersion, ComplianceTag, Confidence, Enum, Reusable value objects (the platform's vocabulary). These are the typed shapes…, A compliance framework mapping., Validated confidence score: 0.0–1.0., SemVer-style version (integer triple). (+5 more)

### Community 77 - "graph/page.tsx"
Cohesion: 0.07
Nodes (22): bubbleSize(), BubbleView(), computeLayout(), edgeColor(), fetchAllFindings(), GraphNodeData, GraphPage(), GROUP_ANCHORS (+14 more)

### Community 78 - "BaseRepository"
Cohesion: 0.23
Nodes (8): BaseRepository, AsyncSession, T, UUID, Generic repository for any model., List with pagination and optional filters., Count records with optional filters., Create a new instance.

### Community 79 - "ResponseSchema"
Cohesion: 0.18
Nodes (15): get_graph(), get, get_kb_source(), knowledge_stats(), list_kb_sources(), get, post, Search the cybersecurity knowledge base. (+7 more)

### Community 80 - "AI-SecOS Core"
Cohesion: 0.18
Nodes (14): AI Gateway Module, AI-SecOS Core, Infrastructure Module, Domain Models Module, Normalizer Module, Platform Bootstrap Module, Plugin System Module, Report Engine Module (+6 more)

### Community 81 - "httpx/main.py"
Cohesion: 0.20
Nodes (14): _add(), _detect_cdn(), _detect_technologies(), _extract_title(), main(), probe_target(), Any, Extract version from header like 'nginx/1.21.6'. (+6 more)

### Community 82 - "shared/assessment.py"
Cohesion: 0.18
Nodes (12): AssessmentResult, AssessmentStatus, AssessmentTransition, Any, datetime, Enum, str, Assessment Model — central intent of a security run. An `Assessment` ties… (+4 more)

### Community 83 - "SecurityFinding"
Cohesion: 0.07
Nodes (25): AssessmentId, Return the same set of findings, possibly tagged with correlation., DefaultFindingDeduplicator, FindingDeduplicator, _max_or_none(), _merge(), _promote_severity(), Severity (+17 more)

### Community 84 - "PROJECT.md"
Cohesion: 0.14
Nodes (12): Communication, In Scope (PoC), Mission, Out of Scope (PoC), Project Charter, Project Overview, Risks & Mitigations, Scope (+4 more)

### Community 85 - "nmap/main.py"
Cohesion: 0.24
Nodes (13): build_nmap_command(), main(), _parse_host(), parse_nmap_xml(), _parse_port(), Any, Parse a single host element., Parse a port element. (+5 more)

### Community 86 - "TokenBudget"
Cohesion: 0.20
Nodes (7): Any, _PlanningError, Exception, Hard limits for a call. `None` = no limit on that field., Estimate prompt tokens; raise `PlanningError` if over budget., Raised when a planned request would exceed its budget., TokenBudget

### Community 87 - "New batch (curated + API-verified — 22 datasets)"
Cohesion: 0.17
Nodes (11): A. Vulnerabilities & CVE / exploit data, Already ingested (existing 3 — DO NOT re-download), B. Network intrusion & malware traffic, C. Malware, D. Phishing / URL / email security, E. Threat intel / SIEM / logs, Expected totals (rough estimate), F. AI / LLM security (+3 more)

### Community 88 - "NmapScanner"
Cohesion: 0.22
Nodes (6): NmapScanner, PluginError, PluginOutput, Run as process: stdin → scan → stdout, Run nmap, parse output, return findings., Parse Nmap XML/text → findings.

### Community 89 - "semgrep.py"
Cohesion: 0.27
Nodes (8): _categorize_semgrep(), _extract_tags(), _normalize_one(), Any, Semgrep Plugin — normalizer. Converts raw `semgrep` output into canonical…, Categorize semgrep finding based on check_id and metadata., Extract tags from semgrep metadata., Normalize a single semgrep finding.

### Community 90 - "shared/__init__.py"
Cohesion: 0.09
Nodes (32): CapabilityAlreadyRegisteredError, CapabilityNotFoundError, CapabilityResolverError, Capability-specific error types., Raised when attempting to register a duplicate capability., Raised when capability resolution fails (missing workflow, etc.)., Raised when a capability is not found in the registry., Capability Registry — typed lookup and lifecycle. Thread-safe in-memory… (+24 more)

### Community 91 - "Release 0.1.0"
Cohesion: 0.15
Nodes (13): Finding Normalizer (normalizer.py), Kali Tools Dockerfile, Risk Scoring Engine, Custom Kali Image (astraix-kali), Docker Compose Stack, Frontend Dashboard, Keep a Changelog Format, Normalized Findings (+5 more)

### Community 92 - "settings/page.tsx"
Cohesion: 0.27
Nodes (5): Input, InputProps, authApi, organizationsApi, Organization

### Community 93 - "error_handlers.py"
Cohesion: 0.31
Nodes (8): _map_error(), Any, FastAPI, Convert platform errors → HTTP responses. FastAPI exception handlers delegate…, Bind platform error handler., Shared mapping logic., register_exception_handlers(), _safe()

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
Cohesion: 0.15
Nodes (6): _get_kb(), _load_kb(), ResearcherAgent, Best-effort lookup of exploitation/technique guidance in the knowledge base for…, Verify findings concurrently (bounded) so long-running re-exploits (e.g.…, VerifierAgent

### Community 98 - "run_trivy_scan"
Cohesion: 0.33
Nodes (8): build_trivy_command(), main(), parse_trivy_results(), Any, Build trivy command arguments., Parse trivy JSON output., Execute trivy and return parsed results., run_trivy_scan()

### Community 99 - "workflow.py"
Cohesion: 0.33
Nodes (8): load_workflow_from_yaml(), Path, Workflow — declarative YAML-loadable structure. Reuse of the canonical…, Read a YAML workflow file and return a typed `Workflow`. Raises…, WorkflowLoaderError, _YamlBundle, Single step inside a Workflow declaration. `kind` selects how the Task Planner…, WorkflowStep

### Community 100 - "scripts"
Cohesion: 0.14
Nodes (13): name, private, scripts, build, dev, format, lint, start (+5 more)

### Community 101 - "BaseSchema"
Cohesion: 0.28
Nodes (6): BaseSchema, PaginatedResponse, Base schema with ORM mode enabled., Standard success response wrapper., Paginated results wrapper., ResponseSchema

### Community 102 - "nuclei.py"
Cohesion: 0.32
Nodes (6): _categorize(), _normalize_one(), Any, Nuclei Plugin — normalizer. Converts raw `nuclei` output into canonical…, Map nuclei tags to finding category., Normalize a single nuclei finding.

### Community 103 - ".validate_invocation"
Cohesion: 0.32
Nodes (5): Any, PluginManifest, Tiny subset of JSON Schema type matching for type-checking most params., _type_match(), ValidationResult

### Community 104 - "vapt/normalizer.py"
Cohesion: 0.36
Nodes (7): canonical_vuln_name(), cvss_for_severity(), normalize_finding(), normalize_findings(), Finding normalization: canonical vulnerability names + CVSS scores. Raw tool…, Map a raw finding title/type onto a standard vulnerability name., Return the finding with a canonical title/type and a CVSS score.

### Community 105 - "KB Source List (Tier 1-3)"
Cohesion: 0.25
Nodes (8): Aif4thah Dojo-101, ElNiak awesome-ai-cybersecurity, GitHub Cybersecurity Topics, naveen-98 Cyber_Security_Reference, okhosting awesome-cyber-security, santosomar AI-agents-for-cybersecurity, KB Source List (Tier 1-3), tomwechsler Cyber Knowledge Base

### Community 106 - "Network VAPT Workflow"
Cohesion: 0.39
Nodes (8): network/recon capability, network/vuln-scan capability, api/security capability, web/vuln-scan capability, Nmap Port Scanner Plugin, Nuclei Vulnerability Scanner Plugin, Network VAPT Workflow, Web Application VAPT Workflow

### Community 107 - "test_health.py"
Cohesion: 0.43
Nodes (6): AsyncClient, client(), asyncio, fixture, test_health_check(), test_root()

### Community 108 - "System Architecture"
Cohesion: 0.25
Nodes (9): System Architecture, Applications Layer, Plugin Executor, Plugin Manager, Plugin Sandbox, Plugin Validator, Plugins Layer, SecurityPlugin PDK (+1 more)

### Community 109 - "FindingContextPayload"
Cohesion: 0.38
Nodes (4): FindingContextPayload, Any, What the AI sees. Pre-serialization. The AI Gateway *never* receives the raw…, Convenience: flatten to a dict for string substitution.

### Community 110 - "ToolAvailabilityChecker"
Cohesion: 0.27
Nodes (6): Check which tools are available in the environment., Check if a specific tool is available., Check if Docker is available., Get availability status of all tools., Get overall health status of the scanner., ToolAvailabilityChecker

### Community 111 - "HTTPX Scanner Plugin"
Cohesion: 0.25
Nodes (8): Network Vulnerability Assessment, External Asset Discovery, Web Discovery, Web Application Security Assessment, HTTPX Scanner Plugin, Nmap Scanner Plugin, Nuclei Scanner Plugin, Subfinder Scanner Plugin

### Community 112 - "Master AI Engineer Rules"
Cohesion: 0.25
Nodes (8): Coding Standards, Python Standards, TypeScript Standards, MVP Scope Definition, Build Later Items, Build Now Items, Never Build Items, Master AI Engineer Rules

### Community 113 - "ToolResult"
Cohesion: 0.29
Nodes (4): Execute a single tool., Add a tool result and update aggregated findings., Result from a single security tool execution., ToolResult

### Community 114 - "External VAPT Platform Adapters"
Cohesion: 0.29
Nodes (6): Adapters, Configuration, Deploying an external platform, External VAPT Platform Adapters, Health, How it works

### Community 115 - "schemas/base.py"
Cohesion: 0.47
Nodes (3): BaseSchema, ErrorResponse, PaginatedResponse

### Community 116 - "wordlists.py"
Cohesion: 0.40
Nodes (5): _probe_image(), Wordlist resolver — curated wordlists baked into the astraix-kali image. Lists…, Purpose -> {path, lines, present} verified inside the Kali image., Run one `wc -l` over every curated list inside the Kali image., wordlist_health()

### Community 117 - "fetch-wordlists.sh"
Cohesion: 0.67
Nodes (5): dedupe(), fetch(), fetch_soft(), log(), fetch-wordlists.sh script

### Community 118 - "Auth API (auth.py)"
Cohesion: 0.29
Nodes (7): Auth API (auth.py), Demo Credentials, passlib/bcrypt Dependency, python-jose Dependency, JWT Auth System, Release 0.0.1 Initial MVP, API Reference

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

### Community 128 - "env.py"
Cohesion: 0.47
Nodes (4): do_run_migrations(), run_async_migrations(), run_migrations_online(), Connection

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
- **309 isolated node(s):** `astraix-backend`, `entrypoint.sh script`, `eslintConfig`, `nextConfig`, `name` (+304 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **27 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BaseModel` connect `BaseModel` to `api.py`, `vapt_platforms.py`, `plugin_system/executor.py`, `PluginRegistry`, `FindingEvidence`, `Workflow`, `get_scan_controller`, `DefaultWorkflowEngine`, `VAPTScanType`, `RoleName`, `ReportFormat`, `VAPTFinding`, `AssessmentRead`, `vapt/routes.py`, `findings.py`, `BasePlugin`, `assets.py`, `domain/models/__init__.py`, `app/models/base.py`, `value_objects.py`, `SecurityFinding`, `workflow.py`, `BaseSchema`, `ToolResult`, `schemas/base.py`?**
  _High betweenness centrality (0.141) - this node is a cross-community bridge._
- **Why does `SecurityFinding` connect `SecurityFinding` to `api.py`, `ReportFormat`, `container.py`, `nuclei.py`, `Severity`, `httpx.py`, `value_objects.py`, `FindingContextPayload`, `vapt/routes.py`, `FindingNormalizer`, `FindingEvidence`, `semgrep.py`, `shared/__init__.py`, `BaseModel`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **Why does `Asset` connect `Asset` to `api.py`, `PluginRegistry`, `vapt/routes.py`, `OrganizationRepository`, `BaseRepository`, `get_scan_controller`, `MembershipRepository`, `BaseModel`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `SecurityFinding` (e.g. with `ContextBuilder` and `FindingContextPayload`) actually correct?**
  _`SecurityFinding` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Are the 52 inferred relationships involving `RoleName` (e.g. with `ApiKeyCreate` and `ApiKeyCreateResponse`) actually correct?**
  _`RoleName` has 52 INFERRED edges - model-reasoned connections that need verification._
- **What connects `astraix-backend`, `entrypoint.sh script`, `eslintConfig` to the rest of the system?**
  _309 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `VAPTAdapter` be split into smaller, more focused modules?**
  _Cohesion score 0.052941176470588235 - nodes in this community are weakly interconnected._