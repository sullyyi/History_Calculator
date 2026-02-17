import pytest

from app.operation.arithmetic import Add, Divide, Multiply, Subtract


@pytest.mark.parametrize(
    "op,a,b,expected",
    [
        (Add(), 2, 3, 5),
        (Subtract(), 5, 2, 3),
        (Multiply(), 4, 2.5, 10),
        (Divide(), 9, 3, 3),
    ],
)
def test_operations_compute(op, a, b, expected):
    assert op.compute(a, b) == expected


def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        Divide().compute(1, 0)
