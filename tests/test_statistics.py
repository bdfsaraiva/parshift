# Copyright (c) 2022-2026 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE or copy
# at http://opensource.org/licenses/MIT)

import pandas as pd
import pytest

from parshift import cond_probs, propensities
from parshift.statistics import _frequency_table


def test_frequency_table(pshift_freq_table):
    result = _frequency_table(pshift_freq_table["df_ps"])
    assert isinstance(result, list)
    assert len(result) == 5
    assert result[0] == pshift_freq_table["freq_table"]


def test_cond_probs_ok(pshift_freq_table):
    result = cond_probs(pshift_freq_table["df_ps"])
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == [
        "Pshift",
        "Frequency",
        "Probability",
        "P(S|D)",
        "P(S|D,C)",
        "Change of Speaker (C)",
        "Directed Remark (D)",
    ]


@pytest.mark.parametrize(
    "pscodes,expecterr", [(1, TypeError), ("Bye", TypeError), ({}, TypeError)]
)
def test_cond_probs_errors(pscodes, expecterr):
    with pytest.raises(expecterr):
        cond_probs(pscodes)


def test_propensities(pshift_freq_table):
    cond_probs_df = cond_probs(pshift_freq_table["df_ps"])
    result = propensities(cond_probs_df)
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ["turn-receiving", "targeting", "termination"]


@pytest.mark.parametrize(
    "pshifts,expected",
    [
        (
            ["A0-AY"] * 5,
            {"turn-receiving": 0.0, "targeting": 0.0, "termination": 1.0},
        ),
        (
            ["A0-XY"] * 5,
            {"turn-receiving": 0.0, "targeting": 1.0, "termination": 0.0},
        ),
        (
            ["AB-BA", "AB-BY", "AB-A0", "AB-AY"],
            {"turn-receiving": 0.5, "targeting": 0.5, "termination": 0.5},
        ),
    ],
)
def test_propensities_values(pshifts, expected):
    """Test the values of the propensities, as defined by Gibson (2003)."""
    result = propensities(cond_probs(pd.DataFrame({"pshift": pshifts})))
    for name, value in expected.items():
        assert result[name][0] == pytest.approx(value)


def test_cond_probs_warns_on_unknown_codes():
    """Test that codes outside the 13 participation shifts are reported."""
    with pytest.warns(UserWarning, match="1 turn.*A0-AA"):
        result = cond_probs(pd.DataFrame({"pshift": ["", "A0-XA", "A0-AA"]}))
    assert result["Frequency"].sum() == 1
