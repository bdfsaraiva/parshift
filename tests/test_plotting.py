import matplotlib.pyplot as plt
import pandas as pd
from parshift import conditional_probabilities
from parshift import frequency_treemap


parshift_annotation_df = pd.read_csv("tests/df.csv").fillna("")


def test_frequency_treemap():
    conditional_probabilities_df = conditional_probabilities(parshift_annotation_df)
    _, ax = plt.subplots()
    assert type(ax) == type(frequency_treemap(conditional_probabilities_df))
