# Copyright (c) 2022-2026 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE or copy
# at http://opensource.org/licenses/MIT)

from __future__ import annotations

import re
import warnings
from typing import TYPE_CHECKING, Any, Dict, List, Tuple

import numpy as np
import pandas as pd

if TYPE_CHECKING:
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
    "utterance_id": np.int64,
    "speaker_id": str,
    "utterance": str,
    "reply_to_id": object,
    "target_id": object,
}


def read_ccsv(
    filepath_or_buffer: FilePath | ReadCsvBuffer[bytes] | ReadCsvBuffer[str],
    **kwargs: Any,
) -> pd.DataFrame:
    """Read a conversation file in CSV format, validate it and return a data frame.

    The conversation file should have the following columns:

    - `utterance_id`: ID of the message (int)
    - `speaker_id`: ID of the user sending the message (str)
    - `utterance`: The message itself (string)
    - `reply_to_id` or `target_id`: The reply ID or the target ID (int)

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
    if (
        len(missing) == 1
        and "reply_to_id" not in missing
        and "target_id" not in missing
    ):
        # If only one column missing, it can't be other than `reply_to_id` or `target_id`
        raise ValueError(f"CSV file is missing the `{missing.pop()}` column")
    elif len(missing) > 1:
        # If more than one column missing, we have a problem
        raise ValueError(f"CSV file is missing the `{'`, `'.join(missing)}` columns")

    # Change Nan values to empty strings in the `reply_to_id` or `target_id` column
    if "reply_to_id" in conversation.columns:
        conversation["reply_to_id"] = conversation["reply_to_id"].fillna("")
    else:
        conversation["target_id"] = conversation["target_id"].fillna("")

    return conversation


def conv2turns(conv_df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Take a conversation data frame and group it into conversation turns.

    A turn is a group of messages sent by the same user and addressed to the
    same target.

    Arguments:
        conv_df: The conversation from where to obtain the conversation turns.

    Returns:
        A list of dictionaries, each representing a conversation turn.
    """

    conv_df = conv_df.reset_index()
    if "reply_to_id" in conv_df.columns:
        last_col = "reply_to_id"
    elif "target_id" in conv_df.columns:
        last_col = "target_id"

    conversation: List[Dict[str, Any]] = []
    turn = 0

    for index, row in conv_df.iterrows():
        # If the row being looped has the same "speaker_id" and the "last_col" value,
        # then merge the message text and message utterance_ids into the previous turn.

        if row[last_col] == "" or row[last_col] == "None":
            row[last_col] = None
        row[last_col] = int(float(row[last_col])) if row[last_col] != None else None

        if (
            index != 0
            and conversation[turn - 1]["speaker_id"] == row["speaker_id"]
            and conversation[turn - 1][last_col] == row[last_col]
        ):
            msg_join = ". ".join(
                [conversation[turn - 1]["utterance"], str(row["utterance"])]
            )
            list_id = conversation[turn - 1]["utterance_ids"] + [row["utterance_id"]]
            conversation[turn - 1]["utterance_ids"] = list_id
            conversation[turn - 1]["utterance"] = msg_join

        # Otherwise, create a new dictionary representing a new turn
        else:
            id = row["utterance_id"]
            speaker_id = row["speaker_id"]
            utterance = row["utterance"]
            last_col_val = row[last_col]

            conversation.append(
                {
                    "utterance_ids": [id],
                    "speaker_id": speaker_id,
                    "utterance": utterance,
                    last_col: (
                        last_col_val
                        if last_col_val != ""
                        and last_col_val != None
                        and last_col_val != "None"
                        else None
                    ),
                }
            )

            # Increment the turn counter
            turn += 1

    return conversation


def _speaker_key(speaker_id: Any) -> str:
    # Speaker IDs are opaque: they are only compared with each other, and leading
    # or trailing spaces do not distinguish speakers
    return str(speaker_id).strip()


def _pshift_code(prev: Tuple[str, str | None], cur: Tuple[str, str | None]) -> str:
    # Each turn is a (speaker, addressee) pair, where an addressee equal to `None`
    # means the turn is addressed to the group
    a, b = prev
    c, d = cur

    # Part 1 - always starts with A
    result = "A"

    # Parte 2 - "0" if the target is the group, "B" otherwise
    result += "0-" if b is None else "B-"

    # Part 3 - "A" if the speaker is the same, "B" if the speaker is the previous target,
    # "X" otherwise
    if c == a:
        result += "A"
    elif b is not None and c == b:
        result += "B"
    else:
        result += "X"

    # Part 4 - "0" if the current target is the group, "A" if the current target is previous
    #  speaker, "B" if the target is the previous target, "Y" otherwise
    if d is None:
        result += "0"
    elif d == a:
        result += "A"
    elif b is not None and d == b:
        result += "B"
    else:
        result += "Y"

    return result


def annotate(conv_df: pd.DataFrame) -> pd.DataFrame:
    """Get Gibson's participation shift codes from turns in a conversation.

    Sequences of messages from a speaker to the same addressee are considered to
    be in the same turn, and therefore will be assigned a single participation
    shift code. In conversations with the `reply_to_id` column, the addressee of
    a reply is the speaker of the replied utterance.

    Only the 13 participation shifts defined by Gibson are assigned. For this
    purpose, the following turns are considered as addressed to the group, and
    a warning is issued:

    - turns addressed to their own speaker (e.g., a speaker replying to
      themselves);
    - in conversations with the `reply_to_id` column, turns replying to an
      utterance which is not in a previous turn (e.g., an utterance outside
      the data).

    Arguments:
        conv_df: The conversation from where to obtain the participation shift codes.

    Returns:
        A data frame with the participation shift codes for each turn.
    """

    if not isinstance(conv_df, pd.DataFrame):
        raise TypeError("Parameter conv_df must be a Pandas DataFrame")

    conversation = conv2turns(conv_df)

    if "reply_to_id" in conv_df.columns:
        last_col = "reply_to_id"
    elif "target_id" in conv_df.columns:
        last_col = "target_id"

    columns = ["utterance_ids", "speaker_id", "utterance", last_col, "pshift"]

    # turns of the conversation (as given by `conv2turns()`, merged by addressee)
    # and their participation shift codes
    turns: List[Dict[str, Any]] = []
    pshifts: List[str] = []

    # (speaker, addressee) of each turn, where addressee is `None` for the group
    parts: List[Tuple[str, str | None]] = []

    # turn (index) of each utterance ID found so far
    turn_of_utterance: Dict[Any, int] = {}

    # number of turns replying to an utterance not in a previous turn, and of
    # turns addressed to their own speaker
    unknown_replies = 0
    self_addressed = 0

    for msg in conversation:
        speaker = _speaker_key(msg["speaker_id"])

        # index of the turn this turn replies to, if any
        replied: int | None = None

        if msg[last_col] is None:
            # if msg has no target, it is directed to the group
            addressee = None
        elif last_col == "reply_to_id":
            # if msg is a reply, it is directed to the speaker of the replied turn
            replied = turn_of_utterance.get(msg[last_col])
            if replied is None:
                unknown_replies += 1
                addressee = None
            else:
                addressee = parts[replied][0]
        else:
            # if msg has a target, it is directed to it
            addressee = _speaker_key(msg[last_col])

        # a speaker does not address themselves: such a turn is directed to the group
        if addressee == speaker:
            self_addressed += 1
            addressee = None
            replied = None

        current = (speaker, addressee)

        if parts and parts[-1] == current:
            # same speaker and addressee as the previous turn: merge them
            turn = len(turns) - 1
            turns[turn]["utterance_ids"] = (
                turns[turn]["utterance_ids"] + msg["utterance_ids"]
            )
            turns[turn]["utterance"] = ". ".join(
                [str(turns[turn]["utterance"]), str(msg["utterance"])]
            )
        else:
            # we cannot calculate the pshift for the first turn
            pshift_label = ""
            if parts:
                # a reply is compared with the replied turn, otherwise the
                # previous turn is used
                previous = parts[replied] if replied is not None else parts[-1]
                pshift_label = _pshift_code(previous, current)

            turn = len(turns)
            turns.append(msg)
            parts.append(current)
            pshifts.append(pshift_label)

        for utterance_id in msg["utterance_ids"]:
            turn_of_utterance[utterance_id] = turn

    if unknown_replies > 0:
        warnings.warn(
            f"{unknown_replies} turn(s) reply to an utterance which is not in a "
            "previous turn, and were considered as addressed to the group",
            UserWarning,
            stacklevel=2,
        )

    if self_addressed > 0:
        warnings.warn(
            f"{self_addressed} turn(s) are addressed to their own speaker (e.g., a "
            "speaker replying to themselves), and were considered as addressed "
            "to the group",
            UserWarning,
            stacklevel=2,
        )

    rows = [
        [
            str(msg["utterance_ids"]),
            str(msg["speaker_id"]),
            msg["utterance"],
            str(msg[last_col]),
            pshift_label,
        ]
        for msg, pshift_label in zip(turns, pshifts)
    ]

    if rows:
        return pd.DataFrame(rows, columns=columns)

    # Keep the column types of a data frame built from empty columns
    return pd.DataFrame({col: [] for col in columns})


def pshift_class(pshift: str) -> str:
    """Returns the participation shift class given a participation shift code.

    Arguments:
        pshift: Participation shift code (e.g., `A0-XA`).

    Returns:
        Participation shift class of the given participation shift code (either
            "Turn Receiving", "Turn Claiming", "Turn Usurping" or "Turn Continuing").
    """

    if not isinstance(pshift, str):
        raise TypeError("Parameter pshift_code must be a String")
    if not re.search("A[B|0]-[A|B|X][A|B|X|Y|0]", pshift):
        raise ValueError("Parameter pshift_code must be a parshift code. eg: AB-B0")

    return _p_shift_dict[pshift]
