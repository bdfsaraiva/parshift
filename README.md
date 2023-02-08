[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/bdfsaraiva/py-Participation-Shifts/blob/main/LICENSE)
[![Docs](https://img.shields.io/badge/docs-Passing-green.svg)](https://bdfsaraiva.github.io/parshift)
[![Build](https://github.com/bdfsaraiva/parshift/actions/workflows/ci.yml/badge.svg)](https://github.com/bdfsaraiva/parshift/actions/workflows/ci.yml)
[![Codeov](https://codecov.io/github/bdfsaraiva/parshift/branch/main/graph/badge.svg?token=O5ZCGFW78U)](https://codecov.io/github/bdfsaraiva/parshift)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# ParShift

ParShift is a python package based on [Gibson's framework](https://doi.org/10.1353/sof.2003.0055) for the analysis of conversational sequences.

The framework is established on the concept of participation shift, which refers to the shifting of individuals between the positions of speaker, target (addressee), and non-addressee (everyone else), in a group conversation.


## Installation
#### From PyPI
```bash
pip install parshift #not available yet 
```
#### From source
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
For an in-depth overview of the features of ParShift 
you can check the [**full documentation**](https://bdfsaraiva.github.io/parshift/) or you can follow along 
with the example below:


| Name  | Link  |
|---|---|
| Participation Shifts with ParShift | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1gYa32dMQDVuKwHDLgl1wJiVyHwUw4_zL?usp=sharing)  |


## Features/Improvements

I open to any form of idea to further improve this package. If you have an idea or a feature request - just open an
issue.🤗


## For developers

After you cloned the repo head into the `parshift` base directory.

Then install all dependencies:

```bash
$ pip install .[dev]
```

Make sure that all tests pass and that there aren't any issues:

```bash
$ pytest ./
```

Now you are ready to start developing on the project! Don't forget to add tests for every new change or feature!
