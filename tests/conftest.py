# Copyright (c) 2022-2023 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE.txt or copy
# at http://opensource.org/licenses/MIT)

"""Fixtures to be used by test functions."""

from os import PathLike
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

# Files containing good conversations, optional parameters required to open them,
# and CSV file containing respective conversation after annotation
_good_conversations = [
    {
        "csv_in": "conv_good.csv",
        "kwargs": {},
        "csv_out": "df_good.csv",
    },
    {
        "csv_in": "conv_good_diffsep.csv",
        "kwargs": {"sep": ";", "quotechar": '"'},
        "csv_out": "df_good.csv",
    },
]

# CSV files containing a conversation after annotation and their expected
# frequency tables
_good_results = [
    {
        "csv_out": "df_good.csv",
        "freq_table": {
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
        },
    },
]

# Incorrect parametrizations of read_ccsv() and expected errors
_bad_params_read_ccsv = [
    {
        "csv_in": 10,
        "kwargs": {},
        "expected_error": ValueError,
    },
    {
        "csv_in": "__this_file_does_not_exist_at_all.csv",
        "kwargs": {},
        "expected_error": FileNotFoundError,
    },
    {
        "csv_in": "some_file.csv",
        "kwargs": {
            "invalid_param_name": "whatever",
        },
        "expected_error": TypeError,
    },
    {
        "csv_in": "conv_missing_id.csv",
        "kwargs": {},
        "expected_error": ValueError,
    },
    {
        "csv_in": "conv_missing_target_and_reply.csv",
        "kwargs": {},
        "expected_error": ValueError,
    },
    {
        "csv_in": "conv_no_id_but_target_and_reply.csv",
        "kwargs": {},
        "expected_error": ValueError,
    },
]


# Mandatory columns and types of conversation dataframe
_p_shift_cols_mandatory = {
    "id": np.int64,
    "user_id": np.int64,
    "message_text": np.dtype("O"),
}

# Optional columns and types of conversation dataframe
_p_shift_cols_optional = {
    "reply_id": np.dtype("O"),
    "target_id": np.dtype("O"),
}


@pytest.fixture()
def p_shift_cols_mandatory():
    """The mandatory columns and types of conversation dataframe."""
    return _p_shift_cols_mandatory


@pytest.fixture()
def p_shift_cols_optional():
    """The optional columns and types of conversation dataframe."""
    return _p_shift_cols_optional


@pytest.fixture()
def datapath(request):
    """The path containing the test data."""
    return Path(request.path.parent, "data")


@pytest.fixture(params=_good_results)
def pshift_freq_table(datapath, request):
    """The dataframe supposed to be generated when reading the good input data."""
    return {
        "df_ps": pd.read_csv(
            Path(datapath, request.param["csv_out"]), index_col=False
        ).fillna(""),
        "freq_table": request.param["freq_table"],
    }


@pytest.fixture(params=_good_conversations)
def file_csv_good(datapath, request):
    """Location of correct CSV test file."""
    return {
        "csv_in": Path(datapath, request.param["csv_in"]),
        "kwargs": request.param["kwargs"],
        "csv_out": Path(datapath, request.param["csv_out"]),
    }


@pytest.fixture(params=_bad_params_read_ccsv)
def file_read_ccsv_bad(datapath, request):
    """Parameters for generating errors in `read_ccsv()`."""
    csv_in = request.param["csv_in"]
    if type(csv_in) in {str, bytes, PathLike}:
        csv_in = Path(datapath, csv_in)

    return {
        "csv_in": csv_in,
        "kwargs": request.param["kwargs"],
        "expected_error": request.param["expected_error"],
    }
