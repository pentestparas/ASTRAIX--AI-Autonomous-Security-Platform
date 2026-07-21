"""Platform — bootstrap, DI container, lifespan, error mapping.

This is the *only* FastAPI-aware module. Everything else is transport-
agnostic. The container exposes:

  - `settings`:       typed configuration.
  - `events`:         event dispatcher.
  - `metrics`:        metrics registry (no-op default at M1).
  - `logger`:         structured logger.
  - `plugins`:        registry + loader.
  - `validator`:      manifest + invocation validator.
  - `sandbox`:        sandbox decision-maker.
  - `executor`:       plugin executor.
  - `normalizers`:    Normalizer registry.
  - `deduplicator`:   Default Finding deduplicator.
  - `enricher`:       Noop enricher.
  - `correlator`:     Noop correlator.
  - `finding_engine`: Finding pipeline.
  - `risk_engine`:    Likelihood/Impact/Exploitability/Business pipeline.
  - `provider_manager`:  Provider Manager (null provider at M1).
  - `prompt_manager`:    Prompt Manager.
  - `context_builder`:   NullContextBuilder.
  - `model_router`:      NullModelRouter.
  - `token_manager`:     NoopTokenManager.
  - `response_parser`:   NoopResponseParser.
  - `ai_gateway`:        DefaultAIGateway.
  - `report_engine`:     NullReportEngine.
  - `workflow_engine`:   DefaultWorkflowEngine.
  - `task_planner`:      DefaultTaskPlanner.
"""

from ai_secos_core.api_platform.container import (
    Container,
    build_default_container,
)
from ai_secos_core.api_platform.app_factory import (
    build_app,
)
from ai_secos_core.api_platform.error_handlers import (
    register_exception_handlers,
)
from ai_secos_core.api_platform.routes import (
    router as platform_router,
)
from ai_secos_core.api_platform.dependencies import (
    get_container,
    get_settings,
)

__all__ = [
    "Container",
    "build_default_container",
    "build_app",
    "register_exception_handlers",
    "platform_router",
    "get_container",
    "get_settings",
]
