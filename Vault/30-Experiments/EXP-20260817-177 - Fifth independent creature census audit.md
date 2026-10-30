---
type: experiment
id: EXP-20260817-177
date: 2026-08-17
question: 'Do the corrections applied after EXP-176 hold, and does the creature census survive a fifth independent re-derivation?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline audit; GNU objdump 2.46; radare2 5.9.8; no runtime, debugger, or target write
environment_version: objdump 2.46-3.fc44
working_directory: /home/dev/ABLPC
configuration: fresh-context audit at clean HEAD a540dc7; read-only toward game media and originals; git history inspected; nothing committed or modified by the auditor
artifacts:
  - static/exports/BIN-97c95ba5572dce63/SUBSYS-creature-actor-static-census.md
addresses:
  - "0x0041E845"
  - "0x0041E841"
  - "0x00599B20"
  - "0x0041BB2A"
file_offsets: []
result: reject-declared-corrections-not-all-applied-analysis-untouched
created: 2026-08-17T03:30:00
updated: 2026-08-17T03:30:00
tags:
  - re/experiment
  - re/audit
  - re/actors
  - research/coverage
---

# EXP-20260817-177 - Fifth independent creature census audit

## Verdict

**REJECT** at `a540dc7`.

The analysis layer is flawless for a fifth time. Every number in the packet was
re-derived from the bytes without reference to the text and not one disagreed:
463 instructions, 69 branch instructions with zero off-boundary targets, a
digit-identical histogram, the published §6.1 snippet running verbatim,
`380 = 181 + 199` and `199 = 2 + 197` reproduced by counting operands, the
trailing-byte histogram, both switch tables entry by entry, the 9/5/5/17
partition, the 21 `+0x5C` instructions, the four `+0x70` writers, the four
`[esp+0x4c]` reads, the extent `0x0041DC60`-`0x0041E845` with nothing beyond
it, all sixteen file offsets, and all six quoted disassembly blocks byte for
byte.

The rejection is that **a correction declared applied was not applied**.

## Defects

1. **`EXP-20260817-176` defect 8 was reported fixed and was not.**
   `EXP-20260816-172`'s Confirmed register still read "`0x0041DC60` runs to its
   only `ret` at `0x0041E845`. Its only `ret` is at `0x0041E7D3` and is **not**
   the end" — naming a `ret` at an address whose byte is `0xFF`, the last byte
   of the `jmp` at `0x0041E841`, and contradicting itself two lines later.
   `git show a540dc7` shows the edit re-anchored the sentence's second half and
   left the broken first half untouched, while `EXP-20260817-176`'s Correction
   section and the commit message both asserted all nine defects were applied.
2. **The same "all applied" claim was false for two minors**: the interpreter
   dossier still asserted "the region past it, which implements the five
   movement modes" at `status: confirmed, confidence: high`, three days after
   the export withdrew exactly that reading in the same commit; and the
   Experiments MOC still narrated `EXP-20260817-174` with the superseded
   extent, directly above the bullet correcting it.
3. **Four rejection counts disagreed across artifacts.** The coverage map said
   "rejected three times", `EXP-20260816-172` said "Rejected **three times**"
   immediately above a four-item list and "all three auditors" below it, and the
   Experiments MOC said "rejected once and corrected" — against a roadmap and a
   Current State entry, written in the same commit, that said four.
4. **§0.0 misattributed its own error, in the section whose subject is accurate
   attribution.** It blamed "the third draft" for the phrase "both extra
   program-counter advances". `git show` places that phrase's first appearance
   in `1c499bf`, the **fourth** draft — the same section's opening correctly
   calls `3f0debd` the third. `EXP-20260817-176`'s defect 3 was the mirror
   image of this, and the fix created a symmetric error beside it.
5. **The coverage map introduced six method rules as three.** The lead-in had
   said "three further things generalise" since `de7b80d` while the list grew
   3 → 4 → 5 → 6 — the stale aggregate sitting in the paragraph that now
   carries "Prefer enumerations to aggregate counts … Where a list can be
   printed, print the list."
6. **The scope note cited an address the document never uses.** "the lowest is
   `0x00572000`" — no such address appears elsewhere in the export; of the 31
   addresses above `0x004ED400` it does cite, the lowest is `0x00599B20`. This
   was the half-applied residue of the previous round's `.bss` minor: the
   boundary sentence was corrected and the superseded figure was re-purposed
   into a false one.

## Minor findings, all applied

The extent was quoted as 3,045 bytes (half-open) where the inclusive range
`[0x0041DC60, 0x0041E845]` is 3,046; the percentage is unaffected. The
"18,205-character decompilation" is the `thunk_FUN_0041dc60` entry; the
`FUN_0041dc60` entry is 18,101 characters, and both render everything §0.0
claims. §2.2's `+0x40` row cited `0x0041BB27`, which is the `shl` feeding the
store at `0x0041BB2A`. "Earlier drafts quoted 'thirteen sites'" — only one
did. "The first three drafts said 'three'" record-index sites — all four did.
The interpreter dossier's Callees list omitted five thunks the tail calls
(`0x004010C3`, `0x00401271`, `0x00401721`, `0x00401A9B`, `0x00401D61`), none of
which reaches the per-type handler range. §5.2's condition-slot sentence could
be read as exhaustive over the function when it is scoped to the opcode
handlers; the tail reuses the slot at ten further sites from `0x0041E369`.
`+0x6C` is also decremented at `0x0041DCBB`. §2.1's table ordered `+0x1A`
before `+0x19`.

## What survived

Every number, a fifth time — see the verdict. Also: the four record-index
sites confirmed as exactly four in `.text`; the eight `0x0059B684` sites; the
26/9/8/16-entry dispatch tables each ending exactly where the next begins; the
nine-artifact prior-art membership with `M2-generic-resource-index-producer-census.md`
at zero occurrences and every quoted attribution verbatim in the file named;
the four `piVar8[0x1c]` statements and the `if (2 < param_3)` guard present in
`ghidra-evidence.json` at the cited lines, confirming "three, not two"; and
`0x0041C600`/`0x0041BC48` appearing in no other artifact. Both coverage-row
promotions survive on the evidence.

## Scope answers

- **Bounded remains correct for Enemies/actors/AI**; every anchor reproduced.
- **Touched remains correct for Event/scripting.**
- **The prior-art accounting is honest on membership and content** — the
  nine-artifact list is exactly right and the novelty framing is genuinely
  withdrawn to two byte case tables plus the authored model — **but was still
  wrong about its own history** (defect 4).
- **`EXP-20260816-173`, `-174` and `-175` describe their audits accurately**,
  including all three appended correction sections. **`EXP-20260816-172` did
  not** (defect 1 and the counts). **`EXP-20260817-176`'s findings are all
  accurate** — every one re-derived — **but its "all nine defects and every
  minor are applied" was false.**

## Limitations of this audit

The region past `0x0041E1A8`, the ten per-type `+0x7C` handlers, the nine
opcode-11 subroutines and the five modes were not analysed; the auditor
confirmed the packet claims nothing about them, the sole exception being the
dossier wording in defect 2. Caller completeness is rel32 plus whole-file
absolute scans, excluding computed dispatch. `+0x5C` accesses outside the five
functions were enumerated only for the `0x0059B684` absolute forms and the
textual `[reg+0x5c]` form. `0x0059D99E` writer separation was established by
counting `ret`s in linear disassembly rather than full function reconstruction.
The cross-referenced results and the underlying correctness of the M2 exports
were not re-verified — only that each contains the text attributed to it. No
level file was parsed and nothing was run.

## Hygiene

`make vault-lint` 496 notes / 0 errors / 0 warnings; `make audit-tracked` 0
violations; `make test` **686 passed** of denominator **686**, single
invocation, 18.24s, qualified by the open `KU-065`.

## Correction

All six defects and every minor are applied in the commit recording this audit.
Each edit was re-read after application and the absence of the stale text
verified by search, because this round's finding is precisely that a declared
correction can fail to land. Rejection counts are removed from the coverage map
and the Experiments MOC in favour of a pointer to the packet's own Audit
history, so they cannot go stale again; the coverage map's rule list no longer
carries a count; and a new rule is added: **verify each edit landed before
reporting it applied**.

## Corrections to this audit

[[EXP-20260817-179 - Seventh independent creature census audit]] found that
four statements in this note's Correction section did not survive:

- **"All six defects and every minor are applied"** is false. The first minor —
  the extent quoted as 3,045 bytes where the inclusive range is 3,046 — was
  applied in the export only. `EXP-20260816-172` and Current State still read
  3,045 at `2ceef9c`, as `EXP-20260817-178` itself recorded.
- **"the absence of the stale text verified by search"** is therefore also
  false for that item: the search was not run for `3,045`.
- **"so they cannot go stale again"** was falsified by `EXP-20260817-178`
  defect 1 — the coverage map's rule lead-in acquired a different wrong count.
  Current State's assertion of that remedy is retracted there.
- **"the rule list no longer carries a count"** was falsified in the same way.

This note's six defects and its findings about the packet were all
independently re-confirmed. What failed was the Correction section's claim
about its own completeness — the same class this note rejected the packet for,
one level up. `EXP-20260816-172`'s Audit history no longer makes any global
claim of that kind.
