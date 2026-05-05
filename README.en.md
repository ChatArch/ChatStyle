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

## Install

Local development:

```bash
pip install -e /home/rexwzh/workspace/core/ChatStyle
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

## Local Checks

```bash
python -m pytest -q
python -m build
mkdocs build --strict
```
