# Copyright (c) 2022-2023 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE or copy
# at http://opensource.org/licenses/MIT)

from __future__ import annotations
from pandas._typing import FilePath, ReadCsvBuffer
from typing import Any

from .annotation import read_ccsv, annotate
from .statistics import cond_probs


def load_and_process(
    filepath_or_buffer: FilePath | ReadCsvBuffer[bytes] | ReadCsvBuffer[str],
    **kwargs: Any,
):
    """Read a conversation file in CSV format, validate it,
    get Gibson's participation shift codes from turns in a conversation,
    determine the conditional probabilities for a sequence of participation shift codes
    and return a dict with parshift annotations and conditional probabilities.

    The conversation file should have the following columns:

    - `id`: ID of the message (int)
    - `user_id`: ID of the user sending the message (str)
    - `message_text`: The message itself (string)
    - `reply_id` or `target_id`: The reply ID or the target ID (int)

    Arguments:
        filepath_or_buffer: Any valid string path to CSV file, as accepted by
            Pandas [`read_csv()`][pandas.read_csv] function.
        **kwargs: Keyword parameters passed to Pandas
            [`read_csv()`][pandas.read_csv] function.

    Returns:
        A dict with two keys:
            - "annot" where the value is dataframe equal as returned by [`annotate()`][parshift.annotation.annotate].
            - "stats" where the value is dataframe equal as returned by [`cond_probs()`][parshift.statistics.cond_probs].
    """

    df_annotate = annotate(read_ccsv(filepath_or_buffer, **kwargs))
    df_stats = cond_probs(df_annotate)
    return {
        "annot": df_annotate,
        "stats": df_stats,
    }
