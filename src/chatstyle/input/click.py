from __future__ import annotations

import click

from ..core import INTERACTIVE_OPTION_HELP


def add_interactive_option(func):
    """Attach the shared interactive option to a Click command."""
    return click.option(
        "--interactive/--no-interactive",
        "interactive",
        "-i/-I",
        default=None,
        help=INTERACTIVE_OPTION_HELP,
    )(func)
