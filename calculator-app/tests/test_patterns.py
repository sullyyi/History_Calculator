from pathlib import Path

from app.calculator.facade import Calculator
from app.observers import LoggerObserver
from app.strategy import ExecutionStrategy


class DoubleResultStrategy:
    def execute(self, calc) -> float:
        return 2 * calc.result()


def test_observer_receives_events(tmp_path: Path):
    calc = Calculator.create_default(history_path=tmp_path / "history.csv")
    logger = LoggerObserver()
    calc.attach(logger)

    calc.execute("add", 2, 3)

    assert any(line.startswith("calculation_added:") for line in logger.lines)


def test_strategy_can_change_execution(tmp_path: Path):
    calc = Calculator.create_default(history_path=tmp_path / "history.csv")
    calc.strategy = DoubleResultStrategy()

    result = calc.execute("add", 2, 3)
    assert result == 10.0