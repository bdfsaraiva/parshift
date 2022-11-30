import pandas as pd
import annotation  # import pshift_annotation, label_type
import squarify
import matplotlib.pyplot as plt


def frequency_table(parshif_annotation_df):

    # df = annotation.parshift_annotation(file_name)

    pshift_codes = [
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
        "A0-A0",
    ]

    dict_prob_empirical_count = {}
    count_start_A0_total = 0
    count_start_AB_total = 0
    count_not_turn_continuing_A0 = 0
    count_not_turn_continuing_AB = 0

    for code in pshift_codes:
        count = 0
        for index, row in parshif_annotation_df.iterrows():
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


def conditional_probabilities(parshif_annotation_df):

    frequency_table_and_counts = frequency_table(parshif_annotation_df)
    freq_table = frequency_table_and_counts[0]

    cond_prob = {}
    for key in freq_table:
        if key.split("-")[0] == "A0":
            if key not in ["A0-AY", "AB-A0", "AB-AY", "A0-A0"]:
                cond_prob[key] = {
                    "CP General": round(freq_table[key] / frequency_table_and_counts[1], 2),
                    "CP excludes turn continuing": round(
                        freq_table[key] / frequency_table_and_counts[3], 2
                    ),
                }
            else:
                cond_prob[key] = {
                    "CP General": round(freq_table[key] / frequency_table_and_counts[1], 2),
                    "CP excludes turn continuing": "",
                }
        else:
            if key not in ["A0-AY", "AB-A0", "AB-AY", "A0-A0"]:
                cond_prob[key] = {
                    "CP General": round(freq_table[key] / frequency_table_and_counts[2], 2),
                    "CP excludes turn continuing": round(
                        freq_table[key] / frequency_table_and_counts[4], 2
                    ),
                }
            else:
                cond_prob[key] = {
                    "CP General": round(freq_table[key] / frequency_table_and_counts[2], 2),
                    "CP excludes turn continuing": "",
                }

    cond_prob = pd.DataFrame.from_dict(cond_prob, orient="index")
    freq = pd.DataFrame.from_dict(freq_table, orient="index", columns=["Frequency"])
    freq["Probability"] = round(freq["Frequency"] / freq["Frequency"].sum(), 2)

    result = (
        pd.concat([freq, cond_prob], axis=1).reset_index().rename(columns={"index": "pshift_code"})
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
        "A0-A0": 4,
    }

    result["p_shift"] = result["pshift_code"].map(annotation.label_type)
    result = result.sort_values(by=["pshift_code"], key=lambda x: x.map(order)).reset_index(
        drop=True
    )

    return result


def frequency_treemap(df):
    gb_pshift = df.groupby(["p_shift"]).sum()

    data = [
        el
        for el in list(zip(gb_pshift["Frequency"].values, gb_pshift["Frequency"].index.values))
        if el[0] != 0
    ]
    labels = [
        f"{el} \n {round( 100 * (list(zip(*data))[0][idx] / sum(list(list(zip(*data))[0]))),1)}%"
        for idx, el in enumerate(list(zip(*data))[1])
    ]

    squarify.plot(list(zip(*data))[0], label=labels, pad=2)

    plt.title("Participation Shifts Frequency (%)")
    plt.axis("off")
    # plt.show()
    return plt


print(conditional_probabilities(annotation.parshift_annotation('py-Participation-Shifts/tests/a.csv')))