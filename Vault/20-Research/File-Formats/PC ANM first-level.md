---
type: file-format
id: FMT-PC-ANM-FIRST-LEVEL
status: inferred
confidence: high
evidence:
  - EXP-20260812-015
  - EXP-20260812-017
  - EXP-20260812-018
  - EXP-20260812-019
  - FUNC-97C95BA5572D-00444B70
  - FUNC-97C95BA5572D-00445FF0
  - EXP-20261001-002
created: 2026-08-12
updated: 2026-10-02
tags:
  - re/file-format
  - re/resources
---

# PC ANM first-level

## Known magic/signature

No magic is confirmed. The independent inspector recognizes only the bounded
header/count/offset shape consumed by `0x00444B70`.

## Extensions

`.ANM`. The exact PC caller appends `.anm` at executable string
`0x004DDC14` before loading through `0x004AE240` at `0x00444CD8`.

## Observed files

All 11 files under the exact derived PC `CD/PLANTS` directory pass the bounded
inspector. Plants 04, 05, 06, and 10 were selected in M2.2 because both
retained Training and Level 01 hardware logs request them. Exact hashes and
offsets are in `reports/resources/pc-plant-anm-first-level.md`.

## Endianness

Little-endian, confirmed by the x86 reads and matching PC file values.

## Header

| Offset | Width | Bounded name | Status |
|---:|---:|---|---|
| `+0x00` | 2 | field 00 | unknown; caller overwrites with 1 before consumer |
| `+0x02` | 2 | signed first-level offset count | confirmed |
| `+0x04` | 2 | field 04 | unknown; caller overwrites before consumer |
| `+0x06` | 2 | field 06 | unknown |
| `+0x08` | `count*4` | file-relative dword offset table | confirmed |

`0x00444B70` permits zero offsets and relocates nonzero offsets in place. The
independent parser retains zero as absent and requires every nonzero offset to
remain within the exact file.

## First nonzero referenced record

Only the first nonzero reference is inspected further by this consumer:

| Relative offset | Width | Bounded name | Status |
|---:|---:|---|---|
| `+0x00` | 8 | unknown prefix | unknown/preserved |
| `+0x08` | 2 | unsigned signed-item count | confirmed |
| `+0x0A` | 2 | unknown field | unknown/preserved |
| `+0x0C` | `count*2` | signed-word items | confirmed width; semantics unknown except `-2` branch |

The routine publishes pointers to the list start and end and reacts when an
item equals `-2`. It does not establish complete nested-record semantics.

## Offsets and counts

- First-level count is read as signed. The safe parser rejects negative counts
  rather than reproducing the original routine's no-loop behavior.
- The nested count is read as unsigned.
- The original consumer receives no byte-size argument. The independent
  parser adds exact file-size bounds for every read and offset.
- Across all 11 files, first-level counts are 3 or 4; the first offset equals
  the offset-table end, and all offsets are nonzero, even, strictly increasing,
  and in range. These are corpus observations, not complete format rules.

## Unknown fields

All header and nested fields not named above remain unknown and are preserved
in the parser's complete source byte string. Since EXP-20261001-002 the slot
records are known to be animation clips (frame count, parts, frames; see
[[#Slot records (2026-10-01)]]); geometry, object and material semantics and
the meanings of the linear, angle and extra words remain unassigned.

## Slot records (2026-10-01)

[[EXP-20261001-002 - Flik animation catalog]] decodes every slot record as
read by pose sampler `0x00445FF0` (disassembly-confirmed). Each nonzero
first-level offset is one slot's record:

| Relative offset | Width | Field | Status |
|---:|---:|---|---|
| `+0x00` | 2 | field 00 | not read by the sampler; equals the slot index in all 303 retail records |
| `+0x02` | 2 | frame count (`& 0x7FFF`); bit `0x8000` selects an unused sampler branch | confirmed |
| `+0x04` | 2 | part count (sampler loop bound) | confirmed |
| `+0x06` | 2 | words per frame | confirmed |
| `+0x08` | 2 | part-list count (equals `+0x04` in every retail record) | confirmed |
| `+0x0A` | 2 | bitmask byte length | confirmed |
| `+0x0C` | `count*2` | per-part word offset into a frame; `-3` inherit, `-2`/`-1` skip | confirmed |
| then | `+0x0A` bytes | per-part bitmask: bit set = part has three extra words | confirmed |
| then | `frames*words*2` | frames of signed 16-bit words | confirmed |

A driven part reads six words (three linear, three 12-bit angles) or nine when
its bitmask bit is set. With `+0x0A` respected, 303 records in 60 of the 61
retail `.ANM` files end exactly at the next record or at file end (zero slack).
`LEVEL00/ROSIEWLK.ANM` is the exception: its first offset `0x10000` lies beyond
its `0x2E99`-byte file, so it does not follow this layout and is rejected.

The earlier statement that the first record's `+0x00` prefix and `+0x0A` are
unknown is superseded for the slot-record layer: `+0x0A` is the bitmask
length. Linear-word, angle-axis and extra-word meanings remain open.

## Cross-referenced functions

- [[FUNC-97C95BA5572D-00444C40]]: `.ANM`/`.ALL` pair coordinator and loader
- [[FUNC-97C95BA5572D-00444B70]]: bounded first-level consumer
- [[FUNC-97C95BA5572D-004AE240]]: whole-file loader

## Runtime observations

`EXP-20260812-015` records exact `.ANM` requests in retained Direct3D hardware
logs. `EXP-20260812-018` replaces plant 04 `.ANM` with the equal-size,
same-first-level-layout plant 10 `.ANM` while leaving plant 04 `.ALL`
unchanged. The exact executable accepts the substitution through Direct3D
Training `NextLife`, but no stable visible difference is discriminated at the
tested start camera. This does not identify `.ANM` semantics or establish
general interchangeability.

`EXP-20260812-019` replaces the `.ANM` and equal-size `.ALL` together. That
exact pair is also accepted through `NextLife`, and its visual delta remains
inside independent control animation variance. Pair acceptance likewise does
not identify either format or establish a general compatibility rule.

## Parser status

`reimplementation/ablpc/anm.py` is a read-only, lossless, bounds-checked
inspector. Since 2026-10-01, `AnmFile.records()` also parses every slot
record (`AnmRecord`), rejecting records that would read past the next record
or file end, unknown negative part values, part spans outside the frame, and
bitmasks too short for the part count. `ablpc-mod inspect-anm` inspects one file; `scan-anm` validates a
directory. Neither command emits payload bytes or edits files.

## Test coverage

At `EXP-20260812-017`, sixteen synthetic tests covered source-byte preservation, zero offsets,
truncated headers, negative/impossible first-level counts, out-of-range
offsets, truncated nested headers, impossible nested counts, metadata-only
JSON, case-insensitive extension scanning, and per-file failure reporting.
The full suite then passed 38 tests. The exact 11-file PC plant corpus passes with
zero failures (`EXP-20260812-017`). Runtime acceptance of one whole-file copy
is evidence about that exact pair, not parser validation for broader layouts
(`EXP-20260812-018`).
The paired result adds an exact runtime compatibility observation without
expanding the parser or editing boundary (`EXP-20260812-019`).
Since commit `b73fb31` (EXP-20261001-002), `tests/test_anm.py` collects 26
cases, adding slot-record parsing and rejection tests; the 38-test figure is
the whole repository suite of 2026-08-12.
