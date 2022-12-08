import matplotlib
import pandas as pd
from parshift import conditional_probabilities
from parshift import plotting


parshift_annotation_df = pd.read_csv("tests/df.csv").fillna("")


def test_frequency_treemap():
    conditional_probabilities_df = conditional_probabilities.conditional_probabilities(
        parshift_annotation_df
    )
    assert isinstance(
        plotting.frequency_treemap(conditional_probabilities_df),
        matplotlib.figure.Figure,
    )
