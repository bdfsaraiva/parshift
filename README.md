[![Tests](https://github.com/bdfsaraiva/parshift/actions/workflows/tests.yml/badge.svg)](https://github.com/bdfsaraiva/parshift/actions/workflows/tests.yml)
[![Codecov](https://codecov.io/gh/bdfsaraiva/parshift/branch/main/graph/badge.svg?token=O5ZCGFW78U)](https://codecov.io/gh/bdfsaraiva/parshift)
[![Docs](https://img.shields.io/badge/docs-stable-blue.svg)](https://bdfsaraiva.github.io/parshift)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/bdfsaraiva/py-Participation-Shifts/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/parshift)](https://pypi.org/project/parshift/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# ParShift

ParShift is a python package based on [Gibson's framework] for the analysis of
conversational sequences.

The framework is established on the concept of participation shift, which refers
to the shifting of individuals between the positions of speaker, target
(addressee), and non-addressee (everyone else), in a group conversation.

## Installation

### From PyPI

```bash
pip install parshift
```

### From source

Directly using pip:

```bash
pip install git+https://github.com/bdfsaraiva/parshift.git#egg=parshift
```

Or each step at a time:

```bash
git clone https://github.com/bdfsaraiva/parshift
cd parshift
pip install .
```

## Getting Started

For an in-depth overview of the features of ParShift please check the
[documentation][docs] or follow along the provided example:

| Name  | Link  |
|---|---|
| Participation Shifts with ParShift | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)][example1]  |

## Features/Improvements

We're open to any idea or suggestion to further improve this package.
If you have an idea or a feature request, just open an [issue]. 🤗

## For developers

After you cloned the repo head into the `parshift` base directory, `cd` into it,
create a virtual environment and then install ParShift in development mode:

```bash
pip install -e .[dev]
```

Make sure that all tests pass and that there aren't any issues:

```bash
pytest
```

Now you are ready to start developing the project! Don't forget to add tests for
every new change or feature!

## License

[MIT License](LICENSE)

[Gibson's framework]:https://doi.org/10.1353/sof.2003.0055
[docs]:https://bdfsaraiva.github.io/parshift/
[example1]:https://colab.research.google.com/drive/1gYa32dMQDVuKwHDLgl1wJiVyHwUw4_zL?usp=sharing
[issue]:https://github.com/bdfsaraiva/parshift/issues/new/choose
