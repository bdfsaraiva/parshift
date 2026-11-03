[![Tests](https://github.com/bdfsaraiva/parshift/actions/workflows/tests.yml/badge.svg)](https://github.com/bdfsaraiva/parshift/actions/workflows/tests.yml)
[![Codecov](https://codecov.io/gh/bdfsaraiva/parshift/branch/main/graph/badge.svg?token=O5ZCGFW78U)](https://codecov.io/gh/bdfsaraiva/parshift)
[![Docs](https://img.shields.io/badge/docs-stable-blue.svg)](https://bdfsaraiva.github.io/parshift)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/bdfsaraiva/parshift/blob/main/LICENSE)
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

### Input format

ParShift reads conversations from CSV files with one utterance (message) per
row and the following columns:

| Column | Description |
|---|---|
| `utterance_id` | ID of the utterance (integer) |
| `speaker_id` | ID of the speaker |
| `utterance` | The utterance itself (text) |
| `reply_to_id` **or** `target_id` | ID of the utterance being replied to, **or** ID of the speaker being addressed (integer); empty if the utterance is addressed to the group |

For example (`conversation.csv`):

```csv
utterance_id,speaker_id,utterance,reply_to_id
0,Ana,Hello everyone!,
1,Bruno,Hi Ana!,0
2,Carla,Good morning.,
3,Ana,"Carla, how are you?",2
4,Carla,"Fine, thanks.",3
5,Bruno,What are we discussing today?,
```

See the [documentation][usage] for how each column is interpreted.

### Quickstart

Annotate the conversation with participation shift codes, and obtain the
conditional probabilities and propensities:

```python
from parshift import annotate, cond_probs, propensities, read_ccsv

conv = read_ccsv("conversation.csv")
pshifts = annotate(conv)  # One participation shift code per turn
stats = cond_probs(pshifts)  # Frequencies and conditional probabilities
print(propensities(stats))  # Gibson's propensities
```

```text
   turn-receiving  targeting  termination
0            0.33        0.0          0.0
```

The same analysis is available through the `Parshift` class, which can also
split the conversation in up to four parts and plot the results:

```python
from parshift import Parshift

ps = Parshift()
ps.process("conversation.csv")  # Use N=2, 3 or 4 to split the conversation
ps.show_stats()
ps.show_plot()
print(ps.get_propensities())
```

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

See [CONTRIBUTING.md](CONTRIBUTING.md) for the guidelines on tests, commit
messages and releases.

## Reference

If you use this software, please cite the following reference:

* Ferreira-Saraiva, B.D., Matos-Carvalho, J.P., Fachada, N. & Pita, M. (2023).
  ParShift: a Python package to study order and differentiation in group
  conversations. *SoftwareX*, 24. 101554.
  <https://doi.org/10.1016/j.softx.2023.101554>

## License

[MIT License](LICENSE)

[Gibson's framework]:https://doi.org/10.1353/sof.2003.0055
[docs]:https://bdfsaraiva.github.io/parshift/
[usage]:https://bdfsaraiva.github.io/parshift/usage/
[example1]:https://colab.research.google.com/drive/1zjstEdkIZrCSgZFkilNf8kvTkRCS-bYG?usp=sharing
[issue]:https://github.com/bdfsaraiva/parshift/issues/new/choose
