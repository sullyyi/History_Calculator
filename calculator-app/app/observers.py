from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Protocol


class Observer(Protocol):
    def update(self, event: str, payload: dict[str, Any]) -> None:
        ...


@dataclass
class LoggerObserver:
    lines: list[str]

    def __init__(self) -> None:
        self.lines = []

    def update(self, event: str, payload: dict[str, Any]) -> None:
        self.lines.append(f"{event}: {payload}")


@dataclass
class AutoSaveObserver:
    save_func: Callable[[], None]

    def update(self, event: str, payload: dict[str, Any]) -> None:
        if event in {"calculation_added", "history_cleared", "history_loaded", "undo", "redo"}:
            self.save_func()