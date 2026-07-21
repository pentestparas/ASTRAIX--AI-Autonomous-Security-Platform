"""Response Parser — safe parsing of provider output back to types.

The Gateway emits a `ParsedAIResponse`; downstream code reads only
this — never raw provider output.

At Milestone 1 we ship the typed shape and a no-op parser. JSON-shape
parsing arrives when concrete providers exist.
"""

from __future__ import annotations

import abc
import json
from dataclasses import dataclass, field
from typing import Any, Mapping

from ai_secos_core.ai_gateway.provider import AIResponse


@dataclass(frozen=True)
class ParsedAIResponse:
    text: str
    structured: dict[str, Any] = field(default_factory=dict)
    provider_id: str = ""
    model: str = ""

    @classmethod
    def from_text(cls, text: str, *, provider_id: str, model: str) -> "ParsedAIResponse":
        """Factory: try JSON parse; fall back to a `{"text": ...}` envelope."""
        try:
            parsed = json.loads(text)
        except (ValueError, TypeError):
            return cls(text=text, structured={"text": text}, provider_id=provider_id, model=model)
        if not isinstance(parsed, dict):
            return cls(text=text, structured={"text": text}, provider_id=provider_id, model=model)
        return cls(text=text, structured=parsed, provider_id=provider_id, model=model)


class ResponseParser(abc.ABC):
    """Parse a `AIResponse` into a typed `ParsedAIResponse`."""

    @abc.abstractmethod
    def parse(self, response: AIResponse) -> ParsedAIResponse: ...


class NoopResponseParser:
    """Default at Milestone 1.

    Just delegates to `ParsedAIResponse.from_text`.
    """

    def parse(self, response: AIResponse) -> ParsedAIResponse:
        return ParsedAIResponse.from_text(
            response.text,
            provider_id=response.provider_id,
            model=response.model,
        )


__all__ = [
    "ResponseParser",
    "NoopResponseParser",
    "ParsedAIResponse",
]
