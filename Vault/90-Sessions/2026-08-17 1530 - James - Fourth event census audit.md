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

# Fourth event census audit

## Agent

James, fresh context, fourth audit of the event packet. No knowledge of the
three earlier rounds beyond the artifacts committed at `2c8c6aa`; every prior
auditor's finding was treated as a claim to re-test against the binary, not as
settled, including the corrections they caused.

## Goal

Judge `2c8c6aa`, which claims to fix the sixteen defects a third-round James
audit raised against `76f126c`. Three questions: did each of K1-K16 land in
**every** carrier and is each correct; are the two claims this round rewrote
most heavily — §2.1's relocation argument and the new `"bugs.log"`/`"at"`
anchor for `0x004ADEA0` — actually right; and what have all four rounds missed.
The model itself was re-derived from scratch rather than inherited.

## Files inspected

`CLAUDE.md`; [[START HERE]]; [[Agent Operating Manual]];
`static/exports/BIN-97c95ba5572dce63/SUBSYS-event-static-census.md`;
[[EXP-20260817-185 - PC event subsystem static census]];
[[FUNC-97C95BA5572D-0042DB10]]; [[FUNC-97C95BA5572D-0042D980]];
[[2026-08-17 1130 - Claude - PC event subsystem census]];
[[2026-08-17 1230 - James - Event census audit]];
[[2026-08-17 1330 - James - Second event census audit]];
[[2026-08-17 1430 - James - Third event census audit]]; the full `2c8c6aa` diff
including [[Current State]], [[Subsystem Coverage Map]], [[Subsystems MOC]],
[[Functions MOC]], `KU-071` in [[Known Unknowns]] and [[Session Index]]; the
trees `4e0157f`, `311f79b` and `4e0157f^` for the earlier drafts and the
novelty negative; the prior art the packet cites —
`SUBSYS-audio-static-census.md`, `SUBSYS-creature-actor-static-census.md`,
[[EXP-20260816-159 - PC audio subsystem static census]]; the generated
`static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json`, parsed as JSON and
its bodies read in full; and `work/copies/BUGS_PC-full-disc/bugs.exe`, re-hashed
to `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.

## Experiments inspected

`EXP-20260817-185` (the packet), `EXP-20260816-159` (the `0x004D81E8` prior art)
and `EXP-20260816-172` via the creature export (the row's earlier anchor).

## Changes made

None. This note only. No packet artifact was touched and nothing was committed.

## Conclusions

**REJECT.** Eight defects, plus four smaller ones.

The model is right and I re-derived all of it independently: the table geometry,
the record layout in both addressing forms, all seven extents, the eight thunk
edges, the nine reachers, both decoded records, the five strings, the
disjointness result, **and** — new this round — the relocation argument, which I
reproduced number for number. Thirteen of the sixteen round-3 fixes are correct
and complete.

But the round's own headline finding failed to propagate to three carriers, and
the packet now holds **two contradictory positions on whether the log-formatter
reading is an inference** — the export and one dossier say it is not, the
experiment note and the session note say it is. That is the fourth consecutive
round of the same partial-propagation failure, and this time it lands on the
Confirmed/Inferred boundary itself. Worse, three of the round-3 fixes introduced
**new** factual errors that the audit which requested them had stated correctly:
a wrong instruction address, a wrong instruction placement, and a wrong
description of the prior-art file.

### Part A — the sixteen fixes, re-verified

Correct and complete:

- **K1.** §2.1 now reads 47/all-inside against `[0x005982A0, 0x005986F0)`, with
  52 named as the widened figure. Both numbers are right (see Part C).
- **K2.** The false causal clause is gone and the three sites are correctly
  split — but the replacement carries a wrong address (L2) and a broken
  sentence (L5).
- **K3.** [[FUNC-97C95BA5572D-0042DB10]]'s Confirmed set now says zero-then-log,
  with the store run `0x0042DB83`-`0x0042DBB0` and the log call at
  `0x0042DBB6`. Verified.
- **K4.** `EXP-20260817-185`'s Confirmed set now says "at all eight log calls —
  though only two of them (`0x0042DAA5`, `0x0042DAD3`) take it from the *table*
  record, the other six from the caller's", and adds the `0x005982C0`
  zero-occurrence fact. Both verified.
- **K5.** §2's `0x0042D950` row now reads "zeroes 128 bytes at `0x00598670`
  (the width of the write; the buffer's own extent is not given)".
- **K6.** [[Subsystems MOC]] now carries the 7-of-9 prior-art correction.
- **K7.** §2.1 names its method. The method is genuinely stronger than a scan —
  but its stated limits are still short by one (L7).
- **K9.** [[Current State]]'s audit history is now a per-round list covering all
  three rejections, matching the creature packet's precedent. The counts 12/10/16
  are right.
- **K10.** The [[Subsystem Coverage Map]] row now reads "corrected after three
  James rejections".
- **K11.** §2.1's result now exists in `EXP-20260817-185`'s Confirmed set.
- **K13.** §0's novelty negative is now scoped to `4e0157f^` and says so
  explicitly. I re-ran it: all fifteen addresses return zero hits across
  `Vault/` and the markdown exports at `8403e02`.
- **K14.** Verified against both trees. `4e0157f` said only
  "`ghidra-evidence.json` contains decompilations mentioning the principal
  addresses used here" and made no `callers` claim; `311f79b` is where "the
  `callers` list is empty for all three functions it does carry" appears. §0's
  corrected attribution is exactly right.
- **K16.** §1.1's preamble no longer says "independently" at the point of
  assertion — but the sentence that replaced it asserts something false (L6).

Landed but wrong: **K2** (L2, L5), **K15** (L3), **K8** (L1, L4, L8).

### Part B — the numbered defects

**L1 (severe) — the round's headline fix reached the export and one dossier and
nothing else, and the packet now states both sides of its own
Confirmed/Inferred boundary.** §2 and [[FUNC-97C95BA5572D-0042DB10]] now declare
the reading is no longer an inference ("That is a decoded byte anchor, not an
interpretation"; "## Inferred — Nothing. The log-formatter reading is no longer
an inference"), and the commit message says "One of the packet's two remaining
inferences is removed." Three carriers were not swept:

- `EXP-20260817-185` **### Inferred** still reads: "Two things, both flagged
  inline above and in the export: ... the reading of `0x004ADEA0` as a **log
  formatter**." This is the note that carries the packet's Confirmed / Inferred
  / Unknown classification and names the export as its artifact, so the
  classification of record now contradicts the artifact of record. Its clause
  "both flagged inline above and in the export" is separately false — the export
  flags only the 32-byte width. The same note's own Confirmed set, twenty lines
  above, says `0x004ADEA0` "writes `"bugs.log"`". One file, two positions.
- [[2026-08-17 1130 - Claude - PC event subsystem census]] **## New hypotheses**
  still reads "Two, both flagged in the export: the 32-byte width ... and the
  reading of `0x004ADEA0` as a log formatter" — contradicted by its own "###
  Third round" section sixteen lines below ("The log formatter is no longer an
  inference at all").
- [[Current State]] line 3490 still reads "(→ `0x004ADEA0`, **read as a log
  formatter**)" — the exact pre-K8 framing — while lines 3532 and 3554 of the
  same file record that the reading is prior art and that round 3 corrected it.

J-round lesson, K-round lesson, and now L-round evidence: the "scripted phrase
sweep across all ten carriers" the commit message describes did not find these
because it swept the *defect* phrase. The third-round audit's closing
recommendation was explicit about this — "grep the **corrected** phrasing, not
the defect phrasing" — and it was not done.

**L2 (severe) — the K2 fix introduced a wrong instruction address, in two
carriers.** Export §3: "At `0x0042DBB6` it is `lea edx,[ebx+0x10]`
(`0x0042DB6E`)". [[FUNC-97C95BA5572D-0042DB10]] Confirmed: "The name that log
line prints is the **caller's** (`lea edx,[ebx+0x10]` at `0x0042DB6E`)".

```text
42db6e: 0f bf 03    movsx eax,WORD PTR [ebx]
42db71: 8d 53 10    lea   edx,[ebx+0x10]
```

`0x0042DB6E` is the `movsx`. The `lea` is at **`0x0042DB71`**. Worse,
`0x0042DB6E` is a real and different landmark in the same function — it is the
`je 0x42db6e` target from `0x0042DB38`, the skip-the-destroy-callback edge — so
the wrong citation reads as deliberate. The third-round audit that requested
this correction gave
`0x0042DB71` correctly in its own K2 bullet; the fix transcribed it wrong. In a
document whose entire method is address-anchored, a wrong address is not a
typo — it is an unverifiable citation.

**L3 (moderate) — the K15 fix states an instruction placement the binary
contradicts.** §1.2 now reads: "The scaling is not always contiguous with the
read — at `0x0042DB18` an `xor` and two `push`es are interleaved, and at
`0x0042DA00` an `xor`."

At `0x0042DB18` only two `push`es intervene (`0x0042DB1B` `push esi`,
`0x0042DB1C` `push edi`) before the first `lea` at `0x0042DB1D`. The
`xor ebp,ebp` is at `0x0042DB16`, **before** the `movsx`, and it is the
zero-register setup for the later `cmp`s, not part of this sequence. The K15
bullet said exactly this ("at `0x0042DA00` an `xor ecx,ecx` intervenes
(`0x0042DA05`) and at `0x0042DB18` two `push`es do"); the fix attached the `xor`
to the wrong site. The substantive claim underneath — no `cmp` between the read
and the first access at any of the three — is correct, and I re-verified it.

**L4 (moderate) — §0 mis-describes the prior-art file, in the paragraph added to
credit it.** §0: "`FUN_004adea0` and `thunk_FUN_004adea0` ... whose bodies render
... the `FUN_004b0150(buf, fmt, &stack)` call, and `s_bugs_log_004e9264` passed
to `FUN_004b0730`/`FUN_004b13a0`/`FUN_004b04e0`."

The body in `ghidra-evidence.json` is:

```text
FUN_004b13e0(s_bugs_log_004e9264);
iVar1 = FUN_004b0730(s_bugs_log_004e9264,&DAT_004e9260);
if (iVar1 != 0) {
  FUN_004b13a0(iVar1,local_400);
  FUN_004b04e0(iVar1);
}
```

The string is passed to **two** functions, `FUN_004b13e0` and `FUN_004b0730`.
`FUN_004b13a0` and `FUN_004b04e0` receive `iVar1`, the returned handle. And the
one call the string *is* passed to that the packet never mentions anywhere —
`FUN_004b13e0`, guarded by `DAT_004e9170` and reached by the third push of
`0x004E9264` at `0x004ADEE5` — is dropped from the description entirely. This is
the fourth successive round in which a statement about this file is wrong, and
the second in which the error is in the sentence written to fix the previous
one.

**L5 (moderate) — the K2 edit left a spliced sentence with a dangling
referent, in the step that carries the `+0x00`/`+0x10` preservation claim.**
§3 step 3 now ends:

> Only `0x0042DAD3` reads the table record, via `lea ecx,[esi-0x24]` at
> `0x0042DABD`, and only there does the surviving name matter; None of the
> four writes `0x005982B0` or the name block;

Capitalised "None" after a semicolon is the visible seam. The substantive
problem is the referent: "the four" now sits in a paragraph about *three* log
calls, two paragraphs after the four clearing paths were last named. The
statement itself is true — I confirmed `0x005982B0` occurs exactly once in the
image, at `0x0042DBD1`, the `rep movs` destination, and none of the four clear
runs touches it or `+0x10` — but the sentence carrying it has been severed from
its subject by a string substitution. Four lines in the export are now unwrapped
at exactly the round-2 and round-3 fix sites (lines 91, 166, 224, 406), which is
the same signature.

**L6 (moderate) — §1.1's new preamble asserts a third limit that is false and
that the two stated limits do not contain.** The preamble: "The cross-check is
**not fully independent** — its origin is imported from the first derivation —
and it does not reach `+0x00` **or supply `+0x10`'s only access form**; see the
two limits stated below the table".

The destroy pass *does* supply `+0x10`'s access form, and it is the only place
in the image that reaches the **table** record's name: §1.1's own `+0x10` row
cites `lea` from `[esi-0x24]` at `0x0042DA9C` and `0x0042DABD`, both inside that
pass, and §1.1's own log-argument split says those two calls (`0x0042DAA5`,
`0x0042DAD3`) are the only two of eight that take the name from the table. So
the clause contradicts the row it introduces. The two limits actually stated
below the table are (a) nine of ten fields, `+0x00` untouched and (b) the
imported origin; neither is the clause promised. K16 asked for the independence
overstatement to be qualified; the qualification that arrived is a new wrong
statement.

**L7 (moderate) — §2.1's method is sound and its numbers are right, but the two
stated limits do not cover the gap its own filter has.** I reproduced the whole
argument independently (Part C). The gap is in the step from result to
conclusion.

The relocation table is an exhaustive enumeration of absolute 32-bit reference
**values**. §2.1 then filters those values by `[0x005982A0, 0x005986F0)` and
concludes "no instruction anywhere outside these seven functions holds an
absolute reference to the table, the flag, the current-record global or the
buffer." An instruction can hold a relocated absolute base *outside* that range
and reach inside it by register index or displacement; its relocation value
falls outside the filter and the enumeration never sees it. This is not a
contrived form — it is the form the subsystem itself uses everywhere:
`mov DWORD PTR [eax+0x5982e4],ecx` at `0x0042DA10` is a relocation value plus a
register. Had the compiler hoisted `0x00598000` into a register, §2.1's sweep
would return zero and the section would claim closure.

The two limits stated are "the computed form" and "the exclusion of
`0x00598290`". Neither names this. For the record, the *result* is safe for this
binary: I swept all relocation values in `[0x00597000, 0x0059A000)` and there is
nothing at all between `0x00598290` and `0x005987D0`, so no base below or inside
the table exists to index from. But §2.1 is written as a proof — "provably
exhaustive", "so none can be hidden" — and the proof as written does not close.

**L8 (moderate) — "`0x004ADEA0` writes the game's log file" is an unqualified
behavioural claim resting on unnamed functions, and it reintroduces D12/K12's
failure mode.** Three problems, all in the same three sentences of §2.

1. **The whole body is gated and no carrier says so.** `0x004ADEA0` opens with
   `mov eax,ds:0x8620ac` / `sub esp,0x400` / `test eax,eax` / `je 0x004ADF2A` at
   `0x004ADEA0`-`0x004ADEAF`. When that global is zero the function formats
   nothing, opens nothing and writes nothing. `KU-071`'s "it appends to
   `"bugs.log"`" and `EXP-185`'s "which writes `"bugs.log"`" carry the same
   unqualified reading. The packet is otherwise scrupulous about exactly this
   ("whether either ever executes is **not** established"); the standard was not
   applied here.
2. **Three unidentified functions are given semantic roles.** "the `0x004B0730`
   call whose result is written to and closed" names `0x004B0730` as an open,
   `0x004B13A0` as a write and `0x004B04E0` as a close. None is an import, none
   is decoded, none is analysed anywhere in the packet. Reading `"at"` as
   "an append-text mode string" is C-runtime convention applied to two decoded
   bytes. `CLAUDE.md`: "Do not rename unidentified functions or structure fields
   merely because a semantic interpretation seems plausible."
3. **"That is a decoded byte anchor, not an interpretation" over-claims.** The
   two strings are decoded bytes; "writes the game's log file" is the
   interpretation built on top of them, and it is a good one — but it is an
   interpretation, which is precisely why `EXP-185` still lists it under
   Inferred. The packet holds both positions and, contrary to the Operating
   Manual, records the contradiction nowhere.

The honest form is available and costs nothing: *`0x004ADEA0` pushes two decoded
strings, `"bugs.log"` and `"at"`, into `0x004B0730` at `0x004ADEFB`-`0x004ADF05`
and passes the returned value to `0x004B13A0` and `0x004B04E0`; the whole body
is gated on `0x008620AC`. The `fopen`/`fputs`/`fclose` reading is inference from
shape and convention.*

### Smaller, also wrong

- **L9.** [[Current State]]: "Round 3 also produced the packet's strongest
  closure result. All 26,713 type-3 base relocations were decoded: exactly 47
  point into ... and all 47 lie inside the seven functions." The export §2.1 and
  `EXP-185` both credit the 47/all-inside result to the **second**-round audit
  ("Found by the second-round audit and re-derived here by two methods"); round
  3 supplied the relocation *method*. Current State gives round 3 both. Same
  attribution axis as J1, K8 and K14, in the note that is the project's handoff
  surface.
- **L10.** The [[Subsystem Coverage Map]] row was not swept with the others. It
  still reads "Table geometry, layout and 7 of the 9 reachers are present in
  `ghidra-evidence.json`" — no log-formatter reading — and "new are the four dead
  entry points, two omitted reachers, the decoded records, the disjointness
  result and the negatives" — no relocation closure result. [[Current State]] and
  [[Subsystems MOC]] both carry both additions. One carrier short, the identical
  shape of K6, J1 and D7.
- **L11.** `KU-071`: "the subsystem's only outbound call, `0x004ADEA0`, is no
  longer unknown". §2's careful wording is "the only outbound **branch** target",
  i.e. the only *direct* one. The subsystem also makes six indirect outbound
  calls — `call [ecx*4+0x5982b4]`, `call [ecx*4+0x5982bc]` twice,
  `call [esi-0x28]`, `call eax`, `jmp eax` — and what those reach is the
  principal thing `KU-071` exists to record. Dropping "branch" makes the
  narrowing claim swallow the unknown it sits next to.
- **L12.** "immediately" survives K15 in four carriers. §1.1's `+0x04` row
  ("**called** at `0x0042DC2A`, immediately after the log string"), its `+0x0C`
  row ("each immediately after the log string"), `EXP-185`'s Confirmed set
  ("each call is immediately preceded by the log string") and [[Current State]]
  line 3470 ("taken from the log strings that immediately precede those calls").
  Four instructions separate the log call at `0x0042DB56` from the `+0x0C` call
  at `0x0042DB67`, four separate `0x0042DCE5` from `0x0042DCF6`, and one
  separates `0x0042DAA5` from `0x0042DAAD`. K15 rejected "followed directly" for
  exactly this class of adjacency wording three sections away in the same file.

### Part C — the two rewritten claims, re-derived from scratch

**§2.1's relocation argument — numbers correct, reasoning short one limit.**
Everything below is mine, from the file:

- PE header: `e_lfanew 0x80`, image base `0x00400000`, `.reloc` at RVA
  `0x00468000`, raw pointer `0x000EF000`, `SizeOfRawData 0x11800`,
  `VirtualSize 0x11668`. The **BASERELOC data directory** gives size
  `0x0000D7F8`; the block walk consumes exactly `0xD7F8` and the remainder of
  the section is zero, so all three figures decode identically. The export's
  "size `0x11800`" describes the section on disk and is harmless.
- 208 blocks, **26,713** type-3 (`HIGHLOW`) entries and 99 type-0 padding
  entries. The count matches exactly.
- Dereferencing every type-3 site: **47** hold a value in
  `[0x005982A0, 0x005986F0)`. Site range `0x0042D959`-`0x0042DD42` — **all 47
  inside `0x0042D950`-`0x0042DD94`, none outside**. Value histogram:
  `AC`×2, `B0`×1, `B2`×3, `B4`×5, `B8`×4, `BC`×7, `E0`×3, `E2`×3, `E4`×6,
  `E8`×3, `0x00598668`×1, `0x00598670`×9.
- Independent whole-file 4-byte little-endian scan at every byte offset
  (headers, all six sections and the 0x4800-byte overlay): **47** hits, all in
  `.text`, all inside the same range. Hit for hit with the relocation method.
- Widening the low bound to `0x00598290`: **52**, the extra five at operand
  offsets `0x00405C0D`, `0x00405C83`, `0x0043DF67`, `0x0043DFB1`, `0x004AE8F9`.
  Disassembled: `0x00405C0C` `mov eax,ds:0x598290` and `0x00405C82`
  `mov eax,ds:0x598290` (reads); `0x0043DF65` and `0x0043DFAF`
  `mov DWORD PTR ds:0x598290,ebx` and `0x004AE8F7`
  `mov DWORD PTR ds:0x598290,0x1` (writes). §2.1's read/write split is right.

The premise — a PE loader must relocate every absolute 32-bit reference — is
sound for a non-`RELOCS_STRIPPED` image, and the enumeration is genuinely
exhaustive **over reference values**. The gap is L7: exhaustive over values is
not exhaustive over references that *reach* a range.

**The `"bugs.log"`/`"at"` anchor — bytes correct, conclusion still carrying
inference.**

- `0x004E9264` → file `0x0E7E64` → `62 75 67 73 2e 6c 6f 67 00` = `"bugs.log"`.
  `0x004E9260` → file `0x0E7E60` → `61 74 00` = `"at"`. Both decoded by me from
  the file, both below `.data`'s raw end `0x004ED400`, so the scope section's
  "no file bytes are decoded above `0x004ED400`" holds.
- `0x004ADEFB: 68 60 92 4e 00 push 0x4e9260`; `0x004ADF00: 68 64 92 4e 00
  push 0x4e9264`; `0x004ADF05: e8 26 28 00 00 call 0x4b0730`. The stated range
  `0x004ADEFB`-`0x004ADF05` is exact. Under cdecl the arguments are
  (`"bugs.log"`, `"at"`) in that order, which is `fopen`'s signature.
- A **third** push of `0x004E9264` exists at `0x004ADEE5`, into `0x004B13E0`,
  guarded by `cmp WORD PTR ds:0x4e9170,0x0`. No carrier mentions it (L4).
- The entire body is gated on `0x008620AC` (L8).

So the anchor is real and it is a large improvement. What it establishes is that
this function names `bugs.log`; that it *writes the game's log file* still rests
on identifying three unnamed callees by shape.

## What I re-derived and confirm

- SHA-256 re-hashed to
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`. `objdump
  -h` and the PE section table match §0 exactly; `.data` raw ends at
  `0x004C1000 + 0x2C400 = 0x004ED400` and its virtual extent reaches
  `0x00863970`, so `0x00598290` is `.bss`-class and is the lowest such address
  the document cites.
- Base `0x005982B0` and stride `0x3C` from `0x0042DBBE`-`0x0042DBD5`; §1's
  quoted block is byte-exact including the `; eax = id * 15` comment. The 16
  bound from `mov edi,0x10` at `0x0042D988` and `mov ebp,0x10` at `0x0042DA79`;
  `0x005982B0 + 0x3C0 = 0x00598670`.
- The whole §1.1 layout, in every addressing form, and the ten rows summing to
  exactly `0x3C`. The destroy pass's origin `0x00598668 = 0x005982B0 + 15 *
  0x3C + 0x34`, step `-0x3C`, and its **nine** distinct displacements
  (`[esi]`, `[esi+0x4]`, `[esi-0x2]`, `[esi-0x4]`, `[esi-0x24]`, `[esi-0x28]`,
  `[esi-0x2c]`, `[esi-0x30]`, `[esi-0x32]`) resolving as stated. The `+0x34`
  row's set/test/clear lists are exhaustive as written.
- `0x005982C0`: zero occurrences whole-file. `0x005982AC`: exactly two, the `a3`
  store immediates at `0x0042D99A` and `0x0042D9DA`; never read.
- §1.2: `movsx` at `0x0042DA00`, `0x0042DB18`, `0x0042DCA8`, all signed, no
  `cmp` between the read and the first access in any of the three; only the two
  passes bounded.
- All seven extents, each with a single `ret`, and `0x0042DD90` as a bare `ret`
  after `int3` padding. File offsets under `VMA - 0x400C00`. Every direct branch
  inside each range enumerated: the only outbound target is `0x00401CF8`.
- The eight `call 0x401cf8` sites; the 4-of-8 clear split, with clears at
  `0x0042DA9A`, `0x0042DB4B`, `0x0042DC0E`, `0x0042DCD5` preceding calls at
  `0x0042DAA5`, `0x0042DB56`, `0x0042DC19`, `0x0042DCE5`, and those four being
  exactly the two-`%s` formats. `0x00598670` pushed first at each, i.e. the
  second `%s`.
- The eight thunks resolved (`0x0040169F`, `0x004013AC`, `0x0040179E`,
  `0x00401217`, `0x00401C44`, `0x004017B2`, `0x00401140`, `0x00401CF8`) and the
  four dead pairs: zero direct branches to any of the four thunks, and all eight
  whole-file little-endian scans return zero. The nine reachers, from a
  branch-target index over the whole `.text`:
  `0x00405CB0`/`0x0043DC5A` → `0x004013AC`;
  `0x00405A73`/`0x00405C54`/`0x0043DAEB`/`0x004AE863` (calls) and `0x004121A1`
  (`e9` tail `jmp`) → `0x00401C44`; `0x0043DAF5`/`0x0043DB10` → `0x004017B2`.
- All five `EVENT` strings byte-exact at `0x0D6E3C`, `0x0D6E64`, `0x0D6EA4`,
  `0x0D6ECC`, `0x0D6F0C`, `%s` counts 1/2/1/2/1, and each referenced **exactly**
  at the sites §3 lists and nowhere else — whole-file scan, 1/3/1/1/2
  occurrences. §3's "and nowhere else" is earned.
- Both records byte-for-byte at file `0x0D6DA8` and `0x0D6DE8`: ids 2 and 3,
  `+0x02` zero, `+0x30`..`+0x3B` zero, `"WINDOWS"`/`"DIRECTX"` at `+0x10` with
  the rest of the 32-byte block zero, and all six callback thunks resolved as
  stated. §4's quoted `0x0043DAEB`-`0x0043DB10` block is byte-exact and
  `jne 0x43db0b` does land on the `push 0x4d81e8`.
- §5 in both directions, and under a wider sweep: no dword anywhere in
  `0x0042D950`-`0x0042DD90` falls in the creature interpreter, program-store or
  pool ranges, and no dword in `0x0041DC60`-`0x0041E845` falls anywhere in
  `[0x00598290, 0x005986F0)`. The creature-side figures match
  `SUBSYS-creature-actor-static-census.md`: 26-entry table at `0x0041E848`,
  bodies `[0x004C7D00, 0x004C83F0)` (40 variable-length programs, so the range
  is not a stride), pool `[0x0059B628, 0x0059D728)` stride `0x84`, `+0x70`
  program counter, `+0x60` wait counter, type-`0x23` records.
- `ghidra-evidence.json`, parsed as JSON: exactly six entries for `0x0042D980`,
  `0x0042DA70`, `0x0042DB10` with the three `thunk_FUN_` `callers` lists as §0
  tabulates and the three `FUN_` lists empty; **zero** occurrences of the
  substrings `0042d950`, `0042d9d0`, `0042da00`, `0042dca0`, `004ae863` and
  `004121a1` anywhere in the 8 MB file; `FUN_0042db10`'s body rendering two
  slots as calls, `&DAT_005982b8` only as a zero-store, four of the five format
  strings, `param_1 + 8`, `&DAT_00598670` with its `0x20` loop and the seven
  named field clears; `thunk_FUN_0042d980` rendering
  `_DAT_005982ac = puVar1 + -2` and `iVar2 = 0x10`; `thunk_FUN_004adea0`'s
  `callers` containing six of the eight log-call sites, all but `0x0042DCE5`
  and `0x0042DD46`. Every one of §0's ghidra claims is right except L4.
- §0's authored prior-art quotations are verbatim from
  `SUBSYS-audio-static-census.md` (the "Indirect dispatch record" section and
  its `0x004D81E8`/`EC`/`F0`/`F4`/`F8` layout) and `EXP-20260816-159`; the §4.1
  refinement is right and byte-compatible (`+0x02` is zero, so a dword read
  yields 3 either way).
- The novelty negative at `4e0157f^` (`8403e02`): all fifteen addresses, zero
  hits, case-insensitive, across `Vault/` and the markdown exports.
- Hygiene: `make vault-lint` **521 notes, 0 errors, 0 warnings**;
  `make audit-tracked` **0 violations** — both run by me. The commit's figures
  are accurate. I did not re-run `make test`; the packet changed no code and the
  commit says the 686/17.54s figure was taken from the log.

**Bounded remains earned.** "Real PC evidence at a documented boundary, with
major parts open" still fits. None of L1-L12 touches the geometry, the layout,
the extents, the records, the disjointness result or §2.1's numbers. Four
auditors have now re-derived the model independently and it has held every time.

## New hypotheses

None.

## Contradictions discovered

Four, all internal to the packet and all live in the committed tree:

1. `EXP-20260817-185`'s Inferred set ("the reading of `0x004ADEA0` as a **log
   formatter**") against the export §2 ("not an interpretation") and
   [[FUNC-97C95BA5572D-0042DB10]] ("no longer an inference") — L1.
2. `EXP-20260817-185`'s Inferred set against its own Confirmed set twenty lines
   above, which states `0x004ADEA0` "writes `"bugs.log"`" — L1.
3. [[2026-08-17 1130 - Claude - PC event subsystem census]]'s "New hypotheses"
   against its own "Third round" section — L1.
4. §1.1's preamble ("does not ... supply `+0x10`'s only access form") against
   §1.1's own `+0x10` row, which cites the destroy pass's `[esi-0x24]` at
   `0x0042DA9C` and `0x0042DABD` as exactly that — L6.

## Tests run

`make vault-lint` 521 notes, 0 errors, 0 warnings; `make audit-tracked` 0
violations — both run by me, output read. Binary work, all mine: `sha256sum`;
`objdump -h`; `objdump -d -M intel` over `0x0042D940`-`0x0042DDA0`,
`0x004ADE90`-`0x004ADFA0`, `0x0043DAEB`-`0x0043DB16`, the five `0x00598290`
sites and every cited thunk; `rabin2 -S`/`-I`; a Python PE-header parser
reading the section table and all sixteen data directories; a full decode of the
base relocation directory (208 blocks, 26,713 type-3, 99 type-0) with every
site dereferenced; whole-file 4-byte little-endian scans at every byte offset
for the table range, the widened range, a `[0x00597000, 0x0059A000)` near-miss
band, all seven functions, all eight thunks, all five strings, both records and
all four disjointness address sets; a branch-target index over `.text` for `e8`
and `e9` forms; byte decoding of the two records, the seven strings and the
section mapping; and `ghidra-evidence.json` parsed as JSON with all six event
entries, both `004adea0` entries, their `callers`, `callees` and
`data_references` read in full.

## Unresolved questions

`KU-071`; the six callback targets; whether any event is registered outside the
two static sites; whether a computed dispatch or a base-plus-index absolute
reference reaches any of these seven functions — my methods share the packet's
blind spot on the first and L7 names the second; what `0x008620AC` and
`0x004E9170` gate in `0x004ADEA0`; the meaning of `+0x02`, `+0x30`, `+0x32`,
`+0x38`, `0x0059F7F0` and of a `0x005982AC` nothing reads; the true extent of
the buffer at `0x00598670`. Not verifiable from artifacts: that the prior-art
greps and extent reads happened before analysis, that `make test` was run at
686/17.54s, and that no `originals/` path, asset or PS1 source was touched.

## Recommended next action

Fix L1 first: it is a live contradiction on the Confirmed/Inferred boundary in
the note that owns that classification. Decide which position the packet holds —
L8 argues the `EXP-185` position is the defensible one, with the anchor stated
as decoded bytes and the `fopen`/`fputs`/`fclose` reading kept as inference —
and then make **all** carriers say it, including [[Current State]] line 3490 and
the session note's "New hypotheses".

Then L2 and L3, which are wrong addresses and a wrong instruction placement
introduced by fixes whose source audit had both right; then L4, L5, L6; then L7
and L8's caveats; then L9-L12.

Before committing, do the thing the last two commit messages promised and the
last audit spelled out: grep the **corrected** phrasing across `Vault/` and
`static/exports/`, not the defect phrasing. L1, L9 and L10 are all places where
the new wording is *absent*, which no defect-phrase sweep can find. And re-read
each edited paragraph as prose afterwards — L5's spliced sentence and the four
unwrapped lines are the signature of substitution without reading.

The lesson this round adds: **a fix is a new claim, and this round's three worst
defects are all fixes that got a fact wrong which the audit requesting them had
stated correctly.** Copying a correction is not verifying it.

## Git commit if applicable

None by the auditor. Nothing in the packet was modified.
