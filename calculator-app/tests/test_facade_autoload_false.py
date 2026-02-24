from pathlib import Path

from app.calculator.facade import Calculator


def test_facade_auto_load_if_exists_returns_false(tmp_path: Path):
    calc = Calculator.create_default(history_path=tmp_path / "does_not_exist.csv")
    assert calc.auto_load_if_exists() is False