---
type: experiment
id: EXP-20260820-003
title: R2n PC state-equivalence read candidates
date: 2026-08-20
environment: Offline static PC analysis only
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
question: Which exact PC-native view and coordinate ranges have sufficient producer/consumer evidence and phase bounds to preregister as future read-only equality candidates after R2m rejected fixed wall-clock alignment?
status: completed
result: Six exact equality ranges and two completion PCs bounded; renderer scratch excluded
created: 2026-08-20
updated: 2026-08-20
tags:
  - experiment
  - pc
  - anthill
  - level01
  - static-analysis
  - camera
---

# EXP-20260820-003 - R2n PC state-equivalence read candidates

## Purpose

[[EXP-20260820-002 - R2m offline cross-time correspondence diagnostic]]
closed fixed wall-clock lag alignment as nonviable. This packet performs the
next sequencing-approved action: offline PC-static analysis of possible
future state-equivalence reads. It does not design or run a runtime arm.

## Method and build binding

The checked retail Ghidra export was used only to locate references, under
[[Ghidra export structure and caveats]]. Native disassembly and the accepted
[[PC camera view-transform chain]] supply claim authority. The full trace is
`static/exports/BIN-97c95ba5572dce63/R2N-state-equivalence-read-candidates.md`.

Retail hash is `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`;
recent arms use auto-hardware hash
`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`.
The files have equal size and identical PE section layout. Their complete
physical diff is eight changed startup-code bytes within file
`0x000A6C6B..0x000A6C73` plus one relocation byte at `0x000FA913`. None
overlaps this packet's instruction or data locators, so the exact addresses
are rebound to the executed build without claiming wider behavioral parity.

## Result: two coherent phase snapshots

At PC `0x00414585`, after the selected-copy function returns and before the
transform call, the admitted upstream candidates are:

| Address | Width | Equality ceiling |
|---|---:|---|
| `0x0059A5EE` | 1 byte | compare bit 0 only; selector semantics remain unknown |
| `0x00599C90` | 18 bytes | selected three-dword plus three-word common input |
| `0x0059D910` | 12 bytes | live Flik coordinates only, not complete player state |

At PC `0x0041458F`, after the transform call returns and before later
main-loop work, the admitted generated-view candidates are:

| Address | Width | Equality ceiling |
|---|---:|---|
| `0x005B58E0` | 18 bytes | generated nine signed matrix words |
| `0x005BDB8C` | 12 bytes | three copied origin dwords |
| `0x005BDBAC` | 18 bytes | renderer-consumed nine-word matrix copy |

`0x005BDB9C/12` is optional and redundant at the second phase: it holds the
derived position-divided-by-32 values supplied by `0x004498F0` to
`0x0045A7F0`, but the renderer also mutates it.

The copied matrix stops at 18 bytes. The physical 32-byte `rep movsd` does not
make the tail one matrix: `+0x12..+0x13` remain unknown and
`+0x14/+0x18/+0x1C` are translation dwords consumed and mutated separately.

## Rejected candidate

Rows at `0x0063E888`, `0x0063E898`, and `0x0063E8A8` plus translation span
`0x0063E8B8` are real render-transform scratch. They are repeatedly reloaded
for different jobs and are not persistent equality anchors. `0x0045A7F0`
reads that scratch indirectly; it is not a caller of `0x00405FE0` and does not
directly consume `0x005B58E0`.

## Claim and authorization ceiling

This packet performs no game launch, process-memory read, signal, input, DAT
creation/write, localizer creation, candidate creation, or runtime/debugger
write. It authorizes none of them.

Any successor must be separately committed and audited. It must bind the
auto-hardware hash, exact completion PCs, exact owned-process execution stop,
coherent reads, receipts, and cleanup. Exact cross-arm equality and equality
of the two matrix copies must fail closed. Asynchronous polling, nearest-state
matching, normalization, tolerances, and post-hoc range expansion are
forbidden. Fresh explicit user authorization is required.

Even a future exact match would establish only these bounded byte/bit values
at two instruction phases. It would not prove complete frame state, face-8
visibility or occlusion, terrain/ground/material/collision identity,
causality, no effect, or retail/derived behavioral equivalence.

## Links

- [[EXP-20260820-002 - R2m offline cross-time correspondence diagnostic]]
- [[PC camera view-transform chain]]
- [[FUNC-97C95BA5572D-00405FE0]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Known Unknowns]]
- [[Reverse Engineering MOC]]
- [[Current State]]
