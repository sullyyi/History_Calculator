from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Protocol


class Observer(Protocol):
    def update(self, event: str, payload: dict[str, Any]) -> None:
        ...


def _get_file_logger(log_file: Path, encoding: str = "utf-8") -> logging.Logger:
    logger = logging.getLogger("calculator")
    logger.setLevel(logging.INFO)

    log_file = Path(log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Avoid duplicate handlers if create_default() is called multiple times in tests
    handler_key = str(log_file.resolve())
    existing = getattr(logger, "_calculator_handler_keys", set())

    if handler_key not in existing:
        fh = logging.FileHandler(log_file, encoding=encoding)
        fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        fh.setFormatter(fmt)
        logger.addHandler(fh)

        existing = set(existing)
        existing.add(handler_key)
        setattr(logger, "_calculator_handler_keys", existing)

    return logger


@dataclass
class InMemoryLoggerObserver:
    lines: list[str] = field(default_factory=list)

    def update(self, event: str, payload: dict[str, Any]) -> None:
        self.lines.append(f"{event}: {payload}")


@dataclass
class LoggingObserver:
    log_file: Path
    encoding: str = "utf-8"

    def update(self, event: str, payload: dict[str, Any]) -> None:
        logger = _get_file_logger(self.log_file, self.encoding)

        if event == "calculation_added":
            op = payload.get("operation")
            a = payload.get("a")
            b = payload.get("b")
            result = payload.get("result")
            logger.info("calc op=%s a=%s b=%s result=%s", op, a, b, result)
        else:
            logger.info("%s %s", event, payload)


@dataclass
class AutoSaveObserver:
    save_func: Callable[[], None]

    def update(self, event: str, payload: dict[str, Any]) -> None:
        if event in {"calculation_added", "history_cleared", "history_loaded", "undo", "redo"}:
            self.save_func()


# Backwards-compatible name expected by existing tests:
LoggerObserver = InMemoryLoggerObserver