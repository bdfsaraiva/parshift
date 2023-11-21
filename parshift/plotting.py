# Copyright (c) 2022-2023 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE or copy
# at http://opensource.org/licenses/MIT)

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import squarify

from .annotation import pshift_class
from typing import Optional


def frequency_treemap(
    cond_probs_df: pd.DataFrame,
    ax: Optional[matplotlib.axes.Axes] = None,
    type: str = "Pshift",
) -> matplotlib.axes.Axes:
    """Get a matplotlib axes object displaying the conditional probabilities or frequencies.

    Arguments:
        cond_probs_df: Dataframe with information about the participation shift
            conditional probabilities. This data frame can be obtained with
            [`cond_probs()`][parshift.statistics.cond_probs]
        type: Column name to be used to plot the treemap, either `"Pshift"`
            (default) or `"Pshift_class"`.
        ax: Matplotlib axes with the treemap plot.

    Returns:
        ax: Matplotlib axes with the participation shifts probabilities or frequency.
    """

    if not isinstance(type, str):
        raise TypeError("Parameter filename must be a String")
    if type not in ["Pshift_class", "Pshift"]:
        raise ValueError(
            "Parameter type must be one of the following: `Pshift`, `Pshift_class`"
        )

    if type == "Pshift_class":
        cond_probs_df["Pshift_class"] = cond_probs_df["Pshift"].apply(pshift_class)

    gb_parshift = cond_probs_df.groupby([type])["Frequency"].sum()

    data = [
        el
        for el in list(zip(gb_parshift.values, gb_parshift.index.values))
        if el[0] != 0
    ]
    labels = [
        f"{el} \n {round( 100 * (list(zip(*data))[0][idx] / sum(list(list(zip(*data))[0]))),1)}%"
        for idx, el in enumerate(list(zip(*data))[1])
    ]

    color_dict = {
        "Turn Receiving": "#86d87c",
        "AB-BA": "#86d87c",
        "AB-B0": "#c6ecbe",
        "AB-BY": "#7cd892",
        "Turn Claiming": "#f4b461",
        "A0-X0": "#f4b461",
        "A0-XA": "#fb9948",
        "A0-XY": "#efa107",
        "Turn Usurping": "#ff4d4d",
        "AB-X0": "#ff4d4d",
        "AB-XA": "#fb7477",
        "AB-XB": "#ef3b6e",
        "AB-XY": "#ef483b",
        "Turn Continuing": "#85eff9",
        "A0-AY": "#3b61ef",
        "AB-A0": "#85eff9",
        "AB-AY": "#b9befb",
    }

    colors = [color_dict[el] for el in list(zip(*data))[1]]

    if ax is None:
        _, ax = plt.subplots()

    squarify.plot(
        list(zip(*data))[0],
        label=labels,
        pad=2,
        color=colors,
        ax=ax,
    )
    # plt.title("Participation Shifts Frequency (%)")
    plt.axis("off")
    return ax
