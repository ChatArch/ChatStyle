"""Opt-in example: a consumer shares ChatStyle policy and Click validation."""
import click
from chatstyle import CommandField, CommandSchema, add_interactive_option, resolve_command_inputs

COUNT = click.IntRange(1, 10)


@click.command()
@click.argument("resource", required=False)
@click.option("--count", type=COUNT, default=None)
@add_interactive_option
def example(resource: str | None, count: int | None, interactive: bool | None) -> None:
    values = resolve_command_inputs(
        schema=CommandSchema("example", (
            CommandField("resource", "Resource", required=True),
            CommandField("count", "Count", default=1, param_type=COUNT, prompt_if_missing=interactive is True),
        )),
        provided={"resource": resource, "count": count},
        interactive=interactive,
        usage="Usage: example [RESOURCE] [--count INTEGER] [-i|-I]",
    )
    for _ in range(values["count"]):
        click.echo(values["resource"])


if __name__ == "__main__":
    example()
