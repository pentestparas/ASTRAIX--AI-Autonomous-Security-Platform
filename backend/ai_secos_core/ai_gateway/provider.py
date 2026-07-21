"""AI Provider port.

A Provider is anything that can take a prompt + structured input and
produce a structured response. Concrete adapters (OpenAI, Anthropic,
MiniMax, Ollama, Gemini, Nemotron, …) plug into Provider Manager only.

Per the directive, **no concrete provider is shipped at Milestone 1**.
We ship:

  - The `AIProvider` abstract base.
  - The typed `AIRequest` / `AIResponse` shapes.
  - A `NullProvider` that returns the input unchanged (used in tests
    and as a safe default).
"""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AITokenUsage:
    """Tokens billed for one call. Independent of model types."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


@dataclass(frozen=True)
class AIRequest:
    """A request is a structured, traceable call.

    `prompt` is the raw text/materialized prompt. `payload` is a
    structured side-channel (findings, asset, etc.) that providers may
    serialize their own way.
    """

    provider_id: str
    model: str
    prompt: str
    payload: dict[str, Any] = field(default_factory=dict)
    max_tokens: int | None = None
    temperature: float | None = None
    correlation_id: str | None = None


@dataclass(frozen=True)
class AIResponse:
    """A provider's structured response."""

    text: str
    usage: AITokenUsage
    raw: dict[str, Any] = field(default_factory=dict)
    provider_id: str = ""
    model: str = ""


class AIProvider(abc.ABC):
    """Concrete providers (OpenAI/Anthropic/...) implement this."""

    provider_id: str

    @abc.abstractmethod
    async def generate(self, request: AIRequest) -> AIResponse:
        raise NotImplementedError

    async def health(self) -> bool:
        return True


class NullProvider:
    """Identity provider for tests and the empty Milestone 1 default.

    Returns request.prompt back as the text. Billed tokens: 0.
    """

    provider_id = "null"

    async def generate(self, request: AIRequest) -> AIResponse:
        return AIResponse(
            text=request.prompt,
            usage=AITokenUsage(),
            raw={"provider": "null", "echo": True},
            provider_id=self.provider_id,
            model=request.model,
        )


__all__ = [
    "AIProvider",
    "AIRequest",
    "AIResponse",
    "AITokenUsage",
    "NullProvider",
]
