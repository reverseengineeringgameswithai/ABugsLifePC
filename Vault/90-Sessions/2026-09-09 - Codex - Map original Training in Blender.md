---
type: session
date: 2026-09-09
updated: 2026-09-09
agent: Codex
status: completed-bounded
tags: [session, implementation/blender]
---

# Map original Training in Blender

## Goal and result

The user asked to map original levels in Blender, using LEVEL00 Training, the
first carousel selection without moving Right. Delivered and opened
`work/level-projects/original-training-map/level.blend`, with packed original
textures, selectable scenery/source offsets, collision/barrier/placement layers,
named landmarks, notes and `overview.png`. [[PC original Training Blender mapping]]
is the persistent handoff; [[EXP-20260909-012 - Original Training Blender mapping]]
contains hashes, counts, evidence and verification limits.

## Evidence and changes

Read the required handoff surfaces, charter/manual, Implementation/File Formats
MOCs, authoring guide, bounded PC DAT/collision/RAW sources and prior Training
runtime receipts. No external PS1 project was consulted. Prior accepted PC log
proves Training loads LEVEL07/LEVEL1.DAT, LEVEL1.RAW and TERR1.ALL; the on-disk
LEVEL00 source inspected during orientation is a different scene.

Added `original_level.py`, the CLI import-original/edit path,
`tools/blender/original_map.py`, a saved-scene verification script and parser
regressions. All278 mesh records import; four original texture pages,1360 collision
triangles,80 barrier segments and78 markers are retained. The43 geometrically
distant primaries and16 secondary objects begin hidden;219 nearby primaries frame
the level. Complete source copies preserve unknown fields. The initial wide-frame
trial remains under `work/level-projects/original-training/`.

## Tests and limitations

73 focused pytest tests and selected `make check` pass,6075 tests deselected;
compatibility/tracked-file checks pass and Vault lint reports zero errors/eight
existing warnings. Hooks already installed. Native texture expansion reproduces
EXP-20260905-005's captured page0 indices/palette exactly. Real Blender5.2 verifies
12414 saved vertices,30875 UV corners,1360 collision faces, four packed textures,
78 markers and named-landmark persistence after saving/reopening a separate copy.
Rendering completed; Blender printed a small shutdown allocation warning on
creation but returned success, and the independent saved-file validation passed.

Animation, actors/scripts, native initialized pickup heights, exact lighting and
original-level game-file export remain open. No fresh PC runtime parity claimed.
Source IDs stay neutral where semantics are unknown. This does not resume streaming.

## Lifecycle and next action

The new mapping Blender session is intentionally open. No private sink. No game
launches, closes, keys, debugger actions or memory operations. Old
editor/project saved hashes were read and retained.
[[Environment Status]] owns the identities.

User can now inspect Training, toggle overlays and save notes/landmarks. A second
level or export back into the original game needs a separately bounded extension.
No Git commit was requested or made; assets remain under ignored work storage.
