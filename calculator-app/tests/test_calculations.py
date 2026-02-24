import pytest
import pandas as pd
from pathlib import Path
from app.calculator.cli import run_repl
from app.calculation.factory import CalculationFactory
from app.calculation.history import CalculationHistory
from app.operation.arithmetic import Power, Root
from app.calculator.facade import Calculator


@pytest.mark.parametrize(
    "op_name,a,b,expected",
    [
        ("add", 1, 2, 3),
        ("sub", 10, 4, 6),
        ("mul", 3, 5, 15),
        ("div", 8, 2, 4),
        ("pow", 2, 3, 8),
        ("root", 9, 2, 3),
    ],
)
def test_factory_create_and_result(op_name, a, b, expected):
    factory = CalculationFactory()
    calc = factory.create(op_name, a, b)
    assert calc.result() == expected


def test_factory_rejects_unknown_operation():
    factory = CalculationFactory()
    with pytest.raises(ValueError):
        factory.create("nope", 2, 3)


def test_history_add_all_clear_and_format_empty():
    history = CalculationHistory()
    assert history.format_lines() == ["(no history)"]

    factory = CalculationFactory()
    history.add(factory.create("add", 2, 3))
    history.add(factory.create("mul", 3, 4))

    df = history.all()
    assert len(df) == 2
    assert set(["operation", "a", "b", "result"]).issubset(df.columns)

    lines = history.format_lines()
    assert len(lines) == 2
    assert any("add" in line for line in lines)

    history.clear()
    df2 = history.all()
    assert len(df2) == 0
    assert history.format_lines() == ["(no history)"]


def test_history_snapshot_and_restore():
    factory = CalculationFactory()
    history = CalculationHistory()

    history.add(factory.create("add", 2, 3))
    history.add(factory.create("mul", 3, 4))

    snap = history.snapshot()

    history.add(factory.create("sub", 10, 1))
    assert len(history.all()) == 3

    history.restore(snap)
    assert len(history.all()) == 2
    lines = history.format_lines()
    assert any("add" in line for line in lines)
    assert any("mul" in line for line in lines)


def test_history_save_and_load_round_trip(tmp_path):
    factory = CalculationFactory()
    history = CalculationHistory()

    history.add(factory.create("add", 2, 3))
    history.add(factory.create("pow", 2, 3))

    path = tmp_path / "history.csv"
    history.save(path)

    new_history = CalculationHistory()
    new_history.load(path)

    df = new_history.all()
    assert len(df) == 2
    lines = new_history.format_lines()
    assert any("add" in line for line in lines)
    assert any("pow" in line for line in lines)

def test_history_load_missing_required_columns_raises(tmp_path):
    path = tmp_path / "bad.csv"
    pd.DataFrame([{"operation": "add", "a": 1, "b": 2}]).to_csv(path, index=False)  # missing "result"

    history = CalculationHistory()
    with pytest.raises(ValueError):
        history.load(path)


def test_calculation_format_includes_operation_and_equals():
    factory = CalculationFactory()
    calc = factory.create("add", 2, 3)
    s = calc.format()
    assert "add" in s
    assert "=" in s


def test_power_complex_result_raises():
    with pytest.raises(ValueError):
        Power().compute(-1, 0.5)

def test_root_negative_non_integer_exponent_raises():
    with pytest.raises(ValueError):
        Root().compute(-8, 2.5)



def test_run_repl_configuration_error(monkeypatch, tmp_path: Path):
    monkeypatch.setenv("CALC_HISTORY_PATH", "")
    outputs = []

    def fake_input(prompt: str) -> str:
        return "exit"

    def fake_output(msg: str) -> None:
        outputs.append(msg)

    run_repl(input_func=fake_input, output_func=fake_output, history_path=tmp_path/"x.csv")
    assert any("Configuration error:" in s for s in outputs)

def test_run_repl_auto_load_warning(monkeypatch, tmp_path: Path):
    monkeypatch.setenv("CALC_HISTORY_PATH", str(tmp_path))  # directory, not file
    monkeypatch.setenv("CALC_AUTO_LOAD", "true")
    monkeypatch.setenv("CALC_AUTO_SAVE", "false")

    inputs = iter(["exit"])
    outputs = []

    def fake_input(prompt: str) -> str:
        return next(inputs)

    def fake_output(msg: str) -> None:
        outputs.append(msg)

    run_repl(input_func=fake_input, output_func=fake_output)
    assert any("Warning: Failed to load history:" in s for s in outputs)

def test_facade_auto_save_writes_file(tmp_path: Path):
    path = tmp_path / "history.csv"
    calc = Calculator.create_default(history_path=path, auto_save=True, auto_load=False)
    calc.execute("add", 1, 2)
    assert path.exists()

def test_facade_auto_load_true_loads_existing(tmp_path: Path):
    path = tmp_path / "history.csv"
    pd.DataFrame([{"operation": "add", "a": 1, "b": 2, "result": 3}]).to_csv(path, index=False)

    calc = Calculator.create_default(history_path=path, auto_save=False, auto_load=True)
    assert len(calc.history.all()) == 1


def test_history_load_missing_required_columns_raises(tmp_path):
    path = tmp_path / "bad.csv"
    # Missing "result"
    pd.DataFrame([{"operation": "add", "a": 1, "b": 2}]).to_csv(path, index=False)

    history = CalculationHistory()
    with pytest.raises(ValueError):
        history.load(path)


def test_history_load_missing_required_columns_hits_branch(tmp_path):
    path = tmp_path / "missing_cols.csv"

    # Only include a totally unrelated column so read_csv succeeds but required columns are missing
    pd.DataFrame([{"x": 1}]).to_csv(path, index=False)

    history = CalculationHistory()
    with pytest.raises(ValueError):
        history.load(path)

def test_history_load_missing_file_raises(tmp_path):
    history = CalculationHistory()
    missing = tmp_path / "nope.csv"

    with pytest.raises(FileNotFoundError):
        history.load(missing)