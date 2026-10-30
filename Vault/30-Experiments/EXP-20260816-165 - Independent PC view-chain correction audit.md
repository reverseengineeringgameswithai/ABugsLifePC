---
type: experiment
id: EXP-20260816-165
date: 2026-08-16
question: 'Does fresh-context adversarial review accept EXP-164 at exact clean worker commit 0336d14, including the direct PC view-matrix join and Bounded Camera disposition?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline static audit; GNU objdump 2.46-3.fc44; radare2; existing checked Ghidra export; no runtime, debugger, or target write
environment_version: Python 3.14.6
working_directory: /home/dev/ABLPC
configuration: fresh-context read-only audit of exact clean subject 0336d14dd0ce36b7f77d90d50e7ab693030b7f52 against parent 0238cccf1e73d8b04c576d2047da5e393b9f240e; exact retail work-copy executable; no originals or external PS1 checkout access
artifacts:
  - static/exports/BIN-97c95ba5572dce63/SUBSYS-camera-view-chain-static-trace.md
  - static/exports/BIN-97c95ba5572dce63/M2-positive-target-selector2-input-provenance.md
  - Vault/20-Research/PC camera view-transform chain.md
addresses:
  - "0x0040605F"
  - "0x00414580"
  - "0x0041458A"
  - "0x0041ADF0"
  - "0x0041B7D0"
  - "0x0041B8C0"
  - "0x0041B920"
  - "0x00423EDE"
  - "0x00423F43"
  - "0x0044D4C1"
  - "0x0044D4F0"
  - "0x00455788"
  - "0x00455799"
  - "0x0045588D"
  - "0x00455910"
  - "0x004636C0"
  - "0x00463C80"
result: accept-exp164-camera-bounded-at-clean-0336d14
created: 2026-08-16T19:46:00-04:00
updated: 2026-08-16T19:46:00-04:00
tags:
  - re/experiment
  - re/audit
  - re/camera
  - research/coverage
---

# EXP-20260816-165 - Independent PC view-chain correction audit

## Verdict

**ACCEPT** at exact clean subject commit
`0336d14dd0ce36b7f77d90d50e7ab693030b7f52` against parent
`0238cccf1e73d8b04c576d2047da5e393b9f240e`.

The EXP-164 correction survives fresh-context hard-truth review. The PC-native
view path is directly joined to renderer consumption, every rejected locator
and count has an honest live replacement, and Camera = Bounded is supported
without promoting source roles, controls, runtime frequency, visual causality,
or indirect-path completeness. No corrective packet remains.

The audit was offline and read-only. It made no repository edit, launched no
game, Wine, Gamescope, debugger, or target, performed no target write or
helper termination, and did not access the external PS1 working tree or
`originals/`.

## Independently reproduced PC evidence

### Direct matrix and renderer join

- `0x00455788` pushes output `0x005B58E0`; `0x00455799` calls thunk
  `0x004012BC -> 0x00463C80`.
- `0x00463C80` writes all nine matrix words through that output pointer at
  `0x00463D55`, `0x00463D6D`, `0x00463D78`, `0x00463DB1`,
  `0x00463DC8`, `0x00463DE1`, `0x00463E17`, `0x00463E31`, and
  `0x00463E48`.
- Renderer `0x0044D4C1` pushes the same `0x005B58E0`; `0x0044D4C6` calls
  thunk `0x00401C4E -> 0x004636C0`, which expands the nine signed words into
  scratch `0x0063E888`-`0x0063E8B0`.
- `0x00455710` also writes origin `0x005BDB8C`/`90`/`94` at
  `0x0045588D`-`0x004558A5` and copies matrix-adjacent dwords into
  `0x005BDBAC`. Renderer pushes matrix/origin at
  `0x0044D4EB`/`0x0044D4F0` and calls `0x004A3990` at `0x0044D4F5`;
  subtraction at `0x004A39C3`/`0x004A39DD` and multiplication from
  `0x004A3A22` independently establish renderer-side world-to-view-like use.

### Source update and selection

- `0x0041ADF0` reads live Flik coordinates `0x0059D910`/`14`/`18`, performs
  Flik-relative arithmetic, smooths position/target fields at
  `0x0041B486`-`0x0041B4B6`, and updates wrapped angle-like values through
  `0x0041B5C0`.
- `0x0041B7D0` tests bit 0 of `0x0059A5EE`. The clear branch copies
  `0x0059DD90`/`0x0059DDA8` into common `0x00599C90` at
  `0x0041B8C0`-`0x0041B906`; the set branch calls
  `0x0041ACC0` and copies `0x0059A5C0`/`0x0059A5E4` at
  `0x0041B920`-`0x0041B966`.
- Main ordering is exact: `0x00414580` calls `0x0041B7D0`, then
  `0x0041458A` calls `0x00455710` with common block `0x00599C90`.

The instructions Confirm two source layouts, selection, Flik-relative source
arithmetic, and the renderer join. “Ordinary follow” and “scripted/setpiece”
remain Inferred roles. The second `0x0043D486 -> 0x00455710` caller's purpose
remains Unknown.

### Corrected adjacent boundaries and counts

- `0x00405FE0` performs the signed 3x3 fixed-point point transform locally
  beginning at `0x0040605F`; it does not merely receive upstream-transformed
  vertices.
- Thunk `0x00401D66 -> 0x00405FE0` has exactly 12 direct calls:
  `0x0044E071`, `0x0044F99D`, `0x00450F3D`, `0x00451B4D`,
  `0x00452B62`, `0x0045377C`, `0x00454199`, `0x00454CDE`,
  `0x004570B2`, `0x004579DE`, `0x004A3E65`, and `0x004A4652`.
  Function `0x0045A7F0` is not among them; indirect callers remain Unknown.
- Viewport structure population/submission is
  `0x00423EDE`-`0x00423F43`, within create/add/setup
  `0x00423E73`-`0x00423F71`. Rejected `0x00423E93` and `0x00423F55`
  are operand bytes, not instruction addresses.
- Only the three reviewed submissions at `0x004047E9`, `0x00405816`, and
  `0x0040598B` are established as `D3DVT_TLVERTEX`; no universal Direct3D
  view-state absence is claimed.
- Thunk `0x00401659 -> 0x004AC460` has exactly seven direct terrain-query
  calls. Three are mapped, leaving four unmapped enclosing functions; exactly
  two of those four read Flik position. Neither query argument is thereby
  promoted to Flik's live point.

## Cross-port and coverage disposition

XPORT-004 remains pinned to registered PS1 commit
`1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51` and committed relative paths.
PS1 evidence confirms no PC fact. Manual-control behavior remains an open
candidate discrepancy under KU-066, not a claimed port difference.

The direct PC renderer join is enough for **Bounded** Camera coverage.
**Mapped** would be false precision because source semantics, selector
meaning, PC controls, second-consumer purpose, update frequency, visual
causality, D3D state beyond the three known submissions, and indirect paths
remain open.

## Validation

- The exact retail executable rehashed to
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Native evidence reproduced under GNU `objdump -d -Mintel`; exact call
  censuses were independently checked, with an aligned radare2 disassembly
  cross-check.
- `make check` reported Vault `468 notes, 0 errors, 0 warnings`, five valid M4
  hash anchors, `648 passed`, and tracked-file audit `0 violation(s)`.
  The suite observation remains qualified by open KU-065 and is not an
  unqualified clean gate.
- After acceptance propagation, a second direct raw-log gate at SHA-256
  `59645e7b70c96de104b2796121299898491e4072878d1b02009f50495d2d5d2b`
  reported Vault `470/0/0`, the same five anchors, `648 passed in 17.69s`, and
  tracked audit 0. This observation carries the same KU-065 qualification.
- `git diff --check 0238ccc 0336d14` passed. The subject delta was exactly 16
  Markdown/static-evidence files, and final `git status --short` was empty.

## Resulting action

Lift DEC-134's temporary Untouched freeze, promote Camera to Bounded, link
this audit from EXP-164 and the camera dossier, and retain KU-066 unchanged as
the semantic/runtime boundary.
