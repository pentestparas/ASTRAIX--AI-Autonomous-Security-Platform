"""Dependency Injection container.

Uses DI’y to wire the entire platform without magics, registries,
or service location.

- Built once at bootstrap.
- Frozen behind an interface so downstream tests don't rely on
  fixture factory internals.
- Often abused to become a god class, but we keep it focused:
      * exposes ~12 typed values
      * thread-safe
      * reinstallable (production + tests)
      * injectables are immutable after build
"""

from __future__ import annotations

import threading
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass

from ai_secos_core.ai_gateway.context import ContextBuilder, NullContextBuilder
from ai_secos_core.ai_gateway.gateway import AIGateway, DefaultAIGateway
from ai_secos_core.ai_gateway.manager import ProviderManager
from ai_secos_core.ai_gateway.prompts import DefaultPromptManager, PromptManager
from ai_secos_core.ai_gateway.provider import NullProvider
from ai_secos_core.ai_gateway.response import NoopResponseParser, ResponseParser
from ai_secos_core.ai_gateway.router import ModelRouter, NullModelRouter
from ai_secos_core.ai_gateway.tokens import NoopTokenManager, TokenManager
from ai_secos_core.config.settings import Settings, load_settings
from ai_secos_core.finding_engine.correlator import FindingCorrelator, NoopFindingCorrelator
from ai_secos_core.finding_engine.deduplicator import (
    DefaultFindingDeduplicator,
    FindingDeduplicator,
)
from ai_secos_core.finding_engine.engine import DefaultFindingEngine, FindingEngine
from ai_secos_core.finding_engine.enricher import FindingEnricher, NoopFindingEnricher
from ai_secos_core.finding_engine.fingerprint import DefaultFindingFingerprinter, FindingFingerprinter
from ai_secos_core.finding_engine.normalizer import FindingNormalizer, NormalizerRegistry
from ai_secos_core.infrastructure.logging import (
    bind_correlation_id,
    configure_logging,
    get_logger,
)
from ai_secos_core.infrastructure.metrics import MetricsRegistry, NoopMetricsRegistry
from ai_secos_core.plugin_system.executor import NoopTaskExecutor, TaskExecutor
from ai_secos_core.plugin_system.loader import PluginLoader
from ai_secos_core.plugin_system.registry import PluginRegistry
from ai_secos_core.plugin_system.sandbox import PluginSandbox
from ai_secos_core.plugin_system.validator import PluginValidator
from ai_secos_core.report_engine.engine import ReportEngine, NullReportEngine
from ai_secos_core.risk_engine.engine import DefaultRiskEngine, RiskEngine
from ai_secos_core.risk_engine.providers import StaticRiskSignalProvider
from ai_secos_core.runtime.task_planner import TaskPlanner, DefaultTaskPlanner, TaskPlannerConfig
from ai_secos_core.runtime.workflow_engine import DefaultWorkflowEngine, WorkflowEngine
from ai_secos_core.shared.events import EventDispatcher, InProcessEventDispatcher


@dataclass(frozen=True)
class Container:
    """The exposed container interface."""

    settings: Settings
    logger: logging.Logger             # structlog bound to settings.observability
    events: EventDispatcher             # InProcessEventDispatcher (for M1)
    metrics: MetricsRegistry            # NoopMetricsRegistry (for M1)
    plugins: PluginRegistry            # empty at start, populated by load()
    events_logger: logging.Logger      # logger specialized for event bus lines

    # plugin_system/
    loader: PluginLoader
    validator: PluginValidator
    sandbox: PluginSandbox
    executor: TaskExecutor             # NoopTaskExecutor (for M1)

    # finding_engine/
    fingerprinter: FindingFingerprinter  # DefaultFindingFingerprinter
    normalizers: NormalizerRegistry     # empty, populated by loader at startup
    deduplicator: FindingDeduplicator   # DefaultFindingDeduplicator
    enricher: FindingEnricher           # NoopFindingEnricher (for M1)
    correlator: FindingCorrelator       # NoopFindingCorrelator (for M1)
    finding_engine: FindingEngine       # DefaultFindingEngine

    # risk_engine/
    risk_engine: RiskEngine              # DefaultRiskEngine

    # ai_gateway/
    provider_manager: ProviderManager        # contains only NullProvider (for M1)
    prompt_manager: PromptManager          # DefaultPromptManager
    context_builder: ContextBuilder       # NullContextBuilder (for M1)
    model_router: ModelRouter              # NullModelRouter
    token_manager: TokenManager           # NoopTokenManager (for M1)
    response_parser: ResponseParser      # NoopResponseParser (for M1)
    ai_gateway: AIGateway                # DefaultAIGateway

    # report_engine/
    report_engine: ReportEngine           # NullReportEngine (for M1)

    # runtime/
    workflow_engine: WorkflowEngine       # DefaultWorkflowEngine
    task_planner: TaskPlanner            # DefaultTaskPlanner

    def load_plugins(self) -> None:
        """At boot, walk the plugins root and populate:
          - plugin registry
          - normalizer registry

        Any error here halts the platform (fail-fast).
        """
        records = self.loader.discover()
        for rec in records:
            # Plugin registry
            self.plugins.register(rec)
            # TODO: Lookup normalizer + register


@dataclass
class _MutableContainer:
    """Mutable (thread-safe) wiring harness."""

    settings: Settings = None
    logger: logging.Logger = None
    events: EventDispatcher = None
    metrics: MetricsRegistry = None
    plugins: PluginRegistry = None

    loader: PluginLoader = None
    validator: PluginValidator = None
    sandbox: PluginSandbox = None
    executor: TaskExecutor = None

    fingerprinter: FindingFingerprinter = None
    normalizers: NormalizerRegistry = None
    deduplicator: FindingDeduplicator = None
    enricher: FindingEnricher = None
    correlator: FindingCorrelator = None
    finding_engine: FindingEngine = None

    risk_engine: RiskEngine = None

    provider_manager: ProviderManager = None
    prompt_manager: PromptManager = None
    context_builder: ContextBuilder = None
    model_router: ModelRouter = None
    token_manager: TokenManager = None
    response_parser: ResponseParser = None
    ai_gateway: AIGateway = None

    report_engine: ReportEngine = None

    workflow_engine: WorkflowEngine = None
    task_planner: TaskPlanner = None

    _lock: threading.Lock = threading.RLock()

    @contextmanager
    def mutate(self) -> Iterator[None]:
        """Safely edit mutable values."""
        with self._lock:
            yield

    def freeze(self) -> Container:
        """Return a frozen copy ready for consumption."""
        with self.mutate():
            assert all(
                attr is not None for attr in self.__dict__.values()
                if not attr.startswith("_")
            ), "Missing required container values"
            return Container(**{
                k: v for k, v in self.__dict__.items()
                if not k.startswith("_")
            })


def build_default_container() -> Container:
    """Wire default implementations for production runtime."""
    settings = load_settings()
    configure_logging(settings.observability)
    logger = get_logger("ai_secos_core.api_platform.container")

    builder = _MutableContainer()

    def wire_value(key: str, value):
        setattr(builder, key, value)

    # Delegate wire-up. Order does not matter beyond circularity.
    with builder.mutate():
        builder.settings = settings
        builder.logger = logger
        wire_value("events", InProcessEventDispatcher())
        wire_value("metrics", NoopMetricsRegistry())
        wire_value("plugins", PluginRegistry())

        wire_value("loader", PluginLoader(settings.plugin_system.plugins_root))
        wire_value("validator", PluginValidator(
            installed_capabilities=(),
            allowed_sandbox_filesystems=("ephemeral",),
            allowed_sandbox_networks=("none", "outbound"),
        ))
        wire_value("sandbox", PluginSandbox(settings.plugin_system))
        wire_value("executor", NoopTaskExecutor())

        wire_value("fingerprinter", DefaultFindingFingerprinter())
        wire_value("normalizers", NormalizerRegistry())
        wire_value("deduplicator", DefaultFindingDeduplicator())
        wire_value("enricher", NoopFindingEnricher())
        wire_value("correlator", NoopFindingCorrelator())
        wire_value("finding_engine", DefaultFindingEngine(
            normalizers=builder.normalizers,
            deduplicator=builder.deduplicator,
            enricher=builder.enricher,
            correlator=builder.correlator,
        ))

        static_providers = (
            StaticRiskSignalProvider(
                source="likelihood",
                default_weight=settings.risk_engine.weights["likelihood"],
            ),
            StaticRiskSignalProvider(
                source="impact",
                default_weight=settings.risk_engine.weights["impact"],
            ),
            StaticRiskSignalProvider(
                source="exploitability",
                default_weight=settings.risk_engine.weights["exploitability"],
            ),
            StaticRiskSignalProvider(
                source="business_context",
                default_weight=settings.risk_engine.weights["business_context"],
            ),
        )
        wire_value("risk_engine", DefaultRiskEngine(
            providers=static_providers,
            weights=settings.risk_engine.weights,
        ))

        wire_value("provider_manager", ProviderManager([NullProvider()]))
        wire_value("prompt_manager", DefaultPromptManager())
        wire_value("context_builder", NullContextBuilder())
        wire_value("model_router", NullModelRouter(builder.provider_manager))
        wire_value("token_manager", NoopTokenManager())
        wire_value("response_parser", NoopResponseParser())
        wire_value("ai_gateway", DefaultAIGateway(
            provider_manager=builder.provider_manager,
            prompt_manager=builder.prompt_manager,
            context_builder=builder.context_builder,
            model_router=builder.model_router,
            token_manager=builder.token_manager,
            response_parser=builder.response_parser,
        ))

        wire_value("report_engine", NullReportEngine())

        wire_value("workflow_engine", DefaultWorkflowEngine())
        wire_value("task_planner", DefaultTaskPlanner(
            executor=builder.executor,
            event_dispatcher=builder.events,
            metrics=builder.metrics,
        ))

    container = builder.freeze()
    log = container.logger.bind(location="container")

    def load_plugins_at_boot():
        try:
            container.load_plugins()
            log.info("plugins.loaded", count=len(container.plugins.list()))
        except Exception:  # noqa: BLE001
            log.exception("plugins.load.failed")
            raise

    # Lifespan hook runs at boot.
    load_plugins_at_boot()

    container.events_logger = logger.getChild("event_bus")
    def log_event(ev):
        container.events_logger.info(
            "event_emitted",
            **ev.payload,
            type=ev.type,
            occurred_at=ev.occurred_at.isoformat(),
        )

    container.events.subscribe("*", log_event)
    return container


__all__ = ["Container", "build_default_container"]
