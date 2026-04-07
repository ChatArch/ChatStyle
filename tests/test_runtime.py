from chatstyle import mask_secret, resolve_interactive_mode


def test_mask_secret_keeps_tail():
    assert mask_secret("abcdefgh") == "****efgh"


def test_resolve_interactive_mode_auto_prompt_flag():
    state = resolve_interactive_mode(None, auto_prompt_condition=False)
    assert state.need_prompt is False
