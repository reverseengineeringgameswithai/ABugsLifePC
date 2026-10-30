---
type: experiment
id: EXP-20260817-178
date: 2026-08-17
question: 'Do the corrections applied after EXP-177 hold, and does the creature census survive a sixth independent re-derivation?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline audit; GNU objdump 2.46; radare2 5.9.8; no runtime, debugger, or target write
environment_version: objdump 2.46-3.fc44
working_directory: /home/dev/ABLPC
configuration: fresh-context audit at clean HEAD 2ceef9c; read-only toward game media and originals; git history inspected; nothing committed or modified by the auditor
artifacts:
  - static/exports/BIN-97c95ba5572dce63/SUBSYS-creature-actor-static-census.md
addresses:
  - "0x0041E1A8"
  - "0x0041E845"
  - "0x0041BB2A"
  - "0x0041E730"
file_offsets: []
result: reject-audit-register-incomplete-and-a-replacement-count-wrong
created: 2026-08-17T04:30:00
updated: 2026-08-17T04:30:00
tags:
  - re/experiment
  - re/audit
  - re/actors
  - research/coverage
---

# EXP-20260817-178 - Sixth independent creature census audit

## Verdict

**REJECT** at `2ceef9c`.

The analysis layer is flawless for a sixth time, and this audit went further
than its predecessors in confirming it: every number re-derived from the bytes
without reference to the text, all six quoted disassembly blocks byte for byte
including the `...` elision in §1.4, the published §6.1 snippet run verbatim,
and two properties nobody had checked before — that the `+0x5C` enumeration is
**exactly 21** instructions with 5 of the interpreter's 10 lying past
`0x0041E1A8` (so "missed half" is exact, not approximate), and that the
interpreter's callee set is exactly ten thunks below `0x0041E1A8` and five
above, none reaching the per-type handler range.

**The §0/§0.0 prior-art and novelty accounting is judged honest** — on
membership, on content, and on its own history. That is the first round at
which that section has passed.

Both defects are in the bookkeeping the fifth round introduced.

## Defects

1. **A wrong count inside the sentence that claims there is no count.**
   `Vault/01-MOCs/Subsystem Coverage Map.md`: "Its **four** audit rounds
   produced the rules below; the list has grown with each round, which is why
   it is no longer introduced by a count". There had been **five** rounds, and
   the list includes a rule `EXP-20260817-177` added. The figure disagreed with
   the roadmap, the Experiments MOC, Current State and `EXP-20260817-177`
   itself. Compounding it, Current State asserted the remedy as accomplished —
   "the rule list is no longer introduced by a count — neither can go stale
   again" — which was false as implemented. This is the previous round's
   defect 5 re-created inside its own fix.
2. **The register that replaced the rejection counts was incomplete and
   self-contradicting.** `EXP-20260817-177`'s structural remedy was to point at
   the packet's own Audit history instead of maintaining counts, and the
   coverage map now does. That target listed only four audits —
   `EXP-20260817-177` appeared nowhere in the file — and its lead-in asserted
   "with all findings applied in the commit recording each one", which
   `EXP-20260817-176`'s Correction section, amended in the same commit,
   explicitly denies.

## Minor findings, all applied

§0.0 quoted the third draft's novelty sentence non-verbatim (it reads "no
earlier export **in this directory** mentions **any of the addresses** …") — in
the section whose subject is accurate attribution. §1.1's "All four earlier
drafts said 'three'" was wrong twice over: there are five earlier drafts, and
drafts 1-2 said "**Two** consumers" while listing three addresses. The extent
read 3,046 bytes in the export but 3,045 in `EXP-20260816-172` and Current
State. §2.2's `+0x40` row said "all four are the stores"; there are **ten**
across the five functions — `0x0041BB2A`, `0x0041BB60`, `0x0041BB7F`,
`0x0041BBA2`, `0x0041BDF8`, `0x0041BE34`, `0x0041E029`, and `0x0041E730`,
`0x0041E785`, `0x0041E791` in the unanalysed region — more than either the
packet or the auditor's own count had. §0.1 said "three drafts got this wrong
in three different ways" while describing two.

## What survived

Every number, a sixth time. Additionally verified to a finer grain than
before: the extent's only `ret` is `0x0041E7D3` and `0x0041E7D4` is referenced
image-wide by exactly two instructions; `0x0041E6E6` has exactly one reference;
`+0x70` has eight references and exactly four writers; `[esp+0x4c]` has four
reads and seven writes; there are exactly four `*4`-scaled record-index sites
and eight `0x0059B684` sites image-wide; `0x0059D99E` has writers in exactly
eleven other functions; the `FUN_0041dc60` decompilation is 18,101 characters
and `thunk_FUN_0041dc60` 18,205, with `PTR_DAT_004c83f0` appearing twice and
`PTR_DAT_004c8758` six times; and every draft attribution matches `git show`.
The branch-target check was re-derived from the handlers rather than taken from
the text, and all 69 land on boundaries inside their own script.

## Scope answers

- **Bounded remains correct for Enemies/actors/AI.** Mapped would require
  runtime evidence, which the packet disclaims throughout and gates behind
  `KU-068`.
- **Touched remains correct for Event/scripting.**
- **The §0/§0.0 accounting is now honest** on membership, content and
  self-history — the only residue was the non-verbatim quotation above.
- **Five of the six experiment notes describe their audits accurately.**
  `EXP-20260816-172` did not: its Audit history omitted the fifth audit and
  asserted all findings applied (defect 2).
- **Not every correction `EXP-20260817-177` required landed cleanly.** Its
  defects 1, 4, 6 and both halves of 2 landed; defect 3 landed in three
  artifacts but the register it delegated to was incomplete; defect 5 was
  replaced by a different wrong count. One minor — the extent figure — landed
  only in the export.

## Limitations of this audit

The region past `0x0041E1A8`, the ten per-type `+0x7C` handlers, the nine
opcode-11 subroutines and the five modes were not analysed; the auditor
verified the packet claims nothing about them and found no sentence implying
more. Caller completeness is rel32 plus whole-file absolute scans, excluding
computed dispatch. `+0x5C` accesses outside the five named functions were
enumerated only for the forms the export names. `0x0059D99E` writer separation
used ret-separation rather than full CFG reconstruction. The underlying
correctness of the M2 exports was not re-verified — only that each contains the
text attributed to it. No level file was parsed and nothing was run.

## Hygiene

`make vault-lint` 498 notes / 0 errors / 0 warnings; `make audit-tracked` 0
violations; `make test` **686 passed** of denominator **686**, single
invocation, 18.17s, qualified by the open `KU-065`.

## Correction

Both defects and every minor are applied in the commit recording this audit.
The coverage map's rule lead-in now carries **no** number and records both
failed lead-ins instead; the Audit history lists every round and states the one
documented exception plainly; Current State's "cannot go stale again" claim is
retracted. Each edit was re-read and the absence of the stale text verified by
search before the commit, per the rule the fifth round added.
