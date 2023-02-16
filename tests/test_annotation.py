from parshift import annotation
import pytest
import pandas as pd


conversation = [
    {
        "ids": ["0"],
        "user_id": "10",
        "message_text": "olá, como vao?",
        "reply_id": "None",
    },
    {"ids": ["1"], "user_id": "11", "message_text": "Olá amigo", "reply_id": "0"},
    {"ids": ["2"], "user_id": "12", "message_text": "Olá a todos", "reply_id": "None"},
    {"ids": ["3"], "user_id": "11", "message_text": "Como vão", "reply_id": "None"},
    {
        "ids": ["4", "5", "6"],
        "user_id": "13",
        "message_text": "tá calado. ola. xiu",
        "reply_id": "2",
    },
    {"ids": ["7"], "user_id": "13", "message_text": "aaaaa", "reply_id": "None"},
    {"ids": ["8"], "user_id": "20", "message_text": "olaaaaa", "reply_id": "5"},
]


def test_read_conversation():
    assert type(annotation._read_conversation("tests/a.csv")) == type(conversation)

    assert len(annotation._read_conversation("tests/a.csv")) == len(conversation)
    assert len(annotation._read_conversation("tests/b.csv", ";")) == len(conversation)

    assert annotation._read_conversation("tests/a.csv") == conversation
    assert annotation._read_conversation("tests/b.csv", ";") == conversation


def test_read_conversation_errors():
    with pytest.raises(TypeError):
        annotation._read_conversation(10)
    with pytest.raises(ValueError):
        annotation._read_conversation("file")
    with pytest.raises(TypeError):
        annotation._read_conversation("file.csv", 1)
    with pytest.raises(ValueError):
        annotation._read_conversation("file.csv", ",,")


def test_parshift_annotation():
    assert type(annotation.parshift_annotation("tests/a.csv")) == type(pd.DataFrame())

    parshift_annotation_df = pd.read_csv("tests/df.csv").fillna("")
    assert len(annotation.parshift_annotation("tests/a.csv")) == len(
        parshift_annotation_df
    )

    assert (
        parshift_annotation_df["parshift_code"].values
        == annotation.parshift_annotation("tests/a.csv")["parshift_code"].values
    ).all()


def test_label_type_values():
    assert annotation._label_type("AB-BA") == "Turn Receiving"


def test_label_type_errors():
    with pytest.raises(TypeError):
        annotation._label_type(1)
    with pytest.raises(ValueError):
        annotation._label_type("hi")
