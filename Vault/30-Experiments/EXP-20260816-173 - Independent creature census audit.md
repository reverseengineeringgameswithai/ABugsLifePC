---
type: experiment
id: EXP-20260816-173
date: 2026-08-16
question: 'Does independent review support the creature-census claims - the pool extent, the CreatListRam anchor, the per-type tables, the word-code VM, the decoded program format, and the two coverage-row promotions?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline audit; GNU objdump 2.46; radare2 5.9.8; no runtime, debugger, or target write
environment_version: objdump 2.46-3.fc44
working_directory: /home/dev/ABLPC
configuration: fresh-context audit at clean HEAD de7b80d; read-only toward game media and originals; nothing committed or modified by the auditor
artifacts:
  - static/exports/BIN-97c95ba5572dce63/SUBSYS-creature-actor-static-census.md
addresses:
  - "0x0041C493"
  - "0x0041E00D"
  - "0x0041E01A"
  - "0x0041BD45"
  - "0x0041BA23"
  - "0x0046574D"
  - "0x00599C60"
  - "0x004C881F"
file_offsets: []
result: reject-six-defects-corrected-analysis-and-both-row-promotions-survive
created: 2026-08-16T23:59:00
updated: 2026-08-16T23:59:00
tags:
  - re/experiment
  - re/audit
  - re/actors
  - research/coverage
---

# EXP-20260816-173 - Independent creature census audit

## Verdict

**REJECT** at `de7b80d`. The analysis is not what failed. A fresh-context
auditor re-derived every opcode handler's PC advance from the disassembly
without reading the worker's table, re-ran the 40-program decode from raw
bytes, and got 463 instructions, zero misalignment, 69 branch/jump
instructions with zero off-boundary targets, and a per-opcode histogram
identical digit for digit. Both switch tables, both loop terminations, every
thunk, every caller, the `KU-069` arithmetic and the `CreatListRam` anchor all
survived unchanged.

The rejection is about the **register**: two bullets in the experiment note's
`### Confirmed` section stated things the instructions do not show, one of
them propagated verbatim into a function dossier. On top of that the published
export miscounted the strings it used to justify a coverage-row promotion, a
number was inflated in three notes relative to the export that derived it, and
the novelty boundary under-credited the M2 export it cites. Each is small;
the pattern is the one this project rejects for.

## What survived independent re-derivation

Binary hash and clean tree. The section table and every spot-checked file
offset. The pool extent from both loop terminations independently. The source
table, the `0x700` copy, the `0x23` gate, and the `LOAD: Type 35,
CreatListRam.` string at its exact site. Builder, update and interpreter
reachability, checked by a byte-level rel32 scan over all of `.text` **plus** a
4-byte absolute-value scan over the whole file — each has exactly one thunk
reference and one call, and none appears as a stored pointer. The auditor
also strengthened one claim: `0x004671D0` is an `int3`-padded function head
with no `ret` anywhere in `[0x004671D0, 0x004679A0)`, which is stronger than
the census's own statement.

Both per-type tables entry by entry, including all nineteen builder rows and
all "—" cells, the eleven-type release set, and the ten distinct handlers. The
`0x004C881F` boolean pattern over the first 48 entries. The full
instruction-size map, re-derived independently before reading §5.2. The 40
programs: contiguity, ascending pointers, the exact `0x6F0` extent, the decode
totals, and the histogram. The external entry point `[0x004C8474] + 0x1A` on
an instruction boundary in script 33, and the whole script-33 listing byte for
byte. The mode dispatch and the corrected "eight no-body, seven select a mode"
statement. Opcode 11's nine subroutines with their arguments. Opcode 16's
comparison against `0x0059D910`/`0x0059D918`, and that `EXP-20260815-128` does
record those as live Flik X and Z. The `rand.dat` chain. That the 4-byte value
`0x004C7970` occurs zero times in the image. The frame table's 28 entries and
opcode 13's 1-based indexing. Every formula in the update pass, and that
`0x0041EEC6` really passes 1 and `0x0041EEE4` really passes 2.

## Defects

1. **The per-type builder claim was false as stated.** The experiment note's
   Confirmed bullet said "Per type, the builder writes a positive count of 1-8
   ... and a thunk pointer into slot `+0x7C`". Of the 36 types in the domain,
   only **9** get both; 5 get a thunk only, 5 a count only, and **17** get
   neither. The export's own §3.1 table showed all the "—" cells; the bullet
   dropped them, and `FUNC-97C95BA5572D-0041C420` repeated the over-general
   form with no qualifier at all — the dossier being what a future agent reads
   first.
2. **A code check was attributed to a handler that has none.** Both the note
   and export §6 said operands stay "inside each handler's own range check",
   citing opcode 13. Opcode 11 is the **only** handler with a range check
   (`dec eax / cmp eax,0x8 / ja` at `0x0041DF4C`-`0x0041DF50`). Opcode 13's
   handler at `0x0041E00D`-`0x0041E02F` has no `cmp` and no `ja`; it indexes
   `[eax*4+0x4c8754]` with the sign-extended operand. The 1..24 span is a
   property of the shipped data. This mattered doubly: it was one of the four
   validations the packet led with, and it is the same unbounded-index class
   the packet opens `KU-069` for elsewhere.
3. **The export miscounted the evidence for a row promotion.** §9 said "four
   strings" and then listed five; there are exactly five, and the experiment
   note, the coverage map and Current State all said five. The export — the
   artifact that publishes the evidence — was the one that was wrong, and it
   is the sole evidence for the Event/scripting row.
4. **A number was inflated ~1.9x in the propagated notes.** The export
   correctly said the cursor `0x00599C60` is *referenced* 380 times; the
   experiment note, Current State and the session note each said *advanced
   from* 380 sites. The split is 181 reads and 199 writes, of which 2 are the
   immediate initialisation, so 197 sites write a value back. The determinism
   hypothesis was stated over the wrong figure.
5. **The novelty boundary under-credited `M2-fixed-pool-index-producer-census.md`.**
   That export already published the `0x1C` source stride, the
   slot-to-source correspondence, and the `0x0046574D`-`0x0046576A` copy of
   `0x700` bytes into `[0x00599EB0, 0x0059A5B0)` under the type-`0x23` gate —
   which is essentially all of §1.2, the item §0 listed as **new**. Sections 7
   and 8 likewise restate prior work without credit. The auditor checked the
   strongest contradiction candidate and found none: the VM indeed never
   writes record `+0x00`, as that M2 census claims.
6. **Two quoted disassembly blocks silently dropped instructions**, and in both
   cases the dropped instruction was the one that made the block mean what the
   surrounding prose said: `mov esi,eax` at `0x00465763` in §1.2, and the
   `jne` at `0x0041E13E` that makes `add edi,0x2` conditional in §5.1. The
   export uses an explicit elision marker elsewhere, so the convention existed
   and was not applied.
7. **§4's structural description of the frame arrays did not match the bytes.**
   "Terminated by `0xFF`, followed by two more bytes" is true for 4 of 25
   distinct arrays; the measured distribution is 1→2, 2→4, 3→4, 4→2, 5→5,
   6→1, 7→6, 8→1, and two arrays have only one trailing byte. The special-value
   enumeration also omitted `0xFC`, which appears three times — the same count
   as `0xFD` and `0xFE`.

## Minor findings, all applied

An operand address cited instead of an instruction address for record `+0x34`
(`0x0041BDD0` → `0x0041BDD2`). §5.2's header sentence did not cover the eight
no-body opcodes, whose 2-byte size comes from the stall-breaker at
`0x0041E140` rather than from a handler. §1.3 omitted the builder block at
`0x0041C52A`-`0x0041C551`, which shifts bit-`0x20` source positions in place
and writes an incrementing counter into source `+0x19` — leaving `+0x19` with
no recorded writer, and the initializer's later unshifted overwrite unrecorded
(the auditor confirmed the net effect is one shift, not two). Record `+0x40`
had two unrecorded writers. The `+0x5C` bit list asserted six tested bits with
no address for any, included bit `0x0002` which is only ever cleared, and
omitted others. §3.3's "zero elsewhere" left the table's extent undefined,
which matters precisely because `KU-069`'s index is unbounded. §8 stated the
`0x0059D99E` decrement unconditionally when it is gated on `+0x6E == 0x3E6`, a
value no per-type default produces and whose producer is Unknown.
`FUNC-97C95BA5572D-0041B9F0` said "each arm sets `+0x44` and most select a
frame sequence", which is wrong under either arm count. The script-16
illustration was one instruction short. Source `+0x16` was attributed to
opcode 3 when only `+0x14` is. `0x005C5860` was labelled without its
cross-reference. `0x004DE2FC` was called a format string though it has no
conversion specifier. §2.3 omitted the second argument `0`.

The auditor also found a **third** unbounded index the packet had not
recorded: source `+0x0D` into the 40-entry script table at `0x0041BD45`, with
no bound check. `KU-069` is broadened from one index to three.

## Scope answers

- **Bounded is correct for Enemies/actors/AI.** The map's definition is "real
  PC evidence at a documented boundary, with major parts open"; this packet
  has a reproducible boundary and states its open parts. None of the defects
  touch the row's anchors, which the auditor verified individually.
- **Touched is correct for Event/scripting.** Five log strings and one push
  site are exactly "incidental observations, no model". The row's own text was
  right; the export's count was wrong.
- **The novelty boundary was partially honest and not enough.** §0 opened by
  saying the subsystem is not untouched and named the right three exports, and
  the genuinely new material is large and real — but its credit list omitted
  five things and the headline "new" item was one of them.

## Limitations of this audit

The ten per-type `+0x7C` handlers, the nine opcode-11 subroutines, the five
modes, and the other called functions were not analysed — the packet claims
nothing about them either. The "no other caller" verification covers rel32
`call`/`jmp` over `.text` plus 4-byte absolute occurrences over the whole
file; it does not exclude register-indirect or computed dispatch, which the
export's §10 also disclaims. No level file was parsed, so `KU-069`'s own
question stands. The accepted camera common block and the runtime provenance
of `EXP-20260815-128` were not re-verified beyond reading the recorded result.
Only the three named M2 exports were checked for prior art, so further
under-credited work may exist. Nothing was run: no game, no debugger, no Wine.

## Hygiene

`make vault-lint` 488 notes / 0 errors / 0 warnings and `make audit-tracked` 0
violations, both matching the subject commit. `make test` on the auditor's
**first** invocation returned `685 passed, 1 failed` of 686 at
`tests/test_input_movie.py::test_log_anchor_uses_only_new_log_bytes` with the
`anchor_timeout` / `NextLife.` signature; the next invocation returned
`686 passed in 18.53s`. That is a third independent recurrence of the exact
`KU-065` node, on a packet that changed no code and no fixture, and it is
recorded there. The denominator is 686 and every passing figure keeps the
`KU-065` qualification.

## Correction

All seven defects and every minor finding are applied in the commit that
records this audit, in
[[EXP-20260816-172 - PC creature actor pool and behaviour VM census]], the
export, both affected dossiers, `KU-069`, and the propagated notes. No derived
number in the analysis changed, because none of them was wrong. A fresh audit
follows this correction.

## Corrections to this audit

[[EXP-20260817-174 - Second independent creature census audit]] found two
statements in this note wrong, and both had been carried into the correction:

- The minor finding that flag bit `0x0002` "is only ever cleared" is **false**.
  It is tested at `0x0041E208` (`test al,0x2`, on `mov al,[esi+0x5c]` at
  `0x0041E201`) — inside `0x0041DC60`, i.e. inside this audit's own declared
  scope. The corrected §2.2.1 repeated the error until EXP-174.
- "**Two** quoted disassembly blocks silently dropped instructions" understates
  it: there are **three**. The §5.2 fetch/dispatch block also omits
  `0x0041DCEC: mov DWORD PTR [esp+0x30],edi`, the only definition of the very
  slot §5.1 then annotates as the saved program counter. That block was never
  corrected in the first pass.

Both errors have the same root cause, which this audit declared as a
limitation and EXP-174 exploited: neither this audit nor the packet read
`0x0041DC60` past `0x0041E1A8`. (This section originally said the function
"runs to `0x0041E7D3`" — that was EXP-174's figure and is itself superseded:
`0x0041E7D3` is the only `ret` but not the end, and the extent is
`0x0041DC60`-`0x0041E845`. See
[[EXP-20260817-175 - Third independent creature census audit]].)
This note's other findings and its "what survived" list were independently
re-confirmed by EXP-174.
