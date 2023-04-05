# Copyright (c) 2022-2023 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE or copy
# at http://opensource.org/licenses/MIT)

from parshift import Parshift
import pandas as pd
import matplotlib.pyplot as plt
import pytest


def test_load_and_process(file_csv_good):
    """Test that `load_and_process` fills stats and annotation attributes."""
    model = Parshift()
    model.load_and_process(file_csv_good["csv_in"], **(file_csv_good["kwargs"]))
    assert type(model.annotation) == type(pd.DataFrame())
    assert type(model.stats) == type(pd.DataFrame())

    model = Parshift()
    model.load_and_process(file_csv_good["csv_in"], **(file_csv_good["kwargs"]), N=2)
    assert type(model.annotation) == type(pd.DataFrame())
    assert isinstance(model.stats, list)


@pytest.mark.parametrize("N,expecterr", [(5, ValueError)])
def test_load_and_process_error(file_csv_good, N, expecterr):
    model = Parshift()
    with pytest.raises(expecterr):
        model.load_and_process(
            file_csv_good["csv_in"], **(file_csv_good["kwargs"]), N=N
        )


def test_get_plot_error():
    model = Parshift()
    with pytest.raises(ValueError):
        model.get_plot()


def test_get_plot(file_csv_good):
    model = Parshift()
    model.load_and_process(file_csv_good["csv_in"], **(file_csv_good["kwargs"]))
    _, ax = plt.subplots()
    assert type(ax) == type(model.get_plot())
    assert type(ax) == type(model.get_plot(type="pshift_class"))

    model = Parshift()
    model.load_and_process(file_csv_good["csv_in"], N=2, **(file_csv_good["kwargs"]))
    _, ax = plt.subplots(1, 2)
    assert type(ax) == type(model.get_plot())
    assert type(ax) == type(model.get_plot(type="pshift_class"))
