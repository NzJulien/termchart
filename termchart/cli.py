"""Command-line interface for termchart.

Usage:
    termchart bar   data.csv --y sales --x month
    termchart line  data.csv --y temperature --x date
    termchart hist  data.csv --y price --bins 15
    termchart scatter data.csv --x age --y salary
    termchart info  data.csv --y price
"""
from __future__ import annotations

import argparse
import sys

from .charts import bar_chart, histogram, line_chart, scatter
from .reader import read_csv, summary


def cmd_bar(args: argparse.Namespace) -> int:
    labels, y, _ = read_csv(args.csv, x_col=args.x, y_col=args.y)
    print()
    print(bar_chart(labels, y.values, title=args.title or y.name,
                    width=args.width, height=args.height, color=args.color))
    print()
    return 0


def cmd_line(args: argparse.Namespace) -> int:
    labels, y, _ = read_csv(args.csv, x_col=args.x, y_col=args.y)
    print()
    print(line_chart(labels, y.values, title=args.title or y.name,
                     width=args.width, height=args.height, color=args.color))
    print()
    return 0


def cmd_hist(args: argparse.Namespace) -> int:
    _, y, _ = read_csv(args.csv, y_col=args.y)
    print()
    print(histogram(y.values, title=args.title or y.name,
                    bins=args.bins, width=args.width, height=args.height, color=args.color))
    print()
    return 0


def cmd_scatter(args: argparse.Namespace) -> int:
    if not args.x:
        print("scatter requires --x <column>", file=sys.stderr)
        return 1
    labels, y, x = read_csv(args.csv, x_col=args.x, y_col=args.y)
    if x is None:
        print(f"--x column must be numeric for scatter plots", file=sys.stderr)
        return 1
    print()
    print(scatter(x.values, y.values, title=args.title or f"{x.name} vs {y.name}",
                  width=args.width, height=args.height, color=args.color))
    print()
    return 0


def cmd_info(args: argparse.Namespace) -> int:
    _, y, _ = read_csv(args.csv, y_col=args.y)
    print()
    print(summary(y))
    print()
    return 0


def _add_common(p: argparse.ArgumentParser) -> None:
    p.add_argument("csv", help="Path to CSV file")
    p.add_argument("--y", dest="y", help="Column to chart (default: first numeric column)")
    p.add_argument("--x", dest="x", help="Label / x-axis column")
    p.add_argument("--title", help="Chart title")
    p.add_argument("--width",  type=int, default=72, help="Total chart width (default 72)")
    p.add_argument("--height", type=int, default=16, help="Chart height in rows (default 16)")
    p.add_argument("--color",  default="cyan",
                   choices=["cyan","green","yellow","red","blue"],
                   help="Bar/line color (default cyan)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="termchart",
        description="Render Unicode charts in the terminal from any CSV file.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_bar = sub.add_parser("bar", help="Horizontal bar chart")
    _add_common(p_bar)
    p_bar.set_defaults(func=cmd_bar)

    p_line = sub.add_parser("line", help="Line / time-series chart")
    _add_common(p_line)
    p_line.set_defaults(func=cmd_line)

    p_hist = sub.add_parser("hist", help="Histogram of a numeric column")
    _add_common(p_hist)
    p_hist.add_argument("--bins", type=int, default=10, help="Number of histogram bins (default 10)")
    p_hist.set_defaults(func=cmd_hist)

    p_scatter = sub.add_parser("scatter", help="Scatter plot (requires --x and --y, both numeric)")
    _add_common(p_scatter)
    p_scatter.set_defaults(func=cmd_scatter)

    p_info = sub.add_parser("info", help="Print column statistics")
    _add_common(p_info)
    p_info.set_defaults(func=cmd_info)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
