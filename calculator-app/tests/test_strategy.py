from pathlib import Path

from app.calculator.facade import Calculator


class DoubleResultStrategy:
    def execute(self, calc) -> float:
        return 2 * calc.result()


def test_direct_execution_default(tmp_path: Path):
    calc = Calculator.create_default(history_path=tmp_path / "history.csv")
    result = calc.execute("add", 2, 3)
    assert result == 5.0


def test_custom_strategy_changes_execution(tmp_path: Path):
    calc = Calculator.create_default(history_path=tmp_path / "history.csv")
    calc.strategy = DoubleResultStrategy()

    result = calc.execute("add", 2, 3)
    assert result == 10.0