---
type: experiment
id: EXP-20260813-037
date: 2026-08-13
question: Which exact retained ID-zero entry stream intervals differ between accepted FLICK.ALL and FLICKD.ALL, and which differences are reached by the demonstrated 0x0044F8E0 walk?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora offline exact-two-file analysis
environment_version: Python 3.14.6; GNU cmp 3.12; GNU objdump 2.44
working_directory: /home/dev/ABLPC
configuration: Exact accepted M2.20 files; retained entries 0-23 only; bounded 0x34/0x3C walk; metadata and offsets only
artifacts:
  - static/exports/BIN-97c95ba5572dce63/M2-id-zero-stream-difference-localization.md
addresses:
  - 0x00448010
  - 0x004480F4
  - 0x00448171
  - 0x0044F8E0
  - 0x0044F8EA
  - 0x004509E6
file_offsets:
  - 0x0004
  - 0x2AE8
  - 0x2C00
  - 0x34EC
result: twenty-three-changed-retained-stream-candidates-all-differences-walk-reached
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/static
  - re/resources
  - re/rendering
---

# EXP-20260813-037 - ID-zero stream-difference localization

> [!IMPORTANT] M2.26 correction
> `EXP-20260813-039` reclassifies the later provenance target: the shared
> `0x80`-stride arena is native-software output, while selected Direct3D uses
> separate batches. This experiment's file intervals, difference counts, and
> record-span localization remain exact.

## Question

Which exact retained ID-zero entry `+0x20` stream intervals contain bytes
that differ between the accepted unchanged `FLICK.ALL` and replacement source
`FLICKD.ALL`, and which differences are reached by the demonstrated
`0x0044F8E0` `0x34`/`0x3C` walk?

## Inputs and procedure

- Verified exact unchanged file SHA-256
  `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`
  and exact accepted replacement-source SHA-256
  `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.
  Both are `0x34EC` bytes.
- Reused only `EXP-20260812-034`'s exact 30-descriptor order, retained indices
  `[0,24)`, and cursor formula. Native instructions independently confirm that
  entry `+0x20` receives the current stream cursor at `0x004480F4-0x004480F6`
  before `0x00448171-0x00448181` advances it by twice the descriptor length.
- Partitioned only retained descriptors 0-23 into exact half-open file
  intervals and compared matching interval offsets.
- Applied `0x0044F8E0`'s demonstrated selector mask, `0x24`/`0x30` strides,
  zero-selector control, four-byte continuation rule, and an explicit
  enclosing interval bound to each file independently.
- Reconciled the result against an independent metadata-only `cmp -l` count.

No runtime was launched, no debugger or breakpoint was used, no file was
modified, no parser/editor was created, no payload byte values were retained,
and no PS1 source was consulted.

## Expected

The exact interval/walk comparison should select one changed retained stream,
retain the smallest exact candidate set, or stop on a contradictory bound.
Every difference inside the retained intervals must be classified.

## Observed

- Both files produce identical interval bounds, selector modes, record starts,
  and terminal control offsets for all 24 retained streams.
- The 24 intervals form the exact contiguous union `[0x0004,0x2AE8)`.
- Entry 8's interval `[0x0AA0,0x0AA4)` is byte-identical. Each entry in
  `{0-7, 9-23}` differs.
- Those 23 streams contain 2,102 differing byte positions across 183 selected
  records. All 2,102 lie in record spans reached by both identical bounded
  walks; zero differing retained bytes are beyond either walk.
- No continuation marker occurs. All terminal controls are identical and
  contain no differences.
- The known whole-file count is exactly reconciled: 2,102 retained-stream
  differences plus 13 descriptor-table differences equals 2,115. No
  difference lies in the non-retained stream range `[0x2AE8,0x2C00)`.

The evidence artifact records every interval, record start, selector mode,
terminal offset, and differing offset through exact record-relative
signatures. It contains no payload byte values.

## Independent checks

- Native `objdump` verifies the entry-pointer store and doubled-length cursor
  advance independently of the offline comparison.
- Both exact files independently satisfy the 30-descriptor/file-end and
  complete cursor partition bounds.
- GNU `cmp -l`, reduced to offsets and counts without retaining byte values,
  independently reports 2,115 total differences, 2,102 in the retained union,
  and the same 13 exact outside offsets.

## Confirmed

- The smallest exact retained-stream candidate set is `{0-7, 9-23}`.
- Every exact accepted-file difference inside those 23 retained streams lies
  within a record span reached by the demonstrated walk in both files.
- Retained entry 8 and the later non-retained stream range do not differ.

## Inferred

At least one member of the 23-entry set can contribute to the M2.20 visible
outcome through the retained-entry path. This follows from the prior accepted
file-to-render result plus the present localization, not from a field or asset
interpretation.

## Unknown and limitations

- Which candidate entry actually emits changed hardware output during the
  M2.20 visible frame or accounts for its repeated local region.
- Whether every differing byte in a reached record is individually read or
  contributes to output. “Reached” here is explicitly a bounded record-span
  classification.
- Meanings of selectors, record fields, descriptor fields, paths, and the
  visible figure.
- General `.ALL` bounds, grammar, malformed behavior, and safe edit surface.

## Contradictions and negative results

The offline discriminator does not select one stream: 23 retained streams
change, not one or a small semantic subset. That broad result is retained
rather than normalized. It also cannot identify visible contribution merely
because every changed byte is walk-reached.

## Result and follow-up

M2.24 is complete. The next bounded discriminator is a read-only matched
Direct3D capture of per-entry hardware-submission deltas around exact handoff
`0x0044C898-0x0044C89E`, limited to the 23-entry candidate set. It must record
metadata only and requires explicit approval before any breakpoint or
execution-control change. No target writes, payload dumps, semantic naming,
unsafe caller-gate instrumentation, PS1 comparison, or general parser is
authorized by this result.
