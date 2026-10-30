---
type: session
date: 2026-08-16
agent: Claude
status: worker-complete
tags:
  - session
  - research/coverage
  - re/actors
---

# Creature actor pool and behaviour VM census

## Agent

Claude.

## Goal

Run the next bounded packet under the recorded coverage preference
Actors/AI → Input → Event/scripting, following the startup sequence in
[[START HERE]], and leave the Vault and the git tree clean for a fresh James
audit.

## Files inspected

- `Vault/00-System/START HERE.md`, `Current State.md`, `Project Roadmap.md`,
  `Environment Status.md`, `Agent Operating Manual.md`
- `Vault/01-MOCs/Subsystem Coverage Map.md`, `Subsystems MOC.md`,
  `Functions MOC.md`
- `Vault/70-Known-Unknowns/Known Unknowns.md`
- `static/exports/BIN-97c95ba5572dce63/`: `SUBSYS-audio-static-census.md` (as
  the method model), `M2-fixed-pool-index-producer-census.md`,
  `M2-generic-resource-index-producer-census.md`,
  `M2-signed-selector-producer-provenance.md`
- `work/copies/BUGS_PC-full-disc/bugs.exe`, re-hashed to
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- One metadata-level listing of `work/copies/BUGS_PC-full-disc/PC/BUGS/CD`

## Experiments inspected

`EXP-20260816-159`/`160` for the coverage-packet method,
`EXP-20260816-164`/`165` for the accepted camera common block,
`EXP-20260815-128` for the live Flik position globals, and
`EXP-20260816-153` for the `<< 5` world-coordinate convention.

## Changes made

- New evidence export
  `static/exports/BIN-97c95ba5572dce63/SUBSYS-creature-actor-static-census.md`.
- New experiment note
  [[EXP-20260816-172 - PC creature actor pool and behaviour VM census]].
- New function dossiers `FUNC-97C95BA5572D-0041DC60` and
  `FUNC-97C95BA5572D-0041EC40`; dated additions to `-0041C420`, `-0041BD10`
  and `-0041B9F0`.
- [[Subsystem Coverage Map]]: Enemies/actors/AI Untouched → **Bounded**;
  Event/scripting Untouched → **Touched**; three new method notes.
- [[Subsystems MOC]] and [[Functions MOC]]: new sections for the pool.
- [[Project Roadmap]] coverage-reconnaissance list and [[Current State]]:
  new entries.
- [[Known Unknowns]]: `KU-068` and `KU-069`.

No script, parser, test or reimplementation module was added or changed. No
game asset, `originals/` path or PS1 source was touched.

## Conclusions

The row's open question is answered as both halves. The pool is the 64-slot
array at `[0x0059B628, 0x0059D728)`, stride `0x84`, bound one-to-one to 64
`0x1C`-byte records the loader copies to `0x00599EB0` on record type `0x23`.
Behind it is a program list — 40 word-code programs at
`[0x004C7D00, 0x004C83F0)`, selected per instance by source byte `+0x0D` — run
by a resumable interpreter at `0x0041DC60` in which seven of the eight no-body
opcodes double as a five-mode state machine.

The naming came from the executable, not from interpretation: the loader logs
`LOAD: Type 35, CreatListRam.` directly after filling the table.

## New hypotheses

That the shared `rand.dat` cursor at `0x00599C60` — referenced 380 times, of
which 197 write a computed value back —
is a candidate explanation for `EXP-20260815-125`'s divergent gameplay under
exact input delivery. Nothing in this packet measures that, and it should not
be cited as evidence until something does.

## Contradictions discovered

None. Every cross-check agreed: the pool extent matches the M2 census reached
from the resource-index direction, the caller chain matches
`M2-generic-resource-index-producer-census.md`, the `0x00467E60` edge matches
`M2-signed-selector-producer-provenance.md`, and opcode 16's operands are the
Flik globals `EXP-20260815-128` established at runtime.

## Tests run

This packet changed no code, so the suite is a regression check only. `make
vault-lint` reports 488 notes, 0 errors, 0 warnings; `make audit-tracked`
reports 0 violations; `make test` is **686 passed**, qualified by the open
`KU-065` as every suite observation must be.

The instruction-size model was validated instead by four independent
structural checks over the shipped data, all of which pass with zero
exceptions:

- the 40 script bodies are contiguous and the last ends exactly at its own
  pointer table's first byte;
- a linear decode of all 40 gives 463 instructions with zero misalignment;
- all 69 branch and jump targets land on instruction boundaries;
- `[0x004C8474] + 0x1A`, written into a slot's `+0x70` by unrelated code at
  `0x004372A8`, lands on a decoded instruction boundary in script 33.

The reproduction snippet for the first three is in the export, §6.1.

## Unresolved questions

`KU-068` (no runtime fact is claimed; which levels even build the pool),
`KU-069` (unbounded type-byte index), the five interpreter modes, the ten
per-type `+0x7C` handlers, the nine opcode-11 subroutines, and every per-type
creature identity.

## Recommended next action

A **fresh James audit** of this packet, per the recorded preference that each
bounded packet gets one. Attack surface worth pointing at: the instruction-size
table (everything else rests on it), the claim that the 6..41 domain is shared
by both switches, the `KU-069` arithmetic, and the honesty of the novelty
boundary in §0 of the export against the three M2 exports it cites (that
count was itself wrong — there are eight; see the Outcome note below).

**Outcome:** that audit ran and returned **REJECT** —
[[EXP-20260816-173 - Independent creature census audit]]. Every one of those
four nominated surfaces held; the defects were elsewhere, in the Confirmed
register, one miscount, one propagated figure, and the attribution in §0. A
second fresh audit,
[[EXP-20260817-174 - Second independent creature census audit]], then rejected
the corrected packet too: this session had read about 44% of `0x0041DC60` while
making claims scoped to all of it, and the novelty claim it nominated for
attack was itself prior art in an export this session never found. All
findings from both audits are applied.

After that, the preference order continues with **Input**, whose row already
has `0x0042F350` and the single `DirectInputCreateA` site from
`EXP-20260816-159` — an import-anchored row, so cheap by the audio census's
own method note.

## Git commit if applicable

One intentional commit; the tree is clean and `work/` scratch was not added.
