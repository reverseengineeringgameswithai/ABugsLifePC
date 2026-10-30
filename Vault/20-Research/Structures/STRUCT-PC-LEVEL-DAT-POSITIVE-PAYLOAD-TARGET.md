---
type: structure
id: STRUCT-PC-LEVEL-DAT-POSITIVE-PAYLOAD-TARGET
status: inferred
confidence: high
evidence:
  - EXP-20260812-008
  - EXP-20260812-009
  - EXP-20260812-010
created: 2026-08-12
updated: 2026-10-02
tags:
  - re/structure
  - re/file-format
---

# PC LEVEL DAT positive payload target

## Scope

This dossier describes the nonnegative-count block consumed by PC function
`0x0045A7F0`. The byte grammar fits the complete Training primary population.
Its PC consumer attribution and cross-file validation are narrower: they cover
scene records satisfying `(flags & 0xBFEF) == 0x49` in the local 21-file corpus.
This dossier does not cover the consumer's negative-count branch or claim that
the block is a complete object definition.

## Confirmed layout

| Relative offset | Width | Structural name | Evidence |
|---:|---:|---|---|
| `+0x00` | 4 | signed entry count | `0x0045A82E`; nonnegative path at `0x0045A897` |
| `+0x04` | `count × 12` | 12-byte entry table | `0x0045A89B–0x0045A89E` |
| variable | 4 | command header: 16-bit mode, signed 16-bit item count | loop from `0x0045A8B0` |
| variable | `item_count × 16` | even-mode command items | even branch and 16-byte advance |
| variable | `item_count × 12` | odd-mode command items | odd branch and 12-byte advance |
| variable | 2 | command-stream terminator `0xFFFF` | `0x0045A8B0` |
| variable | to 4-byte alignment | preserved alignment bytes | Training block adjacency in `EXP-20260812-009` |

Command items contain three (odd mode) or four (even mode) 16-bit byte offsets
into the 12-byte entry table. The read-only parser rejects unaligned or
out-of-range references, negative item counts, truncation, and unsupported
negative entry counts.

## Training anchors

| Target | Entry count | Command stream | Terminator | End | Primary references |
|---:|---:|---:|---:|---:|---:|
| `0x111E4` | 102 | `0x116B0` | `0x11A80` | `0x11A84` | 11 |
| `0x1319C` | 67 | `0x134C4` | `0x13810` | `0x13814` | 17 |

The complete population is in
`reports/level-dat/EXP-20260812-009-training-primary-payload-targets.json`.
All 109 Training primary targets form one contiguous sequence from `0x38DC` to
`0x19E00` under this grammar.

## Consumer path

[[FUNC-97C95BA5572D-0044BB70]] relocates the selected target field.
[[FUNC-97C95BA5572D-004498F0]] selects dispatch `0x49` for Training flags
`0x0059` and passes payload `+0x1C` through thunk `0x00401604` to
[[FUNC-97C95BA5572D-0045A7F0]].

## Inferred semantics

`EXP-20260812-010` confirms that the block contributes reusable visible render
content: reciprocal four-byte target edits change only the independently
identified record-124 and record-125 placement regions. The narrower
interpretation that the 12-byte table is vertex-like remains inferred from
`0x0045A7F0`. Exact vertex fields, primitive names, materials, complete object
identity, and interaction with other payload fields remain unconfirmed.

*Pointer (2026-10-02 audit):* the same count/12-byte-table/tagged-group shape
is decoded for masked dispatch `0x41` in [[PC LEVEL DAT static mesh]]
(EXP-20260818-006/007, 2,543/2,543 retail payloads), where command items are
vertex byte offsets. That dossier's evidence is for dispatch `0x41`; this note's
dispatch-`0x49` semantics are not upgraded by it.

## Unsupported variants

- Negative entry count: the consumer takes a distinct, mutating branch.
- Guarded edits for scene dispatches other than masked value `0x49`; their
  consumer paths and the grammar's cross-file generality remain unverified.
- Arbitrary target offsets not accepted by this bounded parser.

## Next discriminating experiment

During M1.4, test another positive shared/contrasting target in a non-Training
scene after independently identifying the affected placements.

Done: [[EXP-20260812-013 - Level 01 target rebind no visible start effect]]
closed M1.4. A guarded Level 01 rebind was accepted by the executable but
changed no pixel at the tested start camera, so the affected placement was not
identified. This section is historical.
