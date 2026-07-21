# Graph Report - .  (2026-07-15)

## Corpus Check
- 212 files · ~63,371 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1771 nodes · 3873 edges · 117 communities (91 shown, 26 thin omitted)
- Extraction: 77% EXTRACTED · 23% INFERRED · 0% AMBIGUOUS · INFERRED: 901 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Plugin Schemas|Plugin Schemas]]
- [[_COMMUNITY_Metrics System|Metrics System]]
- [[_COMMUNITY_Context Building|Context Building]]
- [[_COMMUNITY_Assessment API|Assessment API]]
- [[_COMMUNITY_App Factory & Null Providers|App Factory & Null Providers]]
- [[_COMMUNITY_Workflow Engine|Workflow Engine]]
- [[_COMMUNITY_Architecture Concepts|Architecture Concepts]]
- [[_COMMUNITY_Frontend Package Config|Frontend Package Config]]
- [[_COMMUNITY_Task & Risk Types|Task & Risk Types]]
- [[_COMMUNITY_Frontend Dashboard Pages|Frontend Dashboard Pages]]
- [[_COMMUNITY_FastAPI Dependencies|FastAPI Dependencies]]
- [[_COMMUNITY_Platform Settings|Platform Settings]]
- [[_COMMUNITY_Plugin Loader|Plugin Loader]]
- [[_COMMUNITY_Risk Engine|Risk Engine]]
- [[_COMMUNITY_Organizations API|Organizations API]]
- [[_COMMUNITY_Assets & Sessions|Assets & Sessions]]
- [[_COMMUNITY_Frontend Project Pages|Frontend Project Pages]]
- [[_COMMUNITY_Capability Loader|Capability Loader]]
- [[_COMMUNITY_Projects API|Projects API]]
- [[_COMMUNITY_Security Scanner Plugins|Security Scanner Plugins]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 76|Community 76]]
- [[_COMMUNITY_Community 78|Community 78]]
- [[_COMMUNITY_Community 79|Community 79]]
- [[_COMMUNITY_Community 81|Community 81]]
- [[_COMMUNITY_Community 82|Community 82]]
- [[_COMMUNITY_Community 83|Community 83]]
- [[_COMMUNITY_Community 84|Community 84]]
- [[_COMMUNITY_Community 85|Community 85]]
- [[_COMMUNITY_Community 86|Community 86]]
- [[_COMMUNITY_Community 87|Community 87]]
- [[_COMMUNITY_Community 88|Community 88]]
- [[_COMMUNITY_Community 89|Community 89]]
- [[_COMMUNITY_Community 90|Community 90]]
- [[_COMMUNITY_Community 91|Community 91]]
- [[_COMMUNITY_Community 92|Community 92]]
- [[_COMMUNITY_Community 93|Community 93]]
- [[_COMMUNITY_Community 94|Community 94]]
- [[_COMMUNITY_Community 110|Community 110]]
- [[_COMMUNITY_Community 112|Community 112]]
- [[_COMMUNITY_Community 113|Community 113]]
- [[_COMMUNITY_Community 116|Community 116]]

## God Nodes (most connected - your core abstractions)
1. `SecurityFinding` - 75 edges
2. `BaseModel` - 69 edges
3. `RoleName` - 55 edges
4. `Container` - 47 edges
5. `_MutableContainer` - 44 edges
6. `MembershipRepository` - 35 edges
7. `build_default_container()` - 34 edges
8. `ProjectRepository` - 31 edges
9. `ApiKeyRepository` - 31 edges
10. `AssessRequest` - 30 edges

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
- **Three-Layer Platform Model** — architecture_ai_secos_core, architecture_applications, architecture_plugins [EXTRACTED 1.00]
- **Capability Resolution Chain** — architecture_applications, architecture_capability, architecture_workflow, architecture_plugins, architecture_security_finding [EXTRACTED 1.00]
- **Asset Discovery Workflow Plugin Composition** — workflows_asset_discovery, plugins_subfinder_plugin, plugins_httpx_plugin, finding_engine, report_engine [EXTRACTED 1.00]
- **Cloud Posture Workflow Plugin Composition** — workflows_cloud_posture, plugins_trivy_plugin, finding_engine, report_engine [EXTRACTED 1.00]
- **Network VAPT Workflow Plugin Composition** — workflows_network_vapt, plugins_nmap_plugin, plugins_nuclei_plugin, finding_engine, report_engine [EXTRACTED 1.00]
- **Web VAPT Workflow Plugin Composition** — workflows_web_vapt, plugins_httpx_plugin, plugins_nuclei_plugin, finding_engine, report_engine [EXTRACTED 1.00]
- **AstraIX Platform Infrastructure** — services_postgres, services_redis, services_backend, services_frontend [EXTRACTED 1.00]
- **Shared Risk Scoring Component** — finding_engine, workflows_asset_discovery, workflows_cloud_posture, workflows_code_audit, workflows_discovery, workflows_network_vapt, workflows_web_vapt [EXTRACTED 1.00]
- **Shared Reporting Component** — report_engine, workflows_asset_discovery, workflows_cloud_posture, workflows_code_audit, workflows_discovery, workflows_network_vapt, workflows_web_vapt [EXTRACTED 1.00]
- **Plugin SDK Schema Defines Plugin Structure** — plugin_sdk, plugins_httpx_plugin, plugins_nmap_plugin, plugins_nuclei_plugin, plugins_semgrep_plugin, plugins_subfinder_plugin, plugins_trivy_plugin [EXTRACTED 1.00]

## Communities (117 total, 26 thin omitted)

### Community 0 - "Plugin Schemas"
Cohesion: 0.05
Nodes (107): TimestampMixin, UUIDMixin, TimestampMixin, UUIDMixin, BaseSchema, Permission, Permission identifiers., Dependency for requiring a specific permission. (+99 more)

### Community 1 - "Metrics System"
Cohesion: 0.06
Nodes (46): Counter, Histogram, MetricsRegistry, _NoopCounter, _NoopHistogram, Metrics primitives (stubs at Milestone 1).  These are typed protocols so service, Monotonically increasing value, optionally labelled., Distribution value, optionally labelled. (+38 more)

### Community 2 - "Context Building"
Cohesion: 0.05
Nodes (41): ContextBuilder, FindingContextPayload, Context Builder — assembles what's fed into a prompt.  Pre-AI responsibilities:, What the AI sees. Pre-serialization.      The AI Gateway *never* receives the ra, Build a `FindingContextPayload` from typed inputs., Return the same set of findings, possibly tagged with correlation., DefaultFindingDeduplicator, FindingDeduplicator (+33 more)

### Community 3 - "Assessment API"
Cohesion: 0.06
Nodes (58): assess(), AssessRequest, AssessResponse, _bootstrap(), FindingSummary, list_capabilities(), FastAPI app for the AI-SecOS Core Web UI.  Run with: uvicorn api:app --reload --, Convert 'https://example.com:443' to 'asset_example_com'. (+50 more)

### Community 4 - "App Factory & Null Providers"
Cohesion: 0.06
Nodes (48): NullContextBuilder, Default at Milestone 1.      Performs no compression or redaction. A future mile, NullProvider, Identity provider for tests and the empty Milestone 1 default.      Returns requ, build_app(), lifespan(), FastAPI app factory.  Binds the DI container to the web transport.  - Health/rea, Start/stop lifetime management. (+40 more)

### Community 5 - "Workflow Engine"
Cohesion: 0.06
Nodes (35): float, Task Planner tests.  Targets:   - DAG topology respecting `depends_on`   - Paral, A -> B -> C runs in serial., A -> B,C -> D runs B/C in parallel., test_diamond_workflow(), test_linear_workflow(), Workflow Engine — declarative Workflow + Capability resolution.  A `Workflow` is, Workflow + the chain of references used to compile it. (+27 more)

### Community 6 - "Architecture Concepts"
Cohesion: 0.05
Nodes (48): System Architecture, AI Gateway Module, AI-SecOS Core, Applications Layer, Capability Abstraction, Infrastructure Module, Domain Models Module, Normalizer Module (+40 more)

### Community 7 - "Frontend Package Config"
Cohesion: 0.04
Nodes (47): dependencies, axios, class-variance-authority, clsx, date-fns, @hookform/resolvers, lucide-react, next (+39 more)

### Community 8 - "Task & Risk Types"
Cohesion: 0.06
Nodes (32): Enum, PluginType, AssessmentStatus, Orchestrator Service  Coordinates plugins, assessments, and findings.  Responsib, Assessment lifecycle., Where a risk axis got its number., RiskFactorSource, Task — the unit the Task Planner reasons about.  A `Task` is a step decoded from (+24 more)

### Community 9 - "Frontend Dashboard Pages"
Cohesion: 0.08
Nodes (30): apiKeysApi, assessmentsApi, assetsApi, findingsApi, healthApi, pluginsApi, scanApi, ApiKey (+22 more)

### Community 10 - "FastAPI Dependencies"
Cohesion: 0.05
Nodes (35): get_container(), get_settings(), Dependency providers for FastAPI routes., FastAPI dependency: immutable container wired to pathOps., Shortcut: typed settings., _map_error(), Convert platform errors → HTTP responses.  FastAPI exception handlers delegate t, Bind platform error handler. (+27 more)

### Community 11 - "Platform Settings"
Cohesion: 0.07
Nodes (37): BaseSettings, get_settings(), Application settings loaded from env vars or .env., Settings, AIGatewaySettings, FindingEngineSettings, load_settings(), ObservabilitySettings (+29 more)

### Community 12 - "Plugin Loader"
Cohesion: 0.06
Nodes (23): LoadedPlugin, PluginLoaderError, Plugin Loader: read manifests from disk → PluginRecords.  The Loader is the *onl, A loader-level result wrapping a successfully parsed manifest., Walk the plugins root; return all parseable plugin records.          Directories, Load a single plugin by directory path.          Raises PluginLoaderError on mis, PluginAlreadyRegisteredError, PluginNotFoundError (+15 more)

### Community 13 - "Risk Engine"
Cohesion: 0.08
Nodes (24): DefaultRiskEngine, _noop_severity_to_score(), NoopRiskEngine, Risk Engine — pipeline orchestrator and entry points.  Two implementations are s, Identity: score derived directly from canonical severity.      Used in tests and, A scored finding (or a typed wrapper around a SecurityFinding)., Engine port: score one or more canonical findings., Score each canonical finding. (+16 more)

### Community 14 - "Organizations API"
Cohesion: 0.08
Nodes (33): MembershipCreate, MembershipUpdate, OrganizationUpdate, ProjectUpdate, UserRepository, User, delete_api_key(), delete_organization() (+25 more)

### Community 15 - "Assets & Sessions"
Cohesion: 0.09
Nodes (23): AsyncSession, get_session(), Database session dependency., BaseRepository, Repository pattern for data access.  Each repository:   - Wraps SQLAlchemy queri, Generic repository for any model., List with pagination and optional filters., Count records with optional filters. (+15 more)

### Community 16 - "Frontend Project Pages"
Cohesion: 0.12
Nodes (20): cn(), roleConfig, formats, templates, authApi, membershipsApi, organizationsApi, projectsApi (+12 more)

### Community 17 - "Capability Loader"
Cohesion: 0.14
Nodes (25): CapabilityLoader, CapabilityLoaderError, LoadedCapability, _parse_asset_category(), _parse_framework(), _parse_manifest(), YAML-based capability loader.  Loads capability manifests from filesystem into t, Parse a YAML mapping into a `CapabilityManifest`. (+17 more)

### Community 18 - "Projects API"
Cohesion: 0.13
Nodes (14): Project, ProjectCreate, ProjectRepository, UUID, create_project(), delete_project(), get_project(), get_project_repo() (+6 more)

### Community 19 - "Security Scanner Plugins"
Cohesion: 0.14
Nodes (25): Finding Engine, web/discovery capability, network/recon capability, network/vuln-scan capability, api/security capability, web/vuln-scan capability, HTTP Probe (httpx) Plugin, Nmap Port Scanner Plugin (+17 more)

### Community 20 - "Community 20"
Cohesion: 0.10
Nodes (17): BasePlugin, FindingOut, PluginError, PluginOutput, PluginSchema, Parse stdin: str → dict., Structured logging accessible to orchestrator., Schema for plugin I/O, described in plugin.yml. (+9 more)

### Community 21 - "Community 21"
Cohesion: 0.13
Nodes (13): QuickAction, quickActions, RecentAssessments(), StatCardProps, StatsCards(), resources, ResourceUsage, services (+5 more)

### Community 22 - "Community 22"
Cohesion: 0.16
Nodes (15): AIGateway, DefaultAIGateway, AI Gateway — composed pipeline.  Pipeline order (matches Architecture):    1. Ro, Single entry point for AI reasoning tasks.      Implementations are responsible, Default wired pipeline., AIResponse, A provider's structured response., NoopResponseParser (+7 more)

### Community 23 - "Community 23"
Cohesion: 0.09
Nodes (21): compilerOptions, allowJs, baseUrl, esModuleInterop, forceConsistentCasingInFileNames, incremental, isolatedModules, jsx (+13 more)

### Community 24 - "Community 24"
Cohesion: 0.22
Nodes (13): statusConfig, severityConfig, statusOptions, statusConfig, CardTitle, Table, TableBody, TableCaption (+5 more)

### Community 25 - "Community 25"
Cohesion: 0.13
Nodes (13): CancellationToken, CancelledError, Cancellation token for running tasks/plans.  The platform-wide cancellation cont, A typed alias for cancellation that originates from the platform., Lightweight, async-friendly cancellation., NoopTaskExecutor, Task Executor — runs a Task.  A planner produces Tasks; the executor is what run, Run a single Task and emit a result. (+5 more)

### Community 26 - "Community 26"
Cohesion: 0.15
Nodes (15): emit_plugin_completed(), emit_plugin_finding(), emit_plugin_progress(), emit_plugin_started(), PluginCompletedPayload, PluginFindingPayload, PluginProgressPayload, PluginStartedPayload (+7 more)

### Community 27 - "Community 27"
Cohesion: 0.13
Nodes (13): get_password_hash(), Organization, OrganizationRepository, delete_organization(), get_org_repo(), get_organization(), list_organizations(), Register a new user and optionally create an organization. (+5 more)

### Community 28 - "Community 28"
Cohesion: 0.21
Nodes (16): _ai_comment_placeholder(), _build_section(), _findings_section(), NullReportEngine, Report Engine — implementation.  At Milestone 1, only the JSON/Markdown default, Render reports from findings + risk scores., JSON/Markdown default at Milestone 1.      Produces deterministic artefacts usin, ReportEngine (+8 more)

### Community 29 - "Community 29"
Cohesion: 0.15
Nodes (10): _InMemoryPromptManager, PromptManager, PromptTemplate, PromptVersionError, Prompt Manager — versioned prompt templates.  A `PromptTemplate` is a parameteri, Raised when a requested `prompt_id` / version combination is unknown., One version of one prompt.      The text uses stdlib `Template` semantics ($-sty, Resolved-source-of-truth for prompt templates. (+2 more)

### Community 30 - "Community 30"
Cohesion: 0.18
Nodes (17): api_key_header, decode_token(), get_current_active_user(), get_current_superuser(), get_current_user(), get_role_permissions(), get_user_organizations(), get_user_projects() (+9 more)

### Community 31 - "Community 31"
Cohesion: 0.16
Nodes (9): CapabilityAlreadyRegisteredError, CapabilityNotFoundError, Capability-specific error types., Raised when attempting to register a duplicate capability., Raised when a capability is not found in the registry., CapabilityRegistry, Capability Registry — typed lookup and lifecycle.  Thread-safe in-memory registr, Thread-safe registry of `Capability` instances keyed by id+version.      Capabil (+1 more)

### Community 32 - "Community 32"
Cohesion: 0.15
Nodes (10): Membership, OrganizationCreate, MembershipRepository, get_membership_repo(), list_memberships(), List organization or project memberships., Remove a member from organization or project., remove_member() (+2 more)

### Community 33 - "Community 33"
Cohesion: 0.18
Nodes (14): Convenience: flatten to a dict for string substitution., Any, AssessmentId, Yield canonical findings from a raw plugin output.          Implementations MUST, _confidence(), _extract_items(), make_httpx_input(), _normalize_one() (+6 more)

### Community 34 - "Community 34"
Cohesion: 0.21
Nodes (10): Assessment, Finding, Orchestrator, Build plugin invocation params from assessment., Persist plugins' findings., Generate fingerprint: title + asset + plugin + severity., Sequences assessment execution: plugins → findings., Execute an assessment by ID. (+2 more)

### Community 35 - "Community 35"
Cohesion: 0.16
Nodes (10): get_plugin_registry(), PluginInstance, PluginRegistry, Execute plugin subprocess. Returns (output, error)., Run subprocess synchronously. Returns (stdout, stderr)., Singleton plugin registry., Loaded plugin: metadata + path., Lifecycle: discover → load → run → results.      Plugins are subprocesses: (+2 more)

### Community 36 - "Community 36"
Cohesion: 0.29
Nodes (4): DefaultTaskPlanner, Default planner: DAG scheduler with retries + parallel workers., Task, TaskId

### Community 37 - "Community 37"
Cohesion: 0.19
Nodes (7): ProviderAlreadyRegisteredError, ProviderManager, ProviderNotFoundError, Provider Manager.  The Manager owns the lifecycle of providers. Applications nev, Thread-safe registry of providers.      The Manager is the *only* place provider, AIProvider, Concrete providers (OpenAI/Anthropic/...) implement this.

### Community 38 - "Community 38"
Cohesion: 0.17
Nodes (8): ApiKey, ApiKeyRepository, get_api_key_repo(), list_api_keys(), List API keys for organization., Enable/disable an API key., revoke_api_key(), toggle_api_key()

### Community 39 - "Community 39"
Cohesion: 0.17
Nodes (13): PluginRegistry, _count_by_capability(), _count_by_type(), get_plugin(), list_plugins(), plugins_info(), List all registered plugins., Get plugin details by ID. (+5 more)

### Community 40 - "Community 40"
Cohesion: 0.18
Nodes (10): Asset, get_orchestrator(), Orchestrator, Resolve plugins for an assessment., Run plugins in parallel., Process plugin findings, dedupe, persist., Stable identifier: title + asset., Singleton orchestrator. (+2 more)

### Community 41 - "Community 41"
Cohesion: 0.18
Nodes (9): ModelRouter, NullModelRouter, Model Router — decides `(provider_id, model)` per request.  At Milestone 1 we sh, Decides which provider/model to use., Pass-through router registered by default at Milestone 1., Deterministic choice for tests / deterministic callers., RoutingDecision, select_first_providers() (+1 more)

### Community 42 - "Community 42"
Cohesion: 0.19
Nodes (10): CapabilityResolverError, Raised when capability resolution fails (missing workflow, etc.)., A Plugin required by the capability (plugin_id, min_version)., RequiredPlugin, Capability Resolver.  Resolves a `Capability` request into a concrete execution, Validate inputs against the capability's input schema (lightweight).          Pe, Raised when capability resolution fails., A Capability fully resolved to executable Workflows. (+2 more)

### Community 43 - "Community 43"
Cohesion: 0.22
Nodes (13): Headers, _add(), _detect_cdn(), _detect_technologies(), _extract_title(), main(), probe_target(), Extract version from header like 'nginx/1.21.6'. (+5 more)

### Community 44 - "Community 44"
Cohesion: 0.23
Nodes (12): Element, build_nmap_command(), main(), _parse_host(), parse_nmap_xml(), _parse_port(), Parse a single host element., Parse a port element. (+4 more)

### Community 45 - "Community 45"
Cohesion: 0.21
Nodes (8): FindingNormalizer, NormalizationError, Normalizer interface + registry.  The Normalizer is how raw plugin output become, Turns a plugin-specific raw output into a `SecurityFinding`.      A single input, HttpxPluginId, Bundle the httpx plugin id constant., Severity levels, ordered from informational to critical., Severity

### Community 46 - "Community 46"
Cohesion: 0.19
Nodes (10): FindingOut, PluginError, PluginManifest, PluginOutput, PluginStatus, PluginRunResult, Result of running a plugin., AssessmentStatus (+2 more)

### Community 47 - "Community 47"
Cohesion: 0.19
Nodes (10): Result, fail(), Failure, is_failure(), is_ok(), ok(), Result type (Rust/Python-port idiom) for explicit success/failure.  Used by serv, Successful outcome carrying a value. (+2 more)

### Community 48 - "Community 48"
Cohesion: 0.24
Nodes (10): AIError, ConfigurationError, FindingEngineError, PlatformError, PluginError, Single error hierarchy for the entire AI-SecOS Core.  Public API (the only types, Base error of the platform.      Carries `code` (machine-readable, stable) and `, ReportEngineError (+2 more)

### Community 49 - "Community 49"
Cohesion: 0.20
Nodes (12): ApiKeyCreate, create_access_token(), create_refresh_token(), verify_password(), OAuth2PasswordRequestForm, timedelta, login(), OAuth2 compatible login for Swagger UI. (+4 more)

### Community 50 - "Community 50"
Cohesion: 0.18
Nodes (11): Orchestrator, cancel_assessment(), create_assessment(), get_assessment(), list_assessments(), Cancel an assessment (mark as cancelled)., List assessments with pagination., Create and queue an assessment for execution. (+3 more)

### Community 51 - "Community 51"
Cohesion: 0.24
Nodes (5): NmapScanner, Run as process: stdin → scan → stdout, Run nmap, parse output, return findings., Parse Nmap XML/text → findings., PluginOutput

### Community 52 - "Community 52"
Cohesion: 0.22
Nodes (7): event_loop(), Pytest configuration and fixtures., mock_registry(), mock_settings(), Override default event loop., Mock settings for tests., Mock plugin registry.

### Community 53 - "Community 53"
Cohesion: 0.28
Nodes (7): _categorize_semgrep(), _extract_tags(), _normalize_one(), Semgrep Plugin — normalizer.  Converts raw `semgrep` output into canonical `Secu, Categorize semgrep finding based on check_id and metadata., Extract tags from semgrep metadata., Normalize a single semgrep finding.

### Community 54 - "Community 54"
Cohesion: 0.25
Nodes (8): delete_finding(), filters__dict(), get_finding(), list_findings(), List findings with pagination., Helper to allow scoped filters., Update finding status / fields., update_finding()

### Community 55 - "Community 55"
Cohesion: 0.29
Nodes (5): AIRequest, AITokenUsage, AI Provider port.  A Provider is anything that can take a prompt + structured in, Tokens billed for one call. Independent of model types., A request is a structured, traceable call.      `prompt` is the raw text/materia

### Community 56 - "Community 56"
Cohesion: 0.25
Nodes (6): _noop_dedup(), Milestone 2 End-to-End Demo — Capability -> Workflow -> Plugin -> Findings.  Dem, Minimal in-memory deduplicator for M2 demo only., M2 End-to-End test.  Validates the vertical slice: Capability → Plugin → Normali, The full M2 path executes end-to-end and emits a summary., test_m2_demo_runs()

### Community 57 - "Community 57"
Cohesion: 0.25
Nodes (5): Capability, ComplianceTag, Promote this manifest to an executable Capability., Executable Capability.      This is what Applications interact with. Capabilitie, A compliance framework mapping (one capability can map to many).

### Community 58 - "Community 58"
Cohesion: 0.25
Nodes (8): Network Vulnerability Assessment, External Asset Discovery, Web Discovery, Web Application Security Assessment, HTTPX Scanner Plugin, Nmap Scanner Plugin, Nuclei Scanner Plugin, Subfinder Scanner Plugin

### Community 59 - "Community 59"
Cohesion: 0.36
Nodes (7): CorrelationId, get_correlation_id(), new_correlation_id(), Correlation id context.  Every critical action (workflow, plugin exec, AI call), Produce a new opaque correlation id (UUID4 hex)., Return the current correlation id, creating one if absent.      Use only at entr, set_correlation_id()

### Community 60 - "Community 60"
Cohesion: 0.36
Nodes (7): build_nuclei_command(), main(), parse_nuclei_json(), Execute nuclei and return parsed results., Build nuclei command arguments., Parse nuclei JSON output lines., run_nuclei_scan()

### Community 61 - "Community 61"
Cohesion: 0.36
Nodes (7): build_semgrep_command(), main(), parse_semgrep_results(), Build semgrep command arguments., Parse semgrep JSON output., Execute semgrep and return parsed results., run_semgrep_scan()

### Community 63 - "Community 63"
Cohesion: 0.36
Nodes (7): build_subfinder_command(), main(), parse_subfinder_json(), Build subfinder command arguments., Parse subfinder JSON output lines., Execute subfinder and return parsed results., run_subfinder()

### Community 64 - "Community 64"
Cohesion: 0.36
Nodes (7): build_trivy_command(), main(), parse_trivy_results(), Build trivy command arguments., Parse trivy JSON output., Execute trivy and return parsed results., run_trivy_scan()

### Community 65 - "Community 65"
Cohesion: 0.33
Nodes (5): _categorize(), _normalize_one(), Nuclei Plugin — normalizer.  Converts raw `nuclei` output into canonical `Securi, Map nuclei tags to finding category., Normalize a single nuclei finding.

### Community 66 - "Community 66"
Cohesion: 0.43
Nodes (4): BaseSchema, ErrorResponse, PaginatedResponse, ResponseSchema

### Community 67 - "Community 67"
Cohesion: 0.40
Nodes (4): do_run_migrations(), run_async_migrations(), run_migrations_online(), Connection

### Community 68 - "Community 68"
Cohesion: 0.40
Nodes (3): navigation, settingsNav, Sidebar()

### Community 71 - "Community 71"
Cohesion: 0.60
Nodes (5): AstraIX Docker Compose, Backend API Service, Frontend Service, PostgreSQL Service, Redis Service

### Community 72 - "Community 72"
Cohesion: 0.50
Nodes (4): platform_error_to_http_response(), PlatformErrorResponse, Map platform errors → HTTP responses.  FastAPI exception handler in `platform/`, Convert a PlatformError to a status/body pair.      `correlation_id` is included

### Community 73 - "Community 73"
Cohesion: 0.40
Nodes (5): Technology Stack, AI Tech Stack, Backend Tech Stack, DevOps Tech Stack, Frontend Tech Stack

## Knowledge Gaps
- **148 isolated node(s):** `UUIDMixin`, `TimestampMixin`, `nextConfig`, `name`, `version` (+143 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **26 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BaseModel` connect `Plugin Schemas` to `Metrics System`, `Community 66`, `Assessment API`, `Community 35`, `Workflow Engine`, `Context Building`, `Task & Risk Types`, `Community 46`, `Assets & Sessions`, `Community 20`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Why does `SecurityFinding` connect `Context Building` to `Plugin Schemas`, `Community 65`, `Community 33`, `Assessment API`, `App Factory & Null Providers`, `Workflow Engine`, `Community 45`, `Risk Engine`, `Community 53`, `Community 28`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `Container` connect `App Factory & Null Providers` to `Metrics System`, `Context Building`, `Assessment API`, `Community 36`, `Community 37`, `Workflow Engine`, `Community 41`, `FastAPI Dependencies`, `Platform Settings`, `Plugin Loader`, `Community 45`, `Risk Engine`, `Community 22`, `Community 29`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Are the 34 inferred relationships involving `SecurityFinding` (e.g. with `ContextBuilder` and `FindingContextPayload`) actually correct?**
  _`SecurityFinding` has 34 INFERRED edges - model-reasoned connections that need verification._
- **Are the 52 inferred relationships involving `RoleName` (e.g. with `Permission` and `RequiresPermission`) actually correct?**
  _`RoleName` has 52 INFERRED edges - model-reasoned connections that need verification._
- **What connects `AI Gateway — typed contract + stub implementations.  Six sub-modules per Archite`, `Context Builder — assembles what's fed into a prompt.  Pre-AI responsibilities:`, `What the AI sees. Pre-serialization.      The AI Gateway *never* receives the ra` to the rest of the system?**
  _586 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Plugin Schemas` be split into smaller, more focused modules?**
  _Cohesion score 0.05121257282211082 - nodes in this community are weakly interconnected._