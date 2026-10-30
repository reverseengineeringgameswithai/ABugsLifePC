---
type: experiment
id: EXP-20260817-183
date: 2026-08-17
question: 'Do the corrections applied after EXP-182 hold, and does the input census survive a second independent re-derivation?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline audit; GNU objdump 2.46; radare2 5.9.8; no runtime, debugger, or target write
environment_version: objdump 2.46-3.fc44
working_directory: /home/dev/ABLPC
configuration: fresh-context audit at clean HEAD afee530; read-only toward game media and originals; git history inspected; nothing committed or modified by the auditor
artifacts:
  - static/exports/BIN-97c95ba5572dce63/SUBSYS-input-static-census.md
addresses:
  - "0x0042F38D"
  - "0x00598B14"
  - "0x0042F4C5"
  - "0x0042F543"
  - "0x00401DF2"
file_offsets: []
result: reject-two-address-level-claims-corrected-substance-fully-reproduced
created: 2026-08-17T09:30:00
updated: 2026-08-17T09:30:00
tags:
  - re/experiment
  - re/audit
  - re/input
  - research/coverage
---

# EXP-20260817-183 - Second independent input census audit

## Verdict

**REJECT** at `afee530`, on two false address-level claims. The substance —
including the whole §3.1 correction the previous round required — reproduced in
full.

The auditor independently re-derived §3.1 from a byte-level scan: **62**
little-endian occurrences of an address in `[0x004D8430, 0x004D8490)`
image-wide, all in `.text`, none as data — 46 stores (24 in `0x0042F0F0`, 11 in
block A, 11 in block B), the 11 byte reads at `0x00430B10`, 3 loop/table
references and 2 `movzx` reads. **No hidden writer of any kind.** Both blocks
source `0x004D9CF9` through `0x004D9DE9` at `0x18` stride, both write the same
eleven of twelve scancode slots, never a mask slot, always excluding
`0x004D8480`; the eleven inverse read/array pairs were checked pairwise; and
the dispatcher's two arms were confirmed to reach the defaults thunk and
`0x00430B10` respectively.

Also reproduced: both GUIDs, both `DIDATAFORMAT`s and their flag names, every
vtable offset, both cooperative levels, both function extents by whole-image
branch analysis, the twelve binding pairs, the direction jump/byte tables with
only four masks passing the bound check, the eight-iteration button loop, the
dead-thunk claim in full, every quoted disassembly block byte for byte, and the
§0 ten-address novelty negative re-derived from scratch at the parent tree.

## Defects

1. **`0x0042F38E` does not exist.** Export §4's store-order parenthetical cited
   it; the store to `0x004D84C4` is at `0x0042F38D`, since `0x0042F388` is a
   five-byte `a3` store. The export contradicted itself — its own §1.1 block
   quotes `42f392`, which a five-byte store at `0x0042F38E` could not precede.
   This line was **added by the previous correction pass**, inside the sentence
   written to fix that audit's defect 4.
2. **"`0x00598B14` … not read here" was false and internally contradicted.**
   §1.5 said so; the address is read twice inside the stated extent, at
   `0x0042F4C5` and `0x0042F543`, and §1.4 of the same document already stated
   that the device loop runs while `edi < [0x00598B14]`. An unhedged negative
   written over a range that was read — the exact failure mode the previous
   correction pass names as its own lesson.

## Minor findings, all applied

The `0x0042F350` dossier gave the joystick-pair store span as
`0x0042F388`-`0x0042F428`; the last store starts at `0x0042F421` and ends at
`0x0042F42A`. §0's `EXP-20260816-159` quotation silently elided
`` `0x0042F350` ``. The novelty negative was described as covering 508 Vault
notes; the parent tree `0f69566` has 504 — 508 is the count at the audited
commit, which would have included the packet's own notes. `Environment Status`
said two distinct `KU-065` suite denominators where the register shows three
(648, 682, 686). The Subsystems MOC's Input block was the one artifact that had
not received the §3.1 correction. The `DIK_TAB` slot is described 0-based in
the export and 1-based in the experiment note.

## A scoping refinement, not a defect

Block A (`0x00430C3F`-`0x00430CBC`) is reached only through thunk
`0x00401DF2`, and that thunk has **zero** call sites and zero data occurrences
in the image, so block A's reachability is unestablished. The remappability
conclusion rests on block B — live off the dispatcher — and on `0x00430B10`.
§3.1 now records this caveat explicitly.

The auditor also noted that the undocumented tail `0x0042ED8E`-`0x0042EEBB`
(joystick axis handling, `0x00598BB4`, and a second write of
`0x004F0440`/`0x004F0444` at `0x0042EEA5`/`0x0042EEAA`) falsifies **nothing**,
because the packet asserts no exclusivity over those writers — and that the
vtable-offset and callee lists for both functions are in fact complete as
stated.

## Scope answers

- **Bounded remains correct for Input**; Mapped requires runtime evidence,
  which the packet disclaims throughout.
- **The §0 prior-art and novelty boundary is honest** — re-derived from scratch
  at the parent tree, 0 hits for all ten addresses, with
  `ghidra-evidence.json` correctly separated as generated prior art. The only
  blemish was the unmarked two-token elision above.
- **Both extents are exactly right**, verified by whole-image branch analysis.
  One thing inside `0x0042F350`'s extent falsified a stated negative — defect 2.
- **All six of the previous audit's defects landed**, verified in the binary and
  the text. Four of its five minors landed cleanly; the verbatim-quotation
  minor landed only partially.
- **The `KU-065` and `Environment Status` records are accurate** against
  `git log`: `102de05` exists in the reflog asserting a passing suite,
  `afee530` is the amend that corrects it, and the amend diff touches exactly
  the three recording files. Only the denominator count was off.

## Limitations of this audit

Entirely static and offline. The DirectInput constants, GUIDs, `DIJOYSTATE`
layout and vtable orders were checked against documented values from
knowledge; no `dinput.h` exists on this host. The enclosing functions of
`0x00464E1C`/`0x0049BDB7`, the enumeration callback, `0x005988E0`, the
consumers of `0x00598B10`, and the full extents and callers of `0x00430C30`,
`0x00430B10` and the function containing `0x00431013` were not analysed.
Computed dispatch was not exhaustively excluded.

## Hygiene

At the audited commit `afee530`: `make vault-lint` 510 notes / 0 errors / 0
warnings; `make audit-tracked` 0 violations; `make test` **686 passed** of
denominator **686**, single run. The intermittent `KU-065` node did not fire
for this auditor.

**During the correction pass**, three consecutive runs gave `1 failed, 685
passed` / `686 passed` / `686 passed`. The failure was the `KU-065` node in its
**recording-anchor** phase — a phase previously seen only in `EXP-20260816-170`'s
isolated runs, not in a canonical suite. Recorded as the fifth recurrence in
`KU-065` and [[Environment Status]], with the raw log retained. Every passing
figure remains qualified.

## Correction

Both defects and every minor are applied in the commit recording this audit.
Each edit was re-read and the absence of the stale text verified by search
before the commit.
