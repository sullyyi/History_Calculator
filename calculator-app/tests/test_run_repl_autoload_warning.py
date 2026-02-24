from pathlib import Path

from app.calculator.cli import run_repl


def test_run_repl_auto_load_warning(monkeypatch, tmp_path: Path):
    # Make auto-load enabled
    monkeypatch.setenv("CALC_AUTO_LOAD", "true")
    monkeypatch.setenv("CALC_AUTO_SAVE", "false")

    # Point history path to a directory to force a load failure
    monkeypatch.setenv("CALC_HISTORY_PATH", str(tmp_path))

    outputs: list[str] = []

    def fake_input(prompt: str) -> str:
        return "exit"

    def fake_output(msg: str) -> None:
        outputs.append(msg)

    run_repl(input_func=fake_input, output_func=fake_output)

    assert any("Warning: Failed to load history:" in s for s in outputs)