---
type: structure
id: STRUCT-PC-CANDIDATE-HARDWARE-SUBMISSION-RECORD
status: inferred
confidence: high
evidence:
  - EXP-20260812-009
  - EXP-20260813-036
  - EXP-20260813-038
  - EXP-20260813-039
created: 2026-08-13
updated: 2026-10-02
tags:
  - re/structure
  - re/rendering
---

# PC candidate software-renderer 0x80-stride output record

## Scope

This dossier records only the selector-1 output structure demonstrably shared
by `0x0044F8E0` and `0x0045A7F0`. Exact selector and initializer evidence in
`EXP-20260813-039` identifies selector 1 as native software rendering and
`0x0049C520` as the arena allocator. It does not define a complete renderer
packet, assign primitive types, or claim that every writer populates the same
variant. The stable note ID retains its earlier candidate-hardware wording so
existing Obsidian links remain valid; that wording is superseded.

## Confirmed layout boundary

| Relative offset | Width | Structural role | Evidence |
|---:|---:|---|---|
| `+0x00` to `< +0x70` | variable writes | output values from transformed source records | native writes in both functions; exact field meanings unknown |
| `+0x70` | 4 | previous list-head pointer | `0x0045021A`, `0x004509A0`, `0x0045FFAE`, `0x0046022B` |
| `+0x74` | 2 | mode/flag word | native constant/table combinations in both functions |
| `+0x76` | 1 | additional mode/index byte | native writes in both functions |
| `< +0x80` | variable | writer-specific suffix values | exact writes differ by path |

The allocation stride is exactly `0x80` bytes:

```text
record = *(0x0081BC28) + *(0x008082C8) * 0x80
*(0x008082C8) += 1
```

Counter `0x008082C8` is checked against capacity `0x0081C138`. The record is
then inserted into a list-head topology reached through pointer global
`0x004E8CC8`. Some M1 paths add a caller-supplied head offset before the
derived depth index; exact same-head membership is therefore not implied by
the shared root.

## Producers

- [[FUNC-97C95BA5572D-0044F8E0]]: representative allocator sequences
  `0x0045005B-0x0045006F` and `0x00450838-0x0045084C`; representative list
  insertion sequences `0x0045020E-0x00450223` and
  `0x00450997-0x004509A9`.
- [[FUNC-97C95BA5572D-0045A7F0]]: representative positive-path allocator
  sequences `0x0045F974-0x0045F987` and `0x0045FFB8-0x0045FFCC`;
  representative insertion sequences `0x0045FFAC-0x0045FFB1` and
  `0x00460219-0x0046022E`.

## Renderer ownership

This is a native-software renderer output record, and `0x004E8CC8` reaches its
list-head array. `0x0049C520` logs `INITSOFTRENDER`, cites `soft.cpp`, writes
capacity `0x2800`, allocates `capacity << 7`, zeros the counter, and clears the
list heads. Both producer functions reach this arena only for renderer
selector 1. `EXP-20260813-038` independently finds the arena triple zero in
selector-2 Direct3D runs, as the corrected ownership predicts. Exact
primitive, material, texture, sort, and field semantics remain unknown.

## Unsupported claims

- A retained-entry source pointer equals an M1 positive target.
- Two emissions enter the same exact head without their runtime offset/depth
  values.
- The tested Direct3D retained-entry path emits into this structure.
- All bytes through `+0x7F` have stable meanings across producer variants.

## Next discriminating experiment

Keep this structure outside the completed M2.31 Direct3D admission-state
result and active offline-first M2.32 evaluator packet. Any future field
naming needs independent software-renderer evidence and must not be inferred
from the separate Direct3D batch layouts.

*Update (2026-10-02 audit):* M2.32 is no longer active. It completed with
[[EXP-20260813-046 - Exact 0A6C live admission receipt]], and
[[EXP-20260813-059 - Independent M2.41 disposition hard-truth audit]] left M2
deferred. No later experiment is cited here for this structure's fields; the
field-naming rule above still applies.
