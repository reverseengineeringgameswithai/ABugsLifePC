---
type: cross-port-comparison
id: XPORT-20260814-001
status: completed
confidence: high
pc_binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
external_source_id: SRC-PS1-ABL
external_commit: 1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51
external_paths:
  - analysis/phase4_e08_object_census.json
  - analysis/phase4_c13_harvester.json
  - tests/test_phase4_c13_harvester.py
pc_evidence:
  - EXP-20260814-111
  - FUNC-97C95BA5572D-00417720
  - FUNC-97C95BA5572D-00456A90
external_evidence:
  - analysis/phase4_e08_object_census.json:4-15,595-624
  - analysis/phase4_c13_harvester.json:475-482
  - tests/test_phase4_c13_harvester.py:40-42
created: 2026-08-14
updated: 2026-10-02
tags:
  - re/cross-port
  - re/gameplay
  - re/collectibles
---

# XPORT-20260814-001 - Training grain selector and count

## Bounded question

Does the committed PS1 research identify a narrow selector/count hypothesis
worth testing independently against the PC Training type-`0x3F` table?

## PS1 source

External source `SRC-PS1-ABL`, commit
`1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51`, read through committed objects
only. The external working tree was dirty and was neither read as authority nor
modified.

- `analysis/phase4_e08_object_census.json:4-15` labels kind `0x14` as grain.
- The same file at lines `595-624` reports Level07/Level1 with one type-`0x3F`
  table, 62 entries, and 50 kind-`0x14` entries.
- `analysis/phase4_c13_harvester.json:475-482` independently records a
  16-byte source-record stride, kind `0x14`, 50 entries, and consumed-y
  sentinel `0x80000000` for the PS1 build.
- `tests/test_phase4_c13_harvester.py:40-42` asserts the 50-entry result.

These are PS1 facts only.

## PC source

- PC executable and exact Training DAT hashes are recorded in
  `EXP-20260814-111`.
- PC file locators: first top record `0x4`, selector at each 16-byte entry
  `+0x0C`, original insertion boundary `0x3E8`.
- PC executable locators: loader/fixup `0x0044BB70`, selector-`0x14` height
  branch `0x00456ACC`, consumed sentinel/counter path in `0x00417720`, and
  a candidate mode/level counter cap at `0x0043A0EB`. `EXP-20260814-112`
  shows the latter is not reached in its controlled Training transition and
  is not needed for a retained 51.

## Similarities

Both separately observed builds use a 62-entry Training type-`0x3F` table with
50 selector/kind-`0x14` entries, a 16-byte entry stride, and consumed-y sentinel
`0x80000000` in the bounded evidence.

## Differences

- The cited PS1 census reports a different source hash prefix from the exact PC
  DAT hash, so file identity is not assumed.
- Executable addresses, runtime pointers, platform behavior, and any format
  semantics beyond the listed measurements are platform-specific.
- The PC recipe relocates 556 PC loader-recognized file-relative fields after
  insertion; no PS1 relocation claim is imported.

## Inferred correspondence

The PS1 `0x14` label was useful only as a candidate search term. It did not
establish the PC meaning.

## PC discrimination and result

`EXP-20260814-111` independently confirms on PC that an appended selector
`0x14` record initializes, becomes the sole consumed adjacent record, and
increments the PC grain counter `0 -> 1`. The PC conclusion is therefore
confirmed within that exact experiment; no wider cross-port structure or
behavior correspondence is promoted.

## Unknown

Whether later levels, other selector classes, completion rules, and the
unidentified `0x00439E90` cap correspond across ports remains unknown. PC-only
`EXP-20260814-112` resolves Training's HUD/tally boundary without promoting a
new cross-port claim.

2026-10-02 audit pointer: PC labels for the other selector classes now come
from PC evidence alone: the `0x00417720` cases, applied to every original
type-`0x3F` table in [[EXP-20260927-001 - Complete original level Blender maps]]. The
per-class comparison with the PS1 enum, including the `0x30` mismatch, is
recorded in [[XPORT-20260818-007 - PS1 Blender-to-native level authoring pipeline and format leads]].
No cross-port correspondence beyond this note's grain measurements is promoted.
