"""Load and validate CSV data into typed columns."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Column:
    name: str
    values: list[float]
    raw: list[str]

    @property
    def min(self) -> float:
        return min(self.values)

    @property
    def max(self) -> float:
        return max(self.values)

    @property
    def mean(self) -> float:
        return sum(self.values) / len(self.values)

    @property
    def total(self) -> float:
        return sum(self.values)

    def __len__(self) -> int:
        return len(self.values)


def read_csv(
    path: str | Path,
    x_col: Optional[str] = None,
    y_col: Optional[str] = None,
) -> tuple[list[str], Column, Optional[Column]]:
    """Read a CSV file and return (labels, y_column, x_column_or_None).

    If x_col is not given, row indices are used as labels.
    y_col is the column to chart; if not given, the first numeric column is used.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    rows: list[dict] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header row")
        fieldnames = list(reader.fieldnames)
        for row in reader:
            rows.append(row)

    if not rows:
        raise ValueError("CSV file is empty")

    def _numeric_columns() -> list[str]:
        result = []
        for col in fieldnames:
            try:
                [float(r[col]) for r in rows if r[col].strip()]
                result.append(col)
            except (ValueError, KeyError):
                pass
        return result

    numeric_cols = _numeric_columns()
    if not numeric_cols:
        raise ValueError("No numeric columns found in CSV")

    # Resolve y column
    if y_col is None:
        y_col = numeric_cols[0]
    elif y_col not in fieldnames:
        raise ValueError(f"Column '{y_col}' not found. Available: {fieldnames}")

    def _load_column(name: str) -> Column:
        raw = [r[name].strip() for r in rows]
        values = []
        for v in raw:
            try:
                values.append(float(v))
            except ValueError:
                raise ValueError(f"Non-numeric value '{v}' in column '{name}'")
        return Column(name=name, values=values, raw=raw)

    y = _load_column(y_col)

    # Resolve x column / labels
    if x_col:
        if x_col not in fieldnames:
            raise ValueError(f"Column '{x_col}' not found. Available: {fieldnames}")
        try:
            x = _load_column(x_col)
            labels = [str(v) for v in x.raw]
        except ValueError:
            # x column is categorical — use raw strings as labels
            labels = [r[x_col].strip() for r in rows]
            x = None
    else:
        labels = [str(i + 1) for i in range(len(y))]
        x = None

    return labels, y, x


def summary(col: Column) -> str:
    import statistics
    vals = col.values
    lines = [
        f"Column : {col.name}",
        f"Count  : {len(vals)}",
        f"Min    : {min(vals):.4g}",
        f"Max    : {max(vals):.4g}",
        f"Mean   : {col.mean:.4g}",
        f"Median : {statistics.median(vals):.4g}",
        f"Stdev  : {statistics.stdev(vals):.4g}" if len(vals) > 1 else "Stdev  : N/A",
        f"Total  : {col.total:.4g}",
    ]
    return "\n".join(lines)
