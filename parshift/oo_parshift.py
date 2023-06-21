# Copyright (c) 2022-2023 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE or copy
# at http://opensource.org/licenses/MIT)

from __future__ import annotations

from typing import Any, List

import matplotlib.pyplot as plt
import pandas as pd
from pandas._typing import FilePath, ReadCsvBuffer

from .annotation import annotate, read_ccsv
from .plotting import frequency_treemap
from .statistics import cond_probs, propensities


class Parshift:
    def __init__(
        self,
        annotation: pd.DataFrame | None = None,
        stats: pd.DataFrame | List[pd.DataFrame] | None = None,
    ):
        """Parshift initialization"""

        self.annotation = annotation
        self.stats = stats

    def process(
        self,
        filepath_or_buffer: FilePath | ReadCsvBuffer[bytes] | ReadCsvBuffer[str],
        N: int = 1,
        **kwargs: Any,
    ):
        """Read a conversation file in CSV format, validate it,
        get Gibson's participation shift codes from turns in a conversation,
        determine the conditional probabilities for a sequence of participation shift codes
        and return a dict with parshift annotations and conditional probabilities.

        The conversation file should have the following columns:

        - `utterance_id`: ID of the message (int)
        - `speaker_id`: ID of the user sending the message (str)
        - `utterance`: The message itself (string)
        - `reply_to_id` or `target_id`: The reply ID or the target ID (int)

        Arguments:
            filepath_or_buffer: Any valid string path to CSV file, as accepted by
                Pandas [`read_csv()`][pandas.read_csv] function.
            N: Number of parts to split the conversation into. Default is 1 (all conversation).
                `N` should be between 1 and 4.
            **kwargs: Keyword parameters passed to Pandas
                [`read_csv()`][pandas.read_csv] function.

        - Parshift.annotation will be data frame equal as returned by [`annotate()`][parshift.annotation.annotate].
        - Parshift.stats will be data frame equal as returned by [`cond_probs()`][parshift.statistics.cond_probs].
        """

        df_annotate = annotate(read_ccsv(filepath_or_buffer, **kwargs))
        self.annotation = df_annotate

        if N == 1:
            self.stats = cond_probs(df_annotate)
        elif N in [2, 3, 4]:
            list_stats = []
            size = len(df_annotate)
            parts = size / N
            for i in range(N):
                # Get all the rows from parts*i to size*(i+1) with all columns
                start = int(parts * i)
                end = int(parts * (i + 1))
                list_stats.append(cond_probs(df_annotate.iloc[start:end, :]))
            self.stats = list_stats
        else:
            raise ValueError("N should be between 1 and 4.")

    def show_plot(self, type: str = "Pshift", filename: str | None = None):
        """Shows the frequency treemap plot returned by [`frequency_treemap()`][parshift.plotting.frequency_treemap]

        Arguments:
            type: Column name to be used to plot the treemap, either `"Pshift"`
                (default) or `"Pshift_class"`.
            filename: Name of the file to save the plot. Default to `None` .

        """

        if self.stats is None:
            raise ValueError(
                "Parshift.stats is None. Please run Parshift.process() first."
            )

        if not isinstance(type, str):
            raise TypeError("Parameter type must be a String")
        if type not in ["Pshift_class", "Pshift"]:
            raise ValueError(
                "Parameter type must be one of the following: `Pshift`, `Pshift_class`"
            )

        if filename != None and not isinstance(filename, str):
            raise TypeError("Parameter filename must be a String")

        if type == "Pshift":
            if isinstance(self.stats, list):
                _, ax = plt.subplots(
                    1, len(self.stats), figsize=(5 * len(self.stats), 5)
                )

                for i in range(len(self.stats)):
                    frequency_treemap(self.stats[i], type=type, ax=ax[i])
                    ax[i].axis("off")
                    ax[i].set_title(f"n {i+1}")
            else:
                ax = frequency_treemap(self.stats, type=type)

            plt.suptitle("Participation-Shift Frequencies")

        elif type == "Pshift_class":
            if isinstance(self.stats, list):
                _, ax = plt.subplots(
                    1, len(self.stats), figsize=(5 * len(self.stats), 5)
                )

                for i in range(len(self.stats)):
                    frequency_treemap(self.stats[i], type=type, ax=ax[i])
                    ax[i].axis("off")
                    ax[i].set_title(f"n {i+1}")
            else:
                ax = frequency_treemap(self.stats, type=type)

            plt.suptitle("Participation Shifts: Class Proportions")

        if filename:
            if ".png" not in filename:
                filename += ".png"
            plt.savefig(filename, dpi=300)

        plt.show()

    def show_stats(self, filename: str | None = None):
        """Prints the stats returned by [`cond_probs()`][parshift.statistics.cond_probs]
        Dataframe. If kwarg N (see [`process`][parshift.Parshift.process]) > 1, prints N data frames.

        Arguments:
            filename: Name of the file (csv) to save the stats data frame. Default to `None`.
        """

        if self.stats is None:
            raise ValueError(
                "Parshift.stats is None. Please run Parshift.process() first."
            )

        if isinstance(self.stats, list):
            for i in range(len(self.stats)):
                print(f"n{i+1}:")
                print(self.stats[i])
                print("-" * 80)

                if filename:
                    if ".csv" not in filename:
                        filename_changed = f"{filename}_n{i+1}.csv"
                    else:
                        filename_changed = filename.replace(".csv", f"_n{i+1}.csv")
                    self.stats[i].to_csv(filename_changed, index=False)

        else:
            print(self.stats)
            if filename:
                if ".csv" not in filename:
                    filename += ".csv"
                self.stats.to_csv(filename, index=False)

    def get_propensities(self, filename: str | None = None) -> pd.DataFrame:
        """Returns a data frame with the Participation Shift propensities.

        Arguments:
            filename: Name of the file (csv) to save the propensities data frame. Default to `None`.

        Returns:
            A Pandas [`DataFrame`][pandas.DataFrame] containing the propensities.
        """

        if self.stats is None:
            raise ValueError(
                "Parshift.stats is None. Please run Parshift.process() first."
            )

        if isinstance(self.stats, list):
            df = propensities(self.stats[0])
            df.index = ["n1"]  # type: ignore
            for i in range(1, len(self.stats)):
                dfx = propensities(self.stats[i])
                dfx.index = [f"n{i+1}"]  # type: ignore
                df = pd.concat([df, dfx])

            if filename:
                if ".csv" not in filename:
                    filename += ".csv"
                df.to_csv(filename, index=False)
            return df

        else:
            df = propensities(self.stats)
            df.index = ["n"]  # type: ignore

            if filename:
                if ".csv" not in filename:
                    filename += ".csv"
                df.to_csv(filename, index=False)
            return df
