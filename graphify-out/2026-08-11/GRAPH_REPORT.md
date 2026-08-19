# Graph Report - .  (2026-08-07)

## Corpus Check
- 44 files · ~158,140 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3314 nodes · 6140 edges · 304 communities (206 shown, 98 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 1017 edges (avg confidence: 0.57)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Finding Engine
- Finding Engine
- Plugin System
- Scanner Executor
- VAPT Orchestrator
- Plugins API
- Organizations & API Keys
- Plugin System
- Knowledge Base Sources
- Auth & API Keys
- App Configuration
- Scanner Execution
- Risk Engine
- Auth & API Keys
- Capability Loader
- Risk Engine
- Organizations API
- Auth & API Keys
- DarkMoon Adapter
- Knowledge Base Sources
- VAPT Models
- Adapter Base Types
- Scanner Tool Registry
- Kali Tool Adapter
- Report Engine
- Scans UI
- Knowledge Base Sources
- RAG Pipeline
- Auth & API Keys
- Recon Orchestrator
- Scanner Execution
- VAPT Adapters
- Auth & API Keys
- Auth & API Keys
- Assessments API
- Auth & API Keys
- VAPT DTOs
- External Adapter Registry
- Scan Orchestration
- Findings API
- Sample VAPT Reports
- VAPT Adapters
- Plugin System
- CWE Vulnerability Mapping
- Plugin System
- Dashboard UI
- Scan Orchestration
- Plugin System
- Plugin System
- Dashboard UI
- Knowledge Base Sources
- Domain Assessment Types
- Plugin System
- Plugin System
- Plugin System
- Plugin System
- Database Layer
- Auth & API Keys
- Xalgorix Adapter
- Database Layer
- Dashboard UI
- Projects API
- Knowledge Base Sources
- AI Gateway Interface
- Prompt Management
- AI Gateway
- Scan Orchestration
- Auth & API Keys
- Report Generation
- Planner Agent
- Risk Engine
- AI Gateway
- Plugin System
- Progress Bus
- Plugin System
- RAG Pipeline
- Planner Agent
- Graph Page
- Knowledge Base Sources
- Plugin System
- Planner Agent
- Misc Utilities
- Finding Engine
- HTTPx Tooling
- Knowledge Base Sources
- Plugin System
- Auth Login
- Knowledge API
- Scan Orchestration
- VAPT Adapters
- Verifier Agent
- Nmap Tooling
- AI Gateway
- Auth & API Keys
- Knowledge Base Sources
- Knowledge Base Sources
- Knowledge Base Sources
- Knowledge Base Sources
- Misc Utilities
- Plugin System
- AI Gateway
- Model Routing
- Scan Orchestration
- Plugin System
- Product Docs
- HTTPx Tooling
- Knowledge Base Sources
- Knowledge Base Sources
- Plugin System
- AI Provider Abstraction
- README Docs
- RAG Pipeline
- Knowledge Base Sources
- Knowledge Base Sources
- Knowledge Base Sources
- Nmap Tooling
- Scanner Execution
- Misc Utilities
- Researcher Agent
- Scan Orchestration
- Plugin System
- Nmap Tooling
- Trivy Tooling
- AI Gateway
- AI SecOS Core
- Plugin System
- VAPT Adapters
- Product Docs
- README Docs
- Engineering Docs
- Engineering Docs
- Knowledge Base Sources
- Nuclei Tooling
- Semgrep Tooling
- Subfinder Tooling
- Trivy Tooling
- ZenAI HTTP Adapter
- Database Layer
- Plugin System
- Plugin System
- Knowledge Base Sources
- Knowledge Base Sources
- Misc Utilities
- Database Layer
- Sample Web App Findings
- Engineering Docs
- Branding Icons
- KB Ingestion
- Fast KB Ingestion
- Knowledge Base Sources
- Knowledge Base Sources
- Container Runtime
- Product Docs
- Engineering Docs
- Infrastructure
- Knowledge Base Sources
- Knowledge Base Sources
- Knowledge Base Sources
- App Configuration
- Misc Utilities
- Misc Utilities
- Frontend Package
- Misc Utilities
- Incident Chain Examples
- Plugin System
- Kaggle Download Script
- Finding Engine
- ESLint Config
- FAISS Index Builder
- KB Embedding Manifest
- Knowledge Base Sources
- Knowledge Base Sources
- Graphify Plugin
- Plugin System
- AI Gateway
- Misc Utilities
- App Configuration
- Backend Dependencies
- Plugin System
- Plugin System
- Plugin System
- Auth & API Keys
- App Configuration
- Infrastructure
- Frontend Package
- Finding Engine
- App Configuration
- Misc Utilities
- Frontend Package
- Frontend Package
- Frontend Package
- Frontend Package
- Frontend Package
- Frontend Package
- Frontend Package
- Infrastructure
- Knowledge Base Sources
- Knowledge Base Sources
- Knowledge Base Sources
- Plugin System
- Report Engine
- Risk Engine
- Runtime Engine
- Misc Utilities
- Engineering Docs
- Active Scan Store
- Dashboard Activity
- Project Persistence
- Graphify Hook
- Auth & API Keys
- Assessments API
- Misc Utilities
- Misc Utilities
- Organizations API
- Organizations API
- Organizations API
- Auth & API Keys
- Auth & API Keys
- Report Engine
- Organizations API
- Organizations API
- Scan Orchestration
- VAPT Core
- Database Layer
- Backend Dependencies
- Backend Dependencies
- Backend Dependencies
- Backend Dependencies
- Backend Dependencies
- Backend Dependencies
- Backend Dependencies
- Backend Dependencies
- Backend Dependencies
- Backend Dependencies
- Misc Utilities
- Misc Utilities
- CWE References
- Product Docs
- Engineering Docs
- Findings API
- AI Agents
- MCP Servers
- Misc Utilities
- Plugin System
- Projects API
- Misc Utilities
- README Docs
- App Configuration
- README Docs
- README Docs
- Misc Utilities
- Database Layer
- Misc Utilities
- Database Layer
- Neo4j Knowledge Graph
- Redis Progress Bus

## God Nodes (most connected - your core abstractions)
1. `SecurityFinding` - 75 edges
2. `MembershipRepository` - 48 edges
3. `Container` - 47 edges
4. `ProjectRepository` - 46 edges
5. `_MutableContainer` - 44 edges
6. `ApiKeyRepository` - 43 edges
7. `BaseModel` - 42 edges
8. `OrganizationRepository` - 42 edges
9. `UserRepository` - 36 edges
10. `build_default_container()` - 34 edges

## Surprising Connections (you probably didn't know these)
- `SQL Injection` --semantically_similar_to--> `SQL Injection in Search Endpoint (CS-2026-002)`  [INFERRED] [semantically similar]
  training-data/vulnerable-programming-dataset/dataset.json → backend/app/report_engine/samples/cybersecify-soc2-iso27001-sample.html
- `Cross-Site Scripting (XSS)` --semantically_similar_to--> `Stored Cross-Site Scripting (4 Instances)`  [INFERRED] [semantically similar]
  training-data/vulnerable-programming-dataset/dataset.json → backend/app/report_engine/samples/purplesec-webapp-sample.pdf
- `AI Integration Architecture` --semantically_similar_to--> `AI Gateway (Gemini)`  [INFERRED] [semantically similar]
  docs/ARCHITECTURE_OVERVIEW.md → AGENTS.md
- `CSKB Sibling Docker Image` --semantically_similar_to--> `Cybersecurity Knowledge Base (TF-IDF)`  [INFERRED] [semantically similar]
  engineering/adr/001-cskb.md → AGENTS.md
- `OWASP Projects (ADR Tier 3)` --semantically_similar_to--> `OWASP Projects`  [INFERRED] [semantically similar]
  engineering/adr/001-cskb.md → SOURCES.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **AstraIX Multi-Agent VAPT Pipeline** — agents_reconorchestrator, agents_researcher_agent, agents_verifier_agent, agents_risk_engine, agents_ai_gateway [EXTRACTED 1.00]
- **External VAPT Platform Adapters** — adapter_raccoon, adapter_lyrie, adapter_xalgorix, adapter_darkmoon, adapter_pentagi, adapter_redamon, adapter_zenai [EXTRACTED 1.00]
- **Report Engine Jinja Template Hierarchy** — backend_app_report_engine_templates_base, backend_app_report_engine_templates_compliance, backend_app_report_engine_templates_technical [EXTRACTED 1.00]
- **Report Template Set (Jinja extends)** — backend_app_report_engine_templates_executive_report [EXTRACTED 1.00]
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

## Communities (304 total, 98 thin omitted)

### Community 0 - "Finding Engine"
Cohesion: 0.05
Nodes (68): assess(), AssessRequest, AssessResponse, _bootstrap(), FindingSummary, list_capabilities(), FastAPI app for the AI-SecOS Core Web UI.  Run with: uvicorn api:app --reload --, Convert 'https://example.com:443' to 'asset_example_com'. (+60 more)

### Community 1 - "Finding Engine"
Cohesion: 0.05
Nodes (49): Container, At boot, walk the plugins root and populate:           - plugin registry, The exposed container interface., FindingCorrelator, NoopFindingCorrelator, Finding Correlator — the contract + the no-op default.  Correlators detect patte, Adds correlation metadata to findings., Return the same set of findings, possibly tagged with correlation. (+41 more)

### Community 2 - "Plugin System"
Cohesion: 0.06
Nodes (49): CorrelationId, Counter, Histogram, MetricsRegistry, _NoopCounter, _NoopHistogram, Metrics primitives (stubs at Milestone 1).  These are typed protocols so service, Monotonically increasing value, optionally labelled. (+41 more)

### Community 3 - "Scanner Executor"
Cohesion: 0.09
Nodes (44): Scanner Executor Service  Enterprise-grade scanner execution with: - Async tool, Execute a single tool., Check which tools are available in the environment., ToolAvailabilityChecker, AstraIX Security Scanner Module  Enterprise-grade security scanning engine that, Finding, BaseModel, Enum (+36 more)

### Community 4 - "VAPT Orchestrator"
Cohesion: 0.06
Nodes (40): AIOrchestrator, get_vapt_orchestrator(), Any, VAPTScanType, VAPT AI Orchestrator AI-powered tool selection and scan coordination. Analyzes…, Run all enabled external adapters in parallel against the target. Adapters run…, Detect when a running scan stops producing activity (stuck). If no event was…, Analyze target to understand what it is. (+32 more)

### Community 5 - "Plugins API"
Cohesion: 0.07
Nodes (39): _count_by_capability(), _count_by_type(), disable_plugin(), enable_plugin(), get_plugin(), list_plugins(), plugins_info(), Any (+31 more)

### Community 6 - "Organizations & API Keys"
Cohesion: 0.08
Nodes (47): ApiKeyCreate, ApiKeyToggleRequest, create_api_key(), create_organization(), create_project(), delete_api_key(), delete_organization(), delete_project() (+39 more)

### Community 7 - "Plugin System"
Cohesion: 0.07
Nodes (37): ProjectDetailPage(), registrableDomain(), formats, templates, apiKeysApi, assessmentsApi, assetsApi, authApi (+29 more)

### Community 8 - "Knowledge Base Sources"
Cohesion: 0.07
Nodes (30): after_kickoff, agent, BaseTool, before_kickoff, crew, CrewBase, VulnerabilityManagement crew for comprehensive vulnerability assessment and…, Creates the VulnerabilityManagement crew with sequential process for systematic… (+22 more)

### Community 9 - "Auth & API Keys"
Cohesion: 0.11
Nodes (21): Any, CancellationToken, CancelledError, Cancellation token for running tasks/plans.  The platform-wide cancellation cont, A typed alias for cancellation that originates from the platform., Lightweight, async-friendly cancellation., NoopTaskExecutor, Task Executor — runs a Task.  A planner produces Tasks; the executor is what run (+13 more)

### Community 10 - "App Configuration"
Cohesion: 0.07
Nodes (37): get_settings(), Application settings. Loaded from `.env` or process-level env vars., Settings, BaseSettings, get_settings(), Application settings loaded from env vars or .env., Settings, AIGatewaySettings (+29 more)

### Community 11 - "Scanner Execution"
Cohesion: 0.08
Nodes (31): AssessmentStatus, get_orchestrator(), Orchestrator, Enum, str, Orchestrator Service  Coordinates plugins, assessments, and findings.  Responsib, Run real VAPT scan using Kali Linux tools.         This is the enterprise-grade, Singleton orchestrator. (+23 more)

### Community 12 - "Risk Engine"
Cohesion: 0.07
Nodes (28): Enum, PluginType, Report Engine — typed shapes only at Milestone 1.  The Engine produces a `Report, Supported output formats., ReportFormat, Typed outputs of the Risk Engine.  A `RiskScore` is a 0–100 value clipped and bo, Where a risk axis got its number., RiskFactorSource (+20 more)

### Community 13 - "Auth & API Keys"
Cohesion: 0.10
Nodes (39): create_project(), delete_organization(), delete_project(), get_api_key_repo(), get_membership_repo(), get_org_repo(), get_organization(), get_project() (+31 more)

### Community 14 - "Capability Loader"
Cohesion: 0.11
Nodes (32): CapabilityLoader, CapabilityLoaderError, LoadedCapability, _parse_asset_category(), _parse_framework(), _parse_manifest(), YAML-based capability loader.  Loads capability manifests from filesystem into t, Parse a YAML mapping into a `CapabilityManifest`. (+24 more)

### Community 15 - "Risk Engine"
Cohesion: 0.08
Nodes (23): build_default_risk_engine(), DefaultRiskEngine, _noop_severity_to_score(), NoopRiskEngine, Risk Engine — pipeline orchestrator and entry points.  Two implementations are s, Identity: score derived directly from canonical severity.      Used in tests and, Convenience factory used by the DI container at M1.      Real DI wires `RiskEngi, A scored finding (or a typed wrapper around a SecurityFinding). (+15 more)

### Community 16 - "Organizations API"
Cohesion: 0.11
Nodes (27): severityConfig, statusOptions, membershipsApi, cn(), roleConfig, Badge(), BadgeProps, Button (+19 more)

### Community 17 - "Auth & API Keys"
Cohesion: 0.10
Nodes (24): ApiKeyCreate, ApiKeyCreateResponse, ApiKeyResponse, create_api_key(), create_organization(), invite_member(), MembershipCreate, MembershipResponse (+16 more)

### Community 18 - "DarkMoon Adapter"
Cohesion: 0.13
Nodes (12): AdapterScanResult, Result of an adapter-run scan phase., DarkMoonAdapter, _HttpAdapter, PentagiAdapter, Any, VAPTScanType, PentAGI - fully autonomous pentesting agent (Go backend, REST API). (+4 more)

### Community 19 - "Knowledge Base Sources"
Cohesion: 0.11
Nodes (29): AsyncClient, FastMCP, create_mcp_server(), create_route_maps(), create_shodan_client(), get_api_key(), load_openapi_spec(), main() (+21 more)

### Community 20 - "VAPT Models"
Cohesion: 0.10
Nodes (23): ASTRAIX VAPT Module  AI-Orchestrated Vulnerability Assessment & Penetration Test, Any, BaseModel, Enum, str, VAPT Data Models  Core data structures for VAPT operations., Request for a VAPT scan., Result from a VAPT scan. (+15 more)

### Community 21 - "Adapter Base Types"
Cohesion: 0.13
Nodes (19): ABC, AdapterStatus, Base classes and contracts for VAPT external adapters., True when the environment contains everything needed to attempt a run., True when the adapter should participate in scans., Return current availability status (should not raise)., Health/availability status of an adapter., Contract implemented by every external VAPT integration. Lifecycle during a… (+11 more)

### Community 22 - "Scanner Tool Registry"
Cohesion: 0.09
Nodes (20): get_tool_registry(), Enum, str, Kali Linux Security Tool Registry  Comprehensive registry of security tools avai, Tool categories matching VAPT workflow., Metadata about a security tool., Default configuration for a tool., Registry for managing security tools. (+12 more)

### Community 23 - "Kali Tool Adapter"
Cohesion: 0.11
Nodes (10): _KaliToolAdapter, LyrieAdapter, Any, VAPTScanType, RaccoonAdapter, Raccoon recon scanner (DNS/WHOIS/TLS/WAF/subdomains/dir-busting)., Filter crash/traceback/banner noise out of tool output before parsing., Lyrie autonomous pentest CLI (lyrie scan -> SARIF findings). (+2 more)

### Community 24 - "Report Engine"
Cohesion: 0.13
Nodes (23): AssessmentModel, details_env(), _finding_to_security_finding(), generate_report(), GenerateReportRequest, list_reports(), list_templates(), AsyncSession (+15 more)

### Community 25 - "Scans UI"
Cohesion: 0.09
Nodes (28): Finding, getSeverityBadge(), getTypeIcon(), getTypeLabel(), LiveScanConsole(), phaseIcons, PlanPhase, PlanTool (+20 more)

### Community 26 - "Knowledge Base Sources"
Cohesion: 0.11
Nodes (26): analysis_step(), exploitation_step(), BaseModel, Uses an LLM with structured output to analyse scan results., Simulates a controlled exploitation attempt against confirmed findings. In a…, Compiles a human-readable penetration test report from the state., Structured result returned by the LLM when analysing scan findings., Simulates subfinder to discover subdomains. (+18 more)

### Community 27 - "RAG Pipeline"
Cohesion: 0.07
Nodes (29): autoprefixer, eslint-config-next, devDependencies, autoprefixer, eslint-config-next, jsdom, postcss, prettier (+21 more)

### Community 28 - "Auth & API Keys"
Cohesion: 0.17
Nodes (28): RoleName, PyEnum, ApiKeyBase, ApiKeyCreate, ApiKeyCreateResponse, ApiKeyRead, MembershipBase, MembershipCreate (+20 more)

### Community 29 - "Recon Orchestrator"
Cohesion: 0.10
Nodes (21): check_tool_availability(), get_available_tools(), get_tool(), get_tools_for_scan_type(), VAPTScanType, VAPTTool, VAPT Tools Registry Direct integration with host-installed security tools. Fast…, Tools run inside the astraix-kali container, not the backend process.… (+13 more)

### Community 30 - "Scanner Execution"
Cohesion: 0.11
Nodes (15): Finding, Parse Nmap text output as fallback., Map Nikto OSVDB ID to severity., Parse Nuclei JSON output to findings., Parse SQLMap JSON output to findings., Map tool-specific severity string to Severity enum., Parse Gobuster JSON output to findings., Parse FFUF JSON output to findings. (+7 more)

### Community 31 - "VAPT Adapters"
Cohesion: 0.10
Nodes (15): LyrieAIAgent, Lyrie AI Agent executor for autonomous security operations.      Features:     -, Run 7-phase autonomous pentest.          Args:             target: URL or local, Scan URL or file for security issues.          Checks:         - Security header, AI red-team an LLM endpoint.          Strategies:         - crescendo: gradual e, Calculate CVSS v3.1 score from vector.          Args:             vector: CVSS v, Verify agent identity using Agent Trust Protocol.          Args:             age, Display ATP compliance badge.          Returns:             dict with badge info (+7 more)

### Community 32 - "Auth & API Keys"
Cohesion: 0.13
Nodes (25): api_key_header, decode_token(), get_current_active_user(), get_current_superuser(), get_current_user(), get_role_permissions(), get_user_organizations(), get_user_projects() (+17 more)

### Community 33 - "Auth & API Keys"
Cohesion: 0.12
Nodes (4): MembershipRepository, ProjectRepository, UUID, Get a project with real asset/assessment/finding counts attached.

### Community 34 - "Assessments API"
Cohesion: 0.10
Nodes (24): build_app(), lifespan(), FastAPI app factory.  Binds the DI container to the web transport.  - Health/rea, Start/stop lifetime management., Create the FastAPI application.      Mostly configures routing + middleware; DI, _map_error(), Convert platform errors → HTTP responses.  FastAPI exception handlers delegate t, Bind platform error handler. (+16 more)

### Community 35 - "Auth & API Keys"
Cohesion: 0.07
Nodes (27): axios, class-variance-authority, clsx, date-fns, dependencies, axios, class-variance-authority, clsx (+19 more)

### Community 36 - "VAPT DTOs"
Cohesion: 0.15
Nodes (6): VAPTFinding, VAPTScanRequest, VAPTScanResult, VAPTSeverity, VAPTTool, VAPTExecutor

### Community 37 - "External Adapter Registry"
Cohesion: 0.15
Nodes (25): Dark-Moon Adapter, Lyrie Adapter, PentAGI Adapter, Raccoon Adapter, Redamon Adapter, Xalgorix Adapter, Zen-ai-pentest Adapter (GitHub Actions), Kali Container Execution via Docker Socket (+17 more)

### Community 38 - "Scan Orchestration"
Cohesion: 0.15
Nodes (23): cancel_assessment(), create_assessment(), get_assessment(), list_assessments(), AsyncSession, delete, get, post (+15 more)

### Community 39 - "Findings API"
Cohesion: 0.15
Nodes (23): bulk_update_findings(), BulkUpdateRequest, delete_finding(), get_finding(), list_findings(), AsyncSession, BaseModel, delete (+15 more)

### Community 40 - "Sample VAPT Reports"
Cohesion: 0.10
Nodes (25): Prime Infoserv VAPT Report of IT Landscape at Betala Stock Broking, Network VAPT of IT Landscape, Cybersecify SOC 2 + ISO 27001 Sample Pentest Report, Broken Auth on API Token Refresh (CS-2026-010), IDOR in Billing API (CS-2026-001), Stored XSS in User Profile Bio (CS-2026-004), Invia VAPT Report (Web Application Penetration Testing), CSRF Leads to Account Takeover (+17 more)

### Community 41 - "VAPT Adapters"
Cohesion: 0.14
Nodes (15): ExternalTool, Any, ScanRequest, ScanResult, Execute a complete security scan., Get tools for a given capability., Execute a single tool and return parsed findings., Execute multiple tools in parallel. (+7 more)

### Community 42 - "Plugin System"
Cohesion: 0.10
Nodes (17): BasePlugin, FindingOut, PluginError, PluginOutput, PluginSchema, Parse stdin: str → dict., Structured logging accessible to orchestrator., Schema for plugin I/O, described in plugin.yml. (+9 more)

### Community 43 - "CWE Vulnerability Mapping"
Cohesion: 0.12
Nodes (24): SQL Injection in Search Endpoint (CS-2026-002), Stored Cross-Site Scripting (4 Instances), CWE-120 Buffer Overflow, CWE-22 Path Traversal, CWE-327 Insecure Cryptography, CWE-416 Use After Free, CWE-502 Insecure Deserialization, CWE-77 Command Injection (+16 more)

### Community 44 - "Plugin System"
Cohesion: 0.12
Nodes (11): CapabilityAlreadyRegisteredError, CapabilityNotFoundError, Capability-specific error types., Raised when attempting to register a duplicate capability., Raised when a capability is not found in the registry., CapabilityVersion, Semantic version (major.minor.patch)., CapabilityRegistry (+3 more)

### Community 45 - "Dashboard UI"
Cohesion: 0.16
Nodes (19): react, QuickAction, Dialog(), DialogContent(), DialogContentProps, DialogContext, DialogContextValue, DialogDescription() (+11 more)

### Community 46 - "Scan Orchestration"
Cohesion: 0.12
Nodes (19): Base, TimestampMixin, UUIDMixin, DeclarativeBase, Mapped, BaseModel, FindingOut, PluginError (+11 more)

### Community 47 - "Plugin System"
Cohesion: 0.19
Nodes (19): Path, find_dataset_dir(), handle_ai_generic(), handle_cve_generic(), handle_ids_generic(), handle_phish_generic(), handle_siem_generic(), main() (+11 more)

### Community 48 - "Plugin System"
Cohesion: 0.16
Nodes (13): DefaultWorkflowEngine, Workflow Engine — declarative Workflow + Capability resolution.  A `Workflow` is, Workflow + the chain of references used to compile it., Declarative workflow repository.      Engines do not *run* workflows; they resol, Process-local default engine.      Workflows are stored by id. Capabilities are, WorkflowEngine, WorkflowRecord, WorkflowResolutionError (+5 more)

### Community 49 - "Dashboard UI"
Cohesion: 0.12
Nodes (16): RecentAssessments(), statusConfig, navigation, settingsNav, Sidebar(), DropdownMenuCheckboxItem, DropdownMenuContent, DropdownMenuItem (+8 more)

### Community 50 - "Knowledge Base Sources"
Cohesion: 0.09
Nodes (22): block_indicator(), check_threat_intel(), disable_account(), find_related_alerts(), get_alert_details(), get_alert_queue(), get_process_tree(), isolate_host() (+14 more)

### Community 51 - "Domain Assessment Types"
Cohesion: 0.16
Nodes (14): Assessment, Exception, Finding, PluginError, PluginOutput, PluginRegistry, Orchestrator, Build plugin invocation params from assessment. (+6 more)

### Community 52 - "Plugin System"
Cohesion: 0.13
Nodes (18): get_dashboard_activity(), get_dashboard_stats(), list_capabilities(), ping(), AsyncSession, get, post, UUID (+10 more)

### Community 53 - "Plugin System"
Cohesion: 0.09
Nodes (21): compilerOptions, allowJs, baseUrl, esModuleInterop, forceConsistentCasingInFileNames, incremental, isolatedModules, jsx (+13 more)

### Community 54 - "Plugin System"
Cohesion: 0.10
Nodes (8): FindingDetail(), formatDetails(), severityStyles, findingsApi, healthApi, pluginsApi, Finding, Plugin

### Community 55 - "Plugin System"
Cohesion: 0.15
Nodes (15): emit_plugin_completed(), emit_plugin_finding(), emit_plugin_progress(), emit_plugin_started(), PluginCompletedPayload, PluginFindingPayload, PluginProgressPayload, PluginStartedPayload (+7 more)

### Community 56 - "Database Layer"
Cohesion: 0.21
Nodes (18): create_asset(), delete_asset(), get_asset(), list_assets(), AsyncSession, delete, get, patch (+10 more)

### Community 57 - "Auth & API Keys"
Cohesion: 0.14
Nodes (7): ApiKeyRepository, get_api_key_repo(), get_membership_repo(), get_organization_repo(), get_project_repo(), get_user_repo(), AsyncSession

### Community 58 - "Xalgorix Adapter"
Cohesion: 0.21
Nodes (3): Any, VAPTScanType, XalgorixAdapter

### Community 59 - "Database Layer"
Cohesion: 0.16
Nodes (10): AsyncSession, get_session(), Database session dependency., BaseRepository, Repository pattern for data access.  Each repository:   - Wraps SQLAlchemy queri, Generic repository for any model., List with pagination and optional filters., Count records with optional filters. (+2 more)

### Community 60 - "Dashboard UI"
Cohesion: 0.14
Nodes (9): QuickActions(), RecentFindings(), StatCardProps, StatsCards(), ComponentRowProps, SystemStatus(), dashboardApi, systemApi (+1 more)

### Community 61 - "Projects API"
Cohesion: 0.12
Nodes (19): OWASP Projects (ADR Tier 3), paulveillard/cybersecurity (ADR Tier 1), Anthropic Cybersecurity Skills Repo, awesome-soc Repo, Berkanktk/CyberSecurity Repo, CAI (Cybersecurity AI) Repo, cybersecurity-knowledge-base Repo, Cybersecurity-Resources Repo (+11 more)

### Community 62 - "Knowledge Base Sources"
Cohesion: 0.14
Nodes (18): AgentState, ai_triage_node(), AIVerdict, analyze_url_tool(), enrich_url_node(), BaseModel, TypedDict, Uses the AI model to decide if the URL is malicious or benign and provide an… (+10 more)

### Community 63 - "AI Gateway Interface"
Cohesion: 0.18
Nodes (12): AIGateway, Single entry point for AI reasoning tasks.      Implementations are responsible, AIResponse, A provider's structured response., NoopResponseParser, ParsedAIResponse, Response Parser — safe parsing of provider output back to types.  The Gateway em, Factory: try JSON parse; fall back to a `{"text": ...}` envelope. (+4 more)

### Community 64 - "Prompt Management"
Cohesion: 0.16
Nodes (9): _InMemoryPromptManager, PromptManager, PromptTemplate, PromptVersionError, Prompt Manager — versioned prompt templates.  A `PromptTemplate` is a parameteri, Raised when a requested `prompt_id` / version combination is unknown., One version of one prompt.      The text uses stdlib `Template` semantics ($-sty, Resolved-source-of-truth for prompt templates. (+1 more)

### Community 65 - "AI Gateway"
Cohesion: 0.14
Nodes (12): AITokenUsage, NoopTokenManager, _PlanningError, Token Manager — budgets, accounting, retries, compression.  At Milestone 1 we sh, Hard limits for a call. `None` = no limit on that field., Pre-call planning + post-call accounting., Estimate prompt tokens; raise `PlanningError` if over budget., Persist a usage line for accounting. (+4 more)

### Community 66 - "Scan Orchestration"
Cohesion: 0.16
Nodes (6): get_graph(), get, get_knowledge_graph(), KnowledgeGraph, _node_id(), _node_tooltip()

### Community 67 - "Auth & API Keys"
Cohesion: 0.30
Nodes (13): Assessment, Base, Asset, Base, TimestampMixin, UUIDMixin, ApiKey, AuditLog (+5 more)

### Community 68 - "Report Generation"
Cohesion: 0.22
Nodes (14): _ai_comment_placeholder(), _build_section(), _findings_section(), NullReportEngine, Report Engine — implementation.  At Milestone 1, only the JSON/Markdown default, Render reports from findings + risk scores., JSON/Markdown default at Milestone 1.      Produces deterministic artefacts usin, ReportEngine (+6 more)

### Community 69 - "Planner Agent"
Cohesion: 0.18
Nodes (8): get_planner(), PlannerAgent, Any, VAPTScanType, AI Planner Agent Decides the VAPT plan: which tools to run, in which phase, and…, Ask the LLM (NVIDIA NIM, falling back to Ollama) to refine tool selection.…, Generate the full phased VAPT plan with KB-grounded reasoning., Knowledge-base-grounded plan generator for VAPT scans.

### Community 70 - "Risk Engine"
Cohesion: 0.12
Nodes (16): Risk Engine, Custom Kali Image (astraix-kali), Docker Compose Stack, Frontend Dashboard, Keep a Changelog Format, Normalized Findings, Plugin Architecture, Real VAPT Pipeline (+8 more)

### Community 71 - "AI Gateway"
Cohesion: 0.19
Nodes (7): ProviderAlreadyRegisteredError, ProviderManager, ProviderNotFoundError, Provider Manager.  The Manager owns the lifecycle of providers. Applications nev, Thread-safe registry of providers.      The Manager is the *only* place provider, AIProvider, Concrete providers (OpenAI/Anthropic/...) implement this.

### Community 72 - "Plugin System"
Cohesion: 0.18
Nodes (12): build_default_container(), _MutableContainer, Dependency Injection container.  Uses DI’y to wire the entire platform without m, # TODO: Lookup normalizer + register, Mutable (thread-safe) wiring harness., Safely edit mutable values., Return a frozen copy ready for consumption., Wire default implementations for production runtime. (+4 more)

### Community 73 - "Progress Bus"
Cohesion: 0.23
Nodes (7): get_progress_bus(), publish_scan_event(), Any, Scan Progress Bus Redis-backed event stream for live scan progress. Each scan…, List scans that are still running (non-terminal status)., Publishes and reads scan progress events (Redis-backed, in-memory fallback)., ScanProgressBus

### Community 74 - "Plugin System"
Cohesion: 0.17
Nodes (7): PluginAlreadyRegisteredError, PluginNotFoundError, PluginRecord, PluginRegistry, Plugin Registry: what exists and how it is looked up.  The Registry owns *record, Pairing of manifest with its resolved filesystem location., In-memory registry. Thread-safe.      Persistence (saving registered plugin stat

### Community 75 - "RAG Pipeline"
Cohesion: 0.14
Nodes (15): AI Gateway (Gemini), OpenAI SDK Dependency, Gemini AI Summaries, CSKB Alternatives Considered, cs kb CLI, CSKB Platform Principles Compliance, ContextBuilder Integration, CSKB Sibling Docker Image (+7 more)

### Community 76 - "Planner Agent"
Cohesion: 0.14
Nodes (15): Cybersecurity Knowledge Base (TF-IDF), faiss-cpu Dependency, fastembed Dependency, kb-data Named Volume, KB Docker Architecture, Knowledge Base HTTP API, Kaggle Security Datasets Manifest, KB + SFT Expansion Pipeline (+7 more)

### Community 77 - "Graph Page"
Cohesion: 0.13
Nodes (3): GROUP_STYLES, SEVERITY_COLORS, ApiClient

### Community 78 - "Knowledge Base Sources"
Cohesion: 0.17
Nodes (14): AgentState, analyze_exploitation_node(), ExploitationInsights, get_kev_vulnerabilities_node(), BaseModel, TypedDict, Uses an AI model to analyze exploitation vectors and associated CWEs., A terminal node that prints the final, combined report. (+6 more)

### Community 79 - "Plugin System"
Cohesion: 0.17
Nodes (9): Translate the decision + manifest into a safe subprocess argv.          The inte, PluginValidationError, PluginValidator, Plugin Validator: schema, capability, and permission checks.  The Validator is t, Tiny subset of JSON Schema type matching for type-checking most params., Validates a manifest + proposed invocation parameters.      Stateless aside from, _type_match(), ValidationResult (+1 more)

### Community 80 - "Planner Agent"
Cohesion: 0.17
Nodes (12): Task Planner tests.  Targets:   - DAG topology respecting `depends_on`   - Paral, A -> B -> C runs in serial., A -> B,C -> D runs B/C in parallel., test_diamond_workflow(), test_linear_workflow(), load_workflow_from_yaml(), Workflow — declarative YAML-loadable structure.  Reuse of the canonical `Workflo, Read a YAML workflow file and return a typed `Workflow`.      Raises `WorkflowLo (+4 more)

### Community 81 - "Misc Utilities"
Cohesion: 0.16
Nodes (12): get_container(), get_settings(), Dependency providers for FastAPI routes., FastAPI dependency: immutable container wired to pathOps., Shortcut: typed settings., health(), FastAPI transport: health, ready, version.  All other API routes beyond these th, Endpoint health; always 200. (+4 more)

### Community 82 - "Finding Engine"
Cohesion: 0.18
Nodes (14): Finding Engine, Semgrep SAST Scanner Plugin, Subfinder Subdomain Enumeration Plugin, Trivy Security Scanner Plugin, Report Engine, code/audit capability, sast/security capability, osint/asset-discovery capability (+6 more)

### Community 83 - "HTTPx Tooling"
Cohesion: 0.22
Nodes (13): Headers, _add(), _detect_cdn(), _detect_technologies(), _extract_title(), main(), probe_target(), Extract version from header like 'nginx/1.21.6'. (+5 more)

### Community 84 - "Knowledge Base Sources"
Cohesion: 0.15
Nodes (11): create_threat_hunting_report(), develop_hunting_strategy(), gather_threat_context(), perform_technical_analysis(), process_indicator_and_run_parallel(), Performs technical analysis on the indicator. Args: indicator_info (str): The…, Gathers threat context information for the indicator. Args: indicator_info…, Develops a hunting strategy for the indicator. Args: indicator_info (str): The… (+3 more)

### Community 85 - "Plugin System"
Cohesion: 0.19
Nodes (8): LoadedPlugin, PluginLoader, PluginLoaderError, Plugin Loader: read manifests from disk → PluginRecords.  The Loader is the *onl, A loader-level result wrapping a successfully parsed manifest., Filesystem-based plugin loader.      The exact YAML layout is opaque outside thi, Walk the plugins root; return all parseable plugin records.          Directories, Load a single plugin by directory path.          Raises PluginLoaderError on mis

### Community 86 - "Auth Login"
Cohesion: 0.23
Nodes (13): login(), login_json(), OAuth2 compatible login for Swagger UI., JSON-based login for frontend applications., Refresh access token., refresh_token(), Token, UserLogin (+5 more)

### Community 87 - "Knowledge API"
Cohesion: 0.19
Nodes (12): get_kb_source(), knowledge_stats(), list_kb_sources(), get, post, Search the cybersecurity knowledge base., Get knowledge base statistics., Rebuild FAISS vector index from chunks.json. (+4 more)

### Community 88 - "Scan Orchestration"
Cohesion: 0.27
Nodes (6): Any, VAPTFinding, VAPTScanRequest, VAPTScanResult, Attach a callback for live progress events (scan_id, event_type, data)., ReconOrchestrator

### Community 89 - "VAPT Adapters"
Cohesion: 0.18
Nodes (8): Any, VAPTScanType, Adapters are skipped for targets they cannot meaningfully test., Execute the adapter against ``target``. Must never raise - errors are captured…, Map arbitrary severity strings from external tools to VAPTSeverity., to_severity(), VAPTFinding, VAPTSeverity

### Community 90 - "Verifier Agent"
Cohesion: 0.24
Nodes (6): VAPTFinding, VAPTSeverity, Best-effort lookup of exploitation/technique guidance in the knowledge base for…, Verify findings concurrently (bounded) so long-running re-exploits (e.g.…, VerifierAgent, get_vapt_executor()

### Community 91 - "Nmap Tooling"
Cohesion: 0.23
Nodes (12): Element, build_nmap_command(), main(), _parse_host(), parse_nmap_xml(), _parse_port(), Parse a single host element., Parse a port element. (+4 more)

### Community 92 - "AI Gateway"
Cohesion: 0.19
Nodes (13): AI Gateway Module, AI-SecOS Core, Infrastructure Module, Domain Models Module, Normalizer Module, Platform Bootstrap Module, Plugin System Module, Report Engine Module (+5 more)

### Community 93 - "Auth & API Keys"
Cohesion: 0.26
Nodes (3): get_knowledge_base(), KnowledgeBase, Hybrid search engine: FAISS vector (fastembed) + TF-IDF fallback.

### Community 94 - "Knowledge Base Sources"
Cohesion: 0.17
Nodes (11): create_threat_hunting_report(), develop_hunting_strategy(), gather_threat_context(), perform_technical_analysis(), process_indicator_and_run_parallel(), Performs technical analysis on the indicator. Args: indicator_info (str): The…, Gathers threat context information for the indicator. Args: indicator_info…, Develops a hunting strategy for the indicator. Args: indicator_info (str): The… (+3 more)

### Community 95 - "Knowledge Base Sources"
Cohesion: 0.22
Nodes (12): example_direct_mcp_usage(), example_infrastructure_mapping(), example_langgraph_integration(), example_security_monitoring(), example_threat_intelligence(), main(), Example of using Shodan MCP server for threat intelligence gathering., Example of mapping an organization's infrastructure using Shodan. (+4 more)

### Community 96 - "Knowledge Base Sources"
Cohesion: 0.26
Nodes (12): demo_dns_intelligence(), demo_infrastructure_reconnaissance(), demo_iot_security_analysis(), demo_vulnerability_assessment(), main(), Demo the IoT security analysis scenario., Demo the DNS intelligence gathering scenario., Simulate running an agent scenario. (+4 more)

### Community 97 - "Knowledge Base Sources"
Cohesion: 0.22
Nodes (12): example_direct_mcp_usage(), example_infrastructure_mapping(), example_langgraph_integration(), example_security_monitoring(), example_threat_intelligence(), main(), Example of using Shodan MCP server for threat intelligence gathering., Example of mapping an organization's infrastructure using Shodan. (+4 more)

### Community 98 - "Misc Utilities"
Cohesion: 0.19
Nodes (10): Result, fail(), Failure, is_failure(), is_ok(), ok(), Result type (Rust/Python-port idiom) for explicit success/failure.  Used by serv, Successful outcome carrying a value. (+2 more)

### Community 99 - "Plugin System"
Cohesion: 0.24
Nodes (10): AIError, ConfigurationError, FindingEngineError, PlatformError, PluginError, Single error hierarchy for the entire AI-SecOS Core.  Public API (the only types, Base error of the platform.      Carries `code` (machine-readable, stable) and `, ReportEngineError (+2 more)

### Community 100 - "AI Gateway"
Cohesion: 0.21
Nodes (9): ContextBuilder, NullContextBuilder, Context Builder — assembles what's fed into a prompt.  Pre-AI responsibilities:, Build a `FindingContextPayload` from typed inputs., Default at Milestone 1.      Performs no compression or redaction. A future mile, DefaultAIGateway, AI Gateway — composed pipeline.  Pipeline order (matches Architecture):    1. Ro, Default wired pipeline. (+1 more)

### Community 101 - "Model Routing"
Cohesion: 0.20
Nodes (8): ModelRouter, NullModelRouter, Model Router — decides `(provider_id, model)` per request.  At Milestone 1 we sh, Decides which provider/model to use., Pass-through router registered by default at Milestone 1., Deterministic choice for tests / deterministic callers., RoutingDecision, select_first_providers()

### Community 102 - "Scan Orchestration"
Cohesion: 0.20
Nodes (8): Asset, AsyncSession, UUID, Run scan using the plugin system (fallback)., Process plugin findings, dedupe, persist., Stable identifier: title + asset., Run an assessment by ID. Updates state as we progress., PluginRunResult

### Community 103 - "Plugin System"
Cohesion: 0.21
Nodes (8): CapabilityResolverError, Raised when capability resolution fails (missing workflow, etc.)., Capability Resolver.  Resolves a `Capability` request into a concrete execution, Validate inputs against the capability's input schema (lightweight).          Pe, Raised when capability resolution fails., A Capability fully resolved to executable Workflows., ResolutionError, ResolvedCapability

### Community 104 - "Product Docs"
Cohesion: 0.17
Nodes (12): Application Security Module, Cloud Security Module, Data Security Module, Defensive Security Module, Email Security Module, GRC & Compliance Module, Identity Security Module, Mobile Security Module (+4 more)

### Community 105 - "HTTPx Tooling"
Cohesion: 0.24
Nodes (10): _confidence(), _extract_items(), make_httpx_input(), _normalize_one(), _normalize_tech(), HTTP Probe (httpx) Plugin — normalizer.  Converts raw `httpx` output into canoni, Stack detection → asset_inventory findings., Convenience: build the stdin payload for the httpx executable. (+2 more)

### Community 106 - "Knowledge Base Sources"
Cohesion: 0.18
Nodes (10): decide_next_step(), IncidentState, initial_analysis(), malware_analysis(), phishing_analysis(), TypedDict, Perform initial analysis of the alert. Args: state (dict): The current state of…, Perform detailed phishing analysis. Extract malicious URL from phishing email… (+2 more)

### Community 107 - "Knowledge Base Sources"
Cohesion: 0.22
Nodes (10): AgentState, call_model(), nmap_scan(), TypedDict, The primary agent node. It calls the AI model to decide the next action., Runs a real Nmap scan on a target IP or domain using python-nmap., Simulates searching Exploit-DB for a given query (e.g., a software name)., Conditional logic to decide whether to continue or end the workflow. (+2 more)

### Community 108 - "Plugin System"
Cohesion: 0.20
Nodes (10): PluginCapabilityRequirement, PluginInputSchema, PluginOutputSchema, PluginResourceLimits, PluginSandboxPolicy, Plugin manifest (the typed shape of a `plugin.yml`).  Schema is intentionally st, A Capability the Plugin requires from the platform., Hard limits applied by the Sandbox. (+2 more)

### Community 109 - "AI Provider Abstraction"
Cohesion: 0.24
Nodes (7): AIRequest, AITokenUsage, NullProvider, AI Provider port.  A Provider is anything that can take a prompt + structured in, Tokens billed for one call. Independent of model types., A request is a structured, traceable call.      `prompt` is the raw text/materia, Identity provider for tests and the empty Milestone 1 default.      Returns requ

### Community 110 - "README Docs"
Cohesion: 0.20
Nodes (10): AI Core Layer, AI Integration Architecture, Data Architecture (Hot/Warm/Cold), Deployment Options, Integration Ecosystem (100+ Native), AstraIX Full-Spectrum Platform Vision, Platform Roadmap (5 Phases to 2027), Platform Technology Stack (+2 more)

### Community 111 - "RAG Pipeline"
Cohesion: 0.20
Nodes (10): scripts, build, dev, format, lint, start, test, test:coverage (+2 more)

### Community 112 - "Knowledge Base Sources"
Cohesion: 0.27
Nodes (9): agent_node(), AgentState, decide_next(), TypedDict, State for the agent graph., Use the LLM to decide the next step or provide an answer., Search the vector store for relevant documents., Decide whether to search again or finish. (+1 more)

### Community 113 - "Knowledge Base Sources"
Cohesion: 0.29
Nodes (9): main(), Test basic connectivity to Shodan API., Test that required environment variables are set., Test that required Python packages are installed., Test that required files are present., test_dependencies(), test_environment_variables(), test_file_structure() (+1 more)

### Community 114 - "Knowledge Base Sources"
Cohesion: 0.44
Nodes (9): download_file(), run_gau(), run_httpx_tech_detection(), run_nuclei(), run_subfinder(), run_tool(), run_waybackurls(), serve_openapi() (+1 more)

### Community 115 - "Nmap Tooling"
Cohesion: 0.22
Nodes (9): AstraIX Autonomous VAPT Platform, astraix-kali:latest Docker Image, Gemini LLM, Gobuster, Nikto, Nmap, Nuclei, Sqlmap (+1 more)

### Community 116 - "Scanner Execution"
Cohesion: 0.22
Nodes (5): Any, Check if a specific tool is available., Check if Docker is available., Get availability status of all tools., Get overall health status of the scanner.

### Community 117 - "Misc Utilities"
Cohesion: 0.28
Nodes (6): BaseSchema, PaginatedResponse, Base schema with ORM mode enabled., Standard success response wrapper., Paginated results wrapper., ResponseSchema

### Community 118 - "Researcher Agent"
Cohesion: 0.36
Nodes (3): _load_kb(), VAPTFinding, ResearcherAgent

### Community 119 - "Scan Orchestration"
Cohesion: 0.22
Nodes (7): event_loop(), Pytest configuration and fixtures., mock_registry(), mock_settings(), Override default event loop., Mock settings for tests., Mock plugin registry.

### Community 120 - "Plugin System"
Cohesion: 0.25
Nodes (9): System Architecture, Applications Layer, Plugin Executor, Plugin Manager, Plugin Sandbox, Plugin Validator, Plugins Layer, SecurityPlugin PDK (+1 more)

### Community 121 - "Nmap Tooling"
Cohesion: 0.28
Nodes (4): NmapScanner, Run as process: stdin → scan → stdout, Run nmap, parse output, return findings., Parse Nmap XML/text → findings.

### Community 122 - "Trivy Tooling"
Cohesion: 0.28
Nodes (7): _extract_cvss(), _normalize_misconfiguration(), _normalize_vulnerability(), Trivy Plugin — normalizer.  Converts raw `trivy` output into canonical `Security, Normalize a single misconfiguration finding., Extract CVSS score from trivy vulnerability data., Normalize a single vulnerability finding.

### Community 123 - "AI Gateway"
Cohesion: 0.29
Nodes (5): FindingContextPayload, What the AI sees. Pre-serialization.      The AI Gateway *never* receives the ra, Convenience: flatten to a dict for string substitution., Numeric, bounded 0–100 risk.      Use `.factors` to display *why* the score is w, RiskScore

### Community 124 - "AI SecOS Core"
Cohesion: 0.25
Nodes (6): _noop_dedup(), Milestone 2 End-to-End Demo — Capability -> Workflow -> Plugin -> Findings.  Dem, Minimal in-memory deduplicator for M2 demo only., M2 End-to-End test.  Validates the vertical slice: Capability → Plugin → Normali, The full M2 path executes end-to-end and emits a summary., test_m2_demo_runs()

### Community 125 - "Plugin System"
Cohesion: 0.25
Nodes (8): Network Vulnerability Assessment, External Asset Discovery, Web Discovery, Web Application Security Assessment, HTTPX Scanner Plugin, Nmap Scanner Plugin, Nuclei Scanner Plugin, Subfinder Scanner Plugin

### Community 126 - "VAPT Adapters"
Cohesion: 0.39
Nodes (8): Dark-Moon Platform, Lyrie AI Platform, Offensive Security Module, PentAGI Platform, RedAmon Platform, VAPT Capability, Xalgorix Platform, Integrated VAPT Platforms (Branding)

### Community 127 - "Product Docs"
Cohesion: 0.25
Nodes (8): ASTRAIX AI-Native Philosophy, The 9 ASTRAIX Domains, ASTRAIX Platform Name, ASTRAIX Brand Visual Identity, SecOS Platform Name, 12 Security Domains (SecOS), SecOS Brand Visual Identity, SecOS AI-First Security Domains

### Community 128 - "README Docs"
Cohesion: 0.25
Nodes (8): SecOS AI Modules, SecOS AI-Native Philosophy, SecOS Differentiation Matrix, SecOS AI-First Difference, SecOS Deployment Options, SecOS Platform, SecOS Vision, README Documentation Index

### Community 129 - "Engineering Docs"
Cohesion: 0.25
Nodes (8): Aif4thah Dojo-101, ElNiak awesome-ai-cybersecurity, GitHub Cybersecurity Topics, naveen-98 Cyber_Security_Reference, okhosting awesome-cyber-security, santosomar AI-agents-for-cybersecurity, KB Source List (Tier 1-3), tomwechsler Cyber Knowledge Base

### Community 130 - "Engineering Docs"
Cohesion: 0.25
Nodes (8): Coding Standards, Python Standards, TypeScript Standards, MVP Scope Definition, Build Later Items, Build Now Items, Never Build Items, Master AI Engineer Rules

### Community 131 - "Knowledge Base Sources"
Cohesion: 0.25
Nodes (6): create_pentest_plan(), perform_reconnaissance(), plan_exploitation(), This function generates a prompt for reconnaissance techniques and tools based…, This function generates a prompt for exploitation methods and tools based on…, This function combines the reconnaissance and exploitation phases into a…

### Community 132 - "Nuclei Tooling"
Cohesion: 0.36
Nodes (7): build_nuclei_command(), main(), parse_nuclei_json(), Execute nuclei and return parsed results., Build nuclei command arguments., Parse nuclei JSON output lines., run_nuclei_scan()

### Community 133 - "Semgrep Tooling"
Cohesion: 0.36
Nodes (7): build_semgrep_command(), main(), parse_semgrep_results(), Build semgrep command arguments., Parse semgrep JSON output., Execute semgrep and return parsed results., run_semgrep_scan()

### Community 134 - "Subfinder Tooling"
Cohesion: 0.36
Nodes (7): build_subfinder_command(), main(), parse_subfinder_json(), Build subfinder command arguments., Parse subfinder JSON output lines., Execute subfinder and return parsed results., run_subfinder()

### Community 135 - "Trivy Tooling"
Cohesion: 0.36
Nodes (7): build_trivy_command(), main(), parse_trivy_results(), Build trivy command arguments., Parse trivy JSON output., Execute trivy and return parsed results., run_trivy_scan()

### Community 137 - "Database Layer"
Cohesion: 0.29
Nodes (7): Product API Endpoints, Database Schema (Core Tables), Product Deployment Architecture, ASTRAIX Product Overview, Known Issues (Demo Mode), Target Market, Phase 1 VAPT Module

### Community 138 - "Plugin System"
Cohesion: 0.29
Nodes (7): Capability Abstraction, Workflow Abstraction, AstraIX Platform Constitution, AI-SecOS Core Runtime, Plugin System, Security Analyst Application, Canonical Security Finding Schema

### Community 139 - "Plugin System"
Cohesion: 0.43
Nodes (7): web/discovery capability, api/security capability, web/vuln-scan capability, HTTP Probe (httpx) Plugin, Nuclei Vulnerability Scanner Plugin, Web Discovery Workflow, Web Application VAPT Workflow

### Community 140 - "Knowledge Base Sources"
Cohesion: 0.29
Nodes (6): create_pentest_plan(), perform_reconnaissance(), plan_exploitation(), This function generates a prompt for reconnaissance techniques and tools based…, This function generates a prompt for exploitation methods and tools based on…, This function combines the reconnaissance and exploitation phases into a…

### Community 141 - "Knowledge Base Sources"
Cohesion: 0.29
Nodes (6): get_current_time(), BaseModel, Returns the current time in H:MM AM/PM format., Scans the specified IP address or range using nmap., scanner(), ScannerInput

### Community 142 - "Misc Utilities"
Cohesion: 0.43
Nodes (4): BaseSchema, ErrorResponse, PaginatedResponse, ResponseSchema

### Community 143 - "Database Layer"
Cohesion: 0.40
Nodes (4): do_run_migrations(), run_async_migrations(), run_migrations_online(), Connection

### Community 144 - "Sample Web App Findings"
Cohesion: 0.33
Nodes (6): PurpleSec Application Penetration Assessment Sample Report, Authorization Restriction Bypass, GraphQL Introspection Enabled, Open Redirect, Session Hijacking, PurpleSec

### Community 145 - "Engineering Docs"
Cohesion: 0.33
Nodes (6): Project Roadmap, Milestone 1 - AI-SecOS Core, Milestone 2 - First Plugin httpx, Milestone 3 - Discovery Capability, Milestone 4 - Web Security Assessment, Milestone 5 - Security Analyst UI

### Community 146 - "Branding Icons"
Cohesion: 0.47
Nodes (6): AstraIX App Icon, White Check Mark, Slate and Cyan Palette, Rounded Square Background, Security Branding Motif, Cyan Shield Glyph

### Community 147 - "KB Ingestion"
Cohesion: 0.53
Nodes (4): chunk_text(), collect_files(), extract_title(), main()

### Community 148 - "Fast KB Ingestion"
Cohesion: 0.53
Nodes (5): chunk_by_lines(), extract_title(), get_files(), main(), Fast knowledge base ingestion - line-based chunking.

### Community 150 - "Knowledge Base Sources"
Cohesion: 0.40
Nodes (5): get_cisa_kev_catalog(), Runs an nmap scan on the specified hosts with the given arguments. :param…, Fetches the latest CISA Known Exploited Vulnerabilities (KEV) catalog. :return:…, run_nmap_scan(), tool

### Community 152 - "Product Docs"
Cohesion: 0.60
Nodes (5): ASTRAIX AI Modules, SecOS AI Core Layer, NeuralSec Engine, SecAgent Framework, ThreatGPT Advisor

### Community 153 - "Engineering Docs"
Cohesion: 0.40
Nodes (5): Technology Stack, AI Tech Stack, Backend Tech Stack, DevOps Tech Stack, Frontend Tech Stack

### Community 154 - "Infrastructure"
Cohesion: 0.50
Nodes (4): platform_error_to_http_response(), PlatformErrorResponse, Map platform errors → HTTP responses.  FastAPI exception handler in `platform/`, Convert a PlatformError to a status/body pair.      `correlation_id` is included

### Community 156 - "Knowledge Base Sources"
Cohesion: 0.40
Nodes (4): get_current_time(), Returns the current time in H:MM AM/PM format., Searches Wikipedia for information on the given query., search_wikipedia()

### Community 157 - "Knowledge Base Sources"
Cohesion: 0.40
Nodes (4): main(), Alternative function to run a custom scenario with user input. This…, Main function to run the ethical hacking agent., run_custom_scenario()

### Community 162 - "Misc Utilities"
Cohesion: 0.50
Nodes (3): float, Confidence, Validated confidence score: 0.0–1.0.

### Community 163 - "Frontend Package"
Cohesion: 0.50
Nodes (3): name, private, version

### Community 167 - "Plugin System"
Cohesion: 0.83
Nodes (4): network/recon capability, network/vuln-scan capability, Nmap Port Scanner Plugin, Network VAPT Workflow

### Community 168 - "Kaggle Download Script"
Cohesion: 0.67
Nodes (3): BATCH, run_one(), download.sh script

## Knowledge Gaps
- **337 isolated node(s):** `severityConfig`, `statusOptions`, `roleConfig`, `BadgeProps`, `buttonVariants` (+332 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **98 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ApiKey` connect `Plugin System` to `Auth & API Keys`?**
  _High betweenness centrality (0.110) - this node is a cross-community bridge._
- **Why does `SecurityFinding` connect `Finding Engine` to `Finding Engine`, `AI Gateway`, `Report Generation`, `Finding Engine`, `HTTPx Tooling`, `Risk Engine`, `Scan Orchestration`, `Risk Engine`, `Trivy Tooling`, `AI Gateway`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `BaseModel` connect `Scan Orchestration` to `Finding Engine`, `Finding Engine`, `Plugin System`, `Plugin System`, `Plugin System`, `Misc Utilities`, `Plugin System`, `Plugin System`, `Planner Agent`, `Misc Utilities`, `Auth & API Keys`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 34 inferred relationships involving `SecurityFinding` (e.g. with `ContextBuilder` and `FindingContextPayload`) actually correct?**
  _`SecurityFinding` has 34 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `MembershipRepository` (e.g. with `ApiKeyCreate` and `ApiKeyCreateResponse`) actually correct?**
  _`MembershipRepository` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 38 inferred relationships involving `Container` (e.g. with `ContextBuilder` and `NullContextBuilder`) actually correct?**
  _`Container` has 38 INFERRED edges - model-reasoned connections that need verification._
- **What connects `severityConfig`, `statusOptions`, `roleConfig` to the rest of the system?**
  _337 weakly-connected nodes found - possible documentation gaps or missing edges._