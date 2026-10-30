---
type: session
date: 2026-08-18
agent: Claude
status: complete
tags:
  - session
  - research/cross-port
  - re/static
---

# Replay-seeded berry-type static candidate

## Agent

Claude.

## Goal

User-directed test of the DuckStation→PC translation loop assessed in
[[2026-08-18 1318 - Claude - PS1 replay translation assessment]]: pick one
short interpreter-recorded PS1 input movie from
`movies/Phase4/Interpreter/`, replay it instrumented in the external
DuckStation fork, and see whether the observation drives a purely static PC
investigation. Target chosen: `Hopper_white_berry_death.movie.json`
(642 frames, state-anchored), aimed at open `KU-073` (PC berry-type variable).

## What was done

- Launched one **isolated** DuckStation instance (external fork, own config
  root in the session scratchpad, `ExecutionMode=Interpreter` pinned and
  verified, audio muted, debugger API on a private localhost port). The
  external repositories (`SRC-PS1-ABL`, `SRC-DUCKSTATION-DBG`) were
  **read-only** throughout; only their committed docs, working-tree movie
  artifacts (hash-pinned), and built binary were consumed.
- `movie.loadAndArm` verified media serial and the anchor state's recorded
  SHA-256 before mutation and scheduled the arm-phase correction; access
  watches were armed after the state load (PS1 equip marker `0x800A6597`
  read/write; contact-array head `0x800B0D18` 256 bytes write);
  `movie.resumeUntilMovieFrame` completed 642/642 at normal speed with the
  owed correction frame consumed.
- Captured the marker's consumers live, disassembled the contact-time handler,
  and translated its arithmetic (`row*5 + marker`, `+2`, cap 200, threshold
  100) into `ghidra-query` searches over the PC export.
- Result: PC `candidate_berry_equip_byte` `0x0059D9A7` and
  `candidate_berry_hit_accumulator` `0x00599B20`, with writers in the
  confirmed pickup path, per-type behaviour gates, and a HUD mirror. Full
  bounded record:
  [[XPORT-20260818-006 - Berry equip byte candidate from replay-seeded static search]].

## Changes made

- New: [[XPORT-20260818-006 - Berry equip byte candidate from replay-seeded static search]].
- Updated: `KU-073` in [[Known Unknowns]] (static candidate recorded, ladder of
  discriminators revised; status stays open),
  [[XPORT-20260817-005 - Berry contact array and type marker shape]]
  (continuation section, running score), [[Subsystems MOC]] (berry-throw
  section), [[Current State]] (new bullet), [[Session Index]].
- No `reimplementation/` code, no target write, no PC runtime session, no
  external-repository modification. The banking commit follows this note.

## Unresolved questions

`KU-073` remains open: colour-to-value binding (read-only labelled A/B is the
next arm) and causal directionality (separately authorized single-byte write).
The PC decay/threshold constants (`0x78`, `-2` above `0x40`) are static-only
observations with no runtime confirmation.

## Process audit

One `duckstation-qt` process was launched and later stopped by verified exact
PID; a follow-up check found no `duckstation-qt` process and the private API
port closed. No game/Wine/Gamescope/86Box process was started; no audio sink
was created. `make session-audit` was run at banking time and its result is
recorded in the banking commit context; any unattributed processes it reports
belong to other sessions and were left untouched per
[[Agent Operating Manual#Runtime instance lifecycle]].
