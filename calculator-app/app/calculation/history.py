from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from .models import Calculation


@dataclass(frozen=True)
class HistorySnapshot:
    """Immutable snapshot of calculator history state."""
    df: pd.DataFrame


class CalculationHistory:
    """pandas-backed history with CSV persistence."""

    REQUIRED_COLUMNS = ("timestamp", "operation", "a", "b", "result")

    def __init__(self) -> None:
        self._df = self._empty_df()

    def _empty_df(self) -> pd.DataFrame:
        return pd.DataFrame(columns=list(self.REQUIRED_COLUMNS))

    def add(self, calc: Calculation) -> None:
        res = float(calc.result())
        row = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "operation": calc.operation.name,
            "a": float(calc.a),
            "b": float(calc.b),
            "result": res,
        }
        self._df = pd.concat([self._df, pd.DataFrame([row])], ignore_index=True)

    def all(self) -> pd.DataFrame:
        return self._df.copy()

    def clear(self) -> None:
        self._df = self._empty_df()

    def format_lines(self) -> list[str]:
        if self._df.empty:
            return ["(no history)"]

        lines: list[str] = []
        for _, row in self._df.iterrows():
            op = str(row["operation"])
            a = float(row["a"])
            b = float(row["b"])
            result = float(row["result"])
            lines.append(f"{op} {a} {b} = {result}")
        return lines

    def snapshot(self) -> HistorySnapshot:
        return HistorySnapshot(df=self._df.copy(deep=True))

    def restore(self, snap: HistorySnapshot) -> None:
        self._df = snap.df.copy(deep=True)

    def save(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        self._df.to_csv(p, index=False)

    def load(self, path: str | Path) -> None:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"History file not found: {p}")

        df = pd.read_csv(p)

        # Backward compatibility: older CSVs may not have timestamp
        if "timestamp" not in df.columns:
            df["timestamp"] = ""

        missing = [c for c in self.REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            raise ValueError(f"History CSV missing required columns: {missing}")

        df = df.loc[:, list(self.REQUIRED_COLUMNS)]
        df["timestamp"] = df["timestamp"].astype(str)
        df["a"] = pd.to_numeric(df["a"])
        df["b"] = pd.to_numeric(df["b"])
        df["result"] = pd.to_numeric(df["result"])

        self._df = df.reset_index(drop=True)