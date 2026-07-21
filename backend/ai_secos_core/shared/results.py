"""Result type (Rust/Python-port idiom) for explicit success/failure.

Used by services that may fail in expected ways and want the
caller to handle both branches at the type system level.

For unexpected errors, raise an exception instead.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, Literal, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Success(Generic[T]):
    """Successful outcome carrying a value."""

    value: T

    @property
    def kind(self) -> Literal["ok"]:
        return "ok"


@dataclass(frozen=True)
class Failure:
    """Failed outcome carrying an error code and message (no exception).

    Use for *anticipated* failures; raise exceptions for programmer errors
    or unrecoverable platform states.
    """

    code: str
    message: str
    details: dict[str, Any]

    @property
    def kind(self) -> Literal["fail"]:
        return "fail"


Result = Success[T] | Failure  # type: ignore[valid-type]


def ok(value: T) -> Success[T]:
    return Success(value=value)


def fail(
    code: str,
    message: str,
    details: dict[str, Any] | None = None,
) -> Failure:
    return Failure(code=code, message=message, details=details or {})


def is_ok(result: Result[Any]) -> bool:
    return isinstance(result, Success)


def is_failure(result: Result[Any]) -> bool:
    return isinstance(result, Failure)


__all__ = [
    "Result",
    "Success",
    "Failure",
    "ok",
    "fail",
    "is_ok",
    "is_failure",
]
