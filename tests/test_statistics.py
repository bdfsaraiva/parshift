# Copyright (c) 2022-2023 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE or copy
# at http://opensource.org/licenses/MIT)

import pandas as pd
import pytest

from parshift import cond_probs
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
        "pshift",
        "Frequency",
        "Probability",
        "CP",
        "CPeTC",
    ]


@pytest.mark.parametrize(
    "pscodes,expecterr", [(1, TypeError), ("Bye", TypeError), ({}, TypeError)]
)
def test_cond_probs_errors(pscodes, expecterr):
    with pytest.raises(expecterr):
        cond_probs(pscodes)
