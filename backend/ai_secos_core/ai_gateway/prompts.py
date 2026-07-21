"""Prompt Manager — versioned prompt templates.

A `PromptTemplate` is a parameterized string rendered with the values
provided at call time. The manager resolves `(prompt_id, version)` →
template text. Versioning is required so prompts can evolve without
silently changing behavior.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from string import Template
from threading import RLock
from typing import Any, Mapping


class PromptVersionError(Exception):
    """Raised when a requested `prompt_id` / version combination is unknown."""


@dataclass(frozen=True)
class PromptTemplate:
    """One version of one prompt.

    The text uses stdlib `Template` semantics ($-style substitution,
    safe for arbitrary content). Substitutions missing at render time
    raise `KeyError`. The manager MUST validate names.
    """

    id: str
    version: str
    text: str
    description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def render(self, params: Mapping[str, Any] | None = None) -> str:
        params = params or {}
        return Template(self.text).safe_substitute(**params)


class PromptManager(abc.ABC):
    """Resolved-source-of-truth for prompt templates."""

    @abc.abstractmethod
    def register(self, template: PromptTemplate) -> None: ...

    @abc.abstractmethod
    def get(self, prompt_id: str, version: str | None = None) -> PromptTemplate: ...

    @abc.abstractmethod
    def has(self, prompt_id: str, version: str = "0.1.0") -> bool: ...


class _InMemoryPromptManager:
    """Process-local default; replace with persistence later if needed."""

    def __init__(self, templates: list[PromptTemplate] | None = None) -> None:
        self._by_id: dict[str, dict[str, PromptTemplate]] = {}
        self._lock = RLock()
        if templates:
            for t in templates:
                self.register(t)

    def register(self, template: PromptTemplate) -> None:
        with self._lock:
            self._by_id.setdefault(template.id, {})[template.version] = template

    def get(self, prompt_id: str, version: str | None = None) -> PromptTemplate:
        with self._lock:
            versions = self._by_id.get(prompt_id)
            if not versions:
                raise PromptVersionError(f"unknown prompt id: {prompt_id}")
            if version is None:
                # Latest registered (deterministic by lex-sorted version).
                last = sorted(versions.items(), key=lambda kv: kv[0])[-1][1]
                return last
            if version not in versions:
                raise PromptVersionError(
                    f"unknown prompt version: {prompt_id}@{version}",
                )
            return versions[version]

    def has(self, prompt_id: str, version: str = "0.1.0") -> bool:
        with self._lock:
            return version in self._by_id.get(prompt_id, {})


DefaultPromptManager = _InMemoryPromptManager  # canonical alias for the DI container

__all__ = [
    "PromptTemplate",
    "PromptManager",
    "DefaultPromptManager",
    "PromptVersionError",
]
