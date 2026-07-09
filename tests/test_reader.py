import pytest
import csv
from pathlib import Path
from termchart.reader import read_csv, Column, summary


def make_csv(tmp_path, data: dict, filename="data.csv") -> Path:
    path = tmp_path / filename
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(data.keys()))
        writer.writeheader()
        rows = [dict(zip(data.keys(), vals)) for vals in zip(*data.values())]
        writer.writerows(rows)
    return path


def test_read_csv_basic(tmp_path):
    path = make_csv(tmp_path, {"month": ["Jan","Feb","Mar"], "sales": [100,200,150]})
    labels, y, x = read_csv(path, x_col="month", y_col="sales")
    assert labels == ["Jan", "Feb", "Mar"]
    assert y.values == [100.0, 200.0, 150.0]
    assert x is None  # categorical x


def test_read_csv_numeric_x(tmp_path):
    path = make_csv(tmp_path, {"age": [1,2,3], "score": [10,20,30]})
    labels, y, x = read_csv(path, x_col="age", y_col="score")
    assert x is not None
    assert x.values == [1.0, 2.0, 3.0]


def test_read_csv_default_y_is_first_numeric(tmp_path):
    path = make_csv(tmp_path, {"name": ["a","b"], "price": [5,10], "qty": [2,3]})
    _, y, _ = read_csv(path)
    assert y.name == "price"


def test_read_csv_default_labels_are_row_numbers(tmp_path):
    path = make_csv(tmp_path, {"val": [9, 8, 7]})
    labels, _, _ = read_csv(path)
    assert labels == ["1", "2", "3"]


def test_read_csv_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        read_csv("/nonexistent/file.csv")


def test_read_csv_missing_column_raises(tmp_path):
    path = make_csv(tmp_path, {"a": [1,2]})
    with pytest.raises(ValueError, match="not found"):
        read_csv(path, y_col="zzz")


def test_read_csv_no_numeric_columns_raises(tmp_path):
    path = make_csv(tmp_path, {"name": ["x","y"], "code": ["a","b"]})
    with pytest.raises(ValueError, match="No numeric"):
        read_csv(path)


def test_column_properties():
    col = Column(name="x", values=[1.0, 2.0, 3.0, 4.0], raw=["1","2","3","4"])
    assert col.min == 1.0
    assert col.max == 4.0
    assert col.mean == 2.5
    assert col.total == 10.0
    assert len(col) == 4


def test_summary_output(tmp_path):
    path = make_csv(tmp_path, {"val": [10, 20, 30, 40, 50]})
    _, y, _ = read_csv(path)
    s = summary(y)
    assert "Min" in s
    assert "Max" in s
    assert "Mean" in s
    assert "Stdev" in s
