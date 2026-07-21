"""AI Gateway — typed contract + stub implementations.

Six sub-modules per Architecture:

  - Provider (port)         provider.py
  - Provider Manager        manager.py
  - Prompt Manager          prompts.py
  - Context Builder         context.py
  - Model Router            router.py
  - Token Manager           tokens.py
  - Response Parser         response.py
  - Gateway                 gateway.py

At Milestone 1 we ship:

  - Typed contracts (no behavior beyond stable identity).
  - Stubs for each sub-module that satisfy the contracts and let
    the platform compile and tests pass.
  - A `NullProvider` (identity; no model call).

Concrete providers (OpenAI, Anthropic, MiniMax, …) are explicitly out of
scope per the directive ("No AI provider implementation").
"""

from ai_secos_core.ai_gateway.provider import (
    AIProvider,
    AIRequest,
    AIResponse,
    AITokenUsage,
    NullProvider,
)
from ai_secos_core.ai_gateway.manager import (
    ProviderManager,
    ProviderAlreadyRegisteredError,
    ProviderNotFoundError,
)
from ai_secos_core.ai_gateway.prompts import (
    PromptTemplate,
    PromptManager,
    PromptVersionError,
)
from ai_secos_core.ai_gateway.context import (
    ContextBuilder,
    NullContextBuilder,
    FindingContextPayload,
)
from ai_secos_core.ai_gateway.router import (
    ModelRouter,
    RoutingDecision,
    NullModelRouter,
)
from ai_secos_core.ai_gateway.tokens import (
    TokenManager,
    NoopTokenManager,
    TokenBudget,
)
from ai_secos_core.ai_gateway.response import (
    ResponseParser,
    NoopResponseParser,
    ParsedAIResponse,
)
from ai_secos_core.ai_gateway.gateway import (
    AIGateway,
    DefaultAIGateway,
)

__all__ = [
    "AIProvider",
    "AIRequest",
    "AIResponse",
    "AITokenUsage",
    "NullProvider",
    "ProviderManager",
    "ProviderAlreadyRegisteredError",
    "ProviderNotFoundError",
    "PromptTemplate",
    "PromptManager",
    "PromptVersionError",
    "ContextBuilder",
    "NullContextBuilder",
    "FindingContextPayload",
    "ModelRouter",
    "RoutingDecision",
    "NullModelRouter",
    "TokenManager",
    "NoopTokenManager",
    "TokenBudget",
    "ResponseParser",
    "NoopResponseParser",
    "ParsedAIResponse",
    "AIGateway",
    "DefaultAIGateway",
]
