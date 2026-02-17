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
    ],
)
def test_factory_create_and_result(op_name, a, b, expected):
    factory = CalculationFactory()
    calc = factory.create(op_name, a, b)
    assert calc.result() == expected


def test_factory_rejects_unknown_operation():
    factory = CalculationFactory()
    with pytest.raises(ValueError):
        factory.create("pow", 2, 3)


def test_history_add_all_clear_and_format_empty():
    history = CalculationHistory()
    assert history.format_lines() == ["(no history)"]

    factory = CalculationFactory()
    history.add(factory.create("add", 2, 3))
    history.add(factory.create("mul", 3, 4))

    items = history.all()
    assert len(items) == 2

    lines = history.format_lines()
    assert len(lines) == 2
    assert "add" in lines[0] or "add" in lines[1]

    history.clear()
    assert history.all() == []
