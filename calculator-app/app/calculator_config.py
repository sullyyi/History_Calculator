from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from app.exceptions import ConfigurationError


def _parse_bool(value: str) -> bool:
    v = value.strip().lower()
    if v in {"1", "true", "yes", "y", "on"}:
        return True
    if v in {"0", "false", "no", "n", "off"}:
        return False
    raise ConfigurationError(f"Invalid boolean value: {value!r}")


@dataclass(frozen=True)
class CalculatorConfig:
    history_path: Path
    auto_load: bool
    auto_save: bool


def load_config() -> CalculatorConfig:
    # Loads .env if present, then environment variables
    load_dotenv()

    history_path_raw = os.getenv("CALC_HISTORY_PATH", "history.csv").strip()
    if not history_path_raw:
        raise ConfigurationError("CALC_HISTORY_PATH cannot be empty.")

    auto_load_raw = os.getenv("CALC_AUTO_LOAD", "true")
    auto_save_raw = os.getenv("CALC_AUTO_SAVE", "false")

    auto_load = _parse_bool(auto_load_raw)
    auto_save = _parse_bool(auto_save_raw)

    return CalculatorConfig(
        history_path=Path(history_path_raw),
        auto_load=auto_load,
        auto_save=auto_save,
    )