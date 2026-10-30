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

# Sixth event census audit

## Agent

James, fresh context, sixth audit of the event packet. No knowledge of the five
earlier rounds beyond the artifacts committed at `671acad`. Every prior
auditor's finding — including the five acceptances of the underlying model —
was treated as a claim to re-test against the binary, not as settled.

## Goal

Judge `671acad`, which claims to fix the fifteen defects a fifth-round James
audit raised against `b69cbb2`. Three questions: did each of M1-M15 land in
**every** carrier and is each correct; are the two things this round changed
most — the `DeleteFileA` promotion and §2.1 restated — right and honestly
scoped; and what have all six rounds missed. The model was re-derived from the
binary rather than inherited.

## Files inspected

`CLAUDE.md`; [[START HERE]]; [[Agent Operating Manual]];
`static/exports/BIN-97c95ba5572dce63/SUBSYS-event-static-census.md`;
[[EXP-20260817-185 - PC event subsystem static census]];
[[FUNC-97C95BA5572D-0042DB10]]; [[FUNC-97C95BA5572D-0042D980]];
[[2026-08-17 1130 - Claude - PC event subsystem census]]; the five prior audits
[[2026-08-17 1230 - James - Event census audit]],
[[2026-08-17 1330 - James - Second event census audit]],
[[2026-08-17 1430 - James - Third event census audit]],
[[2026-08-17 1530 - James - Fourth event census audit]] and
[[2026-08-17 1630 - James - Fifth event census audit]]; the full `671acad` diff
including [[Current State]], [[Subsystem Coverage Map]], [[Subsystems MOC]],
[[Functions MOC]], `KU-071` in [[Known Unknowns]] and [[Session Index]]; a
`4e0157f^` worktree for the novelty negative; the prior art the packet cites —
`SUBSYS-audio-static-census.md`, `SUBSYS-creature-actor-static-census.md`,
[[EXP-20260816-159 - PC audio subsystem static census]]; the generated
`static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json`, parsed as JSON with
the relevant bodies read in full; and `work/copies/BUGS_PC-full-disc/bugs.exe`,
re-hashed to
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.

## Experiments inspected

`EXP-20260817-185` (the packet), `EXP-20260816-159` (the `0x004D81E8` prior art)
and `EXP-20260816-172` via the creature export.

## Changes made

None. This note only. No packet artifact was touched and nothing was committed.

## Conclusions

**REJECT.** Five substantive defects, five moderate, four smaller.

The model is right, and I re-derived all of it independently from the binary:
table geometry, the record layout in both addressing forms, all seven extents
and their single `ret`s, the eight thunk edges, the nine reachers, the four dead
entry points, both decoded records, the five strings and their exclusivity, the
disjointness result, and every number in §2.1 by two methods. Six auditors have
now re-derived this model and it has held every time. Nothing below touches it.

Two of this round's headline changes are right in substance. `0x004B13E0` does
reach `KERNEL32.dll!DeleteFileA`; §2.1's restatement is arithmetically exact and
its scoping is honest. But the sentence written to establish the first
mis-describes the function at the instruction address it cites, and four
carriers still say the opposite of what the packet now concludes.

Three failure modes recur, all of them named by earlier rounds:

1. a fix that asserts something false about the artifact it describes (D1);
2. one file asserting both sides of the Confirmed/Inferred boundary (D2, D3) —
   M4's exact finding, reproduced in the round that fixed M4;
3. a correction that reaches the export and stops (D4, D8, D9, D12).

### Part A — the fifteen fixes, re-verified

Correct and complete:

- **M1.** §2.1 no longer contains the "none lies between" sentence at all; the
  section is restated. I re-decoded the directory: exactly **twelve** distinct
  relocated values lie strictly between `0x00598290` and `0x005987D0`
  (`0x005982AC`, `B0`, `B2`, `B4`, `B8`, `BC`, `E0`, `E2`, `E4`, `E8`,
  `0x00598668`, `0x00598670`), so the withdrawn sentence was indeed false. The
  replacement makes no claim about that interval.
- **M2.** The closure claim is gone from the export and from `EXP-185`. The
  replacement figures are all mine and all exact: 6,473 distinct relocated
  values image-wide, **4,673** below `0x005982A0`, **1,788** at or above
  `0x005986F0`, 12 inside — 4,673 + 1,788 + 12 = 6,473. It does **not** reach
  three other carriers (D4).
- **M5.** [[Current State]] line 3470 now reads "taken from log calls a few
  instructions before them". Verified: four instructions separate `0x0042DB56`
  from `0x0042DB67`, `0x0042DCE5` from `0x0042DCF6` and `0x0042DC19` from
  `0x0042DC2A`; one separates `0x0042DAA5` from `0x0042DAAD`.
- **M6.** The scope section now names `0x00597000`/`0x0059A000` explicitly. I
  extracted every hex literal in the document above `.data`'s raw end
  `0x004ED400`: the lowest is `0x00597000`, and it is now accounted for. The
  fix introduces a different problem (D7).
- **M7.** The spliced "Second … Second" numbering is gone; §2.1 is now a plain
  method/result/limits structure with no ordinals.
- **M8.** [[FUNC-97C95BA5572D-0042DB10]]'s Inferred section no longer says four
  functions receive the strings. The same error survives elsewhere (D2).
- **M10.** §1.1's preamble now reads "the only place that reaches the **table**
  record's name", restoring the qualifier the round-4 audit had used. Verified:
  `lea eax,[esi-0x24]` at `0x0042DA9C` and `lea ecx,[esi-0x24]` at `0x0042DABD`
  are the only two reads of a table record's `+0x10`.
- **M11.** [[Subsystem Coverage Map]] row 60 now says "after five James
  rejections". [[Current State]] line 3536 now says "**Five** fresh James audits
  … 12, then 10, then 16, then 12, then 15 defects". The enumeration beneath it
  was not extended (D10).
- **M14.** §2's third push is now presented with its guard, and `0x004E9170` and
  `0x008620AC` both appear in §6.
- **M15.** `KU-071` now reads "Narrowed by the third- and fifth-round audits".

Landed but wrong or incomplete: **M3** (D1, D9), **M4** (D3), **M9** (D6),
**M12** (D13), **M13** (D5).

### Part B — the numbered defects

**D1 (substantive) — "`0x004B13E0` is a three-instruction wrapper" is false, in
the sentence written to fix M3, and the file §0 spends a page crediting shows
it.** Export §2 line 257:

> `0x004B13E0` is a three-instruction wrapper whose body is `call DWORD PTR
> ds:0x864670` at `0x004B13E5`

Disassembled:

```text
4b13e0: 8b 44 24 04       mov  eax,DWORD PTR [esp+0x4]
4b13e4: 50                push eax
4b13e5: ff 15 70 46 86 00 call DWORD PTR ds:0x864670   ; DeleteFileA
4b13eb: 85 c0             test eax,eax
4b13ed: 75 08             jne  0x4b13f7
4b13ef: ff 15 dc 45 86 00 call DWORD PTR ds:0x8645dc   ; GetLastError
4b13f5: eb 02             jmp  0x4b13f9
4b13f7: 33 c0             xor  eax,eax
4b13f9: 85 c0             test eax,eax
4b13fb: 74 0d             je   0x4b140a
4b13fd: 50                push eax
4b13fe: e8 4d 37 00 00    call 0x4b4b50
4b1403: 83 c4 04          add  esp,0x4
4b1406: 83 c8 ff          or   eax,0xffffffff
4b1409: c3                ret
4b140a: 33 c0             xor  eax,eax
4b140c: c3                ret
```

Seventeen instructions, extent `0x004B13E0`-`0x004B140C`, **two** `ret`s, an
error path that calls `GetLastError` and `0x004B4B50` and returns `-1`. Its
"body" is not one call. `ghidra-evidence.json`'s `FUN_004b13e0` renders exactly
this shape — `BVar1 = DeleteFileA(param_1); if (BVar1 == 0) { DVar2 =
GetLastError(); } … if (DVar2 != 0) { FUN_004b4b50(DVar2); return 0xffffffff; }`
— so the packet had the correct shape in hand while writing the wrong one. This
is the **sixth** consecutive round with a false statement about a fact in that
file, and the **third** consecutive round in which the false statement sits
inside the fix for the previous round's defect. It repeats in
[[2026-08-17 1130 - Claude - PC event subsystem census]] line 242 and in the
commit message.

The identification itself is right and I confirmed it twice, independently of
the JSON: `0x004B13E5` is `ff 15 70 46 86 00`, and walking the import directory
at `0x00864000` resolves IAT slot `0x00864670` to `KERNEL32.dll!DeleteFileA`
(`rabin2 -i` agrees; `0x008645DC` is `GetLastError`).

**D2 (substantive) — the census session note still files the `0x004ADEA0`
reading as an open hypothesis, and re-types the M8 error, in a paragraph this
commit rewrapped.** [[2026-08-17 1130 - Claude - PC event subsystem census]]
"## New hypotheses":

> Two: the 32-byte width of the name at `+0x10` … and the reading of
> `0x004ADEA0` as writing a log file — its filename and mode string are decoded
> bytes, but **the four functions it hands them to are unanalysed**, and its
> body is gated on `0x008620AC`.

Three things are wrong. Every other carrier now says the reading is Confirmed.
**Two** functions receive the strings — `0x004B13E0` and `0x004B0730`; the other
two receive the returned handle — which is the L4/M8 distinction the export §0
and the dossier were both corrected to state. And one of the receivers is not
unanalysed: it is `DeleteFileA`. The same file's new "### Fifth round" section,
150 lines below, says the opposite in bold. This is M4's exact finding — one
file, both sides of the boundary — reproduced in the commit that fixed M4, in a
carrier the **round-4** audit had already named by section. The commit's reflow
touched these exact lines without reading them.

**D3 (substantive) — `EXP-185`'s Confirmed set still headlines the claim §2.1
was renamed to withdraw.** Line 188, in the **Confirmed** list:

> - **The table is referenced only from these seven functions.** … The
>   fifth-round audit then withdrew the claim that a window sweep closes the
>   indexed-base gap: it does not, so this is a strong negative on the absolute
>   addressing form only, **not a proof of isolation**.

The bolded lead asserts isolation; the last clause of the same bullet denies it.
The export deliberately retitled §2.1 from that exact sentence to "Absolute
references to the table", explaining "A narrower claim than the section heading
of earlier drafts suggested, stated plainly because three successive drafts
over-reached here". The retitling did not reach the experiment note, so the
over-reaching form now survives only where it is labelled **Confirmed**.

**D4 (substantive) — the withdrawn closure claim is still on the handoff
surface, in three carriers, credited to this census.**
[[Subsystem Coverage Map]] row 60, [[Subsystems MOC]] line 88 and
[[Current State]] line 3531 all
list, among what is new here, "a relocation-exhaustive **closure result**".
[[Current State]] line 3562 additionally calls §2.1 "the packet's strongest
closure result" and states no limit on it at all. The export now says "this is a
**strong negative on one addressing form**, not a proof of isolation" and "that
claim is withdrawn". Two further problems in the same phrase: the export's own
§2.1 provenance line attributes the 47/all-inside result to the **second-round
audit** and the range correction to the third, and the export's own "what is new
here" list in §0 does not contain the relocation result at all — so three
carriers credit the census with a result its own export declines to claim, under
a name its own export retracted.

**D5 (substantive) — §1.1's `+0x10` access list is still incomplete after the
M13 fix, and still reads as exhaustive.** The row:

> never by absolute address — **only** from a record pointer: `lea` at
> `0x0042DA9C` and `0x0042DABD` … and from the caller's record by `lea
> edx,[ebx+0x10]` (`0x0042DB71`), `add ebx,0x10` (`0x0042DC31`) and `add
> esi,0x10` (`0x0042DD01`)

Five producers, in a row that says in its next sentence that the name is passed
at **all 8** log calls. The three missing ones are `lea eax,[ebx+0x10]` at
`0x0042DB4D` (feeding the log at `0x0042DB56`), `lea eax,[ebx+0x10]` at
`0x0042DC10` (feeding `0x0042DC19`), and `lea eax,[esi+0x10]` at `0x0042DCD7`
(feeding `0x0042DCE5`). The last is an addressing form — an `esi`-based `lea` on
the caller's record — that appears nowhere in the list. M13 was raised on
precisely "an incomplete `+0x10` access list"; the fix added two of the five
missing entries.

**D6 (moderate) — M9 landed in one of the three places the fifth round named.**
§1.1's `+0x08` row is correctly rewritten ("called at `0x0042D9A5` by the
dispatch pass `0x0042D980`, and tail-jumped at `0x0042D9E6` by the run-one
function `0x0042D9D0` — two different functions"). But:

- §4.1 still says the census adds "`+0x08` from the dispatch pass" — the exact
  phrase the fifth round quoted. `+0x08` is reached from two functions, and the
  parallel clause in the same sentence says "`+0x0C` at the destroy site**s**".
- §1.1's `0x005982AC` paragraph still says both stores sit "three instructions
  before the `+0x08` callback is **called**". The count is right at both sites —
  I checked — but the second site's transfer is `ff e0 jmp eax` at `0x0042D9E6`,
  not a call. The fifth round named this sentence too.

**D7 (moderate) — the M6 scope fix contradicts §2.1 and §6.** Scope section:
"The lowest such address this document cites **as a subsystem address** is
`0x00598290`." §2.1: "§6 records it as outside this subsystem." §6:
"`0x00598290`, which is written and read outside this subsystem and **is not
part of the table**." The qualifier added to make the scope sentence exclude the
two window bounds classifies as a subsystem address the one address the document
twice insists is not one. Same signature as M1, M10 and L6: a fix whose new
wording is contradicted by the material it introduces.

**D8 (moderate) — the promotion's own predicate is one step stronger than the
evidence, and §2 says so in the next sentence.** §2:

> So **`0x004ADEA0` writes a log file** is Confirmed, on a named import plus two
> decoded strings … `0x004B0730`, `0x004B13A0` and `0x004B04E0` remain undecoded
> here; their fopen/fprintf/fclose shape is the part that stays inference

What `DeleteFileA` confirms is that the function **deletes** a file named
`bugs.log`, once, guarded by `0x004E9170` (which I verified holds `1` at file
`0x0E7D70`), immediately before pushing `bugs.log` and `at` into `0x004B0730`.
It does not confirm that anything is written: the writing would be done by
`0x004B13A0`, whose role the same paragraph, §6, `EXP-185`'s Inferred set and
the dossier all record as unestablished. The defensible Confirmed statement is
"`0x004ADEA0` deletes `bugs.log` through a named Win32 import and then passes
`bugs.log`, the mode string `at` and a formatted text buffer to three undecoded
functions"; "writes a log file" remains an inference, now a very strong one. The
direction of the reversal is right — round 4's demotion did drop the strongest
available evidence — but the packet has again landed one predicate past its
evidence, on the axis that produced L8, the round-4 demotion, and M3.

**D9 (moderate) — "undecoded" left unqualified in three carriers after the M3
fix qualified it in one.** §2 now says the three remaining callees "remain
undecoded **here**". §6 says "the three **undecoded** functions `0x004ADEA0`
calls after `DeleteFileA`"; `EXP-185`'s Inferred set says "`0x004B0730`,
`0x004B13A0` and `0x004B04E0`, which are undecoded";
[[FUNC-97C95BA5572D-0042DB10]] says "are undecoded". I read all three bodies out
of `ghidra-evidence.json`: `FUN_004b0730` (112 chars, a tail call to
`FUN_004b0700(param_1,param_2,0x40)`), `FUN_004b13a0` (251 chars) and
`FUN_004b04e0` (674 chars) are fully decompiled. M3's complaint was exactly that
"has been decoded" is false for these functions; the fix reached one sentence.

**D10 (moderate) — [[Current State]]'s per-round enumeration still stops at
Round 3.** The sentence above it now correctly says five rejections with five
counts (M11 fixed), but the bulleted list beneath gives Rounds 1-3 only, and the
paragraph that follows still reads "recorded because it **recurred three
times**". Rounds 4 and 5 — including the `DeleteFileA` finding, the demotion,
the re-promotion and the §2.1 withdrawal — appear in no bullet on the handoff
surface. An aggregate count now stands where the enumeration used to match it.

### Smaller, also wrong

- **D11.** Dangling forward reference. The census session note's "## Recommended
  next action" reads "Sixth-round audit by a fresh James — **with the caveat
  recorded below**." No caveat follows; the next and final section is "## Git
  commit if applicable — One intentional commit; tree clean." The previous
  version of the line had no such clause.
- **D12.** §2's "the only outbound branch target from any of them is
  `0x00401CF8`" and [[FUNC-97C95BA5572D-0042DB10]]'s "the only outbound target
  is `0x00401CF8`" both drop the qualifier L11 added to `KU-071`, while
  `0x0042DB10` makes two indirect outbound calls (`call [ecx*4+0x5982bc]` at
  `0x0042DB67`, `call [ecx*4+0x5982b4]` at `0x0042DC2A`). Each sentence is
  preceded by "every **direct** branch … was enumerated", so the scope is
  recoverable — but it is the wording L11 was raised against, unfixed in two
  carriers.
- **D13.** New wrap damage at this round's own edit sites, in the round that
  fixed M12. `KU-071` line 1868 is **125** characters where its neighbours are
  74-80 — the M2/M3 sentence was spliced in without wrapping. Export line 41 is
  **99** characters, made so by this commit's own reflow of that paragraph
  (it was inside the wrap before). [[Subsystems MOC]] line 85 is **91**
  characters, added by this commit. Frontmatter and wikilinks are clean — see
  Tests run — so the M12 repair itself held; the damage is new.
- **D14.** `EXP-185` says `ghidra-evidence.json` "carries this function and all
  **four** of its callees". `0x004ADEA0` has five callees: `0x004B0150`,
  `0x004B13E0`, `0x004B0730`, `0x004B13A0` and `0x004B04E0`. "Four" is a subset
  defined only in the export's §2 and never in the experiment note.

### Part C — the two changed claims, re-derived from scratch

**§2.1.** Everything below is mine, decoded from the file with a Python PE
parser, not read from the packet:

- `e_lfanew 0x80`, image base `0x00400000`, six sections. `.reloc` raw pointer
  `0x000EF000`, `SizeOfRawData 0x11800`, `VirtualSize 0x11668`; the BASERELOC
  data directory gives `0x0000D7F8`, the block walk consumes exactly `0xD7F8`,
  and the remaining `0x4008` bytes are all zero.
- **208** blocks, **26,713** type-3 (`HIGHLOW`), **99** type-0, no other types.
- Dereferencing every type-3 site: **47** values in `[0x005982A0, 0x005986F0)`,
  site range `0x0042D959`-`0x0042DD42`, histogram `AC`×2, `B0`×1, `B2`×3,
  `B4`×5, `B8`×4, `BC`×7, `E0`×3, `E2`×3, `E4`×6, `E8`×3, `0x00598668`×1,
  `0x00598670`×9.
- **"All 47 lie inside the seven function extents" holds exactly.** I tested
  each site against the seven extents individually, not against the enclosing
  span: zero outside. This is the stronger of the two forms and the export now
  states it; `EXP-185` still states the weaker `0x0042D950`-`0x0042DD94` form,
  which is also true.
- Independent whole-file 4-byte little-endian scan at every byte offset:
  **47** hits, identical set. Widening the low bound to `0x00598290`: **52**,
  the extra five at `0x00405C0D`, `0x00405C83`, `0x0043DF67`, `0x0043DFB1`,
  `0x004AE8F9` — matching the five sites §2.1 lists, with the read/write split
  as given.
- Image-wide: **6,473** distinct relocated values, **4,673** below
  `0x005982A0`, **1,788** at or above `0x005986F0`, **12** inside. Every number
  in the restated §2.1 is exact.
- The scoping is honest and does not swing to under-claiming. Two additions I
  checked that the section does not need but that support it: the nearest
  distinct relocated value above the range is `0x005987D0` (`0xE0` above),
  referenced only at `0x0042F4AC`/`0x0042F4D7`; the nearest below is
  `0x00598290`, whose five sites carry no index register.

**The `DeleteFileA` treatment.** The mechanism is exactly as described and I
re-derived all of it. `0x004ADEA0`-`0x004ADEAF` is `mov eax,ds:0x8620ac` /
`sub esp,0x400` / `test eax,eax` / `push esi` / `push edi` / `je 0x4adf2a`, and
`0x004ADF2A` pops and returns, so the whole body is gated. `mov ecx,0x100` +
`rep stos` on `[esp+0x8]` over `0x004ADEB1`-`0x004ADEC0`; `call 0x4b0150` at
`0x004ADED3`. The guarded block at `0x004ADEDB`-`0x004ADEF8` is byte-accurate as
quoted — I compared all five instructions byte for byte. `0x004E9170` holds
`01 00` at file `0x0E7D70`; file `0x0E7E60` is `61 74 00` = `"at"` and
`0x0E7E64` is `62 75 67 73 2e 6c 6f 67 00` = `"bugs.log"`. IAT slot
`0x00864670` is `KERNEL32.dll!DeleteFileA` by my own import-directory walk and
by `rabin2 -i`. The Confirmed/Inferred split is stated consistently in the
export, `EXP-185`, both dossiers, [[Current State]], the coverage row,
[[Subsystems MOC]] and `KU-071` — and inconsistently in the census session note
(D2), with the predicate itself over-reaching (D8) and the wrapper
mis-described (D1).

### Part D — what six rounds had not checked

Everything in this part is new work; none of it produced a defect, and all of it
strengthens the packet.

- **§3's exclusivity claim holds exactly.** Whole-file little-endian scans for
  all five string addresses return `0x004D823C`→1 site (`0x0042DACB`),
  `0x004D8264`→3 (`0x0042DAA0`, `0x0042DB51`, `0x0042DCE0`), `0x004D82A4`→1
  (`0x0042DC35`), `0x004D82CC`→1 (`0x0042DC14`), `0x004D830C`→2 (`0x0042DB78`,
  `0x0042DD08`) — the §3 table exactly, and nothing else in the image. All five
  strings and their file offsets `0x0D6E3C`/`0x0D6E64`/`0x0D6EA4`/`0x0D6ECC`/
  `0x0D6F0C` decode as printed, including the `\n` versus `\n\n` distinction
  between `0x004D823C` and `0x004D830C`.
- **Both decoded records are byte-exact.** `0x004D81A8` (file `0x0D6DA8`):
  `02 00 | 00 00 | 91 1a 40 00 | a5 1a 40 00 | da 17 40 00 | "WINDOWS\0"`, all
  zero from `+0x18`. `0x004D81E8` (file `0x0D6DE8`): `03 00 | 00 00 |
  04 1b 40 00 | d1 11 40 00 | 99 12 40 00 | "DIRECTX\0"`, likewise. All six
  thunks resolve as claimed: `0x00401A91`→`0x004AE580`, `0x00401AA5`→
  `0x004AE780`, `0x004017DA`→`0x004AE810`, `0x00401B04`→`0x0042BA60`,
  `0x004011D1`→`0x0042BB30`, `0x00401299`→`0x0042BB50`.
- **§4's quoted disassembly is byte-accurate**, all nine lines at
  `0x0043DAEB`-`0x0043DB10`, as is §1's `0x0042DBBE`-`0x0042DBD5` block and §2's
  `0x004ADEDB` block. The `cmp`/`jne` at `0x0043DAFD`-`0x0043DB04` does skip
  only `call 0x401c30` (→`0x004A7600`), leaving both registrations unconditional
  within the function.
- **§1.2's bounds reasoning is sound.** All three reads are `movsx` of a signed
  word; the first access after scaling is `[eax+0x5982e4]` at all three; no
  `cmp` of any kind appears between read and first access; the two iterating
  passes carry their own `0x10` counters. The intervening-instruction gloss is
  right at all three sites, including that `0x0042DCA8`'s scaling is contiguous.
- **The dead-caller finding is stronger than claimed.** Beyond the eight scans
  the export ran, I indexed every `e8`/`e9` rel32 in `.text` and additionally
  swept every `eb`/`70`-`7f` rel8 and every `0f 8x` rel32 for targets in
  `{0x0040169F, 0x0040179E, 0x00401217, 0x00401140}` and the four functions:
  zero hits by any form. The thunk table is solid `jmp rel32`, so no
  fall-through reaches them either.
- **The extent and branch enumeration is right for all seven.** Each has exactly
  one `ret` at the stated address followed by `nop`/`int3` padding; walking each
  range instruction by instruction, the only outbound direct transfers are the
  eight `call 0x401cf8` at `0x0042DAA5`, `0x0042DAD3`, `0x0042DB56`,
  `0x0042DBB6`, `0x0042DC19`, `0x0042DC3A`, `0x0042DCE5` and `0x0042DD46`.
  `0x0042DD90` is a bare `ret` after `int3` padding, as stated.
- **§5's disjointness construction holds in both directions**, and its
  comparison table cross-checks against the creature census: `0x0059B628 +
  64 × 0x84 = 0x0059D728`; the 40 variable-length programs at
  `[0x004C7D00, 0x004C83F0)` and the pointer table at `0x004C83F0` match
  `SUBSYS-creature-actor-static-census.md` §6 and `EXP-20260816-172`; the
  26-entry table at `0x0041E848` and `+0x70`/`+0x60` match §5.2 and §4 of that
  export. `0x0041DC60` occurs zero times as a little-endian dword anywhere in
  the image.
- **§0's prior-art accounting is accurate throughout.** Six relevant entries;
  the three `thunk_FUN_` `callers` lists are exactly as tabulated and cover 7 of
  the 9 reachers; the `FUN_` lists are empty; `FUN_0042db10`'s body renders base,
  stride, the 15-dword copy, two of three callback slots as calls (with
  `&DAT_005982b8` a zero-store there and a call in `thunk_FUN_0042d980`), the
  flag as `(&DAT_005982e4)[*param_1 * 0xf] = 1`, the name as `param_1 + 8`, the
  buffer and its `0x20`-iteration zeroing, the seven field clears, and four of
  the five format strings with `0x004D823C` only in `FUN_0042da70`;
  `thunk_FUN_0042d980` renders `_DAT_005982ac = puVar1 + -2` and the `0x10`
  bound; `thunk_FUN_004adea0`'s `callers` list holds six of the eight log sites,
  missing exactly `0x0042DCE5` and `0x0042DD46`; and there is **no** entry for
  `0x0042D950`, `0x0042D9D0`, `0x0042DA00`, `0x0042DCA0` or any of their four
  thunks. Both prior-art quotations — the audio export's "a record of a count
  and three code pointers" and `EXP-20260816-159`'s "a count of 3 followed by
  thunk pointers…" — are verbatim.
- **The novelty negative reproduces.** I checked out `4e0157f^` into a scratch
  worktree and grepped `Vault/` and the markdown exports for all fifteen
  addresses: zero hits for every one.
- **`Bounded` is the right status.** The map defines it as "Real PC evidence at
  a documented boundary, with major parts open", which is what this packet has:
  no runtime, six unnamed callbacks, an unanalysed registration caller.

## Contradictions discovered

Five, all internal to the packet and all live in the committed tree:

1. Export §2's "three-instruction wrapper" against `ghidra-evidence.json`'s own
   `FUN_004b13e0` body and against the binary — D1.
2. The census session note's "New hypotheses" against every other carrier and
   against its own "### Fifth round" section — D2.
3. `EXP-185`'s Confirmed headline "The table is referenced only from these seven
   functions" against the same bullet's "not a proof of isolation" — D3.
4. The export's "not a proof of isolation" against three carriers' "closure
   result" — D4.
5. The scope section's "`0x00598290` … as a subsystem address" against §2.1 and
   §6 — D7.

And one boundary problem rather than a contradiction: §2 declares "writes a log
file" Confirmed while declaring the calls that would write it inference — D8.

## Tests run

`make vault-lint` **523 notes, 0 errors, 0 warnings**; `make audit-tracked`
**0 violations** — both run by me, output read; the commit's hygiene figures are
accurate. I additionally validated the YAML frontmatter of all 523 notes with a
parser (0 failures, so the M12 frontmatter restoration held) and swept every
markdown file under `Vault/` and `static/exports/` for split or unbalanced
wikilinks: two hits, both in [[Decision Log]] (`Runtime Tooling#Live validation
results` and `Runtime Tooling#The ntsync blocker for rr`), both pre-existing and
untouched by this packet. `Subsystems MOC` carries no split link. I did not
re-run `make test`; the packet changed no code.

Binary work, all mine, on `work/copies/BUGS_PC-full-disc/bugs.exe` re-hashed to
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`:
`sha256sum`; `objdump -h`; `rabin2 -i`; `objdump -d -M intel` over
`0x0042D940`-`0x0042DDA0`, `0x004ADE90`-`0x004ADF40`, `0x004B13E0`-`0x004B1440`,
`0x0043DAE0`-`0x0043DB20`, `0x00412180`-`0x004121B8`, `0x004AE855`-`0x004AE875`
and all fifteen cited thunks; a Python PE parser reading the section table and
all sixteen data directories; a full base-relocation decode (208 blocks, 26,713
type-3, 99 type-0) with every site dereferenced, value histograms for the
narrow, widened and `[0x00597000, 0x0059A000)` ranges, an image-wide
distinct-value census, and a per-extent membership test for all 47 sites;
whole-file 4-byte little-endian scans over the entire table range and for
`0x005982AC`, `0x005982B0`, `0x005982B4`, `0x005982C0`, `0x00598290`,
`0x00598670`, all five string addresses, all eight dead thunk/function addresses
and both disjointness address sets; an `e8`/`e9` branch-target index over the
whole `.text` plus rel8 and `0f 8x` sweeps for the dead thunks; an
instruction-by-instruction outbound-branch walk of all seven extents; byte
decoding of both `.data` records, all five `EVENT` strings, `0x004E9170`,
`0x004E9260` and `0x004E9264`; a walk of the import directory at `0x00864000`
resolving IAT slots `0x00864670` and `0x008645DC`; and `ghidra-evidence.json`
parsed as JSON with all six event entries, both `004adea0` entries and all five
`0x004Bxxxx` callee bodies read in full. Plus the novelty negative re-run
against a `4e0157f^` worktree.

## Unresolved questions

`KU-071`; the six callback targets; whether any event is registered outside the
two static sites; whether a computed reference — a register-held pointer, or any
of the 6,461 relocated values outside the range plus an index — reaches these
seven functions; what `0x008620AC` gates and what sets `0x004E9170`; the true
extent of the buffer at `0x00598670`; the meaning of `+0x02`, `+0x30`, `+0x32`,
`+0x38`, `0x0059F7F0`, and of a `0x005982AC` nothing reads.

**Not verifiable from artifacts:** that the prior-art greps happened before
analysis; that no `originals/` path, game asset, PS1 source, process or debugger
was touched; and that `make test` ran at 686 passed in 17.95s.

## Recommended next action

Fix D1 first — it is a one-sentence factual error about the binary at an address
the packet cites, and it repeats in two carriers plus the commit message. Say
what the function is: a `DeleteFileA` wrapper at `0x004B13E0`-`0x004B140C` with
a `GetLastError` failure path returning `-1`.

Then D2 and D3, which are the same defect M4 named, now in two different files;
then D4, which is M2 stopping at the export; then D8, which is the predicate
itself. D5-D7 and D9-D14 after that.

Three process notes, all earned by this round:

- **The failure is now structural, not clerical.** Ten carriers each paraphrase
  the same findings in their own words, so every correction is ten rewrites and
  each rewrite is a fresh chance to be wrong. Five rounds of sweeps — defect
  phrase, corrected phrase, presence, per-claim — have each caught the previous
  round's mode and missed the next. Make the export the single normative
  statement and have the other nine carriers **quote** it rather than restate
  it; a quotation cannot drift and a stale quotation is greppable.
- **A withdrawn claim needs the same sweep as a corrected one.** D3 and D4 are
  both retractions that reached the export and stopped. The presence sweep tests
  for what should be there; nothing tests for what should now be gone.
- **Check the new sentence against the artifact, not against the audit.** D1 is
  the third consecutive instance: the fixer had `FUN_004b13e0`'s body open, and
  wrote a description of the function that the body contradicts.

On convergence: the *model* has converged and did so by round 1 — six
independent re-derivations, no defect has ever touched geometry, layout,
extents, records or disjointness, and this round found none either. The
*document* is not converging: defect counts run 12, 10, 16, 12, 15, 14, and the
residue is concentrating on two axes (`0x004ADEA0`/`ghidra-evidence.json`, and
cross-carrier propagation) that have now failed in six and five consecutive
rounds respectively. Another round of the same process will produce another
round of the same defects. The finding is sound and worth keeping; the way it is
being written down is what needs changing.

## Git commit if applicable

None by the auditor. Nothing in the packet was modified.
