from __future__ import annotations

from chatstyle.render import (
    render_commands,
    render_config_priority,
    render_dry_run,
    render_plan,
    render_stage,
    render_success,
)
from chatstyle.render import (
    TableColumn,
    render_key_values,
    render_priority_chain,
    render_status,
    render_suggested_commands,
    render_table,
)


def test_render_status_routes_warning_to_stderr(capsys):
    render_status("warning", "check token")

    captured = capsys.readouterr()
    assert "[WARN] check token" in captured.err
    assert captured.out == ""


def test_render_status_routes_success_to_stdout(capsys):
    render_status("success", "done")

    captured = capsys.readouterr()
    assert "[OK] done" in captured.out


def test_render_suggested_commands_only_prints(monkeypatch, capsys):
    monkeypatch.setattr("chatstyle.render.output._get_console", lambda: None)

    render_suggested_commands(["sudo systemctl restart demo"], description="Run manually")

    captured = capsys.readouterr()
    assert "Suggested Commands" in captured.err
    assert "Run manually" in captured.err
    assert "sudo systemctl restart demo" in captured.out


def test_render_priority_chain(monkeypatch, capsys):
    monkeypatch.setattr("chatstyle.render.output._get_console", lambda: None)

    render_priority_chain(["CLI", "ENV", "config", "default"], label="Config")

    captured = capsys.readouterr()
    assert "Config: CLI > ENV > config > default" in captured.err


def test_render_key_values_and_table(monkeypatch, capsys):
    monkeypatch.setattr("chatstyle.render.output._get_console", lambda: None)

    render_key_values({"name": "demo", "state": "ok"})
    render_table(
        [{"name": "demo", "state": "ok"}],
        [TableColumn("name", "Name"), TableColumn("state", "State")],
    )

    captured = capsys.readouterr()
    assert "name  : demo" in captured.out
    assert "state : ok" in captured.out
    assert "Name  State" in captured.out
    assert "demo  ok" in captured.out


def test_flow_helpers_delegate_to_generic_output(monkeypatch, capsys):
    monkeypatch.setattr("chatstyle.render.output._get_console", lambda: None)

    render_stage("Check environment")
    render_success("Ready")
    render_commands(["demo --help"])
    render_plan(["check", "write"])
    render_dry_run(["would write config"])
    render_config_priority(["CLI", "ENV", "config", "default"])

    captured = capsys.readouterr()
    assert "[INFO] Check environment" in captured.err
    assert "[OK] Ready" in captured.out
    assert "demo --help" in captured.out
    assert "- check" in captured.out
    assert "- would write config" in captured.out
    assert "Config priority: CLI > ENV > config > default" in captured.err
