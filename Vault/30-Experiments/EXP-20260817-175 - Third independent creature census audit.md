---
type: experiment
id: EXP-20260817-175
date: 2026-08-17
question: 'Do the corrections applied after EXP-174 hold, and does the creature census survive a third independent re-derivation?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline audit; GNU objdump 2.46; radare2 5.9.8; no runtime, debugger, or target write
environment_version: objdump 2.46-3.fc44
working_directory: /home/dev/ABLPC
configuration: fresh-context audit at clean HEAD 3f0debd; read-only toward game media and originals; nothing committed or modified by the auditor
artifacts:
  - static/exports/BIN-97c95ba5572dce63/SUBSYS-creature-actor-static-census.md
addresses:
  - "0x0041E845"
  - "0x0041E7FE"
  - "0x0041BD6C"
  - "0x0041C47D"
  - "0x0041DFA2"
  - "0x0059B684"
file_offsets: []
result: reject-wrong-function-extent-missed-writer-and-uncited-generated-export
created: 2026-08-17T01:30:00
updated: 2026-08-17T01:30:00
tags:
  - re/experiment
  - re/audit
  - re/actors
  - research/coverage
---

# EXP-20260817-175 - Third independent creature census audit

## Verdict

**REJECT** at `3f0debd`. For the third time the numeric analysis is fully
reproducible: all 26 opcode PC advances re-derived from raw handler bytes
before reading §5.2, then 463 instructions, zero misalignments, 69 branch/jump
instructions, zero off-boundary targets, and a digit-identical histogram —
together with every switch table, both loop terminations, the
`380 = 181 + 199` and `199 = 2 + 197` splits, the trailing-byte histogram and
every file offset. The auditor additionally ran the published §6.1
reproduction snippet verbatim and confirmed it passes, and confirmed the
boundary test has discriminating power: wrong branch formulas produce 8-36
failures.

The rejection rests on three Confirmed-level statements the bytes contradict,
plus a §0 that was still wrong about prior art.

## Defects

1. **The function extent is wrong, packet-wide.** `0x0041DC60`'s only `ret` is
   at `0x0041E7D3`, but that is not its end. `0x0041E7D4`-`0x0041E845` is
   entered from inside the function by `jne 0x41e7d4` at `0x0041E6CD` and
   `jge 0x41e7d4` at `0x0041E6D8`, uses the same `esi`/`edi`/`ebp` frame, and
   terminates with `jmp 0x41e6e6` at `0x0041E841`; `mov edi,edi` padding at
   `0x0041E846` then precedes the dispatch table. The extent is
   `0x0041DC60`-`0x0041E845`. This was asserted at eleven sites including a
   dossier marked `status: confirmed, confidence: high`, and — worst — the
   coverage map had turned it into a general method rule whose own worked
   example was wrong.
2. **The `+0x70` writer enumeration is incomplete.** §5.1 claimed three writers
   and §0.1 claimed to record "every `+0x70` writer". There are **four**:
   `0x0041E7FE` writes `+2` (`add eax,0x2` at `0x0041E7FB`) when the mode local
   exceeds 2 (`cmp ecx,0x3 / jl 0x41e801` at `0x0041E7EC`-`0x0041E7F2`, `ecx`
   from `[esp+0x4c]` at `0x0041E6C6`) — i.e. pending opcode 20 or 6. Like the
   others it zeroes `+0x60`. The previous draft's sweep stopped at the wrong
   extent, so defect 1 caused defect 2.
3. **§2.2.1's flag table is incomplete over its own declared scope.** Bit
   `0x0020` is also tested at `0x0041BD6C` (`test bl,dl` on
   `mov dl,[eax+0x5c]` at `0x0041BD69`, with `bl = 0x20` set at `0x0041BD17`
   and unmodified until `0x0041BE61`) inside `0x0041BD10` — one of the five
   named functions. That test gates the `+0x62 = 0x63` / unshifted-position
   block §2.1 itself discusses. Thirteen sites, not twelve.
4. **§0's prior-art list is wrong in both directions.** It named
   `M2-generic-resource-index-producer-census.md`, which contains **zero**
   occurrences of `0x0059B628`, and omitted
   `M2-second-deferral-hard-truth-audit.md`, which contains three and already
   publishes §1.1's headline arithmetic verbatim — "The 64-record pool is
   `[0x0059B628,0x0059D728)` with stride `0x84`" and
   `0x0059B628 + 63 * 0x84 = 0x0059D6A4` — plus `+0x5C` as a flags field via
   `0x00431804` testing slot 25's flags at `0x0059C368`. For a section whose
   entire purpose is prior-art accounting, and which advertised that two
   audits had already widened it, a wrong membership list is gating.
5. **§0's "no earlier export mentions …" is false for `ghidra-evidence.json`.**
   That 8 MB generated artifact sits in the same directory, was committed at
   the project's earliest baseline, and is cited as evidence by many Vault
   notes. It contains `{"from":"0041dcf9","to":"0041e848","type":"DATA"}`, the
   symbols `PTR_DAT_004c83f0` and `PTR_DAT_004c8758`, and a decompilation of
   `FUN_0041dc60` that already renders the 26-way opcode switch, the nine-way
   opcode-11 sub-switch with all nine targets, `&DAT_004c8754 + operand * 4`,
   the `0x005C5860` indexing, the call through record `+0x7C`, and both extra
   program-counter advances. The accompanying claim that the two exports
   naming `0x0041DC60` treat it "only as a function that forwards a pointer"
   is likewise false as scoped.
6. **A fourth silently truncated disassembly block.** §1.4's block omits
   `0x0041C47D: eb 08  jmp 0x41c487` with no elision marker. As in the three
   previous instances, the dropped instruction is the one that makes the prose
   true — it is what makes the two `0x00599CA8` stores mutually exclusive,
   which is exactly what §3.3 asserts.
7. **Stale cross-artifact statement.** `EXP-20260816-172`'s audit-history
   section still read "Rejected **once**" at a HEAD whose own commit message
   says "after **second** rejection". `EXP-20260817-174`'s "No numeric drift
   was found across any artifact" missed it.

## Minor findings, all applied

§5.2 said the condition slot is written by opcodes 4, 14, 16 and 24, omitting
opcode 11 operand 5, whose callee return value is stored at `0x0041DFA2` — as
§5.4 of the same export says. §2.2.1's "One pool access outside them" reads
exclusive: at least eight further sites reach pool `+0x5C` through the
absolute address `0x0059B684`. §1.4's stated range excluded the `0x0041C47F`
line its own block quotes. §5.3's "pending opcode at the saved PC" is
imprecise — `0x0041E14F` reads at the just-persisted PC. §1.4 stated the
`0x005C5860` table "is 64 entries" where the evidence is a 64-dword clear
width, which bounds the zeroed region rather than the table, and
`M2-plant-request-origin-static-trace.md` had already recorded that clear.
Opcode 15 stores `(operand >> 4) & 0xFF`. One half-open/closed range notation
inconsistency.

## What survived

Everything numeric, for the third time, plus every correction from both prior
audits: the pool extent from both loop terminations and the three index sites;
§1.2 byte-exact including the restored `0x00465763`; the `CreatListRam` string
and its site; builder, update and interpreter reachability under rel32 plus
whole-file absolute scans; §1.3's nine builder steps; all four `KU-069`
indexes; §3.1's nineteen rows and four-outcome partition; §3.2's eleven
non-default types; §3.3 over 48 entries; §4's 28 pointers, trailing-byte
histogram and three special values; the full instruction-size map and the
stall-breaker derivation; the 40 programs, their extent, decode totals,
histogram and both example listings; the external entry point; §5.3's mode
dispatch and the mode slot `[esp+0x4c]`; §5.4's nine subroutines; that
`call eax` at `0x0041E7C7` is the **only** register-indirect call in the five
functions and no other outbound edge lands in the handler range; §7's formulas;
§8's `0x3E6` gate; `0x004C7970` occurring zero times; exactly five `EVENT`
strings; and §2.2's tail-field note. Every file offset recomputed correct.

The auditor also verified that the packet genuinely claims nothing about the
per-type handlers, the opcode-11 subroutines or the five modes, rather than
implying something it has not established.

## Scope answers

- **Bounded remains correct for Enemies/actors/AI**, on the map's own
  definition; every row anchor reproduced.
- **Touched remains correct for Event/scripting**: exactly five `EVENT` strings
  in the whole file, all at the cited addresses, one push site, no event code
  read.
- **The §0 novelty boundary was still not honest** — see defects 4 and 5. It is
  now rewritten to account for nine artifacts including the generated export,
  and the address-based novelty framing is **withdrawn**.
- **`EXP-20260816-173` describes its audit accurately**, and its appended
  corrections section is right on both points.
  **`EXP-20260817-174` is accurate on everything it found**, but inherited the
  wrong extent, therefore missed `0x0041E7FE`, and its no-drift statement
  missed one stale line. Both are corrected in that note.

## Limitations of this audit

What the interpreter region past `0x0041E1A8` computes, the ten per-type
`+0x7C` handlers, the nine opcode-11 subroutines and the five modes were not
analysed. Caller checks remain rel32 plus whole-file absolute scans, which
miss computed dispatch by construction. `+0x5C` accesses outside the five named
functions were sampled, not enumerated image-wide. The cross-referenced
results `EXP-20260815-128`, `EXP-20260816-165`, `EXP-20260816-153` and
`KU-064` were not themselves re-verified. No level file was parsed and nothing
was run.

## Hygiene

`make vault-lint` 492 notes / 0 errors / 0 warnings; `make audit-tracked` 0
violations; `make test` **686 passed**, single invocation, denominator 686,
qualified by the open `KU-065` (three prior independent recurrences of the same
`anchor_timeout` / `NextLife.` node). A passing run does not close `KU-065` and
cannot be cited as an unqualified gate.

## Correction

All findings are applied in the commit that records this audit — to the export,
`EXP-20260816-172`, `EXP-20260817-174`, the interpreter dossier, `KU-069`, the
coverage map, the Subsystems MOC, the Experiments MOC and Current State. No
derived number changed, because none was wrong. A fourth fresh audit follows.

## Corrections to this audit

[[EXP-20260817-176 - Fourth independent creature census audit]] found two
errors in this note, both propagated into the correction it drove:

- **"Thirteen sites, not twelve"** (defect 3) is unreproducible. The flag table
  distinguishes twelve bits, carried by **21 distinct instructions** touching
  `+0x5C`/`+0x5D` across the five named functions. No reading of the table or
  the binary yields thirteen. The bit-`0x20` test at `0x0041BD6C` that this
  audit found is real; only the aggregate count was wrong.
- **"both extra program-counter advances"** understates `ghidra-evidence.json`.
  Its decompilation of `FUN_0041dc60` renders **three** — including
  `if (2 < param_3) { … piVar8[0x1c] = piVar8[0x1c] + 2; }`, which is exactly
  the `0x0041E7FE` writer this audit presented as its own discovery. The
  generated artifact already contained it, guard and all.

The extent correction (`0x0041DC60`-`0x0041E845`), the missed writer, the
bit-`0x20` site, the prior-art membership findings and the withdrawal of the
address-based novelty claim all stand and were independently re-verified.
