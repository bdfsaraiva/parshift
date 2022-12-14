import csv
import pandas as pd
import re


def _read_conversation(filename: str, delimiter: str = ",") -> list:
    """Function used to read a conversation file and return a list of dictionary structure.
    The dictionary keys are: `id`, `user_id`, `message_text` and `reply_id`.

    Arguments:
        filename: Path file name.
        delimiter: Parameter delimiter.

    Returns:
        conversation: List of dictionary structure.
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
        csv_reader = csv.reader(file, delimiter=delimiter)

        turn = 0
        for idx, csv_line in enumerate(csv_reader):
            if idx == 0:
                continue  # header

            if (
                idx != 1
                and conversation[turn - 1]["user_id"] == csv_line[1]
                and conversation[turn - 1]["reply_id"] == csv_line[3]
            ):
                msg_join = f"{conversation[turn-1]['message_text']}. {csv_line[2]}"
                list_id = conversation[turn - 1]["id"] + [csv_line[0]]
                conversation[turn - 1]["id"] = list_id
                conversation[turn - 1]["message_text"] = msg_join

            else:
                id = csv_line[0]
                user_id = csv_line[1]
                message_text = csv_line[2]
                reply_id = csv_line[3]
                turn += 1

                conversation.append(
                    {
                        "id": [id],
                        "user_id": user_id,
                        "message_text": message_text,
                        "reply_id": reply_id,
                    }
                )

    return conversation


def parshift_annotation(filename: str, delimiter: str = ",") -> pd.DataFrame:

    """Function used to return a Dataframe which contains the Participation Shift type, based in Gibson's paper.

    Arguments:
        filename: Path file name.
        delimiter: Parameter delimiter.

    Returns:
        New Dataframe with Participation Shift label and type columns added for each turn (sequence of messages from a speaker to the same addressee).
    """

    # # TODO: Adicionar o caso em que o usar j?? tem uma lista de sentences.
    # if not filename and not conversation_list:
    #     raise AssertionError("One of the parameters 'filename' or 'conversation_list' must be not None")
    # elif not conversation_list:
    #     conversation = _read_conversation(filename, delimiter)
    # else:
    #     conversation = conversation_list
    # # TODO: fim

    conversation = _read_conversation(filename, delimiter)

    df = pd.DataFrame(
        {
            "id": [],
            "user_id": [],
            "message_text": [],
            "reply_id": [],
            "label_desc": [],
            "label_code": [],
            "label_value": [],
        }
    )

    part_1 = ""
    part_2 = ""
    label_code_v = ""
    label_type_v = ""

    for idx, msg in enumerate(conversation):

        if (
            msg["reply_id"] == None
            or msg["reply_id"] == "None"
            or msg["reply_id"] == ""
        ):
            part_2 = " " + str(msg["user_id"]) + " to group"
        else:
            for msgPrev in conversation:
                if msg["reply_id"] in msgPrev["id"]:
                    if (
                        msgPrev["reply_id"] == None
                        or msgPrev["reply_id"] == "None"
                        or msgPrev["reply_id"] == ""
                    ):
                        part_1 = str(msgPrev["user_id"]) + " to group,"
                    else:  # reply - reply
                        for msgPrev2 in conversation:
                            if msgPrev["reply_id"] in msgPrev2["id"]:
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
        # print(part_1 + part_2)
        part_1 = part_2[1:] + ","

        def _label_code(label):
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

        if idx != 0:
            msg["label"] = p1p2
            label_code_v = _label_code(p1p2)
            msg["label_code"] = label_code_v
            label_type_v = _label_type(label_code_v)
            msg["label_type"] = label_type_v

        df.loc[len(df.index)] = [
            str(msg["id"]),
            str(msg["user_id"]),
            msg["message_text"],
            str(msg["reply_id"]),
            (p1p2),
            (label_code_v),
            (label_type_v),
        ]
        # print('-'*20)
    return df


def _label_type(label_code: str) -> str:
    """Function used to return the Participation Shift type, based in Gibson's paper.

    Arguments:
        label_code: Participation Shift Code (e.g A0-XA).\n

    Returns:
        Participation shift type in a given turn - one of [Turn Receiving, Turn Claiming, Turn Usurping, Turn Continuing].
    """

    if not isinstance(label_code, str):
        raise TypeError("Parameter label_code must be a String")
    if not re.search("A[B|0]-[A|B|X][A|B|X|Y|0]", label_code):
        raise ValueError("Parameter label_code must be a parshift code. eg: AB-B0")

    p_shift = {
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
        # "A0-A0": "Turn Continuing",
    }
    return p_shift[label_code]
