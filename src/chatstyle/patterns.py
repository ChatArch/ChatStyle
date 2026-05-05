"""Reusable input-resolution patterns for CLI commands."""

from __future__ import annotations

from typing import Any, Callable

from .tui import ask_text


MaskFunction = Callable[[str], str]


def resolve_value(*candidates: Any) -> Any:
    """Return the first usable value from candidates.

    ``None`` and blank strings are missing; ``False`` and ``0`` remain valid.
    """

    for candidate in candidates:
        if candidate is None:
            continue
        if isinstance(candidate, str) and not candidate.strip():
            continue
        return candidate
    return None


def prompt_sensitive_value_with_mask(
    label: str,
    current_value: str | None,
    mask_fn: MaskFunction,
) -> str | None:
    """Prompt for a sensitive value while allowing Enter to keep the current one."""

    prompt_label = label
    if current_value:
        prompt_label = f"{label} (current: {mask_fn(current_value)}, enter to keep)"
    entered = ask_text(prompt_label, password=True)
    if entered:
        return entered
    return current_value


def prompt_text_value(label: str, *candidates: Any, fallback: str = "") -> str:
    """Prompt for text using the first usable candidate as default."""

    default_value = resolve_value(*candidates)
    if default_value is None:
        default_value = fallback
    return ask_text(label, default=str(default_value))


__all__ = [
    "prompt_sensitive_value_with_mask",
    "prompt_text_value",
    "resolve_value",
]
