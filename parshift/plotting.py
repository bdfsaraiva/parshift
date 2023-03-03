import squarify
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import pandas as pd
from .annotation import pshift_type


def frequency_treemap(
    conditional_probabilities_df: pd.DataFrame,
    ax: matplotlib.axes.Axes = None,
    column_name: str = "pshift",
) -> matplotlib.axes.Axes:
    """Function used to return a matplotlib object which contains the conditional probabilities frequencies based in Gibson's paper.

    Arguments:
        conditional_probabilities_df: Dataframe object that contain the whole information about the Participation Shift conditional probabilities.
        column_name: Column name to be used to plot the treemap. Must be one of the following: `pshift`, `pshift_type`.
        ax: Matplotlib axes to plot the treemap.

    Returns:
        ax: Matplotlib axes with the Participation Shifts Frequency.
    """

    if not isinstance(column_name, str):
        raise TypeError("Parameter filename must be a String")
    if column_name not in ["pshift_type", "pshift"]:
        raise ValueError(
            "Parameter column_name must be one of the following: `pshift`, `pshift_type`"
        )

    if column_name == "pshift_type":
        conditional_probabilities_df["pshift_type"] = conditional_probabilities_df[
            "pshift"
        ].apply(pshift_type)

    gb_parshift = conditional_probabilities_df.groupby([column_name])["Frequency"].sum()

    data = [
        el
        for el in list(zip(gb_parshift.values, gb_parshift.index.values))
        if el[0] != 0
    ]
    labels = [
        f"{el} \n {round( 100 * (list(zip(*data))[0][idx] / sum(list(list(zip(*data))[0]))),1)}%"
        for idx, el in enumerate(list(zip(*data))[1])
    ]

    if ax is None:
        _, ax = plt.subplots()

    squarify.plot(
        list(zip(*data))[0],
        label=labels,
        pad=2,
        color=sns.color_palette("Spectral", len(list(zip(*data))[0])),
        ax=ax,
    )
    plt.title("Participation Shifts Frequency (%)")
    plt.axis("off")
    # plt.show()
    return ax
