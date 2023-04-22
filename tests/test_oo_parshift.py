# Copyright (c) 2022-2023 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE or copy
# at http://opensource.org/licenses/MIT)

from parshift import Parshift
import pandas as pd
import matplotlib.pyplot as plt
import pytest


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


def test_get_plot(file_csv_good, monkeypatch):

    # Patch plt.show() so that it doesn't do anything, otherwise tests will hang
    monkeypatch.setattr(plt, "show", lambda *args, **kwargs: None)

    model = Parshift()
    model.process(file_csv_good["csv_in"], **(file_csv_good["kwargs"]))
    model.get_plot()
    model.get_plot(type="Pshift_class")

    model = Parshift()
    model.process(file_csv_good["csv_in"], N=2, **(file_csv_good["kwargs"]))
    model.get_plot()
    model.get_plot(type="Pshift_class")


@pytest.mark.parametrize("type,expecterr", [(1, TypeError), ("Bye", ValueError)])
def test_get_plot_errors(file_csv_good, type, expecterr):
    model = Parshift()

    with pytest.raises(ValueError):
        model.get_plot()

    model.process(file_csv_good["csv_in"], **(file_csv_good["kwargs"]))
    with pytest.raises(expecterr):
        model.get_plot(type=type)


def test_get_stats(file_csv_good):
    model = Parshift()
    model.process(file_csv_good["csv_in"], **(file_csv_good["kwargs"]))
    model.get_stats()

    model = Parshift()
    model.process(file_csv_good["csv_in"], N=2, **(file_csv_good["kwargs"]))
    model.get_stats()


def test_get_stats_errors():
    model = Parshift()
    with pytest.raises(ValueError):
        model.get_stats()
