# Copyright (c) 2022-2023 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE.txt or copy
# at http://opensource.org/licenses/MIT)

"""Fixtures to be used by test functions."""

from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture()
def datapath(request):
    return Path(request.path.parent, "data")


@pytest.fixture()
def file_csv_df_result(datapath):
    """Location of the CSV file with the outputted dataframe."""
    return Path(datapath, "df_result.csv")


@pytest.fixture()
def parshift_annotation_df(file_csv_df_result):
    """The dataframe supposed to be generated when reading the good input data."""
    return pd.read_csv(file_csv_df_result, index_col=False).fillna("")


@pytest.fixture()
def file_csv_good(datapath):
    """Location of correct CSV test file."""
    return Path(datapath, "conv_good.csv")


@pytest.fixture()
def file_csv_good_diffsep(datapath):
    """Location of correct CSV test file with different delimiters, etc."""
    return Path(datapath, "conv_good_diffsep.csv")


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
