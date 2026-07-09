# termchart

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-24%20passing-brightgreen)
![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen)

**Render Unicode bar charts, line charts, histograms, and scatter plots in the terminal from any CSV file. Zero runtime dependencies.**

```
termchart bar data.csv --y sales --x month
```

```
                        Monthly Sales

      200  │  ████
           │  ████
           │  ████             ████
      150  ├  ████             ████  ████
           │  ████  ████       ████  ████
      100  ├  ████  ████  ████ ████  ████
           │  ████  ████  ████ ████  ████
        0  └──────────────────────────────
              Jan   Feb   Mar   Apr   May
              200   180   90    210   160
```

## Install

```bash
git clone https://github.com/NzJulien/termchart.git
cd termchart
pip install -e .
```

## Commands

```bash
termchart bar     data.csv --y revenue --x quarter
termchart line    data.csv --y temperature --x date --color green
termchart hist    data.csv --y price --bins 15
termchart scatter data.csv --x age --y salary --color yellow
termchart info    data.csv --y price
```

## Options

| Flag | Description |
|---|---|
| `--y` | Column to chart (default: first numeric column) |
| `--x` | Label / x-axis column |
| `--title` | Chart title |
| `--width` | Total chart width in characters (default 72) |
| `--height` | Chart height in rows (default 16) |
| `--color` | cyan, green, yellow, red, blue |
| `--bins` | Histogram bin count (default 10) |

## Library usage

```python
from termchart import bar_chart, line_chart, histogram, scatter
from termchart import read_csv

labels, y, x = read_csv("data.csv", x_col="month", y_col="sales")

print(bar_chart(labels, y.values, title="Monthly Sales", color="cyan"))
print(line_chart(labels, y.values, title="Trend", color="green"))
print(histogram(y.values, bins=8))

if x:
    print(scatter(x.values, y.values, title="X vs Y"))
```

## How it works

termchart draws directly to strings using Unicode block elements
(`▁▂▃▄▅▆▇█`) for sub-character vertical resolution, box-drawing
characters (`─│┌┐└┘├┤┬┴┼`) for axes, and ANSI escape codes for color.
No matplotlib, no numpy, no pandas — just the Python standard library.

## Project layout

```
termchart/
├── termchart/
│   ├── canvas.py   # low-level Unicode drawing canvas + color helpers
│   ├── reader.py   # CSV loading, column typing, summary stats
│   ├── charts.py   # bar, line, histogram, scatter renderers
│   └── cli.py      # argparse CLI: bar, line, hist, scatter, info
├── tests/          # pytest suite (24 tests)
└── setup.py
```

## Running the tests

```bash
pip install -e ".[dev]"
pytest -v
```

Made by [NzJulien](https://github.com/NzJulien)
