# Graph Report - .  (2026-08-04)

## Corpus Check
- 65 files · ~101,983 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3060 nodes · 5872 edges · 248 communities (186 shown, 62 thin omitted)
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 1088 edges (avg confidence: 0.58)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Metrics Registry
- AI-SecOS Core API
- Frontend Pages & Auth
- Scanner Executor
- AI Gateway Context
- Finding Correlator
- Plugin Registry
- KB Ingest & Embedding
- CrewAI Vulnerability Mgmt
- Org & Project API
- Capability Errors
- FastAPI App Lifespan
- DI Container
- Auth & Membership
- Findings UI
- Risk Types
- Risk Engine
- Finding Fingerprint
- Task Cancellation
- Projects & Quick Actions
- Docker Compose Stack
- VAPT Scan Pipeline
- Knowledge Base Endpoints
- Reports UI
- ORM Models
- Asset Model & Repo
- Researcher Agent
- Verifier Agent
- VAPT Orchestrator
- Pentest Graph Nodes
- Progress Bus (Redis)
- Scan Routes
- Planner Agent
- Docker Executor
- System Status UI
- Sidebar & Layout
- Worklog & Session State
- Dashboard Stats
- KB Source URLs
- Neo4j Graph DB
- Report Engine
- Community 41
- Community 42
- Community 43
- Community 44
- Community 45
- Community 46
- Community 47
- Community 48
- Community 49
- Community 50
- Community 51
- Community 52
- Community 53
- Community 54
- Community 55
- Community 56
- Community 57
- Community 58
- Community 59
- Community 60
- Community 61
- Community 62
- Community 63
- Community 64
- Community 65
- Community 66
- Community 67
- Community 68
- Community 69
- Community 70
- Community 71
- Community 72
- Community 73
- Community 74
- Community 75
- Community 76
- Community 77
- Community 78
- Community 79
- Community 80
- Community 81
- Community 82
- Community 83
- Community 84
- Community 85
- Community 86
- Community 87
- Community 88
- Community 89
- Community 90
- Community 91
- Community 92
- Community 93
- Community 94
- Community 95
- Community 96
- Community 97
- Community 98
- Community 99
- Community 100
- Community 101
- Community 102
- Community 103
- Community 104
- Community 105
- Community 106
- Community 107
- Community 108
- Community 109
- Community 110
- Community 111
- Community 112
- Community 113
- Community 114
- Community 115
- Community 116
- Community 117
- Community 118
- Community 119
- Community 120
- Community 121
- Community 122
- Community 123
- Community 124
- Community 125
- Community 126
- Community 127
- Community 128
- Community 129
- Community 130
- Community 131
- Community 132
- Community 133
- Community 134
- Community 135
- Community 136
- Community 138
- Community 139
- Community 140
- Community 142
- Community 143
- Community 144
- Community 145
- Community 146
- Community 148
- Community 149
- Community 150
- Community 151
- Community 152
- Community 154
- Community 155
- Community 157
- Community 158
- Community 159
- Community 160
- Community 161
- Community 162
- Community 163
- Community 164
- Community 165
- Community 166
- Community 167
- Community 168
- Community 169
- Community 170
- Community 171
- Community 172
- Community 173
- Community 174
- Community 175
- Community 176
- Community 180
- Community 181
- Community 182
- Community 185
- Community 189
- Community 190
- Community 191
- Community 192
- Community 193
- Community 194
- Community 198
- Community 199
- Community 200
- Community 201
- Community 202
- Community 207
- Community 209
- Community 210
- Community 213
- Community 214
- Community 236
- Community 237
- Community 238
- Community 239
- Community 241
- Community 242
- Community 244
- Community 245
- Community 247

## God Nodes (most connected - your core abstractions)
1. `SecurityFinding` - 75 edges
2. `MembershipRepository` - 54 edges
3. `ProjectRepository` - 50 edges
4. `ApiKeyRepository` - 49 edges
5. `OrganizationRepository` - 48 edges
6. `Container` - 47 edges
7. `_MutableContainer` - 44 edges
8. `BaseModel` - 42 edges
9. `UserRepository` - 42 edges
10. `RoleName` - 36 edges

## Surprising Connections (you probably didn't know these)
- `AI Integration Architecture` --semantically_similar_to--> `AI Gateway`  [INFERRED] [semantically similar]
  docs/ARCHITECTURE_OVERVIEW.md → AGENTS.md
- `Custom Kali Image (astraix-kali)` --semantically_similar_to--> `astraix-kali Image`  [INFERRED] [semantically similar]
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

## Communities (248 total, 62 thin omitted)

### Community 0 - "Metrics Registry"
Cohesion: 0.07
Nodes (42): Counter, Histogram, MetricsRegistry, _NoopCounter, _NoopHistogram, Metrics primitives (stubs at Milestone 1).  These are typed protocols so service, Monotonically increasing value, optionally labelled., Distribution value, optionally labelled. (+34 more)

### Community 1 - "AI-SecOS Core API"
Cohesion: 0.07
Nodes (51): assess(), AssessRequest, AssessResponse, _bootstrap(), FindingSummary, list_capabilities(), FastAPI app for the AI-SecOS Core Web UI.  Run with: uvicorn api:app --reload --, Convert 'https://example.com:443' to 'asset_example_com'. (+43 more)

### Community 2 - "Frontend Pages & Auth"
Cohesion: 0.05
Nodes (38): formats, templates, apiKeysApi, assessmentsApi, assetsApi, authApi, graphApi, healthApi (+30 more)

### Community 3 - "Scanner Executor"
Cohesion: 0.10
Nodes (45): Scanner Executor Service  Enterprise-grade scanner execution with: - Async tool, Check which tools are available in the environment., ToolAvailabilityChecker, AstraIX Security Scanner Module  Enterprise-grade security scanning engine that, Finding, BaseModel, Enum, str (+37 more)

### Community 4 - "AI Gateway Context"
Cohesion: 0.07
Nodes (43): ContextBuilder, NullContextBuilder, Context Builder — assembles what's fed into a prompt.  Pre-AI responsibilities:, Build a `FindingContextPayload` from typed inputs., Default at Milestone 1.      Performs no compression or redaction. A future mile, AIGateway, DefaultAIGateway, AI Gateway — composed pipeline.  Pipeline order (matches Architecture):    1. Ro (+35 more)

### Community 5 - "Finding Correlator"
Cohesion: 0.07
Nodes (34): FindingCorrelator, NoopFindingCorrelator, Finding Correlator — the contract + the no-op default.  Correlators detect patte, Adds correlation metadata to findings., Return the same set of findings, possibly tagged with correlation., Identity correlator. The default at Milestone 1., DefaultFindingDeduplicator, FindingDeduplicator (+26 more)

### Community 6 - "Plugin Registry"
Cohesion: 0.07
Nodes (39): _count_by_capability(), _count_by_type(), disable_plugin(), enable_plugin(), get_plugin(), list_plugins(), plugins_info(), Any (+31 more)

### Community 7 - "KB Ingest & Embedding"
Cohesion: 0.06
Nodes (30): chunk_by_lines(), extract_title(), get_files(), main(), Fast knowledge base ingestion - line-based chunking., main(), Test basic connectivity to Shodan API., Test that required environment variables are set. (+22 more)

### Community 8 - "CrewAI Vulnerability Mgmt"
Cohesion: 0.07
Nodes (30): after_kickoff, agent, BaseTool, before_kickoff, crew, CrewBase, VulnerabilityManagement crew for comprehensive vulnerability assessment and…, Creates the VulnerabilityManagement crew with sequential process for systematic… (+22 more)

### Community 9 - "Org & Project API"
Cohesion: 0.09
Nodes (46): ApiKeyCreate, create_api_key(), create_organization(), create_project(), delete_api_key(), delete_organization(), delete_project(), get_api_key() (+38 more)

### Community 10 - "Capability Errors"
Cohesion: 0.09
Nodes (37): CapabilityAlreadyRegisteredError, CapabilityResolverError, Capability-specific error types., Raised when attempting to register a duplicate capability., Raised when capability resolution fails (missing workflow, etc.)., CapabilityLoader, CapabilityLoaderError, LoadedCapability (+29 more)

### Community 11 - "FastAPI App Lifespan"
Cohesion: 0.07
Nodes (39): AsyncClient, health_check(), lifespan(), get, AstraIX Security Analyst - Main Application Entry point for the FastAPI…, Readiness check (validates dependencies)., Application startup/shutdown., Root endpoint: health/status overview. (+31 more)

### Community 12 - "DI Container"
Cohesion: 0.07
Nodes (37): api_key_header, get_container(), get_settings(), Dependency providers for FastAPI routes., FastAPI dependency: immutable container wired to pathOps., Shortcut: typed settings., health(), FastAPI transport: health, ready, version.  All other API routes beyond these th (+29 more)

### Community 13 - "Auth & Membership"
Cohesion: 0.10
Nodes (39): create_project(), delete_organization(), delete_project(), get_api_key_repo(), get_membership_repo(), get_org_repo(), get_organization(), get_project() (+31 more)

### Community 14 - "Findings UI"
Cohesion: 0.14
Nodes (27): statusConfig, severityConfig, statusOptions, findingsApi, cn(), roleConfig, Badge(), BadgeProps (+19 more)

### Community 15 - "Risk Types"
Cohesion: 0.07
Nodes (27): Enum, PluginType, Typed outputs of the Risk Engine.  A `RiskScore` is a 0–100 value clipped and bo, Where a risk axis got its number., RiskFactorSource, AssessmentResult, AssessmentStatus, AssessmentTransition (+19 more)

### Community 16 - "Risk Engine"
Cohesion: 0.09
Nodes (21): DefaultRiskEngine, _noop_severity_to_score(), NoopRiskEngine, Risk Engine — pipeline orchestrator and entry points.  Two implementations are s, Identity: score derived directly from canonical severity.      Used in tests and, A scored finding (or a typed wrapper around a SecurityFinding)., Engine port: score one or more canonical findings., Score each canonical finding. (+13 more)

### Community 17 - "Finding Fingerprint"
Cohesion: 0.09
Nodes (29): Convenience: flatten to a dict for string substitution., Any, FindingFingerprint, _confidence(), _extract_items(), make_httpx_input(), _normalize_one(), _normalize_tech() (+21 more)

### Community 18 - "Task Cancellation"
Cohesion: 0.09
Nodes (29): CancelledError, Cancellation token for running tasks/plans.  The platform-wide cancellation cont, A typed alias for cancellation that originates from the platform., PlannedExecution, Task Planner — the dynamic heart of the platform.  Per ARCHITECTURE.md:    - Wor, Top-level knobs for the planner., Outcome of one full plan run., Schedule and execute a Workflow as a DAG. (+21 more)

### Community 19 - "Projects & Quick Actions"
Cohesion: 0.10
Nodes (27): react, QuickAction, Dialog(), DialogContent(), DialogContentProps, DialogContext, DialogContextValue, DialogDescription() (+19 more)

### Community 20 - "Docker Compose Stack"
Cohesion: 0.12
Nodes (32): Assessment, Base, Asset, Base, Finding, Base, get_vapt_orchestrator(), get_assessment() (+24 more)

### Community 21 - "VAPT Scan Pipeline"
Cohesion: 0.10
Nodes (19): CapabilityResolver, Capability Resolver.  Resolves a `Capability` request into a concrete execution, Validate inputs against the capability's input schema (lightweight).          Pe, Raised when capability resolution fails., A Capability fully resolved to executable Workflows., Resolves Capabilities to WorkflowRecords ready for the Task Planner., ResolutionError, ResolvedCapability (+11 more)

### Community 22 - "Knowledge Base Endpoints"
Cohesion: 0.14
Nodes (14): CancellationToken, Lightweight, async-friendly cancellation., NoopTaskExecutor, Task Executor — runs a Task.  A planner produces Tasks; the executor is what run, Run a single Task and emit a result., Default at Milestone 1.      The executor performs the bare minimum: a `result`-, TaskExecutor, TaskRunResult (+6 more)

### Community 23 - "Reports UI"
Cohesion: 0.10
Nodes (23): ASTRAIX VAPT Module  AI-Orchestrated Vulnerability Assessment & Penetration Test, Any, BaseModel, Enum, str, VAPT Data Models  Core data structures for VAPT operations., Request for a VAPT scan., Result from a VAPT scan. (+15 more)

### Community 24 - "ORM Models"
Cohesion: 0.13
Nodes (17): ApiKey, ApiKeyToggleRequest, BaseModel, ApiKey, AuditLog, Membership, Organization, Project (+9 more)

### Community 25 - "Asset Model & Repo"
Cohesion: 0.12
Nodes (25): ApiKeyCreate, ApiKeyCreateResponse, ApiKeyResponse, create_api_key(), login(), login_json(), MembershipResponse, OrganizationResponse (+17 more)

### Community 26 - "Researcher Agent"
Cohesion: 0.09
Nodes (20): get_tool_registry(), Enum, str, Kali Linux Security Tool Registry  Comprehensive registry of security tools avai, Tool categories matching VAPT workflow., Metadata about a security tool., Default configuration for a tool., Registry for managing security tools. (+12 more)

### Community 27 - "Verifier Agent"
Cohesion: 0.09
Nodes (30): FastAPI Backend, Neo4j Knowledge Graph, Next.js Frontend, Redis, FastAPI Dependency, Neo4j Driver Dependency, Pydantic v2 Dependency, redis Python Client Dependency (+22 more)

### Community 28 - "VAPT Orchestrator"
Cohesion: 0.09
Nodes (28): Finding, getSeverityBadge(), getTypeIcon(), getTypeLabel(), LiveScanConsole(), phaseIcons, PlanPhase, PlanTool (+20 more)

### Community 29 - "Pentest Graph Nodes"
Cohesion: 0.11
Nodes (26): analysis_step(), exploitation_step(), BaseModel, Uses an LLM with structured output to analyse scan results., Simulates a controlled exploitation attempt against confirmed findings. In a…, Compiles a human-readable penetration test report from the state., Structured result returned by the LLM when analysing scan findings., Simulates subfinder to discover subdomains. (+18 more)

### Community 30 - "Progress Bus (Redis)"
Cohesion: 0.07
Nodes (29): autoprefixer, eslint-config-next, devDependencies, autoprefixer, eslint-config-next, jsdom, postcss, prettier (+21 more)

### Community 31 - "Scan Routes"
Cohesion: 0.17
Nodes (28): RoleName, PyEnum, ApiKeyBase, ApiKeyCreate, ApiKeyCreateResponse, ApiKeyRead, MembershipBase, MembershipCreate (+20 more)

### Community 32 - "Planner Agent"
Cohesion: 0.11
Nodes (15): Finding, Parse Nmap text output as fallback., Map Nikto OSVDB ID to severity., Parse Nuclei JSON output to findings., Parse SQLMap JSON output to findings., Map tool-specific severity string to Severity enum., Parse Gobuster JSON output to findings., Parse FFUF JSON output to findings. (+7 more)

### Community 33 - "Docker Executor"
Cohesion: 0.10
Nodes (15): LyrieAIAgent, Lyrie AI Agent executor for autonomous security operations.      Features:     -, Run 7-phase autonomous pentest.          Args:             target: URL or local, Scan URL or file for security issues.          Checks:         - Security header, AI red-team an LLM endpoint.          Strategies:         - crescendo: gradual e, Calculate CVSS v3.1 score from vector.          Args:             vector: CVSS v, Verify agent identity using Agent Trust Protocol.          Args:             age, Display ATP compliance badge.          Returns:             dict with badge info (+7 more)

### Community 34 - "System Status UI"
Cohesion: 0.13
Nodes (21): _finding_to_security_finding(), generate_report(), GenerateReportRequest, list_reports(), list_templates(), AsyncSession, BaseModel, get (+13 more)

### Community 35 - "Sidebar & Layout"
Cohesion: 0.12
Nodes (16): get_planner(), AI Planner Agent Decides the VAPT plan: which tools to run, in which phase, and…, AIOrchestrator, Any, VAPTScanResult, VAPTScanType, VAPT AI Orchestrator AI-powered tool selection and scan coordination. Analyzes…, Detect when a running scan stops producing activity (stuck). If no event was… (+8 more)

### Community 36 - "Worklog & Session State"
Cohesion: 0.07
Nodes (27): axios, class-variance-authority, clsx, date-fns, dependencies, axios, class-variance-authority, clsx (+19 more)

### Community 37 - "Dashboard Stats"
Cohesion: 0.12
Nodes (9): PlannerAgent, Any, VAPTScanType, Ask the LLM (NVIDIA NIM, falling back to Ollama) to refine tool selection.…, Generate the full phased VAPT plan with KB-grounded reasoning., Knowledge-base-grounded plan generator for VAPT scans., get_knowledge_base(), KnowledgeBase (+1 more)

### Community 38 - "KB Source URLs"
Cohesion: 0.08
Nodes (27): Aif4thah Dojo-101, ElNiak awesome-ai-cybersecurity, GitHub Cybersecurity Topics, naveen-98 Cyber_Security_Reference, okhosting awesome-cyber-security, OWASP Projects (ADR Tier 3), paulveillard/cybersecurity (ADR Tier 1), santosomar AI-agents-for-cybersecurity (+19 more)

### Community 39 - "Neo4j Graph DB"
Cohesion: 0.11
Nodes (17): get_scanner_executor(), Any, Finding, ScanRequest, ScanResult, Execute a single tool., Create appropriate executor for scan request., Get tools for a scan request. (+9 more)

### Community 40 - "Report Engine"
Cohesion: 0.15
Nodes (16): ExternalTool, Any, ScanRequest, ScanResult, Execute a complete security scan., Enterprise VAPT Execution Engine      Features:     - Multi-platform support (Ka, Execute a single tool and return parsed findings., Execute multiple tools in parallel. (+8 more)

### Community 41 - "Community 41"
Cohesion: 0.15
Nodes (6): VAPTFinding, VAPTScanRequest, VAPTScanResult, VAPTSeverity, VAPTTool, VAPTExecutor

### Community 42 - "Community 42"
Cohesion: 0.15
Nodes (23): cancel_assessment(), create_assessment(), get_assessment(), list_assessments(), AsyncSession, delete, get, post (+15 more)

### Community 43 - "Community 43"
Cohesion: 0.14
Nodes (12): get_session(), AsyncSession, TimestampMixin, UUIDMixin, datetime, Nmap Plugin — normalizer.  Converts raw `nmap` output into canonical `SecurityFi, Nuclei Plugin — normalizer.  Converts raw `nuclei` output into canonical `Securi, Semgrep Plugin — normalizer.  Converts raw `semgrep` output into canonical `Secu (+4 more)

### Community 44 - "Community 44"
Cohesion: 0.10
Nodes (17): BasePlugin, FindingOut, PluginError, PluginOutput, PluginSchema, Parse stdin: str → dict., Structured logging accessible to orchestrator., Schema for plugin I/O, described in plugin.yml. (+9 more)

### Community 45 - "Community 45"
Cohesion: 0.11
Nodes (19): _map_error(), Convert platform errors → HTTP responses.  FastAPI exception handlers delegate t, Bind platform error handler., Shared mapping logic., register_exception_handlers(), _safe(), platform_error_to_http_response(), PlatformErrorResponse (+11 more)

### Community 46 - "Community 46"
Cohesion: 0.12
Nodes (18): Asset, AssessmentStatus, get_orchestrator(), Orchestrator, AsyncSession, Enum, str, UUID (+10 more)

### Community 47 - "Community 47"
Cohesion: 0.11
Nodes (23): AstraIX Security Analyst Platform, VAPT Capability, ASTRAIX AI Modules, ASTRAIX AI-Native Philosophy, The 9 ASTRAIX Domains, ASTRAIX Platform Name, ASTRAIX Brand Visual Identity, SecOS AI Modules (+15 more)

### Community 48 - "Community 48"
Cohesion: 0.17
Nodes (21): bulk_update_findings(), BulkUpdateRequest, delete_finding(), get_finding(), list_findings(), AsyncSession, BaseModel, delete (+13 more)

### Community 49 - "Community 49"
Cohesion: 0.09
Nodes (22): block_indicator(), check_threat_intel(), disable_account(), find_related_alerts(), get_alert_details(), get_alert_queue(), get_process_tree(), isolate_host() (+14 more)

### Community 50 - "Community 50"
Cohesion: 0.13
Nodes (13): AIRequest, AIResponse, AITokenUsage, AI Provider port.  A Provider is anything that can take a prompt + structured in, Tokens billed for one call. Independent of model types., A request is a structured, traceable call.      `prompt` is the raw text/materia, A provider's structured response., ParsedAIResponse (+5 more)

### Community 51 - "Community 51"
Cohesion: 0.09
Nodes (21): compilerOptions, allowJs, baseUrl, esModuleInterop, forceConsistentCasingInFileNames, incremental, isolatedModules, jsx (+13 more)

### Community 52 - "Community 52"
Cohesion: 0.13
Nodes (19): BaseSettings, get_settings(), Application settings loaded from env vars or .env., Settings, AIGatewaySettings, FindingEngineSettings, load_settings(), ObservabilitySettings (+11 more)

### Community 53 - "Community 53"
Cohesion: 0.13
Nodes (11): RecentAssessments(), StatCardProps, StatsCards(), resources, ResourceUsage, services, ServiceStatus, SystemStatus() (+3 more)

### Community 54 - "Community 54"
Cohesion: 0.17
Nodes (21): Finding Engine, web/discovery capability, network/recon capability, network/vuln-scan capability, api/security capability, web/vuln-scan capability, HTTP Probe (httpx) Plugin, Nmap Port Scanner Plugin (+13 more)

### Community 55 - "Community 55"
Cohesion: 0.18
Nodes (20): Docker Socket, KALI_IMAGE Env Var, VAPT_DEMO_MODE Env Var, VAPT_USE_DOCKER Env Var, gobuster, astraix-kali Image, nikto, nmap (+12 more)

### Community 56 - "Community 56"
Cohesion: 0.21
Nodes (18): create_asset(), delete_asset(), get_asset(), list_assets(), AsyncSession, delete, get, patch (+10 more)

### Community 57 - "Community 57"
Cohesion: 0.17
Nodes (12): create_organization(), invite_member(), MembershipCreate, OrganizationCreate, Register a new user and optionally create an organization., Create a new organization., Invite a user to organization or project., register() (+4 more)

### Community 58 - "Community 58"
Cohesion: 0.14
Nodes (8): CapabilityNotFoundError, Raised when a capability is not found in the registry., CapabilityVersion, Semantic version (major.minor.patch)., CapabilityRegistry, Capability Registry — typed lookup and lifecycle.  Thread-safe in-memory registr, Thread-safe registry of `Capability` instances keyed by id+version.      Capabil, Capability

### Community 59 - "Community 59"
Cohesion: 0.21
Nodes (16): _ai_comment_placeholder(), _build_section(), _findings_section(), NullReportEngine, Report Engine — implementation.  At Milestone 1, only the JSON/Markdown default, Render reports from findings + risk scores., JSON/Markdown default at Milestone 1.      Produces deterministic artefacts usin, ReportEngine (+8 more)

### Community 60 - "Community 60"
Cohesion: 0.18
Nodes (11): Assessment, Finding, PluginRegistry, Orchestrator, Build plugin invocation params from assessment., Persist plugins' findings., Generate fingerprint: title + asset + plugin + severity., Sequences assessment execution: plugins → findings. (+3 more)

### Community 61 - "Community 61"
Cohesion: 0.16
Nodes (10): AsyncSession, get_session(), Database session dependency., BaseRepository, Repository pattern for data access.  Each repository:   - Wraps SQLAlchemy queri, Generic repository for any model., List with pagination and optional filters., Count records with optional filters. (+2 more)

### Community 62 - "Community 62"
Cohesion: 0.17
Nodes (6): get_graph(), get, get_knowledge_graph(), KnowledgeGraph, _node_id(), _node_tooltip()

### Community 63 - "Community 63"
Cohesion: 0.15
Nodes (17): get_dashboard_activity(), get_dashboard_stats(), list_capabilities(), ping(), AsyncSession, get, post, UUID (+9 more)

### Community 64 - "Community 64"
Cohesion: 0.11
Nodes (19): AI Core Layer, AI Integration Architecture, Application Security Module, Cloud Security Module, Data Architecture (Hot/Warm/Cold), Data Security Module, Defensive Security Module, Deployment Options (+11 more)

### Community 65 - "Community 65"
Cohesion: 0.14
Nodes (18): AgentState, ai_triage_node(), AIVerdict, analyze_url_tool(), enrich_url_node(), BaseModel, TypedDict, Uses the AI model to decide if the URL is malicious or benign and provide an… (+10 more)

### Community 66 - "Community 66"
Cohesion: 0.17
Nodes (14): emit_plugin_completed(), emit_plugin_finding(), emit_plugin_progress(), emit_plugin_started(), PluginCompletedPayload, PluginFindingPayload, PluginProgressPayload, PluginStartedPayload (+6 more)

### Community 67 - "Community 67"
Cohesion: 0.12
Nodes (18): PostgreSQL, Quick Scan API Endpoint, VAPT Routes (routes.py), VAPT Scan Route Handler (route.ts), Alembic Migrations Dependency, asyncpg Dependency, SQLAlchemy 2.0 Dependency, VAPT API (+10 more)

### Community 68 - "Community 68"
Cohesion: 0.18
Nodes (8): ProviderAlreadyRegisteredError, ProviderManager, ProviderNotFoundError, Provider Manager.  The Manager owns the lifecycle of providers. Applications nev, Thread-safe registry of providers.      The Manager is the *only* place provider, AIProvider, Concrete providers (OpenAI/Anthropic/...) implement this., AIError

### Community 69 - "Community 69"
Cohesion: 0.14
Nodes (12): AITokenUsage, NoopTokenManager, _PlanningError, Token Manager — budgets, accounting, retries, compression.  At Milestone 1 we sh, Hard limits for a call. `None` = no limit on that field., Pre-call planning + post-call accounting., Estimate prompt tokens; raise `PlanningError` if over budget., Persist a usage line for accounting. (+4 more)

### Community 70 - "Community 70"
Cohesion: 0.18
Nodes (13): Base, TimestampMixin, UUIDMixin, DeclarativeBase, Mapped, BaseModel, FindingOut, PluginError (+5 more)

### Community 71 - "Community 71"
Cohesion: 0.24
Nodes (3): ProjectRepository, UUID, Project

### Community 72 - "Community 72"
Cohesion: 0.15
Nodes (15): Formatter, bind_correlation_id(), configure_logging(), _console_formatter(), _CorrelationIdFilter, get_logger(), _json_formatter(), Correlation-aware structured logging.  Default backend is `logging` to avoid har (+7 more)

### Community 73 - "Community 73"
Cohesion: 0.13
Nodes (16): AI Gateway, Gemini AI, OpenAI SDK Dependency, Gemini AI Summaries, CSKB Alternatives Considered, cs kb CLI, CSKB Platform Principles Compliance, ContextBuilder Integration (+8 more)

### Community 74 - "Community 74"
Cohesion: 0.18
Nodes (16): Cybersecurity Knowledge Base, Planner Agent, ReconOrchestrator, Researcher Agent, Verifier Agent, faiss-cpu Dependency, fastembed Dependency, LLM Provider Config (+8 more)

### Community 75 - "Community 75"
Cohesion: 0.17
Nodes (8): _InMemoryPromptManager, PromptTemplate, PromptVersionError, Prompt Manager — versioned prompt templates.  A `PromptTemplate` is a parameteri, Raised when a requested `prompt_id` / version combination is unknown., One version of one prompt.      The text uses stdlib `Template` semantics ($-sty, Process-local default; replace with persistence later if needed., Exception

### Community 76 - "Community 76"
Cohesion: 0.12
Nodes (12): float, CapabilityVersion, ComplianceTag, Confidence, Reusable value objects (the platform's vocabulary).  These are the typed shapes, A compliance framework mapping., Validated confidence score: 0.0–1.0., SemVer-style version (integer triple). (+4 more)

### Community 77 - "Community 77"
Cohesion: 0.13
Nodes (3): GROUP_STYLES, SEVERITY_COLORS, ApiClient

### Community 78 - "Community 78"
Cohesion: 0.17
Nodes (14): AgentState, analyze_exploitation_node(), ExploitationInsights, get_kev_vulnerabilities_node(), BaseModel, TypedDict, Uses an AI model to analyze exploitation vectors and associated CWEs., A terminal node that prints the final, combined report. (+6 more)

### Community 79 - "Community 79"
Cohesion: 0.18
Nodes (13): get_kb_source(), knowledge_stats(), list_kb_sources(), get, post, Search the cybersecurity knowledge base., Get knowledge base statistics., Rebuild FAISS vector index from chunks.json. (+5 more)

### Community 80 - "Community 80"
Cohesion: 0.18
Nodes (14): AI Gateway Module, AI-SecOS Core, Infrastructure Module, Domain Models Module, Normalizer Module, Platform Bootstrap Module, Plugin System Module, Report Engine Module (+6 more)

### Community 81 - "Community 81"
Cohesion: 0.22
Nodes (13): Headers, _add(), _detect_cdn(), _detect_technologies(), _extract_title(), main(), probe_target(), Extract version from header like 'nginx/1.21.6'. (+5 more)

### Community 82 - "Community 82"
Cohesion: 0.15
Nodes (11): create_threat_hunting_report(), develop_hunting_strategy(), gather_threat_context(), perform_technical_analysis(), process_indicator_and_run_parallel(), Performs technical analysis on the indicator. Args: indicator_info (str): The…, Gathers threat context information for the indicator. Args: indicator_info…, Develops a hunting strategy for the indicator. Args: indicator_info (str): The… (+3 more)

### Community 83 - "Community 83"
Cohesion: 0.18
Nodes (8): AssessmentId, FindingNormalizer, NormalizationError, Normalizer interface + registry.  The Normalizer is how raw plugin output become, Turns a plugin-specific raw output into a `SecurityFinding`.      A single input, Yield canonical findings from a raw plugin output.          Implementations MUST, HttpxPluginId, Bundle the httpx plugin id constant.

### Community 84 - "Community 84"
Cohesion: 0.27
Nodes (6): Any, VAPTFinding, VAPTScanRequest, VAPTScanResult, Attach a callback for live progress events (scan_id, event_type, data)., ReconOrchestrator

### Community 85 - "Community 85"
Cohesion: 0.23
Nodes (12): Element, build_nmap_command(), main(), _parse_host(), parse_nmap_xml(), _parse_port(), Parse a single host element., Parse a port element. (+4 more)

### Community 86 - "Community 86"
Cohesion: 0.17
Nodes (11): create_threat_hunting_report(), develop_hunting_strategy(), gather_threat_context(), perform_technical_analysis(), process_indicator_and_run_parallel(), Performs technical analysis on the indicator. Args: indicator_info (str): The…, Gathers threat context information for the indicator. Args: indicator_info…, Develops a hunting strategy for the indicator. Args: indicator_info (str): The… (+3 more)

### Community 87 - "Community 87"
Cohesion: 0.22
Nodes (12): example_direct_mcp_usage(), example_infrastructure_mapping(), example_langgraph_integration(), example_security_monitoring(), example_threat_intelligence(), main(), Example of using Shodan MCP server for threat intelligence gathering., Example of mapping an organization's infrastructure using Shodan. (+4 more)

### Community 88 - "Community 88"
Cohesion: 0.26
Nodes (12): demo_dns_intelligence(), demo_infrastructure_reconnaissance(), demo_iot_security_analysis(), demo_vulnerability_assessment(), main(), Demo the IoT security analysis scenario., Demo the DNS intelligence gathering scenario., Simulate running an agent scenario. (+4 more)

### Community 89 - "Community 89"
Cohesion: 0.22
Nodes (12): example_direct_mcp_usage(), example_infrastructure_mapping(), example_langgraph_integration(), example_security_monitoring(), example_threat_intelligence(), main(), Example of using Shodan MCP server for threat intelligence gathering., Example of mapping an organization's infrastructure using Shodan. (+4 more)

### Community 90 - "Community 90"
Cohesion: 0.19
Nodes (10): Result, fail(), Failure, is_failure(), is_ok(), ok(), Result type (Rust/Python-port idiom) for explicit success/failure.  Used by serv, Successful outcome carrying a value. (+2 more)

### Community 91 - "Community 91"
Cohesion: 0.17
Nodes (12): Finding Normalizer (normalizer.py), Kali Tools Dockerfile, Risk Scoring Engine, Custom Kali Image (astraix-kali), Docker Compose Stack, Keep a Changelog Format, Normalized Findings, Plugin Architecture (+4 more)

### Community 92 - "Community 92"
Cohesion: 0.30
Nodes (4): Any, List scans that are still running (non-terminal status)., Publishes and reads scan progress events (Redis-backed, in-memory fallback)., ScanProgressBus

### Community 93 - "Community 93"
Cohesion: 0.21
Nodes (6): DefaultFindingFingerprinter, FindingFingerprinter, Deterministic fingerprinting contract.  Two findings with identical `(asset, cwe, Computes fingerprints for findings., Default deterministic fingerprinter.      The hash is built from fields that uni, Stable byte representation (sorted keys, list-of-tuples).

### Community 94 - "Community 94"
Cohesion: 0.18
Nodes (10): decide_next_step(), IncidentState, initial_analysis(), malware_analysis(), phishing_analysis(), TypedDict, Perform initial analysis of the alert. Args: state (dict): The current state of…, Perform detailed phishing analysis. Extract malicious URL from phishing email… (+2 more)

### Community 95 - "Community 95"
Cohesion: 0.22
Nodes (10): AgentState, call_model(), nmap_scan(), TypedDict, The primary agent node. It calls the AI model to decide the next action., Runs a real Nmap scan on a target IP or domain using python-nmap., Simulates searching Exploit-DB for a given query (e.g., a software name)., Conditional logic to decide whether to continue or end the workflow. (+2 more)

### Community 96 - "Community 96"
Cohesion: 0.20
Nodes (10): PluginCapabilityRequirement, PluginInputSchema, PluginOutputSchema, PluginResourceLimits, PluginSandboxPolicy, Plugin manifest (the typed shape of a `plugin.yml`).  Schema is intentionally st, A Capability the Plugin requires from the platform., Hard limits applied by the Sandbox. (+2 more)

### Community 97 - "Community 97"
Cohesion: 0.31
Nodes (3): _load_kb(), VAPTFinding, ResearcherAgent

### Community 98 - "Community 98"
Cohesion: 0.29
Nodes (6): get_vapt_executor(), get_tool(), get_tools_for_scan_type(), VAPTScanType, VAPTTool, VAPT Tools Registry Direct integration with host-installed security tools. Fast…

### Community 99 - "Community 99"
Cohesion: 0.33
Nodes (5): VAPTFinding, VAPTSeverity, Best-effort lookup of exploitation/technique guidance in the knowledge base for…, Verify findings concurrently (bounded) so long-running re-exploits (e.g.…, VerifierAgent

### Community 100 - "Community 100"
Cohesion: 0.20
Nodes (10): scripts, build, dev, format, lint, start, test, test:coverage (+2 more)

### Community 101 - "Community 101"
Cohesion: 0.27
Nodes (9): agent_node(), AgentState, decide_next(), TypedDict, State for the agent graph., Use the LLM to decide the next step or provide an answer., Search the vector store for relevant documents., Decide whether to search again or finish. (+1 more)

### Community 102 - "Community 102"
Cohesion: 0.44
Nodes (9): download_file(), run_gau(), run_httpx_tech_detection(), run_nuclei(), run_subfinder(), run_tool(), run_waybackurls(), serve_openapi() (+1 more)

### Community 103 - "Community 103"
Cohesion: 0.24
Nodes (5): NmapScanner, Run as process: stdin → scan → stdout, Run nmap, parse output, return findings., Parse Nmap XML/text → findings., PluginOutput

### Community 104 - "Community 104"
Cohesion: 0.22
Nodes (6): PluginValidationError, Plugin Validator: schema, capability, and permission checks.  The Validator is t, Tiny subset of JSON Schema type matching for type-checking most params., _type_match(), ValidationResult, PluginError

### Community 106 - "Community 106"
Cohesion: 0.28
Nodes (6): BaseSchema, PaginatedResponse, Base schema with ORM mode enabled., Standard success response wrapper., Paginated results wrapper., ResponseSchema

### Community 107 - "Community 107"
Cohesion: 0.22
Nodes (7): event_loop(), Pytest configuration and fixtures., mock_registry(), mock_settings(), Override default event loop., Mock settings for tests., Mock plugin registry.

### Community 108 - "Community 108"
Cohesion: 0.25
Nodes (9): System Architecture, Applications Layer, Plugin Executor, Plugin Manager, Plugin Sandbox, Plugin Validator, Plugins Layer, SecurityPlugin PDK (+1 more)

### Community 109 - "Community 109"
Cohesion: 0.25
Nodes (6): _noop_dedup(), Milestone 2 End-to-End Demo — Capability -> Workflow -> Plugin -> Findings.  Dem, Minimal in-memory deduplicator for M2 demo only., M2 End-to-End test.  Validates the vertical slice: Capability → Plugin → Normali, The full M2 path executes end-to-end and emits a summary., test_m2_demo_runs()

### Community 110 - "Community 110"
Cohesion: 0.25
Nodes (4): Check if a specific tool is available., Check if Docker is available., Get availability status of all tools., Get overall health status of the scanner.

### Community 111 - "Community 111"
Cohesion: 0.25
Nodes (8): Network Vulnerability Assessment, External Asset Discovery, Web Discovery, Web Application Security Assessment, HTTPX Scanner Plugin, Nmap Scanner Plugin, Nuclei Scanner Plugin, Subfinder Scanner Plugin

### Community 112 - "Community 112"
Cohesion: 0.25
Nodes (8): Coding Standards, Python Standards, TypeScript Standards, MVP Scope Definition, Build Later Items, Build Now Items, Never Build Items, Master AI Engineer Rules

### Community 113 - "Community 113"
Cohesion: 0.25
Nodes (6): create_pentest_plan(), perform_reconnaissance(), plan_exploitation(), This function generates a prompt for reconnaissance techniques and tools based…, This function generates a prompt for exploitation methods and tools based on…, This function combines the reconnaissance and exploitation phases into a…

### Community 114 - "Community 114"
Cohesion: 0.36
Nodes (7): build_nuclei_command(), main(), parse_nuclei_json(), Execute nuclei and return parsed results., Build nuclei command arguments., Parse nuclei JSON output lines., run_nuclei_scan()

### Community 115 - "Community 115"
Cohesion: 0.36
Nodes (7): build_semgrep_command(), main(), parse_semgrep_results(), Build semgrep command arguments., Parse semgrep JSON output., Execute semgrep and return parsed results., run_semgrep_scan()

### Community 116 - "Community 116"
Cohesion: 0.36
Nodes (7): build_subfinder_command(), main(), parse_subfinder_json(), Build subfinder command arguments., Parse subfinder JSON output lines., Execute subfinder and return parsed results., run_subfinder()

### Community 117 - "Community 117"
Cohesion: 0.36
Nodes (7): build_trivy_command(), main(), parse_trivy_results(), Build trivy command arguments., Parse trivy JSON output., Execute trivy and return parsed results., run_trivy_scan()

### Community 118 - "Community 118"
Cohesion: 0.29
Nodes (7): Auth API (auth.py), Demo Credentials, passlib/bcrypt Dependency, python-jose Dependency, JWT Auth System, Release 0.0.1 Initial MVP, API Reference

### Community 119 - "Community 119"
Cohesion: 0.29
Nodes (4): Model Router — decides `(provider_id, model)` per request.  At Milestone 1 we sh, Deterministic choice for tests / deterministic callers., RoutingDecision, select_first_providers()

### Community 120 - "Community 120"
Cohesion: 0.48
Nodes (7): Report Base Template (base.html), Severity Badge Styles, Compliance Report Template, Executive Report Template, Technical Report Template, Jinja2 Dependency, WeasyPrint Dependency

### Community 121 - "Community 121"
Cohesion: 0.48
Nodes (7): Dark-Moon Platform, Lyrie AI Platform, Offensive Security Module, PentAGI Platform, RedAmon Platform, Xalgorix Platform, Integrated VAPT Platforms (Branding)

### Community 122 - "Community 122"
Cohesion: 0.29
Nodes (7): Capability Abstraction, Workflow Abstraction, AstraIX Platform Constitution, AI-SecOS Core Runtime, Plugin System, Risk Engine, Security Analyst Application

### Community 123 - "Community 123"
Cohesion: 0.29
Nodes (6): create_pentest_plan(), perform_reconnaissance(), plan_exploitation(), This function generates a prompt for reconnaissance techniques and tools based…, This function generates a prompt for exploitation methods and tools based on…, This function combines the reconnaissance and exploitation phases into a…

### Community 124 - "Community 124"
Cohesion: 0.29
Nodes (6): get_current_time(), BaseModel, Returns the current time in H:MM AM/PM format., Scans the specified IP address or range using nmap., scanner(), ScannerInput

### Community 125 - "Community 125"
Cohesion: 0.29
Nodes (6): _categorize_semgrep(), _extract_tags(), _normalize_one(), Categorize semgrep finding based on check_id and metadata., Extract tags from semgrep metadata., Normalize a single semgrep finding.

### Community 126 - "Community 126"
Cohesion: 0.43
Nodes (4): BaseSchema, ErrorResponse, PaginatedResponse, ResponseSchema

### Community 127 - "Community 127"
Cohesion: 0.40
Nodes (4): FindingContextPayload, What the AI sees. Pre-serialization.      The AI Gateway *never* receives the ra, Numeric, bounded 0–100 risk.      Use `.factors` to display *why* the score is w, RiskScore

### Community 128 - "Community 128"
Cohesion: 0.40
Nodes (4): do_run_migrations(), run_async_migrations(), run_migrations_online(), Connection

### Community 129 - "Community 129"
Cohesion: 0.40
Nodes (5): CorrelationId, get_correlation_id(), Correlation id context.  Every critical action (workflow, plugin exec, AI call), Return the current correlation id, creating one if absent.      Use only at entr, set_correlation_id()

### Community 130 - "Community 130"
Cohesion: 0.33
Nodes (6): Project Roadmap, Milestone 1 - AI-SecOS Core, Milestone 2 - First Plugin httpx, Milestone 3 - Discovery Capability, Milestone 4 - Web Security Assessment, Milestone 5 - Security Analyst UI

### Community 131 - "Community 131"
Cohesion: 0.47
Nodes (6): AstraIX App Icon, White Check Mark, Slate and Cyan Palette, Rounded Square Background, Security Branding Motif, Cyan Shield Glyph

### Community 132 - "Community 132"
Cohesion: 0.40
Nodes (3): navigation, settingsNav, Sidebar()

### Community 133 - "Community 133"
Cohesion: 0.53
Nodes (4): chunk_text(), collect_files(), extract_title(), main()

### Community 135 - "Community 135"
Cohesion: 0.40
Nodes (5): get_cisa_kev_catalog(), Runs an nmap scan on the specified hosts with the given arguments. :param…, Fetches the latest CISA Known Exploited Vulnerabilities (KEV) catalog. :return:…, run_nmap_scan(), tool

### Community 136 - "Community 136"
Cohesion: 0.40
Nodes (5): Technology Stack, AI Tech Stack, Backend Tech Stack, DevOps Tech Stack, Frontend Tech Stack

### Community 138 - "Community 138"
Cohesion: 0.40
Nodes (4): get_current_time(), Returns the current time in H:MM AM/PM format., Searches Wikipedia for information on the given query., search_wikipedia()

### Community 139 - "Community 139"
Cohesion: 0.40
Nodes (4): main(), Alternative function to run a custom scenario with user input. This…, Main function to run the ethical hacking agent., run_custom_scenario()

### Community 145 - "Community 145"
Cohesion: 0.50
Nodes (3): name, private, version

### Community 148 - "Community 148"
Cohesion: 0.50
Nodes (4): Trivy Security Scanner Plugin, cloud/posture capability, container/security capability, iac/security capability

## Knowledge Gaps
- **265 isolated node(s):** `severityConfig`, `statusOptions`, `roleConfig`, `inter`, `metadata` (+260 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **62 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SecurityFinding` connect `Finding Correlator` to `AI-SecOS Core API`, `AI Gateway Context`, `Community 70`, `Community 76`, `Risk Engine`, `Finding Fingerprint`, `Community 83`, `Community 125`, `Community 59`, `Community 93`, `Community 127`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `BaseModel` connect `Community 70` to `Community 96`, `AI-SecOS Core API`, `Metrics Registry`, `Finding Correlator`, `Community 106`, `Community 44`, `Community 76`, `Task Cancellation`, `VAPT Scan Pipeline`, `Community 126`, `Scan Routes`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `build_default_container()` connect `AI Gateway Context` to `Metrics Registry`, `AI-SecOS Core API`, `Community 68`, `Finding Correlator`, `KB Ingest & Embedding`, `Community 72`, `Risk Engine`, `Community 52`, `VAPT Scan Pipeline`, `Knowledge Base Endpoints`, `Community 59`, `Community 93`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Are the 34 inferred relationships involving `SecurityFinding` (e.g. with `ContextBuilder` and `FindingContextPayload`) actually correct?**
  _`SecurityFinding` has 34 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `MembershipRepository` (e.g. with `ApiKeyCreate` and `ApiKeyCreateResponse`) actually correct?**
  _`MembershipRepository` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `ProjectRepository` (e.g. with `ApiKeyCreate` and `ApiKeyCreateResponse`) actually correct?**
  _`ProjectRepository` has 24 INFERRED edges - model-reasoned connections that need verification._
- **What connects `severityConfig`, `statusOptions`, `roleConfig` to the rest of the system?**
  _265 weakly-connected nodes found - possible documentation gaps or missing edges._