# Copyright (c) 2022-2023 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE or copy
# at http://opensource.org/licenses/MIT)

import pandas as pd
import pytest

from parshift import annotate, pshift_type, read_ccsv


def test_read_ccsv_return(file_csv_good, p_shift_cols_mandatory, p_shift_cols_optional):
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


def test_read_ccsv_errors(file_read_ccsv_bad):
    """Test errors raised by `read_ccsv()`."""
    with pytest.raises(file_read_ccsv_bad["expected_error"]):
        read_ccsv(file_read_ccsv_bad["csv_in"], **(file_read_ccsv_bad["kwargs"]))


def test_annotate_return(file_csv_good):
    """Test that `annotate()` returns the expected data frame."""

    # Read the conversation
    df_read_ccsv = read_ccsv(
        file_csv_good["csv_in"], **(file_csv_good["kwargs"])
    ).reset_index(drop=False)

    # Read the expected results
    parshift_annotation_df = pd.read_csv(
        file_csv_good["csv_out"], index_col=False
    ).fillna("")

    # Apply the annotate() function on the conversation
    conv_annot = annotate(df_read_ccsv)

    # Check that the annotate() function returns the expected type
    assert type(conv_annot) == type(parshift_annotation_df)

    # Check that the annotate() function returns a dataframe with the expected
    # shape/size
    assert conv_annot.shape == parshift_annotation_df.shape

    # Check that the participation shifts are as expected
    assert (
        parshift_annotation_df["pshift"].values == conv_annot["pshift"].values
    ).all()


@pytest.mark.parametrize(
    "conv,expecterr", [(10, TypeError), ("some_string", TypeError)]
)
def test_annotate_errors(conv, expecterr):
    """Test errors raised by `annotate()`."""
    with pytest.raises(expecterr):
        annotate(conv)


@pytest.mark.parametrize(
    "ps,pstype",
    [
        ("AB-BA", "Turn Receiving"),
        ("AB-BA", "Turn Receiving"),
        ("AB-B0", "Turn Receiving"),
        ("AB-BY", "Turn Receiving"),
        ("A0-X0", "Turn Claiming"),
        ("A0-XA", "Turn Claiming"),
        ("A0-XY", "Turn Claiming"),
        ("AB-X0", "Turn Usurping"),
        ("AB-XA", "Turn Usurping"),
        ("AB-XB", "Turn Usurping"),
        ("AB-XY", "Turn Usurping"),
        ("A0-AY", "Turn Continuing"),
        ("AB-A0", "Turn Continuing"),
        ("AB-AY", "Turn Continuing"),
    ],
)
def test_pshift_type_return(ps, pstype):
    """Test that `pshift_type()` returns the expected type of p-shift."""
    assert pshift_type(ps) == pstype


@pytest.mark.parametrize("ps,expecterr", [(1, TypeError), ("hi", ValueError)])
def test_pshift_type_errors(ps, expecterr):
    """Test that `pshift_type()` throws the expected errors."""
    with pytest.raises(expecterr):
        pshift_type(ps)
