---
type: session
agent: Codex
date: 2026-08-15
status: completed-with-open-level03-validation
tags:
  - cap-002
  - runtime
  - input-replay
---

# 2026-08-15 1258 - Codex - CAP-002 PC input movies

## Scope

Implement the bounded CAP-002 input-recording worker for the Windows PC port,
validate it against the real Gamescope/Wine game window, update the Obsidian
handoff, and leave no runtime or Git residue.

## Boundary correction

The initial thought of consulting the DuckStation external-debugger skill was
stopped immediately after the user clarified that DuckStation is PS1-specific
and this repository is authoritative for the PC port. No DuckStation action or
file was used. The final worker is entirely PC-native: X11 window events,
Wine/Gamescope process ownership, retail PC executable hashing, and PC
`bugs.log` renderer gates.

## Work completed

- Added `scripts/input-movie.py` 1.0.0 with production exact-window keyboard
  record, strict movie validation, hash/window/focus-gated replay, receipt
  comparison, new-log/manual-delay/optional-frame-hash anchors, and emergency
  held-key release.
- Declared and enforced no `/dev/input`, host-keyboard, XRecord, display-wide,
  unrelated-window, or internal-game-frame capability.
- Added 11 focused asset-free regressions and `make input-movie-caps`.
- Recorded a four-event Down/Return movie from a fresh retail-PC selector arm
  and replayed it in two more fresh process groups. All three arms passed the
  complete Direct3D/no-software log gates. Both replays dispatched 4/4 events,
  released all keys, stayed below 1.8 ms maximum absolute drift, and agreed by
  receipt.
- Curated only the asset-free input movie and three JSON receipts under
  `dynamic/wine/`; game logs and exploratory artifacts remain ignored under
  `work/`.
- Updated [[PC input movies]], [[Runtime Tooling]], the CAP-002 register,
  [[Project Roadmap]], [[Current State]], [[Environment Status]],
  [[Known Unknowns#KU-057]], [[Decision Log]], and the relevant MOCs.
- Passed `make check`: 545 tests, Vault 349 notes
  with zero findings, five-anchor M4 compatibility, tracked audit, and diff
  checks. The Make test target now supplies the repository package path
  explicitly, closing the clean-shell collection failure found on the first
  gate attempt.

## Durable outcome

See [[EXP-20260815-119 - PC input movie recorder and hardware replay]].
CAP-002 is partially resolved at the exact-window keyboard and opening-selector
boundary. It remains open for a user-recorded Level03 route repeated alongside
the read-only KU-057 trace. Monotonic schedule offsets are not engine frames;
log/frame anchors have fixture rather than live gameplay coverage.

## Lifecycle

Each owned game/Gamescope process group was closed before the next arm. Private
mute sinks were absent after cleanup. Final repository and runtime audits are
recorded in the task handoff.
