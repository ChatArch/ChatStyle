from __future__ import annotations

import click

from chatstyle.mask import format_current_secret, prompt_sensitive_value
from chatstyle.prompt import ask_checkbox, ask_select
from chatstyle.output import render_suggested_commands


def test_ask_select_click_fallback(monkeypatch):
    real_import = __import__

    def fake_import(name, *args, **kwargs):
        if name == "questionary":
            raise ImportError(name)
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", fake_import)
    monkeypatch.setattr(click, "prompt", lambda *args, **kwargs: 2)

    assert ask_select("Pick one", ["a", "b"]) == "b"


def test_ask_checkbox_click_fallback(monkeypatch):
    real_import = __import__

    def fake_import(name, *args, **kwargs):
        if name == "questionary":
            raise ImportError(name)
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", fake_import)
    monkeypatch.setattr(click, "prompt", lambda *args, **kwargs: "1,3")

    selected = ask_checkbox("Pick many", ["a", "b", "c"])

    assert selected == ["a", "c"]


def test_prompt_sensitive_value_keeps_current(monkeypatch):
    monkeypatch.setattr("chatstyle.mask.ask_text", lambda *args, **kwargs: "")

    assert format_current_secret("abcdefgh") == "current: ab****gh"
    assert prompt_sensitive_value("token", "abcdefgh") == "abcdefgh"


def test_render_suggested_commands_outputs_commands(capsys):
    render_suggested_commands(["sudo systemctl restart demo"], description="Run manually")

    captured = capsys.readouterr()
    assert "Suggested Commands" in captured.err
    assert "sudo systemctl restart demo" in captured.out
