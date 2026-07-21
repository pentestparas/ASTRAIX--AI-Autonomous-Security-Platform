"""AI Gateway — composed pipeline.

Pipeline order (matches Architecture):

  1. Routing  (`ModelRouter.route`)           decide (provider, model)
  2. Context  (`ContextBuilder.build`)         assemble canonical payload
  3. Prompt   (`PromptManager.render`)         materialize prompt text
  4. Tokens   (`TokenManager.plan`)            validate budget
  5. Provider (`ProviderManager.get.generate`) call the provider
  6. Tokens   (`TokenManager.record`)          account usage
  7. Parse    (`ResponseParser.parse`)         convert to typed shape

Each sub-module is injectable. The Gateway itself is a thin
orchestrator.

At Milestone 1 we ship the typed contract `AIGateway` and the
`DefaultAIGateway` orchestrator wired to the null/stub
implementations. Concrete providers are explicitly out of scope.
"""

from __future__ import annotations

import abc
from typing import Any, Mapping

from ai_secos_core.ai_gateway.context import ContextBuilder, NullContextBuilder
from ai_secos_core.ai_gateway.manager import ProviderManager
from ai_secos_core.ai_gateway.prompts import PromptManager, DefaultPromptManager
from ai_secos_core.ai_gateway.provider import AIRequest
from ai_secos_core.ai_gateway.response import ParsedAIResponse, ResponseParser, NoopResponseParser
from ai_secos_core.ai_gateway.router import ModelRouter, NullModelRouter
from ai_secos_core.ai_gateway.tokens import (
    NoopTokenManager,
    TokenBudget,
    TokenManager,
)


class AIGateway(abc.ABC):
    """Single entry point for AI reasoning tasks.

    Implementations are responsible for routing, context, prompts,
    tokens, the call, accounting, and parsing — in that order.
    """

    @abc.abstractmethod
    async def complete(
        self,
        *,
        prompt_id: str,
        prompt_version: str | None,
        payload: Mapping[str, Any],
        budget: TokenBudget | None = None,
        requested_model: str | None = None,
        requested_provider: str | None = None,
        correlation_id: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> ParsedAIResponse:
        raise NotImplementedError


class DefaultAIGateway:
    """Default wired pipeline."""

    def __init__(
        self,
        *,
        provider_manager: ProviderManager,
        prompt_manager: PromptManager | None = None,
        context_builder: ContextBuilder | None = None,
        model_router: ModelRouter | None = None,
        token_manager: TokenManager | None = None,
        response_parser: ResponseParser | None = None,
    ) -> None:
        self._providers = provider_manager
        self._prompts = prompt_manager or DefaultPromptManager()
        self._context = context_builder or NullContextBuilder()
        self._router = model_router or NullModelRouter(provider_manager)
        self._tokens = token_manager or NoopTokenManager()
        self._parser = response_parser or NoopResponseParser()

    async def complete(
        self,
        *,
        prompt_id: str,
        prompt_version: str | None,
        payload: Mapping[str, Any],
        budget: TokenBudget | None = None,
        requested_model: str | None = None,
        requested_provider: str | None = None,
        correlation_id: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> ParsedAIResponse:
        # 1. Routing
        decision = await self._router.route(
            requested_model=requested_model,
            requested_provider=requested_provider,
        )

        # 2. Context (caller provides a fully-built payload as Mapping[str, Any])
        #    We don't reach in here — context_builder is reserved for canonical
        #    knowledge objects, not free-form call payloads.

        # 3. Prompt
        template = self._prompts.get(prompt_id, prompt_version)
        prompt_text = template.render(payload)

        # 4. Tokens
        budget = budget or TokenBudget.unlimited()
        self._tokens.plan(prompt_text, budget)

        # 5. Call
        request = AIRequest(
            provider_id=decision.provider_id,
            model=decision.model,
            prompt=prompt_text,
            payload=dict(payload),
            max_tokens=max_tokens,
            temperature=temperature,
            correlation_id=correlation_id,
        )
        provider = self._providers.get(decision.provider_id)
        response = await provider.generate(request)

        # 6. Tokens (record)
        self._tokens.record(response.usage, correlation_id=correlation_id)

        # 7. Parse
        return self._parser.parse(response)


__all__ = [
    "AIGateway",
    "DefaultAIGateway",
]
