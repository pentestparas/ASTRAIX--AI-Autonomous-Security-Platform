# Graph Report - .  (2026-07-23)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2218 nodes · 4641 edges · 162 communities (115 shown, 47 thin omitted)
- Extraction: 80% EXTRACTED · 20% INFERRED · 0% AMBIGUOUS · INFERRED: 920 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4f236374`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- AssessRequest
- assessments.py
- projects/page.tsx
- Enum
- AI-SecOS Core
- ScannerExecutor
- FindingNormalizer
- StaticRiskSignalProvider
- v1/auth.py
- PromptManager
- Any
- [id]/page.tsx
- Workflow
- organizations.py
- DefaultWorkflowEngine
- api.ts
- ToolRegistry
- DefaultTaskPlanner
- AIGateway
- PluginExecutionRequest
- SecurityFinding
- ProviderManager
- VAPTOutputParser
- LyrieAIAgent
- RoleName
- FastAPI
- VAPTExecutor
- SystemStatus.tsx
- str
- devDependencies
- core/auth.py
- dependencies
- BaseSettings
- Finding Engine
- BasePlugin
- datetime
- DefaultFindingDeduplicator
- vapt/models.py
- vapt/routes.py
- EventDispatcher
- MembershipRepository
- compilerOptions
- PluginManifest
- NullReportEngine
- ApiKeyRepository
- AsyncSession
- UserRepository
- VAPTScanResult
- .run_scan
- ToolCapability
- VAPTExecutor
- _MutableContainer
- PluginRegistry
- index.ts
- CapabilityRegistry
- MetricsRegistry
- Base
- ProjectRepository
- PluginLoader
- PlatformError
- value_objects.py
- BaseModel
- plugins.py
- get_container
- VAPTTool
- httpx/main.py
- app/main.py
- schemas/assessment.py
- nmap/main.py
- configure_logging
- results.py
- findings.py
- PluginManifest
- stream.py
- OrganizationRepository
- ScanRequest
- plugin_system/manifest.py
- Container
- get_correlation_id
- scripts
- app/schemas/__init__.py
- backend/tests/conftest.py
- _normalize_one
- m2_demo.py
- HTTPX Scanner Plugin
- ApiClient
- run_nuclei_scan
- run_semgrep_scan
- run_subfinder
- run_trivy_scan
- _map_error
- schemas/base.py
- env.py
- Sidebar.tsx
- load_manifest
- AstraIX Docker Compose
- Technology Stack
- app/layout.tsx
- ai_secos_core/tests/conftest.py
- core/logging.py
- package.json
- Any
- .eslintrc.json
- ai_gateway/__init__.py
- api_platform/__init__.py
- ai_secos_core/config/__init__.py
- capabilities/__init__.py
- Cloud Security Posture Assessment
- Static Application Security Testing
- constants.py
- eslint
- finding_engine/__init__.py
- next.config.js
- next-env.d.ts
- next
- @radix-ui/react-dropdown-menu
- @radix-ui/react-progress
- react-hook-form
- zustand
- postcss
- @testing-library/react
- infrastructure/__init__.py
- plugin_system/__init__.py
- report_engine/__init__.py
- risk_engine/__init__.py
- runtime/__init__.py
- shared/__init__.py
- start-dev.sh
- ApiKeyCreate
- Product Vision
- MembershipCreate
- MembershipUpdate
- Orchestrator
- Organization
- OrganizationCreate
- OrganizationUpdate
- Plugin SDK Schema
- Project
- ProjectCreate
- ProjectUpdate
- Prompt Templates
- Operational Rules
- User

## God Nodes (most connected - your core abstractions)
1. `SecurityFinding` - 75 edges
2. `BaseModel` - 52 edges
3. `MembershipRepository` - 50 edges
4. `Container` - 47 edges
5. `ProjectRepository` - 47 edges
6. `ApiKeyRepository` - 46 edges
7. `_MutableContainer` - 44 edges
8. `OrganizationRepository` - 44 edges
9. `UserRepository` - 39 edges
10. `build_default_container()` - 34 edges

## Surprising Connections (you probably didn't know these)
- `FindingOut` --inherits--> `BaseModel`  [EXTRACTED]
  plugins/core/plugin-sdk/base.py → backend/app/models/base.py
- `PluginError` --inherits--> `BaseModel`  [EXTRACTED]
  plugins/core/plugin-sdk/base.py → backend/app/models/base.py
- `PluginOutput` --inherits--> `BaseModel`  [EXTRACTED]
  plugins/core/plugin-sdk/base.py → backend/app/models/base.py
- `PluginSchema` --inherits--> `BaseModel`  [EXTRACTED]
  plugins/core/plugin-sdk/base.py → backend/app/models/base.py
- `AIGateway` --uses--> `ContextBuilder`  [INFERRED]
  backend/ai_secos_core/ai_gateway/gateway.py → backend/ai_secos_core/ai_gateway/context.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Three-Layer Platform Model** — engineering_architecture_ai_secos_core, engineering_architecture_applications, engineering_architecture_plugins [EXTRACTED 1.00]
- **Capability Resolution Chain** — engineering_architecture_applications, engineering_architecture_capability, engineering_architecture_workflow, engineering_architecture_plugins, engineering_architecture_security_finding [EXTRACTED 1.00]
- **Asset Discovery Workflow Plugin Composition** — workflows_asset_discovery, plugins_subfinder_plugin, plugins_httpx_plugin, finding_engine, report_engine [EXTRACTED 1.00]
- **Cloud Posture Workflow Plugin Composition** — workflows_cloud_posture, plugins_trivy_plugin, finding_engine, report_engine [EXTRACTED 1.00]
- **Network VAPT Workflow Plugin Composition** — workflows_network_vapt, plugins_nmap_plugin, plugins_nuclei_plugin, finding_engine, report_engine [EXTRACTED 1.00]
- **Web VAPT Workflow Plugin Composition** — workflows_web_vapt, plugins_httpx_plugin, plugins_nuclei_plugin, finding_engine, report_engine [EXTRACTED 1.00]
- **AstraIX Platform Infrastructure** — services_postgres, services_redis, services_backend, services_frontend [EXTRACTED 1.00]
- **Shared Risk Scoring Component** — finding_engine, workflows_asset_discovery, workflows_cloud_posture, workflows_code_audit, workflows_discovery, workflows_network_vapt, workflows_web_vapt [EXTRACTED 1.00]
- **Shared Reporting Component** — report_engine, workflows_asset_discovery, workflows_cloud_posture, workflows_code_audit, workflows_discovery, workflows_network_vapt, workflows_web_vapt [EXTRACTED 1.00]
- **Plugin SDK Schema Defines Plugin Structure** — plugins_core_plugin_sdk_plugin_sdk, plugins_httpx_plugin, plugins_nmap_plugin, plugins_nuclei_plugin, plugins_semgrep_plugin, plugins_subfinder_plugin, plugins_trivy_plugin [EXTRACTED 1.00]

## Communities (162 total, 47 thin omitted)

### Community 0 - "AssessRequest"
Cohesion: 0.07
Nodes (55): assess(), AssessRequest, AssessResponse, _bootstrap(), FindingSummary, list_capabilities(), FastAPI app for the AI-SecOS Core Web UI.  Run with: uvicorn api:app --reload --, Convert 'https://example.com:443' to 'asset_example_com'. (+47 more)

### Community 1 - "assessments.py"
Cohesion: 0.05
Nodes (42): Assessment, AssessmentCreate, Asset, cancel_assessment(), create_assessment(), get_assessment(), list_assessments(), AsyncSession (+34 more)

### Community 2 - "projects/page.tsx"
Cohesion: 0.06
Nodes (43): react, ScanResult, scanTypesInfo, Finding, Project, riskColors, ScanResult, scanTypes (+35 more)

### Community 3 - "Enum"
Cohesion: 0.09
Nodes (40): CapabilityAlreadyRegisteredError, CapabilityNotFoundError, CapabilityResolverError, Capability-specific error types., Raised when attempting to register a duplicate capability., Raised when capability resolution fails (missing workflow, etc.)., Raised when a capability is not found in the registry., CapabilityLoader (+32 more)

### Community 4 - "AI-SecOS Core"
Cohesion: 0.05
Nodes (48): System Architecture, AI Gateway Module, AI-SecOS Core, Applications Layer, Capability Abstraction, Infrastructure Module, Domain Models Module, Normalizer Module (+40 more)

### Community 5 - "ScannerExecutor"
Cohesion: 0.10
Nodes (36): get_scanner_executor(), Scanner Executor Service  Enterprise-grade scanner execution with: - Async tool, Execute a single tool., Create appropriate executor for scan request., Get the global scanner executor instance., Main scanner execution service.      Features:     - Multi-tool execution with D, ScannerExecutor, AstraIX Security Scanner Module  Enterprise-grade security scanning engine that (+28 more)

### Community 6 - "FindingNormalizer"
Cohesion: 0.08
Nodes (27): FindingCorrelator, NoopFindingCorrelator, Finding Correlator — the contract + the no-op default.  Correlators detect patte, Adds correlation metadata to findings., Identity correlator. The default at Milestone 1., DefaultFindingEngine, FindingEngine, FindingEngineConfig (+19 more)

### Community 7 - "StaticRiskSignalProvider"
Cohesion: 0.08
Nodes (24): DefaultRiskEngine, _noop_severity_to_score(), NoopRiskEngine, Risk Engine — pipeline orchestrator and entry points.  Two implementations are s, Identity: score derived directly from canonical severity.      Used in tests and, A scored finding (or a typed wrapper around a SecurityFinding)., Engine port: score one or more canonical findings., Score each canonical finding. (+16 more)

### Community 8 - "v1/auth.py"
Cohesion: 0.10
Nodes (38): create_project(), delete_organization(), delete_project(), get_api_key_repo(), get_membership_repo(), get_org_repo(), get_organization(), get_project() (+30 more)

### Community 9 - "PromptManager"
Cohesion: 0.07
Nodes (22): _InMemoryPromptManager, PromptManager, PromptTemplate, PromptVersionError, Prompt Manager — versioned prompt templates.  A `PromptTemplate` is a parameteri, Raised when a requested `prompt_id` / version combination is unknown., One version of one prompt.      The text uses stdlib `Template` semantics ($-sty, Resolved-source-of-truth for prompt templates. (+14 more)

### Community 10 - "Any"
Cohesion: 0.09
Nodes (29): Convenience: flatten to a dict for string substitution., Any, FindingFingerprint, _confidence(), _extract_items(), make_httpx_input(), _normalize_one(), _normalize_tech() (+21 more)

### Community 11 - "[id]/page.tsx"
Cohesion: 0.13
Nodes (24): statusConfig, severityConfig, statusOptions, findingsApi, cn(), roleConfig, Asset, Finding (+16 more)

### Community 12 - "Workflow"
Cohesion: 0.09
Nodes (29): CancelledError, Cancellation token for running tasks/plans.  The platform-wide cancellation cont, A typed alias for cancellation that originates from the platform., PlannedExecution, Task Planner — the dynamic heart of the platform.  Per ARCHITECTURE.md:    - Wor, Top-level knobs for the planner., Outcome of one full plan run., Schedule and execute a Workflow as a DAG. (+21 more)

### Community 13 - "organizations.py"
Cohesion: 0.12
Nodes (33): create_api_key(), create_project(), delete_api_key(), delete_organization(), delete_project(), get_api_key(), get_organization(), get_project() (+25 more)

### Community 14 - "DefaultWorkflowEngine"
Cohesion: 0.10
Nodes (19): CapabilityResolver, Capability Resolver.  Resolves a `Capability` request into a concrete execution, Validate inputs against the capability's input schema (lightweight).          Pe, Raised when capability resolution fails., A Capability fully resolved to executable Workflows., Resolves Capabilities to WorkflowRecords ready for the Task Planner., ResolutionError, ResolvedCapability (+11 more)

### Community 15 - "api.ts"
Cohesion: 0.08
Nodes (13): apiKeysApi, assessmentsApi, assetsApi, authApi, healthApi, membershipsApi, organizationsApi, pluginsApi (+5 more)

### Community 16 - "ToolRegistry"
Cohesion: 0.09
Nodes (20): get_tool_registry(), Enum, str, Kali Linux Security Tool Registry  Comprehensive registry of security tools avai, Tool categories matching VAPT workflow., Metadata about a security tool., Default configuration for a tool., Registry for managing security tools. (+12 more)

### Community 17 - "DefaultTaskPlanner"
Cohesion: 0.15
Nodes (12): CancellationToken, Lightweight, async-friendly cancellation., NoopTaskExecutor, Task Executor — runs a Task.  A planner produces Tasks; the executor is what run, Run a single Task and emit a result., Default at Milestone 1.      The executor performs the bare minimum: a `result`-, TaskExecutor, TaskRunResult (+4 more)

### Community 18 - "AIGateway"
Cohesion: 0.11
Nodes (20): AIGateway, AI Gateway — composed pipeline.  Pipeline order (matches Architecture):    1. Ro, Single entry point for AI reasoning tasks.      Implementations are responsible, AIRequest, AIResponse, AITokenUsage, NullProvider, AI Provider port.  A Provider is anything that can take a prompt + structured in (+12 more)

### Community 19 - "PluginExecutionRequest"
Cohesion: 0.14
Nodes (21): NoopTaskExecutor, PluginExecutionRequest, PluginExecutionResult, PluginExecutionStatus, PluginExecutor, Plugin Executor: drives the subprocess lifecycle.  Owns the *mechanics*:    - Re, Drive asyncio's subprocess for one plugin invocation., Convert non-JSON values to strings, swallowing exceptions. (+13 more)

### Community 20 - "SecurityFinding"
Cohesion: 0.10
Nodes (18): ContextBuilder, FindingContextPayload, NullContextBuilder, Context Builder — assembles what's fed into a prompt.  Pre-AI responsibilities:, What the AI sees. Pre-serialization.      The AI Gateway *never* receives the ra, Build a `FindingContextPayload` from typed inputs., Default at Milestone 1.      Performs no compression or redaction. A future mile, DefaultAIGateway (+10 more)

### Community 21 - "ProviderManager"
Cohesion: 0.11
Nodes (16): ProviderAlreadyRegisteredError, ProviderManager, ProviderNotFoundError, Provider Manager.  The Manager owns the lifecycle of providers. Applications nev, Thread-safe registry of providers.      The Manager is the *only* place provider, AIProvider, Concrete providers (OpenAI/Anthropic/...) implement this., ModelRouter (+8 more)

### Community 22 - "VAPTOutputParser"
Cohesion: 0.11
Nodes (15): Finding, Parse Nmap text output as fallback., Map Nikto OSVDB ID to severity., Parse Nuclei JSON output to findings., Parse SQLMap JSON output to findings., Map tool-specific severity string to Severity enum., Parse Gobuster JSON output to findings., Parse FFUF JSON output to findings. (+7 more)

### Community 23 - "LyrieAIAgent"
Cohesion: 0.10
Nodes (15): LyrieAIAgent, Lyrie AI Agent executor for autonomous security operations.      Features:     -, Run 7-phase autonomous pentest.          Args:             target: URL or local, Scan URL or file for security issues.          Checks:         - Security header, AI red-team an LLM endpoint.          Strategies:         - crescendo: gradual e, Calculate CVSS v3.1 score from vector.          Args:             vector: CVSS v, Verify agent identity using Agent Trust Protocol.          Args:             age, Display ATP compliance badge.          Returns:             dict with badge info (+7 more)

### Community 24 - "RoleName"
Cohesion: 0.17
Nodes (28): RoleName, PyEnum, ApiKeyBase, ApiKeyCreate, ApiKeyCreateResponse, ApiKeyRead, MembershipBase, MembershipCreate (+20 more)

### Community 25 - "FastAPI"
Cohesion: 0.10
Nodes (18): lifespan(), Application startup/shutdown., get_dashboard_stats(), list_capabilities(), UUID, List available security scan capabilities., Get dashboard statistics for an organization., close_db() (+10 more)

### Community 26 - "VAPTExecutor"
Cohesion: 0.13
Nodes (17): ExternalTool, Any, ScanRequest, ScanResult, Execute a complete security scan., Get tools for a given capability., Enterprise VAPT Execution Engine      Features:     - Multi-platform support (Ka, Execute a single tool and return parsed findings. (+9 more)

### Community 27 - "SystemStatus.tsx"
Cohesion: 0.12
Nodes (17): RecentAssessments(), StatCardProps, StatsCards(), resources, ResourceUsage, services, ServiceStatus, SystemStatus() (+9 more)

### Community 28 - "str"
Cohesion: 0.09
Nodes (19): PluginType, Where a risk axis got its number., RiskFactorSource, Asset, AssetCriticality, AssetIdentifier, AssetInventory, AssetType (+11 more)

### Community 29 - "devDependencies"
Cohesion: 0.07
Nodes (27): autoprefixer, eslint-config-next, devDependencies, autoprefixer, eslint-config-next, jsdom, prettier, prettier-plugin-tailwindcss (+19 more)

### Community 30 - "core/auth.py"
Cohesion: 0.15
Nodes (23): api_key_header, decode_token(), get_current_active_user(), get_current_superuser(), get_current_user(), get_role_permissions(), get_user_organizations(), get_user_projects() (+15 more)

### Community 31 - "dependencies"
Cohesion: 0.08
Nodes (25): axios, class-variance-authority, clsx, date-fns, dependencies, axios, class-variance-authority, clsx (+17 more)

### Community 32 - "BaseSettings"
Cohesion: 0.11
Nodes (22): BaseSettings, get_settings(), Application settings loaded from env vars or .env., Settings, AIGatewaySettings, FindingEngineSettings, load_settings(), ObservabilitySettings (+14 more)

### Community 33 - "Finding Engine"
Cohesion: 0.13
Nodes (25): Finding Engine, web/discovery capability, network/recon capability, network/vuln-scan capability, api/security capability, web/vuln-scan capability, HTTP Probe (httpx) Plugin, Nmap Port Scanner Plugin (+17 more)

### Community 34 - "BasePlugin"
Cohesion: 0.10
Nodes (17): BasePlugin, FindingOut, PluginError, PluginOutput, PluginSchema, Parse stdin: str → dict., Structured logging accessible to orchestrator., Schema for plugin I/O, described in plugin.yml. (+9 more)

### Community 35 - "datetime"
Cohesion: 0.11
Nodes (18): TimestampMixin, UUIDMixin, datetime, Nmap Plugin — normalizer.  Converts raw `nmap` output into canonical `SecurityFi, _categorize(), Nuclei Plugin — normalizer.  Converts raw `nuclei` output into canonical `Securi, Map nuclei tags to finding category., Subfinder Plugin — normalizer.  Converts raw `subfinder` output into canonical ` (+10 more)

### Community 36 - "DefaultFindingDeduplicator"
Cohesion: 0.11
Nodes (13): DefaultFindingDeduplicator, _max_or_none(), _merge(), _promote_severity(), Deduplication: collapsing equivalent findings.  Two findings with the same finge, Merge a re-observed finding with its prior canonical record.      Strategy:, In-memory implementation.      Suitable for single-process Milestone 1 / Milesto, DefaultFindingFingerprinter (+5 more)

### Community 37 - "vapt/models.py"
Cohesion: 0.17
Nodes (17): get_vapt_executor(), VAPT Executor  Executes security tools inside Docker containers (Kali Linux). Pr, Resolve tools to execute., ASTRAIX VAPT Module  AI-Orchestrated Vulnerability Assessment & Penetration Test, Enum, str, VAPT Data Models  Core data structures for VAPT operations., Request for a VAPT scan. (+9 more)

### Community 38 - "vapt/routes.py"
Cohesion: 0.15
Nodes (21): get_vapt_orchestrator(), get_assessment(), list_tools(), AsyncSession, BaseModel, UUID, quick_scan(), VAPT API Routes  Fast API endpoints for VAPT operations with database persistenc (+13 more)

### Community 39 - "EventDispatcher"
Cohesion: 0.11
Nodes (12): ProgressTicker, Streaming-aware Plugin Executor.  Wraps the base `PluginExecutor` and emits `plu, Wraps a PluginExecutor to emit streaming events.      The wrapper preserves the, Background ticker to emit periodic plugin.progress events.      Started when a p, StreamingPluginExecutor, DomainEvent, EventDispatcher, InProcessEventDispatcher (+4 more)

### Community 40 - "MembershipRepository"
Cohesion: 0.16
Nodes (14): create_organization(), invite_member(), MembershipCreate, OrganizationCreate, Register a new user and optionally create an organization., Create a new organization., Invite a user to organization or project., register() (+6 more)

### Community 41 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowJs, baseUrl, esModuleInterop, forceConsistentCasingInFileNames, incremental, isolatedModules, jsx (+13 more)

### Community 42 - "PluginManifest"
Cohesion: 0.13
Nodes (12): PluginManifest, Validate entrypoint format for the declared runtime.          Examples:, Typed representation of a `plugin.yml` declaration., PluginAlreadyRegisteredError, PluginNotFoundError, PluginRecord, PluginRegistry, Plugin Registry: what exists and how it is looked up.  The Registry owns *record (+4 more)

### Community 43 - "NullReportEngine"
Cohesion: 0.19
Nodes (17): _ai_comment_placeholder(), _build_section(), _findings_section(), NullReportEngine, Report Engine — implementation.  At Milestone 1, only the JSON/Markdown default, Render reports from findings + risk scores., JSON/Markdown default at Milestone 1.      Produces deterministic artefacts usin, ReportEngine (+9 more)

### Community 44 - "ApiKeyRepository"
Cohesion: 0.18
Nodes (14): ApiKey, ApiKeyCreate, ApiKeyCreateResponse, ApiKeyResponse, create_api_key(), MembershipResponse, OrganizationResponse, ProjectCreate (+6 more)

### Community 45 - "AsyncSession"
Cohesion: 0.14
Nodes (12): AsyncSession, get_session(), Database session dependency., BaseRepository, Repository pattern for data access.  Each repository:   - Wraps SQLAlchemy queri, Generic repository for any model., List with pagination and optional filters., Count records with optional filters. (+4 more)

### Community 46 - "UserRepository"
Cohesion: 0.16
Nodes (15): login(), login_json(), OAuth2 compatible login for Swagger UI., JSON-based login for frontend applications., Refresh access token., refresh_token(), Token, UserLogin (+7 more)

### Community 47 - "VAPTScanResult"
Cohesion: 0.14
Nodes (9): Result from a VAPT scan., VAPTScanResult, AIOrchestrator, Any, Generate AI insights on scan results., AI orchestrator for VAPT.          Responsibilities:     - Analyze target to det, Analyze target and run appropriate scan., Analyze target to understand what it is. (+1 more)

### Community 48 - ".run_scan"
Cohesion: 0.12
Nodes (12): Any, Finding, ScanRequest, ScanResult, Get tools for a scan request., Get default tools for a capability., Build execution context for tools., Remove duplicate findings based on fingerprint. (+4 more)

### Community 49 - "ToolCapability"
Cohesion: 0.14
Nodes (16): Check which tools are available in the environment., Check if a specific tool is available., Get availability status of all tools., ToolAvailabilityChecker, Enum, str, Scanner Models  Enterprise-grade data models for security scanning operations. A, CVSS-based severity levels. (+8 more)

### Community 50 - "VAPTExecutor"
Cohesion: 0.15
Nodes (8): Parse tool output to findings., VAPT executor using Docker containers.      Tools run inside isolated Kali Linux, Execute demo scan with realistic sample findings., Execute a complete VAPT scan., Check if Docker is available., VAPTExecutor, A security finding from VAPT scan., VAPTFinding

### Community 51 - "_MutableContainer"
Cohesion: 0.15
Nodes (14): build_default_container(), _MutableContainer, Dependency Injection container.  Uses DI’y to wire the entire platform without m, # TODO: Lookup normalizer + register, Mutable (thread-safe) wiring harness., Safely edit mutable values., Return a frozen copy ready for consumption., Wire default implementations for production runtime. (+6 more)

### Community 52 - "PluginRegistry"
Cohesion: 0.14
Nodes (11): get_plugin_registry(), PluginInstance, PluginRegistry, Execute plugin subprocess. Returns (output, error)., Run subprocess synchronously. Returns (stdout, stderr)., Get manifests of all registered plugins., Singleton plugin registry., Loaded plugin: metadata + path. (+3 more)

### Community 53 - "index.ts"
Cohesion: 0.11
Nodes (18): ApiKey, ApiKeyCreateResponse, ApiResponse, Capability, DashboardStats, FindingSummary, LoginRequest, Membership (+10 more)

### Community 54 - "CapabilityRegistry"
Cohesion: 0.16
Nodes (6): CapabilityVersion, Semantic version (major.minor.patch)., CapabilityRegistry, Capability Registry — typed lookup and lifecycle.  Thread-safe in-memory registr, Thread-safe registry of `Capability` instances keyed by id+version.      Capabil, Capability

### Community 55 - "MetricsRegistry"
Cohesion: 0.15
Nodes (9): Counter, Histogram, MetricsRegistry, _NoopCounter, _NoopHistogram, Metrics primitives (stubs at Milestone 1).  These are typed protocols so service, Monotonically increasing value, optionally labelled., Distribution value, optionally labelled. (+1 more)

### Community 56 - "Base"
Cohesion: 0.34
Nodes (16): Base, TimestampMixin, UUIDMixin, DeclarativeBase, Mapped, Assessment, Asset, Finding (+8 more)

### Community 58 - "PluginLoader"
Cohesion: 0.17
Nodes (9): Path, LoadedPlugin, PluginLoader, PluginLoaderError, Plugin Loader: read manifests from disk → PluginRecords.  The Loader is the *onl, A loader-level result wrapping a successfully parsed manifest., Filesystem-based plugin loader.      The exact YAML layout is opaque outside thi, Walk the plugins root; return all parseable plugin records.          Directories (+1 more)

### Community 59 - "PlatformError"
Cohesion: 0.17
Nodes (13): platform_error_to_http_response(), PlatformErrorResponse, Map platform errors → HTTP responses.  FastAPI exception handler in `platform/`, Convert a PlatformError to a status/body pair.      `correlation_id` is included, ConfigurationError, FindingEngineError, PlatformError, PluginError (+5 more)

### Community 60 - "value_objects.py"
Cohesion: 0.12
Nodes (12): float, CapabilityVersion, ComplianceTag, Confidence, Reusable value objects (the platform's vocabulary).  These are the typed shapes, A compliance framework mapping., Validated confidence score: 0.0–1.0., SemVer-style version (integer triple). (+4 more)

### Community 61 - "BaseModel"
Cohesion: 0.21
Nodes (13): BaseModel, FindingOut, PluginError, PluginManifest, PluginOutput, PluginStatus, PluginRunResult, Result of running a plugin. (+5 more)

### Community 62 - "plugins.py"
Cohesion: 0.19
Nodes (13): PluginRegistry, _count_by_capability(), _count_by_type(), get_plugin(), list_plugins(), plugins_info(), List all registered plugins., Get plugin details by ID. (+5 more)

### Community 63 - "get_container"
Cohesion: 0.16
Nodes (12): get_container(), get_settings(), Dependency providers for FastAPI routes., FastAPI dependency: immutable container wired to pathOps., Shortcut: typed settings., health(), FastAPI transport: health, ready, version.  All other API routes beyond these th, Endpoint health; always 200. (+4 more)

### Community 64 - "VAPTTool"
Cohesion: 0.15
Nodes (10): Run a tool inside a Docker container., Build command for Docker execution., Enforce rate limiting., BaseModel, Health status of a VAPT tool., Security tool definition., Build full command with target., ToolHealth (+2 more)

### Community 65 - "httpx/main.py"
Cohesion: 0.22
Nodes (13): Headers, _add(), _detect_cdn(), _detect_technologies(), _extract_title(), main(), probe_target(), Extract version from header like 'nginx/1.21.6'. (+5 more)

### Community 66 - "app/main.py"
Cohesion: 0.18
Nodes (11): health_check(), AstraIX Security Analyst - Main Application  Entry point for the FastAPI applica, Root endpoint: health/status overview., Basic liveness check., Readiness check (validates dependencies)., readiness_check(), root(), AsyncClient (+3 more)

### Community 67 - "schemas/assessment.py"
Cohesion: 0.29
Nodes (8): BaseSchema, AssessmentBase, AssessmentCreate, AssessmentRead, AssessmentSummary, Lightweight assessment summary., FindingBase, FindingRead

### Community 68 - "nmap/main.py"
Cohesion: 0.23
Nodes (12): Element, build_nmap_command(), main(), _parse_host(), parse_nmap_xml(), _parse_port(), Parse a single host element., Parse a port element. (+4 more)

### Community 69 - "configure_logging"
Cohesion: 0.22
Nodes (12): Formatter, configure_logging(), _console_formatter(), _CorrelationIdFilter, get_logger(), _json_formatter(), Correlation-aware structured logging.  Default backend is `logging` to avoid har, Inject the active correlation id into every record. (+4 more)

### Community 70 - "results.py"
Cohesion: 0.19
Nodes (10): Result, fail(), Failure, is_failure(), is_ok(), ok(), Result type (Rust/Python-port idiom) for explicit success/failure.  Used by serv, Successful outcome carrying a value. (+2 more)

### Community 71 - "findings.py"
Cohesion: 0.22
Nodes (9): FindingUpdate, delete_finding(), filters__dict(), get_finding(), list_findings(), List findings with pagination., Helper to allow scoped filters., Update finding status / fields. (+1 more)

### Community 72 - "PluginManifest"
Cohesion: 0.20
Nodes (6): Translate the decision + manifest into a safe subprocess argv.          The inte, Plugin Validator: schema, capability, and permission checks.  The Validator is t, Tiny subset of JSON Schema type matching for type-checking most params., _type_match(), ValidationResult, PluginManifest

### Community 73 - "stream.py"
Cohesion: 0.26
Nodes (10): emit_plugin_completed(), emit_plugin_finding(), emit_plugin_progress(), emit_plugin_started(), PluginCompletedPayload, PluginFindingPayload, PluginProgressPayload, PluginStartedPayload (+2 more)

### Community 74 - "OrganizationRepository"
Cohesion: 0.27
Nodes (5): Permission, str, Permission identifiers., OrganizationRepository, Organization

### Community 75 - "ScanRequest"
Cohesion: 0.22
Nodes (9): AssessmentStatus, Enum, str, Orchestrator Service  Coordinates plugins, assessments, and findings.  Responsib, Assessment lifecycle., Any, Request to execute one or more security tools against a target., Get merged config for a specific tool. (+1 more)

### Community 76 - "plugin_system/manifest.py"
Cohesion: 0.20
Nodes (10): PluginCapabilityRequirement, PluginInputSchema, PluginOutputSchema, PluginResourceLimits, PluginSandboxPolicy, Plugin manifest (the typed shape of a `plugin.yml`).  Schema is intentionally st, A Capability the Plugin requires from the platform., Hard limits applied by the Sandbox. (+2 more)

### Community 77 - "Container"
Cohesion: 0.24
Nodes (8): build_app(), lifespan(), FastAPI app factory.  Binds the DI container to the web transport.  - Health/rea, Start/stop lifetime management., Create the FastAPI application.      Mostly configures routing + middleware; DI, Container, At boot, walk the plugins root and populate:           - plugin registry, The exposed container interface.

### Community 78 - "get_correlation_id"
Cohesion: 0.22
Nodes (8): CorrelationId, bind_correlation_id(), Set the active correlation id for subsequent logs., LogRecord, get_correlation_id(), Correlation id context.  Every critical action (workflow, plugin exec, AI call), Return the current correlation id, creating one if absent.      Use only at entr, set_correlation_id()

### Community 79 - "scripts"
Cohesion: 0.20
Nodes (10): scripts, build, dev, format, lint, start, test, test:coverage (+2 more)

### Community 80 - "app/schemas/__init__.py"
Cohesion: 0.28
Nodes (6): BaseSchema, PaginatedResponse, Base schema with ORM mode enabled., Standard success response wrapper., Paginated results wrapper., ResponseSchema

### Community 81 - "backend/tests/conftest.py"
Cohesion: 0.22
Nodes (7): event_loop(), Pytest configuration and fixtures., mock_registry(), mock_settings(), Override default event loop., Mock settings for tests., Mock plugin registry.

### Community 82 - "_normalize_one"
Cohesion: 0.28
Nodes (7): _categorize_semgrep(), _extract_tags(), _normalize_one(), Semgrep Plugin — normalizer.  Converts raw `semgrep` output into canonical `Secu, Categorize semgrep finding based on check_id and metadata., Extract tags from semgrep metadata., Normalize a single semgrep finding.

### Community 83 - "m2_demo.py"
Cohesion: 0.25
Nodes (6): _noop_dedup(), Milestone 2 End-to-End Demo — Capability -> Workflow -> Plugin -> Findings.  Dem, Minimal in-memory deduplicator for M2 demo only., M2 End-to-End test.  Validates the vertical slice: Capability → Plugin → Normali, The full M2 path executes end-to-end and emits a summary., test_m2_demo_runs()

### Community 84 - "HTTPX Scanner Plugin"
Cohesion: 0.25
Nodes (8): Network Vulnerability Assessment, External Asset Discovery, Web Discovery, Web Application Security Assessment, HTTPX Scanner Plugin, Nmap Scanner Plugin, Nuclei Scanner Plugin, Subfinder Scanner Plugin

### Community 86 - "run_nuclei_scan"
Cohesion: 0.36
Nodes (7): build_nuclei_command(), main(), parse_nuclei_json(), Execute nuclei and return parsed results., Build nuclei command arguments., Parse nuclei JSON output lines., run_nuclei_scan()

### Community 87 - "run_semgrep_scan"
Cohesion: 0.36
Nodes (7): build_semgrep_command(), main(), parse_semgrep_results(), Build semgrep command arguments., Parse semgrep JSON output., Execute semgrep and return parsed results., run_semgrep_scan()

### Community 88 - "run_subfinder"
Cohesion: 0.36
Nodes (7): build_subfinder_command(), main(), parse_subfinder_json(), Build subfinder command arguments., Parse subfinder JSON output lines., Execute subfinder and return parsed results., run_subfinder()

### Community 89 - "run_trivy_scan"
Cohesion: 0.36
Nodes (7): build_trivy_command(), main(), parse_trivy_results(), Build trivy command arguments., Parse trivy JSON output., Execute trivy and return parsed results., run_trivy_scan()

### Community 90 - "_map_error"
Cohesion: 0.33
Nodes (6): _map_error(), Convert platform errors → HTTP responses.  FastAPI exception handlers delegate t, Bind platform error handler., Shared mapping logic., register_exception_handlers(), _safe()

### Community 91 - "schemas/base.py"
Cohesion: 0.43
Nodes (4): BaseSchema, ErrorResponse, PaginatedResponse, ResponseSchema

### Community 92 - "env.py"
Cohesion: 0.40
Nodes (4): do_run_migrations(), run_async_migrations(), run_migrations_online(), Connection

### Community 93 - "Sidebar.tsx"
Cohesion: 0.40
Nodes (3): navigation, settingsNav, Sidebar()

### Community 94 - "load_manifest"
Cohesion: 0.40
Nodes (5): load_manifest(), PluginLimits, PluginManifest, PluginSchema, Load a plugin.json from a directory.

### Community 95 - "AstraIX Docker Compose"
Cohesion: 0.60
Nodes (5): AstraIX Docker Compose, Backend API Service, Frontend Service, PostgreSQL Service, Redis Service

### Community 96 - "Technology Stack"
Cohesion: 0.40
Nodes (5): Technology Stack, AI Tech Stack, Backend Tech Stack, DevOps Tech Stack, Frontend Tech Stack

### Community 100 - "package.json"
Cohesion: 0.50
Nodes (3): name, private, version

## Knowledge Gaps
- **184 isolated node(s):** `UUIDMixin`, `TimestampMixin`, `nextConfig`, `severityConfig`, `statusOptions` (+179 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **47 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SecurityFinding` connect `SecurityFinding` to `AssessRequest`, `DefaultFindingDeduplicator`, `FindingNormalizer`, `StaticRiskSignalProvider`, `Any`, `NullReportEngine`, `_normalize_one`, `value_objects.py`, `BaseModel`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Why does `BaseModel` connect `BaseModel` to `AssessRequest`, `BasePlugin`, `schemas/assessment.py`, `datetime`, `findings.py`, `PluginManifest`, `plugin_system/manifest.py`, `Workflow`, `DefaultWorkflowEngine`, `app/schemas/__init__.py`, `PluginRegistry`, `SecurityFinding`, `Base`, `RoleName`, `schemas/base.py`, `value_objects.py`, `load_manifest`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Why does `build_default_container()` connect `_MutableContainer` to `BaseSettings`, `AssessRequest`, `DefaultFindingDeduplicator`, `configure_logging`, `FindingNormalizer`, `StaticRiskSignalProvider`, `EventDispatcher`, `NullReportEngine`, `Container`, `DefaultWorkflowEngine`, `DefaultTaskPlanner`, `AIGateway`, `PluginExecutionRequest`, `SecurityFinding`, `ProviderManager`, `PluginLoader`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Are the 34 inferred relationships involving `SecurityFinding` (e.g. with `ContextBuilder` and `FindingContextPayload`) actually correct?**
  _`SecurityFinding` has 34 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `MembershipRepository` (e.g. with `ApiKeyCreate` and `ApiKeyCreateResponse`) actually correct?**
  _`MembershipRepository` has 19 INFERRED edges - model-reasoned connections that need verification._
- **What connects `UUIDMixin`, `TimestampMixin`, `nextConfig` to the rest of the system?**
  _184 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `AssessRequest` be split into smaller, more focused modules?**
  _Cohesion score 0.06557377049180328 - nodes in this community are weakly interconnected._