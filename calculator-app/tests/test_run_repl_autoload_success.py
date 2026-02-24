from pathlib import Path

import pandas as pd

from app.calculator.cli import run_repl


def test_run_repl_auto_load_success(monkeypatch, tmp_path: Path):
    history_file = tmp_path / "history.csv"
    pd.DataFrame([{"operation": "add", "a": 1, "b": 2, "result": 3}]).to_csv(history_file, index=False)

    monkeypatch.setenv("CALC_HISTORY_PATH", str(history_file))
    monkeypatch.setenv("CALC_AUTO_LOAD", "true")
    monkeypatch.setenv("CALC_AUTO_SAVE", "false")

    outputs: list[str] = []

    def fake_input(prompt: str) -> str:
        return "exit"

    def fake_output(msg: str) -> None:
        outputs.append(msg)

    run_repl(input_func=fake_input, output_func=fake_output)

    assert any("Loaded history from:" in s for s in outputs)