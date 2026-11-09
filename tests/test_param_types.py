"""Opt-in shared Click converters validate CLI, default and prompted inputs."""
from pathlib import Path
from types import SimpleNamespace

import click
import pytest

from chatstyle import CommandField, CommandSchema, resolve_command_inputs


def resolve(field, value, *, interactive=False, runtime=None):
    return resolve_command_inputs(
        schema=CommandSchema("demo", (field,)), provided={field.name: value},
        interactive=interactive, usage="Usage: demo [-i|-I]", prompt_runtime_override=runtime,
    )[field.name]


@pytest.mark.parametrize("value", ["4", 4])
def test_click_range_converts_supplied_values(value):
    field = CommandField("count", "Count", param_type=click.IntRange(1, 10))
    assert resolve(field, value) == 4


@pytest.mark.parametrize("value", ["bad", "0", "11"])
def test_click_range_rejects_supplied_values_cleanly(value):
    field = CommandField("count", "Count", param_type=click.IntRange(1, 10))
    with pytest.raises(click.ClickException, match="Count"):
        resolve(field, value)


def test_prompted_values_receive_the_same_click_range(monkeypatch):
    monkeypatch.setattr("chatstyle.core.interactive.is_interactive_available", lambda: True)
    field = CommandField("count", "Count", default=4, prompt_if_missing=True, param_type=click.IntRange(1, 10))
    runtime = SimpleNamespace(ask_text=lambda *args, **kwargs: "11")
    with pytest.raises(click.ClickException, match="Count"):
        resolve(field, None, interactive=True, runtime=runtime)


def test_click_choice_converts_to_canonical_spelling():
    field = CommandField("kind", "Kind", param_type=click.Choice(["Model", "Dataset"], case_sensitive=False))
    assert resolve(field, "dataset") == "Dataset"


def test_click_path_rejects_existing_file(tmp_path):
    path = tmp_path / "file"
    path.write_text("data")
    field = CommandField("directory", "Directory", param_type=click.Path(path_type=Path, file_okay=False))
    with pytest.raises(click.ClickException, match="Directory"):
        resolve(field, str(path))


def test_click_type_applies_to_defaults():
    field = CommandField("count", "Count", default="3", param_type=click.IntRange(1, 10))
    assert resolve(field, None) == 3


def test_sensitive_conversion_does_not_keep_raw_error_chain():
    value = "sensitive-canary-never-display"
    field = CommandField("number", "Number", sensitive=True, param_type=click.INT)
    with pytest.raises(click.ClickException) as exc:
        resolve(field, value)
    assert value not in str(exc.value)
    assert exc.value.__cause__ is None
    assert exc.value.__context__ is None


def test_zero_default_is_shown_and_accepted_as_zero(monkeypatch):
    monkeypatch.setattr("chatstyle.core.interactive.is_interactive_available", lambda: True)
    seen = []

    def accept(message, default="", **kwargs):
        seen.append(default)
        return default

    field = CommandField("count", "Count", default=0, prompt_if_missing=True, param_type=click.IntRange(0, 10))
    value = resolve(field, None, interactive=True, runtime=SimpleNamespace(ask_text=accept))
    assert seen == ["0"]
    assert value == 0
    assert isinstance(value, int)


def test_legacy_numeric_kind_fails_as_click_error_not_raw_valueerror():
    field = CommandField("count", "Count", kind="int")
    with pytest.raises(click.ClickException, match="Count"):
        resolve(field, "not-a-number")
