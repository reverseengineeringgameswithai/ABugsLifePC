---
type: session
date: 2026-08-12
agent: Codex
status: completed
tags:
  - session
  - re/static
  - re/resources
---

# Character request and retained range

## Agent

Codex

## Goal

Execute roadmap packet M2.21 under the START HERE workflow, bind accepted
Training `CHARS/FLICK.ALL` to its exact PC request/loader/first-consumer path
and bounded destination, preserve Obsidian evidence structure, avoid the unsafe
debugger region, and leave Git clean.

## Files inspected

- The full required START HERE sequence, Project Charter, Agent Operating
  Manual, current roadmap/state/environment, decision and unknown registers,
  relevant MOCs, function dossiers, M2.20 evidence, and prior resource traces.
- Exact structured Ghidra export and native disassembly of the unchanged
  executable hash
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Exact derived work-copy `CHARS/FLICK.ALL` and `CHARS3/FLICKD.ALL`, both
  `0x34EC` bytes with the hashes recorded in M2.20, only at offsets directly
  consumed by the traced instructions.
- Retained accepted run `RUN-WINE-20260812-231216`, including load line 1460.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments inspected

- [[EXP-20260812-015 - Plant pair caller and consumer trace]]
- [[EXP-20260812-033 - Character ALL replacement visible outcome]]
- [[EXP-20260812-034 - Character request and first consumer trace]]

## Changes made

- Added a reviewable static trace with exact request arms, thunk/call chain,
  one-file descriptor arithmetic, cursor boundary, and fixed destination
  addresses.
- Added `EXP-20260812-034`; updated the four affected function dossiers,
  Current State, roadmap, Known Unknowns, Decision Log, PC content census,
  format/capability boundaries, and relevant MOCs.
- Closed M2.21, resolved KU-033 at the request/first-consumer boundary, added
  KU-034 for the remaining M1 bridge, and recorded `DEC-20260812-029`.
- Made [[Project Roadmap#M2.22 — Character retained-range first-use bridge]]
  the single next packet. No runtime, debugger, parser, editor, or target-state
  modification was used.

## Conclusions

- **Confirmed:** `0x004671D0` supplies initial object index zero and calls
  `0x00445020`; its default `chars\flick`, ID-zero arm reaches
  `0x00444C40`, `.ALL` helper/consumer `0x00448010`, and whole-file loader
  `0x004AE240` at call site `0x00448079`.
- **Confirmed:** Both exact M2.20 `.ALL` files supply the same bounded 30
  source descriptors and comparison sequence. The first consumer materializes
  25 shared entries, but the coordinator consumes the final entry and retains
  header indices `[0,24)` in slot `0x005B18E0`, mapping to
  `[0x005A9660, 0x005A9DE0)`.
- **Confirmed:** Native disassembly, exact selected-file arithmetic, and the
  retained accepted runtime request independently agree at this boundary.
- **Unknown:** `.ALL` field meanings/general layout, arena capacity, filename
  identity, the exact entry contributing to the M2.20 render delta, and any M1
  placement/payload dependency.

## New hypotheses

The exact ID-zero retained range is the narrowest PC-native candidate for the
M2.20 visible character-family outcome. M2.22 must test its first safe use
rather than treat the path or render box as identity evidence.

## Contradictions discovered

The raw first-consumer count is 25, while the retained per-resource header
range contains 24 entries. Native caller instructions explain the difference:
the coordinator recognizes and excludes the final materialized entry. Both
bounds are preserved rather than normalized into one count.

## Tests run

- Native `objdump` disassembly/string checks and address-directed exact-file
  arithmetic: passed.
- `git diff --check`: passed.
- `make check`: dependency smoke imports, Vault lint (141 notes, zero errors
  or warnings), 130 tests, and tracked-file audit (zero violations) passed.

## Unresolved questions

- Which first post-initialization code reads slot `0x005B18E0` or retained
  entries `[0x005A9660, 0x005A9DE0)`?
- Can one M1-supported Training record or positive payload target be connected
  to that exact range under a bounded safe event?
- Which exact entry/subrange contributes to the M2.20 local render result?

## Recommended next action

Execute [[Project Roadmap#M2.22 — Character retained-range first-use bridge]].
Begin with static xrefs and native data-flow from the exact ID-zero header and
range after `0x004679C7`. Use a read-only natural-pause runtime window only if
static candidates remain ambiguous and after required breakpoint approval.

## Git commit if applicable

Bounded commit message: `research: trace character request and retained range`.
