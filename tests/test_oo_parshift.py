# Copyright (c) 2022-2023 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE or copy
# at http://opensource.org/licenses/MIT)

import os
from os import path

import matplotlib.pyplot as plt
import pandas as pd
import pytest

from parshift import Parshift


def test_process(file_csv_good):
    """Test that `load_and_process` fills stats and annotation attributes."""
    model = Parshift()
    model.process(file_csv_good["csv_in"], **(file_csv_good["kwargs"]))
    assert type(model.annotation) == type(pd.DataFrame())
    assert type(model.stats) == type(pd.DataFrame())

    model = Parshift()
    model.process(file_csv_good["csv_in"], **(file_csv_good["kwargs"]), N=2)
    assert type(model.annotation) == type(pd.DataFrame())
    assert isinstance(model.stats, list)


@pytest.mark.parametrize("N,expecterr", [(5, ValueError)])
def test_process_error(file_csv_good, N, expecterr):
    model = Parshift()
    with pytest.raises(expecterr):
        model.process(file_csv_good["csv_in"], **(file_csv_good["kwargs"]), N=N)


def test_show_plot(file_csv_good, monkeypatch):
    # Patch plt.show() so that it doesn't do anything, otherwise tests will hang
    monkeypatch.setattr(plt, "show", lambda *args, **kwargs: None)

    model = Parshift()
    model.process(file_csv_good["csv_in"], **(file_csv_good["kwargs"]))
    model.show_plot()
    model.show_plot(type="Pshift_class")

    model = Parshift()
    model.process(file_csv_good["csv_in"], N=2, **(file_csv_good["kwargs"]))
    model.show_plot()
    model.show_plot(type="Pshift_class")

    model.show_plot(filename="test")
    assert path.exists("test.png")
    if path.exists("test.png"):
        os.remove("test.png")


@pytest.mark.parametrize("type,expecterr", [(1, TypeError), ("Bye", ValueError)])
def test_show_plot_errors(file_csv_good, type, expecterr):
    model = Parshift()

    with pytest.raises(ValueError):
        model.show_plot()

    model.process(file_csv_good["csv_in"], **(file_csv_good["kwargs"]))
    with pytest.raises(expecterr):
        model.show_plot(type=type)

    with pytest.raises(TypeError):
        model.show_plot(filename=1)


def test_show_stats(file_csv_good):
    model = Parshift()
    model.process(file_csv_good["csv_in"], **(file_csv_good["kwargs"]))
    model.show_stats(filename="test")
    assert path.exists("test.csv")
    if path.exists("test.csv"):
        os.remove("test.csv")

    model = Parshift()
    n = 2
    model.process(file_csv_good["csv_in"], N=n, **(file_csv_good["kwargs"]))
    model.show_stats(filename="test")
    for i in range(n):
        assert path.exists(f"test_n{i+1}.csv")
        if path.exists(f"test_n{i+1}.csv"):
            os.remove(f"test_n{i+1}.csv")


def test_show_stats_errors():
    model = Parshift()
    with pytest.raises(ValueError):
        model.show_stats()


def test_get_propensities_error():
    model = Parshift()
    with pytest.raises(ValueError):
        model.get_propensities()


def test_get_propensities(file_csv_good):
    model = Parshift()
    model.process(file_csv_good["csv_in"], **(file_csv_good["kwargs"]))
    result = model.get_propensities()
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ["turn-receiving", "targeting", "termination"]

    model.process(file_csv_good["csv_in"], **(file_csv_good["kwargs"]), N=2)
    result = model.get_propensities()
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ["turn-receiving", "targeting", "termination"]
    assert list(result.index) == ["n1", "n2"]
    model.get_propensities(filename="test_propensities")
    assert path.exists("test_propensities.csv")
    if path.exists("test_propensities.csv"):
        os.remove("test_propensities.csv")
