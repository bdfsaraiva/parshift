from parshift import annotation
import pytest
import pandas as pd


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
    assert type(annotation.read_ccsv("tests/a.csv")) == type(pd.DataFrame())

    assert len(annotation.read_ccsv("tests/a.csv").columns) >= 3
    # assert len(annotation.read_ccsv("tests/b.csv", ";")) == len(conversation)


def test_read_conversation_errors():
    with pytest.raises(TypeError):
        annotation.read_ccsv(10)
    with pytest.raises(ValueError):
        annotation.read_ccsv("file")
    with pytest.raises(TypeError):
        annotation.read_ccsv("file.csv", 1)
    with pytest.raises(ValueError):
        annotation.read_ccsv("file.csv", ",,")


def test_parshift_annotation():
    df_read_ccsv = annotation.read_ccsv("tests/a.csv").reset_index(drop=False)
    parshift_annotation_df = pd.read_csv("tests/df.csv", index_col=False).fillna("")

    assert type(annotation.annotate(df_read_ccsv)) == type(parshift_annotation_df)

    assert len(annotation.annotate(df_read_ccsv)) == len(parshift_annotation_df)

    # print(parshift_annotation_df["pshift"].values)
    print(parshift_annotation_df)
    # print(annotation.annotate(df_read_ccsv)["pshift"].values)
    assert (
        parshift_annotation_df["pshift"].values
        == annotation.annotate(df_read_ccsv)["pshift"].values
    ).all()


def test_pshift_type_values():
    assert annotation.pshift_type("AB-BA") == "Turn Receiving"


def test_pshift_type_errors():
    with pytest.raises(TypeError):
        annotation.pshift_type(1)
    with pytest.raises(ValueError):
        annotation.pshift_type("hi")
