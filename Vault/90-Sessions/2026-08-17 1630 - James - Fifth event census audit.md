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

# Fifth event census audit

## Agent

James, fresh context, fifth audit of the event packet. No knowledge of the four
earlier rounds beyond the artifacts committed at `b69cbb2`. Every prior
auditor's finding — including the four acceptances of the underlying model —
was treated as a claim to re-test against the binary, not as settled.

## Goal

Judge `b69cbb2`, which claims to fix the twelve defects a fourth-round James
audit raised against `2c8c6aa`. Three questions: did each of L1-L12 land in
**every** carrier and is each correct; are the two claims this round rewrote —
§2.1's relocation argument with its new second limit, and the demotion of
`0x004ADEA0` back to Inferred with a gate recorded — actually right; and what
have all five rounds missed. The model was re-derived from the binary rather
than inherited.

## Files inspected

`CLAUDE.md`; [[START HERE]]; [[Agent Operating Manual]];
`static/exports/BIN-97c95ba5572dce63/SUBSYS-event-static-census.md`;
[[EXP-20260817-185 - PC event subsystem static census]];
[[FUNC-97C95BA5572D-0042DB10]]; [[FUNC-97C95BA5572D-0042D980]];
[[2026-08-17 1130 - Claude - PC event subsystem census]]; the four prior audits
[[2026-08-17 1230 - James - Event census audit]],
[[2026-08-17 1330 - James - Second event census audit]],
[[2026-08-17 1430 - James - Third event census audit]] and
[[2026-08-17 1530 - James - Fourth event census audit]]; the full `b69cbb2` diff
including [[Current State]], [[Subsystem Coverage Map]], [[Subsystems MOC]],
[[Functions MOC]], `KU-071` in [[Known Unknowns]] and [[Session Index]]; the
tree `4e0157f^` for the novelty negative; the prior art the packet cites —
`SUBSYS-audio-static-census.md`, `SUBSYS-creature-actor-static-census.md`; the
generated `static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json`, parsed as
JSON with the relevant bodies read in full; and
`work/copies/BUGS_PC-full-disc/bugs.exe`, re-hashed to
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.

## Experiments inspected

`EXP-20260817-185` (the packet), `EXP-20260816-159` (the `0x004D81E8` prior art)
and `EXP-20260816-172` via the creature export.

## Changes made

None. This note only. No packet artifact was touched and nothing was committed.

## Conclusions

**REJECT.** Five severe defects, six moderate, four smaller.

The model is right, and I re-derived all of it independently from the binary:
table geometry, the record layout in both addressing forms, all seven extents
and their single `ret`s, the eight thunk edges, the nine reachers, both decoded
records, the five strings and their exclusivity, the disjointness result, §2.1's
47/52/26,713 figures by two methods, and the `157` figure this round adds. Five
auditors have now re-derived the model and it has held every time.

The failures are again in the writing, and two of them are substantive.

First, §2.1's **new** closing sentence is false against the binary and
contradicts the same section's own result three paragraphs above; and the sweep
offered as closure does not close the hole it names.

Second, §2's **new** sentence "none of `0x004B0730`, `0x004B13A0`, `0x004B04E0`
or `0x004B13E0` is an import or has been decoded" is false in both halves for
`0x004B13E0`. `ghidra-evidence.json` decodes it as `DeleteFileA(param_1)`, and
the binary's own import directory confirms it: `0x004B13E5`'s
`call DWORD PTR ds:0x864670` is `KERNEL32.dll!DeleteFileA`. This is the fifth
consecutive round in which a statement about `ghidra-evidence.json` is wrong,
and the third in which the error sits in the sentence written to fix the
previous one — only this time the packet *under*-claims, and in doing so drops
the single strongest piece of evidence available for the reading it demotes.

And the round-4 lesson did not take. L1's fix left the contradiction standing in
the file the audit named, L12's fix never reached [[Current State]], and the
rejection count in two carriers is now one short of reality.

### Part A — the twelve fixes, re-verified

Correct and complete:

- **L2.** Export §3 and [[FUNC-97C95BA5572D-0042DB10]] now cite `0x0042DB71`.
  Verified: `42db6e 0f bf 03 movsx eax,WORD PTR [ebx]`, `42db71 8d 53 10
  lea edx,[ebx+0x10]`. The added gloss naming `0x0042DB6E` as the `movsx` is
  right.
- **L3.** §1.2 now reads "at `0x0042DB18` two `push`es intervene
  (`0x0042DB1B`, `0x0042DB1C`) and at `0x0042DA00` an `xor` does
  (`0x0042DA05`)", with the parenthetical placing `0x0042DB16`'s `xor ebp,ebp`
  before the read. All four addresses verified; `0x0042DB1B` is `push esi`,
  `0x0042DB1C` `push edi`, `0x0042DA05` `xor ecx,ecx`. The substantive claim —
  no `cmp` between the read and the first access at any of the three — I
  re-verified.
- **L4** (export only). §0 now says the string goes to `FUN_004b13e0` and
  `FUN_004b0730` and the returned handle to `FUN_004b13a0` and `FUN_004b04e0`.
  That matches the JSON body exactly. It is repeated wrongly in the dossier
  (M8).
- **L9.** [[Current State]] now reads "Round 3 also corrected and hardened the
  packet's strongest closure result, which the round-2 audit had found." I
  checked both source notes: the 1330 audit reports the 47/all-inside whole-file
  result; the 1430 audit supplies the 26,713-relocation method and catches the
  52/47 range mixing. The attribution is right.
- **L11.** `KU-071` now reads "the subsystem's only outbound **direct** call —
  the six callback calls are indirect". Verified: `call eax` (`0x0042D9A5`),
  `jmp eax` (`0x0042D9E6`), `call [esi-0x28]` (`0x0042DAAD`),
  `call [ecx*4+0x5982bc]` (`0x0042DB67`, `0x0042DCF6`) and
  `call [ecx*4+0x5982b4]` (`0x0042DC2A`) — six, one of which is a tail `jmp`
  counted as a call.

Landed but wrong or incomplete: **L1** (M4), **L5** (M7, M12), **L6** (M10),
**L7** (M1, M2, M6), **L8** (M3, M8, M14), **L10** (M11), **L12** (M5).

L10's coverage-row sweep did land the `0x004ADEA0` reading and the relocation
result, but left the row's rejection count stale (M11).

### Part B — the numbered defects

**M1 (severe) — §2.1's new gap claim is false as written and contradicts the
section's own 47 result.** The sentence: "across `[0x00597000, 0x0059A000)`
there are 157 distinct relocated values, and **none lies between `0x00598290`
and `0x005987D0`**."

157 is right; I decoded the directory myself (208 blocks, 26,713 type-3, 99
type-0, consuming exactly the `0xD7F8` the BASERELOC data directory gives) and
dereferenced every site. But **twelve** of those 157 lie strictly between
`0x00598290` and `0x005987D0`: `0x005982AC`, `B0`, `B2`, `B4`, `B8`, `BC`,
`E0`, `E2`, `E4`, `E8`, `0x00598668` and `0x00598670`. They are exactly the
twelve values behind the 47 sites §2.1 counts three paragraphs above, so the
section asserts and denies the same fact on one page. The claim the sentence
means — nothing *other than the table's own references* lies in that interval —
is true and is never stated. The commit message repeats the false form verbatim.

**M2 (severe) — the second sweep does not close the hole it is offered to
close, and §2.1 says it does.** The section states the hole correctly: the
enumeration filters on the relocated *value*, so a base relocated outside the
range and indexed into it is invisible. Then: "So no relocated base outside the
range is positioned to index into it. The result stands; the one-line proof did
not, and this is what closes it."

It does not close it, for three reasons I checked against the binary:

1. The sweep covers a `0x3000`-byte window. The image has **6,473** distinct
   relocated values; **4,673** lie below `0x005982A0` and **1,788** at or above
   `0x005986F0`. The window excludes 6,316 of them by fiat, and the nearest
   distinct value below the window floor is `0x00596F40` — `0x1350` away, well
   inside a single `disp32`. x86 `[base + reg]` and `[reg + disp32]` impose no
   distance bound, so window width is not an argument.
2. The stated form is restricted to "`[base + reg]` where `base < 0x005982A0`".
   A base *above* the range reaches into it with a negative index or a negative
   displacement just as easily; `0x005987D0` and the 1,787 higher values are
   never tested for that, and the section's own "the nearest above is
   `0x005987D0`" is offered as if it settled the question.
3. The form actually at risk — a pointer loaded into a register and then
   displaced — carries no relocation *at the point of use* at all. That is
   limit one (the computed form), which no relocation sweep can address.

What the sweep genuinely establishes is narrower and worth keeping: no relocated
base in `[0x00597000, 0x0059A000)` other than the table's own sits within
`0x10` below or `0xE0` above the range, and `0x00598290`'s five sites are all
direct `mov ds:0x598290` with no index register (verified: `0x00405C0C` and
`0x00405C82` read, `0x0043DF65`, `0x0043DFAF` and `0x004AE8F7` write). The
section should say that instead of "this is what closes it".

**M3 (severe) — §2 asserts four functions are undecoded when the packet's own
cited prior-art file decodes all four, and one of them resolves to a Win32
import.** §2: "none of `0x004B0730`, `0x004B13A0`, `0x004B04E0` or
`0x004B13E0` is an import or has been decoded, so their roles are
unestablished."

`ghidra-evidence.json` carries `FUN_004b0730`, `FUN_004b13a0`, `FUN_004b04e0`,
`FUN_004b13e0` and `FUN_004b0150`, each with a full decompiler body. The
`0x004B13E0` body is:

```text
undefined4 FUN_004b13e0(LPCSTR param_1)
{
  BVar1 = DeleteFileA(param_1);
  ...
}
```

I confirmed that independently from the binary, without the JSON: `0x004B13E5`
is `ff 15 70 46 86 00  call DWORD PTR ds:0x864670`, and walking the import
directory at `0x00864000` resolves IAT slot `0x00864670` to
`KERNEL32.dll!DeleteFileA` (and `0x008645DC`, used at `0x004B13EF`, to
`GetLastError`). Two independent evidence forms, which is the standard the
Operating Manual asks for.

Three consequences:

- "has been decoded" is false for all four, in the section whose subject is
  what is and is not established. This is the fifth successive round with a
  wrong statement about `ghidra-evidence.json`, and §0 already carries the
  sentence "Three successive drafts of this section under-credited this file in
  three different ways."
- "is an import" is false in substance for `0x004B13E0`: it is a two-instruction
  wrapper over one.
- The packet drops a real finding. The third `0x004E9264` push at `0x004ADEE5`
  — which this round added to §2 — is guarded by `cmp WORD PTR ds:0x4e9170,0x0`
  at `0x004ADEDB` and clears `0x004E9170` at `0x004ADEEA`, i.e. it fires once.
  What it calls deletes the file named `"bugs.log"`. A one-shot delete followed
  by an `"at"`-mode open of the same name is direct evidence for the log
  reading the packet demotes to inference, and it is nowhere in any carrier.

**M4 (severe) — L1's fix left the contradiction standing inside the file the
round-4 audit named.** [[EXP-20260817-185 - PC event subsystem static census]]
line 159, in the **Confirmed** set:

> the only outbound target from any of them is `0x00401CF8` (→ `0x004ADEA0`),
> **which writes `"bugs.log"`**: that filename and the mode string `"at"` are
> pushed at `0x004ADEFB`-`0x004ADF05`...

Line 206, in the **Inferred** set of the same note: "the reading of
`0x004ADEA0` as writing a **log file** ... the conclusion drawn from them is
inference."

The fourth-round audit stated this precisely — "The same note's own Confirmed
set, twenty lines above, says `0x004ADEA0` 'writes "bugs.log"'. One file, two
positions." The commit fixed the Inferred half and left the Confirmed half. The
presence sweep the commit message describes — "for every carrier mentioning
`0x004ADEA0`, assert the inference flag, the `"bugs.log"` anchor and the
`0x008620AC` gate are all present" — cannot catch this, because it tests for
presence of the correction, not absence of the contrary claim. A per-file
presence test passes on a file that says both things.

**M5 (severe) — L12 did not reach [[Current State]], the carrier the round-4
audit named by line number.** Line 3470 still reads:

> `create` and `destroy` are the binary's own words, taken from the log strings
> that **immediately** precede those calls

Four instructions separate `0x0042DB56` from `0x0042DB67`, four separate
`0x0042DCE5` from `0x0042DCF6`, four separate `0x0042DC19` from `0x0042DC2A`,
and one separates `0x0042DAA5` from `0x0042DAAD`. The export §1.1 and
`EXP-185` were both corrected; the handoff surface was not. A whole-repository
grep for `immediately` finds exactly one remaining event-packet occurrence
outside the corrected gloss, and it is this one. Fifth consecutive round of "a
fix applied at the first occurrence is not a fix applied".

**M6 (moderate) — the scope section's ".bss-class" statement is now false, made
so by this round's own L7 fix.** The scope section: "the lowest such address
this document cites is `0x00598290`". §2.1's new paragraph cites
`0x00597000` (and `0x0059A000`). I extracted every hex literal in the document:
above `.data`'s raw end `0x004ED400` the lowest cited is now `0x00597000`. The
sweep-range addresses were added without revisiting the section that bounds
them.

**M7 (moderate) — §2.1 is now numbered "Three limits ... First ... Second ...
Second", with the third limit spliced mid-paragraph.** Lines 310-330: the new
second limit was inserted ahead of the existing one without renumbering, and the
existing one now begins mid-sentence — "The result stands; the one-line proof
did not, and this is what closes it. Second, the range deliberately starts at /
`0x005982A0` and so / **excludes `0x00598290`**". Same substitution-without-
reading signature the fourth round recorded as L5, in the section that round
rewrote.

**M8 (moderate) — the dossier reintroduces the L4 error the export just fixed.**
[[FUNC-97C95BA5572D-0042DB10]] "## Inferred", written this round:

> `"bugs.log"` and `"at"` are decoded bytes, but **the four functions receiving
> them** are unanalysed, so the conclusion is inference.

Two functions receive the strings — `0x004B13E0` and `0x004B0730`. `0x004B13A0`
and `0x004B04E0` receive the returned handle. That is exactly the distinction
L4 was raised about and that §0 was corrected to state. The correction was made
in one carrier and the error re-typed in another, in the same commit.

**M9 (moderate) — §1.1's `+0x08` row attributes an instruction to the wrong
function; missed by all five rounds.** The row: "**called** at `0x0042D9A5` and
tail-jumped at `0x0042D9E6`, **by the dispatch pass**."

`0x0042D9E6` (`ff e0 jmp eax`) is inside `0x0042D9D0`-`0x0042D9E8`, which §2's
own table names "run one record by pointer" — a different function from the
dispatch pass `0x0042D980`-`0x0042D9B3`. §4.1 repeats it: "`+0x08` from the
dispatch pass". [[FUNC-97C95BA5572D-0042D980]] gets it right ("`0x0042D9D0`
performs the same operation for a single record given by pointer, tail-jumping
to `+0x08` at `0x0042D9E6`"), so the packet holds both readings. §1.1's
`0x005982AC` paragraph has the same shape — "at `0x0042D99A` and `0x0042D9DA`,
three instructions before the `+0x08` callback is called" — where the second
site's `+0x08` transfer is a `jmp`, not a `call`. The "three instructions"
count is right at both sites; I checked.

**M10 (moderate) — the L6 fix over-generalises the auditor's own precise
statement, and now contradicts the row in the other direction.** New preamble:
"It is, however, the *only* source for `+0x10`'s access form, since that field
has no `id`-scaled absolute form at all."

The fourth-round audit said "it is the only place in the image that reaches the
**table** record's name" — which is true and which I verified. The fix dropped
"table record". §1.1's own `+0x10` row lists two further access forms —
`[ebx+0x10]` and `[esi+0x10]` on the caller's record — and §3 gives a third,
`add ebx,0x10` / `add esi,0x10`. So the preamble again asserts something the row
it introduces contradicts, which is precisely what L6 was raised about. The
stated reason ("no `id`-scaled absolute form") supports a different claim than
the one made.

**M11 (moderate) — the rejection count is stale in two carriers and
inconsistent with a third.** [[Subsystem Coverage Map]] row 60: "EXP-185,
corrected after **three** James rejections". [[Current State]] line 3536:
"**Three** fresh James audits rejected this packet in succession — 12, then 10,
then 16 defects", followed by a per-round list that stops at Round 3. There have
been four rejections (12, 10, 16, 12) and this commit is the answer to the
fourth; [[2026-08-17 1130 - Claude - PC event subsystem census]] duly gained a
"### Fourth round" section in the same commit. The coverage-map convention
counts rejections elsewhere in the same table — Input "after two rejections",
Enemies "after seven rejections" — and [[Current State]] records the creature
packet's fourth rejection under its own heading. A reader of the handoff surface
is told the packet has survived one fewer audit than it has.

### Smaller, also wrong

- **M12.** New wrap damage at this round's edit sites, in four files, while the
  commit message says "The export is rewrapped". The export's paragraphs were
  *split*, not rewrapped: mid-paragraph short lines now sit at 101, 170, 184,
  231, 233, 237, 325, 359 and 444. The same edit pass left over-long
  mid-paragraph lines in [[Subsystems MOC]] (line 85, 118 chars), `EXP-185`
  (line 191, 91 chars) and the census session note (line 71, 113 chars), and a
  ragged break in [[Current State]] at 3490-3491 and `KU-071` at 1866. L5's
  signature, one round later.
- **M13.** §1.1's `+0x10` row says the name is reached "never by absolute
  address — **only `lea`** from a record pointer ... or from the caller's
  record". Two of the eight name arguments are produced by `add reg,0x10`:
  `0x0042DC31` (`add ebx,0x10`, for the log at `0x0042DC3A`) and `0x0042DD01`
  (`add esi,0x10`, for the log at `0x0042DD46`). §3 states both explicitly.
- **M14.** §2's new "(and `0x004E9264` again at `0x004ADEE5`)" presents that
  push as unconditional. It is guarded by `cmp WORD PTR ds:0x4e9170,0x0` at
  `0x004ADEDB`, and the guarded block clears `0x004E9170` at `0x004ADEEA` — a
  one-shot. Neither `0x004E9170` nor `0x008620AC` appears in §6's list of what
  the census does not establish, although §2 says the gate's value is
  unestablished.
- **M15.** `KU-071` files this round's results under "Narrowed by the
  **third**-round audit": the `0x008620AC` gate, the restoration to inference
  and the "direct" qualifier are all fourth-round results. Same attribution
  axis as L9, in the note L9 was raised against.

### Part C — the two rewritten claims, re-derived from scratch

**§2.1's relocation argument.** Everything below is mine, decoded from the file:

- PE header `e_lfanew 0x80`, image base `0x00400000`, six sections. `.reloc`
  raw pointer `0x000EF000`, `SizeOfRawData 0x11800`, `VirtualSize 0x11668`;
  the BASERELOC data directory gives `0x0000D7F8`, the block walk consumes
  exactly `0xD7F8`, and the remaining `0x4008` bytes of the section are zero.
  The export's "size `0x11800`" describes the section on disk and is harmless.
- **208** blocks, **26,713** type-3 (`HIGHLOW`) entries, **99** type-0 padding
  entries, no other types. Matches the export.
- Dereferencing every type-3 site: **47** values in `[0x005982A0, 0x005986F0)`,
  site range `0x0042D959`-`0x0042DD42`. I checked the stronger form the export
  does not state: every one of the 47 falls inside one of the **seven function
  extents**, not merely inside `0x0042D950`-`0x0042DD94`. Value histogram:
  `AC`x2, `B0`x1, `B2`x3, `B4`x5, `B8`x4, `BC`x7, `E0`x3, `E2`x3, `E4`x6,
  `E8`x3, `0x00598668`x1, `0x00598670`x9.
- Independent whole-file 4-byte little-endian scan at every byte offset: **47**
  hits, identical set. Widening the low bound to `0x00598290`: **52**, the extra
  five at operand offsets `0x00405C0D`, `0x00405C83`, `0x0043DF67`,
  `0x0043DFB1`, `0x004AE8F9`; disassembled, the read/write split §2.1 gives is
  right and none of the five carries an index register.
- The band `[0x00597000, 0x0059A000)`: **1,145** sites, **157** distinct values.
  157 is right. The gap claim is not (M1), and the closure claim does not
  follow (M2). Image-wide there are 6,473 distinct relocated values, 4,673 below
  `0x005982A0` and 1,788 at or above `0x005986F0`.

**The `0x004ADEA0` treatment.** The demotion itself is correct and I would have
asked for it. The gate is right: `0x004ADEA0 a1 ac 20 86 00 mov eax,ds:0x8620ac`
/ `0x004ADEAB test eax,eax` / `0x004ADEAF 74 79 je 0x4adf2a`, and `0x004ADF2A`
is `pop edi / pop esi / add esp,0x400 / ret`, so the whole body is skipped. The
formatting is as described: `sub esp,0x400` at `0x004ADEA5`, `mov ecx,0x100` +
`rep stos` on `[esp+0x8]` over `0x004ADEB1`-`0x004ADEC0`, then
`FUN_004b0150(buf, fmt, va)` at `0x004ADED3`. `0x004ADEFB 68 60 92 4e 00
push 0x4e9260`, `0x004ADF00 68 64 92 4e 00 push 0x4e9264`, `0x004ADF05 call
0x4b0730`; file offsets `0x0E7E60` = `61 74 00` = `"at"` and `0x0E7E64` =
`62 75 67 73 2e 6c 6f 67 00` = `"bugs.log"`. The returned value goes to
`0x004B13A0` with the buffer and then to `0x004B04E0`.

What is over- and under-claimed: the demotion is not applied in `EXP-185`'s
Confirmed set (M4); "has been decoded" is false for all four callees and "is an
import" is false in substance for `0x004B13E0` (M3); the dossier mis-states who
receives the strings (M8); the third push is presented without its guard (M14).

## New hypotheses

One, and it is not mine to promote: `0x004ADEA0`'s guarded first-call path
deletes `"bugs.log"` before the append-mode opens begin — `FUN_004b13e0` is
`DeleteFileA`, confirmed both in `ghidra-evidence.json` and by resolving IAT
slot `0x00864670` in the binary's own import directory, and `0x004E9170` is
cleared inside the guarded block so it fires once per process. If the packet
wants to keep the log reading at Inferred that is defensible, but it must stop
saying the callees are undecoded, and it should record this.

## Contradictions discovered

Five, all internal to the packet and all live in the committed tree:

1. §2.1's "none lies between `0x00598290` and `0x005987D0`" against §2.1's own
   47 values, twelve of which do — M1.
2. `EXP-185`'s Confirmed set ("which writes `"bugs.log"`") against its own
   Inferred set — M4, and the same contradiction the fourth round recorded.
3. §2's "none ... has been decoded" against §0's own account of
   `ghidra-evidence.json`, which decodes all four — M3.
4. §1.1's `+0x08` row and §4.1 ("by the dispatch pass") against
   [[FUNC-97C95BA5572D-0042D980]] and §2's function table — M9.
5. §1.1's preamble ("the *only* source for `+0x10`'s access form") against
   §1.1's `+0x10` row and §3 — M10.

Also inconsistent across carriers rather than internally: the rejection count
(M11) and the "immediately" wording (M5).

## Tests run

`make vault-lint` **522 notes, 0 errors, 0 warnings**; `make audit-tracked`
**0 violations** — both run by me, output read. The commit's hygiene figures are
accurate. I did not re-run `make test`; the packet changed no code.

Binary work, all mine, on `work/copies/BUGS_PC-full-disc/bugs.exe` re-hashed to
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`:
`sha256sum`; `objdump -h`; `rabin2 -I`; `objdump -d -M intel` over
`0x0042D940`-`0x0042DDA0`, `0x004ADE90`-`0x004ADF60`,
`0x0043DAE0`-`0x0043DB20`, all fifteen cited thunks, the four log callees and
the five `0x00598290` sites; a Python PE parser reading the section table and
all sixteen data directories; a full base-relocation decode (208 blocks, 26,713
type-3, 99 type-0) with every site dereferenced and value histograms for the
narrow, widened and `[0x00597000, 0x0059A000)` ranges plus an image-wide
distinct-value census; whole-file 4-byte little-endian scans for the table
range, the widened range, `0x005982AC`, `0x005982B0`, `0x005982C0`, all five
strings, all eight dead thunk/function addresses and all four disjointness
address sets; an `e8`/`e9` branch-target index over the whole `.text`; byte
decoding of both `.data` records and all five `EVENT` strings; a walk of the
import directory at `0x00864000` resolving IAT slots `0x00864670` and
`0x008645DC`; and `ghidra-evidence.json` parsed as JSON with all six event
entries, both `004adea0` entries and the five `0x004Bxxxx` callee bodies read in
full. Plus the novelty negative re-run against a `4e0157f^` worktree: all
fifteen addresses, zero hits across `Vault/` and the markdown exports.

## Unresolved questions

`KU-071`; the six callback targets; whether any event is registered outside the
two static sites; whether a computed reference — a pointer in a register, or any
of the 6,316 relocated bases outside §2.1's window plus an index — reaches these
seven functions, which M2 shows §2.1 does not answer; what `0x008620AC` gates;
the true extent of the buffer at `0x00598670`; the meaning of `+0x02`, `+0x30`,
`+0x32`, `+0x38`, `0x0059F7F0` and of a `0x005982AC` nothing reads. Not
verifiable from artifacts: that the prior-art greps happened before analysis,
that `make test` ran at 686/17.32s, and that no `originals/` path, asset or PS1
source was touched.

## Recommended next action

Fix M3 first — it is the only defect that changes what the packet knows.
`0x004B13E0` is `DeleteFileA`, provable twice; say so, drop "has been decoded"
and "is an import", and record the one-shot `0x004E9170` delete. Then decide
whether that moves the log reading off Inferred, and make **all** carriers say
whichever answer you pick.

Then M1 and M2: state the gap claim as "no relocated value in the band other
than the table's own lies within `0x10` below or `0xE0` above the range", delete
"this is what closes it", and say plainly that the base-plus-index form is not
closed for bases outside the band or above the range.

Then M4 and M5, which are two carriers the fourth-round audit named explicitly
and by line; then M6-M11; then the smaller four.

Two process notes, both earned by this round:

- A **presence** sweep is not enough either. M4 is a file that contains the
  corrected phrasing *and* the contradicted one. The test that catches it is:
  for each claim, enumerate every sentence in every carrier that bears on it,
  and read them together. Round 3 swept the defect phrase, round 4 swept the
  corrected phrase, and both missed the same file.
- Three of this round's defects (M1, M3, M8) are sentences written to fix a
  defect that assert something false about a fact the fixer had in hand. M1
  contradicts a number in the same section; M3 contradicts the file §0 spends
  a page crediting; M8 re-types the error §0 just corrected. Before committing
  a fix, check the new sentence against the artifact it describes, not against
  the audit that asked for it.

## Git commit if applicable

None by the auditor. Nothing in the packet was modified.
