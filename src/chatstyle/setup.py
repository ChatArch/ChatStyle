"""Setup-stage compatibility wrappers.

New code should prefer ``chatstyle.flow`` / ``chatstyle.output`` helpers.
The setup names remain as scenario wrappers because setup commands are a
common consumer, but this module does not execute installs or write config.
"""

from __future__ import annotations

from collections.abc import Iterable

from .flow import (
    render_commands,
    render_failure,
    render_flow_start,
    render_priority_chain,
    render_stage,
    render_success,
    render_warning,
)


def setup_start(name: str) -> None:
    render_flow_start(f"{name} setup", title="Setup")


def setup_stage(message: str) -> None:
    render_stage(message)


def setup_success(message: str) -> None:
    render_success(message)


def setup_warning(message: str) -> None:
    render_warning(message)


def setup_failure(message: str) -> None:
    render_failure(message)


def setup_suggested_commands(commands: Iterable[str], *, heading: str | None = None) -> None:
    """Print commands users should run manually when setup cannot execute them."""

    render_commands(commands, description=heading)


def setup_config_priority(items: Iterable[str]) -> None:
    render_priority_chain(items, label="Config priority")


__all__ = [
    "setup_config_priority",
    "setup_failure",
    "setup_stage",
    "setup_start",
    "setup_success",
    "setup_suggested_commands",
    "setup_warning",
]
