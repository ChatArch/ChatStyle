from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import click


DEFAULT_TREE_HELP = "Print the registered CLI tree and exit."
DEFAULT_TREE_BRIEF_HELP = "Print the registered CLI tree without parameter signatures and exit."
DEFAULT_HELP_OPTION_HELP = "Show this message and exit."


def _format_metavar(name: str) -> str:
    return name.replace("_", "-").upper()


def _format_argument(param: click.Argument) -> str:
    metavar = _format_metavar(param.name or "ARG")
    if param.nargs == -1:
        metavar = f"{metavar}..."
    if not param.required:
        return f"[{metavar}]"
    return f"<{metavar}>"


def _format_option(param: click.Option, *, optional: bool = True, brief: bool = False) -> str:
    visible_opts = [opt for opt in param.opts if opt.startswith("--")]
    visible_opts.extend(opt for opt in param.secondary_opts if opt.startswith("--"))
    flag = visible_opts[0] if visible_opts else (param.opts[0] if param.opts else param.name or "OPTION")
    if brief or param.is_flag:
        label = flag
    else:
        label = f"{flag} {_format_metavar(param.name or 'VALUE')}"
    return f"[{label}]" if optional else label


def _command_signature(command: click.Command) -> str:
    parts: list[str] = []
    for param in command.params:
        if getattr(param, "hidden", False):
            continue
        if isinstance(param, click.Argument):
            parts.append(_format_argument(param))
        elif isinstance(param, click.Option):
            parts.append(_format_option(param))
    return " ".join(parts)


def _command_summary(command: click.Command) -> str:
    summary = (command.short_help or command.help or "").strip()
    return summary.splitlines()[0] if summary else ""


def _option_help(param: click.Option, overrides: Mapping[str, str]) -> str:
    for opt in [*param.opts, *param.secondary_opts]:
        if opt in overrides:
            return overrides[opt]
    return (param.help or "").strip()


def _root_option_items(
    root: click.Command,
    *,
    brief: bool,
    option_help_overrides: Mapping[str, str],
    help_option_help: str,
) -> list[tuple[str, str]]:
    items = [("--help", help_option_help)]
    for param in root.params:
        if not isinstance(param, click.Option) or getattr(param, "hidden", False):
            continue
        label = _format_option(param, optional=False, brief=brief)
        items.append((label, _option_help(param, option_help_overrides)))
    return items


def _group_items(group: click.Group) -> list[tuple[str, click.Command]]:
    ctx = click.Context(group)
    items: list[tuple[str, click.Command]] = []
    for name in group.list_commands(ctx):
        command = group.get_command(ctx, name)
        if command is None or command.hidden:
            continue
        items.append((name, command))
    return items


def render_click_tree(
    root: click.Command,
    *,
    root_name: str | None = None,
    brief: bool = False,
    include_root_options: bool = True,
    option_help_overrides: Mapping[str, str] | None = None,
    help_option_help: str = DEFAULT_HELP_OPTION_HELP,
) -> str:
    """Render a Click command/group tree from registered command metadata.

    The default output includes argument and option signatures for commands.
    Set ``brief=True`` to keep only command/option nodes and their summaries.
    """

    option_help_overrides = option_help_overrides or {}
    lines = [root_name or root.name or "cli"]

    def walk_command(name: str, command: click.Command, prefix: str, last: bool) -> None:
        branch = "└── " if last else "├── "
        child_prefix = prefix + ("    " if last else "│   ")
        signature = "" if brief else _command_signature(command)
        summary = _command_summary(command)
        label = f"{name} {signature}".strip()
        suffix = f"  # {summary}" if summary else ""
        lines.append(f"{prefix}{branch}{label}{suffix}")
        if isinstance(command, click.Group):
            walk_items(_group_items(command), child_prefix)

    def walk_items(items: list[tuple[str, Any]], prefix: str = "") -> None:
        for index, (name, item) in enumerate(items):
            last = index == len(items) - 1
            branch = "└── " if last else "├── "
            if isinstance(item, str):
                suffix = f"  # {item}" if item else ""
                lines.append(f"{prefix}{branch}{name}{suffix}")
            else:
                walk_command(name, item, prefix, last)

    entries: list[tuple[str, Any]] = []
    if include_root_options:
        entries.extend(_root_option_items(root, brief=brief, option_help_overrides=option_help_overrides, help_option_help=help_option_help))
    if isinstance(root, click.Group):
        entries.extend(_group_items(root))
    walk_items(entries)
    return "\n".join(lines)


def tree_callback(
    *,
    brief: bool = False,
    renderer_options: Mapping[str, Any] | None = None,
):
    """Return a Click option callback that prints a registered command tree."""

    renderer_options = renderer_options or {}

    def callback(ctx: click.Context, param: click.Option, value: bool) -> None:
        del param
        if not value or ctx.resilient_parsing:
            return
        if not isinstance(ctx.command, click.Command):
            raise click.ClickException("--tree is only available on Click commands")
        click.echo(render_click_tree(ctx.command, brief=brief, **renderer_options))
        ctx.exit()

    return callback


def add_tree_option(
    func=None,
    *,
    help: str = DEFAULT_TREE_HELP,
    brief_help: str = DEFAULT_TREE_BRIEF_HELP,
    option_names: tuple[str, ...] = ("--tree",),
    brief_option_names: tuple[str, ...] = ("--tree-brief",),
    include_brief_option: bool = True,
    renderer_options: Mapping[str, Any] | None = None,
):
    """Attach standard ``--tree`` and optional ``--tree-brief`` flags to a Click command."""

    def decorator(target):
        wrapped = target
        if include_brief_option:
            wrapped = click.option(
                *brief_option_names,
                is_flag=True,
                is_eager=True,
                expose_value=False,
                callback=tree_callback(brief=True, renderer_options=renderer_options),
                help=brief_help,
            )(wrapped)
        wrapped = click.option(
            *option_names,
            is_flag=True,
            is_eager=True,
            expose_value=False,
            callback=tree_callback(brief=False, renderer_options=renderer_options),
            help=help,
        )(wrapped)
        return wrapped

    if func is None:
        return decorator
    return decorator(func)
