import click
from click.testing import CliRunner

from chatstyle import (
    CommandField,
    CommandSchema,
    add_interactive_option,
    add_tree_option,
    render_click_tree,
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


@click.group(name="demo")
@click.version_option("1.0.0", prog_name="demo")
@add_tree_option
@click.option("--env", "env_profile", help="Environment profile.")
def tree_demo(env_profile):
    """Demo command tree."""


@tree_demo.command()
@click.argument("target", required=False)
@click.option("--force", is_flag=True, help="Force deployment.")
def deploy(target, force):
    """Deploy a target."""


@tree_demo.group()
def nested():
    """Nested command group."""


@nested.command()
@click.argument("items", nargs=-1)
def leaf(items):
    """Process nested items."""


@tree_demo.command(hidden=True)
def secret():
    """Hidden command."""


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
    monkeypatch.setattr("chatstyle.core.interactive.is_interactive_available", lambda: True)

    def fake_ask_text(message, *, default="", password=False):
        assert message == "name"
        return "alice"

    monkeypatch.setattr("chatstyle.tui.prompt.ask_text", fake_ask_text)
    result = runner.invoke(demo, ["-i"])

    assert result.exit_code == 0
    assert result.output.strip() == "name=alice count=1"


def test_click_command_default_flag_normalizes_to_auto(monkeypatch):
    runner = CliRunner()
    monkeypatch.setattr("chatstyle.core.interactive.is_interactive_available", lambda: True)

    def fake_ask_text(message, *, default="", password=False):
        return "bob"

    monkeypatch.setattr("chatstyle.tui.prompt.ask_text", fake_ask_text)
    result = runner.invoke(demo, [])

    assert result.exit_code == 0
    assert result.output.strip() == "name=bob count=1"


def test_render_click_tree_includes_command_signatures_by_default():
    output = render_click_tree(tree_demo)

    assert "demo" in output
    assert "--help  # Show this message and exit." in output
    assert "--version  # Show the version and exit." in output
    assert "--tree  # Print the registered CLI tree and exit." in output
    assert "--tree-brief  # Print the registered CLI tree without parameter signatures and exit." in output
    assert "--env ENV-PROFILE  # Environment profile." in output
    assert "deploy [TARGET] [--force]  # Deploy a target." in output
    assert "nested  # Nested command group." in output
    assert "leaf [ITEMS...]  # Process nested items." in output
    assert "secret" not in output


def test_render_click_tree_brief_omits_parameter_signatures():
    output = render_click_tree(tree_demo, brief=True)

    assert "deploy  # Deploy a target." in output
    assert "leaf  # Process nested items." in output
    assert "[TARGET]" not in output
    assert "[--force]" not in output
    assert "[ITEMS...]" not in output
    assert "--env  # Environment profile." in output


def test_tree_options_print_full_and_brief_trees():
    runner = CliRunner()

    full = runner.invoke(tree_demo, ["--tree"])
    brief = runner.invoke(tree_demo, ["--tree-brief"])

    assert full.exit_code == 0, full.output
    assert brief.exit_code == 0, brief.output
    assert "deploy [TARGET] [--force]  # Deploy a target." in full.output
    assert "leaf [ITEMS...]  # Process nested items." in full.output
    assert "deploy  # Deploy a target." in brief.output
    assert "leaf  # Process nested items." in brief.output
    assert "[TARGET]" not in brief.output
    assert "[ITEMS...]" not in brief.output
