import pandas as pd
from parshift.annotation import _label_type
from parshift.annotation import parshift_annotation


def _frequency_table(parshift_annotation_df) -> list:
    """
    This function takes in a dataframe of ParShift annotations and returns a frequency table of ParShift codes.

    Arguments:
        parshift_annotation_df: A Pandas dataframe containing ParShift annotations

    Returns:
        A list containing a dictionary of ParShift codes and their frequencies, the total number of times a ParShift code starting with "A0" appears,
            the total number of times a Parshift code starting with "AB" appears, the total number of times a Parshift code with "A0" assuming change of
            speaker, and the total number of times a ParShift code with "AB" appears assuming change of speaker.
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
        # "A0-A0",
    ]

    dict_prob_empirical_count = {}
    count_start_A0_total = 0
    count_start_AB_total = 0
    count_not_turn_continuing_A0 = 0
    count_not_turn_continuing_AB = 0

    for code in parshift_codes:
        count = 0
        for index, row in parshift_annotation_df.iterrows():
            if row["label_code"] == code:
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


def conditional_probabilities(parshift_annotation_df: pd.DataFrame) -> pd.DataFrame:

    """
    Calculate the conditional probabilities for a given `parshift_annotation` DataFrame based on Gibson's framework.

    Arguments:
        parshift_annotation_df: A DataFrame with `parshift` annotations. See [here](https://bdfsaraiva.github.io/parshift/api/annotation.html#parshift.annotation.parshift_annotation)

    Returns:
        A DataFrame containing the frequency, probability and conditional probabilities (two) for each parshift code.
            This DataFrame is divided into two 'subgroups', those beginning with an undirected remark (A0-) and
            those beginning with a directed one (AB-).
            CP (Conditional Probability) -> Frequency divided by total occurrences in each subgroup.
            CPeTC (Conditional Probability excluding Turn Continuing type) -> Frequency divided by total occurrences
            in each subgroup, assuming change of speaker.
    """

    if not isinstance(parshift_annotation_df, pd.DataFrame):
        raise TypeError("Parameter parshift_annotation_df must be a Dataframe")

    frequency_table_and_counts = _frequency_table(parshift_annotation_df)
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

    cond_prob = pd.DataFrame.from_dict(cond_prob, orient="index")
    freq = pd.DataFrame.from_dict(freq_table, orient="index", columns=["Frequency"])
    freq["Probability"] = round(freq["Frequency"] / freq["Frequency"].sum(), 2)

    result = (
        pd.concat([freq, cond_prob], axis=1)
        .reset_index()
        .rename(columns={"index": "parshift_code"})
    )
    order = {
        "AB-BA": 5,
        "AB-B0": 6,
        "AB-BY": 11,
        "A0-X0": 1,
        "A0-XA": 0,
        "A0-XY": 2,
        "AB-X0": 7,
        "AB-XA": 8,
        "AB-XB": 9,
        "AB-XY": 12,
        "A0-AY": 3,
        "AB-A0": 10,
        "AB-AY": 12,
        # "A0-A0": 4,
    }

    result["parshift"] = result["parshift_code"].map(_label_type)
    result = result.sort_values(
        by=["parshift_code"], key=lambda x: x.map(order)
    ).reset_index(drop=True)

    return result
