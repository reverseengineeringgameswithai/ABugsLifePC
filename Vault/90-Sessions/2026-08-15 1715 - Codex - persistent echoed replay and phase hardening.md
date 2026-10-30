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

# Persistent echoed replay and phase hardening

## Scope

Correct CAP-002's measured delivered-stream defect, replay the user's immutable
Training movie in fresh pristine PC arms, retain any remaining contradiction,
and harden future recordings without using the PS1/DuckStation tooling or
changing the `ntsync` privilege boundary.

## Work performed

`scripts/input-movie.py` 1.3.0 now uses a persistent X11/XTEST replay
connection plus mandatory exact-window delivery echo. It disables nested-
display auto-repeat only during replay, restores it on every exit, rejects
unrelated or mismatched events, measures target delivery rather than a pre-send
subprocess boundary, and binds bounded runtime-log checkpoints into new
schema-2 log-anchored movies while retaining schema-1 playback. The Tk
companion is 1.3.0 and defaults gameplay
recording to the post-initialization `NextLife.` marker while retaining a
clearly menu-only Level Select option and the weaker manual fallback.

The immutable Level Select movie was replayed in three fresh arms. One failed
closed on an unexpected `Super_L`. Two accepted 300/300 exact target echoes at
under 0.52 ms maximum delivery drift and agreed under the input receipt
comparison. Their game outcomes nevertheless differed: the first returned to
Level Select, while the second remained in Training. This separates the fixed
input-emitter defect from an unresolved game-phase/engine determinism problem.

## Evidence and limits

[[EXP-20260815-125 - Persistent echoed replay and residual gameplay divergence]]
records run IDs, hashes, timing, runtime observations, and the retained
contradiction. No internal-frame claim is made. The old movie is not rewritten
as a `NextLife` movie because its source phase at that boundary is unknown; the
next live discriminator requires a new user recording.

No original, executable, asset, PS1 source, game memory, or privileged kernel
state was changed. `rr` was not run and `/dev/ntsync` was not removed.

## Validation and lifecycle

Focused input-movie/companion tests pass 27/27 and the canonical repository
suite passes 561 tests. Vault lint reports 361 notes, zero errors, and zero
warnings; all five M4 compatibility anchors and the tracked-file audit pass.
All owned live runtime groups and private sinks were closed before
documentation and commit. The final Git state is recorded at handoff.
