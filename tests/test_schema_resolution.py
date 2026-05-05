import click
import pytest

from chatstyle.resolve import resolve_command_inputs
from chatstyle.schema import CommandConstraint, CommandField, CommandSchema


def test_resolve_command_inputs_uses_defaults_without_prompt(monkeypatch):
    monkeypatch.setattr("chatstyle.interactive.is_interactive_available", lambda: False)
    schema = CommandSchema(
        name="demo",
        fields=(
            CommandField("name", prompt="name", required=True, default="rex"),
            CommandField("count", prompt="count", kind="int", default="2"),
        ),
    )

    values = resolve_command_inputs(
        schema=schema,
        provided={"name": None, "count": None},
        interactive=None,
        usage="Usage: demo",
    )

    assert values == {"name": "rex", "count": 2}


def test_resolve_command_inputs_prompts_when_missing(monkeypatch):
    monkeypatch.setattr("chatstyle.interactive.is_interactive_available", lambda: True)
    prompted = []

    def fake_ask_text(message, *, default="", password=False):
        prompted.append((message, default, password))
        return "alice"

    monkeypatch.setattr("chatstyle.prompt.ask_text", fake_ask_text)
    schema = CommandSchema(
        name="demo",
        fields=(CommandField("name", prompt="name", required=True),),
    )

    values = resolve_command_inputs(
        schema=schema,
        provided={"name": None},
        interactive=None,
        usage="Usage: demo",
    )

    assert values == {"name": "alice"}
    assert prompted == [("name", "", False)]


def test_resolve_command_inputs_force_non_interactive_errors(monkeypatch):
    monkeypatch.setattr("chatstyle.interactive.is_interactive_available", lambda: True)
    schema = CommandSchema(
        name="demo",
        fields=(CommandField("name", prompt="name", required=True),),
    )

    with pytest.raises(click.ClickException, match="Missing required value: name"):
        resolve_command_inputs(
            schema=schema,
            provided={"name": None},
            interactive=False,
            usage="Usage: demo",
        )


def test_resolve_command_inputs_errors_without_tty(monkeypatch):
    monkeypatch.setattr("chatstyle.interactive.is_interactive_available", lambda: False)
    schema = CommandSchema(
        name="demo",
        fields=(CommandField("name", prompt="name", required=True),),
    )

    with pytest.raises(click.ClickException, match="Missing required value: name"):
        resolve_command_inputs(
            schema=schema,
            provided={"name": None},
            interactive=None,
            usage="Usage: demo",
        )


def test_resolve_command_inputs_runs_constraint_validation(monkeypatch):
    monkeypatch.setattr("chatstyle.interactive.is_interactive_available", lambda: False)
    schema = CommandSchema(
        name="demo",
        fields=(
            CommandField("domain", prompt="domain"),
            CommandField("rr", prompt="rr"),
        ),
        constraints=(
            CommandConstraint(
                validator=lambda values: None
                if values.get("domain") or values.get("rr")
                else "Need domain or rr",
            ),
        ),
    )

    with pytest.raises(click.ClickException, match="Need domain or rr"):
        resolve_command_inputs(
            schema=schema,
            provided={"domain": None, "rr": None},
            interactive=False,
            usage="Usage: demo",
        )


def test_resolve_command_inputs_prompts_for_prompt_if_missing(monkeypatch):
    monkeypatch.setattr("chatstyle.interactive.is_interactive_available", lambda: True)

    def fake_ask_text(message, *, default="", password=False):
        assert message == "token"
        assert default == "cached"
        return "fresh"

    monkeypatch.setattr("chatstyle.prompt.ask_text", fake_ask_text)
    schema = CommandSchema(
        name="demo",
        fields=(
            CommandField(
                "token",
                prompt="token",
                default="cached",
                prompt_if_missing=True,
                sensitive=True,
            ),
        ),
    )

    values = resolve_command_inputs(
        schema=schema,
        provided={"token": None},
        interactive=None,
        usage="Usage: demo",
    )

    assert values == {"token": "fresh"}



def test_resolve_command_inputs_prompts_checkbox_kind(monkeypatch):
    monkeypatch.setattr("chatstyle.interactive.is_interactive_available", lambda: True)
    monkeypatch.setattr("chatstyle.prompt.ask_checkbox", lambda *args, **kwargs: ["a", "b"])
    schema = CommandSchema(
        name="demo",
        fields=(
            CommandField(
                "items",
                prompt="items",
                kind="checkbox",
                choices=("a", "b"),
                prompt_if_missing=True,
            ),
        ),
    )

    values = resolve_command_inputs(
        schema=schema,
        provided={"items": None},
        interactive=None,
        usage="Usage: demo",
    )

    assert values == {"items": ["a", "b"]}
