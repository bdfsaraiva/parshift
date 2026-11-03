# Contributing to ParShift

Ideas, bug reports and pull requests are welcome. For a bug or a feature
request, please open an [issue](https://github.com/bdfsaraiva/parshift/issues).

## Development setup

```bash
git clone https://github.com/bdfsaraiva/parshift
cd parshift
python -m venv env
source env/bin/activate  # On Windows: . env\Scripts\activate
pip install -e .[dev]
```

Alternatively, with [uv](https://docs.astral.sh/uv/), the dependencies can be
installed with the exact versions in `uv.lock`:

```bash
uv sync --extra dev
```

## Before opening a pull request

- Add tests for every change or new feature, and make sure all tests pass,
  including the type checks run by `pytest`:

  ```bash
  pytest
  ```

- Format the code with [black](https://black.readthedocs.io/en/stable/):

  ```bash
  black parshift tests
  ```

- If the documentation changed, check that it builds without warnings:

  ```bash
  cd docs
  mkdocs build --strict
  ```

- Add an entry to [`CHANGELOG.md`](CHANGELOG.md) for changes visible to users.

## Golden tests

The tests in `tests/test_golden.py` compare the output of `annotate()`,
`cond_probs()` and `propensities()` for a set of conversations with the output
stored in `tests/data/golden.json`. They fail whenever the results change.

If a change is not supposed to change the results, these tests must pass
without changes. If it is (e.g., a bug fix), regenerate the expected outputs,
check in the diff that only the intended results changed, and document the
change in `CHANGELOG.md` under "Results may change":

```bash
python -m tests.update_golden
```

## Commit messages

Commit messages are in English, in the imperative mood, start with a capital
letter and have no period at the end, for example:

```text
Fix termination propensity using A0-XY instead of A0-AY
Add quickstart and input format to README
```

## Releases

1. Update the version in `pyproject.toml` and in `CITATION.cff`, and move the
   changes in `CHANGELOG.md` to a section for the new version.
2. Merge into `main` through a pull request, after CI passes.
3. Create a release on GitHub with a tag named `vX.Y.Z` on `main`. The tag
   publishes the package on PyPI and deploys the documentation.
