---
type: experiment
id: EXP-20260816-164
date: 2026-08-16
question: 'Does the single offline correction ordered by EXP-162 replace every rejected live camera claim with a reproducible PC-native view chain and support Bounded coverage without semantic inflation?'
status: completed-accepted
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; GNU objdump 2.46-3.fc44; checked Ghidra export; offline static PC evidence only
environment_version: Python 3.14.6
working_directory: /home/dev/ABLPC
configuration: clean subject HEAD 0238cccf1e73d8b04c576d2047da5e393b9f240e; exact retail work-copy executable; read-only toward originals and external PS1 source; no game, debugger, target write, implementation, or semantic rename
artifacts:
  - static/exports/BIN-97c95ba5572dce63/SUBSYS-camera-view-chain-static-trace.md
  - static/exports/BIN-97c95ba5572dce63/M2-positive-target-selector2-input-provenance.md
  - Vault/20-Research/PC camera view-transform chain.md
addresses:
  - "0x00405FE0"
  - "0x0040605F"
  - "0x00414580"
  - "0x0041458A"
  - "0x0041ACC0"
  - "0x0041ADF0"
  - "0x0041B7D0"
  - "0x0041B8C0"
  - "0x0041B920"
  - "0x00423EDE"
  - "0x00423F43"
  - "0x0044D4C1"
  - "0x0044D4F0"
  - "0x00455710"
  - "0x00455799"
  - "0x0045588D"
  - "0x00455910"
  - "0x004636C0"
  - "0x00463C80"
file_offsets:
  - "0x000053E0"
  - "0x0000545F"
  - "0x00013980"
  - "0x0001398A"
  - "0x0001A0C0"
  - "0x0001A1F0"
  - "0x0001ABD0"
  - "0x0001ACC0"
  - "0x0001AD20"
  - "0x000232DE"
  - "0x00023343"
  - "0x0004C8C1"
  - "0x0004C8F0"
  - "0x00054B10"
  - "0x00054B99"
  - "0x00054C8D"
  - "0x00054D10"
  - "0x00062AC0"
  - "0x00063080"
result: accepted-pc-view-anchor-supports-bounded-camera-coverage
created: 2026-08-16T19:30:00-04:00
updated: 2026-08-16T19:46:00-04:00
tags:
  - re/experiment
  - re/correction
  - re/camera
  - research/coverage
---

# EXP-20260816-164 - PC view-chain correction and coverage reclassification

## Worker verdict

**ACCEPTED by the fresh-context James audit in
[[EXP-20260816-165 - Independent PC view-chain correction audit]].** Native
instructions reproduce the corrected PC-only view chain, all rejected live
claims have bounded replacements, and the evidence supports Camera = Bounded
without promoting the source roles or manual controls. The accepted subject is
clean commit `0336d14dd0ce36b7f77d90d50e7ab693030b7f52`, and DEC-134's
temporary Untouched freeze is lifted by that verdict.

This packet is offline and PC-static only. It launched no game, Wine,
Gamescope, debugger, or target, performed no target write, changed no
implementation, assigned no semantic function/field name, and did not inspect
or modify the external PS1 checkout.

## Corrections completed

### Viewport and TL-vertex wording

- The correct short viewport structure locator is
  `0x00423EDE`-`0x00423F43` (file
  `0x000232DE`-`0x00023343`). The complete create/add/setup sequence is
  `0x00423E73`-`0x00423F71`.
- The three known Direct3D submissions at `0x004047E9`, `0x00405816`, and
  `0x0040598B` use `D3DVT_TLVERTEX`, so those known paths consume
  transformed/lit vertices and their relevant transform is game code. This
  does not prove the universal absence of Direct3D view state.

### Transform placement and caller correction

`0x00405FE0` reads pointer arguments and then performs the 3x3 signed
fixed-point transform locally beginning at `0x0040605F`; the first complete
component is `0x00406069`-`0x004060A1`. The twelve direct calls to thunk
`0x00401D66 -> 0x00405FE0` include one at `0x0044F99D` inside
`0x0044F8E0` and none inside `0x0045A7F0`. The checked pre-existing
`M2-positive-target-selector2-input-provenance.md` independently says
`0x0045A7F0` transforms coordinates and fills its batches inline. Therefore
the rejected upstream-transform and `0x0045A7F0` caller claims are removed.

### Confirmed PC-only structural chain

The exact evidence is exported in
`static/exports/BIN-97c95ba5572dce63/SUBSYS-camera-view-chain-static-trace.md`.
The bounded chain is:

```text
0x0041ADF0 updates Flik-relative source 0x0059DD90
                 |
0x0041B7D0 selects 0x0059DD90 or 0x0059A5C0
                 |
          common 0x00599C90
                 |
0x00455710 -> 0x00463C80 -> matrix 0x005B58E0
          \-> origin 0x005BDB8C; matrix copy 0x005BDBAC
                 |
renderer 0x0044D430 at 0x0044D4C1/0x0044D4F0
                 |
0x004636C0 -> scratch 0x0063E888-0x0063E8B0
                 |
local game-code transform in 0x00405FE0 from 0x0040605F
```

Confirmed instructions support each arrow: source reads/writes, flag-selected
copies, common-block argument, angle-to-matrix output, origin stores, two
renderer consumption edges, nine-word scratch load, and local matrix
multiply. The source roles “gameplay follow” and “setpiece/cinematic” remain
Inferred. Player controls, update frequency, all indirect paths, and the
second `0x0043D486 -> 0x00455710` call's role remain Unknown.

### Terrain census

Thunk `0x00401659 -> 0x004AC460` still has exactly seven direct calls:
`0x004329E9`, `0x004336D5`, `0x00433BA2`, `0x0043507E`,
`0x00437AD9`, `0x0043E716`, and `0x0044085A`. Subtracting reset functions
`0x00432930`/`0x00437A20` and known City dispatcher `0x00433900` leaves
four unmapped functions: `0x004336A0`, `0x00434E10`, `0x0043E6B0`, and
`0x0043F9E0`. Exactly two enclosing functions read Flik position, but neither
terrain-query argument is thereby proved to be Flik's live point.

## Evidence classification

- **Confirmed:** the instruction-level structural chain, correct viewport
  boundaries, three known TL-vertex submissions, local transform placement,
  `0x0045A7F0` non-caller disposition, and exact seven/four/two terrain
  counts.
- **Inferred:** ordinary follow-source, alternate scripted-source, and camera
  semantics for the two source blocks.
- **Unknown:** source/selector gameplay meanings, PC manual controls, runtime
  frequency and visual causality, second consumer-call role, all indirect
  callers, and D3D view state beyond the three known submissions.

## Cross-port disposition

XPORT-004 remains policy-clean at external commit
`1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51`. Its PS1 facts remain PS1-only.
The PC now independently supports the structural search hypotheses of two
sources/one selector and a render-consumed world-to-view-like transform; that
similarity does not promote PS1 names or roles into PC confirmation. The
manual-controls discrepancy remains open under KU-066, not a port difference.

## Coverage effect

The corrected PC evidence is sufficient for **Bounded**, not Mapped: a real
view-transform path is located, but controls, source semantics, frequency,
and runtime visual causality remain open. EXP-165 independently accepted the
chain and this classification at exact clean subject commit `0336d14`; the
coverage row is therefore promoted to Bounded without changing those open
questions.

## Independent audit result

[[EXP-20260816-165 - Independent PC view-chain correction audit]] returns
**ACCEPT** at clean subject commit
`0336d14dd0ce36b7f77d90d50e7ab693030b7f52`. The auditor independently
reproduced the retail binary hash, direct matrix join, renderer consumption,
source/update ordering, local transform, exact `12` builder calls, viewport
instruction boundaries, three-known-site TL-vertex scope, exact
seven/four/two terrain classification, XPORT boundary, live-claim hygiene,
and the Bounded-not-Mapped disposition. No corrective packet remains.
