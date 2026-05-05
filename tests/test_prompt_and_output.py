from __future__ import annotations

import click

from chatstyle.security import format_current_secret, prompt_sensitive_value
from chatstyle.tui import ask_checkbox, ask_checkbox_with_controls, ask_select
from chatstyle.render import render_suggested_commands


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


def test_ask_checkbox_with_controls_falls_back_to_click(monkeypatch):
    real_import = __import__

    def fake_import(name, *args, **kwargs):
        if name in {"prompt_toolkit.application", "questionary"}:
            raise ImportError(name)
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", fake_import)
    monkeypatch.setattr(click, "prompt", lambda *args, **kwargs: "2")

    selected = ask_checkbox_with_controls("Pick many", ["a", "b", "c"])

    assert selected == ["a"]


def test_prompt_sensitive_value_keeps_current(monkeypatch):
    monkeypatch.setattr("chatstyle.security.mask.ask_text", lambda *args, **kwargs: "")

    assert format_current_secret("abcdefgh") == "current: ab****gh"
    assert prompt_sensitive_value("token", "abcdefgh") == "abcdefgh"


def test_render_suggested_commands_outputs_commands(capsys):
    render_suggested_commands(["sudo systemctl restart demo"], description="Run manually")

    captured = capsys.readouterr()
    assert "Suggested Commands" in captured.err
    assert "sudo systemctl restart demo" in captured.out
