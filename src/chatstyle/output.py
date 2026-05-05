"""Rendering helpers for CLI interaction."""

from __future__ import annotations

from collections.abc import Iterable

import click


_STATUS_LABELS = {
    "info": "INFO",
    "success": "OK",
    "warning": "WARN",
    "error": "ERROR",
    "failure": "ERROR",
}


def get_style():
    """Compatibility shim for older questionary-based callers."""
    return None


def _get_console():
    try:
        from rich.console import Console
    except ImportError:  # pragma: no cover - optional dependency fallback
        return None
    return Console(stderr=True)


def render_heading(title: str, subtitle: str | None = None) -> None:
    """Render a generic CLI section heading."""

    console = _get_console()
    if not console:
        if subtitle:
            click.echo(f"\n{title}\n{subtitle}", err=True)
        else:
            click.echo(f"\n{title}", err=True)
        return

    try:
        from rich.panel import Panel
    except ImportError:  # pragma: no cover - optional dependency fallback
        if subtitle:
            click.echo(f"\n{title}\n{subtitle}", err=True)
        else:
            click.echo(f"\n{title}", err=True)
        return

    console.print(
        Panel.fit(
            subtitle or "",
            title=f"[bold cyan]{title}[/bold cyan]",
            border_style="cyan",
            padding=(0, 1),
        )
    )


def render_note(message: str) -> None:
    """Render a low-emphasis note."""

    console = _get_console()
    if not console:
        click.echo(message, err=True)
        return
    console.print(f"[dim]{message}[/dim]")


def render_status(kind: str, message: str, *, err: bool | None = None) -> None:
    """Render a business-neutral status line.

    ``kind`` is intentionally small and generic; downstream projects own
    product-specific meaning and recovery suggestions.
    """

    normalized = kind.lower()
    label = _STATUS_LABELS.get(normalized, normalized.upper())
    if err is None:
        err = normalized in {"warning", "error", "failure"}
    click.echo(f"[{label}] {message}", err=err)


def render_suggested_commands(
    commands: Iterable[str],
    *,
    heading: str = "Suggested Commands",
    description: str | None = None,
) -> None:
    """Render commands the user may run manually.

    The helper only prints commands. It never executes them.
    """

    render_heading(heading, description)
    for command in commands:
        click.echo(command)


def render_priority_chain(items: Iterable[str], *, label: str = "Priority") -> None:
    """Render a generic priority chain such as CLI > env > config > default."""

    render_note(f"{label}: " + " > ".join(items))


_render_heading = render_heading
_render_note = render_note


__all__ = [
    "get_style",
    "render_heading",
    "render_note",
    "render_priority_chain",
    "render_status",
    "render_suggested_commands",
]
