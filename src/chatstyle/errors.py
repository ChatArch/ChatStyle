from __future__ import annotations

import click

from .constants import FORCE_INTERACTIVE_NO_TTY_MESSAGE


def abort_if_force_without_tty(
    force_interactive: bool, can_prompt: bool, usage: str
) -> None:
    if force_interactive and not can_prompt:
        raise click.ClickException(
            f"{FORCE_INTERACTIVE_NO_TTY_MESSAGE}\n{usage}"
        )


def abort_if_missing_without_tty(
    *,
    missing_required: bool,
    interactive: bool | None,
    can_prompt: bool,
    message: str,
    usage: str,
) -> None:
    if missing_required and (interactive is False or not can_prompt):
        raise click.ClickException(f"{message}\n{usage}")
