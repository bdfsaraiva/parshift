# Copyright (c) 2022-2023 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE or copy
# at http://opensource.org/licenses/MIT)

import pandas as pd

_cp_order = {
    "AB-BA": 4,
    "AB-B0": 5,
    "AB-BY": 10,
    "A0-X0": 1,
    "A0-XA": 0,
    "A0-XY": 2,
    "AB-X0": 6,
    "AB-XA": 7,
    "AB-XB": 8,
    "AB-XY": 11,
    "A0-AY": 3,
    "AB-A0": 9,
    "AB-AY": 12,
}


def _frequency_table(parshift_annotation_df) -> list:
    """
    This function takes in a dataframe of ParShift annotations and returns a frequency table of ParShift codes.

    Arguments:
        parshift_annotation_df: A Pandas dataframe containing ParShift annotations

    Returns:
        A list containing a dictionary of ParShift codes and their frequencies,
        the total number of times a ParShift code starting with "A0" appears,
        the total number of times a Parshift code starting with "AB" appears,
        the total number of times a Parshift code with "A0" assuming change of speaker,
        and the total number of times a ParShift code with "AB" appears assuming
        change of speaker.
    """

    parshift_codes = [
        "AB-BA",
        "AB-B0",
        "AB-BY",
        "A0-X0",
        "A0-XA",
        "A0-XY",
        "AB-X0",
        "AB-XA",
        "AB-XB",
        "AB-XY",
        "A0-AY",
        "AB-A0",
        "AB-AY",
    ]

    dict_prob_empirical_count = {}
    count_start_A0_total = 0
    count_start_AB_total = 0
    count_not_turn_continuing_A0 = 0
    count_not_turn_continuing_AB = 0

    for code in parshift_codes:
        count = 0
        for index, row in parshift_annotation_df.iterrows():
            if row["pshift"] == code:
                count += 1

        dict_prob_empirical_count[code] = count

        if code.split("-")[0] == "A0":
            count_start_A0_total += count
            if code not in ["A0-AY", "AB-A0", "AB-AY", "A0-A0"]:
                count_not_turn_continuing_A0 += count
        else:
            count_start_AB_total += count
            if code not in ["A0-AY", "AB-A0", "AB-AY", "A0-A0"]:
                count_not_turn_continuing_AB += count

    return [
        dict_prob_empirical_count,
        count_start_A0_total,
        count_start_AB_total,
        count_not_turn_continuing_A0,
        count_not_turn_continuing_AB,
    ]


def cond_probs(pshift_codes: pd.DataFrame) -> pd.DataFrame:
    """Determine the conditional probabilities for a sequence of participation shift codes.

    Arguments:
        pshift_codes: A sequence of participation shift code obtained with
            [`annotate()`][parshift.annotation.annotate].

    Returns:
        A dataframe containing the frequency, probability and conditional probabilities
            (two) for each parshift code. This dataframe is divided into two 'subgroups':
            (1) those beginning with an undirected remark (A0-); and, (2) those beginning
            with a directed one (AB-). The `CP` (conditional probability) column contains
            the frequency divided by total occurrences in each subgroup, while the `CPeTC`
            (Conditional Probability excluding Turn Continuing type) column contains the
            frequency divided by total occurrences in each subgroup, assuming change of
            speaker.
    """

    if not isinstance(pshift_codes, pd.DataFrame):
        raise TypeError("Parameter parshift_annotation_df must be a Dataframe")

    frequency_table_and_counts = _frequency_table(pshift_codes)
    freq_table = frequency_table_and_counts[0]

    cond_prob = {}
    for key in freq_table:
        if key.split("-")[0] == "A0":
            if key not in ["A0-AY", "AB-A0", "AB-AY", "A0-A0"]:
                cond_prob[key] = {
                    "CP": round(freq_table[key] / frequency_table_and_counts[1], 2),
                    "CPeTC": round(freq_table[key] / frequency_table_and_counts[3], 2),
                }
            else:
                cond_prob[key] = {
                    "CP": round(freq_table[key] / frequency_table_and_counts[1], 2),
                    "CPeTC": "",
                }
        else:
            if key not in ["A0-AY", "AB-A0", "AB-AY", "A0-A0"]:
                cond_prob[key] = {
                    "CP": round(freq_table[key] / frequency_table_and_counts[2], 2),
                    "CPeTC": round(freq_table[key] / frequency_table_and_counts[4], 2),
                }
            else:
                cond_prob[key] = {
                    "CP": round(freq_table[key] / frequency_table_and_counts[2], 2),
                    "CPeTC": "",
                }

    cond_prob_df = pd.DataFrame.from_dict(cond_prob, orient="index")
    freq = pd.DataFrame.from_dict(freq_table, orient="index", columns=["Frequency"])
    freq["Probability"] = round(freq["Frequency"] / freq["Frequency"].sum(), 2)

    result = (
        pd.concat([freq, cond_prob_df], axis=1)
        .reset_index()
        .rename(columns={"index": "pshift"})
    )

    result = result.sort_values(
        by=["pshift"], key=lambda x: x.map(_cp_order)
    ).reset_index(drop=True)

    result_ordered = result.iloc[:, [0, 1, 2, 3, 4]]
    return result_ordered
