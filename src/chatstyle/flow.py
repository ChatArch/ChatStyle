"""Generic flow display helpers for multi-step CLI commands."""

from __future__ import annotations

from collections.abc import Iterable

from .output import (
    render_heading,
    render_priority_chain,
    render_status,
    render_suggested_commands as _render_suggested_commands,
)


def render_flow_start(name: str, *, title: str = "Flow") -> None:
    """Render the start of a named command flow."""

    render_heading(title, f"Start {name}")


def render_stage(message: str) -> None:
    """Render the current stage of a command flow."""

    render_status("info", message, err=True)


def render_success(message: str) -> None:
    """Render a successful flow result."""

    render_status("success", message, err=False)


def render_warning(message: str) -> None:
    """Render a recoverable warning."""

    render_status("warning", message, err=True)


def render_failure(message: str) -> None:
    """Render a failure message."""

    render_status("failure", message, err=True)


def render_commands(
    commands: Iterable[str],
    *,
    heading: str = "Suggested Commands",
    description: str | None = None,
) -> None:
    """Render commands the user may run manually without executing them."""

    _render_suggested_commands(commands, heading=heading, description=description)


__all__ = [
    "render_commands",
    "render_failure",
    "render_flow_start",
    "render_priority_chain",
    "render_stage",
    "render_success",
    "render_warning",
]
