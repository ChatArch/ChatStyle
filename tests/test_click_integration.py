import click
from click.testing import CliRunner

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
        CommandField("count", prompt="count", kind="int", default="1"),
    ),
)


@click.command()
@click.option("--name", required=False)
@click.option("--count", required=False)
@add_interactive_option
def demo(name, count, interactive):
    values = resolve_command_inputs(
        schema=DEMO_SCHEMA,
        provided={"name": name, "count": count},
        interactive=interactive,
        usage="Usage: demo [--name TEXT] [--count INTEGER] [-i|-I]",
    )
    click.echo(f"name={values['name']} count={values['count']}")


def test_click_command_accepts_explicit_values():
    runner = CliRunner()
    result = runner.invoke(demo, ["--name", "rex", "--count", "3"])

    assert result.exit_code == 0
    assert result.output.strip() == "name=rex count=3"


def test_click_command_uses_no_interactive_flag():
    runner = CliRunner()
    result = runner.invoke(demo, ["-I"])

    assert result.exit_code != 0
    assert "Missing required value: name" in result.output


def test_click_command_prompts_with_interactive_flag(monkeypatch):
    runner = CliRunner()
    monkeypatch.setattr("chatstyle.interactive.is_interactive_available", lambda: True)

    def fake_ask_text(message, *, default="", password=False):
        assert message == "name"
        return "alice"

    monkeypatch.setattr("chatstyle.prompt.ask_text", fake_ask_text)
    result = runner.invoke(demo, ["-i"])

    assert result.exit_code == 0
    assert result.output.strip() == "name=alice count=1"


def test_click_command_default_flag_normalizes_to_auto(monkeypatch):
    runner = CliRunner()
    monkeypatch.setattr("chatstyle.interactive.is_interactive_available", lambda: True)

    def fake_ask_text(message, *, default="", password=False):
        return "bob"

    monkeypatch.setattr("chatstyle.prompt.ask_text", fake_ask_text)
    result = runner.invoke(demo, [])

    assert result.exit_code == 0
    assert result.output.strip() == "name=bob count=1"
