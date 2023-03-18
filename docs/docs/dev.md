# Development

## Installing for development and/or improving the package

```bash
$ git clone https://github.com/bdfsaraiva/parshift
$ cd parshift
$ python -m venv env
$ source env/bin/activate
$ pip install -e .[dev]
```

On Windows replace `source env/bin/activate` with `. env\Scripts\activate`.

## Run tests

Test can be run with the following command:

```bash
$ pytest
```

To generate an HTML page with coverage data, do the following:

```bash
$ pytest --cov=parshift --cov-report=html
```

Then open the generated `htmlcov/index.html` file in your browser to see the
coverage HTML site.

## Build docs

Considering we're in the `parshift` project folder, run the following commands:

```bash
$ cd docs
$ mkdocs build
```

The generated documentation will be placed in `docs/site`. Alternatively, the
documentation can be generated and served locally with:

```bash
$ mkdocs serve
```

## Code style

ParShift's source code follows the [black] style.

[black]: https://black.readthedocs.io/en/stable/
