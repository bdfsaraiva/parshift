import matplotlib.pyplot as plt
import pandas as pd

from parshift import conditional_probabilities, frequency_treemap


def test_frequency_treemap(pshift_freq_table):
    conditional_probabilities_df = conditional_probabilities(
        pshift_freq_table["df_ps"]
    )
    _, ax = plt.subplots()
    assert type(ax) == type(frequency_treemap(conditional_probabilities_df))
    assert type(ax) == type(
        frequency_treemap(conditional_probabilities_df, column_name="pshift_type")
    )
