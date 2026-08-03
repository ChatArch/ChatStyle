import pytest

from chatstyle import (
    AUTO_PROMPT_ENV_VAR,
    BACK_VALUE,
    INTERACTIVE_OPTION_HELP,
    auto_prompt_enabled,
    create_choice,
    get_separator,
    mask_secret,
    normalize_interactive,
    resolve_interactive_mode,
)


def test_mask_secret_keeps_recognizable_shape():
    assert mask_secret("abcdefgh") == "ab****gh"
    assert mask_secret("ab") == "**"


def test_resolve_interactive_mode_auto_prompt_flag():
    state = resolve_interactive_mode(None, auto_prompt_condition=False)
    assert state.need_prompt is False


@pytest.mark.parametrize("value", ["0", "false", "FALSE", " no ", "off", "OFF"])
def test_auto_prompt_false_values(monkeypatch, value):
    monkeypatch.setenv(AUTO_PROMPT_ENV_VAR, value)

    assert auto_prompt_enabled() is False


def test_auto_prompt_defaults_to_enabled(monkeypatch):
    monkeypatch.delenv(AUTO_PROMPT_ENV_VAR, raising=False)

    assert auto_prompt_enabled() is True


def test_auto_prompt_env_disables_automatic_mode(monkeypatch):
    monkeypatch.setenv(AUTO_PROMPT_ENV_VAR, "false")
    monkeypatch.setattr("chatstyle.core.interactive.is_interactive_available", lambda: True)

    state = resolve_interactive_mode(
        None,
        auto_prompt_condition=True,
        respect_auto_prompt_env=True,
    )

    assert state.need_prompt is False
    assert state.force_interactive is False


def test_explicit_interactive_overrides_auto_prompt_env(monkeypatch):
    monkeypatch.setenv(AUTO_PROMPT_ENV_VAR, "false")
    monkeypatch.setattr("chatstyle.core.interactive.is_interactive_available", lambda: True)

    state = resolve_interactive_mode(
        True,
        auto_prompt_condition=True,
        respect_auto_prompt_env=True,
    )

    assert state.need_prompt is True
    assert state.force_interactive is True


def test_low_level_resolver_keeps_legacy_default(monkeypatch):
    monkeypatch.setenv(AUTO_PROMPT_ENV_VAR, "false")
    monkeypatch.setattr("chatstyle.core.interactive.is_interactive_available", lambda: True)

    state = resolve_interactive_mode(None, auto_prompt_condition=True)

    assert state.need_prompt is True


def test_normalize_interactive_keeps_explicit_flag():
    assert normalize_interactive(False) is False


def test_choice_and_constants_exports():
    assert BACK_VALUE == "__BACK__"
    assert "interactive" in INTERACTIVE_OPTION_HELP
    assert get_separator() == {"separator": True}
    choice = create_choice("Demo", "demo")
    assert getattr(choice, "value", None) == "demo" or choice["value"] == "demo"
