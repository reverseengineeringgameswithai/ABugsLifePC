---
type: experiment
id: EXP-20261001-002
date: 2026-10-01
question: "Which animations does Flik's PC player model have, and which native action state plays each?"
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: static analysis (Fedora; GNU objdump 2.44; Ghidra baseline export)
environment_version: GNU objdump 2.44; Python 3.14 with pefile; Ghidra baseline export (search surface only)
working_directory: /home/dev/ABLPC
configuration: Read-only static analysis of work/copies/BUGS_PC-full-disc; no runtime launch, no memory access, no game-file edits
artifacts:
  - config/animation/pc-flik-animations.json
  - reports/animation/flik-animation-catalog.json
  - reports/animation/flik-animation-catalog.md
  - scripts/flik-animation-catalog.py
  - reimplementation/ablpc/flik_animation.py
  - tests/test_flik_animation.py
addresses:
  - 0x00402DC0
  - 0x00445FF0
  - 0x00444B70
  - 0x00445020
  - 0x004C1CE8
  - 0x004C1FA8
  - 0x0043F9E0
  - 0x0042F100
file_offsets:
  - CHARS/FLICK.ANM 0x8 (40-slot offset table)
  - CHARS/FLICK.ANM 0xA8 (slot 3, first record)
result: static-catalogue-complete-for-player-model
created: 2026-10-01T18:01:13-04:00
updated: 2026-10-01T18:01:13-04:00
tags:
  - re/experiment
---

# EXP-20261001-002 - Flik animation catalog

## Question

Which animations does Flik's PC player model have, and which native action
state plays each?

## Inputs

- Retail executable SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
  (`work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe`).
- `CHARS/FLICK.ANM` `1743b26a…e8ab1` (= `CHARS3/FLICKD.ANM`),
  and:
  - `CHARS3/FLICKP.ANM` `95e77803dfaef08b616eaed738e3edc183c0de3336f7da6473bb69ad3c0ed3b7`
  - `CHARS4/FLICKP.ANM` `85ecebab2dc71bb8b6ae23b728ed8f855775dd6cf4ff1ef9be1b3b5a2e6e3fe9`
  - `CHARS3/FLIKHARV.ANM` `5442b76ff7b0911fed6f79b40390b3f7e83a04b2bcb1d5730fad86d581557f48`
  - `CHARS2/ATTAFLIK.ANM` `267ba06ac8fbb88aecfe978795e65e2daa0f99b3cac86db46b06b7da4ccefc2d`
- All 61 retail `.ANM` files for the multi-file check.
- No PS1 source, runtime, memory access or edit was used.

## Procedure

1. Walked FLICK.ANM's first-level table with the existing inspector, then
   read slot records under the hypothesis frames × words-per-frame.
2. Found the record consumer: pose sampler `0x00445FF0`. Confirmed its reads
   with fresh `objdump -d` (`0x00446025`, `0x0044607E`–`0x004460F1`).
3. Validated the record grammar on every retail `.ANM`.
4. Traced the sampler's four call sites and Flik's caller `0x00402DC0`; dumped
   its 35-row state table, frame scripts and idle tables from the executable
   bytes and confirmed the indexing instructions (`0x00403181`–`0x004033D9`).
5. Named each state's trigger from every writer of `0x0059D998` (census of
   immediate and register stores) and the controller's input, timer and carry
   logic, with default key bindings from `0x0042F100`. Three parallel static
   traces; load-bearing claims were rechecked in disassembly (speed cap
   `0x0043FC19`, throw counter `0x00440541`/`0x00440555`, key table).
6. Compared the player-model variants slot for slot and parsed the two
   non-player Flik models.
7. Implemented `AnmFile.records()`, `flik_animation.py`, the label file and
   the generator, with synthetic tests and a retail-gated test.

## Observed

- **Record grammar.** `+0x02` frames (`& 0x7FFF`), `+0x04` parts, `+0x06`
  words per frame, `+0x08` list count, `+0x0A` bitmask length, part list,
  bitmask, frames. With the bitmask length respected, **303 records in 60 of
  61 files end with zero slack**; every `+0x00` equals its slot.
  `LEVEL00/ROSIEWLK.ANM` is the exception (first offset beyond its file).
- **FLICK.ANM.** 40 slots, slot 26 absent; 24 parts (21 driven, 3 `-2`);
  frame counts 8–58; words per frame 129/126 (full body), 72 (parts 9–20) and
  57 (parts 0–8). Five slots are half-body layers.
- **State table.** 35 rows at `0x004C1CE8`, a `0xFFFFFFFF` word at
  `0x004C1FA4`, idle tables at `0x004C1FA8/B8/C8`. Every script frame lies
  within its slots. State `0x20` names absent slot 26 and no store writes
  `0x20`.
- **Coverage.** Sampler call sites: `0x004032FE`, `0x004033D9` (Flik),
  `0x00448569` (entity types), `0x0044CE05` (plants). Slots 7 and 12 have no
  reference. Berry-throw overlays use slots 2, 11 and 23; the strand swing
  uses slot 32 through header `+0x88`.
- **Variants.** FLICKD is identical; both FLICKP files have 29 parts and the
  same frame count in every present slot; CHARS4/FLICKP also lacks slots 30,
  31 and 37, exactly the fidgets its levels' idle table never picks.
- **Non-player models.** ATTAFLIK (actor slot 39, Riverbed Flight only) is
  drawn instead of Flik: `0x004362D0` copies his position and sets
  `0x0059D9A0` bit 0 (`0x0043634A`), which Flik's renderer tests at
  `0x0044C51A`; its slots are a flight loop, hurt, berry throw and death.
  FLIKHARV (actor slot 63, hook `0x00415E30`) is the rideable harvester:
  ridden moving, ridden standing, parked (`0x00416038`, `0x00416014`).
- **Triggers.** As tabulated in [[PC Flik animation catalog]] and
  `config/animation/pc-flik-animations.json`, each with addresses.

## Interpretation

The catalogue is complete for the player model at the slot and state level:
the only paths that sample Flik's file are enumerated, and every reachable
slot is labelled. Twenty-eight state names are confirmed by the code that
sets them; seven carry `candidate` names (states 1, 2, 6, 7, `0x10`, `0x1C`
and `0x1F`). One contradiction is recorded (movement state 4,
gliding versus hover-dive-pound).

## Result

Static catalogue complete for the player model and both non-player Flik
models. `tests/test_anm.py` (26) and `tests/test_flik_animation.py` (13) pass; the
generator's `--check` reproduces the committed reports.

## Follow-up

- A read-only runtime arm on the state word (see [[Known Unknowns#Flik animations]]).
- `.ALL` hierarchy decoding for visual previews and part names.
