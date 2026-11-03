# Copyright (c) 2022-2026 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE or copy
# at http://opensource.org/licenses/MIT)

from importlib.metadata import version

import parshift


def test_version():
    """Test that `__version__` is the version of the installed package."""
    assert parshift.__version__ == version("parshift")
    assert parshift.__version__.count(".") == 2
