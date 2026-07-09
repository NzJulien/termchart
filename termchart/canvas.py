"""Low-level Unicode drawing canvas for terminal charts."""
from __future__ import annotations


# Block elements for sub-character vertical resolution
EIGHTHS = " ▁▂▃▄▅▆▇█"
BRAILLE_ROW = ["⣀", "⣤", "⣶", "⣿"]  # for line charts

# Box-drawing chars
H = "─"
V = "│"
TL = "┌"
TR = "┐"
BL = "└"
BR = "┘"
T  = "┬"
B  = "┴"
L  = "├"
R  = "┤"
X  = "┼"

COLORS = {
    "red":    "\033[91m",
    "green":  "\033[92m",
    "yellow": "\033[93m",
    "blue":   "\033[94m",
    "cyan":   "\033[96m",
    "reset":  "\033[0m",
    "bold":   "\033[1m",
    "dim":    "\033[2m",
}


def c(text: str, color: str) -> str:
    code = COLORS.get(color, "")
    return f"{code}{text}{COLORS['reset']}" if code else text


class Canvas:
    """A 2-D grid of characters, printable as a terminal string."""

    def __init__(self, width: int, height: int, fill: str = " "):
        self.width = width
        self.height = height
        self._grid: list[list[str]] = [[fill] * width for _ in range(height)]

    def set(self, x: int, y: int, char: str) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            self._grid[y][x] = char

    def get(self, x: int, y: int) -> str:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self._grid[y][x]
        return " "

    def hline(self, x: int, y: int, length: int, char: str = H) -> None:
        for i in range(length):
            self.set(x + i, y, char)

    def vline(self, x: int, y: int, length: int, char: str = V) -> None:
        for i in range(length):
            self.set(x, y + i, char)

    def text(self, x: int, y: int, s: str) -> None:
        for i, ch in enumerate(s):
            self.set(x + i, y, ch)

    def render(self) -> str:
        return "\n".join("".join(row) for row in self._grid)


def normalise(values: list[float], lo: float, hi: float, height: int) -> list[float]:
    """Map values into [0, height] range."""
    span = hi - lo or 1.0
    return [(v - lo) / span * height for v in values]


def y_axis_labels(lo: float, hi: float, n_ticks: int) -> list[tuple[int, str]]:
    """Return [(row_index, label_str)] for y-axis tick labels."""
    span = hi - lo
    ticks = []
    for i in range(n_ticks + 1):
        frac = i / n_ticks
        value = lo + frac * span
        label = _fmt(value)
        row = n_ticks - i  # top row = high value
        ticks.append((row, label))
    return ticks


def _fmt(v: float) -> str:
    if v == int(v) and abs(v) < 1e6:
        return str(int(v))
    return f"{v:.3g}"
