# Graph Report - astraix-security-analyst  (2026-08-18)

## Corpus Check
- 264 files · ~193,141 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3311 nodes · 7873 edges · 180 communities (153 shown, 27 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 987 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bb915bbb`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- _HttpAdapter
- api.py
- api.ts
- vapt_platforms.py
- plugin_system/executor.py
- Severity
- Workflow
- Container
- organizations.py
- capabilities/loader.py
- vapt/models.py
- get_current_user
- User
- _KaliToolAdapter
- FindingEvidence
- EventDispatcher
- Finding
- VAPTScanRequest
- projects/page.tsx
- vapt/routes.py
- shared/__init__.py
- task_planner.py
- VAPTTarget
- MembershipRepository
- BaseModel
- ToolRegistry
- FastAPI Backend
- scans/page.tsx
- PluginRegistry
- devDependencies
- RoleName
- VAPTOutputParser
- LyrieAIAgent
- ReportFormat
- AIOrchestrator
- dependencies
- flows_engine.py
- Knowledge Base Corpus
- container.py
- VAPTExecutor
- VAPTFinding
- assessments.py
- vapt/orchestrator.py
- dropdown-menu.tsx
- ScanController
- ProviderManager
- AstraIX Full-Spectrum Platform Vision
- ResponseSchema
- BasePlugin
- Asset
- compilerOptions
- Orchestrator
- SystemStatus.tsx
- Finding Engine
- VAPT Executor (executor.py)
- UserRepository
- VAPTScanType
- repositories/__init__.py
- [id]/page.tsx
- PromptTemplate
- SecurityFinding
- KnowledgeGraph
- kb.py
- Unified Security Hub
- kaggle-security-datasets/build.py
- MetricsRegistry
- PostgreSQL
- XalgorixAdapter
- ai_gateway/__init__.py
- garak_scanner.py
- infrastructure/__init__.py
- infrastructure/logging.py
- AI Gateway
- Cybersecurity Knowledge Base
- ScanProgressBus
- CapabilityRegistry
- graph/page.tsx
- BaseRepository
- web_form_scanner.py
- AI-SecOS Core
- httpx/main.py
- value_objects.py
- DefaultFindingDeduplicator
- PROJECT.md
- nmap/main.py
- DefaultWorkflowEngine
- New batch (curated + API-verified — 22 datasets)
- NmapScanner
- Confidence
- ScannerExecutor
- Release 0.1.0
- button.tsx
- code_review_scanner.py
- run_nuclei_scan
- run_semgrep_scan
- run_subfinder
- Pentest Report — OWASP Juice Shop AI Chatbot (`localhost:3002`)
- run_trivy_scan
- results.py
- scripts
- BaseSchema
- _MutableContainer
- .validate_invocation
- vapt/normalizer.py
- CHECKPOINT — AstraIX continuation point
- get_container
- test_health.py
- System Architecture
- app/main.py
- ToolAvailabilityChecker
- HTTPX Scanner Plugin
- Master AI Engineer Rules
- semgrep.py
- External VAPT Platform Adapters
- PluginRegistry
- wordlists.py
- fetch-wordlists.sh
- OrganizationRepository
- ai_secos_core/tests/conftest.py
- Report Base Template (base.html)
- download.sh
- AstraIX Platform Constitution
- app/layout.tsx
- graphify.js
- reports.py
- error_handlers.py
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
- recon.py
- dom_xss_scanner.py
- KB Source List (Tier 1-3)
- get_role_permissions
- FindingContextPayload
- get_kb_source
- CapabilityVersion
- env.py
- api_surface_scanner.py
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
3. `VAPTFinding` - 67 edges
4. `RoleName` - 60 edges
5. `VAPTExecutor` - 59 edges
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

## Communities (180 total, 27 thin omitted)

### Community 0 - "_HttpAdapter"
Cohesion: 0.13
Nodes (9): DarkMoonAdapter, _HttpAdapter, PentagiAdapter, Any, PentAGI - fully autonomous pentesting agent (Go backend, REST API)., RedAmon - agentic red team framework (graph-powered, webapp API)., Base for adapters that talk to an external HTTP API., Dark-Moon autonomous pentest platform. Mode A (HTTP): DARKMOON_BASE_URL +… (+1 more)

### Community 1 - "api.py"
Cohesion: 0.07
Nodes (51): assess(), AssessRequest, AssessResponse, _bootstrap(), FindingSummary, index(), list_capabilities(), Any (+43 more)

### Community 2 - "api.ts"
Cohesion: 0.06
Nodes (41): formats, MIME_TYPES, templateIcons, apiKeysApi, assessmentsApi, assetsApi, findingsApi, graphApi (+33 more)

### Community 3 - "vapt_platforms.py"
Cohesion: 0.08
Nodes (42): get_scanner_executor(), Scanner Executor Service Enterprise-grade scanner execution with: - Async tool…, Get the global scanner executor instance., AstraIX Security Scanner Module Enterprise-grade security scanning engine that…, Finding, Enum, str, Scanner Models Enterprise-grade data models for security scanning operations.… (+34 more)

### Community 4 - "plugin_system/executor.py"
Cohesion: 0.06
Nodes (53): NoopTaskExecutor, PluginExecutionRequest, PluginExecutionResult, PluginExecutionStatus, PluginExecutor, CorrelationId, Enum, PluginRegistry (+45 more)

### Community 5 - "Severity"
Cohesion: 0.08
Nodes (33): DefaultRiskEngine, _noop_severity_to_score(), NoopRiskEngine, Severity, Risk Engine — pipeline orchestrator and entry points. Two implementations are…, Identity: score derived directly from canonical severity. Used in tests and as…, A scored finding (or a typed wrapper around a SecurityFinding)., Engine port: score one or more canonical findings. (+25 more)

### Community 6 - "Workflow"
Cohesion: 0.14
Nodes (22): Schedule and execute a Workflow as a DAG., TaskPlanner, load_workflow_from_yaml(), Path, Workflow — declarative YAML-loadable structure. Reuse of the canonical…, Read a YAML workflow file and return a typed `Workflow`. Raises…, WorkflowLoaderError, _YamlBundle (+14 more)

### Community 8 - "Container"
Cohesion: 0.18
Nodes (14): build_app(), lifespan(), FastAPI, FastAPI app factory. Binds the DI container to the web transport. -…, Start/stop lifetime management., Create the FastAPI application. Mostly configures routing + middleware; DI…, Container, At boot, walk the plugins root and populate: - plugin registry - normalizer… (+6 more)

### Community 9 - "organizations.py"
Cohesion: 0.09
Nodes (46): ApiKeyCreate, create_api_key(), create_organization(), create_project(), delete_api_key(), delete_organization(), delete_project(), get_api_key() (+38 more)

### Community 10 - "capabilities/loader.py"
Cohesion: 0.09
Nodes (44): CapabilityAlreadyRegisteredError, CapabilityNotFoundError, CapabilityResolverError, Capability-specific error types., Raised when attempting to register a duplicate capability., Raised when capability resolution fails (missing workflow, etc.)., Raised when a capability is not found in the registry., Capability Registry — first-class Capability abstraction. Applications request… (+36 more)

### Community 11 - "vapt/models.py"
Cohesion: 0.07
Nodes (37): AdapterScanResult, AdapterStatus, Any, Base classes and contracts for VAPT external adapters., True when the environment contains everything needed to attempt a run., True when the adapter should participate in scans., Adapters are skipped for targets they cannot meaningfully test., Return current availability status (should not raise). (+29 more)

### Community 12 - "get_current_user"
Cohesion: 0.17
Nodes (19): api_key_header, decode_token(), get_current_active_user(), get_current_superuser(), get_current_user(), get_user_organizations(), get_user_projects(), AsyncSession (+11 more)

### Community 13 - "User"
Cohesion: 0.12
Nodes (32): create_project(), delete_organization(), delete_project(), get_organization(), get_project(), list_api_keys(), list_memberships(), list_organizations() (+24 more)

### Community 14 - "_KaliToolAdapter"
Cohesion: 0.09
Nodes (10): _ContainerRunner, _KaliToolAdapter, LyrieAdapter, Any, RaccoonAdapter, Raccoon recon scanner (DNS/WHOIS/TLS/WAF/subdomains/dir-busting)., Minimal Docker-socket runner for one-shot commands in the Kali image., Filter crash/traceback/banner noise out of tool output before parsing. (+2 more)

### Community 15 - "FindingEvidence"
Cohesion: 0.21
Nodes (15): _confidence(), _extract_items(), HttpxPluginId, make_httpx_input(), _normalize_one(), _normalize_tech(), Any, HTTP Probe (httpx) Plugin — normalizer. Converts raw `httpx` output into… (+7 more)

### Community 16 - "EventDispatcher"
Cohesion: 0.10
Nodes (24): ProgressTicker, Streaming-aware Plugin Executor. Wraps the base `PluginExecutor` and emits…, Wraps a PluginExecutor to emit streaming events. The wrapper preserves the…, Background ticker to emit periodic plugin.progress events. Started when a…, StreamingPluginExecutor, emit_plugin_completed(), emit_plugin_finding(), emit_plugin_progress() (+16 more)

### Community 17 - "Finding"
Cohesion: 0.13
Nodes (20): Asset, Finding, TimestampMixin, UUIDMixin, AssessmentStatus, get_orchestrator(), Orchestrator, Assessment (+12 more)

### Community 18 - "VAPTScanRequest"
Cohesion: 0.23
Nodes (6): Any, VAPTExecutor, Attach a callback for live progress events (scan_id, event_type, data)., ReconOrchestrator, Request for a VAPT scan., VAPTScanRequest

### Community 19 - "projects/page.tsx"
Cohesion: 0.13
Nodes (23): react, QuickAction, FindingDetail(), formatDetails(), severityStyles, Dialog(), DialogContent(), DialogContentProps (+15 more)

### Community 20 - "vapt/routes.py"
Cohesion: 0.07
Nodes (56): get_scan_controller(), Exception, Raised at a checkpoint when the scan was stopped by the user., ScanStoppedError, get_vapt_orchestrator(), adapters_health(), ApprovalDecision, _finding_fingerprint() (+48 more)

### Community 21 - "shared/__init__.py"
Cohesion: 0.25
Nodes (11): ConfigurationError, FindingEngineError, PlatformError, Any, Exception, Single error hierarchy for the entire AI-SecOS Core. Public API (the only types…, Base error of the platform. Carries `code` (machine-readable, stable) and…, ReportEngineError (+3 more)

### Community 22 - "task_planner.py"
Cohesion: 0.09
Nodes (31): CancellationToken, CancelledError, Cancellation token for running tasks/plans. The platform-wide cancellation…, A typed alias for cancellation that originates from the platform., Lightweight, async-friendly cancellation., NoopTaskExecutor, Any, Task Executor — runs a Task. A planner produces Tasks; the executor is what… (+23 more)

### Community 23 - "VAPTTarget"
Cohesion: 0.33
Nodes (3): Any, field_validator, VAPTTarget

### Community 24 - "MembershipRepository"
Cohesion: 0.09
Nodes (15): ApiKey, ApiKeyRepository, get_api_key_repo(), get_membership_repo(), get_organization_repo(), get_project_repo(), get_user_repo(), MembershipRepository (+7 more)

### Community 25 - "BaseModel"
Cohesion: 0.17
Nodes (45): ApiKeyCreate, ApiKeyCreateResponse, ApiKeyResponse, create_api_key(), create_organization(), invite_member(), MembershipCreate, MembershipResponse (+37 more)

### Community 26 - "ToolRegistry"
Cohesion: 0.09
Nodes (20): get_tool_registry(), Enum, str, Kali Linux Security Tool Registry Comprehensive registry of security tools…, Tool categories matching VAPT workflow., Metadata about a security tool., Default configuration for a tool., Registry for managing security tools. (+12 more)

### Community 27 - "FastAPI Backend"
Cohesion: 0.10
Nodes (28): FastAPI Backend, Neo4j Knowledge Graph, Next.js Frontend, Redis, FastAPI Dependency, Neo4j Driver Dependency, Pydantic v2 Dependency, redis Python Client Dependency (+20 more)

### Community 28 - "scans/page.tsx"
Cohesion: 0.08
Nodes (29): Finding, getSeverityBadge(), getTypeIcon(), getTypeLabel(), LiveScanConsole(), phaseIcons, PlanPhase, PlanTool (+21 more)

### Community 29 - "PluginRegistry"
Cohesion: 0.10
Nodes (14): PluginLoader, PluginLoaderError, Path, PluginError, PluginManifest, Filesystem-based plugin loader. The exact YAML layout is opaque outside this…, Walk the plugins root; return all parseable plugin records. Directories without…, Load a single plugin by directory path. Raises PluginLoaderError on missing… (+6 more)

### Community 30 - "devDependencies"
Cohesion: 0.06
Nodes (31): autoprefixer, eslint, eslint-config-next, devDependencies, autoprefixer, eslint, eslint-config-next, jsdom (+23 more)

### Community 31 - "RoleName"
Cohesion: 0.20
Nodes (29): str, RoleName, ApiKeyBase, ApiKeyCreate, ApiKeyCreateResponse, ApiKeyRead, MembershipBase, MembershipCreate (+21 more)

### Community 32 - "VAPTOutputParser"
Cohesion: 0.08
Nodes (20): Finding, Severity, Parse lyrie hack output to findings. Lyrie outputs JSON or SARIF format.…, Parse SARIF format output from lyrie., Parse Nmap text output as fallback., Map lyrie severity string to Severity enum., Parse Nikto XML output to findings., Map Nikto OSVDB ID to severity. (+12 more)

### Community 33 - "LyrieAIAgent"
Cohesion: 0.12
Nodes (12): LyrieAIAgent, Lyrie AI Agent executor for autonomous security operations. Features: - 7-phase…, Run 7-phase autonomous pentest. Args: target: URL or local path to pentest…, Scan URL or file for security issues. Checks: - Security headers (CSP, HSTS,…, AI red-team an LLM endpoint. Strategies: - crescendo: gradual escalation - tap:…, Calculate CVSS v3.1 score from vector. Args: vector: CVSS vector string (e.g.,…, Verify agent identity using Agent Trust Protocol. Args: agent_id: Agent…, Display ATP compliance badge. Returns: dict with badge information (+4 more)

### Community 34 - "ReportFormat"
Cohesion: 0.12
Nodes (35): _ai_comment_placeholder(), _build_section(), _findings_section(), NullReportEngine, ReportRequest, Report Engine — implementation. At Milestone 1, only the JSON/Markdown default…, Render reports from findings + risk scores., JSON/Markdown default at Milestone 1. Produces deterministic artefacts using… (+27 more)

### Community 35 - "AIOrchestrator"
Cohesion: 0.06
Nodes (30): build_curl_command(), get_matrix_agent(), MatrixAgent, parse_probe_output(), Test Matrix Agent The LLM-driven exploitation test matrix: given the mined web…, Heuristic positive-signal check for an HTTP matrix entry. Returns (suspicious,…, Build the Kali curl probe for one matrix entry. GET entries encode params into…, Split a probe output into (http_status, body). (+22 more)

### Community 36 - "dependencies"
Cohesion: 0.07
Nodes (29): axios, class-variance-authority, clsx, d3-force, dagre, date-fns, dependencies, axios (+21 more)

### Community 37 - "flows_engine.py"
Cohesion: 0.12
Nodes (19): Any, Ask the LLM (Ollama primary, NVIDIA secondary) for a JSON array., Build the validated exploitation test matrix for the target., LLM synthesis of the findings into an attack-chain narrative., PlannerAgent, Any, Ask the LLM (NVIDIA NIM, falling back to Ollama) to refine tool selection.…, Generate the full phased VAPT plan with KB-grounded reasoning. (+11 more)

### Community 38 - "Knowledge Base Corpus"
Cohesion: 0.12
Nodes (19): OWASP Projects (ADR Tier 3), paulveillard/cybersecurity (ADR Tier 1), Anthropic Cybersecurity Skills Repo, awesome-soc Repo, Berkanktk/CyberSecurity Repo, CAI (Cybersecurity AI) Repo, cybersecurity-knowledge-base Repo, Cybersecurity-Resources Repo (+11 more)

### Community 39 - "container.py"
Cohesion: 0.13
Nodes (27): Dependency Injection container. Uses DI’y to wire the entire platform without…, # TODO: Lookup normalizer + register, FindingCorrelator, NoopFindingCorrelator, Finding Correlator — the contract + the no-op default. Correlators detect…, Adds correlation metadata to findings., Identity correlator. The default at Milestone 1., FindingDeduplicator (+19 more)

### Community 40 - "VAPTExecutor"
Cohesion: 0.13
Nodes (18): ExternalTool, Any, ScanRequest, Orchestrates scans across multiple tools and platforms. Supports: - Sequential…, Execute a complete security scan., Get tools for a given capability., Enterprise VAPT Execution Engine Features: - Multi-platform support (Kali,…, Execute a single tool and return parsed findings. (+10 more)

### Community 41 - "VAPTFinding"
Cohesion: 0.05
Nodes (20): get_vapt_executor(), Parse API surface discovery JSONL findings, preserving severity, category,…, Run exactly one tool against the target for the autonomous agent. Returns…, Run a raw command inside the Kali container (e.g. a curl probe). Returns…, Reduce a URL target to bare host[:port] for host-oriented tools., Return the port explicitly present in the target URL, else None., Extract an explicit port from a URL target, else the scheme default., Map loopback targets to the Docker gateway host. Tool containers run in… (+12 more)

### Community 42 - "assessments.py"
Cohesion: 0.15
Nodes (23): AssessmentModel, cancel_assessment(), create_assessment(), get_assessment(), list_assessments(), AsyncSession, delete, get (+15 more)

### Community 43 - "vapt/orchestrator.py"
Cohesion: 0.10
Nodes (28): get_graph(), get, get_dashboard_activity(), get_dashboard_stats(), list_capabilities(), ping(), get, UUID (+20 more)

### Community 44 - "dropdown-menu.tsx"
Cohesion: 0.20
Nodes (8): DropdownMenuCheckboxItem, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuRadioItem, DropdownMenuSeparator, DropdownMenuSubContent, DropdownMenuSubTrigger

### Community 45 - "ScanController"
Cohesion: 0.10
Nodes (11): Any, Store the agent loop's partial results so an aborted/timed-out loop can still…, Register a pending operator decision for a dangerous tool call., Settle a pending approval. Returns False when unknown or already settled., Wait for the operator's decision. None = timed out / not resolved., A pending operator decision for a dangerous agent tool call., Registry + control flags for scans currently executing in-process., Track a running scan so control endpoints can reach its task. (+3 more)

### Community 46 - "ProviderManager"
Cohesion: 0.19
Nodes (8): ProviderAlreadyRegisteredError, ProviderManager, ProviderNotFoundError, Provider Manager. The Manager owns the lifecycle of providers. Applications…, Thread-safe registry of providers. The Manager is the *only* place providers…, AIProvider, Concrete providers (OpenAI/Anthropic/...) implement this., AIError

### Community 47 - "AstraIX Full-Spectrum Platform Vision"
Cohesion: 0.09
Nodes (29): AstraIX Security Analyst Platform, Data Architecture (Hot/Warm/Cold), Deployment Options, Integration Ecosystem (100+ Native), AstraIX Full-Spectrum Platform Vision, Platform Roadmap (5 Phases to 2027), VAPT Capability, ASTRAIX AI Modules (+21 more)

### Community 48 - "ResponseSchema"
Cohesion: 0.09
Nodes (43): create_asset(), delete_asset(), get_asset(), list_assets(), AsyncSession, delete, get, patch (+35 more)

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
Cohesion: 0.13
Nodes (10): QuickActions(), RecentAssessments(), RecentFindings(), StatCardProps, StatsCards(), ComponentRowProps, SystemStatus(), dashboardApi (+2 more)

### Community 54 - "Finding Engine"
Cohesion: 0.17
Nodes (21): Finding Engine, web/discovery capability, network/recon capability, network/vuln-scan capability, api/security capability, web/vuln-scan capability, HTTP Probe (httpx) Plugin, Nmap Port Scanner Plugin (+13 more)

### Community 55 - "VAPT Executor (executor.py)"
Cohesion: 0.18
Nodes (20): Docker Socket, KALI_IMAGE Env Var, VAPT_DEMO_MODE Env Var, VAPT_USE_DOCKER Env Var, gobuster, astraix-kali Image, nikto, nmap (+12 more)

### Community 56 - "UserRepository"
Cohesion: 0.12
Nodes (20): get_api_key_repo(), get_membership_repo(), get_org_repo(), get_project_repo(), get_user_repo(), login(), login_json(), AsyncSession (+12 more)

### Community 57 - "VAPTScanType"
Cohesion: 0.11
Nodes (23): agent_loop_supported(), AgentLoop, get_agent_loop(), Any, Autonomous VAPT Agent Loop (Phase 1) RedAmon-inspired agentic workflow: instead…, One agent-loop step (one tool execution attempt)., The autonomous tool-calling loop with phase + approval gating., Ground the agent with methodology guidance from the knowledge base, specific to… (+15 more)

### Community 58 - "repositories/__init__.py"
Cohesion: 0.09
Nodes (27): AsyncSession, post, Run a security assessment scan., run_assessment(), get_session(), AsyncSession, Database session dependency., Base (+19 more)

### Community 59 - "[id]/page.tsx"
Cohesion: 0.15
Nodes (27): cvssColor(), FindingsPage(), severityConfig, statusOptions, cvssColor(), fmtLabel(), ProjectDetailPage(), registrableDomain() (+19 more)

### Community 60 - "PromptTemplate"
Cohesion: 0.17
Nodes (8): _InMemoryPromptManager, PromptTemplate, PromptVersionError, Any, Exception, Raised when a requested `prompt_id` / version combination is unknown., One version of one prompt. The text uses stdlib `Template` semantics ($-style…, Process-local default; replace with persistence later if needed.

### Community 61 - "SecurityFinding"
Cohesion: 0.08
Nodes (23): Return the same set of findings, possibly tagged with correlation., Insert one finding. Returns `(stored_finding, was_new)`. When `was_new=False`,…, Return a new (or in-place enriched) finding., _create_os_finding(), _normalize_host(), Any, Nmap Plugin — normalizer. Converts raw `nmap` output into canonical…, Create a finding for detected OS. (+15 more)

### Community 62 - "KnowledgeGraph"
Cohesion: 0.18
Nodes (5): KnowledgeGraph, _node_id(), _node_tooltip(), Any, Record one agent-loop step as a ChainStep node linked to the target (target…

### Community 63 - "kb.py"
Cohesion: 0.09
Nodes (24): apply_finding_relevance_floor(), get_kb(), is_semantic_kb(), kb_context_for_finding(), kb_ready(), kb_snippets(), kb_sources_for(), kb_stats() (+16 more)

### Community 64 - "Unified Security Hub"
Cohesion: 0.13
Nodes (19): Application Security Module, Cloud Security Module, Dark-Moon Platform, Data Security Module, Defensive Security Module, Email Security Module, GRC & Compliance Module, Identity Security Module (+11 more)

### Community 65 - "kaggle-security-datasets/build.py"
Cohesion: 0.23
Nodes (19): find_dataset_dir(), handle_ai_generic(), handle_cve_generic(), handle_ids_generic(), handle_phish_generic(), handle_siem_generic(), main(), Path (+11 more)

### Community 66 - "MetricsRegistry"
Cohesion: 0.15
Nodes (9): Counter, Histogram, MetricsRegistry, _NoopCounter, _NoopHistogram, Protocol, Metrics primitives (stubs at Milestone 1). These are typed protocols so…, Monotonically increasing value, optionally labelled. (+1 more)

### Community 67 - "PostgreSQL"
Cohesion: 0.09
Nodes (24): Auth API (auth.py), Demo Credentials, PostgreSQL, Quick Scan API Endpoint, VAPT Routes (routes.py), VAPT Scan Route Handler (route.ts), Alembic Migrations Dependency, asyncpg Dependency (+16 more)

### Community 69 - "ai_gateway/__init__.py"
Cohesion: 0.06
Nodes (52): ABC, ContextBuilder, NullContextBuilder, Context Builder — assembles what's fed into a prompt. Pre-AI responsibilities:…, Build a `FindingContextPayload` from typed inputs., Default at Milestone 1. Performs no compression or redaction. A future…, AIGateway, DefaultAIGateway (+44 more)

### Community 70 - "garak_scanner.py"
Cohesion: 0.17
Nodes (20): add(), _attempt_prompt(), direct_probe(), endpoint_reachable(), find_chat_endpoint(), guess_response_field(), http(), main() (+12 more)

### Community 71 - "infrastructure/__init__.py"
Cohesion: 0.18
Nodes (13): platform_error_to_http_response(), PlatformErrorResponse, Map platform errors → HTTP responses. FastAPI exception handler in `platform/`…, Convert a PlatformError to a status/body pair. `correlation_id` is included so…, Cross-cutting infrastructure components. This package provides: - Structured…, get_correlation_id(), new_correlation_id(), CorrelationId (+5 more)

### Community 72 - "infrastructure/logging.py"
Cohesion: 0.09
Nodes (33): Platform-wide constants. Pure values that have no dependency on environment…, AI-SecOS Core configuration package. Single point of access to typed settings.…, AIGatewaySettings, FindingEngineSettings, load_settings(), ObservabilitySettings, PlatformSettings, BaseSettings (+25 more)

### Community 73 - "AI Gateway"
Cohesion: 0.12
Nodes (18): AI Gateway, Gemini AI, OpenAI SDK Dependency, Gemini AI Summaries, AI Core Layer, AI Integration Architecture, CSKB Alternatives Considered, cs kb CLI (+10 more)

### Community 74 - "Cybersecurity Knowledge Base"
Cohesion: 0.17
Nodes (17): Cybersecurity Knowledge Base, Planner Agent, ReconOrchestrator, Researcher Agent, Verifier Agent, faiss-cpu Dependency, fastembed Dependency, kb-data Named Volume (+9 more)

### Community 75 - "ScanProgressBus"
Cohesion: 0.25
Nodes (5): Any, Drop all stored events/status for a scan (used on restart)., List scans that are still running (non-terminal status)., Publishes and reads scan progress events (Redis-backed, in-memory fallback)., ScanProgressBus

### Community 76 - "CapabilityRegistry"
Cohesion: 0.18
Nodes (5): CapabilityVersion, Semantic version (major.minor.patch)., CapabilityRegistry, Capability, Thread-safe registry of `Capability` instances keyed by id+version.…

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

### Community 82 - "value_objects.py"
Cohesion: 0.08
Nodes (22): AssessmentId, FindingNormalizer, NormalizationError, Any, Normalizer interface + registry. The Normalizer is how raw plugin output…, Turns a plugin-specific raw output into a `SecurityFinding`. A single input may…, Yield canonical findings from a raw plugin output. Implementations MUST yield…, _categorize() (+14 more)

### Community 83 - "DefaultFindingDeduplicator"
Cohesion: 0.14
Nodes (14): DefaultFindingDeduplicator, _max_or_none(), _merge(), _promote_severity(), Severity, Deduplication: collapsing equivalent findings. Two findings with the same…, Merge a re-observed finding with its prior canonical record. Strategy: -…, In-memory implementation. Suitable for single-process Milestone 1 / Milestone 2… (+6 more)

### Community 84 - "PROJECT.md"
Cohesion: 0.14
Nodes (12): Communication, In Scope (PoC), Mission, Out of Scope (PoC), Project Charter, Project Overview, Risks & Mitigations, Scope (+4 more)

### Community 85 - "nmap/main.py"
Cohesion: 0.24
Nodes (13): build_nmap_command(), main(), _parse_host(), parse_nmap_xml(), _parse_port(), Any, Parse a single host element., Parse a port element. (+5 more)

### Community 86 - "DefaultWorkflowEngine"
Cohesion: 0.10
Nodes (22): CapabilityResolver, Any, Capability, Capability Resolver. Resolves a `Capability` request into a concrete execution…, Validate inputs against the capability's input schema (lightweight). Performs…, Raised when capability resolution fails., A Capability fully resolved to executable Workflows., Resolves Capabilities to WorkflowRecords ready for the Task Planner. (+14 more)

### Community 87 - "New batch (curated + API-verified — 22 datasets)"
Cohesion: 0.17
Nodes (11): A. Vulnerabilities & CVE / exploit data, Already ingested (existing 3 — DO NOT re-download), B. Network intrusion & malware traffic, C. Malware, D. Phishing / URL / email security, E. Threat intel / SIEM / logs, Expected totals (rough estimate), F. AI / LLM security (+3 more)

### Community 88 - "NmapScanner"
Cohesion: 0.22
Nodes (6): NmapScanner, PluginError, PluginOutput, Run as process: stdin → scan → stdout, Run nmap, parse output, return findings., Parse Nmap XML/text → findings.

### Community 89 - "Confidence"
Cohesion: 0.50
Nodes (3): Confidence, Validated confidence score: 0.0–1.0., float

### Community 90 - "ScannerExecutor"
Cohesion: 0.12
Nodes (15): PluginRegistry, Any, Finding, ScanRequest, VAPTExecutor, Execute a single tool., Create appropriate executor for scan request., Get tools for a scan request. (+7 more)

### Community 91 - "Release 0.1.0"
Cohesion: 0.15
Nodes (13): Finding Normalizer (normalizer.py), Kali Tools Dockerfile, Risk Scoring Engine, Custom Kali Image (astraix-kali), Docker Compose Stack, Frontend Dashboard, Keep a Changelog Format, Normalized Findings (+5 more)

### Community 92 - "button.tsx"
Cohesion: 0.18
Nodes (10): Button, ButtonProps, buttonVariants, Input, InputProps, Progress, cn(), authApi (+2 more)

### Community 93 - "code_review_scanner.py"
Cohesion: 0.27
Nodes (16): add(), _emit(), fingerprint_repo(), http_get(), main(), _parse_bandit(), _parse_codeql(), _parse_gitleaks() (+8 more)

### Community 94 - "run_nuclei_scan"
Cohesion: 0.33
Nodes (8): build_nuclei_command(), main(), parse_nuclei_json(), Any, Execute nuclei and return parsed results., Build nuclei command arguments., Parse nuclei JSON output lines., run_nuclei_scan()

### Community 95 - "run_semgrep_scan"
Cohesion: 0.33
Nodes (8): build_semgrep_command(), main(), parse_semgrep_results(), Any, Build semgrep command arguments., Parse semgrep JSON output., Execute semgrep and return parsed results., run_semgrep_scan()

### Community 96 - "run_subfinder"
Cohesion: 0.33
Nodes (8): build_subfinder_command(), main(), parse_subfinder_json(), Any, Build subfinder command arguments., Parse subfinder JSON output lines., Execute subfinder and return parsed results., run_subfinder()

### Community 97 - "Pentest Report — OWASP Juice Shop AI Chatbot (`localhost:3002`)"
Cohesion: 0.12
Nodes (15): Appendix — Environment Notes, Attack Chain Summary (kill-chain used in engagement), Executive Summary, F1 — JWT `alg:none` → Admin Session Forgery (CRITICAL), F2 — SQL Injection in Login (CRITICAL), F3 — Unauthenticated Admin Registration (HIGH), F4 — Chatbot Auth Bypass → Cross-User Order Leak (HIGH), F5 — Prompt Injection → Greedy Coupon (HIGH) (+7 more)

### Community 98 - "run_trivy_scan"
Cohesion: 0.33
Nodes (8): build_trivy_command(), main(), parse_trivy_results(), Any, Build trivy command arguments., Parse trivy JSON output., Execute trivy and return parsed results., run_trivy_scan()

### Community 99 - "results.py"
Cohesion: 0.18
Nodes (12): fail(), Failure, is_failure(), is_ok(), ok(), Any, T, Result type (Rust/Python-port idiom) for explicit success/failure. Used by… (+4 more)

### Community 100 - "scripts"
Cohesion: 0.14
Nodes (13): name, private, scripts, build, dev, format, lint, start (+5 more)

### Community 101 - "BaseSchema"
Cohesion: 0.28
Nodes (6): BaseSchema, PaginatedResponse, Base schema with ORM mode enabled., Standard success response wrapper., Paginated results wrapper., ResponseSchema

### Community 102 - "_MutableContainer"
Cohesion: 0.20
Nodes (12): build_default_container(), _MutableContainer, Mutable (thread-safe) wiring harness., Safely edit mutable values., Return a frozen copy ready for consumption., Wire default implementations for production runtime., PluginValidator, Validates a manifest + proposed invocation parameters. Stateless aside from… (+4 more)

### Community 103 - ".validate_invocation"
Cohesion: 0.32
Nodes (5): Any, PluginManifest, Tiny subset of JSON Schema type matching for type-checking most params., _type_match(), ValidationResult

### Community 104 - "vapt/normalizer.py"
Cohesion: 0.36
Nodes (7): canonical_vuln_name(), cvss_for_severity(), normalize_finding(), normalize_findings(), Finding normalization: canonical vulnerability names + CVSS scores. Raw tool…, Map a raw finding title/type onto a standard vulnerability name., Return the finding with a canonical title/type and a CVSS score.

### Community 105 - "CHECKPOINT — AstraIX continuation point"
Cohesion: 0.29
Nodes (6): 1. System state after restart, 2. Product features live right now, 3. Scan history (validated), 4. Known issues / gotchas, 5. Next steps (when resuming), CHECKPOINT — AstraIX continuation point

### Community 106 - "get_container"
Cohesion: 0.29
Nodes (10): get_container(), Request, FastAPI dependency: immutable container wired to pathOps., health(), Any, get, Endpoint health; always 200., Ready — fail if plugins unload or config invalid. (+2 more)

### Community 107 - "test_health.py"
Cohesion: 0.43
Nodes (6): AsyncClient, client(), asyncio, fixture, test_health_check(), test_root()

### Community 108 - "System Architecture"
Cohesion: 0.25
Nodes (9): System Architecture, Applications Layer, Plugin Executor, Plugin Manager, Plugin Sandbox, Plugin Validator, Plugins Layer, SecurityPlugin PDK (+1 more)

### Community 109 - "app/main.py"
Cohesion: 0.10
Nodes (24): get_settings(), BaseSettings, Application settings loaded from env vars or .env., Settings, get_settings(), BaseSettings, Application settings. Loaded from `.env` or process-level env vars., Settings (+16 more)

### Community 110 - "ToolAvailabilityChecker"
Cohesion: 0.27
Nodes (6): Check which tools are available in the environment., Check if a specific tool is available., Check if Docker is available., Get availability status of all tools., Get overall health status of the scanner., ToolAvailabilityChecker

### Community 111 - "HTTPX Scanner Plugin"
Cohesion: 0.25
Nodes (8): Network Vulnerability Assessment, External Asset Discovery, Web Discovery, Web Application Security Assessment, HTTPX Scanner Plugin, Nmap Scanner Plugin, Nuclei Scanner Plugin, Subfinder Scanner Plugin

### Community 112 - "Master AI Engineer Rules"
Cohesion: 0.25
Nodes (8): Coding Standards, Python Standards, TypeScript Standards, MVP Scope Definition, Build Later Items, Build Now Items, Never Build Items, Master AI Engineer Rules

### Community 113 - "semgrep.py"
Cohesion: 0.27
Nodes (8): _categorize_semgrep(), _extract_tags(), _normalize_one(), Any, Semgrep Plugin — normalizer. Converts raw `semgrep` output into canonical…, Categorize semgrep finding based on check_id and metadata., Extract tags from semgrep metadata., Normalize a single semgrep finding.

### Community 114 - "External VAPT Platform Adapters"
Cohesion: 0.29
Nodes (6): Adapters, Configuration, Deploying an external platform, External VAPT Platform Adapters, Health, How it works

### Community 115 - "PluginRegistry"
Cohesion: 0.05
Nodes (55): _count_by_capability(), _count_by_type(), disable_plugin(), enable_plugin(), get_plugin(), list_plugins(), plugins_info(), Any (+47 more)

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

### Community 123 - "app/layout.tsx"
Cohesion: 0.40
Nodes (3): inter, jetbrainsMono, metadata

### Community 127 - "reports.py"
Cohesion: 0.25
Nodes (14): details_env(), _dict_to_security_finding(), _finding_evidence(), _finding_to_security_finding(), generate_report(), GenerateReportRequest, list_reports(), list_templates() (+6 more)

### Community 128 - "error_handlers.py"
Cohesion: 0.31
Nodes (8): _map_error(), Any, FastAPI, Convert platform errors → HTTP responses. FastAPI exception handlers delegate…, Bind platform error handler., Shared mapping logic., register_exception_handlers(), _safe()

### Community 130 - "Project Roadmap"
Cohesion: 0.33
Nodes (6): Project Roadmap, Milestone 1 - AI-SecOS Core, Milestone 2 - First Plugin httpx, Milestone 3 - Discovery Capability, Milestone 4 - Web Security Assessment, Milestone 5 - Security Analyst UI

### Community 131 - "AstraIX App Icon"
Cohesion: 0.47
Nodes (6): AstraIX App Icon, White Check Mark, Slate and Cyan Palette, Rounded Square Background, Security Branding Motif, Cyan Shield Glyph

### Community 132 - "useActiveScansStore"
Cohesion: 0.24
Nodes (8): navigation, settingsNav, Sidebar(), LABELS, Topbar(), ActiveScan, ActiveScansState, useActiveScansStore

### Community 136 - "Technology Stack"
Cohesion: 0.40
Nodes (5): Technology Stack, AI Tech Stack, Backend Tech Stack, DevOps Tech Stack, Frontend Tech Stack

### Community 148 - "Trivy Security Scanner Plugin"
Cohesion: 0.50
Nodes (4): Trivy Security Scanner Plugin, cloud/posture capability, container/security capability, iac/security capability

### Community 152 - "recon.py"
Cohesion: 0.33
Nodes (8): _fetch_text(), _mine_text(), mine_web_surface(), Any, Web Surface Miner (recon) Mines the target's HTML + JS bundles to extract the…, Short human/LLM-readable summary of the mined surface., Fetch the target index + JS bundles and return the mined surface. Returns:: {…, summarize_surface()

### Community 153 - "dom_xss_scanner.py"
Cohesion: 0.56
Nodes (8): add(), chromium_available(), collect_scripts(), discover_urls(), http_get(), main(), render_dom(), scan_client_js()

### Community 154 - "KB Source List (Tier 1-3)"
Cohesion: 0.25
Nodes (8): Aif4thah Dojo-101, ElNiak awesome-ai-cybersecurity, GitHub Cybersecurity Topics, naveen-98 Cyber_Security_Reference, okhosting awesome-cyber-security, santosomar AI-agents-for-cybersecurity, KB Source List (Tier 1-3), tomwechsler Cyber Knowledge Base

### Community 155 - "get_role_permissions"
Cohesion: 0.50
Nodes (4): get_role_permissions(), has_permission(), Get permissions for a role., Check if a role has a specific permission.

### Community 156 - "FindingContextPayload"
Cohesion: 0.38
Nodes (4): FindingContextPayload, Any, What the AI sees. Pre-serialization. The AI Gateway *never* receives the raw…, Convenience: flatten to a dict for string substitution.

### Community 157 - "get_kb_source"
Cohesion: 0.22
Nodes (9): get_kb_source(), knowledge_stats(), list_kb_sources(), get, Search the cybersecurity knowledge base., Get knowledge base statistics., List all source documents stored on disk inside the knowledge base., Read a single source document from the knowledge base (path-traversal safe). (+1 more)

### Community 159 - "env.py"
Cohesion: 0.47
Nodes (4): do_run_migrations(), run_async_migrations(), run_migrations_online(), Connection

### Community 161 - "api_surface_scanner.py"
Cohesion: 0.36
Nodes (6): expand(), http(), is_content(), main(), Replace :param tokens with sample values., Heuristic: non-trivial body content that is not the SPA shell.

## Knowledge Gaps
- **330 isolated node(s):** `astraix-backend`, `entrypoint.sh script`, `eslintConfig`, `nextConfig`, `name` (+325 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **27 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BaseModel` connect `BaseModel` to `api.py`, `vapt_platforms.py`, `plugin_system/executor.py`, `Workflow`, `vapt/models.py`, `FindingEvidence`, `VAPTScanRequest`, `vapt/routes.py`, `VAPTTarget`, `CapabilityVersion`, `RoleName`, `AIOrchestrator`, `VAPTFinding`, `assessments.py`, `ResponseSchema`, `BasePlugin`, `repositories/__init__.py`, `SecurityFinding`, `value_objects.py`, `DefaultWorkflowEngine`, `BaseSchema`, `PluginRegistry`, `reports.py`?**
  _High betweenness centrality (0.132) - this node is a cross-community bridge._
- **Why does `SecurityFinding` connect `SecurityFinding` to `api.py`, `ReportFormat`, `ai_gateway/__init__.py`, `Severity`, `container.py`, `Workflow`, `FindingEvidence`, `semgrep.py`, `value_objects.py`, `DefaultFindingDeduplicator`, `shared/__init__.py`, `BaseModel`, `FindingContextPayload`, `reports.py`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Why does `VAPTFinding` connect `VAPTFinding` to `AIOrchestrator`, `flows_engine.py`, `vapt/normalizer.py`, `vapt/models.py`, `vapt/orchestrator.py`, `VAPTScanRequest`, `VAPTTarget`, `VAPTScanType`, `BaseModel`, `kb.py`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `SecurityFinding` (e.g. with `ContextBuilder` and `FindingContextPayload`) actually correct?**
  _`SecurityFinding` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Are the 52 inferred relationships involving `RoleName` (e.g. with `ApiKeyCreate` and `ApiKeyCreateResponse`) actually correct?**
  _`RoleName` has 52 INFERRED edges - model-reasoned connections that need verification._
- **What connects `astraix-backend`, `entrypoint.sh script`, `eslintConfig` to the rest of the system?**
  _330 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `_HttpAdapter` be split into smaller, more focused modules?**
  _Cohesion score 0.12873563218390804 - nodes in this community are weakly interconnected._