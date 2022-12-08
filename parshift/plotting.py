import squarify
import matplotlib.pyplot as plt
import pandas as pd
from parshift import conditional_probabilities


def frequency_treemap(conditional_probabilities_df):
    """
    Function used to return a matplotlib object which contains the conditional probabilities frequencies based in Gibson's paper.\n
    --- **Arguments**\n
    `conditional_probabilities_df` (Dataframe): Dataframe object that contain the whole
    information about the Participation Shift conditional probabilities.\n
    --- **Returns**\n
    `df` (matplotlib): Matplotlib object with the Participation Shifts Frequency (%).
    """
    gb_parshift = conditional_probabilities_df.groupby(["parshift"])["Frequency"].sum()

    data = [
        el
        for el in list(zip(gb_parshift.values, gb_parshift.index.values))
        if el[0] != 0
    ]
    labels = [
        f"{el} \n {round( 100 * (list(zip(*data))[0][idx] / sum(list(list(zip(*data))[0]))),1)}%"
        for idx, el in enumerate(list(zip(*data))[1])
    ]

    f = plt.figure()
    squarify.plot(list(zip(*data))[0], label=labels, pad=2)
    plt.title("Participation Shifts Frequency (%)")
    plt.axis("off")
    # plt.show()
    return f
