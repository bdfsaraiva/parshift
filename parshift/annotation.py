# Copyright (c) 2022-2023 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE or copy
# at http://opensource.org/licenses/MIT)

from __future__ import annotations

import re
from typing import Any, Dict, List

import numpy as np
import pandas as pd
from pandas._typing import FilePath, ReadCsvBuffer

# Participation shift types
_p_shift_dict = {
    "AB-BA": "Turn Receiving",
    "AB-B0": "Turn Receiving",
    "AB-BY": "Turn Receiving",
    "A0-X0": "Turn Claiming",
    "A0-XA": "Turn Claiming",
    "A0-XY": "Turn Claiming",
    "AB-X0": "Turn Usurping",
    "AB-XA": "Turn Usurping",
    "AB-XB": "Turn Usurping",
    "AB-XY": "Turn Usurping",
    "A0-AY": "Turn Continuing",
    "AB-A0": "Turn Continuing",
    "AB-AY": "Turn Continuing",
}

# Expected column types
_p_shift_cols = {
    "id": np.int64,
    "user_id": np.int64,
    "message_text": str,
    "reply_id": object,
    "target_id": object,
}


def read_ccsv(
    filepath_or_buffer: FilePath | ReadCsvBuffer[bytes] | ReadCsvBuffer[str],
    **kwargs: Any,
) -> pd.DataFrame:
    """Read a conversation file in CSV format, validate it and return a dataframe.

    The conversation file should have the following columns:

    - `id`: ID of the message (int)
    - `user_id`: ID of the user sending the message (int)
    - `message_text`: The message itself (string)
    - `reply_id` or `target_id`: The reply ID or the target ID (int)

    Arguments:
        filepath_or_buffer: Any valid string path to CSV file, as accepted by
            Pandas [`read_csv()`][pandas.read_csv] function.
        **kwargs: Keyword parameters passed to Pandas
            [`read_csv()`][pandas.read_csv] function.

    Returns:
        A Pandas [`DataFrame`][pandas.DataFrame] containing the validated
            conversation.
    """

    # Read the conversation file
    conversation: pd.DataFrame = pd.read_csv(filepath_or_buffer, dtype=_p_shift_cols, **kwargs)  # type: ignore

    # Obtain potentially missing columns
    missing = _p_shift_cols.keys() - conversation.columns

    # Check if we have missing columns
    if len(missing) == 1 and "reply_id" not in missing and "target_id" not in missing:
        # If only one column missing, it can't be other than `reply_id` or `target_id`
        raise ValueError(f"CSV file is missing the `{missing.pop()}` column")
    elif len(missing) > 1:
        # If more than one column missing, we have a problem
        raise ValueError(f"CSV file is missing the `{'`, `'.join(missing)}` columns")

    return conversation


def conv2turns(conv_df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Take a conversation dataframe and group it into conversation turns.

    A turn is a group of messages sent by the same user and addressed to the
    same target.

    Arguments:
        conv_df: The conversation from where to obtain the conversation turns.

    Returns:
        A list of dictionaries, each representing a conversation turn.
    """

    conv_df = conv_df.reset_index()
    if "reply_id" in conv_df.columns:
        last_col = "reply_id"
    elif "target_id" in conv_df.columns:
        last_col = "target_id"

    conversation: List[Dict[str, Any]] = []
    turn = 0

    for index, row in conv_df.iterrows():
        # If the row being looped has the same "user_id" and the "last_col" value,
        # then merge the message text and message IDs into the previous turn.
        if (
            index != 0
            and conversation[turn - 1]["user_id"] == row["user_id"]
            and str(conversation[turn - 1][last_col]) == row[last_col]
        ):
            msg_join = ". ".join(
                [conversation[turn - 1]["message_text"], row["message_text"]]
            )
            list_id = conversation[turn - 1]["ids"] + [row["id"]]
            conversation[turn - 1]["ids"] = list_id
            conversation[turn - 1]["message_text"] = msg_join

        # Otherwise, create a new dictionary representing a new turn
        else:
            id = row["id"]
            user_id = row["user_id"]
            message_text = row["message_text"]
            last_col_val = row[last_col]

            conversation.append(
                {
                    "ids": [id],
                    "user_id": user_id,
                    "message_text": message_text,
                    last_col: int(last_col_val) if last_col_val != "None" else None,
                }
            )

            # Increment the turn counter
            turn += 1

    return conversation


def _pshift_code(label: str) -> str:

    # split the label into 4 parts
    a = label.split(",")[0].split("to")[0].replace(" ", "")
    b = label.split(",")[0].split("to")[1].replace(" ", "")
    c = label.split(",")[1].split("to")[0].replace(" ", "")
    d = label.split(",")[1].split("to")[1].replace(" ", "")

    # Part 1 - always starts with A
    result = "A"

    # Parte 2 - "0" if the target is the group, "B" otherwise
    result += "0-" if b == "group" else "B-"

    # Part 3 - "A" if the speaker is the same, "B" if the speaker is the previous target,
    # "X" otherwise
    if c == a:
        result += "A"
    elif c == b:
        result += "B"
    else:
        result += "X"

    # Part 4 - "0" if the current target is the group, "A" if the current target is previous
    #  speaker, "B" if the target is the previous target, "Y" otherwise
    if d == "group":
        result += "0"
    elif d == a:
        result += "A"
    elif d == b:
        result += "B"
    else:
        result += "Y"

    return result


def annotate(conv_df: pd.DataFrame) -> pd.DataFrame:
    """Get Gibson's participation shift codes from turns in a conversation.

    Sequences of messages from a speaker to the same addressee are considered to
    be in the same turn, and therefore will be assigned a single participation
    shift code.

    Arguments:
        conv_df: The conversation from where to obtain the participation shift codes.

    Returns:
        A dataframe with the participation shift codes for each turn.
    """

    if not isinstance(conv_df, pd.DataFrame):
        raise TypeError("Parameter conv_df must be a Pandas DataFrame")

    conversation = conv2turns(conv_df)

    # part1 will take the parshift label for the previous turn
    part_1 = ""

    # part2 will take the parshift label for the current turn
    part_2 = ""

    if "reply_id" in conv_df.columns:
        annotate_df = pd.DataFrame(
            {
                "ids": [],
                "user_id": [],
                "message_text": [],
                "reply_id": [],
                "label_desc": [],
                "pshift": [],
            }
        )

        # calculate the participation shift for each turn
        for idx, msg in enumerate(conversation):
            if (
                msg["reply_id"] == None
                or msg["reply_id"] == "None"
                or msg["reply_id"] == ""
            ):
                part_2 = " " + str(msg["user_id"]) + " to group"
            else:
                for msgPrev in conversation[: idx + 1]:
                    if msg["reply_id"] in msgPrev["ids"]:
                        if (
                            msgPrev["reply_id"] == None
                            or msgPrev["reply_id"] == "None"
                            or msgPrev["reply_id"] == ""
                        ):
                            part_1 = str(msgPrev["user_id"]) + " to group,"

                        else:  # reply - reply
                            for msgPrev2 in conversation[:idx]:
                                if msgPrev["reply_id"] in msgPrev2["ids"]:
                                    part_1 = (
                                        str(msgPrev["user_id"])
                                        + " to "
                                        + str(msgPrev2["user_id"])
                                        + ","
                                    )

                        part_2 = (
                            " " + str(msg["user_id"]) + " to " + str(msgPrev["user_id"])
                        )

            # p1p2 takes the parshift label for the previous + current turn
            p1p2 = part_1 + part_2

            # part_1 takes the part_2 label for the next iteration
            part_1 = part_2[1:] + ","

            # set value to "" for first turn
            pshift_label = ""

            # we cannot calculate the pshift for the first turn
            if idx != 0:
                pshift_label = _pshift_code(p1p2)

            annotate_df.loc[len(annotate_df.index)] = [  # type: ignore
                str(msg["ids"]),
                str(msg["user_id"]),
                msg["message_text"],
                str(msg["reply_id"]),
                p1p2,
                pshift_label,
            ]

    elif "target_id" in conv_df.columns:
        annotate_df = pd.DataFrame(
            {
                "ids": [],
                "user_id": [],
                "message_text": [],
                "target_id": [],
                "label_desc": [],
                "pshift": [],
            }
        )

        # calculate the participation shift for each turn
        for idx, msg in enumerate(conversation):
            # if msg has no target, it is directed to the group
            if (
                msg["target_id"] == None
                or msg["target_id"] == "None"
                or msg["target_id"] == ""
            ):
                part_2 = " " + str(msg["user_id"]) + " to group"

            # if msg has a target, we save it
            else:
                part_2 = " " + str(msg["user_id"]) + " to " + str(msg["target_id"])

            # p1p2 takes the parshift label for the previous + current turn
            p1p2 = part_1 + part_2

            # part_1 takes the part_2 label for the next iteration
            part_1 = part_2[1:] + ","

            # set value to "" for first turn
            pshift_label = ""

            # we cannot calculate the pshift for the first turn
            if idx != 0:
                msg["label"] = p1p2
                pshift_label = _pshift_code(p1p2)
                msg["pshift"] = pshift_label

            annotate_df.loc[len(annotate_df.index)] = [  # type: ignore
                str(msg["ids"]),
                str(msg["user_id"]),
                msg["message_text"],
                str(msg["target_id"]),
                p1p2,
                pshift_label,
            ]

    annotate_df.drop(columns=["label_desc"], inplace=True)

    return annotate_df


def pshift_type(pshift_code: str) -> str:
    """Returns the participation shift type given a participation shift code.

    Arguments:
        pshift_code: Participation shift code (e.g A0-XA).

    Returns:
        Participation shift type in given the participation shift code (either
            "Turn Receiving", "Turn Claiming", "Turn Usurping" or  "Turn Continuing").
    """

    if not isinstance(pshift_code, str):
        raise TypeError("Parameter pshift_code must be a String")
    if not re.search("A[B|0]-[A|B|X][A|B|X|Y|0]", pshift_code):
        raise ValueError("Parameter pshift_code must be a parshift code. eg: AB-B0")

    return _p_shift_dict[pshift_code]
