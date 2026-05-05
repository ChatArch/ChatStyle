from __future__ import annotations

from chatstyle.patterns import prompt_sensitive_value_with_mask, prompt_text_value, resolve_value


def test_resolve_value_preserves_false_and_zero():
    assert resolve_value(None, "", " value ") == " value "
    assert resolve_value(None, False, "fallback") is False
    assert resolve_value(None, 0, "fallback") == 0


def test_prompt_text_value_uses_first_candidate(monkeypatch):
    calls = []

    def fake_ask_text(label, default="", password=False):
        calls.append((label, default, password))
        return default

    monkeypatch.setattr("chatstyle.patterns.ask_text", fake_ask_text)

    assert prompt_text_value("Name", None, "demo") == "demo"
    assert calls == [("Name", "demo", False)]


def test_prompt_sensitive_value_with_mask_keeps_current(monkeypatch):
    monkeypatch.setattr("chatstyle.patterns.ask_text", lambda *args, **kwargs: "")

    assert (
        prompt_sensitive_value_with_mask("Token", "abcdefgh", lambda value: value[:2] + "****")
        == "abcdefgh"
    )
