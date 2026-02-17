from __future__ import annotations

from typing import Dict

from app.operation.arithmetic import Add, Divide, Multiply, Subtract
from app.operation.base import Operation

from .models import Calculation


class CalculationFactory:
    """Creates Calculation instances from a string operation name."""

    def __init__(self) -> None:
        self._ops: Dict[str, Operation] = {
            "add": Add(),
            "sub": Subtract(),
            "mul": Multiply(),
            "div": Divide(),
        }

    @property
    def supported(self) -> tuple[str, ...]:
        return tuple(self._ops.keys())

    def create(self, op_name: str, a: float, b: float) -> Calculation:
        op_name = op_name.strip().lower()
        if op_name not in self._ops:
            raise ValueError(f"Unsupported operation: {op_name}")
        return Calculation(operation=self._ops[op_name], a=a, b=b)
