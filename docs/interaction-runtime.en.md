# Interaction Runtime

`chatstyle` extracts the most reusable interaction runtime pieces from ChatArch CLI practices while staying generic, lightweight, and reusable by Click CLI projects beyond ChatTool.

## Runtime Boundary

ChatStyle owns how generic CLI input is collected, validated, and displayed. It does not own what a product command does.

Included:

- Click `-i/-I` integration.
- TTY availability checks.
- Missing-argument prompting policy.
- Prompt, choice, confirm, and checkbox primitives.
- Defaults, secrets, field validation, and cross-field constraints.
- Common output, flow-stage display, and suggested command display.

Excluded:

- ChatTool or other product workflows.
- Concrete config file formats or writes.
- Remote API calls, installation logic, or environment checks.
- Business error parsing or product-specific recovery.

## Module Map

- `chatstyle.schema`: declares `CommandField`, `CommandSchema`, and `CommandConstraint`.
- `chatstyle.resolve`: merges explicit arguments, defaults, interactive prompts, and validation.
- `chatstyle.click`: provides Click integration helpers such as `add_interactive_option()`.
- `chatstyle.interactive`: detects TTY, normalizes interactive mode, and decides whether to prompt.
- `chatstyle.errors`: provides shared Click-facing abort and error helpers.
- `chatstyle.prompt`: provides text, path, confirm, select, and checkbox prompt primitives.
- `chatstyle.choice`: provides choice, separator, and questionary adapters.
- `chatstyle.mask`: masks secrets, formats current-secret hints, and prompts sensitive values.
- `chatstyle.output`: displays headings, notes, status lines, suggested commands, priority chains, and Rich/click fallback.
- `chatstyle.flow`: displays flow stages, results, and suggested commands.
- `chatstyle.constants`: stores shared `-i/-I` copy, `BACK_VALUE`, and checkbox indicators.

See [Modules](modules.md) for responsibilities, [Interaction Conventions](conventions.md) for behavior rules, and [Development Guide](development.md) for maintenance rules.

## CommandSchema Flow

Downstream projects should collect command inputs through one resolver flow:

1. Declare fields with `CommandField`.
2. Group fields and constraints with `CommandSchema`.
3. Keep recoverable Click options as `required=False`.
4. Add `-i/-I` with `@add_interactive_option`.
5. Call `resolve_command_inputs()` in the callback.
6. Run business logic only after the resolver returns complete values.

```python
import click

from chatstyle import CommandField, CommandSchema, add_interactive_option, resolve_command_inputs

SCHEMA = CommandSchema(
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
        schema=SCHEMA,
        provided={"name": name, "output": output},
        interactive=interactive,
        usage="Usage: demo [--name TEXT] [--output PATH] [-i|-I]",
    )
    click.echo(values["output"])
```

## Interactive Tri-State

- `interactive=True`: force interactive mode from `-i` or `--interactive`.
- `interactive=False`: disable prompting from `-I` or `--no-interactive`.
- `interactive=None`: automatic mode; prompt only when recoverable values are missing and TTY is available.

Non-TTY environments must fail fast instead of blocking. Automation should pass complete arguments or use `-I` to disable prompts.

## Dependency Strategy

- `click` is the core dependency.
- `questionary`, `prompt_toolkit`, and `rich` are optional dependencies.
- Optional dependencies must be imported lazily.
- Without optional dependencies, public APIs must remain importable and core flows must keep Click fallback behavior.

## Downstream Usage

- Depend on ChatStyle as an external package instead of copying source code.
- Keep business logic in the downstream command/service layer.
- Put only generic field collection, prompts, masking, and display helpers in the ChatStyle layer.
- Compatibility facades may delegate to `chatstyle`, but should not maintain a second implementation.
