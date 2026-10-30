---
type: session
date: 2026-10-01
agent: Claude
status: complete
tags:
  - session
---

# Map Flik's animations

## Agent

Claude (Opus 5.5) in Claude Code, a fresh session after `/clear`.

## Goal

"Please map out all of the animations that Flik has and store it in a way where
we can reference it later. I'll let you take control." Mid-task the user asked
"is this an exhaustive animations export of Flik"; the answer (below) separates
the complete static map from a keyframe or visual export.

## Files inspected

- START HERE, Current State, Environment Status, Project Charter, Cross-Port
  Evidence Policy (no PS1 source was consulted), [[Ghidra export structure and caveats]];
- [[PC ANM first-level]], [[PC ANM inspector]], [[EXP-20260812-033 - Character ALL replacement visible outcome]],
  [[EXP-20260812-034 - Character request and first consumer trace]],
  [[FUNC-97C95BA5572D-00402DC0]], [[FUNC-97C95BA5572D-00445FF0]],
  EXP-20260930-004, [[PC level roster and numbering]];
- decompiler and fresh `objdump -d` of `00402DC0`, `00445FF0`, `00444B70`,
  `00445020`, `00448010`, `0043ED60`, `0043F9E0`, `0041C9B0`, `00434620`,
  `00436B40`, `00439E90`, `00468010`, `00468BF0`, the key reader `0042EC31`
  and defaults `0042F100`;
- every retail `.ANM` in `work/copies/BUGS_PC-full-disc` (read only).

Three parallel static traces (input bits and modes; carry, hazards and death;
model variants and sampler users) and a fourth (non-player Flik models)
reported back; their load-bearing claims were rechecked in disassembly.

## Changes made

- `reimplementation/ablpc/anm.py`: `AnmRecord` and `AnmFile.records()`,
  bounds-checked slot records as read by `00445FF0`; the first-level API is
  unchanged.
- `reimplementation/ablpc/flik_animation.py`: retail-hash-locked state-table,
  script and idle-table reader; variant and non-player model comparison;
  label validation against the binary.
- `config/animation/pc-flik-animations.json`: authored labels with status and
  evidence per state, slot and non-player slot.
- `scripts/flik-animation-catalog.py` and
  `reports/animation/flik-animation-catalog.{json,md}` (metadata only).
- `tests/test_anm.py` (+10 synthetic record tests) and
  `tests/test_flik_animation.py`.
- Vault: [[PC Flik animation catalog]], [[EXP-20261001-002 - Flik animation catalog]],
  the ANM format and two function dossiers, Known Unknowns, Decision Log,
  Current State and MOCs.

## Evidence

- Record grammar: sampler disassembly and 303 records in 60 of 61 retail files
  with zero slack.
- State table: retail bytes at `004C1CE8` and the indexing instructions.
- Coverage: the four sampler call sites; no reference to slots 7 or 12; no
  store of `0x20` to the state word.

## Validation

- `tests/test_anm.py` and `tests/test_flik_animation.py`: 39 passed.
- Every test importing the ANM parser, CLI or new module (7 files): 395 passed.
- `make python-doctor vault-lint m4-compatibility audit-tracked`: pass.
- `scripts/flik-animation-catalog.py --check`: current.
- The full suite was not rerun (about 50 minutes, with pre-existing
  unidentified failures recorded on 2026-09-30); this change adds modules and
  tests and alters no existing behaviour.

## Runtime

None. No launch, no memory access, no game-file edit. The larger-save
production in [[Environment Status#Current runtime handoff]] was left open and
untouched.

## Answer to "is this exhaustive?"

For the player model, yes at the slot and state level: every way the
executable plays Flik's file is enumerated and every reachable slot is
labelled. Two non-player models are also covered: the FLIKHARV harvester and
ATTAFLIK, which replaces Flik on screen in Riverbed Flight. It is a map, not a
keyframe or visual export: pose data stays out of Git, and drawing poses needs
the undecoded `.ALL` part hierarchy.

## Next

A read-only runtime arm on `0x0059D998`/`0x0059D996`, which also settles the
movement-state-4 contradiction; then `.ALL` hierarchy decoding for previews.
