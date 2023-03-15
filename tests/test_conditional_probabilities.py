import pandas as pd
import pytest

from parshift import conditional_probabilities
from parshift.conditional_probabilities import _frequency_table


def test_frequency_table(pshift_freq_table):
    result = _frequency_table(pshift_freq_table["df_ps"])
    assert isinstance(result, list)
    assert len(result) == 5
    assert result[0] == pshift_freq_table["freq_table"]


def test_conditional_probabilities_errors():
    with pytest.raises(TypeError):
        conditional_probabilities(1)
    with pytest.raises(TypeError):
        conditional_probabilities("Bye")
    with pytest.raises(TypeError):
        conditional_probabilities(dict())


def test_conditional_probabilities(pshift_freq_table):
    result = conditional_probabilities(pshift_freq_table["df_ps"])
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == [
        "pshift",
        "Frequency",
        "Probability",
        "CP",
        "CPeTC",
    ]
