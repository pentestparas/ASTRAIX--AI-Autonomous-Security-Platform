# Graph Report - astraix-security-analyst  (2026-08-14)

## Corpus Check
- 258 files · ~181,438 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3203 nodes · 7724 edges · 186 communities (156 shown, 30 thin omitted)
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
- plugins/registry.py
- Container
- organizations.py
- capabilities/loader.py
- VAPTAdapter
- get_current_user
- User
- _KaliToolAdapter
- SecurityFinding
- EventDispatcher
- service.py
- ReconOrchestrator
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
- PluginRegistry
- devDependencies
- RoleName
- VAPTOutputParser
- LyrieAIAgent
- reports.py
- VAPTScanResult
- dependencies
- kb_snippets
- Knowledge Base Corpus
- NormalizerRegistry
- ExternalTool
- VAPTFinding
- assessments.py
- v1/__init__.py
- RecentAssessments.tsx
- ScanController
- ProviderManager
- AstraIX Full-Spectrum Platform Vision
- findings.py
- BasePlugin
- AssetIdentifier
- compilerOptions
- Orchestrator
- SystemStatus.tsx
- Finding Engine
- VAPT Executor (executor.py)
- UserRepository
- .run
- core/auth.py
- findings/page.tsx
- PromptTemplate
- metrics.py
- KnowledgeGraph
- kb.py
- Unified Security Hub
- kaggle-security-datasets/build.py
- ResponseSchema
- PostgreSQL
- XalgorixAdapter
- container.py
- garak_scanner.py
- infrastructure/logging.py
- settings.py
- AI Gateway
- Cybersecurity Knowledge Base
- ScanProgressBus
- CapabilityRegistry
- graph/page.tsx
- BaseRepository
- web_form_scanner.py
- AI-SecOS Core
- httpx/main.py
- DefaultTaskPlanner
- DefaultFindingDeduplicator
- PROJECT.md
- nmap/main.py
- DefaultWorkflowEngine
- New batch (curated + API-verified — 22 datasets)
- NmapScanner
- OrganizationRepository
- ScannerExecutor
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
- get_container
- .validate_invocation
- vapt/normalizer.py
- CHECKPOINT — AstraIX continuation point
- assets.py
- test_health.py
- System Architecture
- app/main.py
- .get_health_status
- HTTPX Scanner Plugin
- Master AI Engineer Rules
- core/logging.py
- External VAPT Platform Adapters
- PluginRegistry
- wordlists.py
- fetch-wordlists.sh
- get
- ai_secos_core/tests/conftest.py
- Report Base Template (base.html)
- download.sh
- AstraIX Platform Constitution
- app/layout.tsx
- graphify.js
- control.py
- PluginError
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
- services/orchestrator.py
- backend/tests/conftest.py
- KB Source List (Tier 1-3)
- Network VAPT Workflow
- FindingContextPayload
- ToolResult
- .transition
- env.py
- plugin.py
- list_capabilities
- Cloud Security Posture Assessment
- Static Application Security Testing
- test_m2_demo.py
- entrypoint.sh
- .child_asset
- Any
- next.config.js
- next-env.d.ts
- @hookform/resolvers
- _to_domain_finding
- @radix-ui/react-dropdown-menu
- .canonical_string
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

## Communities (186 total, 30 thin omitted)

### Community 0 - "_HttpAdapter"
Cohesion: 0.12
Nodes (10): _HttpAdapter, PentagiAdapter, Any, PentAGI - fully autonomous pentesting agent (Go backend, REST API)., RedAmon - agentic red team framework (graph-powered, webapp API)., Base for adapters that talk to an external HTTP API., zen-ai-pentest GitHub Action adapter (CI/CD). Requires a GitHub repo with the…, RedamonAdapter (+2 more)

### Community 1 - "api.py"
Cohesion: 0.07
Nodes (60): assess(), AssessRequest, AssessResponse, _bootstrap(), FindingSummary, Any, post, FastAPI app for the AI-SecOS Core Web UI. Run with: uvicorn api:app --reload… (+52 more)

### Community 2 - "api.ts"
Cohesion: 0.06
Nodes (41): formats, MIME_TYPES, templateIcons, apiKeysApi, assessmentsApi, assetsApi, findingsApi, graphApi (+33 more)

### Community 3 - "vapt_platforms.py"
Cohesion: 0.09
Nodes (43): Scanner Executor Service Enterprise-grade scanner execution with: - Async tool…, Check which tools are available in the environment., ToolAvailabilityChecker, AstraIX Security Scanner Module Enterprise-grade security scanning engine that…, Finding, Enum, str, Scanner Models Enterprise-grade data models for security scanning operations.… (+35 more)

### Community 4 - "plugin_system/executor.py"
Cohesion: 0.06
Nodes (53): Counter, Histogram, MetricsRegistry, Protocol, Monotonically increasing value, optionally labelled., Distribution value, optionally labelled., NoopTaskExecutor, PluginExecutionRequest (+45 more)

### Community 5 - "risk_engine/engine.py"
Cohesion: 0.09
Nodes (30): DefaultRiskEngine, _noop_severity_to_score(), NoopRiskEngine, Severity, Risk Engine — pipeline orchestrator and entry points. Two implementations are…, Identity: score derived directly from canonical severity. Used in tests and as…, A scored finding (or a typed wrapper around a SecurityFinding)., Engine port: score one or more canonical findings. (+22 more)

### Community 6 - "plugins/registry.py"
Cohesion: 0.27
Nodes (12): FindingOut, PluginOutput, load_manifest(), PluginLimits, PluginManifest, PluginSchema, Path, Load a plugin.json from a directory. (+4 more)

### Community 8 - "Container"
Cohesion: 0.07
Nodes (37): build_app(), lifespan(), FastAPI, FastAPI app factory. Binds the DI container to the web transport. -…, Start/stop lifetime management., Create the FastAPI application. Mostly configures routing + middleware; DI…, build_default_container(), Container (+29 more)

### Community 9 - "organizations.py"
Cohesion: 0.09
Nodes (46): ApiKeyCreate, create_api_key(), create_organization(), create_project(), delete_api_key(), delete_organization(), delete_project(), get_api_key() (+38 more)

### Community 10 - "capabilities/loader.py"
Cohesion: 0.11
Nodes (38): CapabilityResolverError, Raised when capability resolution fails (missing workflow, etc.)., Capability Registry — first-class Capability abstraction. Applications request…, CapabilityLoader, CapabilityLoaderError, LoadedCapability, _parse_asset_category(), _parse_framework() (+30 more)

### Community 11 - "VAPTAdapter"
Cohesion: 0.13
Nodes (18): AdapterStatus, Base classes and contracts for VAPT external adapters., True when the environment contains everything needed to attempt a run., True when the adapter should participate in scans., Return current availability status (should not raise)., Health/availability status of an adapter., Contract implemented by every external VAPT integration. Lifecycle during a…, VAPTAdapter (+10 more)

### Community 12 - "get_current_user"
Cohesion: 0.17
Nodes (19): api_key_header, decode_token(), get_current_active_user(), get_current_superuser(), get_current_user(), get_user_organizations(), get_user_projects(), AsyncSession (+11 more)

### Community 13 - "User"
Cohesion: 0.14
Nodes (30): delete_organization(), delete_project(), get_organization(), get_project(), list_api_keys(), list_memberships(), list_organizations(), list_projects() (+22 more)

### Community 14 - "_KaliToolAdapter"
Cohesion: 0.09
Nodes (10): _ContainerRunner, _KaliToolAdapter, LyrieAdapter, Any, RaccoonAdapter, Raccoon recon scanner (DNS/WHOIS/TLS/WAF/subdomains/dir-busting)., Minimal Docker-socket runner for one-shot commands in the Kali image., Filter crash/traceback/banner noise out of tool output before parsing. (+2 more)

### Community 15 - "SecurityFinding"
Cohesion: 0.04
Nodes (81): AssessmentId, _max_or_none(), _merge(), _promote_severity(), Severity, Deduplication: collapsing equivalent findings. Two findings with the same…, Merge a re-observed finding with its prior canonical record. Strategy: -…, Deterministic fingerprinting contract. Two findings with identical `(asset,… (+73 more)

### Community 16 - "EventDispatcher"
Cohesion: 0.10
Nodes (24): ProgressTicker, Streaming-aware Plugin Executor. Wraps the base `PluginExecutor` and emits…, Wraps a PluginExecutor to emit streaming events. The wrapper preserves the…, Background ticker to emit periodic plugin.progress events. Started when a…, StreamingPluginExecutor, emit_plugin_completed(), emit_plugin_finding(), emit_plugin_progress() (+16 more)

### Community 17 - "service.py"
Cohesion: 0.14
Nodes (18): Asset, AssessmentStatus, get_orchestrator(), Orchestrator, Assessment, AsyncSession, Enum, str (+10 more)

### Community 18 - "ReconOrchestrator"
Cohesion: 0.33
Nodes (3): Any, Attach a callback for live progress events (scan_id, event_type, data)., ReconOrchestrator

### Community 19 - "[id]/page.tsx"
Cohesion: 0.12
Nodes (27): react, cvssColor(), fmtLabel(), ProjectDetailPage(), registrableDomain(), severityConfig, statusOptions, QuickAction (+19 more)

### Community 20 - "vapt/routes.py"
Cohesion: 0.14
Nodes (34): get_scan_controller(), get_vapt_orchestrator(), get_progress_bus(), ApprovalDecision, _finding_fingerprint(), get_scan_progress(), list_approvals(), _mark_assessment_stopped() (+26 more)

### Community 21 - "shared/__init__.py"
Cohesion: 0.08
Nodes (30): Plugin Registry: what exists and how it is looked up. The Registry owns…, Workflow Engine — declarative Workflow + Capability resolution. A `Workflow` is…, WorkflowResolutionError, ConfigurationError, FindingEngineError, PluginError, Single error hierarchy for the entire AI-SecOS Core. Public API (the only types…, ReportEngineError (+22 more)

### Community 22 - "Workflow"
Cohesion: 0.08
Nodes (41): CancelledError, Cancellation token for running tasks/plans. The platform-wide cancellation…, A typed alias for cancellation that originates from the platform., NoopTaskExecutor, Task Executor — runs a Task. A planner produces Tasks; the executor is what…, Run a single Task and emit a result., Default at Milestone 1. The executor performs the bare minimum: a `result`-only…, TaskExecutor (+33 more)

### Community 23 - "VAPTScanType"
Cohesion: 0.10
Nodes (34): agent_loop_supported(), Autonomous VAPT Agent Loop (Phase 1) RedAmon-inspired agentic workflow: instead…, get_planner(), AI Planner Agent Decides the VAPT plan: which tools to run, in which phase, and…, get_vapt_executor(), ASTRAIX VAPT Module AI-Orchestrated Vulnerability Assessment & Penetration…, Enum, field_validator (+26 more)

### Community 24 - "MembershipRepository"
Cohesion: 0.10
Nodes (9): ApiKey, ApiKeyRepository, MembershipRepository, ProjectRepository, datetime, Project, UUID, Get a project with real asset/assessment/finding counts attached. (+1 more)

### Community 25 - "BaseModel"
Cohesion: 0.19
Nodes (43): ApiKeyCreate, ApiKeyCreateResponse, ApiKeyResponse, create_api_key(), create_organization(), create_project(), invite_member(), MembershipCreate (+35 more)

### Community 26 - "ToolRegistry"
Cohesion: 0.09
Nodes (20): get_tool_registry(), Enum, str, Kali Linux Security Tool Registry Comprehensive registry of security tools…, Tool categories matching VAPT workflow., Metadata about a security tool., Default configuration for a tool., Registry for managing security tools. (+12 more)

### Community 27 - "FastAPI Backend"
Cohesion: 0.10
Nodes (28): FastAPI Backend, Neo4j Knowledge Graph, Next.js Frontend, Redis, FastAPI Dependency, Neo4j Driver Dependency, Pydantic v2 Dependency, redis Python Client Dependency (+20 more)

### Community 28 - "scans/page.tsx"
Cohesion: 0.09
Nodes (28): Finding, getSeverityBadge(), getTypeIcon(), getTypeLabel(), LiveScanConsole(), phaseIcons, PlanPhase, PlanTool (+20 more)

### Community 29 - "PluginRegistry"
Cohesion: 0.09
Nodes (18): LoadedPlugin, PluginLoader, PluginLoaderError, Path, PluginError, PluginManifest, Plugin Loader: read manifests from disk → PluginRecords. The Loader is the…, A loader-level result wrapping a successfully parsed manifest. (+10 more)

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

### Community 34 - "reports.py"
Cohesion: 0.10
Nodes (43): AssessmentModel, _ai_comment_placeholder(), _build_section(), _findings_section(), NullReportEngine, ReportRequest, Report Engine — implementation. At Milestone 1, only the JSON/Markdown default…, Render reports from findings + risk scores. (+35 more)

### Community 35 - "VAPTScanResult"
Cohesion: 0.10
Nodes (18): kb_ready(), Result from a VAPT scan., VAPTScanResult, AIOrchestrator, Any, Analyze target and run the AI-planned scan with live progress events., Run the autonomous agent loop, falling back to the classic phased recon…, Run all enabled external adapters in parallel against the target. Adapters run… (+10 more)

### Community 36 - "dependencies"
Cohesion: 0.07
Nodes (29): axios, class-variance-authority, clsx, d3-force, dagre, date-fns, dependencies, axios (+21 more)

### Community 37 - "kb_snippets"
Cohesion: 0.19
Nodes (7): kb_snippets(), Formatted KB snippets, e.g. ``[source/title] text``, for prompts., PlannerAgent, Any, Ask the LLM (NVIDIA NIM, falling back to Ollama) to refine tool selection.…, Generate the full phased VAPT plan with KB-grounded reasoning., Knowledge-base-grounded plan generator for VAPT scans.

### Community 38 - "Knowledge Base Corpus"
Cohesion: 0.12
Nodes (19): OWASP Projects (ADR Tier 3), paulveillard/cybersecurity (ADR Tier 1), Anthropic Cybersecurity Skills Repo, awesome-soc Repo, Berkanktk/CyberSecurity Repo, CAI (Cybersecurity AI) Repo, cybersecurity-knowledge-base Repo, Cybersecurity-Resources Repo (+11 more)

### Community 39 - "NormalizerRegistry"
Cohesion: 0.09
Nodes (27): FindingCorrelator, NoopFindingCorrelator, Finding Correlator — the contract + the no-op default. Correlators detect…, Adds correlation metadata to findings., Return the same set of findings, possibly tagged with correlation., Identity correlator. The default at Milestone 1., FindingDeduplicator, Stateful dedupe of findings by fingerprint. (+19 more)

### Community 40 - "ExternalTool"
Cohesion: 0.14
Nodes (14): ExternalTool, Any, ScanRequest, Execute a complete security scan., Get tools for a given capability., Execute a single tool and return parsed findings., Execute multiple tools in parallel., Build command list for tool execution. (+6 more)

### Community 41 - "VAPTFinding"
Cohesion: 0.06
Nodes (11): Run exactly one tool against the target for the autonomous agent. Returns…, Synthetic findings so the agent loop works in demo mode., Reduce a URL target to bare host[:port] for host-oriented tools., Extract an explicit port from a URL target, else the scheme default., Map loopback targets to the Docker gateway host. Tool containers run in…, Emit findings ONLY when sqlmap confirms an injection point. sqlmap…, VAPTExecutor, A security finding from VAPT scan. (+3 more)

### Community 42 - "assessments.py"
Cohesion: 0.16
Nodes (22): cancel_assessment(), create_assessment(), get_assessment(), list_assessments(), AsyncSession, delete, get, post (+14 more)

### Community 43 - "v1/__init__.py"
Cohesion: 0.14
Nodes (20): get_dashboard_activity(), get_dashboard_stats(), list_capabilities(), ping(), AsyncSession, get, post, UUID (+12 more)

### Community 44 - "RecentAssessments.tsx"
Cohesion: 0.11
Nodes (22): statusConfig, FindingDetail(), formatDetails(), severityStyles, Badge(), BadgeProps, CardDescription, CardFooter (+14 more)

### Community 45 - "ScanController"
Cohesion: 0.10
Nodes (11): Any, Store the agent loop's partial results so an aborted/timed-out loop can still…, Register a pending operator decision for a dangerous tool call., Settle a pending approval. Returns False when unknown or already settled., Wait for the operator's decision. None = timed out / not resolved., A pending operator decision for a dangerous agent tool call., Registry + control flags for scans currently executing in-process., Track a running scan so control endpoints can reach its task. (+3 more)

### Community 46 - "ProviderManager"
Cohesion: 0.19
Nodes (8): ProviderAlreadyRegisteredError, ProviderManager, ProviderNotFoundError, Provider Manager. The Manager owns the lifecycle of providers. Applications…, Thread-safe registry of providers. The Manager is the *only* place providers…, AIProvider, Concrete providers (OpenAI/Anthropic/...) implement this., AIError

### Community 47 - "AstraIX Full-Spectrum Platform Vision"
Cohesion: 0.09
Nodes (29): AstraIX Security Analyst Platform, Data Architecture (Hot/Warm/Cold), Deployment Options, Integration Ecosystem (100+ Native), AstraIX Full-Spectrum Platform Vision, Platform Roadmap (5 Phases to 2027), VAPT Capability, ASTRAIX AI Modules (+21 more)

### Community 48 - "findings.py"
Cohesion: 0.14
Nodes (22): bulk_update_findings(), BulkUpdateRequest, delete_finding(), get_finding(), list_findings(), AsyncSession, delete, get (+14 more)

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
Cohesion: 0.23
Nodes (13): Finding Engine, web/discovery capability, HTTP Probe (httpx) Plugin, Semgrep SAST Scanner Plugin, Subfinder Subdomain Enumeration Plugin, Report Engine, code/audit capability, sast/security capability (+5 more)

### Community 55 - "VAPT Executor (executor.py)"
Cohesion: 0.18
Nodes (20): Docker Socket, KALI_IMAGE Env Var, VAPT_DEMO_MODE Env Var, VAPT_USE_DOCKER Env Var, gobuster, astraix-kali Image, nikto, nmap (+12 more)

### Community 56 - "UserRepository"
Cohesion: 0.15
Nodes (13): login(), login_json(), OAuth2 compatible login for Swagger UI., JSON-based login for frontend applications., Refresh access token., refresh_token(), create_access_token(), create_refresh_token() (+5 more)

### Community 57 - ".run"
Cohesion: 0.17
Nodes (13): AgentLoop, get_agent_loop(), Any, The autonomous tool-calling loop with phase + approval gating., Ground the agent with methodology guidance from the knowledge base, specific to…, Ground newly observed vuln classes in KB so the next tool decision exploits…, Return (rejected, reason) when the model may NOT write a final report yet -…, Call the LLM with function tools; return (text, tool_calls). Prefers NVIDIA NIM… (+5 more)

### Community 58 - "core/auth.py"
Cohesion: 0.11
Nodes (34): get_role_permissions(), has_permission(), Get permissions for a role., Check if a role has a specific permission., Base, get_session(), AsyncSession, Assessment (+26 more)

### Community 59 - "findings/page.tsx"
Cohesion: 0.20
Nodes (15): cvssColor(), FindingsPage(), severityConfig, statusOptions, roleConfig, Card, CardContent, Table (+7 more)

### Community 60 - "PromptTemplate"
Cohesion: 0.17
Nodes (8): _InMemoryPromptManager, PromptTemplate, PromptVersionError, Any, Exception, Raised when a requested `prompt_id` / version combination is unknown., One version of one prompt. The text uses stdlib `Template` semantics ($-style…, Process-local default; replace with persistence later if needed.

### Community 61 - "metrics.py"
Cohesion: 0.25
Nodes (3): _NoopCounter, _NoopHistogram, Metrics primitives (stubs at Milestone 1). These are typed protocols so…

### Community 62 - "KnowledgeGraph"
Cohesion: 0.13
Nodes (9): get_graph(), get, get_knowledge_graph(), KnowledgeGraph, _node_id(), _node_tooltip(), Any, Record one agent-loop step as a ChainStep node linked to the target (target… (+1 more)

### Community 63 - "kb.py"
Cohesion: 0.14
Nodes (18): apply_finding_relevance_floor(), get_kb(), is_semantic_kb(), kb_context_for_finding(), kb_sources_for(), kb_stats(), Any, Shared knowledge-base client for the whole VAPT AI pipeline. The AstraIX… (+10 more)

### Community 64 - "Unified Security Hub"
Cohesion: 0.13
Nodes (19): Application Security Module, Cloud Security Module, Dark-Moon Platform, Data Security Module, Defensive Security Module, Email Security Module, GRC & Compliance Module, Identity Security Module (+11 more)

### Community 65 - "kaggle-security-datasets/build.py"
Cohesion: 0.23
Nodes (19): find_dataset_dir(), handle_ai_generic(), handle_cve_generic(), handle_ids_generic(), handle_phish_generic(), handle_siem_generic(), main(), Path (+11 more)

### Community 66 - "ResponseSchema"
Cohesion: 0.13
Nodes (28): get_kb_source(), knowledge_stats(), list_kb_sources(), get, Search the cybersecurity knowledge base., Get knowledge base statistics., List all source documents stored on disk inside the knowledge base., Read a single source document from the knowledge base (path-traversal safe). (+20 more)

### Community 67 - "PostgreSQL"
Cohesion: 0.09
Nodes (24): Auth API (auth.py), Demo Credentials, PostgreSQL, Quick Scan API Endpoint, VAPT Routes (routes.py), VAPT Scan Route Handler (route.ts), Alembic Migrations Dependency, asyncpg Dependency (+16 more)

### Community 69 - "container.py"
Cohesion: 0.07
Nodes (54): ABC, ContextBuilder, NullContextBuilder, Context Builder — assembles what's fed into a prompt. Pre-AI responsibilities:…, Build a `FindingContextPayload` from typed inputs., Default at Milestone 1. Performs no compression or redaction. A future…, AIGateway, DefaultAIGateway (+46 more)

### Community 70 - "garak_scanner.py"
Cohesion: 0.20
Nodes (16): add(), _attempt_prompt(), direct_probe(), find_chat_endpoint(), guess_response_field(), http(), main(), parse_garak_report() (+8 more)

### Community 71 - "infrastructure/logging.py"
Cohesion: 0.11
Nodes (21): platform_error_to_http_response(), PlatformErrorResponse, Map platform errors → HTTP responses. FastAPI exception handler in `platform/`…, Convert a PlatformError to a status/body pair. `correlation_id` is included so…, Cross-cutting infrastructure components. This package provides: - Structured…, bind_correlation_id(), _console_formatter(), _CorrelationIdFilter (+13 more)

### Community 72 - "settings.py"
Cohesion: 0.19
Nodes (14): Platform-wide constants. Pure values that have no dependency on environment…, AI-SecOS Core configuration package. Single point of access to typed settings.…, AIGatewaySettings, FindingEngineSettings, ObservabilitySettings, PlatformSettings, BaseSettings, Typed platform settings (Pydantic v2, 12-factor). Loading model: - All values… (+6 more)

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
Cohesion: 0.10
Nodes (16): CapabilityAlreadyRegisteredError, CapabilityNotFoundError, Capability-specific error types., Raised when attempting to register a duplicate capability., Raised when a capability is not found in the registry., CapabilityVersion, Semantic version (major.minor.patch)., CapabilityRegistry (+8 more)

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

### Community 82 - "DefaultTaskPlanner"
Cohesion: 0.17
Nodes (10): CancellationToken, Lightweight, async-friendly cancellation., Any, TaskRunResult, DefaultTaskPlanner, Any, Default planner: DAG scheduler with retries + parallel workers., Any (+2 more)

### Community 83 - "DefaultFindingDeduplicator"
Cohesion: 0.17
Nodes (7): DefaultFindingDeduplicator, In-memory implementation. Suitable for single-process Milestone 1 / Milestone 2…, DefaultFindingFingerprinter, FindingFingerprinter, Computes fingerprints for findings., Default deterministic fingerprinter. The hash is built from fields that…, Stable byte representation (sorted keys, list-of-tuples).

### Community 84 - "PROJECT.md"
Cohesion: 0.14
Nodes (12): Communication, In Scope (PoC), Mission, Out of Scope (PoC), Project Charter, Project Overview, Risks & Mitigations, Scope (+4 more)

### Community 85 - "nmap/main.py"
Cohesion: 0.24
Nodes (13): build_nmap_command(), main(), _parse_host(), parse_nmap_xml(), _parse_port(), Any, Parse a single host element., Parse a port element. (+5 more)

### Community 86 - "DefaultWorkflowEngine"
Cohesion: 0.13
Nodes (15): CapabilityResolver, Any, Capability, Validate inputs against the capability's input schema (lightweight). Performs…, Raised when capability resolution fails., A Capability fully resolved to executable Workflows., Resolves Capabilities to WorkflowRecords ready for the Task Planner., ResolutionError (+7 more)

### Community 87 - "New batch (curated + API-verified — 22 datasets)"
Cohesion: 0.17
Nodes (11): A. Vulnerabilities & CVE / exploit data, Already ingested (existing 3 — DO NOT re-download), B. Network intrusion & malware traffic, C. Malware, D. Phishing / URL / email security, E. Threat intel / SIEM / logs, Expected totals (rough estimate), F. AI / LLM security (+3 more)

### Community 88 - "NmapScanner"
Cohesion: 0.22
Nodes (6): NmapScanner, PluginError, PluginOutput, Run as process: stdin → scan → stdout, Run nmap, parse output, return findings., Parse Nmap XML/text → findings.

### Community 89 - "OrganizationRepository"
Cohesion: 0.17
Nodes (8): get_api_key_repo(), get_membership_repo(), get_org_repo(), get_project_repo(), get_user_repo(), AsyncSession, OrganizationRepository, Organization

### Community 90 - "ScannerExecutor"
Cohesion: 0.13
Nodes (16): PluginRegistry, get_scanner_executor(), Any, Finding, ScanRequest, VAPTExecutor, Create appropriate executor for scan request., Get tools for a scan request. (+8 more)

### Community 91 - "Release 0.1.0"
Cohesion: 0.15
Nodes (13): Finding Normalizer (normalizer.py), Kali Tools Dockerfile, Risk Scoring Engine, Custom Kali Image (astraix-kali), Docker Compose Stack, Frontend Dashboard, Keep a Changelog Format, Normalized Findings (+5 more)

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
Cohesion: 0.31
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

### Community 102 - "get_container"
Cohesion: 0.15
Nodes (18): get_container(), Request, FastAPI dependency: immutable container wired to pathOps., _map_error(), Any, FastAPI, Convert platform errors → HTTP responses. FastAPI exception handlers delegate…, Bind platform error handler. (+10 more)

### Community 103 - ".validate_invocation"
Cohesion: 0.32
Nodes (5): Any, PluginManifest, Tiny subset of JSON Schema type matching for type-checking most params., _type_match(), ValidationResult

### Community 104 - "vapt/normalizer.py"
Cohesion: 0.36
Nodes (7): canonical_vuln_name(), cvss_for_severity(), normalize_finding(), normalize_findings(), Finding normalization: canonical vulnerability names + CVSS scores. Raw tool…, Map a raw finding title/type onto a standard vulnerability name., Return the finding with a canonical title/type and a CVSS score.

### Community 105 - "CHECKPOINT — AstraIX continuation point"
Cohesion: 0.29
Nodes (6): 1. System state after restart, 2. Product features live right now, 3. Scan history (validated), 4. Known issues / gotchas, 5. Next steps (when resuming), CHECKPOINT — AstraIX continuation point

### Community 106 - "assets.py"
Cohesion: 0.22
Nodes (17): create_asset(), delete_asset(), get_asset(), list_assets(), AsyncSession, delete, get, patch (+9 more)

### Community 107 - "test_health.py"
Cohesion: 0.43
Nodes (6): AsyncClient, client(), asyncio, fixture, test_health_check(), test_root()

### Community 108 - "System Architecture"
Cohesion: 0.25
Nodes (9): System Architecture, Applications Layer, Plugin Executor, Plugin Manager, Plugin Sandbox, Plugin Validator, Plugins Layer, SecurityPlugin PDK (+1 more)

### Community 109 - "app/main.py"
Cohesion: 0.17
Nodes (15): close_db(), init_db(), health_check(), lifespan(), FastAPI, get, AstraIX Security Analyst - Main Application Entry point for the FastAPI…, Root endpoint: health/status overview. (+7 more)

### Community 110 - ".get_health_status"
Cohesion: 0.25
Nodes (4): Check if a specific tool is available., Check if Docker is available., Get availability status of all tools., Get overall health status of the scanner.

### Community 111 - "HTTPX Scanner Plugin"
Cohesion: 0.25
Nodes (8): Network Vulnerability Assessment, External Asset Discovery, Web Discovery, Web Application Security Assessment, HTTPX Scanner Plugin, Nmap Scanner Plugin, Nuclei Scanner Plugin, Subfinder Scanner Plugin

### Community 112 - "Master AI Engineer Rules"
Cohesion: 0.25
Nodes (8): Coding Standards, Python Standards, TypeScript Standards, MVP Scope Definition, Build Later Items, Build Now Items, Never Build Items, Master AI Engineer Rules

### Community 113 - "core/logging.py"
Cohesion: 0.20
Nodes (10): post, Rebuild FAISS vector index from chunks.json., rebuild_knowledge_index(), get_settings(), BaseSettings, Application settings. Loaded from `.env` or process-level env vars., Settings, get_logger() (+2 more)

### Community 114 - "External VAPT Platform Adapters"
Cohesion: 0.29
Nodes (6): Adapters, Configuration, Deploying an external platform, External VAPT Platform Adapters, Health, How it works

### Community 115 - "PluginRegistry"
Cohesion: 0.15
Nodes (8): get_plugin_registry(), PluginRegistry, Run subprocess synchronously. Returns (stdout, stderr)., Enable a plugin by ID. Returns True if found., Disable a plugin by ID. Returns True if found., Singleton plugin registry., Lifecycle: discover → load → run → results. Plugins are subprocesses: -…, Discover plugins and validate manifests. Returns: list of plugin IDs.

### Community 116 - "wordlists.py"
Cohesion: 0.24
Nodes (9): Get status of curated wordlists baked into the Kali image., wordlists_health(), list_wordlists(), _probe_image(), Wordlist resolver — curated wordlists baked into the astraix-kali image. Lists…, Purpose -> {path, lines, present} verified inside the Kali image., Alias for wordlist_health() — used by the API endpoint., Run one `wc -l` over every curated list inside the Kali image. (+1 more)

### Community 117 - "fetch-wordlists.sh"
Cohesion: 0.67
Nodes (5): dedupe(), fetch(), fetch_soft(), log(), fetch-wordlists.sh script

### Community 118 - "get"
Cohesion: 0.16
Nodes (14): adapters_health(), get_assessment(), list_tools(), get, UUID, Get status of all VAPT tools., Check VAPT tools health., Get health of all external VAPT platform adapters. (+6 more)

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

### Community 127 - "control.py"
Cohesion: 0.18
Nodes (6): Exception, Scan Control Channel In-process control plane for active scans: pause, resume,…, Cooperative pause/stop gate. No-op for scans that are not registered. While…, Raised at a checkpoint when the scan was stopped by the user., ScanStoppedError, Scan Progress Bus Redis-backed event stream for live scan progress. Each scan…

### Community 128 - "PluginError"
Cohesion: 0.28
Nodes (6): PluginError, Any, PluginManifest, Execute plugin subprocess. Returns (output, error)., Get manifests of all registered plugins., Run plugin as subprocess. Args: plugin_id: Plugin identifier params: Plugin…

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

### Community 152 - "services/orchestrator.py"
Cohesion: 0.25
Nodes (6): get_session(), AsyncSession, Database session dependency., AssessmentStatus, Orchestrator Service The orchestrator runs assessments via the plugin system:…, Assessment lifecycle states.

### Community 153 - "backend/tests/conftest.py"
Cohesion: 0.32
Nodes (7): mock_orchestrator(), mock_registry(), mock_settings(), fixture, Pytest configuration and fixtures., Mock settings for tests., Mock plugin registry.

### Community 154 - "KB Source List (Tier 1-3)"
Cohesion: 0.25
Nodes (8): Aif4thah Dojo-101, ElNiak awesome-ai-cybersecurity, GitHub Cybersecurity Topics, naveen-98 Cyber_Security_Reference, okhosting awesome-cyber-security, santosomar AI-agents-for-cybersecurity, KB Source List (Tier 1-3), tomwechsler Cyber Knowledge Base

### Community 155 - "Network VAPT Workflow"
Cohesion: 0.39
Nodes (8): network/recon capability, network/vuln-scan capability, api/security capability, web/vuln-scan capability, Nmap Port Scanner Plugin, Nuclei Vulnerability Scanner Plugin, Network VAPT Workflow, Web Application VAPT Workflow

### Community 156 - "FindingContextPayload"
Cohesion: 0.38
Nodes (4): FindingContextPayload, Any, What the AI sees. Pre-serialization. The AI Gateway *never* receives the raw…, Convenience: flatten to a dict for string substitution.

### Community 157 - "ToolResult"
Cohesion: 0.29
Nodes (4): Execute a single tool., Add a tool result and update aggregated findings., Result from a single security tool execution., ToolResult

### Community 158 - ".transition"
Cohesion: 0.33
Nodes (5): AssessmentTransition, Any, datetime, Record a state transition. Returns self (for fluent use)., A single lifecycle event on an Assessment.

### Community 159 - "env.py"
Cohesion: 0.47
Nodes (4): do_run_migrations(), run_async_migrations(), run_migrations_online(), Connection

### Community 160 - "plugin.py"
Cohesion: 0.50
Nodes (4): PluginStatus, PluginType, Enum, str

### Community 161 - "list_capabilities"
Cohesion: 0.50
Nodes (4): index(), list_capabilities(), get, List available capabilities.

### Community 164 - "test_m2_demo.py"
Cohesion: 0.50
Nodes (3): M2 End-to-End test. Validates the vertical slice: Capability → Plugin →…, The full M2 path executes end-to-end and emits a summary., test_m2_demo_runs()

### Community 171 - "_to_domain_finding"
Cohesion: 0.67
Nodes (3): Finding, Map a VAPTFinding to the domain Finding model, packing the rich forensic fields…, _to_domain_finding()

## Knowledge Gaps
- **314 isolated node(s):** `astraix-backend`, `entrypoint.sh script`, `eslintConfig`, `nextConfig`, `name` (+309 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **30 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BaseModel` connect `BaseModel` to `PluginError`, `api.py`, `vapt_platforms.py`, `plugin_system/executor.py`, `plugins/registry.py`, `SecurityFinding`, `vapt/routes.py`, `shared/__init__.py`, `Workflow`, `VAPTScanType`, `ToolResult`, `RoleName`, `plugin.py`, `reports.py`, `VAPTScanResult`, `VAPTFinding`, `assessments.py`, `findings.py`, `BasePlugin`, `core/auth.py`, `BaseSchema`, `assets.py`, `get`?**
  _High betweenness centrality (0.131) - this node is a cross-community bridge._
- **Why does `SecurityFinding` connect `SecurityFinding` to `api.py`, `reports.py`, `container.py`, `risk_engine/engine.py`, `NormalizerRegistry`, `DefaultFindingDeduplicator`, `shared/__init__.py`, `Workflow`, `BaseModel`, `FindingContextPayload`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Why does `Asset` connect `api.py` to `OrganizationRepository`, `.child_asset`, `.canonical_string`, `BaseRepository`, `service.py`, `AssetIdentifier`, `vapt/routes.py`, `get`, `MembershipRepository`, `BaseModel`, `UserRepository`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `SecurityFinding` (e.g. with `ContextBuilder` and `FindingContextPayload`) actually correct?**
  _`SecurityFinding` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Are the 52 inferred relationships involving `RoleName` (e.g. with `ApiKeyCreate` and `ApiKeyCreateResponse`) actually correct?**
  _`RoleName` has 52 INFERRED edges - model-reasoned connections that need verification._
- **What connects `astraix-backend`, `entrypoint.sh script`, `eslintConfig` to the rest of the system?**
  _314 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `_HttpAdapter` be split into smaller, more focused modules?**
  _Cohesion score 0.11931818181818182 - nodes in this community are weakly interconnected._