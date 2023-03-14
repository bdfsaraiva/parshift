import pandas as pd
import pytest

from parshift import annotate, pshift_type, read_ccsv

# conversation = [
#     {
#         "ids": ["0"],
#         "user_id": "10",
#         "message_text": "olá, como vao?",
#         "reply_id": "None",
#     },
#     {"ids": ["1"], "user_id": "11", "message_text": "Olá amigo", "reply_id": "0"},
#     {"ids": ["2"], "user_id": "12", "message_text": "Olá a todos", "reply_id": "None"},
#     {"ids": ["3"], "user_id": "11", "message_text": "Como vão", "reply_id": "None"},
#     {
#         "ids": ["4", "5", "6"],
#         "user_id": "13",
#         "message_text": "tá calado. ola. xiu",
#         "reply_id": "2",
#     },
#     {"ids": ["7"], "user_id": "13", "message_text": "aaaaa", "reply_id": "None"},
#     {"ids": ["8"], "user_id": "20", "message_text": "olaaaaa", "reply_id": "5"},
# ]


def test_read_conversation():
    assert type(read_ccsv("tests/a.csv")) == type(pd.DataFrame())

    assert len(read_ccsv("tests/a.csv").columns) >= 3
    # assert len(read_ccsv("tests/b.csv", ";")) == len(conversation)


def test_read_conversation_errors():
    with pytest.raises(ValueError):
        read_ccsv(10)
    with pytest.raises(FileNotFoundError):
        read_ccsv("file")
    with pytest.raises(TypeError):
        read_ccsv("file.csv", 1)
    with pytest.raises(TypeError):
        read_ccsv("file.csv", not_valid=",,")
    with pytest.raises(ValueError):
        read_ccsv("tests/conv_missing_id.csv")
    with pytest.raises(ValueError):
        read_ccsv("tests/conv_missing_target_and_reply.csv")


def test_parshift_annotation1():
    df_read_ccsv = read_ccsv("tests/a.csv").reset_index(drop=False)
    parshift_annotation_df = pd.read_csv("tests/df.csv", index_col=False).fillna("")

    assert type(annotate(df_read_ccsv)) == type(parshift_annotation_df)

    assert len(annotate(df_read_ccsv)) == len(parshift_annotation_df)

    # print(parshift_annotation_df["pshift"].values)
    print(parshift_annotation_df)
    # print(annotate(df_read_ccsv)["pshift"].values)
    assert (
        parshift_annotation_df["pshift"].values
        == annotate(df_read_ccsv)["pshift"].values
    ).all()


def test_parshift_annotation2():
    df_read_ccsv = read_ccsv("tests/b.csv", sep=";", quotechar='"').reset_index(
        drop=False
    )
    parshift_annotation_df = pd.read_csv("tests/df.csv", index_col=False).fillna("")

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
