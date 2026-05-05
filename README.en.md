<div align="center">
    <a href="https://pypi.python.org/pypi/chatstyle">
        <img src="https://img.shields.io/pypi/v/chatstyle.svg" alt="PyPI version" />
    </a>
    <a href="https://github.com/ChatArch/ChatStyle/actions/workflows/ci.yml">
        <img src="https://github.com/ChatArch/ChatStyle/actions/workflows/ci.yml/badge.svg" alt="Tests" />
    </a>
    <a href="https://chatarch.github.io/ChatStyle">
        <img src="https://img.shields.io/badge/docs-mkdocs-blue.svg" alt="Documentation" />
    </a>
</div>

<div align="center">

[English](README.en.md) | [简体中文](README.md)
</div>

# ChatStyle

ChatStyle is a reusable CLI interaction style and runtime package extracted from ChatTool practices. It provides prompt, choice, output, masking, setup display, interactive policy, and CommandSchema runtime helpers so new CLI projects can reuse consistent missing-argument prompting, `-i/-I`, TTY handling, defaults, and validation.

The current version remains `0.1.0` for local development and release preparation.

## Features

- `chatstyle.prompt`: text, path, confirm, select, and checkbox prompts.
- `chatstyle.choice`: choice, separator, and questionary fallback adapters.
- `chatstyle.output`: headings, notes, and Rich/click fallback display.
- `chatstyle.mask`: secret masking and sensitive input helpers.
- `chatstyle.setup`: setup-stage output, suggested commands, and config-priority display.
- `chatstyle.schema` / `chatstyle.resolve`: declarative command input schema and resolution.
- `chatstyle.click`: Click `-i/-I` option integration.
- `chatstyle.interactive` / `chatstyle.errors`: TTY, interactive policy, and error helpers.

## Sections

### Command Schema Runtime

`schema`, `resolve`, and `click` form the declarative command input layer. They handle field declaration, defaults, missing-argument prompting, field validation, cross-field constraints, and `-i/-I` integration.

### Prompt And Choice

`prompt` and `choice` provide text input, path input, confirmation, single select, checkbox selection, select-all controls, and choice/separator construction. `questionary` and `prompt_toolkit` are imported lazily; Click fallback keeps the package usable without them.

### Output And Setup

`output` provides common headings and notes with Rich/click fallback. `setup` provides setup wizard stage output, suggested commands, and config-priority display.

### Mask And Interactive Policy

`mask` handles secret masking and sensitive input. `interactive`, `errors`, and `constants` handle TTY detection, interactive state, shared copy, and error display.

## Install

Local development:

```bash
pip install -e ".[dev]"
```

Project dependency:

```toml
dependencies = ["chatstyle"]
```

## Minimal Example

```python
import click

from chatstyle import (
    CommandField,
    CommandSchema,
    add_interactive_option,
    resolve_command_inputs,
)


DEMO_SCHEMA = CommandSchema(
    name="demo",
    fields=(
        CommandField("name", prompt="name", required=True),
        CommandField("output", prompt="output path", kind="path", default="./out.txt"),
        CommandField("token", prompt="token", sensitive=True, prompt_if_missing=True),
    ),
)


@click.command()
@click.option("--name", required=False)
@click.option("--output", required=False)
@click.option("--token", required=False)
@add_interactive_option
def demo(name, output, token, interactive):
    values = resolve_command_inputs(
        schema=DEMO_SCHEMA,
        provided={"name": name, "output": output, "token": token},
        interactive=interactive,
        usage="Usage: demo [--name TEXT] [--output PATH] [--token TEXT] [-i|-I]",
    )
    click.echo(f"run demo for {values['name']} -> {values['output']}")
```

## Docs

```bash
pip install -e ".[docs]"
mkdocs serve
```

More docs:

- `docs/modules.en.md`: module sections and boundaries.
- `docs/conventions.en.md`: interaction conventions and behavior rules.
- `docs/development.en.md`: development and maintenance rules.
- `docs/interaction-runtime.en.md`: runtime boundaries and downstream usage.

## Local Checks

```bash
python -m pytest -q
python -m build
mkdocs build --strict
```
