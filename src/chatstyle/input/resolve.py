from __future__ import annotations

from typing import Any

import click

from ..core import abort_if_force_without_tty
from ..core import resolve_interactive_mode
from ..tui import prompt as prompt_runtime
from .schema import CommandField, CommandSchema

PromptRuntime = Any
InteractiveResolver = Any


def _is_empty(value: Any) -> bool:
    return value is None or value == "" or value == () or value == []


def _normalize_field_value(field: CommandField, value: Any):
    if _is_empty(value):
        return value
    if field.kind == "int" and not isinstance(value, int):
        value = int(value)
    if field.kind == "float" and not isinstance(value, float):
        value = float(value)
    if field.normalizer is not None:
        value = field.normalizer(value)
    return value


def _prompt_for_field(field: CommandField, current: Any, runtime: PromptRuntime):
    default = current if not _is_empty(current) else field.resolve_default()
    if field.kind == "select":
        if not field.choices:
            raise click.ClickException(f"Field '{field.name}' is missing choices.")
        return runtime.ask_select(field.prompt, list(field.choices))
    if field.kind == "checkbox":
        return runtime.ask_checkbox(
            field.prompt, list(field.choices), default_values=default or []
        )
    if field.kind == "confirm":
        return runtime.ask_confirm(
            field.prompt, default=bool(default) if default is not None else True
        )
    if field.kind == "path":
        return runtime.ask_path(field.prompt, default=str(default or ""))
    return runtime.ask_text(
        field.prompt,
        default=str(default or ""),
        password=field.sensitive,
    )


def _collect_errors(schema: CommandSchema, values: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in schema.fields:
        value = values.get(field.name)
        if field.required and _is_empty(value):
            errors.append(
                field.missing_message or f"Missing required value: {field.name}"
            )
            continue
        if field.validator is None or _is_empty(value):
            continue
        message = field.validator(value, values)
        if message:
            errors.append(message)

    for constraint in schema.constraints:
        message = constraint.validator(values)
        if message:
            errors.append(constraint.message or message)
    return errors


def resolve_command_inputs(
    *,
    schema: CommandSchema,
    provided: dict[str, Any],
    interactive: bool | None,
    usage: str,
    prompt_runtime_override: PromptRuntime | None = None,
    interactive_resolver_override: InteractiveResolver | None = None,
) -> dict[str, Any]:
    values: dict[str, Any] = {}
    missing_before_defaults: set[str] = set()
    for field in schema.fields:
        raw = provided.get(field.name)
        if _is_empty(raw):
            missing_before_defaults.add(field.name)
        if _is_empty(raw):
            raw = field.resolve_default()
        values[field.name] = _normalize_field_value(field, raw)

    promptable_missing = [
        field
        for field in schema.fields
        if field.name in missing_before_defaults
        and (field.required or field.prompt_if_missing)
    ]
    initial_errors = _collect_errors(schema, values)

    resolver = interactive_resolver_override or resolve_interactive_mode
    resolution = resolver(
        interactive=interactive,
        auto_prompt_condition=bool(promptable_missing or initial_errors),
    )
    abort_if_force_without_tty(
        resolution.force_interactive,
        resolution.can_prompt,
        usage,
    )

    if initial_errors and resolution.interactive is False:
        raise click.ClickException(initial_errors[0])
    if initial_errors and resolution.interactive is None and not resolution.can_prompt:
        raise click.ClickException(f"{initial_errors[0]}\n{usage}")

    runtime = prompt_runtime_override or prompt_runtime
    if resolution.need_prompt:
        for field in schema.fields:
            current = values.get(field.name)
            should_prompt = field.name in missing_before_defaults and (
                field.required or field.prompt_if_missing
            )
            if not should_prompt:
                continue
            prompted = _prompt_for_field(field, current, runtime)
            values[field.name] = _normalize_field_value(field, prompted)

    final_errors = _collect_errors(schema, values)
    if final_errors:
        raise click.ClickException(final_errors[0])
    return values
