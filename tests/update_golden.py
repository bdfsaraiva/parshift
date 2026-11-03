# Copyright (c) 2022-2023 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE or copy
# at http://opensource.org/licenses/MIT)

"""Regenerate the expected outputs stored in `tests/data/golden.json`.

The conversations (inputs) in the JSON file are kept as they are, only the
outputs of `annotate()`, `cond_probs()` and `propensities()` are rewritten.
Run it only when a change in the output is intended, and review the diff:

    python -m tests.update_golden
"""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from parshift import annotate, cond_probs, propensities, read_ccsv

GOLDEN_PATH = Path(__file__).parent / "data" / "golden.json"


def load_golden() -> List[Dict[str, Any]]:
    """Load the golden conversations and their expected outputs."""
    with open(GOLDEN_PATH, encoding="utf-8") as f:
        return json.load(f)


def conversation_df(entry: Dict[str, Any]) -> pd.DataFrame:
    """Build the conversation data frame of a golden entry using `read_ccsv()`."""
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(["utterance_id", "speaker_id", "utterance", entry["column"]])
    for utt_id, speaker, utterance, target in entry["rows"]:
        writer.writerow([utt_id, speaker, utterance, "" if target is None else target])
    buffer.seek(0)
    return read_ccsv(buffer)


def frame_to_json(df: pd.DataFrame) -> Dict[str, Any]:
    """Convert a data frame into a version independent representation."""
    return {
        "columns": [str(c) for c in df.columns],
        "index": [str(i) for i in df.index],
        "values": df.astype(str).values.tolist(),
    }


def outputs(entry: Dict[str, Any]) -> Dict[str, Any]:
    """Compute the outputs of the processing pipeline for a golden entry."""
    df_annot = annotate(conversation_df(entry))
    df_cp = cond_probs(df_annot)
    df_prop = propensities(df_cp)
    return {
        "annotate": frame_to_json(df_annot),
        "cond_probs": frame_to_json(df_cp),
        "propensities": frame_to_json(df_prop),
    }


def main() -> None:
    entries = load_golden()
    for entry in entries:
        entry.update(outputs(entry))
    with open(GOLDEN_PATH, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=1)
        f.write("\n")


if __name__ == "__main__":
    main()
