"""termchart — render Unicode charts in the terminal from CSV data.

Zero runtime dependencies beyond the Python standard library.

Modules
-------
- reader   : load and validate CSV data
- charts   : bar, line, histogram, and scatter renderers
- canvas   : low-level Unicode drawing canvas
- cli      : argparse CLI
"""
from .charts import bar_chart, line_chart, histogram, scatter
from .reader import read_csv, Column

__version__ = "1.0.0"
__all__ = ["bar_chart", "line_chart", "histogram", "scatter", "read_csv", "Column"]
