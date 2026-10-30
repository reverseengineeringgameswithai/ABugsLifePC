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

# Event census audit

## Agent

James, fresh context, first audit of the event packet.

## Goal

Judge the PC event subsystem census committed at `4e0157f` against the binary
alone, with no prior context on the work. Attack surface as handed over: the
table arithmetic, the record layout and its claimed second derivation, the four
dead-entry-point completeness claims, all seven extents, the two decoded static
records, the §5 disjointness proof, the §0 prior-art boundary, the
Confirmed/Inferred discipline, and the Vault propagation.

## Files inspected

`CLAUDE.md`; [[START HERE]]; [[Agent Operating Manual]];
`static/exports/BIN-97c95ba5572dce63/SUBSYS-event-static-census.md`;
[[EXP-20260817-185 - PC event subsystem static census]];
[[FUNC-97C95BA5572D-0042DB10]]; [[FUNC-97C95BA5572D-0042D980]]; the `4e0157f`
diff in full, including [[Current State]], [[Project Roadmap]],
[[Subsystem Coverage Map]], [[Subsystems MOC]], [[Functions MOC]],
[[Experiments MOC]], `KU-071` and
[[2026-08-17 1130 - Claude - PC event subsystem census]]; the prior art it
cites — `SUBSYS-audio-static-census.md`,
[[EXP-20260816-159 - PC audio subsystem static census]] and
`SUBSYS-creature-actor-static-census.md`; the generated
`static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json`; the parent tree
`4e0157f^` for the novelty negative; and
`work/copies/BUGS_PC-full-disc/bugs.exe`, re-hashed to
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.

## Experiments inspected

`EXP-20260817-185` (the packet), `EXP-20260816-159` (the `0x004D81E8` prior
art) and `EXP-20260816-172` (the row's previous anchor, via the creature
export).

## Changes made

None. This note only.

## Conclusions

**REJECT.** Twelve defects. The model is substantially right — I re-derived
the table, the stride, the 16-record bound, the whole record layout and every
decoded byte, and all seven extents, and they hold — but the export carries two
statements that the binary contradicts outright, two incomplete enumerations
presented as complete, an under-attributed generated prior art whose
decompilations already contain three of the four things §0 calls new, one
structure-field name with no evidence behind it inside a set declared free of
inference, and several missing negatives.

Defects, in severity order.

**D1 — "every log site" is false, twice, and `0x00598670` is not a formatting
buffer.** §1: "`0x00598670` is the 128-byte scratch buffer (`mov ecx,0x20` +
`rep stos`) that **every log site clears before formatting**". §2, on
`0x0042D950`: "**no direct caller**; the same `rep stos` is inlined at **every
log site** instead". Both false.

- There are **eight** direct log calls inside the seven functions —
  `0x0042DAA5`, `0x0042DAD3`, `0x0042DB56`, `0x0042DBB6`, `0x0042DC19`,
  `0x0042DC3A`, `0x0042DCE5`, `0x0042DD46` — and only **four** are preceded by
  the inlined clear (`0x0042DA9A`, `0x0042DB4B`, `0x0042DC0E`, `0x0042DCD5`).
  The other four never touch `0x00598670`. The four that do are exactly the
  sites whose format string carries two `%s` (`0x004D8264` ×3 and `0x004D82CC`
  ×1); the four one-`%s` formats do not.
- `0x00598670` is not a formatting destination. `0x00401CF8` → `0x004ADEA0`,
  which at `0x004ADEA5` does `sub esp,0x400`, zeroes a `0x400`-byte **stack
  local** at `[esp+0x8]` (`mov ecx,0x100` / `rep stos`,
  `0x004ADEB1`-`0x004ADEC0`), calls `0x004B0150` with that local, the format
  string `[esp+0x40c]` and the vararg pointer `lea [esp+0x410]` — a
  `vsprintf`-shaped call — and then writes the result to a file
  (`0x004B0730` / `0x004B13A0` / `0x004B04E0`). `0x00598670` is pushed as the
  *third* argument at the four sites, i.e. as the **second `%s` vararg**, and it
  is zeroed immediately beforehand, so it renders as an empty string.

  Propagated: [[Current State]] "`0x0042D950`'s body is inlined at every log
  site instead"; `EXP-20260817-185` Confirmed "`0x0042D950` has no direct caller
  **because** the same `rep stos` is inlined at every log site".

  Fix: give the 4-of-8 split with both lists; describe `0x00598670` as a zeroed
  global passed as the second `%s` at the four two-`%s` sites; delete the
  causal "because", which is an inference and a false one.

**D2 — `0x0042D950` has a thunk, and the export does not know it.**
`0x0040169F: e9 ac c2 02 00  jmp 0x42d950` sits in the same
`0x00401000`-`0x00402000` jmp table as the other six thunks the export names.
The export never mentions it. Two consequences: §2's stated method — "For the
**three** whose thunks are empty, both directions were checked ... neither the
thunk address nor the function address occurs anywhere in the file as a 4-byte
little-endian value" — covers three functions when the packet claims four dead;
and the fourth's dead-ness is asserted on a different and false basis (D1).
Propagated to [[Subsystems MOC]] ("Dead entry points: `0x0042D9D0`,
`0x0042DA00`, `0x0042DCA0` (thunks with no callers); `0x0042D950` has no direct
caller") and [[Current State]]. The *conclusion* survives my own check —
`0x0040169F` has zero direct branches to it and neither `0x0040169F` nor
`0x0042D950` occurs as a 4-byte LE value anywhere in the file — but the packet
did not establish it.

**D3 — the `0x0042DA70` reacher list is short by one.** §2: "thunk
`0x00401C44`, from `0x00405A73`, `0x00405C54`, `0x0043DAEB`, `0x004AE863`".
There is a fifth: `0x004121A1: e9 9e fa fe ff  jmp 0x401c44`, a tail jump into
the destroy-all thunk at the end of a function that also calls `0x004017C6` and
logs `0x004C52B4`. Missing a `jmp`-form reacher is precisely the failure mode
the packet warns about elsewhere.

**D4 — "every field except the name" is false; the id is preserved too.**
§2 row `0x0042DA00` ("clear slot by id: zero every field except the name"), §3
step 3 ("zero `+0x34`, `+0x38`, `+0x30`, `+0x02`, `+0x32`, `+0x04`, `+0x08`,
`+0x0C` — every field except the name") and [[FUNC-97C95BA5572D-0042DB10]]
Confirmed all say it. None of the four clearing paths writes `+0x00`:
`0x0042DA10`-`0x0042DA3D`, `0x0042DB83`-`0x0042DBB0`,
`0x0042DAB0`-`0x0042DAD0` and `0x0042DD13`-`0x0042DD40` touch `0x005982E4`,
`0x005982E8`, `0x005982E0`, `0x005982B2`, `0x005982E2`, `0x005982B4`,
`0x005982B8`, `0x005982BC` and no other field. Correct wording: "every field
except the id at `+0x00` and the name at `+0x10`". The §1.1 table is already
consistent with the truth, so the prose contradicts the packet's own table.

**D5 — the second derivation is nine displacements, not eight, and the one it
drops is the one it most needed.** §1.1 lists eight destroy-pass operands and
says "**every one** consistent with the table above"; `EXP-20260817-185` says
"every one of its **eight** operand displacements resolves consistently";
[[Current State]] says "all eight". The destroy pass uses **nine** distinct
record-relative displacements. The missing one is `mov WORD PTR [esi-0x2],bx`
at `0x0042DAC0` → `+0x32` — a field whose §1.1 row is justified as "zeroed on
clear/delete", so the corroborating walk omits the very displacement that
corroborates it. (It does resolve: `0x34 - 0x02 = 0x32`.)

**D6 — the `+0x34` row's site list is incomplete.** §1.1: "in-use flag: set to
`1` at `0x0042DBE0`, tested at `0x0042DB26`, `0x0042DCB4`, `0x0042D992` and
`0x0042D9D4`". A fifth test exists: `cmp DWORD PTR [esi],ebx` at `0x0042DA80`,
the destroy-all pass's own gate. The row also omits that the flag is cleared at
`0x0042DA10`, `0x0042DAB0`, `0x0042DB83` and `0x0042DD13`, while every other
zeroed field's row does record that role.

**D7 — §0 under-attributes the generated prior art, and three of the four
"new" items are in it.** §0 says only: "**Prior art, generated:**
`ghidra-evidence.json` contains decompilations mentioning the principal
addresses used here." What that file actually contains, for `FUN_0042db10`,
`FUN_0042d980` and `FUN_0042da70`, is full decompiled bodies plus
per-instruction `data_references`, already rendering: the base
`&DAT_005982b0` with `* 0x3c` scaling and the `0xf`-dword copy loop; both
16-iteration loops (`iVar2 = 0x10`); the three code-pointer slots **as calls** —
`(**(code **)(&DAT_005982b4 + *param_1 * 0x3c))()`,
`(**(code **)(&DAT_005982bc + *param_1 * 0x3c))()` and `(*(code *)*puVar1)()`;
the in-use flag `&DAT_005982e4`; the current-record write
`_DAT_005982ac = puVar1 + -2`; the name argument as `param_1 + 8`; and all five
`EVENT` format strings by name. So of §0's four "what is new here" items —
"the table's base, stride and extent, the record layout including its **three**
callback slots, which entry points are live and which are dead, the two records
the executable actually registers, and the demonstration that this machinery is
disjoint" — the first two are prior art in the generated file. What is
genuinely new, and should be what §0 claims: the thunk-resolved caller and
dead-entry analysis (ghidra's `callers` arrays are **empty** for all three, and
it has no function entry at all for `0x0042D950`, `0x0042D9D0`, `0x0042DA00` or
`0x0042DCA0`), the decoded static records, the disjointness test, and the audio
cross-link. This is the same under-attribution defect the creature packet was
rejected for.

**D8 — "update" is a semantic field name with no evidence.** §1.1: "`+0x08`
... **called** at `0x0042D9A5` and tail-jumped at `0x0042D9E6` — the **update**
callback". `create` and `destroy` are anchored in the adjacent format strings
`0x004D82CC` ("create function %s called") and `0x004D8264` ("destroy function
%s called"). Nothing anchors `update`: `+0x08` is invoked with no log line, and
no callee was analysed. `CLAUDE.md` forbids naming a structure field from a
plausible reading, and `EXP-20260817-185` declares "**Inferred:** Nothing ...
The record field names — create, update, destroy — are descriptions of where
each pointer is called from, not assigned purposes", which is true of two of
the three and false of the third. Propagated to the coverage row,
[[Subsystems MOC]], `KU-071`, [[Current State]], both dossiers and the commit
message. Fix:
`+0x08` / "the callback the `0x0042D980` pass invokes", and move any "update"
reading to Inferred.

**D9 — inference inside a Confirmed set that declares itself inference-free.**
Besides D1 and D8:

- "a **32-byte** name at `+0x10`" — no instruction gives the width. It is
  bounded by the next accessed field at `+0x30`. The decoded records are
  consistent with 32 bytes; consistency is not a decoded field width. Belongs
  in Inferred, or state the derivation.
- "the **log-formatter** thunk (→ `0x004ADEA0`)" — asserted, never evidenced.
  §0 does not list `0x00401CF8` or `0x004ADEA0` among the addresses checked
  against prior art, and in `4e0157f^` neither appears in any authored note —
  only in `ghidra-evidence.json`. The name happens to be right (I read
  `0x004ADEA0`), which is luck, not method.

**D10 — `0x005982AC` is never read, and the export does not say so.** §1.1:
"`0x005982AC` ... holds the **current record pointer**, written at `0x0042D99A`
and `0x0042D9DA`". Both cited sites are `a3` stores. A whole-file 4-byte LE
scan finds exactly two occurrences of `0x005982AC` in the image, and they are
those two stores: nothing in the executable reads it. That negative is at least
as interesting as the writes and belongs in §1.1 or §6.

**D11 — the id is not bounds-checked, and the "16-slot table" model does not
say so.** All three id-scaled entry points read the id with `movsx` — a
**signed** word — and scale by `0x3C` with no range test: `0x0042DB18`
(register), `0x0042DA00` (clear) and `0x0042DCA8` (delete). Only the two
iterating passes are bounded, by `mov edi,0x10` / `mov ebp,0x10`. So the table
is 16 slots as *walked*, while the writers can address outside
`[0x005982B0, 0x00598670)` for any id outside `0..15`. §6 does not record this.

**D12 — runtime-flavoured wording in a packet that claims no runtime
behaviour.** §Scope: "This census claims **no** runtime behaviour." §4 is
headed "What the executable **actually registers**" and concludes "So the
executable statically registers **two** events, into slots 2 and 3". §4.1: the
`"DIRECTX"` create callback is "**invoked** at `0x0042DC2A` when the record is
registered", and "The audio and input subsystems **are therefore brought up as
an event callback**". Nothing here shows the enclosing function of
`0x0043DAEB`-`0x0043DB15` ever executes — §6 lists that function as
unanalysed — and the second registration sits behind
`cmp WORD PTR ds:0x59f7f0,bp` / `jne 0x43db0b`, whose meaning §6 also lists as
unknown. Two static registration **sites** exist; that is the static fact.

Minor, not counted in the twelve: §1.1's "`+0x10` ... passed as the `%s` of
every log line" — at the four two-`%s` sites it is only the *first* `%s`, and
inside `0x0042DB10` the pushed name comes from the caller's source buffer
(`[ebx+0x10]` at `0x0042DB50`, `0x0042DB77`, `0x0042DC13`, `0x0042DC34`), not
from the table record, so the "destroy function" line at `0x0042DB56` prints
the **incoming** record's name while calling the **outgoing** occupant's
`+0x0C`. And §1.1's "independently cross-checked" overstates: the destroy
pass's origin `0x00598668` can only be placed on `+0x34` by importing the base,
stride and flag offset from the first derivation, so it is a consistency check
in a different addressing form, not an independent one.

What survived unchanged, re-derived by me from the binary and not taken on
trust:

- SHA-256 re-hash, and the `objdump -h` section table exactly as §0 states.
- Base `0x005982B0` and stride `0x3C` from `0x0042DBC1`-`0x0042DBD5`
  (`mov ecx,0xf` / `lea edi,[eax*4+0x5982b0]`, `eax = id * 15`).
- **16 is a real bound, not an inference from the neighbour**: `mov edi,0x10`
  at `0x0042D988` and `mov ebp,0x10` at `0x0042DA79`. `0x005982B0 + 0x3C0 =
  0x00598670`, and `0x00598668 = 0x005982B0 + 15 * 0x3C + 0x34` with a `-0x3C`
  step.
- Every record displacement, in all four addressing forms present — id-scaled
  absolute, the destroy pass's `esi`-on-`+0x34` walk, the dispatch pass's
  `esi`-on-`+0x08` walk, and the caller-supplied pointer forms in `0x0042D9D0`
  (`[eax+0x34]`, `[eax+0x8]`) and `0x0042DCA0`. The layout in §1.1 is right.
- All seven extents, plus `0x0042DD90`. I scanned every direct branch in the
  whole image for targets in `[0x0042D950, 0x0042DD94]`: there are exactly
  **eight**, all `jmp`s from the `0x00401xxx` thunk table, none landing
  mid-function and none past a claimed end. No `ret` was mistaken for an end.
- Whole-file 4-byte LE scan for all seven function addresses and all eight
  thunks: zero hits. The dead-entry *conclusions* hold, including for
  `0x0042D950` (see D2 for why the packet did not earn it).
- The five `EVENT` strings, byte-exact, at the stated file offsets, each
  referenced only at the listed sites and nowhere else in the image.
- Both static records decoded byte-for-byte at `0x0D6DA8` and `0x0D6DE8`, id 2
  `"WINDOWS"` and id 3 `"DIRECTX"`, `+0x30`..`+0x3B` all zero; and all six
  callback thunks resolved — `0x00401A91`→`0x004AE580`,
  `0x00401AA5`→`0x004AE780`, `0x004017DA`→`0x004AE810`,
  `0x00401B04`→`0x0042BA60`, `0x004011D1`→`0x0042BB30`,
  `0x00401299`→`0x0042BB50`.
- §4's quoted `0x0043DAEB`-`0x0043DB10` block, byte-for-byte.
- §5 in both directions, and a stronger sweep than the one claimed: **no**
  dword anywhere in `0x0042D950`-`0x0042DD94` falls in `0x0041D000`-`0x0041F000`,
  `0x004C7000`-`0x004C9000` or `0x0059B000`-`0x0059E000`. The creature-side
  figures also match `SUBSYS-creature-actor-static-census.md` (26-entry table
  at `0x0041E848`, bodies `[0x004C7D00, 0x004C83F0)`, pool stride `0x84`,
  `+0x70` PC, `+0x60` wait counter, type-`0x23` records).
- §0's novelty negative against `4e0157f^`: every address in the list appears
  only in `ghidra-evidence.json`. That negative is sound; its companion
  attribution is not (D7). The audio prior-art quotations are verbatim and the
  §4.1 refinement is right — the `0x004D81E8` offsets in
  `SUBSYS-audio-static-census.md` are exactly right under the event layout, and
  the leading `3` is the id word, byte-compatible with the earlier "count of 3".
- Hygiene: `make vault-lint` 518 notes / 0 / 0; `make audit-tracked` 0
  violations; `make test` 686 passed in 17.69s. All three commit claims hold.

Could **not** verify: any runtime fact (none is claimed, correctly); whether
the enclosing function of `0x0043DAEB`-`0x0043DB15` ever runs, hence whether
either record is ever registered; whether any of these entry points is reached
by computed dispatch — my scans share the packet's blind spot and its §6 caveat
is the right one to keep; the procedural claims that extents were read and the
prior-art greps run before analysis, which artifacts cannot settle; and that no
`originals/` path, asset or PS1 source was touched.

The **Bounded** status itself is earned under the [[Subsystem Coverage Map]]
vocabulary — "real PC evidence at a documented boundary, with major parts open"
fits — but the row, [[Subsystems MOC]], `KU-071` and [[Current State]] all
carry D8's unsupported `update`, and [[Current State]] additionally carries D1
and D5. The propagation must be corrected with the export.

## New hypotheses

None.

## Contradictions discovered

One internal: §3's and §2's "every field except the name" contradicts §1.1's
own table, which correctly shows `+0x00` outside the zeroed set (D4).

## Tests run

`make vault-lint` 518 notes, 0 errors, 0 warnings; `make audit-tracked` 0
violations; `make test` 686 passed in 17.69s — all three run by me, logs read.
Binary work: `objdump -d -M intel` over the full image and over each cited
range, plus Python little-endian decoding of the two records, the five strings,
the section mapping and every whole-file absolute-value scan quoted above.

## Unresolved questions

`KU-071`; the six callback targets; whether any event is registered outside the
two static sites, and whether computed dispatch reaches any of these seven
entry points; the meaning of `+0x02`, `+0x30`, `+0x32`, `+0x38`, `0x0059F7F0`,
and of a `0x005982AC` that nothing reads.

## Recommended next action

Correct the export first — D1, D2, D3, D4, D5 are wrong or incomplete
statements about the binary and must be fixed in
`SUBSYS-event-static-census.md` before anything cites it — then D7's §0
paragraph, then D8 through D12. Propagate the same corrections to
`EXP-20260817-185`, both dossiers, [[Current State]],
[[Subsystem Coverage Map]], [[Subsystems MOC]] and `KU-071`. Re-audit
afterwards with fresh context.

## Git commit if applicable

None by the auditor. Nothing in the packet was modified.
