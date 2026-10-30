---
type: experiment
id: EXP-20260816-160
date: 2026-08-16
question: 'Does independent review support the audio census claims - the bring-up anchors, the track table, the counts, the DSStream reading, the input split, and the Bounded row status?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline audit; radare2; no runtime, debugger, or target write
environment_version: Python 3.14.6
working_directory: /home/dev/ABLPC
configuration: audit at clean HEAD 00c5ae5; read-only toward game media and originals; nothing committed or modified
artifacts:
  - static/exports/BIN-97c95ba5572dce63/SUBSYS-audio-static-census.md
addresses:
  - "0x004A3480"
  - "0x0042B020"
  - "0x0042B747"
  - "0x0042B781"
  - "0x0042C130"
  - "0x0042C3B0"
  - "0x004D81E8"
file_offsets: []
result: reject-six-claims-corrected-anchors-and-bounded-row-survive
created: 2026-08-16T22:15:00
updated: 2026-08-16T22:15:00
tags:
  - re/experiment
  - re/audit
  - re/audio
  - research/coverage
---

# EXP-20260816-160 - Independent audio census audit

## Verdict

**REJECT** at `00c5ae5`. The census's core anchors are real and most of its
numbers reproduce exactly, but six Confirmed-level claims were wrong or
unreproducible, and an indirect-dispatch attack found a material completeness
miss. The row-level judgement survives: audio stays **Bounded** after the
corrections, and no runtime session is required to fix any of it.

## What survived independent re-derivation

Imports and IATs exactly as tabled; the three import jump thunks at
`0x004AFEA8`/`AE`/`B4`; zero `FF 15` sites to any of them. The bring-up at
`0x004A3480` re-disassembled in full — both `0x300`-dword clears, the
callback thunk to `0x0049DD00`, the GUID pointer, the object out-pointer, the
`[vtbl+0x18]` call with `([0x0059F73C], 1)`, and `[0x007ECA40] = 1` strictly
inside the `je`-guarded success block. Its resolved callers are exactly
`0x00412CAB`, `0x00412DE5`, `0x0042BAD0`, none direct. The track-table portion of this audit was itself incomplete: it missed
register-based stores and therefore omitted DEAD and LESS13. Correction
[[EXP-20260909-005 - PC Mr Soil dialogue mechanism]] establishes **40 populated
track slots** at stride8 `0x00596528`, indices0..39, with null index40 and
zero second dwords. DEAD occupies15/16/22/23; LESS13 occupies37/38/39. The
disc holds35 WAV files. This correction preserves the old audit failure
rather than retroactively claiming it verified those stores. All
per-import `mmio` counts, the top-three call-site counts 34/23/19, and
`0x0042BB90`'s three callers. Both function dossiers were judged disciplined:
`candidate_` names, the vtable reading kept Inferred, music kept Inferred.

## Defects

1. **`38` `mmio` call sites is `37`.** The census's own per-import table sums
   to 37; only the headline was wrong.
2. **`Seventeen` thunk-reachable module functions is `12`.** The census
   counted ordinary `jmp` instructions *inside* module functions as
   thunk-table entries. Only `E9` entries within `0x00401000`-`0x00402000` are
   thunks.
3. **"Every caller being outside the module" is false.** `0x0042B020` has two
   in-module call sites, `0x0042B747` and `0x0042B781`. The census's own
   tooling printed "32 from outside" of 34 and the prose contradicted it.
4. **`0x0042C29F` is not a function start.** It is a `je` target inside a
   byte-scan loop; the containing function begins at `0x0042C130` — the same
   DSStream token parser `EXP-20260816-143` already recorded, which the census
   listed separately.
5. **"A DSStream window class is registered" is not what the site shows.**
   `DSStreamWndClass` has exactly one reference in the image: the `push` at
   `0x0042C3B0` feeding **`UnregisterClassA`**, a cleanup site. Registration
   may exist behind a structure field, but the Confirmed bullet asserted
   something not seen.
6. **"Music track table" under Confirmed contradicted the note's own
   Inferred section**, which states that no instruction distinguishes music
   from effects. The label had propagated to the census heading, Current
   State, and the roadmap; the function dossier had it right.
7. **Missed indirect dispatch.** A `.data` record at `0x004D81E8` holds a
   count of 3 and three thunk pointers (`0x00401B04`, `0x004011D1`,
   `0x00401299` — to `0x0042BA60`, `0x0042BB30`, `0x0042BB50`) followed by the
   string `"DIRECTX"`. `0x0042BA60` has **zero** direct call sites, so under
   the census's own method its central initializer was unreachable — a gap the
   census disclosed as unscanned but whose consequences it did not follow.

Minor: some sites were cited at operand rather than instruction addresses
(`0x0042C3B1`, `0x0042BA1F`, `0x0042BABF` for `0x0042C3B0`, `0x0042BA1E`,
`0x0042BABE`); the globals table omitted the single dword cleared at
`0x004A3493` (`0x007EDDF8`).

## Scope answers

- **The input split is warranted.** Both call sites verified: `0x0042BAD0` to
  the DirectSound bring-up thunk and `0x0042BAED` to `0x00401582` ->
  `0x0042F350`, whose `0x0042F43D` is the sole `DirectInputCreateA` site. The
  `"DIRECTX"` record naming that initializer family strengthens it further.
- **Bounded is right, not Touched.** Deliberate cited anchors with a
  documented static-only boundary exceed "incidental observations". The
  auditor declined the offer to downgrade, requiring only that the row's
  anchors lose `0x0042C29F`.

## Limitations of the audit

Full dataflow for register-indirect calls (`FF D0`-family) was not attempted;
the indirect scan covered absolute materialisation of module and thunk
addresses, which found the `"DIRECTX"` record but cannot rule out computed
dispatch. `0x0042B020`, `0x0042C0D0` and `0x0042C110` remain unidentified, as
the census itself records. No runtime claims were checked because none are
made.

## Correction

All seven items are applied in the same commit that records this audit. One
further minor item the auditor offered — a logical index bound read from a
`cmp` in the builder — was **dropped rather than recorded**, because the
disassembly at that address could not be cleanly reproduced during the
correction, and this project does not bank numbers that do not reproduce.
