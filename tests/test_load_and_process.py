# Copyright (c) 2022-2023 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE or copy
# at http://opensource.org/licenses/MIT)

from parshift import load_and_process


def test_load_and_process(file_csv_good):
    """Test that `load_and_process` returns a dict."""

    result = load_and_process(file_csv_good["csv_in"], **(file_csv_good["kwargs"]))

    assert type(result) == dict
