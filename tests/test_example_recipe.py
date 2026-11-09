"""Exercise only the optional recipe, not future consumer CLI commands."""
from pathlib import Path
import runpy
from click.testing import CliRunner


def example():
    return runpy.run_path(str(Path(__file__).resolve().parents[1]/"examples/interactive_input.py"))["example"]


def test_example_complete_no_prompt_input_executes():
    r=CliRunner().invoke(example(),["demo","--count","2","-I"])
    assert r.exit_code==0,r.output
    assert r.output=="demo\ndemo\n"


def test_example_missing_required_input_fails():
    r=CliRunner().invoke(example(),["-I"])
    assert r.exit_code!=0
    assert "Missing required value: resource" in r.output


def test_example_prompted_count_uses_same_range(monkeypatch):
    monkeypatch.setattr("chatstyle.core.interactive.is_interactive_available",lambda:True)
    r=CliRunner().invoke(example(),["demo","-i"],input="11\n")
    assert r.exit_code!=0
    assert "Invalid value for Count" in r.output
