---
type: session
agent: Codex
date: 2026-08-15
status: complete
tags:
  - sessions/codex
  - cap-002
  - input-movies
---

# Anchored movie live replay

## Scope

Launch the corrected PC companion for a new user recording, then replay the
latest completed movie in a fresh pristine session while preserving exact
runtime ownership, PC-only authority, and repository hygiene.

## Procedure

The first fresh companion used `--research --windowed --mute`. The user chose
the default Level Select anchor and produced accepted record
`RUN-INP-REC-20260815-160815`. The session was closed through scoped SIGTERM;
its launcher group and private sink cleared.

The latest movie validated as a 300-event, 54.331-second production movie at
SHA-256 `abc45db...17b91`. A second fresh companion/session was launched. The
exact replay worker was armed on its recorded marker before one disclosed
Down/Return setup pair selected Hardware. Replay
`RUN-INP-REP-20260815-161221` accepted all 300 events and released every key.

## Outcome

The replay log passed every Hardware/Direct3D marker and loaded Training
`gfx\training.raw` plus `level07\level1.raw`, reaching `NextLife`. This corrects
the earlier Level Select divergence. The user nevertheless observed later
gameplay desynchronization.

The movie's first gameplay-looking `z` is only 1.337545224 seconds after the
second Return release, while that one wall-clock schedule spans the entire
Training load and initialization. This session originally treated variable
load duration as a supported but unproved mechanism. Timestamped target-echo
evidence in EXP-124 supersedes that inference for the tested replay.

[[EXP-20260815-123 - Level Select anchored route gameplay desynchronization]]
records the evidence and limits the Level Select marker to menu/level entry.
[[EXP-20260815-124 - Replay echo identifies target input stream distortion]]
places `NextLife` about 954 ms before the first gameplay `z` and proves that
the current backend transforms target event sequence/timing. Correct delivery
before the deferred first-`NextLife` phase discriminator.

## Lifecycle

Both owned companion sessions, game/Wine/Gamescope groups, replay worker, and
private sinks were closed. The final runtime audit was clear. The ignored movie
remains under `work/copies/input-movies/`; only asset-free record/replay
receipts are curated.

The complete repository gate passes 557 tests, Vault 357/0/0, the five M4
hash anchors, and the tracked-file audit.
