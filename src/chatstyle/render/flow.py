"""Generic flow display helpers for multi-step CLI commands."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from .output import (
    render_heading,
    render_key_values,
    render_list,
    render_priority_chain,
    render_progress,
    render_status,
    render_success as _render_success,
    render_suggested_commands,
    render_warning as _render_warning,
)


def render_flow_start(name: str, *, title: str = "Flow") -> None:
    """Render the start of a named command flow."""

    render_heading(title, f"Start {name}")


def render_stage(message: str) -> None:
    """Render the current stage of a command flow."""

    render_status("info", message, err=True)


def render_progress_step(message: str) -> None:
    """Render an in-progress flow step."""

    render_progress(message)


def render_success(message: str) -> None:
    """Render a successful flow result."""

    _render_success(message)


def render_warning(message: str) -> None:
    """Render a recoverable warning."""

    _render_warning(message)


def render_failure(message: str) -> None:
    """Render a failure message."""

    render_status("failure", message, err=True)


def render_skip(message: str) -> None:
    """Render a skipped flow step."""

    render_status("skip", message, err=True)


def render_commands(
    commands: Iterable[str],
    *,
    heading: str = "Suggested Commands",
    description: str | None = None,
) -> None:
    """Render commands the user may run manually without executing them."""

    render_suggested_commands(commands, heading=heading, description=description)


def render_plan(steps: Iterable[str], *, heading: str = "Plan") -> None:
    """Render a planned sequence of actions without executing them."""

    render_list(steps, heading=heading, bullet="-")


def render_dry_run(steps: Iterable[str], *, heading: str = "Dry Run") -> None:
    """Render a dry-run plan."""

    render_list(steps, heading=heading, bullet="-")


def render_config_priority(items: Iterable[str]) -> None:
    """Render config source priority."""

    render_priority_chain(items, label="Config priority")


def render_config_sources(items: Mapping[str, Any] | Iterable[tuple[str, Any]]) -> None:
    """Render config source summary."""

    render_key_values(items, heading="Config Sources")


__all__ = [
    "render_commands",
    "render_config_priority",
    "render_config_sources",
    "render_dry_run",
    "render_failure",
    "render_flow_start",
    "render_plan",
    "render_priority_chain",
    "render_progress_step",
    "render_skip",
    "render_stage",
    "render_success",
    "render_warning",
]
