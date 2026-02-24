from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from app.calculation.factory import CalculationFactory
from app.calculation.history import CalculationHistory, HistorySnapshot
from app.observers import Observer, AutoSaveObserver
from app.strategy import ExecutionStrategy, DirectExecutionStrategy


@dataclass
class Calculator:
    factory: CalculationFactory
    history: CalculationHistory
    history_path: Path

    # Strategy pattern: interchangeable execution behavior
    strategy: ExecutionStrategy = field(default_factory=DirectExecutionStrategy)

    # Observer pattern: subscribers get notified on changes
    _observers: list[Observer] = field(default_factory=list)

    # Memento stacks (undo/redo)
    _undo_stack: list[HistorySnapshot] = field(default_factory=list)
    _redo_stack: list[HistorySnapshot] = field(default_factory=list)

    @classmethod
    def create_default(
        cls,
        history_path: str | Path = "history.csv",
        auto_save: bool = False,
        auto_load: bool = False,
    ) -> "Calculator":
        calc = cls(
            factory=CalculationFactory(),
            history=CalculationHistory(),
            history_path=Path(history_path),
        )

        if auto_save:
            calc.attach(AutoSaveObserver(save_func=calc.save))

        if auto_load:
            # Auto-load is an app policy decision; it should not crash startup.
            calc.auto_load_if_exists()

        return calc

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def _notify(self, event: str, payload: dict[str, Any]) -> None:
        for obs in list(self._observers):
            obs.update(event, payload)

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
        self._notify("history_cleared", {"rows": 0})

    def execute(self, op_name: str, a: float, b: float) -> float:
        calc = self.factory.create(op_name, a, b)

        self._record_undo_before_change()

        # Strategy determines how we execute a calculation
        result = self.strategy.execute(calc)

        self.history.add(calc)
        self._notify(
            "calculation_added",
            {"operation": calc.operation.name, "a": a, "b": b, "result": result},
        )
        return result

    def undo(self) -> bool:
        if not self._undo_stack:
            return False

        self._redo_stack.append(self.history.snapshot())
        snap = self._undo_stack.pop()
        self.history.restore(snap)

        self._notify("undo", {"rows": len(self.history.all())})
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            return False

        self._undo_stack.append(self.history.snapshot())
        snap = self._redo_stack.pop()
        self.history.restore(snap)

        self._notify("redo", {"rows": len(self.history.all())})
        return True

    def save(self) -> None:
        self.history.save(self.history_path)
        self._notify("history_saved", {"path": str(self.history_path)})

    def load(self) -> None:
        # LBYL: check before attempting to load
        if not self.history_path.exists():
            raise FileNotFoundError(f"History file not found: {self.history_path}")

        self._record_undo_before_change()
        self.history.load(self.history_path)
        self._notify("history_loaded", {"path": str(self.history_path), "rows": len(self.history.all())})

    def auto_load_if_exists(self) -> bool:
        """Load history if the CSV exists. Returns True if loaded, False otherwise."""
        if not self.history_path.exists():
            return False
        self.history.load(self.history_path)
        self._notify("history_loaded", {"path": str(self.history_path), "rows": len(self.history.all())})
        return True