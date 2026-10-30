---
type: experiment
id: EXP-20260817-184
date: 2026-08-17
question: 'Do the corrections applied after EXP-183 hold, and does the input census stand at its documented boundary?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline audit; GNU objdump 2.46; radare2 5.9.8; no runtime, debugger, or target write
environment_version: objdump 2.46-3.fc44
working_directory: /home/dev/ABLPC
configuration: fresh-context audit at clean HEAD 52a9024; read-only toward game media and originals; git history inspected; nothing committed or modified by the auditor
artifacts:
  - static/exports/BIN-97c95ba5572dce63/SUBSYS-input-static-census.md
addresses:
  - "0x0042F350"
  - "0x0042EBC0"
  - "0x00401DF2"
  - "0x004AFEA8"
  - "0x0042F077"
file_offsets: []
result: accept-zero-defects-input-row-bounded
created: 2026-08-17T10:30:00
updated: 2026-08-17T10:30:00
tags:
  - re/experiment
  - re/audit
  - re/input
  - research/coverage
---

# EXP-20260817-184 - Third independent input census audit

## Verdict

**ACCEPT** at `52a9024`. **Zero defects.**

Every numeric and completeness claim was recomputed from the binary rather than
read from the text, and all of them came out exactly as stated: the 46/24/22
store census, both eleven-address blocks, the `0x18`-stride array and its
eleven pairwise inverse mappings, both dispatcher arms, both function extents,
both GUIDs, both `DIDATAFORMAT`s, every vtable offset, the twelve binding pairs
and DIK names, the direction jump/byte tables, the eight-iteration button loop,
the dead-thunk claim, the eight `call esi` sites, and the §0 ten-address
negative re-run against the correct parent tree `0f69566` (504 Vault notes, 43
exports, 0 hits).

Both of the second audit's required corrections landed and are correct in the
binary: `0x0042F38D` is the real store address, and `0x00598B14` is now
documented as read at `0x0042F4C5` and `0x0042F543`.

**The new block-A caveat — the highest-risk text in the audited commit, because
the correction pass wrote it — is independently true.** `0x00401DF2` has zero
call sites and zero data occurrences, and no branch anywhere enters block A
except that thunk.

**Every cited address in the `.text` range resolves to a real instruction
start.** The auditor checked all 140 distinct such addresses across the export,
both dossiers and all three experiment notes, with five correctly-explained
exceptions: `0x0042EED0` (documented as a byte table), `0x0042F42A`
(documented as an end byte), and `0x0042F38E`/`0x0042F428`, which appear only
inside audit-note descriptions of the values being rejected.

## Findings beyond the packet's own claims

Two of the packet's "only" statements were verified **beyond** their stated
scope: `0x00598BC8` has exactly two writers image-wide (`0x0042F35F` zero,
`0x0042F49F` one) and `0x00598B1C` exactly two (`0x0042F359`, `0x0042F558`).
`0x004AFEA8` was confirmed as `jmp [0x00864508]` with `0x00864508` the
`DirectInputCreateA` IAT slot, and `0x0042F43D` its only reference. The
enumeration callback's write of `0x00598B14` was located at `0x0042F077`.

Vault-lint arithmetic reconciles end to end: 504 parent-tree notes + 4 + 2 + 2
= 512.

## Minor findings, all applied

An ownerless quoted gloss in §0, now attributed. The preamble's `.data`
sentence was over-broad — `.idata`, `.rsrc` and `.reloc` lie above
`0x004ED400` and do have file content — now scoped, with `0x0086478C`
identified as an `.idata` IAT slot. "mentions every address used here" for
`ghidra-evidence.json` is now "every **principal** address", since 64 of the
export's intra-function instruction addresses are absent from it — an error
that had over-conceded prior art. The direction table's "all other 0x71
indices" is now "the remaining 0x6D of the table's 0x71 indices". §7's hedge on
the enumeration callback is tightened to record the `0x0042F077` write.
`Environment Status`'s bullet head said "a fourth time" while reporting five.
`KU-070`'s title still asked whether the bindings are remappable, which its own
Known section answers. The block-A caveat had reached only §3.1, `EXP-183` and
Current State; it is now in `KU-070`, `EXP-181` and the Subsystems MOC. The
`DIK_TAB` slot is now described 0-based in both places.

## Scope answers

- **Bounded is correct for Input.** Mapped reserves itself for a model with
  cited static **and runtime** evidence; this packet has none and says so in
  §7, both dossiers' Dynamic-evidence sections, `KU-070`'s impact boundary and
  `EXP-181`.
- **The §0 prior-art and novelty boundary is honest.** The negative re-derives
  against the correct parent tree, the anchors are credited, §5 is labelled
  restatement, and `ghidra-evidence.json` is separated as generated prior art
  with its addresses genuinely present. Both blemishes erred *against* the
  packet's own novelty.
- **Both extents are exactly correct**, and although undocumented material
  exists inside each — `0x0042F365`-`0x0042F377` and `0x0042F42B`/`0x0042F431`
  in the bring-up, and the tail `0x0042ED8E`-`0x0042EEB7` in the per-frame read
  — the auditor checked each against every negative the packet states and
  **none is falsified**. The round-2 failure mode does not recur.
- **Every correction the second audit required landed**, verified in the binary
  and by sweep for stale text. Every surviving occurrence of corrected wording
  is historiography inside a defect description, never a live claim.

## Limitations of this audit

Entirely static and offline. The DirectInput constants, the three vtable
layouts and the `DIJOYSTATE` field order were checked against documented values
from knowledge; no `dinput.h` exists on this host, though the `DIJOYSTATE`
layout is self-confirmed by the binary. The §3.1 store census is exhaustive
only over accesses whose address appears as a 4-byte immediate or displacement;
a store through a computed pointer would not be caught, as §7 concedes. The
enclosing functions of `0x00464E1C`/`0x0049BDB7`, the consumers of
`0x00598B10`, `0x005988E0`, the full extents and callers of `0x00430C30`,
`0x00430B10` and the function containing `0x00431013`, the `0x18`-stride record
layout beyond its first byte, and the two `movzx` readers were not analysed.

## Hygiene

`make vault-lint` 512 notes / 0 errors / 0 warnings; `make audit-tracked` 0
violations; `make test` **686 passed** of denominator **686**, single run. The
intermittent `KU-065` node did not fire for this auditor, and the packet's own
three-run record (1 failed / 685 passed, then 686, then 686) is correctly
recorded as the fifth recurrence, with the recording-anchor phase correctly
identified as new to a canonical suite.

## Disposition

The packet is **accepted** at its documented boundary:

- **Input** stands at **Bounded**;
- `KU-070` keeps every runtime and control-name claim closed, and now records
  that the controls are configurable with block B as the demonstrated path;
- no milestone status changes, and M5 stays where `EXP-20260816-171` left it.

Three fresh contexts re-derived the analysis. The two rejections were a false
completeness claim that concealed a real finding — the configuration path — and
two address-level claims introduced by its correction. The identifier layer,
both extents and the §0 novelty boundary reproduced at every round.
