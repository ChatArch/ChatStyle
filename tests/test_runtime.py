from chatstyle import (
    BACK_VALUE,
    INTERACTIVE_OPTION_HELP,
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


def test_normalize_interactive_keeps_explicit_flag():
    assert normalize_interactive(False) is False


def test_choice_and_constants_exports():
    assert BACK_VALUE == "__BACK__"
    assert "interactive" in INTERACTIVE_OPTION_HELP
    assert get_separator() == {"separator": True}
    choice = create_choice("Demo", "demo")
    assert getattr(choice, "value", None) == "demo" or choice["value"] == "demo"
