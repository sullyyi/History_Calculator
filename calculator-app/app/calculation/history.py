from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd

from .models import Calculation


@dataclass(frozen=True)
class HistorySnapshot:
    """Immutable snapshot of calculator history state."""
    df: pd.DataFrame


class CalculationHistory:
    """pandas-backed history with CSV persistence."""

    REQUIRED_COLUMNS = ("operation", "a", "b", "result")

    def __init__(self) -> None:
        self._df = self._empty_df()

    def _empty_df(self) -> pd.DataFrame:
        return pd.DataFrame(columns=list(self.REQUIRED_COLUMNS))

    def add(self, calc: Calculation) -> None:
        row = {
            "operation": calc.operation.name,
            "a": float(calc.a),
            "b": float(calc.b),
            "result": float(calc.result()),
        }
        self._df = pd.concat([self._df, pd.DataFrame([row])], ignore_index=True)

    def all(self) -> pd.DataFrame:
        """Return a copy of the current history DataFrame."""
        return self._df.copy()

    def clear(self) -> None:
        self._df = self._empty_df()

    def format_lines(self) -> list[str]:
        if self._df.empty:
            return ["(no history)"]

        lines: list[str] = []
        for _, row in self._df.iterrows():
            op = row["operation"]
            a = float(row["a"])
            b = float(row["b"])
            result = float(row["result"])
            lines.append(f"{op} {a} {b} = {result}")
        return lines

    def snapshot(self) -> HistorySnapshot:
        """Create a deep copy snapshot for undo/redo."""
        return HistorySnapshot(df=self._df.copy(deep=True))

    def restore(self, snap: HistorySnapshot) -> None:
        """Restore history from a snapshot."""
        self._df = snap.df.copy(deep=True)

    def save(self, path: str | Path) -> None:
        """Save current history to CSV."""
        p = Path(path)

        # EAFP: attempt write and raise if it fails (permissions, invalid path, etc.)
        self._df.to_csv(p, index=False)

    def load(self, path: str | Path) -> None:
        """Load history from CSV, replacing current state."""
        p = Path(path)

        # LBYL: check existence before reading
        if not p.exists():
            raise FileNotFoundError(f"History file not found: {p}")

        df = pd.read_csv(p)

        missing = [c for c in self.REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            raise ValueError(f"History CSV missing required columns: {missing}")

        # Normalize column order (keeps output stable)
        df = df.loc[:, list(self.REQUIRED_COLUMNS)]

        # Ensure numeric columns are numeric (raises if invalid)
        df["a"] = pd.to_numeric(df["a"])
        df["b"] = pd.to_numeric(df["b"])
        df["result"] = pd.to_numeric(df["result"])

        self._df = df.reset_index(drop=True)