import pytest
from termchart.charts import bar_chart, line_chart, histogram, scatter


def test_bar_chart_returns_string():
    result = bar_chart(["A", "B", "C"], [10.0, 20.0, 15.0])
    assert isinstance(result, str)
    assert len(result) > 0


def test_bar_chart_contains_title():
    result = bar_chart(["A"], [5.0], title="My Title")
    assert "My Title" in result


def test_bar_chart_empty_returns_message():
    result = bar_chart([], [], title="empty")
    assert "no data" in result.lower()


def test_bar_chart_single_value():
    result = bar_chart(["only"], [42.0])
    assert isinstance(result, str)


def test_bar_chart_negative_values():
    result = bar_chart(["A", "B"], [-5.0, 10.0])
    assert isinstance(result, str)


def test_line_chart_returns_string():
    result = line_chart(["1", "2", "3", "4"], [1.0, 4.0, 2.0, 5.0])
    assert isinstance(result, str)
    assert len(result) > 0


def test_line_chart_with_title():
    result = line_chart(["x"], [1.0], title="Trend")
    assert "Trend" in result


def test_line_chart_empty_returns_message():
    result = line_chart([], [])
    assert "no data" in result.lower()


def test_histogram_returns_string():
    values = [1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 4.0, 5.0]
    result = histogram(values, bins=4)
    assert isinstance(result, str)


def test_histogram_custom_bins():
    values = list(range(1, 21))
    result = histogram([float(v) for v in values], bins=5)
    assert isinstance(result, str)


def test_histogram_empty_returns_message():
    result = histogram([])
    assert "no data" in result.lower()


def test_scatter_returns_string():
    result = scatter([1.0, 2.0, 3.0], [3.0, 1.0, 4.0])
    assert isinstance(result, str)


def test_scatter_empty_returns_message():
    result = scatter([], [])
    assert "no data" in result.lower()


def test_scatter_with_title():
    result = scatter([1.0, 2.0], [2.0, 4.0], title="Age vs Score")
    assert "Age vs Score" in result


def test_bar_chart_respects_width():
    narrow = bar_chart(["A", "B"], [1.0, 2.0], width=40)
    wide   = bar_chart(["A", "B"], [1.0, 2.0], width=80)
    narrow_max = max(len(l) for l in narrow.split("\n"))
    wide_max   = max(len(l) for l in wide.split("\n"))
    assert wide_max >= narrow_max
