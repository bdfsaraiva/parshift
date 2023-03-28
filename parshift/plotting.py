# Copyright (c) 2022-2023 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE or copy
# at http://opensource.org/licenses/MIT)

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import squarify

from .annotation import pshift_type


def frequency_treemap(
    cond_probs_df: pd.DataFrame,
    ax: matplotlib.axes.Axes = None,
    column_name: str = "pshift",
) -> matplotlib.axes.Axes:
    """Get a matplotlib axes object displaying the conditional probabilities or frequencies.

    Arguments:
        cond_probs_df: Dataframe with information about the participation shift
            conditional probabilities. This dataframe can be obtained with
            [`cond_probs()`][parshift.statistics.cond_probs]
        column_name: Column name to be used to plot the treemap, either `"pshift"`
            (default) or `"pshift_type"`.
        ax: Matplotlib axes with the treemap plot.

    Returns:
        ax: Matplotlib axes with the participation shifts probabilities or frequency.
    """

    if not isinstance(column_name, str):
        raise TypeError("Parameter filename must be a String")
    if column_name not in ["pshift_type", "pshift"]:
        raise ValueError(
            "Parameter column_name must be one of the following: `pshift`, `pshift_type`"
        )

    if column_name == "pshift_type":
        cond_probs_df["pshift_type"] = cond_probs_df["pshift"].apply(pshift_type)

    gb_parshift = cond_probs_df.groupby([column_name])["Frequency"].sum()

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

    return ax
