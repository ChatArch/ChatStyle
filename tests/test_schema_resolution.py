import click
import pytest

from chatstyle.input import resolve_command_inputs
from chatstyle.input import CommandConstraint, CommandField, CommandSchema
from chatstyle.core import InteractiveResolution


def test_resolve_command_inputs_uses_defaults_without_prompt(monkeypatch):
    monkeypatch.setattr("chatstyle.core.interactive.is_interactive_available", lambda: False)
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


def test_required_default_prompts_when_value_missing_and_tty(monkeypatch):
    monkeypatch.setattr("chatstyle.core.interactive.is_interactive_available", lambda: True)
    prompted = []

    def fake_ask_text(message, *, default="", password=False):
        prompted.append((message, default, password))
        return "alice"

    monkeypatch.setattr("chatstyle.tui.prompt.ask_text", fake_ask_text)
    schema = CommandSchema(
        name="demo",
        fields=(CommandField("name", prompt="name", required=True, default="rex"),),
    )

    values = resolve_command_inputs(
        schema=schema,
        provided={"name": None},
        interactive=None,
        usage="Usage: demo",
    )

    assert values == {"name": "alice"}
    assert prompted == [("name", "rex", False)]


def test_resolve_command_inputs_prompts_when_missing(monkeypatch):
    monkeypatch.setattr("chatstyle.core.interactive.is_interactive_available", lambda: True)
    prompted = []

    def fake_ask_text(message, *, default="", password=False):
        prompted.append((message, default, password))
        return "alice"

    monkeypatch.setattr("chatstyle.tui.prompt.ask_text", fake_ask_text)
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


def test_resolve_command_inputs_respects_disabled_auto_prompt(monkeypatch):
    monkeypatch.setenv("CHATARCH_AUTO_PROMPT", "off")
    monkeypatch.setattr("chatstyle.core.interactive.is_interactive_available", lambda: True)
    monkeypatch.setattr(
        "chatstyle.tui.prompt.ask_text",
        lambda *args, **kwargs: pytest.fail("automatic prompt should be disabled"),
    )
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


def test_resolve_command_inputs_explicit_interactive_overrides_env(monkeypatch):
    monkeypatch.setenv("CHATARCH_AUTO_PROMPT", "off")
    monkeypatch.setattr("chatstyle.core.interactive.is_interactive_available", lambda: True)
    monkeypatch.setattr("chatstyle.tui.prompt.ask_text", lambda *args, **kwargs: "alice")
    schema = CommandSchema(
        name="demo",
        fields=(CommandField("name", prompt="name", required=True),),
    )

    values = resolve_command_inputs(
        schema=schema,
        provided={"name": None},
        interactive=True,
        usage="Usage: demo",
    )

    assert values == {"name": "alice"}


def test_resolve_command_inputs_force_non_interactive_errors(monkeypatch):
    monkeypatch.setattr("chatstyle.core.interactive.is_interactive_available", lambda: True)
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
    monkeypatch.setattr("chatstyle.core.interactive.is_interactive_available", lambda: False)
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
    monkeypatch.setattr("chatstyle.core.interactive.is_interactive_available", lambda: False)
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
    monkeypatch.setattr("chatstyle.core.interactive.is_interactive_available", lambda: True)

    def fake_ask_text(message, *, default="", password=False):
        assert message == "token"
        assert default == "cached"
        return "fresh"

    monkeypatch.setattr("chatstyle.tui.prompt.ask_text", fake_ask_text)
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
    monkeypatch.setattr("chatstyle.core.interactive.is_interactive_available", lambda: True)
    monkeypatch.setattr("chatstyle.tui.prompt.ask_checkbox", lambda *args, **kwargs: ["a", "b"])
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


def test_resolve_command_inputs_accepts_prompt_runtime_override(monkeypatch):
    monkeypatch.setattr("chatstyle.core.interactive.is_interactive_available", lambda: True)

    class Runtime:
        @staticmethod
        def ask_text(message, *, default="", password=False):
            assert message == "name"
            assert default == ""
            assert password is False
            return "adapter"

    schema = CommandSchema(
        name="demo",
        fields=(CommandField("name", prompt="name", required=True),),
    )

    values = resolve_command_inputs(
        schema=schema,
        provided={"name": None},
        interactive=None,
        usage="Usage: demo",
        prompt_runtime_override=Runtime,
    )

    assert values == {"name": "adapter"}


def test_resolve_command_inputs_accepts_interactive_resolver_override():
    def fake_resolver(*, interactive, auto_prompt_condition):
        assert interactive is None
        assert auto_prompt_condition is True
        return InteractiveResolution(
            interactive=None,
            can_prompt=True,
            force_interactive=False,
            need_prompt=True,
        )

    class Runtime:
        @staticmethod
        def ask_text(message, *, default="", password=False):
            return "adapter"

    schema = CommandSchema(
        name="demo",
        fields=(CommandField("name", prompt="name", required=True),),
    )

    values = resolve_command_inputs(
        schema=schema,
        provided={"name": None},
        interactive=None,
        usage="Usage: demo",
        prompt_runtime_override=Runtime,
        interactive_resolver_override=fake_resolver,
    )

    assert values == {"name": "adapter"}
