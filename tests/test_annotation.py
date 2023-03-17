# Copyright (c) 2022-2023 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE.txt or copy
# at http://opensource.org/licenses/MIT)

import pandas as pd
import pytest

from parshift import annotate, pshift_type, read_ccsv


def test_read_conversation(
    file_csv_good, p_shift_cols_mandatory, p_shift_cols_optional
):
    """Test that `read_ccsv()` returns a data frame with the appropriate columns."""

    # Get the object read by read_ccsv()
    df_conv = read_ccsv(file_csv_good["csv_in"], **(file_csv_good["kwargs"]))

    # Is it a data frame?
    assert type(df_conv) == type(pd.DataFrame())

    # Does it have the required columns of the required type?
    for col_name in p_shift_cols_mandatory:
        assert col_name in df_conv.columns
        assert p_shift_cols_mandatory[col_name] == df_conv.dtypes[col_name]

    # Does it have one of the optional columns with the correct type?
    num_opt_cols = 0
    for col_name in p_shift_cols_optional:
        if col_name in df_conv.columns:
            assert p_shift_cols_optional[col_name] == df_conv.dtypes[col_name]
            num_opt_cols += 1
    assert num_opt_cols > 0


def test_read_conversation_errors(file_read_ccsv_bad):
    with pytest.raises(file_read_ccsv_bad["expected_error"]):
        read_ccsv(file_read_ccsv_bad["csv_in"], **(file_read_ccsv_bad["kwargs"]))


def test_parshift_annotation(file_csv_good):
    df_read_ccsv = read_ccsv(
        file_csv_good["csv_in"], **(file_csv_good["kwargs"])
    ).reset_index(drop=False)
    parshift_annotation_df = pd.read_csv(
        file_csv_good["csv_out"], index_col=False
    ).fillna("")

    assert type(annotate(df_read_ccsv)) == type(parshift_annotation_df)

    assert len(annotate(df_read_ccsv)) == len(parshift_annotation_df)

    # print(parshift_annotation_df["pshift"].values)
    print(parshift_annotation_df)
    # print(annotate(df_read_ccsv)["pshift"].values)
    assert (
        parshift_annotation_df["pshift"].values
        == annotate(df_read_ccsv)["pshift"].values
    ).all()


def test_pshift_type_values():
    assert pshift_type("AB-BA") == "Turn Receiving"


def test_pshift_type_errors():
    with pytest.raises(TypeError):
        pshift_type(1)
    with pytest.raises(ValueError):
        pshift_type("hi")
