from __future__ import annotations

from dataclasses import dataclass

from app.calculation.history import HistorySnapshot


@dataclass
class MementoCaretaker:
    undo_stack: list[HistorySnapshot]
    redo_stack: list[HistorySnapshot]

    def __init__(self) -> None:
        self.undo_stack = []
        self.redo_stack = []

    def clear_redo(self) -> None:
        self.redo_stack.clear()

    def can_undo(self) -> bool:
        return bool(self.undo_stack)

    def can_redo(self) -> bool:
        return bool(self.redo_stack)