---
type: session
date: 2026-08-17
agent: Claude
status: worker-complete
tags:
  - session
  - research/coverage
  - re/input
---

# PC input subsystem census

## Agent

Claude.

## Goal

Open the Input row of [[Subsystem Coverage Map]], the second in the recorded
Actors/AI → Input → Event/scripting preference.

## Files inspected

`Vault/00-System/` startup notes; the coverage map and the audio census's
method note; every file in `static/exports/BIN-97c95ba5572dce63/` including
`ghidra-evidence.json`, grepped for each principal address before any analysis;
[[PC autonomous game control]] and `EXP-20260816-145` for the chooser;
`work/copies/BUGS_PC-full-disc/bugs.exe`, re-hashed to
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.

## Experiments inspected

`EXP-20260816-159` (the Input anchor and the method note),
`EXP-20260816-145` (the chooser).

## Changes made

New export `SUBSYS-input-static-census.md`; new experiment note
[[EXP-20260817-181 - PC input subsystem static census]]; new dossiers
`FUNC-97C95BA5572D-0042F350` and `-0042EBC0`; Input row Touched → Bounded;
`KU-070`; entries in the three MOCs, [[Current State]] and this index.

No script, parser, test or reimplementation module changed. No game asset,
`originals/` path or PS1 source touched.

## Conclusions

The devices are a `GUID_SysKeyboard` keyboard at `c_dfDIKeyboard`
(non-exclusive foreground) and enumerated joysticks promoted to
`IID_IDirectInputDevice2A` at `c_dfDIJoystick` (exclusive foreground). Per-frame
state is read at `0x0042EBC0` into `0x00598A10` and `0x00598B60` and reduced to
action bits at `0x00598B10` through a runtime-written twelve-entry table, plus
a four-direction analog synthesis.

Two findings generalise: the binding table is written at runtime from two call
sites, and `GetAsyncKeyState` is reached only by a register load — its import
thunk is dead.

## New hypotheses

None. The joystick button-index reading in §4 of the export is marked Inferred.

## Contradictions discovered

None. Every cross-check agreed: the `0x0059F73C` window handle matches the
audio census's, the data-format `dwDataSize` values match the buffer sizes the
consumers pass, and `Poll` at `+0x64` matches the interface the bring-up
queried for.

## Tests run

No repository test suite is affected — this packet changed no code. Method
checks: two GUIDs and two `DIDATAFORMAT` structures decoded from raw bytes and
compared against documented values; both function extents established from
their `ret` and padding before any claim was scoped to them; the direction
jump table and byte table decoded and cross-checked against the mask values;
`esi` verified not reloaded between the `GetAsyncKeyState` load and its eight
call sites.

Two claims failed verification during drafting and were corrected before
commit: "`0x004016AE`'s only call site" (there are two) and the lowest
`.bss`-class address cited (`0x004F0440`, not `0x005987D0`).

## Unresolved questions

`KU-070`; the enumeration callback `0x00401979`; `0x005988E0`; the enclosing
functions of the two per-frame call sites; the extents of `0x0042F600` and
`0x0042F680`.

## Recommended next action

A **fresh James audit** of this packet. Attack surface worth pointing at: the
identifier decodings (everything rests on them), both extent statements, the
twelve-entry table arithmetic, the dead-thunk completeness claim, and the §0
prior-art boundary against every export including the generated one.

## Git commit if applicable

One intentional commit; tree clean.
