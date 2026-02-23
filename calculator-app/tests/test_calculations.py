import pytest

from app.calculation.factory import CalculationFactory
from app.calculation.history import CalculationHistory


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
