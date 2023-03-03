import pytest
import pandas as pd
from parshift import conditional_probabilities
from parshift.conditional_probabilities import _frequency_table

parshift_annotation_df = pd.read_csv("tests/df.csv", index_col=False).fillna("")


def test_frequency_table():

    result = _frequency_table(parshift_annotation_df)
    assert isinstance(result, list)
    assert len(result) == 5
    expected_result_df = {
        "AB-BA": 0,
        "AB-B0": 0,
        "AB-BY": 0,
        "A0-X0": 1,
        "A0-XA": 2,
        "A0-XY": 0,
        "AB-X0": 1,
        "AB-XA": 1,
        "AB-XB": 0,
        "AB-XY": 0,
        "A0-AY": 0,
        "AB-A0": 1,
        "AB-AY": 0,
    }
    assert result[0] == expected_result_df


def test_conditional_probabilities_errors():
    with pytest.raises(TypeError):
        conditional_probabilities(1)
    with pytest.raises(TypeError):
        conditional_probabilities("Bye")
    with pytest.raises(TypeError):
        conditional_probabilities(dict())


def test_conditional_probabilities():
    result = conditional_probabilities(parshift_annotation_df)
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == [
        "pshift",
        "Frequency",
        "Probability",
        "CP",
        "CPeTC",
    ]
