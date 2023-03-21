import matplotlib.pyplot as plt
import pandas as pd
import pytest

from parshift import cond_probs, frequency_treemap


def test_frequency_treemap(pshift_freq_table):
    conditional_probabilities_df = cond_probs(pshift_freq_table["df_ps"])
    _, ax = plt.subplots()
    assert type(ax) == type(frequency_treemap(conditional_probabilities_df))
    assert type(ax) == type(
        frequency_treemap(conditional_probabilities_df, column_name="pshift_type")
    )


def test_frequency_treemap_errors(pshift_freq_table):
    conditional_probabilities_df = cond_probs(pshift_freq_table["df_ps"])
    with pytest.raises(TypeError):
        frequency_treemap(conditional_probabilities_df, column_name=1)
    with pytest.raises(ValueError):
        frequency_treemap(conditional_probabilities_df, column_name="Bye")
