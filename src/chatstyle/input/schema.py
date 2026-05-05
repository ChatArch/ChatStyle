"""Declarative command input schema for interactive CLI commands."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Sequence


ValueValidator = Callable[[Any, dict[str, Any]], str | None]
ConstraintValidator = Callable[[dict[str, Any]], str | None]


@dataclass(frozen=True)
class CommandField:
    name: str
    prompt: str
    kind: str = "text"
    required: bool = False
    default: Any = None
    default_factory: Callable[[], Any] | None = None
    choices: Sequence[Any] = ()
    sensitive: bool = False
    prompt_if_missing: bool = False
    normalizer: Callable[[Any], Any] | None = None
    validator: ValueValidator | None = None
    missing_message: str | None = None

    def resolve_default(self):
        if self.default_factory is not None:
            return self.default_factory()
        return self.default


@dataclass(frozen=True)
class CommandConstraint:
    validator: ConstraintValidator
    message: str = ""


@dataclass(frozen=True)
class CommandSchema:
    name: str
    fields: Sequence[CommandField] = field(default_factory=tuple)
    constraints: Sequence[CommandConstraint] = field(default_factory=tuple)
