from __future__ import annotations

from dataclasses import dataclass

from app.operation.base import Operation


@dataclass(frozen=True)
class Calculation:
    """A single calculation: operation(a, b) -> result."""

    operation: Operation
    a: float
    b: float

    def result(self) -> float:
        return self.operation.compute(self.a, self.b)

    def format(self) -> str:
        return f"{self.operation.name} {self.a} {self.b} = {self.result()}"
