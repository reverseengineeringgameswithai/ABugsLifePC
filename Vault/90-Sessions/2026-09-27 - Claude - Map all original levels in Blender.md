---
type: session
date: 2026-09-27
agent: Claude
status: complete
tags:
  - session
---

# Map all original levels in Blender

## Agent

Claude (Opus 5.5) in Claude Code.

## Goal

User request: "i believe we are able to map out levels as we did with Training.
Could you work on the rest of the OG levels and save them as Blender files?
Make sure you get all the objects."

## Files inspected

START HERE, Current State, Environment Status, [[PC original Training Blender mapping]],
[[PC level roster and numbering]], [[PC Anthill remaining object inventory]],
[[FUNC-97C95BA5572D-004498F0]], [[FUNC-97C95BA5572D-0041BD10]], the Training/Cliffside
importers and population scripts, and Ghidra exports for `004671D0`, `004498F0`,
`00453FF0`, `00454B70`, `0044F8E0`, `00417720`, `0041C420`, `0043E6B0`.

## Experiments inspected

[[EXP-20260909-012 - Original Training Blender mapping]], [[EXP-20260909-013 - Populate original Training Blender map]],
EXP-20260914-010, [[EXP-20260926-001 - Static Anthill remaining object inventory]].

## Changes made

- New `reimplementation/ablpc/original_levels.py`: engine→file rule, pinned
  hashes, all drawn dispatches, sprite batches, undispatched rows, creature rows
  and models, normal-table metadata, 128-pixel pages, spawn table.
- New `scripts/map-original-levels.py` and `tools/blender/original_level_map.py`.
- `tools/blender/original_map.py`: the sidebar lists a map's declared layers
  (`pc_map_layers`); Training maps without it behave as before.
- New `tests/test_original_levels.py` (16 tests).
- Sixteen private maps under `work/level-projects/original-levels/`; metadata in
  `reports/original-levels/EXP-20260927-001.json`.
- Vault: [[EXP-20260927-001 - Complete original level Blender maps]],
  [[PC original level Blender maps]], roster file rule, Current State, Known
  Unknowns, Decision Log, MOCs.

## Conclusions

All 9,673 scene records of engines 1..16 are drawn or kept (one undispatched
0x83 row), with 936 pickups, 525 creature slots and every level's Flik start.
The generalized path reproduces the Training and Cliffside counts.

## New hypotheses

Model tails are per-corner normal tables (structural fit across the corpus).

## Contradictions discovered

A first draft drew those tails as geometry, creating giant white hexagons around
seeds; the corpus check replaced that reading before delivery. A sky-down floor
query had placed interior grains "under" roofs; own-position queries and a
clipped close-up show the literal grain Y is consistent.

## Tests run

- `tests/test_original_levels.py` (16), `tests/test_original_level.py` and
  `tests/test_original_population.py`: 73 passed together.
- All 16 Blender builds: save, reopen and full object/vertex/placement checks pass.
- `make check`: python-doctor, Vault lint (0 errors, 0 warnings after the START HERE
  update), M4 compatibility, tracked-file audit (0 violations) and `git diff --check`
  pass. The full suite (7,426 tests) was **not** a clean pass:
  - First 4,713 tests: 12 failures, all in `tests/test_r2q_quiet_census_design.py`
    (`executed-source drifted`; pre-existing, see [[Known Unknowns#Current regression-gate failure]]).
    The user reports R2q was recently dropped for taking too long, so this gate may be outdated.
    The previously listed `test_r2p_p0e_y_restore` failure passed in this run.
  - The background run finished after 3 h 24 min: 203 failed, 371 errors. R2q tests
    left about 49 GB in `/tmp/pytest-of-dev` (RAM-backed tmpfs), and later tests hit
    `Disk quota exceeded`. All 485 non-R2q failures were in files that passed in the
    separate run below. This session's pytest temporary folders were then removed,
    and `/tmp` returned to 1.2 GB used.
  - The other 79 files (2,301 tests), run separately: 2,300 passed, 1 failed.
    `tests/test_repo_hygiene.py::test_agents_and_claude_instructions_are_identical` fails at
    HEAD: `AGENTS.md` has had a paragraph that `CLAUDE.md` lacks since `0376cad`.
    Neither file was changed in this session.

## Unresolved questions

See [[Known Unknowns#Original level maps]].

## Recommended next action

User review of the maps in Blender. Optionally name creature types by a live
observation of one spawn per type.

## Git commit if applicable

Not committed; the user did not request a commit.
