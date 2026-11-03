# Usage

## Input format

ParShift reads conversations from CSV files (with
[`read_ccsv()`][parshift.read_ccsv]) or from Pandas data frames with one
utterance (message) per row and the following columns:

| Column | Description |
| ------ | ----------- |
| `utterance_id` | ID of the utterance (integer) |
| `speaker_id` | ID of the speaker |
| `utterance` | The utterance itself (text) |
| `reply_to_id` **or** `target_id` | See [reply and target modes](#reply-and-target-modes) below |

An empty value (or `None`) in the `reply_to_id` or `target_id` column means the
utterance is addressed to the group. Additional keyword arguments of
[`read_ccsv()`][parshift.read_ccsv] are passed to Pandas
[`read_csv()`][pandas.read_csv], e.g., `sep=";"` for files separated by
semicolons.

## Reply and target modes

The addressee of each utterance is given by one of two columns, which define
how ParShift interprets the conversation:

- **`reply_to_id`** (reply mode): ID of the **utterance** being replied to. The
  addressee is the speaker of that utterance. This is the format of chats and
  forums where messages reply to other messages.
- **`target_id`** (target mode): ID of the **speaker** being addressed. This is
  the format of annotated conversations where the addressee is known.

If both columns exist, `reply_to_id` is used and `target_id` is ignored.

For example, the same conversation in both modes:

Reply mode:

```csv
utterance_id,speaker_id,utterance,reply_to_id
0,10,Hello everyone!,
1,11,Hi!,0
2,10,How are you?,1
```

Target mode:

```csv
utterance_id,speaker_id,utterance,target_id
0,10,Hello everyone!,
1,11,Hi!,10
2,10,How are you?,11
```

Both give the participation shift codes `A0-XA` (speaker 11 answers a remark
to the group by 10) and `AB-BA` (10 answers back).

## Turns

Participation shifts are computed between **turns**, not between utterances. A
turn is a sequence of consecutive utterances by the same speaker to the same
addressee (or to the group). In reply mode, the addressee is the speaker of the
replied utterance, so consecutive replies to different utterances of the same
speaker are in the same turn.

The first turn of a conversation has no participation shift code, since there
is no previous turn. In reply mode, a turn is compared with the turn it
replies to; otherwise, it is compared with the previous turn.

[`annotate()`][parshift.annotate] only assigns the 13 participation shifts
defined by Gibson. For this purpose, the following turns are considered as
addressed to the group, and a warning with their number is issued:

- turns addressed to their own speaker, e.g., a speaker replying to their own
  utterance, or targeting themselves;
- in reply mode, turns replying to an utterance which is not in a previous turn,
  e.g., an utterance outside the data, in truncated or segmented conversations.

## Known limitations

- **IDs in `reply_to_id` and `target_id` must be integers.** Other values
  raise a `ValueError`. In target mode this means that speakers must be
  identified by integers, so that they can be addressed.
- **In target mode, speaker IDs must be written as the integers in
  `target_id`.** Speaker IDs are compared as text, without leading and
  trailing spaces, while targets are converted to integers. For example, a
  speaker `007` is not recognized as the target `7`.
- **Speaker IDs are otherwise opaque**: they can contain any text, including
  spaces and commas. Leading and trailing spaces do not distinguish speakers.
- **[`Parshift.process()`][parshift.Parshift.process] splits a conversation in
  at most 4 parts** (`N` between 1 and 4), with approximately the same number of turns each.
