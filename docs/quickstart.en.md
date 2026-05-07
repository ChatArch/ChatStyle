# Quickstart

This guide shows how downstream projects can add ChatStyle to a new Click CLI and wrap new interaction interfaces. The examples stay business-neutral and are suitable as a starting point after `chattool pypi init`.

## Install Dependencies

For local ChatStyle development:

```bash
pip install -e /home/rexwzh/workspace/core/ChatStyle
```

For downstream package dependencies:

```toml
dependencies = [
  "click>=8.0",
  "chatstyle>=0.1.0",
]
```

## Add A New CLI Command

Use `CommandSchema` for recoverable inputs. Keep Click options non-required, then let `resolve_command_inputs()` handle missing-argument prompts, defaults, validation, `-i/-I`, and non-TTY behavior.

Use this end-to-end path when adding a command:

1. Declare non-required Click options / arguments; Click only receives explicit input.
2. Describe each field with `CommandField`: prompt copy, kind, default, sensitivity, required flag, and field validator.
3. Describe cross-field rules with `CommandConstraint`, such as "remote mode requires a token".
4. Add `@add_interactive_option` to wire `--interactive/--no-interactive` and `-i/-I`.
5. In the callback, call `resolve_command_inputs()` with Click values, the schema, interactive mode, and usage text.
6. Run business logic only after the resolver returns complete values; network calls, file writes, and domain decisions stay outside ChatStyle.

```python
# src/demoapp/cli.py
from __future__ import annotations

import click

from chatstyle import (
    CommandConstraint,
    CommandField,
    CommandSchema,
    add_interactive_option,
    render_success,
    resolve_command_inputs,
)


def _validate_name(value, _values):
    if len(value) < 2:
        return "name must contain at least 2 characters"
    return None


def _require_token_for_remote(values):
    if values.get("mode") == "remote" and not values.get("token"):
        return "token is required when mode is remote"
    return None


CREATE_SCHEMA = CommandSchema(
    name="create",
    fields=(
        CommandField("name", prompt="Project name", required=True, validator=_validate_name),
        CommandField("path", prompt="Output path", kind="path", default="./demo"),
        CommandField("mode", prompt="Mode", kind="select", choices=("local", "remote"), default="local"),
        CommandField("token", prompt="API token", sensitive=True, prompt_if_missing=False),
        CommandField("yes", prompt="Continue", kind="confirm", default=True),
    ),
    constraints=(CommandConstraint(_require_token_for_remote),),
)


@click.group()
def cli():
    pass


@cli.command()
@click.option("--name")
@click.option("--path")
@click.option("--mode")
@click.option("--token")
@click.option("--yes/--no", default=None)
@add_interactive_option
def create(name, path, mode, token, yes, interactive):
    values = resolve_command_inputs(
        schema=CREATE_SCHEMA,
        provided={"name": name, "path": path, "mode": mode, "token": token, "yes": yes},
        interactive=interactive,
        usage="Usage: demo create [--name TEXT] [--path PATH] [--mode local|remote] [-i|-I]",
    )
    render_success(f"Created {values['name']} at {values['path']}")
```

Run it with:

```bash
demo create --name alpha -I
demo create -i
demo create --mode remote --token "$TOKEN"
```

## Where Fallback Happens

ChatStyle has several fallback layers, each with a different responsibility:

| Layer | Location | Responsibility |
| --- | --- | --- |
| Value-source fallback | `chatstyle.input.resolve.resolve_command_inputs()` | Uses `CommandField.default` / `default_factory` when explicit input is missing; `required` / `prompt_if_missing` decide whether a missing field prompts. |
| Interactive policy fallback | `chatstyle.core.interactive.resolve_interactive_mode()` | `interactive=None` is automatic mode: prompt only when TTY is available and recoverable missing fields or initial validation errors exist; `-I` disables prompts; `-i` forces prompts. |
| Non-TTY fallback | `chatstyle.input.resolve.resolve_command_inputs()` + `chatstyle.core.errors` | Never blocks without a TTY; fields with defaults can continue, while required fields without defaults fail fast with usage. |
| TUI dependency fallback | `chatstyle.tui.prompt` | When `questionary` / `prompt_toolkit` are unavailable, `ask_select()`, `ask_checkbox()`, and similar helpers fall back to Click text prompts. |
| Output fallback | `chatstyle.render.output` | When `rich` is unavailable, headings, status lines, tables, and suggested commands fall back to `click.echo()`. |
| Business-wrapper fallback | Downstream `ui.py` / `config.py` | Environment variables, config files, existing tokens, and business priority chains should be resolved downstream, then passed to ChatStyle as `provided` values or `default_factory`. |

`required=True` does not mean "has no default". A required field without a default must be provided or prompted. A required field with a default means "when explicit input is missing, automatic TTY mode should still prompt so the user can confirm or override the default". In `-I` or non-TTY mode, the default remains the automation fallback.

## Add Checkbox Input

Use `checkbox` fields for plugins, templates, feature flags, and other multi-select inputs:

```python
FEATURE_SCHEMA = CommandSchema(
    name="features",
    fields=(
        CommandField(
            "features",
            prompt="Select features",
            kind="checkbox",
            choices=("docs", "tests", "ci"),
            default=("tests",),
            prompt_if_missing=True,
        ),
    ),
)
```

## Wrap A New Interaction Interface

Downstream projects can compose ChatStyle primitives into business-specific interfaces. The wrapper may know business meaning; ChatStyle itself should not.

```python
# src/demoapp/ui.py
from __future__ import annotations

from chatstyle import (
    create_choice,
    get_separator,
    mask_secret,
    prompt_sensitive_value,
    render_key_values,
    render_stage,
)
from chatstyle.tui import ask_select


def ask_environment(default="dev"):
    value = ask_select(
        "Environment",
        [
            create_choice("Development", "dev", checked=default == "dev"),
            create_choice("Production", "prod", checked=default == "prod"),
            get_separator(),
            create_choice("Cancel", "cancel"),
        ],
    )
    return value


def ask_api_token(current_token=None):
    return prompt_sensitive_value("API token", current_token)


def render_config_preview(config):
    render_stage("Config preview")
    safe_config = {**config, "token": mask_secret(config.get("token"))}
    render_key_values(safe_config)
```

## Recommended Rules

- Do not mark recoverable Click options as `required=True`.
- Use `-I` for automation and `-i` for manual repair or initialization.
- Sensitive fields must use password prompts and must be masked before output.
- Prefer schema `default` / `default_factory` for defaults; downstream projects should resolve business-specific config priority before passing values to ChatStyle.
- Use `required=True` with a default when the user should confirm or override that default; omit `required` when the default should be used silently.
- Downstream projects may wrap `ask_xxx()` / `render_xxx()`, but business logic, network calls, and file writes stay outside ChatStyle.
- Use `chatstyle.render` for stages, plans, dry runs, and suggested commands in long-running flows.
