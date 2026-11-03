# Copyright (c) 2022-2023 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE or copy
# at http://opensource.org/licenses/MIT)

import pandas as pd
import pytest

from parshift import annotate, pshift_class, read_ccsv


def test_read_ccsv_return(file_csv_good, p_shift_cols_mandatory, p_shift_cols_optional):
    """Test that `read_ccsv()` returns a data frame with the appropriate columns."""

    # Get the object read by read_ccsv()
    df_conv = read_ccsv(file_csv_good["csv_in"], **(file_csv_good["kwargs"]))

    # Is it a data frame?
    assert type(df_conv) == type(pd.DataFrame())

    # Does it have the required columns of the required type?
    for col_name in p_shift_cols_mandatory:
        assert col_name in df_conv.columns
        assert p_shift_cols_mandatory[col_name](df_conv.dtypes[col_name])

    # Does it have one of the optional columns with the correct type?
    num_opt_cols = 0
    for col_name in p_shift_cols_optional:
        if col_name in df_conv.columns:
            assert p_shift_cols_optional[col_name](df_conv.dtypes[col_name])
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
        file_csv_good["csv_out"], index_col=False, dtype=object
    ).fillna("")

    # Apply the annotate() function on the conversation
    conv_annot = annotate(df_read_ccsv)

    # Check that the annotate() function returns the expected type
    assert type(conv_annot) == type(parshift_annotation_df)

    # Check that the annotate() function returns a data frame with the expected
    # shape/size
    assert conv_annot.shape == parshift_annotation_df.shape

    # Check that the participation shifts are as expected
    assert (
        parshift_annotation_df["pshift"].values == conv_annot["pshift"].values
    ).all()


@pytest.mark.parametrize("last_col", ["reply_to_id", "target_id"])
def test_annotate_empty(last_col):
    """Test that `annotate()` returns an empty data frame for an empty conversation."""

    conv = pd.DataFrame(
        {"utterance_id": [], "speaker_id": [], "utterance": [], last_col: []}
    )
    conv_annot = annotate(conv)

    assert conv_annot.shape == (0, 5)
    assert list(conv_annot.columns) == [
        "utterance_ids",
        "speaker_id",
        "utterance",
        last_col,
        "pshift",
    ]


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
    assert pshift_class(ps) == pstype


@pytest.mark.parametrize("ps,expecterr", [(1, TypeError), ("hi", ValueError)])
def test_pshift_type_errors(ps, expecterr):
    """Test that `pshift_type()` throws the expected errors."""
    with pytest.raises(expecterr):
        pshift_class(ps)


def _conversation(rows):
    """Build a conversation data frame in reply mode from a list of tuples."""
    return pd.DataFrame(
        rows, columns=["utterance_id", "speaker_id", "utterance", "reply_to_id"]
    )


@pytest.mark.parametrize(
    "names",
    [
        ("Vitor", "Antonio", "Beto", "Ana"),
        ("tom", "Bob", "Eve", "Dan"),
        ("Ana Maria", "AnaMaria", "Eve", "Dan"),
        ("group", "Bob", "Eve", "Dan"),
        ("Smith, J", "Bob", "Eve", "Dan"),
    ],
)
def test_annotate_speaker_names_are_opaque(names):
    """Test that speaker IDs with "to", spaces, commas or equal to "group" are
    treated as any other ID."""
    s1, s2, s3, s4 = names
    conv = _conversation(
        [
            (0, s1, "a", ""),
            (1, s2, "b", 0),
            (2, s3, "c", ""),
            (3, s2, "d", ""),
            (4, s4, "e", 2),
            (5, s1, "f", 4),
            (6, s2, "g", 5),
        ]
    )
    assert list(annotate(conv)["pshift"]) == [
        "",
        "A0-XA",
        "AB-X0",
        "A0-X0",
        "A0-XA",
        "AB-XA",
        "AB-XA",
    ]


def test_annotate_strips_speaker_whitespace():
    """Test that leading and trailing spaces do not distinguish speakers."""
    conv = _conversation([(0, " 10", "a", ""), (1, "11", "b", 0), (2, "10", "c", 1)])
    result = annotate(conv)
    assert list(result["pshift"]) == ["", "A0-XA", "AB-BA"]
    assert list(result["speaker_id"]) == [" 10", "11", "10"]


def test_annotate_unknown_reply_warns():
    """Test that a reply to an utterance not in a previous turn is considered as
    addressed to the group, with a warning."""
    conv = _conversation(
        [(0, "S1", "a", ""), (1, "S2", "b", 0), (2, "S3", "c", 999), (3, "S4", "d", "")]
    )
    with pytest.warns(UserWarning, match="1 turn"):
        result = annotate(conv)
    assert list(result["pshift"]) == ["", "A0-XA", "AB-X0", "A0-X0"]


def test_annotate_self_reply_is_addressed_to_group():
    """Test that a speaker replying to themselves is considered as addressing the
    group, with a warning."""
    conv = _conversation(
        [(0, "S1", "a", ""), (1, "S2", "b", 0), (2, "S1", "c", 1), (3, "S1", "d", 0)]
    )
    with pytest.warns(UserWarning, match="1 turn.*themselves"):
        result = annotate(conv)
    assert list(result["pshift"]) == ["", "A0-XA", "AB-BA", "AB-A0"]


def test_annotate_self_target_is_addressed_to_group():
    """Test that a speaker targeting themselves is considered as addressing the
    group, with a warning."""
    conv = pd.DataFrame(
        [(0, "10", "a", ""), (1, "11", "b", 10), (2, "10", "c", 10)],
        columns=["utterance_id", "speaker_id", "utterance", "target_id"],
    )
    with pytest.warns(UserWarning, match="1 turn.*themselves"):
        result = annotate(conv)
    assert list(result["pshift"]) == ["", "A0-XA", "AB-B0"]


def test_annotate_merges_turns_with_same_addressee():
    """Test that consecutive messages from the same speaker to the same addressee
    are in the same turn, even if they reply to different utterances."""
    conv = _conversation(
        [
            (0, "S1", "a", ""),
            (1, "S1", "b", ""),
            (2, "S2", "c", 0),
            (3, "S2", "d", 1),
            (4, "S3", "e", ""),
        ]
    )
    result = annotate(conv)
    assert list(result["utterance_ids"]) == ["[0, 1]", "[2, 3]", "[4]"]
    assert list(result["utterance"]) == ["a. b", "c. d", "e"]
    assert list(result["reply_to_id"]) == ["None", "0", "None"]
    assert list(result["pshift"]) == ["", "A0-XA", "AB-X0"]
