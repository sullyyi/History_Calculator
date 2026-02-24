from __future__ import annotations

from typing import Protocol

from app.calculation.models import Calculation


class ExecutionStrategy(Protocol):
    def execute(self, calc: Calculation) -> float:
        ...


class DirectExecutionStrategy:
    def execute(self, calc: Calculation) -> float:
        return calc.result()