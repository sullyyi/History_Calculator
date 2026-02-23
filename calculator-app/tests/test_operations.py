import pytest

from app.operation.arithmetic import Add, Divide, Multiply, Subtract, Power, Root


@pytest.mark.parametrize(
    "op,a,b,expected",
    [
        (Add(), 2, 3, 5),
        (Subtract(), 5, 2, 3),
        (Multiply(), 4, 2.5, 10),
        (Divide(), 9, 3, 3),
        (Power(), 2, 3, 8),
        (Power(), 9, 0.5, 3),
        (Root(), 9, 2, 3),
        (Root(), 27, 3, 3),
        (Root(), -8, 3, -2),
    ],
)
def test_operations_compute(op, a, b, expected):
    assert op.compute(a, b) == expected


def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        Divide().compute(1, 0)


def test_root_with_zero_exponent_raises():
    with pytest.raises(ZeroDivisionError):
        Root().compute(16, 0)


def test_root_negative_even_exponent_raises():
    with pytest.raises(ValueError):
        Root().compute(-8, 2)