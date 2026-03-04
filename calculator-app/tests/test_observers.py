from pathlib import Path

from app.calculator.facade import Calculator
from app.observers import AutoSaveObserver, LoggingObserver


def test_logger_observer_records_events(tmp_path: Path):
    calc = Calculator.create_default(history_path=tmp_path / "history.csv")
    logger = LoggerObserver()
    calc.attach(logger)

    calc.execute("add", 2, 3)

    assert any(line.startswith("calculation_added:") for line in logger.lines)


def test_autosave_observer_calls_save_func():
    calls: list[str] = []

    def fake_save() -> None:
        calls.append("saved")

    obs = AutoSaveObserver(save_func=fake_save)

    obs.update("calculation_added", {})
    assert calls == ["saved"]

    obs.update("history_saved", {})
    assert calls == ["saved"]


def test_logging_observer_writes_file(tmp_path: Path) -> None:
    log_file = tmp_path / "calc.log"
    obs = LoggingObserver(log_file=log_file, encoding="utf-8")

    obs.update("calculation_added", {"operation": "add", "a": 2, "b": 3, "result": 5})

    assert log_file.exists()
    assert log_file.read_text(encoding="utf-8").strip() != ""