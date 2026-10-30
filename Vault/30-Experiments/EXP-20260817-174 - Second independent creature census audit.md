---
type: experiment
id: EXP-20260817-174
date: 2026-08-17
question: 'Do the corrections applied after EXP-173 hold, and does the creature census survive a second independent re-derivation?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline audit; GNU objdump 2.46; radare2 5.9.8; no runtime, debugger, or target write
environment_version: objdump 2.46-3.fc44
working_directory: /home/dev/ABLPC
configuration: fresh-context audit at clean HEAD 47d447f; read-only toward game media and originals; nothing committed or modified by the auditor
artifacts:
  - static/exports/BIN-97c95ba5572dce63/SUBSYS-creature-actor-static-census.md
addresses:
  - "0x0041E7D3"
  - "0x0041E7C7"
  - "0x0041E208"
  - "0x0041E1EB"
  - "0x0041E2E1"
  - "0x0041DCEC"
  - "0x0041DDD4"
  - "0x0041DEE1"
file_offsets: []
result: reject-unread-function-tail-and-uncited-prior-art-both-corrected
created: 2026-08-17T00:30:00
updated: 2026-08-17T00:30:00
tags:
  - re/experiment
  - re/audit
  - re/actors
  - research/coverage
---

# EXP-20260817-174 - Second independent creature census audit

## Verdict

**REJECT** at `47d447f`. For the second time the analysis reproduced
completely — all 26 opcode PC advances re-derived from
`0x0041DC60`-`0x0041E147` without reading §5.2, then 463 instructions, zero
misalignment, 69 branch/jump instructions with zero off-boundary targets, and
a histogram identical digit for digit. Both switch tables, both loop
terminations, the `380 = 181 + 199` and `199 = 2 + 197` splits, the
trailing-byte histogram, the five `EVENT` strings and every caller claim held.
Every correction from `EXP-20260816-173` was independently verified as right.

The rejection has one root cause with four consequences, plus one recurrence.

## Root cause: an unread function tail

Function `0x0041DC60` runs to its only `ret` at **`0x0041E7D3`**. Both prior
drafts read it only to `0x0041E1A8` — about 45% — while §2.2.1 and §5.2 made
completeness claims scoped to that whole function. In the unread tail:

1. **Flag bit `0x0002` is tested** at `0x0041E208` (`test al,0x2`, on
   `mov al,[esi+0x5c]` at `0x0041E201`), directly refuting §2.2.1's Confirmed
   cell "no test of it found in scope". Worse, that cell existed *because*
   `EXP-20260816-173` asserted it as a minor finding — an audit error carried
   into the correction.
2. **Four more tested bits are missing**: `0x0004` at `0x0041E589`, `0x0100`
   at `0x0041E442`-`0x0041E448`, `0x0400` at `0x0041E3EC`-`0x0041E3F1`, and
   `0x2000` at `0x0041E65F`-`0x0041E669`. Of the ten `[esi+0x5c]` sites in the
   function, the export accounted for five — exactly the five before
   `0x0041E1A8`.
3. **`0x0041E140` is not "the only place a blocking instruction is ever
   stepped over".** `0x0041E1EB` writes `+0x70` with `edi+2` when the mode
   local is 2 (pending opcode 9 or 18), and `0x0041E2E1` writes it with `+6`
   when the pending opcode is 17 or 18. The `+6` advance is an unexamined
   consequence of the size model the census leads with.
4. **The `+0x7C` handler call edge was missing entirely.** At `0x0041E79E` the
   interpreter loads `[esi+0x7c]`, null-checks it, builds a stack record
   containing the pool record pointer, and executes `call eax` at
   `0x0041E7C7`. This is the invocation point for all ten per-type handlers
   the builder installs. It is an **outbound register-indirect call**: the
   census's own caller-completeness method — rel32 scans plus absolute-value
   scans — misses it by construction, which is exactly what §10 disclaims for
   inbound edges and had not considered for outbound ones.

## Second finding: the headline novelty was prior art

`static/exports/BIN-97c95ba5572dce63/M2-plant-request-origin-static-trace.md`,
cited nowhere in either draft, already publishes: that `0x004679A0` calls
`0x0041C420` "which rebuilds the **64** records rooted at `0x0059B628`"; the
`0x2100` clear; that the builder "walks **64** source records at a `0x1C`-byte
stride and 64 destination records at a `0x84`-byte stride"; the
`0x0046574D`-`0x0046576A` copy of `0x700` bytes into `0x00599EB0`; and the
string **`LOAD: Type 35, CreatListRam.`** — observed in retained Training and
Level 01 hardware logs, i.e. with runtime corroboration this offline census
does not have.

So the subsystem identity and the 64-to-64 map, presented as the headline new
result in the first draft and still reserved as partly new in the second, are
prior art. **Eight** exports in that directory reference `0x0059B628`; both
drafts said three, and `EXP-20260816-173` had flagged exactly this exposure as
its own limitation without the correction pass widening the search.

## Third finding: a third truncated disassembly block

§5.2's fetch/dispatch quote omits `0x0041DCEC: mov DWORD PTR [esp+0x30],edi`
with no elision marker — the only definition of the slot §5.1's block then
annotates as "PC before this instruction". This is a recurrence of the defect
class `EXP-20260816-173` rejected for, and that audit's own count of "two
blocks" was itself one short.

## Fourth finding: a fourth unbounded index

VM opcodes 4 and 10 read the record-type pointer table `0x005C5860` with
`mov reg,[ecx*4+0x5c5860]` at `0x0041DDD4` and `0x0041DEE1`, where `ecx` is
the raw source `+0x0E`/`+0x0F` byte (0..255). That table holds 64 entries —
the clear at `0x00467207`-`0x00467215` that `KU-064` already records — so a
source byte of 64 or more reads past it. `KU-069` goes from three indexes to
four.

## Minor findings, all applied

§1.1 said "Two consumers" and cited three sites. `FUNC-97C95BA5572D-0041C420`
said "Two further facts" above four bullets. §2.2's "not observed" closing
line was false for `+0x14`, `+0x1C`, `+0x20`, `+0x24` and `+0x7A`, all touched
in the tail. §5.3 never said where the mode is stored (`[esp+0x4c]`,
initialised at `0x0041DCB5`, read at `0x0041E1A8` and `0x0041E214`). The
coverage map built a general method lesson on the `CreatListRam` find that the
prior-art correction undercuts. `EXP-20260816-172`'s Confirmed heading
"Blocking opcodes are states" was interpretive where the dossier correctly
kept it Inferred.

## What survived

Everything numeric, again, and every first-audit correction: the pool extent
from both loop terminations; the source table and `0x700` copy; the
`CreatListRam` string at its exact site; builder, update and interpreter
reachability under rel32 plus whole-file absolute scans; §3.1's four-outcome
partition and all nineteen rows; §3.2's eleven non-default types; §3.3's
pattern over 48 entries; the full instruction-size map including the
stall-breaker derivation, which the auditor independently judged sound and
found corroborated by `lea edx,[edi+0x2]` at `0x0041E1E2`; the 40 programs,
their contiguity, the `0x6F0` extent, the decode totals and histogram; script
33 and script 16 byte for byte; the external entry point; the mode dispatch
and the "eight no-body, seven select a mode" statement; opcode 11 as the sole
range-checked handler; the `rand.dat` chain; `0x004C7970` occurring zero times
in the whole file; and the `0x3E6` gate on the `0x0059D99E` decrement. No
numeric drift was found across any artifact.

The auditor also re-confirmed `EXP-20260816-173`'s contradiction check: the
interpreter reads record `+0x00` at `0x0041E594`, `0x0041E671` and
`0x0041E69F` but never writes it, as `M2-fixed-pool-index-producer-census.md`
claims.

## Scope answers

- **Bounded remains correct for Enemies/actors/AI.** Every row anchor was
  independently reproduced; the defects concern register, completeness and
  attribution, not the anchors.
- **Touched remains correct for Event/scripting.** Exactly five `EVENT`
  occurrences in the whole file, all at the cited addresses, plus one push
  site.
- **The §0 novelty boundary was still not honest**, and now wrong on the item
  it named as headline. It is rewritten to state novelty by address instead of
  by narrative.
- **`EXP-20260816-173` describes the prior audit accurately** apart from two
  statements, both corrected in place: the bit-`0x0002` claim and the
  "two blocks" count.

## Limitations of this audit

The ten per-type `+0x7C` handlers, the nine opcode-11 subroutines and the
other called functions were not analysed. The tail `0x0041E1A8`-`0x0041E7D3`
was read only for flag tests, `+0x70` writers, record-field accesses and
gating control flow — not for what it computes, so the packet's Unknown
register on the five modes stands. Caller checks remain rel32 plus whole-file
absolute scans, which by construction miss computed dispatch — as the
`call eax` finding demonstrates. Cross-referenced results (`EXP-20260815-128`,
`EXP-20260816-165`, `EXP-20260816-153`, `KU-064`) were not themselves
re-verified. No level file was parsed. Nothing was run.

## Hygiene

`make vault-lint` 490 notes / 0 errors / 0 warnings; `make audit-tracked` 0
violations; `make test` **686 passed** in a single invocation with no failure
on that run. The suite figure keeps its `KU-065` qualification: the same node
failed on the previous audit's first invocation one commit earlier.

## Correction

All findings are applied in the commit that records this audit — to the
export, `EXP-20260816-172`, `EXP-20260816-173`, the interpreter dossier, the
builder dossier, `KU-069`, the coverage map, the Subsystems MOC and Current
State. No derived number changed, because none was wrong. A third fresh audit
follows.

## Corrections to this audit

[[EXP-20260817-175 - Third independent creature census audit]] found two
errors in this note, both propagated into the correction it drove:

- **The function extent is wrong.** `0x0041DC60`'s only `ret` is at
  `0x0041E7D3`, but that is not its end: `0x0041E7D4`-`0x0041E845` is entered
  from `0x0041E6CD` and `0x0041E6D8`, shares the frame, and returns with
  `jmp 0x41e6e6` at `0x0041E841`. The extent is `0x0041DC60`-`0x0041E845`.
- **Consequently the `+0x70` sweep stopped early.** There are **four** writers,
  not three: this note's table missed `0x0041E7FE` (`+2`, entered when the mode
  local exceeds 2, i.e. pending opcode 20 or 6).

Its "No numeric drift was found across any artifact" also missed one: the
subject's own audit-history section still read "rejected once". Every other
finding and its "what survived" list were independently re-confirmed.
