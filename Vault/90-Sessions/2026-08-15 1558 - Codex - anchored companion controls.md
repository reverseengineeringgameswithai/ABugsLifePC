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

# Anchored companion controls

## Scope

Implement the user's preferred correction after the first long PC input movie
diverged: replace the ambiguous three-second default with one convenient,
visible, shared game-state anchor for recording and replay. Preserve the
Windows PC authority, unchanged pinned launcher, Obsidian evidence trail, exact
input scope, and clean runtime/repository lifecycle.

## Implementation

Updated `scripts/input-movie.py` and
`scripts/play-pristine-with-inputs.py` to 1.1.0.

- Recording defaults to new PC research-log bytes containing
  `--- Start LevelSelect ---`; manual delay remains a labeled weaker fallback.
- The worker emits optional `armed`, `recording-started`, and `replay-started`
  NDJSON supervisor events over an inherited descriptor.
- The companion displays **ARMED**, **RECORDING NOW**, and **REPLAYING NOW**
  from those worker events and adds a Replay menu/button.
- Replay validates the movie, uses its recorded anchor, and preserves a log
  movie's recorded post-marker neutral interval before schedule zero.
- **Next recording output** and **Last saved** are distinct UI fields.
- Cleanup retains the exact isolated process-group ID after launcher-leader
  exit; SIGINT/SIGTERM request the normal scoped cleanup path.

Renderer choice is now setup: start Record or Replay at the renderer selector,
wait for **ARMED**, then select Hardware. Route input begins at Level Select,
not during renderer setup.

## Verification

- 23/23 focused input-movie/companion fixtures pass.
- The complete repository gate passes 557 tests, Vault 355/0/0, the five M4
  hash anchors, and the tracked-file audit.
- Both Python entry points compile.
- Machine-readable capability and dry-run output pass.
- The pinned `scripts/play-pristine.sh` remains SHA-256
  `68c9171749bd7b207a15b4202193ccfddd2661fbb383deb34b1a5a5a4049977e`.
- No game, Wine, Gamescope, input-movie, companion, or private mute-sink
  residue was present before or after the offline work.

## Durable outcome

[[EXP-20260815-122 - Anchored companion record and replay controls]] records
the fixture-accepted correction and
[[Decision Log#DEC-20260815-115 - Default companion routes to a shared PC log milestone]]
records the design boundary. [[PC input movies]], [[Runtime Tooling]], the
roadmap, capability register, Current State, environment status, KU-057, and
both relevant MOCs now point to it.

The Level Select marker remains provisional. This session launched no live
game and makes no Training, Level03, gameplay-acceptance, or engine-frame
claim.

## Next action

Launch the companion for one fresh user usability arm. Choose Record before
selecting Hardware, wait for **RECORDING NOW**, and record the intended route.
Then choose Replay in a fresh session before selecting Hardware and verify the
level load independently from the accepted input receipt.
