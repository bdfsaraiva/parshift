# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.1.0] - 2026-11-03

This release fixes defects that produced wrong results.

### Results may change

Results obtained with previous versions may change in the following cases.
Analyses based on such conversations should be repeated.

- **`termination` propensity of any conversation with at least one `A0-XY` or
  `A0-AY` participation shift.** The propensity summed the probability of
  `A0-XY` instead of `A0-AY`, contrary to Gibson's definition (the probability
  of the speaker keeping the floor). For example, for the sequence of codes
  `A0-AY`, `A0-AY`, `A0-AY`, `A0-XA`, the `termination` propensity was `0.0`
  and is now `0.75`; for `A0-XY`, `A0-XY`, `A0-XY`, `A0-XA`, it was `0.75` and
  is now `0.0`. The `turn-receiving` and `targeting` propensities are not
  affected.
- **Participation shift codes in conversations where a speaker ID contains
  `to`, internal spaces or commas, or is equal to `group`.** These IDs were
  split or confused with the group. For example, in a conversation between
  `Vitor`, `Antonio`, `Beto` and `Ana`, the codes `AB-XY`, `AB-XY`, `AB-XY`,
  `AB-XA`, `AB-XY`, `AB-XY` are now `A0-XA`, `AB-X0`, `A0-X0`, `A0-XA`,
  `AB-XA`, `AB-XA`. IDs with commas previously raised an `IndexError`.
  Leading and trailing spaces still do not distinguish speakers.
- **Participation shift codes in conversations with a `reply_to_id` that is
  not in a previous turn** (e.g., in truncated or segmented conversations).
  These turns reused the data of the previous turn, giving invalid codes such
  as `AB-AB` (not one of the 13 participation shifts) and a wrong code in the
  next turn. They are now considered as addressed to the group, with a
  warning. For example, the codes `A0-XA`, `AB-AB`, `AB-X0` are now `A0-XA`,
  `AB-X0`, `A0-X0`.
- **Participation shift codes in conversations where a speaker replies to
  themselves or targets themselves.** These turns gave invalid codes such as
  `A0-AA`, `AB-AA` or `AB-BB`, which were not counted in the statistics, or,
  with `target_id`, wrong codes such as `A0-XY`. A speaker does not address
  themselves, so these turns are now considered as addressed to the group,
  with a warning. For example, the codes `A0-XA`, `AB-BA`, `A0-AA` are now
  `A0-XA`, `AB-BA`, `AB-A0`.
- **Turns in conversations with `reply_to_id`, when a speaker replies in
  sequence to different utterances of the same speaker.** Consecutive
  messages from a speaker to the same addressee form a single turn, but with
  `reply_to_id` they were only merged when replying to the same utterance,
  giving invalid codes such as `A0-A0` and `AB-AB`, or an extra turn. They are
  now merged when the addressee (the speaker of the replied utterance) is the
  same. For example, if `S2` replies to two consecutive
  utterances of `S1`, the codes `A0-XA`, `A0-XA`, `AB-X0` (turns `[0, 1]`,
  `[2]`, `[3]`, `[4]`) are now `A0-XA`, `AB-X0` (turns `[0, 1]`, `[2, 3]`,
  `[4]`). The `reply_to_id` of a merged turn is the one of its first message.

As a result, `annotate()` now only gives the 13 participation shifts defined
by Gibson, which are unchanged, as are their classes.

### Fixed

- `frequency_treemap()` no longer adds the `Pshift_class` column to the data
  frame it receives. Previously, after plotting with `type="Pshift_class"`, the
  column also appeared in the statistics (e.g., in the CSV file saved by
  `Parshift.show_stats()`).
- `frequency_treemap()` now hides the axis of the given `ax` instead of the
  current axes.

### Added

- `cond_probs()` issues a warning when there are codes outside the 13
  participation shifts (which are not given by `annotate()`, but may exist in
  codes obtained otherwise). These codes are still not counted.

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

[1.1.0]: https://github.com/bdfsaraiva/parshift/compare/v1.0.3...v1.1.0
[1.0.3]: https://github.com/bdfsaraiva/parshift/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/bdfsaraiva/parshift/releases/tag/v1.0.2
