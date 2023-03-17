# Copyright (c) 2022-2023 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE.txt or copy
# at http://opensource.org/licenses/MIT)

"""Fixtures to be used by test functions."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

_good_conversations = [
    {"csv_in": "conv_good.csv", "kwargs": {}, "csv_out": "df_good.csv"},
    {
        "csv_in": "conv_good_diffsep.csv",
        "kwargs": {"sep": ";", "quotechar": '"'},
        "csv_out": "df_good.csv",
    },
]

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
    }
]

_p_shift_cols_mandatory = {
    "id": np.int64,
    "user_id": np.int64,
    "message_text": np.dtype("O"),
}

_p_shift_cols_optional = {
    "reply_id": np.dtype("O"),
    "target_id": np.dtype("O"),
}


@pytest.fixture()
def p_shift_cols_mandatory():
    return _p_shift_cols_mandatory


@pytest.fixture()
def p_shift_cols_optional():
    return _p_shift_cols_optional


@pytest.fixture()
def datapath(request):
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


@pytest.fixture()
def file_csv_missing_id(datapath):
    """Location of CSV test file with missing ID."""
    return Path(datapath, "conv_missing_id.csv")


@pytest.fixture()
def file_csv_missing_target_and_reply(datapath):
    """Location of CSV test file with missing target and reply IDs."""
    return Path(datapath, "conv_missing_target_and_reply.csv")


@pytest.fixture()
def file_csv_no_id_but_target_and_reply(datapath):
    """Location of CSV test file with no ID but having target and reply IDs."""
    return Path(datapath, "conv_missing_target_and_reply.csv")
