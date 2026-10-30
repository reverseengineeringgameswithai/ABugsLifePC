---
type: session
date: 2026-08-12
agent: Claude
status: completed
tags:
  - session
  - re/dynamic
  - implementation/tooling
---

# Runtime tooling live validation

## Agent

Claude

## Goal

Validate all six runtime tools from [[Runtime Tooling]] against the live
Training game, and validate the `rr` arm now that
`kernel.perf_event_paranoid` was set to `1`.

## Files inspected

- [[Current State]], [[Project Roadmap]], [[Environment Status]],
  [[Decision Log]], [[Known Unknowns]], and [[Runtime Tooling]].
- Live game process `/proc` state; `bugs.log` renderer markers.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments inspected

- [[EXP-20260812-015 - Plant pair caller and consumer trace]] (plant 10 path).

## Changes made

- **Fixes (each with a regression test):** Windows-path cmdline basename in
  `scripts/evidence_lib.py`; Wine `SIGUSR1` pass-through in
  `scripts/gdb-harness.py`; per-API apitrace wrapper name in
  `scripts/apitrace-capture.sh`. Committed as `148376d`, `9f47e97`, and the
  apitrace fix.
- Vault: [[Runtime Tooling]] live-validation section; `DEC-20260812-020`;
  `KU-028`/`029`/`030` updates; [[Environment Status]] and [[Current State]].
- Curated metadata for the validation runs retained under `dynamic/wine/`;
  cores/frames/traces stayed in git-ignored `work/` paths.

## Conclusions

- **Confirmed:** All six tools work against the live WoW64 game. The GDB
  harness reached `NextLife` and its watchpoint plus `core-grep` independently
  reproduced `0x006C342B` at `0x005B1AA4` (matching
  `RUN-GDB-20260812-153150`). frozen-capture froze/captured/resumed the game;
  relay set/restored the registry with correct metadata; apitrace `--api egl`
  captured a 2.2 GB EGL trace.
- **Confirmed (established defaults):** frozen-capture backend is
  `gamescopectl screenshot <path>` (asynchronous); apitrace needs `--api egl`
  because WineD3D drives GL through EGL here.
- **Confirmed (negative):** `rr record` cannot record the Wine game on this
  NVIDIA host (FATAL on an unsupported NVIDIA ioctl during Wine init); `rr`
  works on a trivial program and the wrapper is validated (`KU-028`).

## New hypotheses

- Forcing Wine onto the host AMD Radeon / Mesa path may let `rr` record,
  avoiding the NVIDIA ioctls (`KU-028`).

## Contradictions discovered

- None. Synthetic tests had passed while three real defects existed; the live
  run exposed them, and regression tests now cover each.

## Tests run

- Full `pytest -q tests` (117 → with new regression tests) and the
  tracked-file audit pass; `make check` at close. Live runs recorded under
  `RUN-{GDB,CORE,FRZ,RR,APITRACE,WINE}-2026081?-*`.

## Unresolved questions

- Whether the frozen-frame `SIGSTOP` perturbs later game state (`KU-029`);
  whether the apitrace EGL stream discriminates `KU-012` (`KU-030`); whether
  `rr` works via the AMD path (`KU-028`).

## Recommended next action

Resume the active M2 packet in
[[Project Roadmap#M2 — Resource dependency graph and one editable asset family]].
The GDB harness is now available to replace hand-transcribed watchpoint runs.

## Git commit if applicable

Bounded commits: the three fixes, plus
`docs: record runtime tooling live-validation results`.
