---
type: session
date: 2026-08-17
agent: Claude
status: closed-unaccepted
tags:
  - session
  - research/coverage
  - re/events
---

# PC event subsystem census

## Agent

Claude.

## Goal

Open the Event/scripting row of [[Subsystem Coverage Map]], the last of the
recorded Actors/AI → Input → Event/scripting preference, following the startup
sequence in [[START HERE]].

## Files inspected

`Vault/00-System/` startup notes (re-read this session); the coverage map;
every file in `static/exports/BIN-97c95ba5572dce63/` including
`ghidra-evidence.json`, grepped for the five `EVENT` strings and every address
used, before any analysis; `SUBSYS-audio-static-census.md` and
`EXP-20260816-159` for the `0x004D81E8` prior art;
`work/copies/BUGS_PC-full-disc/bugs.exe`, re-hashed to
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.

## Experiments inspected

`EXP-20260816-172` (the row's anchor) and `EXP-20260816-159` (the `0x004D81E8`
record and its missing caller).

## Changes made

New export `SUBSYS-event-static-census.md`; new experiment note
[[EXP-20260817-185 - PC event subsystem static census]]; new dossiers
`FUNC-97C95BA5572D-0042DB10` and `-0042D980`; Event/scripting row Touched →
Bounded; `KU-071`; the audio row and Subsystems MOC audio line updated with the
closed caller question; entries in the three MOCs, [[Current State]] and this
index.

No script, parser, test or reimplementation module changed. No game asset,
`originals/` path or PS1 source touched. No Decision Log entry — coverage
censuses have not added them, and this packet records no decision.

## Conclusions

The event subsystem is a 16-slot callback registry, not a VM and not a trigger
stream, and it is disjoint from the creature scripts by address in both
directions. Each record carries an id, a name and three native callbacks
(create, `+0x08`, destroy — `+0x08` is left unnamed because no log string
describes it). Two static registration call sites pass `"WINDOWS"` and
`"DIRECTX"`; whether either executes is not established.

The most useful by-product is a cross-link: `0x0042BA60`, whose absent caller
the audio census explicitly recorded, is the `"DIRECTX"` event's create
callback.

## New hypotheses

None. The export's §6 is the normative list of what this packet does not
establish; this note does not restate it.

Two readings are marked Inferred there rather than Confirmed: the 32-byte width
of the name at `+0x10` (adjacency, not an instruction) and that `0x004ADEA0`
*writes* to `bugs.log` (that it **deletes** it is confirmed by
`KERNEL32.dll!DeleteFileA`; the write runs through three functions this census
does not decode).

## Contradictions discovered

None. One prior-art **refinement**: the audio census's "count of 3" at
`0x004D81E8` is the event id. Its offsets were exactly right and are
independently confirmed.

## Tests run

No repository test suite is affected — this packet changed no code. Method
checks: all seven function extents established from their single `ret` and
padding, with every direct branch inside each enumerated; the record layout
derived from `id`-scaled addressing and then cross-checked against the destroy
pass's backwards walk, all nine distinct displacements consistent; the five log
strings decoded from file bytes and each confirmed referenced only at the
listed sites; the four dead functions and their four thunks checked in both
directions, including whole-file absolute-value scans — eight scans, all
returning zero; and the disjointness from the creature VM tested by address
intersection both ways.

Two attributions failed verification during drafting and were corrected before
commit: a quotation attributed jointly to the audio export and `EXP-159` when
the wording is `EXP-159`'s, and a §4.1 quotation of the export that was
actually `EXP-159`'s phrasing. Both are now verbatim from the file named.

## Unresolved questions

`KU-071`; the six callback targets; whether any event is registered outside the
two static sites; `+0x02`/`+0x30`/`+0x32`/`+0x38`; `0x0059F7F0`.

## Audit outcome

A fresh-context James audit **rejected** the first version with **12 defects**.
It independently re-derived the table, stride, the 16-record bound, the record
layout, all seven extents and every decoded byte, and found those sound; the
defects were in claims layered on top of them.

| # | Defect | What the binary shows |
|---|---|---|
| D1 | "every log site clears" the buffer; `0x00598670` called the log formatting buffer | 4 of 8 log calls clear it, exactly the two-`%s` sites; `0x004ADEA0` formats into a `0x400`-byte stack local and `0x00598670` is pushed as a **vararg** |
| D2 | `0x0042D950` "no direct caller"; "the three whose thunks are empty" while claiming four dead | thunk `0x0040169F` exists and was missed; the dead conclusion survives but was not earned |
| D3 | destroy-all reacher list of four | `0x004121A1` tail-jumps into the thunk — five |
| D4 | clear zeroes "every field except the name" | no clearing path writes `+0x00` either; the id survives too |
| D5 | "all eight" displacements in the second derivation | nine; the missing one is `+0x32` at `0x0042DAC0` |
| D6 | `+0x34` site list | omitted the `0x0042DA80` test and the four clear sites |
| D7 | `ghidra-evidence.json` "contains decompilations mentioning the principal addresses" | it carries full bodies for three of the seven, rendering base, stride, layout and callback slots — the geometry is prior art |
| D8 | `+0x08` named "update" | no log string names it; create/destroy are the binary's own words, `+0x08` has none |
| D9 | "32-byte" name and "log-formatter" inside a set declared inference-free | both are inferences |
| D10 | `0x005982AC` "holds the current record pointer" | written twice, read nowhere |
| D11 | not recorded | the id is `movsx`-signed and scaled with no bounds check at three entry points |
| D12 | "the executable statically registers two events"; "invoked at" | two call sites in an unanalysed function; no runtime claim is supported |

Every one was re-verified against the binary before correcting — including one
refinement to the audit itself: the `cmp`/`jne` at `0x0043DAFD` guards only the
intervening `call 0x401c30`, not the second registration, so both calls are
unconditional *within* their function. What is unestablished is whether that
function runs.

Three of the twelve added findings rather than removing them: the never-read
global, the unchecked index, and the preserved id.

### Second round

A second fresh James **rejected the correction round** with **10 defects**. It
confirmed all twelve first-round findings were real and seven fixes correct and
complete — but found that four had landed **only where the wording first
occurred**, and one had **over-corrected**.

| # | Defect | What the binary/file shows |
|---|---|---|
| J1 | §0: "the `callers` list is empty for all three functions it does carry" | **False.** `ghidra-evidence.json` has six relevant entries; the three `thunk_FUN_` ones carry populated `callers` covering **7 of the 9** reachers. The D7 fix over-corrected into a new false claim, and the item put first among "what is new" was nearly prior art |
| J2 | §0: the `0x0042DB10` body renders "all three" callback slots as calls and "all five" format strings | Two calls (`+0x08` is a zero-store there) and four strings (`0x004D823C` is only in `FUN_0042da70`) |
| J3 | D3 unpropagated | §6 and EXP-185 still said eight reaching sites; there are nine |
| J4 | D4 unpropagated | §2's destroy-all and delete-one rows still said "zero the record" |
| J5 | §3 is headed "in order" but says "log … and zero" | Zeroing completes at `0x0042DBB0`/`0x0042DAD0`/`0x0042DD40` **before** the log calls at `0x0042DBB6`/`0x0042DAD3`/`0x0042DD46` |
| J6 | §1.1's `+0x10` row: "Accessed as `0x005982C0`" | That value occurs **zero** times in the file. `+0x10` has one derivation, not two — and only 2 of 8 log calls take the name from the *table* record |
| J7 | §5: per-instance state "`+0x34` only" | Contradicts §6's four unknown fields, which are copied in and cleared |
| J8 | The commit said the session note was corrected; it was appended to | Five defects survived verbatim in its original body |
| J9 | `FUNC-…-0042DB10` still declared "Inferred: Nothing" | Its Callees section now carries the log-formatter reading — D9's exact failure mode |
| J10 | "a 128-byte zeroed buffer" | Only the width of the write is evidence, not the object's extent |

The pattern is the lesson: **a fix applied at the first occurrence is not a fix
applied**. The correction round was verified defect-by-defect against the
binary but not swept across carriers, so four fixes were half-landed and one
introduced a fresh false claim. This round ends with a scripted sweep of every
defect phrase across all ten carriers instead.

The audit also supplied a **stronger result** than the packet claimed, which I
re-verified independently and adopted as §2.1: of the 52 instruction sites
referencing `[0x005982A0, 0x005986F0)`, 47 are inside the seven functions and
the other five all reference `0x00598290`, which sits below the table base and
was already recorded as outside the subsystem.

### Third round

A third fresh James **rejected** again, with **11 numbered defects plus 5
smaller**. Seven of the ten round-2 fixes were correct and complete; the
failures were in the two that mattered most and in the section adopted from the
round-2 audit.

| # | Defect | What the binary/file shows |
|---|---|---|
| K1 | §2.1: "**52 sites**, of which 47 lie inside … the five outside are all `0x00598290`" | `0x00598290` is **not in** the stated range `[0x005982A0, 0x005986F0)`. Within that range there are **47**, all inside, none outside. The count came from a wider range than the bound written next to it — I adopted the audit's 47/all-inside result and broadened the number without broadening the range |
| K2 | §3: "The name survives the clear, which is what lets the log line still print it" | False at 2 of 3 sites. `0x0042DBB6` uses `lea edx,[ebx+0x10]` and `0x0042DD46` uses `add esi,0x10`/`push esi` — the **caller's** record. Only `0x0042DAD3` reads the table record. §1.1's own fix said this in the same commit |
| K3–K6 | J5, J6, J10, J1 each unpropagated to one carrier | Third occurrence of the same failure mode |
| K7 | §2.1 named no method and carried no computed-reference caveat | Now uses the base relocation table — exhaustive for the absolute form by construction |
| K8 | §2 called the `0x004ADEA0` log-formatter reading "this census's own reading" | `ghidra-evidence.json` carries `FUN_004adea0`/`thunk_FUN_004adea0` rendering the whole derivation. **Third round on the prior-art axis.** The audit also supplied a far better anchor the packet had never found |
| K9–K11 | Propagation: a now-false "all twelve were verified", an unrecorded second rejection, a stale round count, §2.1 missing from the experiment note | — |
| K12–K16 | Runtime wording, a present-tense novelty negative, a wrong claim about which draft did what, "followed directly" where instructions intervene, and an over-strong "independently cross-checked" | — |

**K8 is the most valuable finding of all three rounds.** `0x004ADEA0` pushes
`0x004E9264` and `0x004E9260` at `0x004ADEFB`-`0x004ADF05`, which decode from
file offsets `0x0E7E64` and `0x0E7E60` as **`"bugs.log"`** and **`"at"`**. The
log formatter is no longer an inference at all — it opens a named file in
append-text mode. That removes one of the packet's two remaining inferences.

**K1 and K7 together** upgraded §2.1 from a grep result to a proof. All 26,713
type-3 base relocations were decoded and dereferenced: exactly 47 point into
`[0x005982A0, 0x005986F0)`, all 47 inside the seven functions. A PE loader must
relocate every absolute 32-bit reference, so no absolute reference can hide
from this enumeration — and the two limits (the computed form, and the
deliberate exclusion of `0x00598290`) are now stated rather than glossed.

### Fourth round

A fourth fresh James **rejected** with **8 defects plus 4 smaller**. Thirteen
of the sixteen round-3 fixes were correct and complete. Two findings matter
more than the individual defects.

**Three fixes got a fact wrong that the audit requesting them had stated
correctly.** L2: the round-3 audit gave `lea edx,[ebx+0x10]` at `0x0042DB71`;
the fix wrote `0x0042DB6E`, which is the `movsx` before it. L3: the audit said
only two `push`es intervene at `0x0042DB18`; the fix added an `xor` that sits
*before* the read. L4: the paragraph written to credit `ghidra-evidence.json`
mis-stated which functions receive `s_bugs_log_004e9264` — it goes to
`FUN_004b13e0` and `FUN_004b0730`, not to the two that receive the handle.
Transcribing an auditor's correction is not the same as verifying it.

**A defect-phrase sweep cannot find a carrier where the corrected phrasing is
absent.** L1, L9 and L10 are exactly that: the round-3 sweep searched for the
old wording and found none, while three carriers had simply never received the
new wording. This round therefore runs a **presence** sweep — for every carrier
mentioning `0x004ADEA0`, assert the inference flag, the `"bugs.log"` anchor and
the `0x008620AC` gate are all present — and it caught five gaps the phrase
sweep could not.

| # | Defect | What the binary/file shows |
|---|---|---|
| L1 | The packet stated **both sides** of its own Confirmed/Inferred boundary | Export and the dossier said the log reading is no longer inference; EXP-185's Inferred list, the session note's New hypotheses and Current State still said it was |
| L2 | `lea edx,[ebx+0x10]` cited at `0x0042DB6E` | It is at `0x0042DB71`; `0x0042DB6E` is `0f bf 03 movsx eax,[ebx]` |
| L3 | "an `xor` and two `push`es are interleaved" at `0x0042DB18` | `xor ebp,ebp` is at `0x0042DB16`, before the read; only the two `push`es intervene |
| L4 | `s_bugs_log_004e9264` "passed to `FUN_004b0730`/`FUN_004b13a0`/`FUN_004b04e0`" | It goes to `FUN_004b13e0` and `FUN_004b0730`; the other two receive the returned handle. Fourth round in a row with a wrong statement about this file |
| L5 | A sentence severed by string substitution, plus four unwrapped lines | Substitution damage; fixed and the file rewrapped |
| L6 | §1.1's preamble claimed the cross-check "does not … supply `+0x10`'s only access form" | It *is* the only source — `[esi-0x24]` at `0x0042DA9C`/`0x0042DABD`. Contradicted the row it introduced |
| L7 | §2.1 written as a proof, but the proof did not close | The enumeration filters on the relocated **value** landing in range, so a base relocated outside and indexed inside escapes it — the very form this subsystem uses. Closed by a separate sweep: of 157 distinct relocated values in `[0x00597000, 0x0059A000)`, none lies between `0x00598290` and `0x005987D0` |
| L8 | "`0x004ADEA0` writes the game's log file … a decoded byte anchor, not an interpretation" | Over-claimed. The strings are decoded; the conclusion is not. `0x004B0730`, `0x004B13A0`, `0x004B04E0`, `0x004B13E0` are unanalysed, and the whole body is gated on `0x008620AC` at `0x004ADEA0`-`0x004ADEAF` |
| L9–L12 | Round-3 credited with a round-2 result; the coverage row never swept; `KU-071` dropped "direct" from "only outbound call" while six indirect callback calls exist; "immediately preceded/after" where one to four instructions intervene | — |

L7 and L8 are the substantive ones. (Round 5 then found the second sweep does
**not** close it either, and round 6 confirmed the withdrawal: §2.1 is a
negative on the absolute addressing form, full stop.) The closure result
appeared to need a second sweep, and the `"bugs.log"` finding was over-promoted from a decoded
anchor to a settled conclusion in the same round that discovered it.

### Fifth round

A fifth fresh James **rejected** with **15 defects** (5 severe, 6 moderate, 4
smaller). The model was again re-derived independently and held in full.

The single most valuable finding closes the question round 4 had left open.
**`0x004B13E0` reaches `KERNEL32.dll!DeleteFileA`** — `call DWORD PTR
ds:0x864670` at `0x004B13E5`, IAT slot `0x00864670`. (This note first called it
"a three-instruction wrapper"; the sixth-round audit showed it is
`0x004B13E0`-`0x004B140C`, 17 instructions with two `ret`s and a `GetLastError`
failure path. The import identification was right; the description of the
function was not.) And the guarded sequence at
`0x004ADEDB`-`0x004ADEF8` deletes `"bugs.log"` once (armed by `0x004E9170`,
which holds `1` in the image, cleared on first use) before the `"at"`-mode open.
So `0x004ADEA0` writes a log file is **Confirmed on a named import**, and round
4's demotion to Inferred — which I made on the audit's advice — was itself an
over-correction. The fopen/fprintf/fclose shape of the remaining three callees
stays inference, and nothing depends on it.

The other severe findings were mine:

| # | Defect | What the file shows |
|---|---|---|
| M1 | §2.1: "none lies between `0x00598290` and `0x005987D0`" | **Twelve** relocated values lie between — they are exactly the in-range ones behind the 47 counted three paragraphs above. The true statement needed "no value *outside* the range"; the qualifier that made it true was dropped |
| M2 | §2.1 claimed that sweep closed the indexed-base gap | It does not. The image has 6,473 distinct relocated values, 4,673 below the range and 1,788 above; `[base + reg]` has no distance bound, so no window sweep closes it |
| M3 | §2 said four callees are undecoded and none is an import | `ghidra-evidence.json` decodes all four, and one is `DeleteFileA`. **Fifth consecutive round with a wrong statement about that file** — this time *under*-claiming |
| M4 | `EXP-185` asserted both sides of the boundary in one file | Its Confirmed set said `0x004ADEA0` "writes `bugs.log`" while its Inferred set called that inference. A per-file **presence** sweep cannot catch a file containing both |
| M5 | L12 never reached `Current State` — the carrier round 4 named by line number | Fifth round of the same partial-propagation failure |

`0x005982AC`, §2.1 and the `0x004ADEA0` reading have now each produced defects
in three or more consecutive rounds. §2.1 is therefore **restated rather than
re-argued**: the plain result (47 absolute references, all inside the seven
functions) with an explicit statement of the two forms it does not cover, and
the closure claim withdrawn. Adding another layer of argument is what generated
K1, L7 and M1/M2 in turn.

M12 was self-inflicted twice over: the round-4 claim "the export is rewrapped"
was false, and this round's actual rewrap script destroyed YAML frontmatter in
three notes and split fourteen wikilinks in `Subsystems MOC`. Frontmatter was
restored from `HEAD`, the MOC reverted and its one edit re-applied, and the
export's one split wikilink repaired. Lint is clean; the lesson is that a
mechanical reflow does not belong anywhere near a shared MOC.

### Sixth round

A sixth fresh James **rejected** with **14 defects** (5 substantive, 5 moderate,
4 smaller). The model held a sixth time, and this auditor re-derived more of it
than any previous round — including a stronger form of §2.1 the export had not
claimed (all 47 references fall inside the seven **individual** extents, not
merely the enclosing span) and a stronger dead-thunk result (dead against
`rel32`, `rel8` *and* `0f 8x` sweeps).

The substantive findings:

| # | Defect | What the binary shows |
|---|---|---|
| D1 | "`0x004B13E0` is a three-instruction wrapper" | It is `0x004B13E0`-`0x004B140C`: 17 instructions, two `ret`s, with a `GetLastError` (IAT `0x008645DC`) failure path returning `-1`. The `DeleteFileA` identification was right; the description was not — **and the false sentence sits inside the fix for round 5's finding about that same function** |
| D2 | The session note's "New hypotheses" still filed the `0x004ADEA0` reading as open | Contradicting its own round-5 section 16 lines below. M4's exact failure mode, in the commit that fixed M4 |
| D3 | `EXP-185`'s Confirmed set still headlined "referenced only from these seven functions" | The export deliberately retitled §2.1 away from that; the retitling never reached the experiment note, so the over-reaching form survived only where labelled Confirmed |
| D4 | "relocation-exhaustive **closure result**" still on three handoff surfaces | The claim was withdrawn at round 5 — in the export. **Retractions were never swept**, only corrections |
| D5 | §1.1's `+0x10` producer list, "corrected" at round 5, still incomplete and still worded as exhaustive | Eight producers, not five: `0x0042DB4D`, `0x0042DC10` and `0x0042DCD7` were missing, the last an addressing form absent entirely |
| D8 | The round-5 promotion over-reached by one step | `DeleteFileA` confirms `0x004ADEA0` **deletes** `bugs.log`. That it **writes** a log still runs through `0x004B0730`/`0x004B13A0`, undecoded here — so the Confirmed claim is now the deletion plus the filename/mode hand-off, and the write stays Inferred |

**The structural change, adopted this round on the auditor's recommendation.**
The root cause of six rounds of propagation defects is that ten carriers each
*paraphrase* the same findings, so every correction is ten rewrites and ten
chances to be wrong — and five successive sweep strategies each caught the
previous failure mode and missed the next. From here the **export is
normative** and the Vault carriers point to it rather than restate it. D3 and
D4 also show retractions need sweeping, not just corrections; that sweep is now
part of the routine.

## Outcome

**Closed unaccepted at round 6** by researcher decision, recorded as
`DEC-20260817-138`. No seventh audit was run.

The reasoning, in short: nothing gates on this row, the Vault codifies no
acceptance requirement, and six independent re-derivations are unusually strong
support for the conclusions — while what the audit history actually demonstrates
is a *detail-level* defect rate. The honest response to that is to state it on
the export rather than keep grinding toward a stamp or hide the residue behind
one. The export now carries a status header saying: trust the conclusions,
re-derive the details.

`KU-071` remains open and carries the discriminating experiment.

## Git commit if applicable

One intentional commit; tree clean.
