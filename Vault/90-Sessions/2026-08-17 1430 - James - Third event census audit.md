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

# Third event census audit

## Agent

James, fresh context, third audit of the event packet. No knowledge of the two
earlier rounds beyond the artifacts committed at `76f126c`; both prior auditors'
findings were treated as claims to re-test against the binary, not as settled.

## Goal

Judge `76f126c`, which claims to fix the ten defects a second-round James audit
raised against `311f79b`, and to adopt one finding offered by that audit as a
new §2.1. Three questions: did each of J1-J10 land in **every** carrier and is
each correct; is the adopted §2.1 right; and what have all three rounds missed.

## Files inspected

`CLAUDE.md`; [[START HERE]]; [[Agent Operating Manual]];
`static/exports/BIN-97c95ba5572dce63/SUBSYS-event-static-census.md`;
[[EXP-20260817-185 - PC event subsystem static census]];
[[FUNC-97C95BA5572D-0042DB10]]; [[FUNC-97C95BA5572D-0042D980]];
[[2026-08-17 1130 - Claude - PC event subsystem census]];
[[2026-08-17 1230 - James - Event census audit]];
[[2026-08-17 1330 - James - Second event census audit]]; the full `76f126c`
diff including [[Current State]], [[Subsystem Coverage Map]],
[[Subsystems MOC]], [[Functions MOC]], `KU-071` in [[Known Unknowns]] and
[[Session Index]]; the trees `4e0157f` and `311f79b` for the earlier drafts of
§0 and `4e0157f^` for the novelty negative; the prior art the packet cites —
`SUBSYS-audio-static-census.md`, `SUBSYS-creature-actor-static-census.md`,
[[EXP-20260816-159 - PC audio subsystem static census]] and
[[EXP-20260816-172 - PC creature actor pool and behaviour VM census]]; the
generated `static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json`, parsed as
JSON rather than grepped; and `work/copies/BUGS_PC-full-disc/bugs.exe`,
re-hashed to
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.

## Experiments inspected

`EXP-20260817-185` (the packet), `EXP-20260816-159` (the `0x004D81E8` prior art)
and `EXP-20260816-172` via the creature export (the row's earlier anchor).

## Changes made

None. This note only. No packet artifact was touched and nothing was committed.

## Conclusions

**REJECT.** Eleven defects, plus five smaller ones.

The model underneath is right and I re-derived all of it: the table geometry,
the record layout, all seven extents, the eight thunk edges, the nine reachers,
both decoded records, the five strings and the disjointness result all hold. J1,
J2, J3, J4, J7, J8 and J9 are correctly and completely fixed. But the two fixes
that matter most this round both failed again in the same way the round-2 audit
named: **J5's fix over-corrected into a new false causal claim, J6's and J10's
fixes landed at some occurrences and not others, and J5's fix never reached one
of the two dossiers at all.** The one thing adopted from the previous audit —
§2.1 — was adopted with its central number wrong.

### Part A — the ten fixes, re-verified

Correct and complete:

- **J1.** `ghidra-evidence.json` holds exactly six entries covering
  `0x0042D980`, `0x0042DA70` and `0x0042DB10` — a `FUN_` and a `thunk_FUN_`
  each. The three `thunk_FUN_` `callers` lists are `['0043dc5a','00405cb0']`,
  `['0043daeb','00405c54','00405a73']` and `['0043daf5','0043db10']`; the three
  `FUN_` lists are empty. That is 7 of the 9 reachers §2 lists. The file has no
  entry at `0042d950`, `0042d9d0`, `0042da00`, `0042dca0`, `0042dd90` or at any
  of the four dead thunks. §0's corrected paragraph, the [[Current State]]
  paragraph and the [[Subsystem Coverage Map]] row all now say this correctly.
- **J2.** `FUN_0042db10`'s body renders **two** slots as calls
  (`&DAT_005982b4`, `&DAT_005982bc`); `&DAT_005982b8` appears only as
  `(&DAT_005982b8)[iVar2 * 0xf] = 0`. It renders **four** format strings;
  `004d823c` appears only in `FUN_0042da70`. `thunk_FUN_0042d980` renders
  `_DAT_005982ac = puVar1 + -2` and `iVar2 = 0x10`. Every bullet in the
  corrected list checks out against the JSON.
- **J3.** Nine reachers, everywhere: §2's rows, §6's list and `EXP-185`'s
  Unknown set all say nine and name the same nine. I re-derived them from a
  branch-target index over all 357,242 decoded instructions:
  `0x00405CB0`/`0x0043DC5A` → `0x004013AC`;
  `0x00405A73`/`0x00405C54`/`0x0043DAEB`/`0x004AE863` (calls) and
  `0x004121A1` (`e9` tail `jmp`, last instruction before padding) →
  `0x00401C44`; `0x0043DAF5`/`0x0043DB10` → `0x004017B2`.
- **J4.** All three clearing rows in §2, §3 and the `0042DB10` dossier now say
  "every field except the id at `+0x00` and the name at `+0x10`". No "zero the
  record" survives anywhere. The four clear runs
  (`0x0042DA10`-`0x0042DA3D`, `0x0042DAB0`-`0x0042DAD0`,
  `0x0042DB83`-`0x0042DBB0`, `0x0042DD13`-`0x0042DD40`) touch only `E4`, `E8`,
  `E0`, `B2`, `E2`, `B4`, `B8`, `BC`.
- **J7.** §5's per-instance-state row now lists `+0x02`, `+0x30`, `+0x32` and
  `+0x38` beside `+0x34` and matches §6.
- **J8.** The session note body was genuinely corrected, not appended to: all
  five surviving phrases are gone (`create/update/destroy` → `+0x08` unnamed;
  "Two events are statically registered" → two call sites; the
  inference-free claim → two flagged inferences; eight displacements → nine;
  three dead thunks → four). The audio coverage row and the
  [[Subsystems MOC]] audio line no longer say "invoked at".
- **J9.** [[FUNC-97C95BA5572D-0042DB10]]'s Inferred section now carries the
  log-formatter reading.

Correct where it landed, incomplete elsewhere: **J5** (see K2, K3), **J6** (K4),
**J10** (K5), **J1** (K6). The adopted §2.1 is wrong (K1).

### Part B — the numbered defects

**K1 (severe) — §2.1's headline number counts sites from a range wider than the
range it states.** §2.1: "Every instruction in the image that references any
address in `[0x005982A0, 0x005986F0)` — the table plus its buffer, with margin
either side — was enumerated: **52 sites, of which 47 lie inside
`0x0042D950`-`0x0042DD94`**. The five outside are all the same address,
`0x00598290`".

`0x00598290` is **not in** `[0x005982A0, 0x005986F0)`. It is 16 bytes below the
stated lower bound and 32 below the table base, i.e. outside the "margin" the
sentence claims. So the five sites do not belong to the enumeration they are
being counted into, and 52 is not the number of sites referencing the stated
range.

Two independent methods give the same answer. A whole-file 4-byte little-endian
scan for values in `[0x005982A0, 0x005986F0)` returns **47** hits, every one
inside the seven functions and none outside. Widening the low bound to
`0x00598290` returns 52 — the missing five being `0x00405C0D`, `0x00405C83`,
`0x0043DF67`, `0x0043DFB1`, `0x004AE8F9` (operand offsets of instructions at
`0x00405C0C`, `0x00405C82`, `0x0043DF65`, `0x0043DFAF`, `0x004AE8F7`). So 52
is the count over `[0x00598290, 0x005986F0)`, and the paragraph is the two
ranges glued together.

The previous audit's own figure — "47 whole-file hits, all inside them" — was
right. The packet adopted the finding, broadened the count, and did not
broaden the range. Propagated verbatim into
[[2026-08-17 1130 - Claude - PC event subsystem census]] ("of the 52 instruction
sites referencing `[0x005982A0, 0x005986F0)`") and into the commit message.

Fix: state the scanned range as `[0x00598290, 0x005986F0)` and keep 52/47/5, or
keep `[0x005982A0, 0x005986F0)` and say **47 sites, all inside**, mentioning
`0x00598290` separately as a nearby address the sweep deliberately reached down
to.

**K2 (severe) — §3's new causal sentence is false at two of the three sites it
covers, and contradicts §1.1 in the same commit.** §3 step 3, added by the J5
fix: "The name survives the clear, which is what lets the log line still print
it."

Only one of the three sites prints the table record's name.

- `0x0042DAD3` (destroy-all): the argument is `lea ecx,[esi-0x24]` at
  `0x0042DABD` — the **table** record's `+0x10`. Here the sentence is true.
- `0x0042DBB6` (register): the argument is `lea edx,[ebx+0x10]` at `0x0042DB71`
  — the **caller's** record, pushed at `0x0042DB77`. The clear writes only the
  table record, so nothing about the printed name depends on surviving it.
- `0x0042DD46` (delete-one): `add esi,0x10` at `0x0042DD01`, `push esi` at
  `0x0042DD07`, where `esi` is `[esp+0xc]` — again the **caller's** record.

§1.1, corrected in this same commit under J6, already states the fact that
refutes the sentence: "only 2 of them (`0x0042DAA5`, `0x0042DAD3`, in the
destroy-all pass) take it from the *table* record; the other 6 pass the
caller's". One fix in this commit contradicts another fix in this commit.

Fix: scope the clause to `0x0042DAD3`, or delete it. The ordering claim it is
attached to — last store `0x0042DBB0`/`0x0042DAD0`/`0x0042DD40`, log call
`0x0042DBB6`/`0x0042DAD3`/`0x0042DD46` — is itself correct; I verified all six
addresses.

**K3 (moderate) — the J5 fix never reached
[[FUNC-97C95BA5572D-0042DB10]].** Its Confirmed section still reads: "then
**logs `0x004D830C` and zeroes** `+0x34`, `+0x38`, `+0x30`, `+0x02`, `+0x32`,
`+0x04`, `+0x08`, `+0x0C`". That is the exact log-then-zero inversion J5
rejected, in a Confirmed set, in one of the two dossiers the commit message
says were swept. The eight stores run `0x0042DB83`-`0x0042DBB0`; the call to
`0x00401CF8` is at `0x0042DBB6`.

**K4 (moderate) — the second half of the J6 fix never reached
`EXP-20260817-185`.** Its Confirmed set still reads: "`+0x10` a name **passed
as a `%s` of every log line**". The round-2 audit named this carrier explicitly
("The same wording sits in `EXP-20260817-185`'s Confirmed set"). In a bullet
headed "A record carries three native callbacks" the phrase describes the
**table** record's field, and the table record's `+0x10` is the argument at 2
of the 8 log calls, not 8. The export §1.1 now carries the corrected "at all 8
log calls, but only 2 of them ... take it from the *table* record"; the
experiment note does not.

**K5 (moderate) — the J10 fix never reached the export's own §2 table.** §2 row
`0x0042D950`: "zeroes the **128-byte buffer** at `0x00598670`". §1, three
sections earlier and corrected in this commit, says "Its own extent is not
given by any instruction — 128 bytes is the width of the write, not a known
object size." [[Current State]] and [[Subsystems MOC]] were both corrected; the
extent table in the same file was not. The only evidence is `mov ecx,0x20` +
`rep stos` at `0x0042D951`-`0x0042D95D`.

**K6 (minor-moderate) — the J1 fix never reached [[Subsystems MOC]].** Its
event section still says only "Table geometry and record layout are also in
`ghidra-evidence.json`; re-derived, not first found, by `EXP-20260817-185`".
The correction that the caller data is prior art too — 7 of the 9 reachers,
already thunk-resolved — landed in [[Current State]] and the
[[Subsystem Coverage Map]] row and stops there. Same enumeration, one carrier
short.

**K7 (moderate) — §2.1 states no method and carries no caveat, while making the
strongest claim in the document.** It concludes "no instruction anywhere
outside these seven functions touches the table, the flag, the current-record
global or the buffer", and introduces itself as "A stronger result than the
caller analysis". No method is named. The only method that can produce such a
figure is an absolute-value/displacement sweep, which by construction cannot
see a reference computed from a base held in a register — the same class of
miss §6's last bullet concedes for call targets, and the same class the input
census's `GetAsyncKeyState` finding is cited for. §6 has no data-reference
counterpart to that caveat.

For what it is worth, the absolute-form half of the claim can be made
**provably** complete rather than scan-complete, and the packet did not use the
available method: every absolute address operand in this image is relocatable
and therefore listed in `.reloc`. Decoding the 26,713 type-3 relocations and
reading the dword at each target gives exactly **47** entries whose value lies
in `[0x005982A0, 0x005986F0)`, all inside the seven functions, and exactly
**52** in `[0x00598290, 0x005986F0)` with the same five outside. That is an
exhaustive enumeration of the absolute form, not a sample of it — and it agrees
with the byte scan hit for hit. It still says nothing about computed
references, which is precisely the caveat §2.1 needs.

**K8 (moderate) — §0's generated-prior-art enumeration is still short, on the
one claim the packet flags as Inferred.** §0: "It holds **six** relevant
entries — a `FUN_` entry and a `thunk_FUN_` entry for each of `0x0042D980`,
`0x0042DA70` and `0x0042DB10`."

`ghidra-evidence.json` also holds `thunk_FUN_004adea0` (address `00401cf8`) and
`FUN_004adea0` (address `004adea0`), both with full bodies, and
`FUN_004adea0.callees` = `['004b0730','004b13a0','004b13e0','004b0150',
'004b04e0']`. Those bodies render the whole of §1's log-formatter derivation:
`undefined4 auStack_400 [256]`, the `0x100`-iteration zeroing,
`FUN_004b0150(auStack_400, param_1, &stack0x00000008)`, and the write through
`FUN_004b0730`/`FUN_004b13a0`/`FUN_004b04e0`. §2 nonetheless says "'Log
formatter' for `0x004ADEA0` is **this census's own reading**". This is the third
round on the same axis: D7 rejected the packet for under-crediting this file,
J1 rejected the over-correction, and the entries underpinning §1's central
refutation ("It is **not** the log formatter's output buffer") are still
uncredited while §0 asserts an exhaustive count of relevant entries.

Worse for the packet, the binary carries a stronger anchor than either the
export or its Inferred classification uses, and §0's grep of "every address
subsequently used" never reached it: at `0x004ADEFB`-`0x004ADF05` the function
pushes `0x004E9260` and `0x004E9264` into `0x004B0730`, and those decode from
file bytes as `"at"` and `"bugs.log"`. A function that opens `bugs.log` in
append-text mode and writes the formatted buffer to it is not an inference of
the same weight as "a `vsprintf`-shaped call".

**K9 (moderate) — [[Current State]]'s audit history is now false and stops one
round short.** It reads: "A fresh James audit **rejected** the first version of
this packet with 12 defects: ... All twelve were verified against the binary and
corrected before re-audit." The re-audit established that four of the twelve
had landed only where the wording first occurred and one had over-corrected
into a false claim, so five of the twelve were **not** corrected before
re-audit. The 10-defect second rejection appears nowhere in that paragraph; the
only trace of it in the whole note is an oblique clause three paragraphs
earlier ("a second-round audit caught this packet asserting those lists were
empty"). The creature packet's precedent (`2cb6b07`, "Replace creature census
audit history with a per-round fact table") is the standard this row should
meet.

**K10 (minor-moderate) — the [[Subsystem Coverage Map]] row's provenance is
stale.** Row: "EXP-185, **corrected after a first-round James rejection**". Two
rejections have now occurred. The same table's Input row reads "**accepted** at
`EXP-20260817-184` after two rejections and corrections" and its Enemies row
"after seven rejections and corrections", so counting rounds is the table's own
convention and this row now understates by one.

**K11 (minor-moderate) — §2.1 exists in no experiment note.** The closure result
is adopted this round as a new Confirmed-grade section of the export and is
restated in the session note, but `EXP-20260817-185` — the note that carries
the Confirmed / Inferred / Unknown classification for this packet and names the
export as its artifact — does not mention it, the 52 or 47 figure, or
`0x00598290` anywhere. A headline result that lives only in an artifact and a
session note is not classified evidence.

### Smaller, also wrong

- **K12.** §1: "at the four sites whose format string has two `%s`, it supplies
  the second one **and renders empty because it was just zeroed**." The scope
  section says "This census claims **no** runtime behaviour." What a `%s`
  renders is a runtime statement, and it rests on the `vsprintf` reading the
  packet itself classifies as Inferred. D12 was raised for this class of
  wording.
- **K13.** §0: "**No authored Vault note or markdown export mentions any of:**
  `0x0042D950`, ... `0x00401CF8` or `0x004ADEA0`." Present tense, and false in
  the tree that contains the sentence — all fifteen now appear in authored Vault
  notes, this packet's included. Against `4e0157f^` the negative does hold; I
  re-ran it for all fifteen and got zero hits each. It needs "before this
  packet".
- **K14.** §0: "The `FUN_` entries' `callers` lists are empty, **which is what
  the first two drafts of this section looked at**." The first draft
  (`4e0157f`) said only "`ghidra-evidence.json` contains decompilations
  mentioning the principal addresses used here" and made no callers claim at
  all. Only the second draft (`311f79b`) asserted emptiness.
- **K15.** §1.2: the three `movsx` reads are "each **followed directly** by the
  `*3`/`*5`/`shl 2` sequence". At `0x0042DA00` an `xor ecx,ecx` intervenes
  (`0x0042DA05`) and at `0x0042DB18` two `push`es do (`0x0042DB1B`,
  `0x0042DB1C`). The substantive claim — no range test between the read and the
  first access — is correct at all three; "directly" is not.
- **K16.** §1.1's preamble still asserts "**independently** cross-checked
  against the destroy pass" at the point of assertion, three paragraphs before
  "Two limits on how independent this cross-check is". Round 1 raised this as an
  uncounted minor and it survives unchanged.

### What I re-derived and confirm

- SHA-256 re-hashed to
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
  `objdump -h` matches §0's section table exactly; `.data` `0x004C1000 +
  0x2C400 = 0x004ED400`, and `0x00598290` is the lowest `.bss`-class address
  the document cites.
- Base `0x005982B0` and stride `0x3C` from `0x0042DBBE`-`0x0042DBD5`, quoted
  byte-for-byte in §1 and correct including the `; eax = id * 15` comment; the
  16 bound from `mov edi,0x10` at `0x0042D988` and `mov ebp,0x10` at
  `0x0042DA79`; `0x005982B0 + 0x3C0 = 0x00598670`; destroy-pass origin
  `0x00598668 = 0x005982B0 + 15 * 0x3C + 0x34`, step `-0x3C`.
- The full §1.1 layout in every addressing form, including the destroy pass's
  **nine** distinct displacements (`[esi]`, `[esi+0x4]`, `[esi-0x4]`,
  `[esi-0x2]`, `[esi-0x28]`, `[esi-0x24]`, `[esi-0x2c]`, `[esi-0x30]`,
  `[esi-0x32]`) and the `+0x34` row's set-, test- and clear-site lists, which
  are exhaustive as written.
- `0x005982C0`: zero occurrences whole-file. `0x005982AC`: exactly two, the
  `a3` store immediates at `0x0042D99A` and `0x0042D9DA`; never read.
- All seven extents and `0x0042DD90`, each with a single `ret`; file offsets
  under `VMA - 0x400C00`. Direct branches into `[0x0042D950, 0x0042DD94]` from
  outside: exactly eight, all `jmp`s from the `0x00401xxx` table
  (`0x004010C8`, `0x00401140`, `0x00401217`, `0x004013AC`, `0x0040169F`,
  `0x0040179E`, `0x004017B2`, `0x00401C44`), none landing mid-function. The
  only outbound **direct** target from any of the seven is `0x00401CF8`; the
  eight `call 0x401cf8` sites and the four indirect callback calls are the
  complete outbound set.
- The four dead pairs: zero branches target `0x0040169F`, `0x0040179E`,
  `0x00401217` or `0x00401140`, and all eight whole-file little-endian scans
  (four thunks, four functions) return zero.
- The 4-of-8 clear/log split, with the clears at `0x0042DA9A`, `0x0042DB4B`,
  `0x0042DC0E`, `0x0042DCD5` preceding the calls at `0x0042DAA5`, `0x0042DB56`,
  `0x0042DC19`, `0x0042DCE5`, and those four being exactly the two-`%s`
  formats. `0x004ADEA0` verified instruction for instruction against §1.
- All five `EVENT` strings byte-exact at `0x0D6E3C`, `0x0D6E64`, `0x0D6EA4`,
  `0x0D6ECC`, `0x0D6F0C`, with `%s` counts 1/2/1/2/1, and each referenced
  **exactly** at the sites §3 lists and nowhere else — whole-file scan, 1/3/1/1/2
  occurrences respectively. §3's "and nowhere else" is earned.
- Both records byte-for-byte at file `0x0D6DA8` and `0x0D6DE8`: ids 2 and 3,
  `+0x02` zero, `+0x30`..`+0x3B` zero, names `"WINDOWS"`/`"DIRECTX"` at
  `+0x10`, and all six callback thunks resolved as stated. `0x004D81A8` and
  `0x004D81E8` each occur exactly once in the image. §4's quoted
  `0x0043DAEB`-`0x0043DB10` block is byte-exact, and `jne 0x43db0b` does land
  on the `push 0x4d81e8`.
- §5 in both directions, plus the creature-side figures against
  `SUBSYS-creature-actor-static-census.md`: 26-entry dispatch table at
  `0x0041E848` (line 566), bodies `[0x004C7D00, 0x004C83F0)` (line 753), pool
  `[0x0059B628, 0x0059D728)` stride `0x84`, `+0x70` program counter, `+0x60`
  wait counter, type-`0x23` = `LOAD: Type 35, CreatListRam.`.
- §0's authored prior-art quotations are verbatim from
  `SUBSYS-audio-static-census.md` (lines 174-186),
  `EXP-20260816-159` (lines 114-117) and the creature export (lines 917-921);
  the §4.1 refinement is right and byte-compatible.
- Beyond the packet: the enclosing function of both registration sites is
  `0x0043DA40`-`0x0043DFE6`, reached only through thunk `0x00401866`, which is
  itself called from `0x004B17AA`; no branch anywhere targets any address in
  `(0x0043DA40, 0x0043DB04)`. The second-round audit's counter-finding holds.
- Hygiene: `make vault-lint` 520 notes / 0 errors / 0 warnings;
  `make audit-tracked` 0 violations; `make test` 686 passed in 17.48s — all
  three run by me, logs read. The commit's hygiene figures are accurate.

**Bounded remains earned.** "Real PC evidence at a documented boundary, with
major parts open" still fits, and none of K1-K16 touches the geometry, the
layout, the extents, the records or the disjointness result. K1 weakens §2.1
from "closed on the absolute-address axis" to exactly that — but the closure
itself survives, at 47 sites rather than 52.

## New hypotheses

None.

## Contradictions discovered

Three, all internal to the packet and all introduced or left by this commit:
§3's "the name survives the clear, which is what lets the log line still print
it" against §1.1's "only 2 of them ... take it from the *table* record" (K2);
§2's "the 128-byte buffer" against §1's "128 bytes is the width of the write,
not a known object size" (K5); and [[FUNC-97C95BA5572D-0042DB10]]'s "logs
`0x004D830C` and zeroes ..." against §3's zero-then-log ordering (K3).

## Tests run

`make vault-lint` 520 notes, 0 errors, 0 warnings; `make audit-tracked` 0
violations; `make test` 686 passed in 17.48s. Binary work: `objdump -d -M intel`
over the full image (357,242 instructions) and over each cited range; a Python
branch-target index over all direct `call`/`jmp`/`jcc`; whole-file 4-byte
little-endian scans for every thunk, function, field, string and record address
cited; interval sweeps over `[0x005982A0, 0x005986F0)`,
`[0x00598290, 0x005986F0)`, `[0x00598280, 0x005982A0)` and
`[0x00598670, 0x005986F0)`; an exhaustive decode of the `.reloc` directory
(26,713 type-3 relocations) as an independent enumeration of every absolute
address operand in the image; byte decoding of the two records, the five
strings, the two `0x004ADEA0` filename arguments and the section mapping; and
`ghidra-evidence.json` parsed as JSON with its six event entries, its two
`004adea0` entries and every `data_references` list read in full.

## Unresolved questions

`KU-071`; the six callback targets; whether any event is registered outside the
two static sites; whether computed dispatch or a computed data reference
reaches any of these seven functions — my methods share the packet's blind spot
on the second and §6 has no caveat for it (K7); the meaning of `+0x02`,
`+0x30`, `+0x32`, `+0x38`, `0x0059F7F0` and of a `0x005982AC` nothing reads;
the true extent of the buffer at `0x00598670`. Not verifiable from artifacts:
that the prior-art greps and extent reads happened before analysis, and that no
`originals/` path, asset or PS1 source was touched.

## Recommended next action

Fix K1 first — it is the only wrong number in the packet and it is in the one
section this round added. Then K2 and K3, which are the J5 fix breaking in two
directions at once. Then the three unpropagated fixes K4, K5, K6, and only then
K7-K11. Before committing, run the sweep the last commit message promised and
grep the **corrected** phrasing, not the defect phrasing, across `Vault/` and
`static/exports/` — every one of K3, K4, K5 and K6 is a place where the new
wording is absent, which a defect-phrase grep will not find. Re-audit with
fresh context afterwards.

The lesson this round adds to the last one: **an adopted finding is a borrowed
claim, and a borrowed claim needs the same verification as an authored one.**
§2.1 arrived from an audit with the number 47 attached to the range
`[0x005982A0, 0x005986F0)`; it was committed as 52 against the same range,
"independently re-verified".

## Git commit if applicable

None by the auditor. Nothing in the packet was modified.
