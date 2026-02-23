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
class Power(Operation):
    name = "pow"

    def compute(self, a: float, b: float) -> float:
        result = a ** b
        # Avoid complex results for this calculator
        if isinstance(result, complex):
            raise ValueError("Result is not a real number. (complex)")
        return result


class Root(Operation):
    name = "root"

    def compute(self, a: float, b: float) -> float:
        # LBYL: explicitly validate before computing
        if b == 0:
            raise ZeroDivisionError("Cannot take a root with exponent 0.")

        # If a is negative, only odd integer roots yield a real result
        if a < 0:
            if float(b).is_integer():
                b_int = int(b)
                if b_int % 2 == 0:
                    raise ValueError("Even root of a negative number is not a real number.")
                return -((-a) ** (1 / b_int))
            raise ValueError("Root of a negative number requires an odd integer exponent.")

        return a ** (1 / b)