---
type: experiment
id: EXP-20260817-176
date: 2026-08-17
question: 'Do the corrections applied after EXP-175 hold, and does the creature census survive a fourth independent re-derivation?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline audit; GNU objdump 2.46; radare2 5.9.8; no runtime, debugger, or target write
environment_version: objdump 2.46-3.fc44
working_directory: /home/dev/ABLPC
configuration: fresh-context audit at clean HEAD 1c499bf; read-only toward game media and originals; nothing committed or modified by the auditor
artifacts:
  - static/exports/BIN-97c95ba5572dce63/SUBSYS-creature-actor-static-census.md
addresses:
  - "0x0041519B"
  - "0x004151B0"
  - "0x0041E3D7"
  - "0x0041E6C6"
  - "0x0041E7FE"
  - "0x0041E46E"
file_offsets: []
result: reject-accounting-layer-only-analysis-and-both-row-promotions-survive
created: 2026-08-17T02:30:00
updated: 2026-08-17T02:30:00
tags:
  - re/experiment
  - re/audit
  - re/actors
  - research/coverage
---

# EXP-20260817-176 - Fourth independent creature census audit

## Verdict

**REJECT** at `1c499bf`, on the accounting layer alone.

The numeric core reproduced for the fourth time: all 26 opcode PC advances
re-derived from raw handler bytes before reading §5.2, then 463 instructions,
zero misalignments, 69 branch instructions, zero off-boundary targets, and a
digit-identical histogram — plus every switch table, both loop terminations,
the `380 = 181 + 199` and `199 = 2 + 197` splits, the trailing-byte histogram,
the boolean table, every file offset and every thunk. The published §6.1
snippet runs verbatim. This audit also confirmed, for the first time, that
**all six quoted disassembly blocks match objdump byte for byte** — the defect
class that had recurred in each of the three previous rounds is closed.

The extent correction from `EXP-20260817-175` was independently verified:
exactly one `ret` in `0x0041DC60`-`0x0041E845`, `0x0041E7D4` entered only from
`0x0041E6CD`/`0x0041E6D8`, leaving by `jmp 0x41e6e6` at `0x0041E841` whose
last byte is `0x0041E845`, `mov edi,edi` padding at `0x0041E846`, dispatch
table decoding cleanly from `0x0041E848`. **Nothing extends further.** The four
`+0x70` writers are four and only four. §2.2.1's flag *enumeration* is complete
and every cell correct. The nine-artifact prior-art membership list and every
attribution quoted in §0 were verified individually and are right.

What failed is arithmetic, counting and attribution — in the very sections
whose subject is honesty about scope and prior art.

## Defects

1. **A wrong derived percentage.** §0.1 said the first two drafts read "under
   40%". `0x0041E1A8 - 0x0041DC60 = 1,352` of the extent's `3,045` bytes is
   **44.4%**; no endpoint choice yields under 40%. It also disagreed with four
   artifacts that said 45% (a figure computed against the superseded extent),
   and with the export's own §10, which calls the remainder "more than half".
2. **An unreproducible site count.** §2.2.1 said "Thirteen sites in total".
   The table distinguishes twelve bits and names 31 addresses; the binary has
   **21 distinct instructions** touching `+0x5C`/`+0x5D` across the five named
   functions. No reading yields thirteen. The figure had propagated to
   `EXP-20260817-175`, `EXP-20260816-172`, Current State and the roadmap.
3. **The third draft's errors attributed to the second.** §0's parenthetical
   and §0.0's opening blamed "the second draft" for the eight-file prior-art
   list and the "no earlier export mentions …" claim. Both first appear in
   `3f0debd`, the **third** draft — the first two carry a three-export list and
   neither contains that sentence. §0.1 of the same document and the coverage
   map both said "the third", so the export contradicted itself inside its own
   prior-art section.
4. **The generated Ghidra export was understated, in the flattering
   direction.** §0.0 said its decompilation renders "both extra program-counter
   advances". It renders **three**, the third being
   `if (2 < param_3) { … piVar8[0x1c] = piVar8[0x1c] + 2; }` — precisely the
   `0x0041E7FE` writer that `EXP-20260817-175` presented as its own discovery
   and that this packet had described as newly recorded. It was already in the
   generated artifact, guard and all.
5. **An incomplete enumeration over the swept extent.** §5.3 said the mode slot
   `[esp+0x4c]` is read at `0x0041E1A8` and `0x0041E214`. It is read at
   **four** sites — those two plus `0x0041E3D7` and `0x0041E6C6` — and the last
   is the load §5.1's own writer table cites by address.
6. **Stale text left after a withdrawal.** `KU-069` still called `0x005C5860`
   the "**64-entry**" table in the same bullet that says the clear bounds the
   zeroed region rather than the extent, and
   `FUNC-97C95BA5572D-0041C420` still said "the 64-entry table". §1.4 had
   applied the restatement; two artifacts had not.
7. **A superseded extent asserted as fact.** `EXP-20260816-173`'s appended
   correction section still stated "the function runs to `0x0041E7D3`" without
   qualification, and `EXP-20260817-175`'s Correction section did not list that
   note among the artifacts it touched.
8. **A self-contradictory sentence naming a non-existent instruction.**
   `EXP-20260816-172`'s Confirmed register read "runs to its only `ret` at
   `0x0041E845` — its only `ret`, at `0x0041E7D3`, is not the end".
   `0x0041E845` is not a `ret`; it is the last byte of the `jmp` at
   `0x0041E841`.
9. **An under-count of record-index sites.** §1.1 said "Three sites reach a
   record by index". `0x0041519B` performs the identical arithmetic with
   different registers and immediately reads the resulting record's `+0x5C` at
   `0x004151B0` — a fourth site, and another `+0x5C` reader outside the five
   analysed functions.

## Minor findings, all applied

Source `+0x1A` is read at `0x0041E46E` and appeared in no field table. §5.1's
entry condition for `0x0041E2E1` listed only the pending-opcode test, where the
path also requires flag bit `0x0002`, mode `< 3`, `word[0x0059DD80] == 0` and
the source `+0x16` distance test. Opcode 14 uses only the operand's low byte.
The export called the tail's five states "movement modes" while
`EXP-20260816-172` registers what they do as Unknown. The scope note's
`0x00572000` `.bss` threshold is not the real boundary — `.data`'s raw content
ends at `0x004ED400`. The Experiments MOC narrates `EXP-20260817-174` with the
superseded extent immediately below the bullet that corrects it.

## What survived

Everything numeric, a fourth time, and every structural correction from the
three prior rounds: the pool extent and stride from both loop terminations; the
source table, `0x700` copy and type-`0x23` gate; the `CreatListRam` string at
its site; builder, update and interpreter reachability with zero absolute
references; §1.3's nine builder steps; all four `KU-069` indexes with
`type = 65` landing exactly on `0x00599EB0`; §3.1's nineteen rows, ten thunks
and 9/5/5/17 partition; §3.2's eleven non-default types; §3.3 over 48 entries;
§4's 28 pointers, histogram and special values; the complete instruction-size
map; the 40 programs, extent, totals, histogram and both listings; the external
entry point; §5.3's dispatch tables; §5.4's nine subroutines; `call eax` at
`0x0041E7C7` as the only register-indirect call in the five functions; §7's
formulas; §8's `0x3E6` gate; `0x004C7970` at zero references; exactly five
`EVENT` strings; the eight `0x0059B684` absolute-form sites; and the
nine-artifact prior-art list with every attribution verified line by line.

The auditor also confirmed the packet genuinely claims nothing about the
per-type handlers, the opcode-11 subroutines or the five modes, and that
§2.2's field list covers every `[esi+disp]` offset the interpreter touches.

## Scope answers

- **Bounded remains correct for Enemies/actors/AI.** Every row anchor
  reproduced; no defect touches one.
- **Touched remains correct for Event/scripting.**
- **The prior-art accounting is now correct on membership and attribution of
  content, but was still wrong on which draft made which error, and still
  understated the generated export.** Both are fixed here.
- **`EXP-20260817-174` describes its audit accurately**, including its appended
  corrections. **`EXP-20260816-173` was accurate except for the superseded
  extent in its appended section** (defect 7). **`EXP-20260817-175` is accurate
  on its findings**, but its "thirteen sites" and "both extra advances" are
  wrong; both are corrected in that note.

## Limitations of this audit

What the region past `0x0041E1A8` computes, the ten per-type `+0x7C` handlers,
the nine opcode-11 subroutines and the five modes were not analysed. `+0x5C`
accesses outside the five named functions were checked exhaustively only for
the `0x0059B684` absolute form. Caller completeness is rel32 plus whole-file
absolute scans, excluding computed dispatch by construction. The
cross-referenced results `EXP-20260815-128`, `EXP-20260816-153`,
`EXP-20260816-165`, `EXP-20260816-155`/`KU-064` and `EXP-20260815-129` were not
re-verified. No level file was parsed and nothing was run.

## Hygiene

`make vault-lint` 494 notes / 0 errors / 0 warnings; `make audit-tracked` 0
violations; `make test` **686 passed** of denominator **686**, single
invocation, 17.95s. The figure keeps its `KU-065` qualification — three prior
independent recurrences of the same `anchor_timeout` / `NextLife.` node — and
neither closes that unknown nor may be cited as an unqualified gate.

## Correction

The findings were applied in the commit recording this audit — but **not all
of them**, as [[EXP-20260817-177 - Fifth independent creature census audit]]
established. Three were declared applied and were not:

- **defect 8 was not fixed.** The edit re-anchored the sentence's second half
  and left "runs to its only `ret` at `0x0041E845`" in place, so the note
  still named a `ret` at an address holding the last byte of a `jmp`, and
  still contradicted itself two lines later;
- the dossier's "movement modes" wording, listed here as a minor, was not
  changed, leaving a withdrawn interpretation asserted at
  `status: confirmed, confidence: high`;
- the Experiments MOC's stale narration of `EXP-20260817-174`'s extent was
  likewise untouched.

The lesson is recorded rather than smoothed: "all findings applied" is itself
a claim, and this packet has now had it be false once. Verify each edit landed
before asserting it. No derived number in the analysis changed, because none
was wrong.
