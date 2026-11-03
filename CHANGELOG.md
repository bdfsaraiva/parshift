# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.3] - 2026-11-03

Maintenance release. **The output of ParShift does not change**: for the same
input, `annotate()`, `cond_probs()`, `propensities()` and the `Parshift` class
return the same results as in version 1.0.2.

### Changed

- Minimum Python version is now 3.11.
- Minimum versions of the dependencies are now declared: `numpy>=1.26`,
  `pandas>=2.2`, `matplotlib>=3.8` and `squarify>=0.4.3`. NumPy was already
  used, but was not declared as a dependency.
- Package metadata updated to current standards (SPDX license expression,
  supported Python versions, `Typing :: Typed` classifier).

### Fixed

- Compatibility with pandas 3: removed the deprecated usages that raised
  `Pandas4Warning` in `annotate()` and `cond_probs()`.
- `parshift` no longer imports pandas private types at runtime.
- Documentation build with current versions of mkdocstrings.

### Added

- Golden tests that freeze the output of the processing pipeline for 43
  conversations, checked with pandas 2 and pandas 3.
- CI runs the tests weekly, with the minimum versions of the dependencies and
  with the latest Python version, and builds the documentation in strict mode.

## [1.0.2] - 2025-09-12

- Last release before this changelog was created.

[1.0.3]: https://github.com/bdfsaraiva/parshift/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/bdfsaraiva/parshift/releases/tag/v1.0.2
