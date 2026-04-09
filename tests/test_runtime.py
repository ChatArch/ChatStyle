from chatstyle import mask_secret, normalize_interactive, resolve_interactive_mode


def test_mask_secret_keeps_tail():
    assert mask_secret("abcdefgh") == "****efgh"


def test_resolve_interactive_mode_auto_prompt_flag():
    state = resolve_interactive_mode(None, auto_prompt_condition=False)
    assert state.need_prompt is False


def test_normalize_interactive_keeps_explicit_flag():
    assert normalize_interactive(False) is False
