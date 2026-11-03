# Copyright (c) 2022-2026 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE or copy
# at http://opensource.org/licenses/MIT)

"""Golden tests: compare the output of the processing pipeline with the one
stored in `tests/data/golden.json`. To regenerate the expected outputs after an
intended change, run `python -m tests.update_golden`."""

import pytest

from parshift import annotate, cond_probs, propensities
from parshift.annotation import _p_shift_dict

from .update_golden import conversation_df, frame_to_json, load_golden

# Some golden conversations reply to utterances which do not exist and have
# self-replies on purpose
pytestmark = [
    pytest.mark.filterwarnings(
        "ignore:.*reply to an utterance which is not in a previous turn:UserWarning"
    ),
    pytest.mark.filterwarnings(
        "ignore:.*are addressed to their own speaker:UserWarning"
    ),
]

_golden = load_golden()


@pytest.fixture(params=_golden, ids=[e["name"] for e in _golden])
def golden(request):
    """A golden conversation and its expected outputs."""
    return request.param


def test_golden_annotate(golden):
    result = annotate(conversation_df(golden))
    assert frame_to_json(result) == golden["annotate"]


def test_golden_cond_probs(golden):
    result = cond_probs(annotate(conversation_df(golden)))
    assert frame_to_json(result) == golden["cond_probs"]


def test_golden_propensities(golden):
    result = propensities(cond_probs(annotate(conversation_df(golden))))
    assert frame_to_json(result) == golden["propensities"]


def test_golden_codes_are_valid(golden):
    """Test that `annotate()` only gives the 13 participation shifts (and no code
    for the first turn)."""
    result = annotate(conversation_df(golden))
    assert set(result["pshift"][1:]) <= set(_p_shift_dict)
    assert result["pshift"][0] == ""
