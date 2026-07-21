"""Metrics primitives (stubs at Milestone 1).

These are typed protocols so services can record counters and histograms
without committing to Prometheus / StatsD / OTLP. A future milestone may
add a Prometheus adapter implementing the same interfaces.

All recording methods are **best-effort**: when no registry is bound,
calls evaluate to no-ops via the `NoopMetricsRegistry` default.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol, Sequence


class Counter(Protocol):
    """Monotonically increasing value, optionally labelled."""

    def inc(self, amount: float = 1.0, labels: dict[str, str] | None = None) -> None: ...


class Histogram(Protocol):
    """Distribution value, optionally labelled."""

    def observe(self, value: float, labels: dict[str, str] | None = None) -> None: ...


class MetricsRegistry(Protocol):
    def counter(
        self,
        name: str,
        *,
        unit: str | None = None,
        description: str | None = None,
        label_names: Sequence[str] | None = None,
    ) -> Counter: ...

    def histogram(
        self,
        name: str,
        *,
        unit: str | None = None,
        description: str | None = None,
        buckets: Iterable[float] | None = None,
        label_names: Sequence[str] | None = None,
    ) -> Histogram: ...


# ---------------------------------------------------------------------------


@dataclass
class _NoopCounter:
    name: str

    def inc(self, amount: float = 1.0, labels: dict[str, str] | None = None) -> None:
        return None


@dataclass
class _NoopHistogram:
    name: str

    def observe(self, value: float, labels: dict[str, str] | None = None) -> None:
        return None


class NoopMetricsRegistry:
    """Default no-op implementation.

    Used at Milestone 1 because real metrics exporters are deferred.
    Services can be tested with this registry without side effects.
    """

    def counter(
        self,
        name: str,
        *,
        unit: str | None = None,
        description: str | None = None,
        label_names: Sequence[str] | None = None,
    ) -> Counter:
        return _NoopCounter(name=name)

    def histogram(
        self,
        name: str,
        *,
        unit: str | None = None,
        description: str | None = None,
        buckets: Iterable[float] | None = None,
        label_names: Sequence[str] | None = None,
    ) -> Histogram:
        return _NoopHistogram(name=name)


__all__ = [
    "Counter",
    "Histogram",
    "MetricsRegistry",
    "NoopMetricsRegistry",
]
