from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.calculation.factory import CalculationFactory
from app.calculation.history import CalculationHistory, HistorySnapshot


@dataclass
class Calculator:
    factory: CalculationFactory
    history: CalculationHistory
    history_path: Path
    _undo_stack: list[HistorySnapshot]
    _redo_stack: list[HistorySnapshot]

    @classmethod
    def create_default(cls, history_path: str | Path = "history.csv") -> "Calculator":
        return cls(
            factory=CalculationFactory(),
            history=CalculationHistory(),
            history_path=Path(history_path),
            _undo_stack=[],
            _redo_stack=[],
        )

    def supported_ops_text(self) -> str:
        return ", ".join(self.factory.supported)

    def help_text(self) -> str:
        ops = self.supported_ops_text()
        return (
            "Commands:\n"
            "  add | sub | mul | div | pow | root  -> perform arithmetic\n"
            "  history                            -> show history\n"
            "  clear                              -> clear history\n"
            "  undo                               -> undo last change\n"
            "  redo                               -> redo last undone change\n"
            "  save                               -> save history to CSV\n"
            "  load                               -> load history from CSV\n"
            "  help                               -> show this help\n"
            "  exit                               -> quit\n\n"
            "Usage:\n"
            "  <op> <a> <b>\n"
            f"Supported ops: {ops}"
        )

    def history_lines(self) -> list[str]:
        return self.history.format_lines()

    def _record_undo_before_change(self) -> None:
        self._undo_stack.append(self.history.snapshot())
        self._redo_stack.clear()

    def clear(self) -> None:
        self._record_undo_before_change()
        self.history.clear()

    def execute(self, op_name: str, a: float, b: float) -> float:
        calc = self.factory.create(op_name, a, b)
        self._record_undo_before_change()
        result = calc.result()
        self.history.add(calc)
        return result

    def undo(self) -> bool:
        if not self._undo_stack:
            return False
        self._redo_stack.append(self.history.snapshot())
        snap = self._undo_stack.pop()
        self.history.restore(snap)
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            return False
        self._undo_stack.append(self.history.snapshot())
        snap = self._redo_stack.pop()
        self.history.restore(snap)
        return True

    def save(self) -> None:
        self.history.save(self.history_path)

    def load(self) -> None:
        # LBYL: check before attempting to load
        if not self.history_path.exists():
            raise FileNotFoundError(f"History file not found: {self.history_path}")
        self._record_undo_before_change()
        self.history.load(self.history_path)

    def auto_load_if_exists(self) -> bool:
        """Load history if the CSV exists. Returns True if loaded, False otherwise."""
        if not self.history_path.exists():
            return False
        self.history.load(self.history_path)
        return True