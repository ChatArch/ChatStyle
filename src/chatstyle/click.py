from __future__ import annotations

import click


def add_interactive_option(func):
    """Attach the shared interactive option to a Click command."""
    return click.option(
        "--interactive/--no-interactive",
        "interactive",
        "-i/-I",
        default=None,
        help="Auto prompt on missing args, -i forces interactive, -I disables it.",
    )(func)
