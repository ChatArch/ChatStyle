# chatstyle

Reusable CLI interaction and scaffold helpers extracted from ChatTool practices.

Current goal:

- collect reusable CLI interaction rules
- package common prompt / masking / interactive-mode helpers
- provide a light runtime that future `cli-style` scaffolds can depend on

Current extracted runtime includes:

- interactive mode resolution and TTY policy
- secret masking
- declarative command schema and constraint objects
- shared input resolver for Click-based commands
- shared `--interactive/--no-interactive` Click option helper
- minimal prompt primitives for text/path/confirm/select

Intentionally not extracted yet:

- complex product-specific TUI flows
- heavily customized checkbox controls
- ChatTool business helpers and command-specific orchestration

This repository is currently an extraction target. At this stage, code may be copied
from ChatTool first, then refined here before any upstream decoupling happens.

## Layout

- `src/`: reusable runtime code
- `tests/`: lightweight package tests
- `docs/`: long-lived package notes
- `.github/workflows/`: CI and publish automation skeleton

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
    ),
)


@click.command()
@click.option("--name", required=False)
@click.option("--output", required=False)
@add_interactive_option
def demo(name, output, interactive):
    values = resolve_command_inputs(
        schema=DEMO_SCHEMA,
        provided={"name": name, "output": output},
        interactive=interactive,
        usage="Usage: demo [--name TEXT] [--output PATH] [-i|-I]",
    )
    click.echo(f"run demo for {values['name']} -> {values['output']}")
```

## Local Checks

```bash
python -m pytest -q
python -m build
```
