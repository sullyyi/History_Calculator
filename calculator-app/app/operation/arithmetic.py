from __future__ import annotations

from .base import Operation


class Add(Operation):
    name = "add"

    def compute(self, a: float, b: float) -> float:
        return a + b


class Subtract(Operation):
    name = "sub"

    def compute(self, a: float, b: float) -> float:
        return a - b


class Multiply(Operation):
    name = "mul"

    def compute(self, a: float, b: float) -> float:
        return a * b


class Divide(Operation):
    name = "div"

    def compute(self, a: float, b: float) -> float:
        # LBYL: explicitly check before dividing
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a / b
