---
type: session
date: 2026-08-17
agent: James
status: rejected
tags:
  - session
  - re/audit
  - research/coverage
---

# Second event census audit

## Agent

James, fresh context, second audit of the event packet. No knowledge of the
first round beyond the artifacts committed at `311f79b`; the previous auditor's
findings were treated as claims to re-test, not as settled.

## Goal

Judge the correction commit `311f79b`, which claims to fix all twelve defects a
first-round James audit raised against `4e0157f`. Two questions: did each fix
land and is each correct, including whether any "fix" corrected something that
was not wrong; and what did **both** rounds miss.

## Files inspected

`CLAUDE.md`; [[START HERE]]; [[Agent Operating Manual]];
`static/exports/BIN-97c95ba5572dce63/SUBSYS-event-static-census.md`;
[[EXP-20260817-185 - PC event subsystem static census]];
[[FUNC-97C95BA5572D-0042DB10]]; [[FUNC-97C95BA5572D-0042D980]];
[[2026-08-17 1130 - Claude - PC event subsystem census]];
[[2026-08-17 1230 - James - Event census audit]]; the full `4e0157f` and
`311f79b` diffs including [[Current State]], [[Subsystem Coverage Map]],
[[Subsystems MOC]], [[Functions MOC]], [[Experiments MOC]], [[Project Roadmap]]
and `KU-071`; the prior art the packet cites —
`SUBSYS-audio-static-census.md`, `SUBSYS-creature-actor-static-census.md`,
[[EXP-20260816-159 - PC audio subsystem static census]] — and the generated
`static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json`, read directly as
JSON rather than grepped; the parent tree `4e0157f^` for the novelty negative;
and `work/copies/BUGS_PC-full-disc/bugs.exe`, re-hashed to
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.

## Experiments inspected

`EXP-20260817-185` (the packet), `EXP-20260816-159` (the `0x004D81E8` prior
art) and `EXP-20260816-172` via the creature export (the row's earlier anchor).

## Changes made

None. This note only. No packet artifact was touched and nothing was committed.

## Conclusions

**REJECT.** Ten defects.

All twelve first-round findings were re-tested against the binary and all
twelve were real. Eleven of the twelve fixes are technically right where they
landed. But four landed in only some of the places the same statement appears,
one over-corrected into two new false claims about the generated prior art, and
the artifact the commit message says was corrected — the session note — was
only appended to, so five of the twelve defects still stand verbatim in it.
Three further defects are in text neither round examined.

### Part A — the twelve fixes, re-verified

Correct and complete:

- **D1.** Eight `call 0x401cf8` sites exist inside `[0x0042D950, 0x0042DD94)`;
  exactly four are preceded by the inlined `rep stos`, and they are exactly the
  two-`%s` sites. Strings decoded byte-exact from file bytes:
  `0x004D823C`/`0x004D82A4`/`0x004D830C` carry one `%s`, `0x004D8264` and
  `0x004D82CC` two. `0x004ADEA0` verified instruction for instruction —
  `sub esp,0x400` at `0x004ADEA5`, `mov ecx,0x100` + `rep stos` on `[esp+0x8]`
  at `0x004ADEB1`-`0x004ADEC0`, `push lea [esp+0x410]` / `push [esp+0x40c]` /
  `push edx` into `0x004B0150`, then `0x004B0730`/`0x004B13A0`/`0x004B04E0`.
  Under that frame arg 1 is the format and `0x00598670`, pushed first at each
  of the four sites, is the second vararg. The correction is right and the
  causal "because" is gone.
- **D2.** `0x0040169F: e9 ac c2 02 00 jmp 0x42d950` is now named. Zero direct
  branches target it, and all eight whole-file 4-byte LE scans (four thunks,
  four functions) return zero. The four-dead claim is now earned as written.
- **D5.** The destroy pass uses exactly **nine** distinct record-relative
  displacements; the nine listed resolve as stated, `+0x00` is untouched, and
  the independence caveat about the imported origin `0x00598668` is correct.
- **D6.** The `+0x34` row is now exhaustive: set at `0x0042DBE0`; tested at
  `0x0042DB26`, `0x0042DCB4`, `0x0042D992`, `0x0042D9D4`, `0x0042DA80`; cleared
  at `0x0042DA10`, `0x0042DAB0`, `0x0042DB83`, `0x0042DD13`. No other site.
- **D8.** `create` and `destroy` are anchored: `0x004D82CC` is pushed at
  `0x0042DC14` and `+0x04` called at `0x0042DC2A`; `0x004D8264` is pushed at
  `0x0042DAA0`/`0x0042DB51`/`0x0042DCE0` with `+0x0C` called at `0x0042DAAD`/
  `0x0042DB67`/`0x0042DCF6`. `+0x08` has no string. The unnaming is right.
- **D10.** A whole-file scan for `0x005982AC` returns exactly two hits, the
  immediates of the `a3` stores at `0x0042D99A` and `0x0042D9DA`. Never read.
- **D11.** `movsx` at `0x0042DA00`, `0x0042DB18`, `0x0042DCA8`; no range test
  reaches the first access in any of the three. Only `mov edi,0x10` /
  `mov ebp,0x10` bound the two passes.

Correct where it landed, incomplete elsewhere: **D3** (see J3), **D4** (J4),
**D9** (J9), **D12** (J8 and the audio coverage row). Over-corrected: **D7**
(J1, J2).

The packet's counter-claim against the audit is **correct, and understated**.
`jne 0x43db0b` at `0x0043DB04` lands on the `push 0x4d81e8` that sets up the
second registration, so it skips only `call 0x401c30`. Stronger: the enclosing
function is `0x0043DA40`-`0x0043DFE6` (entered through thunk `0x00401866`,
single exit `ret 0x10` at `0x0043DFE6`), and **no** branch anywhere in the
image targets any address in `[0x0043DA40, 0x0043DB04)`. Both registrations are
therefore on the function's straight-line entry path, not merely unconditional
relative to that one test. The packet could have claimed more than it did.

### Part B — defects

**J1 — §0's central novelty claim is false: `ghidra-evidence.json` already
carries the thunk-resolved caller lists.** §0: "`ghidra-evidence.json` has **no
entry at all** for `0x0042D950`, `0x0042D9D0`, `0x0042DA00` or `0x0042DCA0`,
and the `callers` list is empty for all three functions it does carry", and
"the thunk-resolved caller analysis, and with it the finding that four of the
seven entry points are unreachable (ghidra has no entry for those four and **no
caller data for the other three**)".

The first half is true; the second is false. The file carries **six** entries
covering three functions, not three:

| entry `name` | entry `address` | `callers` |
|---|---|---|
| `FUN_0042d980` | `0042d980` | `[]` |
| `FUN_0042da70` | `0042da70` | `[]` |
| `FUN_0042db10` | `0042db10` | `[]` |
| `thunk_FUN_0042d980` | `004013ac` | `['0043dc5a', '00405cb0']` |
| `thunk_FUN_0042da70` | `00401c44` | `['0043daeb', '00405c54', '00405a73']` |
| `thunk_FUN_0042db10` | `004017b2` | `['0043daf5', '0043db10']` |

The export names the three entries by their **thunk** names — precisely the
three that carry callers — and then says the caller lists are empty. Seven of
the nine reachers §2 enumerates are already in that file, in already
thunk-resolved form. Only `0x004AE863` and `0x004121A1` are not. So the item
§0 puts first among what is new is the item most nearly prior art. D7 was
raised for under-crediting this file; the correction re-under-credits it on the
one axis that carries the packet's novelty claim.

Propagated to [[Current State]] ("What is new is the thunk-resolved caller
analysis and the four dead entry points"), the [[Subsystem Coverage Map]] row
("the caller analysis and dead entry points are new") and `EXP-20260817-185`
Artifacts ("What is new is the thunk-resolved caller analysis and the four dead
entry points (ghidra has no entry for those four)").

Fix: record that ghidra's thunk entries already give the caller lists for all
three live entry points; what is genuinely new is the two reachers it misses
(`0x004AE863` and the `0x004121A1` tail `jmp`), the `jmp`-form reacher search,
and the two-direction dead-entry proof for the four functions it has no entry
for at all.

**J2 — §0 credits the `0x0042DB10` body with two things it does not contain.**
"Its `0x0042DB10` body alone already renders: ... **all three** code-pointer
slots as calls — `(**(code **)(&DAT_005982b4 + *param_1 * 0x3c))()` and the
`&DAT_005982bc` equivalent; ... and **all five** format strings by symbol."

`FUN_0042db10`'s decompilation renders **two** slots as calls; `&DAT_005982b8`
appears only as `(&DAT_005982b8)[iVar2 * 0xf] = 0;`. The bullet contradicts
itself — it says three and then names two. And it renders **four** format
strings (`004d8264`, `004d830c`, `004d82cc`, `004d82a4`); the fifth,
`004d823c`, appears only in `FUN_0042da70`. Fix: attribute the third slot to
`FUN_0042d980` (`(*(code *)*puVar1)()`) and the fifth string to
`FUN_0042da70`, or drop "alone".

**J3 — the D3 fix did not propagate; the site count is still eight.** §2 now
lists five reachers of `0x0042DA70` including `0x004121A1`, but §6 still reads
"The enclosing functions and callers of `0x00405CB0`, `0x0043DC5A`,
`0x00405A73`, `0x00405C54`, `0x0043DAEB`, `0x004AE863`, `0x0043DAF5` and
`0x0043DB10`" — `0x004121A1` absent — and `EXP-20260817-185` Unknown still says
"the enclosing functions and callers of the **eight** sites that reach the live
entry points". There are nine: two for `0x0042D980`, five for `0x0042DA70`, two
for `0x0042DB10`.

**J4 — the D4 fix did not propagate inside its own table; two §2 rows still
say "zero the record".** The `0x0042DA00` row was corrected to "zero every
field except the id at `+0x00` and the name at `+0x10`", but the `0x0042DA70`
row still reads "log, then **zero the record**" and the `0x0042DCA0` row "log,
**zero the record**". Neither path writes `+0x00` or `+0x10` — the export
proves it two sections later, naming those very ranges
(`0x0042DAB0`-`0x0042DAD0`, `0x0042DD13`-`0x0042DD40`). The table now holds one
corrected row and two carrying the exact wording D4 rejected.

**J5 — the lifecycle order is inverted at three sites, in a section headed
"in order".** §3 step 3: "log `0x004D830C` ("deleted") **and zero** `+0x34`,
`+0x38`, ...". The binary zeroes first: the eight writes run
`0x0042DB83`-`0x0042DBB0` and the log call is at `0x0042DBB6`. Same inversion
in §2's `0x0042DA70` row ("log, then zero") — writes `0x0042DAB0`-`0x0042DAD0`,
log call `0x0042DAD3` — and its `0x0042DCA0` row — writes
`0x0042DD13`-`0x0042DD40`, log call `0x0042DD46`. Only the name pointer is
captured before the zeroing (`lea ecx,[esi-0x24]` at `0x0042DABD`), which is
why the printed name survives. In a numbered "in order" list of instruction
addresses this is a wrong statement about the binary, not a stylistic choice.

**J6 — §1.1's `+0x10` row asserts an address that occurs nowhere in the file,
and a "%s of every log line" that holds for two log lines in eight.** Neither
round examined this row. Both halves are wrong.

- "Accessed as `0x005982C0`": a whole-file 4-byte little-endian scan for
  `0x005982C0` returns **zero** occurrences. Every other row's address is a
  real operand — `0x005982B0` once (`0x0042DBD1`), `B2` three times, `B4` five,
  `B8` four, `BC` seven, `E0`/`E2` three each, `E4` six, `E8` three. The §1.1
  preamble says the table is "Derived from the `id`-scaled absolute addresses
  each field is accessed by"; for `+0x10` no such access exists. Its offset
  comes only from `lea [esi-0x24]` in the destroy pass and `[ebx+0x10]` /
  `[esi+0x10]` on caller-supplied pointers — that is, from the *cross-check*.
  So `+0x10` has one derivation, not two, precisely at the field whose width is
  already conceded to be inference. The corrected "confirmed twice from
  different addressing forms" framing does not hold for this row and the export
  does not say so.
- "name; passed as a `%s` of every log line": the **table** record's `+0x10` is
  the argument at only `0x0042DAA5` and `0x0042DAD3`, both via
  `lea [esi-0x24]`. At the other six — `0x0042DB56`, `0x0042DBB6`,
  `0x0042DC19`, `0x0042DC3A`, `0x0042DCE5`, `0x0042DD46` — the argument is the
  **caller-supplied** record's `+0x10`. The consequence is worth stating: at
  `0x0042DB56` the line prints the *incoming* record's name while the `+0x0C`
  called at `0x0042DB67` belongs to the *outgoing* occupant of the slot. The
  same wording sits in `EXP-20260817-185`'s Confirmed set.

**J7 — §5's "in-use flag `+0x34` only" contradicts §6.** The disjointness
table's "Per-instance state" row gives events "in-use flag `+0x34` only".
`+0x02`, `+0x30`, `+0x32` and `+0x38` are per-record fields copied in by the
`rep movs` at `0x0042DBD5` and zeroed by all four clearing paths, and §6 lists
their meaning as unestablished. "Only" is an unearned negative, and it sits
inside the argument the packet calls a proof.

**J8 — the session note was appended to, not corrected, while the commit
message claims otherwise.** `311f79b` states "Corrections propagated to Current
State, the coverage row, `KU-071`, both MOCs, both dossiers, the experiment
note and the session note."
[[2026-08-17 1130 - Claude - PC event subsystem census]] gained an "Audit
outcome" section listing the twelve defects, and nothing else changed. Outside
that table the note still says:

| Section | Surviving text | Defect |
|---|---|---|
| Conclusions | "three native callbacks (create/**update**/destroy)" | D8 |
| Conclusions | "**Two events are statically registered**" | D12 |
| New hypotheses | "Every statement in the export is an instruction or a decoded byte" | D9 |
| Tests run | "all **eight** displacements consistent" | D5 |
| Tests run | "the **three** dead thunks checked in both directions" | D2 |

The note now contradicts its own defect table five times. A related residual:
the **audio** row of [[Subsystem Coverage Map]] still reads "`0x0042BA60` is
the `"DIRECTX"` **event create callback**, **invoked at** `0x0042DC2A`" — the
verb the export deliberately abandoned under D12, where §4.1 now says only that
`+0x04` is the target of the `call` at that address.

**J9 — [[FUNC-97C95BA5572D-0042DB10]] still declares itself inference-free
while carrying the log-formatter reading.** The correction added to its Callees
section "Thunk `0x00401CF8` → `0x004ADEA0`, **read here as a log formatter**"
— which `EXP-20260817-185` now classifies as Inferred — but left "## Inferred /
Nothing beyond the instructions" untouched two sections above. That is D9's
exact failure mode, in one of the "both dossiers" the commit claims to have
corrected. [[FUNC-97C95BA5572D-0042D980]] is clean: it makes no log call and
asserts no formatter reading.

**J10 — "a 128-byte zeroed buffer" states a size the file does not give.** §1
asserts `0x00598670`'s extent as fact; the only evidence is the `mov ecx,0x20`
zeroing width. I scanned the whole image for any 4-byte little-endian value in
`[0x005982A0, 0x005986F0)`: 47 hits, **every one inside the seven functions**,
and none above `0x00598670`. Nothing establishes where that buffer ends. It
should read "at least 128 bytes are zeroed", or the extent belongs in §6 beside
the other unestablished sizes.

### What I re-derived and confirm

- SHA-256 re-hashed; `objdump -h` matches §0's section table exactly, including
  `.data`'s raw end at `0x004ED400` and the `.bss`-class boundary.
- Base `0x005982B0` and stride `0x3C` from `0x0042DBC1`-`0x0042DBD5`; the 16
  bound from `mov edi,0x10` at `0x0042D988` and `mov ebp,0x10` at `0x0042DA79`;
  `0x005982B0 + 0x3C0 = 0x00598670`; origin `0x00598668` with `-0x3C` step.
- All seven extents and `0x0042DD90`, and their file offsets under
  `VMA - 0x400C00`. Direct branches into `[0x0042D950, 0x0042DD94]` from
  outside: exactly eight, all `jmp`s from the `0x00401xxx` table
  (`0x004010C8`, `0x00401140`, `0x00401217`, `0x004013AC`, `0x0040169F`,
  `0x0040179E`, `0x004017B2`, `0x00401C44`); none lands mid-function. The only
  outbound direct target from any of the seven is `0x00401CF8`.
- The nine reachers of the three live entry points, including
  `0x004121A1: e9 9e fa fe ff jmp 0x401c44` in a function that also calls
  `0x004017C6` and logs `0x004C52B4`.
- Both records byte-for-byte at file `0x0D6DA8` / `0x0D6DE8`, ids 2 and 3,
  `+0x02` zero, `+0x30`..`+0x3B` zero, names `"WINDOWS"` / `"DIRECTX"`, and all
  six callback thunks resolved as stated. `0x004D81A8` and `0x004D81E8` each
  occur exactly once in the image, at the two `push`es.
- All five `EVENT` strings byte-exact at the stated `.data` offsets, and each
  referenced exactly at the sites §3 lists and nowhere else — verified by
  whole-file scan, not by reading the region.
- §5 in both directions, and under a stronger sweep than claimed: no dword
  anywhere in the event range falls in `0x0041D000`-`0x0041F000`,
  `0x004C7000`-`0x004C9000` or `0x0059B000`-`0x0059E000`, and none in the
  interpreter range falls in `0x00598000`-`0x00599000`. The creature-side
  figures match `SUBSYS-creature-actor-static-census.md` exactly, including
  `[0x004C7D00, 0x004C83F0)`.
- The §0 authored prior-art quotations are verbatim from
  `SUBSYS-audio-static-census.md`, `EXP-20260816-159` and the creature export,
  and the §4.1 refinement is right.
- The novelty negative against `4e0157f^`: all fifteen listed addresses,
  including the two added by the correction (`0x00401CF8`, `0x004ADEA0`),
  appear in no authored note or markdown export in that tree.
- Hygiene: `make vault-lint` 519 notes / 0 / 0; `make audit-tracked` 0
  violations; `make test` 686 passed in 17.29s — run by me, logs read.

**Bounded remains earned.** "Real PC evidence at a documented boundary, with
major parts open" fits, and none of J1-J10 touches the table geometry, the
record layout, the extents or the disjointness result. The status is not the
problem; the text layered on top of it is.

### One finding offered to the packet

Nothing anywhere in the image references any address in
`[0x005982A0, 0x005986F0)` outside the seven functions — 47 whole-file hits,
all inside them. That is a stronger boundary result than §2's per-thunk scans
and is worth recording: on the absolute-address axis, this subsystem is closed.

## New hypotheses

None.

## Contradictions discovered

Four, all internal to the packet: §2's two uncorrected "zero the record" rows
against §3 and against the corrected `0x0042DA00` row (J4); §5's "`+0x34` only"
against §6's four unknown fields (J7); the session note's Conclusions, New
hypotheses and Tests run against its own audit-outcome table, five times (J8);
and `FUNC-97C95BA5572D-0042DB10`'s "Inferred: Nothing" against its own Callees
section (J9).

## Tests run

`make vault-lint` 519 notes, 0 errors, 0 warnings; `make audit-tracked` 0
violations; `make test` 686 passed in 17.29s. Binary work: `objdump -d -M intel`
over the full image, a Python branch-target index over all 357,242 decoded
instructions, whole-file little-endian scans for every thunk, function, table
field, string and record address cited, an interval sweep over
`[0x005982A0, 0x005986F0)`, byte decoding of the two records and the five
strings, and control-flow reconstruction of `0x0043DA40`-`0x0043DFE6`.
`ghidra-evidence.json` was parsed as JSON and its six relevant entries read in
full.

## Unresolved questions

`KU-071`; the six callback targets; whether any event is registered outside the
two static sites; whether computed dispatch reaches any of the seven entry
points — my scans share the packet's blind spot and §6's caveat is the right
one to keep; the meaning of `+0x02`, `+0x30`, `+0x32`, `+0x38`, `0x0059F7F0`
and of a `0x005982AC` nothing reads; the true extent of the buffer at
`0x00598670` (J10). Not verifiable from artifacts: that the greps and extent
reads happened before analysis, and that no `originals/` path, asset or PS1
source was touched.

## Recommended next action

Fix J1 and J2 first — they are false statements about a file in the repository
and they carry the packet's novelty claim into [[Current State]] and the
coverage row. Then the propagation misses J3, J4, J8 and J9, which are the same
four defects the first round already raised, surviving in places the correction
did not reach; the session note needs its body corrected, not another appendix.
Then J5, J6, J7, J10 in the export. Re-audit with fresh context afterwards. The
recurring pattern across both rounds is that a fix is applied at the first place
the wording occurs and nowhere else — a grep for the corrected phrase across
`Vault/` and `static/exports/` before commit would have caught J3, J4, J8 and J9.

## Git commit if applicable

None by the auditor. Nothing in the packet was modified.
