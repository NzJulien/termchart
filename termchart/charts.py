"""Chart renderers: bar, line, histogram, scatter."""
from __future__ import annotations

import math
from .canvas import Canvas, EIGHTHS, c, normalise, y_axis_labels, _fmt, H, V, BL, BR, TL, TR, L, R, B, T, X


def _header(title: str, width: int, color: str = "cyan") -> str:
    pad = max(0, width - len(title)) // 2
    return c(" " * pad + title, color)


def _y_label_width(lo: float, hi: float) -> int:
    labels = [_fmt(lo), _fmt(hi), _fmt((lo + hi) / 2)]
    return max(len(l) for l in labels) + 1


# ── Bar chart ─────────────────────────────────────────────────────────────────

def bar_chart(
    labels: list[str],
    values: list[float],
    title: str = "",
    width: int = 72,
    height: int = 16,
    color: str = "cyan",
    show_values: bool = True,
) -> str:
    if not values:
        return "(no data)"

    lo = min(0.0, min(values))
    hi = max(values) or 1.0
    yw = _y_label_width(lo, hi)
    chart_w = width - yw - 2
    n = len(values)
    bar_w = max(1, chart_w // n)

    lines = []
    if title:
        lines.append(_header(title, width, color))
        lines.append("")

    # Y-axis ticks
    ticks = y_axis_labels(lo, hi, height)
    tick_map = {row: label for row, label in ticks}

    normalised = normalise(values, lo, hi, height)

    rows = []
    for row in range(height, -1, -1):
        label = tick_map.get(row, "")
        prefix = label.rjust(yw) + " " + (L if row == 0 else V) + " "
        seg = ""
        for i, norm in enumerate(normalised):
            filled_rows = norm
            cell_top = row
            cell_bottom = row - 1
            if filled_rows >= cell_top:
                seg += c("█" * bar_w, color)
            elif filled_rows > cell_bottom:
                frac = filled_rows - cell_bottom
                idx = min(len(EIGHTHS) - 1, int(frac * (len(EIGHTHS) - 1)))
                seg += c(EIGHTHS[idx] * bar_w, color)
            else:
                seg += " " * bar_w
        rows.append(prefix + seg)

    lines.extend(rows)

    # X-axis
    x_axis = " " * (yw + 1) + B + H * (bar_w * n + 1)
    lines.append(x_axis)

    # X labels (truncated to bar_w)
    lbl_row = " " * (yw + 2)
    for lbl in labels:
        short = lbl[:bar_w].center(bar_w)
        lbl_row += short
    lines.append(c(lbl_row, "dim"))

    if show_values:
        val_row = " " * (yw + 2)
        for v in values:
            val_str = _fmt(v)[:bar_w].center(bar_w)
            val_row += c(val_str, "yellow")
        lines.append(val_row)

    return "\n".join(lines)


# ── Line chart ────────────────────────────────────────────────────────────────

def line_chart(
    labels: list[str],
    values: list[float],
    title: str = "",
    width: int = 72,
    height: int = 16,
    color: str = "green",
    marker: str = "●",
) -> str:
    if not values:
        return "(no data)"

    lo = min(values)
    hi = max(values) or (lo + 1)
    yw = _y_label_width(lo, hi)
    chart_w = width - yw - 2
    n = len(values)

    canvas = Canvas(chart_w, height + 1)
    ticks = y_axis_labels(lo, hi, height)
    tick_map = {row: label for row, label in ticks}
    normalised = normalise(values, lo, hi, height)

    # Plot points and connecting lines
    prev_x = prev_y = None
    step = max(1, chart_w // max(n - 1, 1))
    for i, norm in enumerate(normalised):
        px = min(i * step, chart_w - 1)
        py = height - int(round(norm))
        canvas.set(px, py, c(marker, color))

        if prev_x is not None and prev_y is not None:
            # Interpolate between previous and current point
            dx = px - prev_x
            dy = py - prev_y
            steps = max(abs(dx), abs(dy))
            for s in range(1, steps):
                ix = prev_x + round(s * dx / steps)
                iy = prev_y + round(s * dy / steps)
                if canvas.get(ix, iy) == " ":
                    if abs(dy) > abs(dx):
                        canvas.set(ix, iy, c("│", color))
                    else:
                        canvas.set(ix, iy, c("─", color))
        prev_x, prev_y = px, py

    lines = []
    if title:
        lines.append(_header(title, width, color))
        lines.append("")

    grid_rows = canvas.render().split("\n")
    for row_idx, grid_row in enumerate(grid_rows):
        label = tick_map.get(height - row_idx, "")
        sep = L if row_idx == height else V
        lines.append(label.rjust(yw) + " " + sep + " " + grid_row)

    x_axis = " " * (yw + 1) + B + H * (chart_w + 1)
    lines.append(x_axis)

    # Sample x labels
    lbl_row = " " * (yw + 2)
    shown = min(n, chart_w // 4)
    label_step = max(1, n // shown) if shown else n
    last_end = 0
    for i, lbl in enumerate(labels):
        if i % label_step == 0:
            pos = yw + 2 + min(i * step, chart_w - 1)
            padding = pos - last_end
            if padding > 0:
                short = lbl[:6]
                lbl_row += " " * padding + c(short, "dim")
                last_end = pos + len(short)

    lines.append(lbl_row)
    return "\n".join(lines)


# ── Histogram ────────────────────────────────────────────────────────────────

def histogram(
    values: list[float],
    title: str = "",
    bins: int = 10,
    width: int = 72,
    height: int = 16,
    color: str = "yellow",
) -> str:
    if not values:
        return "(no data)"

    lo, hi = min(values), max(values)
    if lo == hi:
        hi = lo + 1

    bin_size = (hi - lo) / bins
    counts = [0] * bins
    for v in values:
        idx = min(bins - 1, int((v - lo) / bin_size))
        counts[idx] += 1

    bin_labels = [_fmt(lo + i * bin_size) for i in range(bins)]
    return bar_chart(bin_labels, [float(c_) for c_ in counts],
                     title=title or f"Histogram ({bins} bins)",
                     width=width, height=height, color=color, show_values=False)


# ── Scatter plot ─────────────────────────────────────────────────────────────

def scatter(
    x_values: list[float],
    y_values: list[float],
    title: str = "",
    width: int = 60,
    height: int = 20,
    color: str = "cyan",
    marker: str = "·",
) -> str:
    if not x_values or not y_values:
        return "(no data)"

    x_lo, x_hi = min(x_values), max(x_values)
    y_lo, y_hi = min(y_values), max(y_values)
    if x_lo == x_hi: x_hi = x_lo + 1
    if y_lo == y_hi: y_hi = y_lo + 1

    yw = _y_label_width(y_lo, y_hi)
    chart_w = width - yw - 2

    canvas = Canvas(chart_w, height)
    for xv, yv in zip(x_values, y_values):
        px = int((xv - x_lo) / (x_hi - x_lo) * (chart_w - 1))
        py = height - 1 - int((yv - y_lo) / (y_hi - y_lo) * (height - 1))
        cur = canvas.get(px, py)
        if cur == " " or cur == marker:
            canvas.set(px, py, c(marker, color))
        else:
            canvas.set(px, py, c("✦", "yellow"))  # overlap indicator

    ticks = y_axis_labels(y_lo, y_hi, height - 1)
    tick_map = {row: label for row, label in ticks}

    lines = []
    if title:
        lines.append(_header(title, width, color))
        lines.append("")

    grid_rows = canvas.render().split("\n")
    for row_idx, grid_row in enumerate(grid_rows):
        label = tick_map.get(height - 1 - row_idx, "")
        sep = L if row_idx == height - 1 else V
        lines.append(label.rjust(yw) + " " + sep + " " + grid_row)

    x_axis = " " * (yw + 1) + B + H * (chart_w + 1)
    lines.append(x_axis)
    lines.append(" " * (yw + 2) + c(_fmt(x_lo), "dim") + " " * (chart_w - 8) + c(_fmt(x_hi), "dim"))
    return "\n".join(lines)
