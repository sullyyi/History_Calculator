from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from app.exceptions import ConfigurationError


def _get_env(name: str, default: str) -> str:
    v = os.getenv(name)
    if v is not None:
        return v
    return default


def _get_env_fallback(primary: str, fallback: str, default: str) -> str:
    v = os.getenv(primary)
    if v is not None:
        return v
    v2 = os.getenv(fallback)
    if v2 is not None:
        return v2
    return default


def _parse_bool(value: str) -> bool:
    v = value.strip().lower()
    if v in {"1", "true", "yes", "y", "on"}:
        return True
    if v in {"0", "false", "no", "n", "off"}:
        return False
    raise ConfigurationError(f"Invalid boolean value: {value!r}")


def _parse_int(value: str, name: str) -> int:
    try:
        return int(value.strip())
    except Exception as exc:
        raise ConfigurationError(f"Invalid integer for {name}: {value!r}") from exc


def _parse_float(value: str, name: str) -> float:
    try:
        return float(value.strip())
    except Exception as exc:
        raise ConfigurationError(f"Invalid float for {name}: {value!r}") from exc


@dataclass(frozen=True)
class CalculatorConfig:
    history_dir: Path
    history_file: str
    log_dir: Path
    log_file: str

    max_history_size: int
    auto_save: bool
    auto_load: bool
    precision: int
    max_input_value: float
    default_encoding: str

    @property
    def history_path(self) -> Path:
        return self.history_dir / self.history_file

    @property
    def log_path(self) -> Path:
        return self.log_dir / self.log_file


def load_config() -> CalculatorConfig:
    load_dotenv()

    # PDF names (primary) with CALC_* backward-compatible fallbacks
    history_dir_raw = _get_env_fallback("CALCULATOR_HISTORY_DIR", "CALC_HISTORY_DIR", ".")
    history_file_raw = _get_env_fallback("CALCULATOR_HISTORY_FILE", "CALC_HISTORY_FILE", "history.csv")

    log_dir_raw = _get_env_fallback("CALCULATOR_LOG_DIR", "CALC_LOG_DIR", ".")
    log_file_raw = _get_env_fallback("CALCULATOR_LOG_FILE", "CALC_LOG_FILE", "calculator.log")

    max_history_size_raw = _get_env_fallback("CALCULATOR_MAX_HISTORY_SIZE", "CALC_MAX_HISTORY_SIZE", "1000")
    auto_save_raw = _get_env_fallback("CALCULATOR_AUTO_SAVE", "CALC_AUTO_SAVE", "false")
    auto_load_raw = _get_env_fallback("CALCULATOR_AUTO_LOAD", "CALC_AUTO_LOAD", "true")

    precision_raw = _get_env_fallback("CALCULATOR_PRECISION", "CALC_PRECISION", "6")
    max_input_raw = _get_env_fallback("CALCULATOR_MAX_INPUT_VALUE", "CALC_MAX_INPUT_VALUE", "1000000000")
    encoding_raw = _get_env_fallback("CALCULATOR_DEFAULT_ENCODING", "CALC_DEFAULT_ENCODING", "utf-8")

    history_dir = Path(history_dir_raw).expanduser()
    log_dir = Path(log_dir_raw).expanduser()

    history_file = history_file_raw.strip()
    log_file = log_file_raw.strip()

    if not history_file:
        raise ConfigurationError("CALCULATOR_HISTORY_FILE cannot be empty.")
    if not log_file:
        raise ConfigurationError("CALCULATOR_LOG_FILE cannot be empty.")

    return CalculatorConfig(
        history_dir=history_dir,
        history_file=history_file,
        log_dir=log_dir,
        log_file=log_file,
        max_history_size=_parse_int(max_history_size_raw, "CALCULATOR_MAX_HISTORY_SIZE"),
        auto_save=_parse_bool(auto_save_raw),
        auto_load=_parse_bool(auto_load_raw),
        precision=_parse_int(precision_raw, "CALCULATOR_PRECISION"),
        max_input_value=_parse_float(max_input_raw, "CALCULATOR_MAX_INPUT_VALUE"),
        default_encoding=encoding_raw.strip() or "utf-8",
    )