"""Business-neutral rendering helpers for ChatArch CLI tools."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

import click


_STATUS_LABELS = {
    "info": "INFO",
    "progress": "...",
    "success": "OK",
    "warning": "WARN",
    "error": "ERROR",
    "failure": "ERROR",
    "skip": "SKIP",
    "skipped": "SKIP",
}
_STATUS_ERR_DEFAULT = {"info", "progress", "warning", "error", "failure", "skip", "skipped"}


@dataclass(frozen=True)
class TableColumn:
    """Column definition for simple terminal tables."""

    key: str
    title: str | None = None

    @property
    def label(self) -> str:
        return self.title or self.key


def get_style():
    """Compatibility shim for older questionary-based callers."""
    return None


def _get_console():
    try:
        from rich.console import Console
    except ImportError:  # pragma: no cover - optional dependency fallback
        return None
    return Console(stderr=True)


def _echo_lines(lines: Iterable[str], *, err: bool = True) -> None:
    for line in lines:
        click.echo(line, err=err)


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


def render_section(title: str, subtitle: str | None = None) -> None:
    """Alias for rendering a section heading."""

    render_heading(title, subtitle)


def render_step(title: str, detail: str | None = None) -> None:
    """Render a step title for a multi-step CLI flow."""

    render_heading(title, detail)


def render_note(message: str) -> None:
    """Render a low-emphasis note."""

    console = _get_console()
    if not console:
        click.echo(message, err=True)
        return
    console.print(f"[dim]{message}[/dim]")


def render_status(kind: str, message: str, *, err: bool | None = None) -> None:
    """Render a business-neutral status line."""

    normalized = kind.lower()
    label = _STATUS_LABELS.get(normalized, normalized.upper())
    if err is None:
        err = normalized in _STATUS_ERR_DEFAULT
    click.echo(f"[{label}] {message}", err=err)


def render_info(message: str) -> None:
    render_status("info", message)


def render_progress(message: str) -> None:
    render_status("progress", message)


def render_success(message: str) -> None:
    render_status("success", message, err=False)


def render_warning(message: str) -> None:
    render_status("warning", message, err=True)


def render_error(message: str) -> None:
    render_status("error", message, err=True)


def render_skip(message: str) -> None:
    render_status("skip", message, err=True)


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

    render_note(f"{label}: " + " > ".join(str(item) for item in items))


def render_key_values(
    items: Mapping[str, Any] | Iterable[tuple[str, Any]],
    *,
    heading: str | None = None,
    err: bool = False,
) -> None:
    """Render key-value pairs with stable alignment."""

    pairs = list(items.items() if isinstance(items, Mapping) else items)
    if heading:
        render_heading(heading)
    if not pairs:
        click.echo("(none)", err=err)
        return
    width = max(len(str(key)) for key, _ in pairs)
    for key, value in pairs:
        click.echo(f"{str(key).ljust(width)} : {value}", err=err)


def render_list(
    items: Iterable[Any],
    *,
    heading: str | None = None,
    bullet: str = "-",
    err: bool = False,
) -> None:
    """Render a simple bullet list."""

    values = list(items)
    if heading:
        render_heading(heading)
    if not values:
        click.echo("(none)", err=err)
        return
    for item in values:
        click.echo(f"{bullet} {item}", err=err)


def _row_value(row: Mapping[str, Any] | Sequence[Any], column: TableColumn, index: int) -> str:
    if isinstance(row, Mapping):
        return str(row.get(column.key, ""))
    if index < len(row):
        return str(row[index])
    return ""


def render_table(
    rows: Iterable[Mapping[str, Any] | Sequence[Any]],
    columns: Sequence[TableColumn | tuple[str, str] | str],
    *,
    heading: str | None = None,
    err: bool = False,
) -> None:
    """Render a plain text table with deterministic widths."""

    normalized_columns = [
        col
        if isinstance(col, TableColumn)
        else TableColumn(col[0], col[1])
        if isinstance(col, tuple)
        else TableColumn(str(col))
        for col in columns
    ]
    materialized = list(rows)
    if heading:
        render_heading(heading)
    if not normalized_columns:
        click.echo("(no columns)", err=err)
        return
    table_rows = [
        [_row_value(row, column, index) for index, column in enumerate(normalized_columns)]
        for row in materialized
    ]
    widths = [len(column.label) for column in normalized_columns]
    for row in table_rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))
    header = "  ".join(column.label.ljust(widths[index]) for index, column in enumerate(normalized_columns))
    divider = "  ".join("-" * width for width in widths)
    click.echo(header, err=err)
    click.echo(divider, err=err)
    for row in table_rows:
        click.echo("  ".join(value.ljust(widths[index]) for index, value in enumerate(row)), err=err)


def render_summary(
    title: str,
    items: Mapping[str, Any] | Iterable[tuple[str, Any]],
    *,
    err: bool = False,
) -> None:
    """Render a titled key-value summary block."""

    render_key_values(items, heading=title, err=err)


def render_error_block(message: str, *, usage: str | None = None, details: Iterable[str] = ()) -> None:
    """Render a readable CLI error block without raising an exception."""

    render_error(message)
    for detail in details:
        click.echo(f"  - {detail}", err=True)
    if usage:
        click.echo(usage, err=True)


_render_heading = render_heading
_render_note = render_note


__all__ = [
    "TableColumn",
    "get_style",
    "render_error",
    "render_error_block",
    "render_heading",
    "render_info",
    "render_key_values",
    "render_list",
    "render_note",
    "render_priority_chain",
    "render_progress",
    "render_section",
    "render_skip",
    "render_status",
    "render_step",
    "render_success",
    "render_suggested_commands",
    "render_summary",
    "render_table",
    "render_warning",
]
