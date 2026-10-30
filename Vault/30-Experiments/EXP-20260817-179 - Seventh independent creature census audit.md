---
type: experiment
id: EXP-20260817-179
date: 2026-08-17
question: 'Do the corrections applied after EXP-178 hold, and does the creature census survive a seventh independent re-derivation?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline audit; GNU objdump 2.46; radare2 5.9.8; no runtime, debugger, or target write
environment_version: objdump 2.46-3.fc44
working_directory: /home/dev/ABLPC
configuration: fresh-context audit at clean HEAD f13da89; read-only toward game media and originals; git history inspected; nothing committed or modified by the auditor
artifacts:
  - static/exports/BIN-97c95ba5572dce63/SUBSYS-creature-actor-static-census.md
addresses:
  - "0x0041E1A8"
  - "0x0041E845"
  - "0x0041E369"
file_offsets: []
result: reject-audit-history-self-description-only-analysis-and-rows-survive
created: 2026-08-17T05:30:00
updated: 2026-08-17T05:30:00
tags:
  - re/experiment
  - re/audit
  - re/actors
  - research/coverage
---

# EXP-20260817-179 - Seventh independent creature census audit

## Verdict

**REJECT** at `f13da89`.

The analysis layer is flawless for a seventh time, and this round verified it
more finely still: all 69 branch targets land not only on instruction
boundaries but **inside their own script**; the `+0x5C` enumeration is exactly
21 after checking every rebased base register in all five functions for other
forms (the four `[esi-0xe]` sites in `0x0041EC40` are the only non-obvious
ones); `+0x40` is exactly the ten listed stores; the ten further condition-slot
uses from `0x0041E369` are exactly ten; and §10's "more than half" computes to
1,694/3,046 = 55.6%.

**The prior-art and novelty accounting passed a second time**, including the
now-verbatim third-draft quotation and every draft attribution against
`git show`. Both coverage-row promotions are correct.

All three defects are in the packet's description of **its own audit history**.

## Defects

1. **The Audit history asserted one exception where the record documents two.**
   `EXP-20260816-172` read "Findings were applied in the commit recording each
   one — with **one** documented exception" and "**Every other round's findings
   did land**". `EXP-20260817-177` declared "All six defects and every minor
   are applied"; its first minor was the 3,045→3,046 extent figure, and at
   `2ceef9c` that figure had been applied in the export only —
   `EXP-20260816-172` and Current State still read 3,045.
   `EXP-20260817-178` records exactly this in the same commit ("One minor — the
   extent figure — landed only in the export"). So the register contradicted a
   note written alongside it, in the direction that flattered the packet, and
   it is the register the coverage map delegates to *instead of* carrying
   counts.
2. **`EXP-20260817-177`'s Correction section was never amended**, breaking a
   convention applied to rounds 1-4, and still asserted four things
   `EXP-20260817-178` falsified: that all six defects and every minor were
   applied; that the absence of stale text was verified by search; that the
   rejection counts "cannot go stale again"; and that the coverage map's rule
   list no longer carries a count.
3. **The coverage map's own rule understated the phenomenon it exists to
   catch**: "'All findings applied' is a claim like any other, and it has been
   false here **once**." It has been false twice.

## Minor findings, all applied

The rule-list lead-in said the list "has grown with **every** round"; it did
not grow at rounds 1 or 6. The same rule said "declared **nine defects** fixed;
three were not" — one defect and two minors. Current State said the extent is
3,046 "everywhere", where 3,045 correctly survives in the audit notes as the
recorded superseded figure. The roadmap opened "Rejected **three times** —"
before appending later rounds, so the bolded count read as a total. §0.1's
"arithmetically impossible for **any** endpoint" was stated more absolutely
than derived.

## What survived

Every number, a seventh time, plus the finer checks in the verdict. Also
re-derived independently: the pool extent and stride from both loop
terminations; `0x700`/`0x1C`/64; `380 = 181 + 199` and `199 = 2 + 197`; the
trailing-byte histogram; §3.1's nineteen rows, ten thunks and 9/5/5/17
partition; §3.2's eleven types; §3.3 over 48 entries; all twelve flag bit rows
instruction by instruction including the register provenance of `bl` at
`0x0041ED95` and `0x0041BD17`; the extent with nothing beyond it; four `+0x70`
writers with every gate including `ecx` surviving unclobbered from `0x0041E6C6`
to `0x0041E7EC`; four `[esp+0x4c]` reads and seven writes; four record-index
sites; eight `0x0059B684` sites; nine prior-art artifacts with every quoted
attribution verbatim; the Ghidra character counts and "three, not two"; all six
quoted disassembly blocks byte-exact including the objdump line-wrapped `7f`
byte at `0x0041C486`; reachability with zero stored absolute pointers; all
table extents; the external entry point; and all sixteen file offsets.

## Scope answers

- **Bounded remains correct for Enemies/actors/AI**; Mapped is correctly
  withheld pending `KU-068`.
- **Touched remains correct for Event/scripting.**
- **The §0/§0.0 accounting is honest** — membership, content and self-history.
- **Six of seven experiment notes describe their audits accurately.**
  `EXP-20260817-177` did not (defect 2), and `EXP-20260816-172`'s Audit history
  did not (defect 1).
- **`EXP-20260817-178`'s two defects and five minors all landed as edits**, but
  its replacement text for the Audit history introduced defect 1, and the
  propagation its findings required into `EXP-20260817-177` was not made.

## Limitations of this audit

The region past `0x0041E1A8`, the ten per-type `+0x7C` handlers, the nine
opcode-11 subroutines and the five modes were not analysed; the auditor
verified the packet claims nothing about them and found no sentence implying
more. Caller completeness is rel32 plus whole-file absolute scans, excluding
computed dispatch. `+0x5C` accesses outside the five named functions were
enumerated only for the forms the export names. `0x0059D99E` writer separation
used `ret`-separation rather than full CFG reconstruction. The underlying
correctness of the M2 exports and the cross-referenced results was not
re-verified. No level file was parsed and nothing was run.

## Hygiene

`make vault-lint` 500 notes / 0 errors / 0 warnings; `make audit-tracked` 0
violations; `make test` **686 passed** of denominator **686**, single
invocation, 17.84s, qualified by the open `KU-065`.

## Correction

All three defects and every minor are applied in the commit recording this
audit. The structural change is that `EXP-20260816-172`'s Audit history is now
a **per-round fact table making no global claim** about whether findings
landed: three successive drafts made such a claim and each was falsified by the
next round, so the failure was structural rather than clerical. A row states
what one round found and whether that round's commit applied what it declared;
adding a row is mechanical and cannot be globally wrong. `EXP-20260817-177`
gains the Corrections section its predecessors have, and the coverage map's
rule now says the claim has been false twice and recommends per-item facts over
completeness assertions.

## Corrections to this audit

[[EXP-20260817-180 - Eighth independent creature census audit]] found one
figure in this note's "What survived" section short: the mode slot has **eight**
writes, not seven. The eighth is `0x0041E2E9`
(`mov DWORD PTR [esp+0x50],0x1`), which addresses the same slot only because
`push 0x59d910` at `0x0041E2E4` has displaced `esp` by 4. No `[esp+0x4c]`
search finds it. The four-reads figure is right, and nothing else in this note
is affected — the site writes `1`, consistent with the mode-`> 2` gate this
note verified.
