import csv
import pandas as pd
import re


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


def read_ccsv(
    filename: str, delimiter: str = ",", quotechar: str = '"'
) -> pd.DataFrame:
    """Function used to read a conversation file and return a list of dictionary structure.
    The dictionary keys are: `id`, `user_id`, `message_text` and one of [`reply_id`, `target_id`].

    Arguments:
        filename: Path to csv file.
        delimiter: Parameter delimiter.
        quotechar: Parameter quotechar.

    Returns:
        conversation: Pandas DataFrame.
    """

    if not isinstance(filename, str):
        raise TypeError("Parameter filename must be a String")
    if not re.search("^.*\.csv$", filename):
        raise ValueError("Parameter filename must be a CSV file")
    if not isinstance(delimiter, str):
        raise TypeError("Parameter delimiter must be a String")
    if len(delimiter) != 1:
        raise ValueError("Parameter delimiter must be one character")

    conversation = []
    with open(filename, "r", encoding="utf8") as file:
        csv_reader = csv.reader(file, delimiter=delimiter, quotechar=quotechar)
        first_line_csv = list(csv_reader)[0]

    if "'reply_id'" in first_line_csv or "'target_id'" in first_line_csv:
        conversation = pd.read_csv(
            filename, delimiter=delimiter, quotechar=quotechar, index_col="'id'"
        )
        return conversation
    else:
        raise ValueError("CSV file must contain reply_id or target_id column")


def _group_turns(conversation_df: pd.DataFrame) -> list:

    conversation_df = conversation_df.reset_index()
    if "'reply_id'" in conversation_df.columns:
        last_col = "'reply_id'"
    elif "'target_id'" in conversation_df.columns:
        last_col = "'target_id'"

    conversation = []
    turn = 0

    for index, row in conversation_df.iterrows():

        if (
            index != 0
            and conversation[turn - 1]["user_id"] == row["'user_id'"]
            and str(conversation[turn - 1][last_col[1:-1]]) == row[last_col]
        ):
            msg_join = ". ".join(
                [conversation[turn - 1]["message_text"], row["'message_text'"]]
            )
            list_id = conversation[turn - 1]["ids"] + [row["'id'"]]
            conversation[turn - 1]["ids"] = list_id
            conversation[turn - 1]["message_text"] = msg_join

        else:
            id = row["'id'"]
            user_id = row["'user_id'"]
            message_text = row["'message_text'"]
            last_col_val = row[last_col]
            turn += 1

            conversation.append(
                {
                    "ids": [id],
                    "user_id": user_id,
                    "message_text": message_text,
                    last_col[1:-1]: int(last_col_val)
                    if last_col_val != "None"
                    else None,
                }
            )

    return conversation


def _pshift_code(label):
    # label split
    a = label.split(",")[0].split("to")[0].replace(" ", "")
    b = label.split(",")[0].split("to")[1].replace(" ", "")
    c = label.split(",")[1].split("to")[0].replace(" ", "")
    d = label.split(",")[1].split("to")[1].replace(" ", "")

    # 1
    result = "A"

    # 2
    result += "0-" if b == "group" else "B-"

    # 3
    if c == a:
        result += "A"
    elif c == b:
        result += "B"
    else:
        result += "X"

    # 4
    if d == "group":
        result += "0"
    elif d == a:
        result += "A"
    elif d == b:
        result += "B"
    else:
        result += "Y"

    return result


def annotate(conversation_df: pd.DataFrame) -> pd.DataFrame:

    """Function used to return a Dataframe which contains the Participation Shift type, based in Gibson's paper.

    Arguments:
        conversation_df: Pandas DataFrame.

    Returns:
        New Dataframe with Participation Shift label and type columns added for each turn (sequence of messages from a speaker to the same addressee)
    """

    if not isinstance(conversation_df, pd.DataFrame):
        print(type(conversation_df))
        raise TypeError("Parameter conversation_df must be a Pandas DataFrame")

    conversation = _group_turns(conversation_df)

    part_1 = ""
    part_2 = ""

    if "'reply_id'" in conversation_df.columns:

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

            p1p2 = part_1 + part_2
            part_1 = part_2[1:] + ","
            label_code_v = ""

            if idx != 0:
                msg["label"] = p1p2
                label_code_v = _pshift_code(p1p2)
                msg["pshift"] = label_code_v

            annotate_df.loc[len(annotate_df.index)] = [
                str(msg["ids"]),
                str(msg["user_id"]),
                msg["message_text"],
                str(msg["reply_id"]),
                p1p2,
                label_code_v,
            ]

    elif "'target_id'" in conversation_df.columns:

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

        for idx, msg in enumerate(conversation):

            if (
                msg["target_id"] == None
                or msg["target_id"] == "None"
                or msg["target_id"] == ""
            ):
                part_2 = " " + str(msg["user_id"]) + " to group"
            else:
                msgPrev = conversation[idx - 1]
                part_2 = " " + str(msg["user_id"]) + " to " + str(msgPrev["user_id"])

            p1p2 = part_1 + part_2
            part_1 = part_2[1:] + ","

            if idx != 0:
                msg["label"] = p1p2
                label_code_v = _pshift_code(p1p2)
                msg["pshift"] = label_code_v

            annotate_df.loc[len(annotate_df.index)] = [
                str(msg["ids"]),
                str(msg["user_id"]),
                msg["message_text"],
                str(msg["target_id"]),
                (p1p2),
                (label_code_v),
            ]

    annotate_df.drop(columns=["label_desc"], inplace=True)

    return annotate_df


def pshift_type(pshift_code: str) -> str:
    """Function used to return the Participation Shift type, based in Gibson's paper.

    Arguments:
        pshift_code: Participation Shift Code (e.g A0-XA).\n

    Returns:
        Participation shift type in a given turn - one of [Turn Receiving, Turn Claiming, Turn Usurping, Turn Continuing].
    """

    if not isinstance(pshift_code, str):
        raise TypeError("Parameter pshift_code must be a String")
    if not re.search("A[B|0]-[A|B|X][A|B|X|Y|0]", pshift_code):
        raise ValueError("Parameter pshift_code must be a parshift code. eg: AB-B0")

    return _p_shift_dict[pshift_code]
