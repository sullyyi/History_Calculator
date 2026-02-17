from __future__ import annotations

from typing import List

from .models import Calculation


class CalculationHistory:
    """In-memory session history."""

    def __init__(self) -> None:
        self._items: List[Calculation] = []

    def add(self, calc: Calculation) -> None:
        self._items.append(calc)

    def all(self) -> list[Calculation]:
        return list(self._items)

    def clear(self) -> None:
        self._items.clear()

    def format_lines(self) -> list[str]:
        if not self._items:
            return ["(no history)"]
        return [c.format() for c in self._items]
