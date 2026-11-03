# Copyright (c) 2022-2023 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE or copy
# at http://opensource.org/licenses/MIT)

import matplotlib.pyplot as plt
import pytest

from parshift import cond_probs, frequency_treemap


def test_frequency_treemap(pshift_freq_table):
    conditional_probabilities_df = cond_probs(pshift_freq_table["df_ps"])
    _, ax = plt.subplots()
    assert type(ax) == type(frequency_treemap(conditional_probabilities_df))
    assert type(ax) == type(
        frequency_treemap(conditional_probabilities_df, type="Pshift_class")
    )


@pytest.mark.parametrize("type,expecterr", [(1, TypeError), ("Bye", ValueError)])
def test_frequency_treemap_errors(pshift_freq_table, type, expecterr):
    conditional_probabilities_df = cond_probs(pshift_freq_table["df_ps"])
    with pytest.raises(expecterr):
        frequency_treemap(conditional_probabilities_df, type=type)


@pytest.mark.parametrize("type", ["Pshift", "Pshift_class"])
def test_frequency_treemap_does_not_mutate_input(pshift_freq_table, type):
    conditional_probabilities_df = cond_probs(pshift_freq_table["df_ps"])
    columns_before = list(conditional_probabilities_df.columns)
    frequency_treemap(conditional_probabilities_df, type=type)
    assert list(conditional_probabilities_df.columns) == columns_before
    plt.close("all")


def test_frequency_treemap_hides_given_axes_only(pshift_freq_table):
    conditional_probabilities_df = cond_probs(pshift_freq_table["df_ps"])
    _, (a1, a2) = plt.subplots(1, 2)
    plt.sca(a2)
    frequency_treemap(conditional_probabilities_df, ax=a1)
    assert a1.axison is False
    assert a2.axison is True
    plt.close("all")
