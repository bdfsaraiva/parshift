# Copyright (c) 2022-2023 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE or copy
# at http://opensource.org/licenses/MIT)

from parshift import Parshift
import pandas as pd
import matplotlib.pyplot as plt
import pytest


def test_load_and_process(file_csv_good):
    """Test that `load_and_process` returns a dict."""
    model = Parshift()
    model.load_and_process(file_csv_good["csv_in"], **(file_csv_good["kwargs"]))
    assert type(model.annotation) == type(pd.DataFrame())
    assert type(model.stats) == type(pd.DataFrame())


def test_get_plot(file_csv_good):
    """Test that `load_and_process` returns a dict."""

    model = Parshift()
    model.load_and_process(file_csv_good["csv_in"], **(file_csv_good["kwargs"]))
    _, ax = plt.subplots()
    assert type(ax) == type(model.get_plot())
    assert type(ax) == type(model.get_plot(type="pshift_type"))
