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

# Replay target stream diagnosis

## Scope

Determine why the accepted replay of the user's Training-completion movie
visibly desynchronized, without changing the implementation or game.

## Procedure

I launched one fresh pristine research/windowed/muted companion, armed both
the unchanged source replay and a second production recorder on the same exact
game window, and selected Hardware outside the shared Level Select anchor. A
third monotonic observer timestamped Training load, initialization, and
`NextLife` log milestones.

Replay `RUN-INP-REP-20260815-162512` accepted 300/300 events. Echo record
`RUN-INP-REC-20260815-162512` retained 304 normalized target events plus 150
normalized-away preparatory releases. Source/echo sequence and timing were
then compared offline without editing either movie.

## Outcome

The first gameplay `z` arrived about 954 ms after the fresh replay's
`NextLife`, disproving the proposed direct loading-loss mechanism in this
arm. The target echo instead proves that the current per-event synchronous
`xdotool` path transforms the stream: it inserts two `Right` release/press
pairs and stretches several sub-0.053-ms transitions to about 15.1 ms. Some
holds change by 20-35 ms. The receipt timestamps before the send subprocess,
so its accepted drift does not measure this delivery error.

This is a confirmed replay-backend defect capable of causing gameplay
desynchronization. The exact altered event responsible for the user's first
visible divergence remains unknown because no visible/game-state timestamp
exists. [[EXP-20260815-124 - Replay echo identifies target input stream distortion]]
records the evidence and supersedes the loading inference in EXP-123.

## Lifecycle

The owned companion session, game/Wine/Gamescope group, both input workers,
observer, and private sink were closed. One scoped Wine device process required
`SIGKILL` after ignoring `SIGTERM`; the final targeted audit was clear. The
source and diagnostic movies remain ignored under `work/copies/input-movies/`.
Only the two asset-free receipts and Vault record are committed. The complete
repository gate passes 557 tests, Vault 359/0/0, all five M4 hash anchors, and
the tracked-file audit.
