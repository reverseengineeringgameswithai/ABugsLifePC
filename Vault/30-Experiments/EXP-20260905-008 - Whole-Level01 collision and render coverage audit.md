---
type: experiment
id: EXP-20260905-008
date: 2026-09-05
question: Is source 99 the only collision source changed, and how does its footprint relate to changed rendering?
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Offline existing PC parsers; no executable or runtime controls invoked
environment_version: Existing repository venv; no environment change
working_directory: /home/dev/ABLPC
configuration: Hash-pinned retail EXP-007 Level01 versus authored EXP-006 Level01
artifacts:
  - reports/terrain/EXP-20260905-008.json
  - work/experiments/EXP-20260905-008/audit.py
  - work/experiments/EXP-20260905-008/coverage-map.svg
addresses:
  - 0x004A8410
  - 0x004A8A1A
  - 0x004AC460
  - 0x0045A8B0
file_offsets: [43924, 43926, 44540, 44542, 45884, 48380, 48384, 8580, 18672, 113136, 332820]
result: Confirmed source-99-only collision edit; broad active-floor replacement and nonmatching render footprint
created: 2026-09-05
updated: 2026-09-05
tags:
  - re/experiment
  - terrain/collision
---

# EXP-20260905-008 - Whole-Level01 collision and render coverage audit

## Bounded question

After [[EXP-20260905-007 - Retail position control and missing floor footprints]], the user asked whether the observed area was the only place collision had been removed. This experiment inventories all files in the two Level01 trees, every TERRAIN.ALL source record and payload, resolved active collision cells, barriers, and all supported static render references. No assets are edited and the user's existing game is not inspected or controlled.

## Inputs and method

Retail: `work/copies/EXP-20260905-007/og-game/PC/BUGS/CD/LEVEL01`.
Authored: `work/copies/EXP-20260905-006/game/PC/BUGS/CD/LEVEL01`.

Retail TERRAIN.ALL SHA-256: `62f3b73f21630eb19c04e585a92e1f3e32a76fdcb6ec36bae18f9c1ec3a2a868`.
Authored TERRAIN.ALL SHA-256: `1ff3af9f0b5b2c2957bde8e877e1d988054455f3e1be18f8ea0e6cb57875d16b`.
Retail LEVEL.DAT SHA-256: `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`.
Authored LEVEL.DAT SHA-256: `99fbff1754fc43979542de40e56c04d10d7af4fccde8d13e919853b679429a21`.

The read-only operator reuses `TerrainAll`, `TerrainHeightModel`, `floor_cells`, `BarrierPayload`, `LevelDat`, `mesh_groups`, `render_census`, and existing projected-polygon predicates. Active-cell enumeration resolves clones and omits inactive templates. Both full raw-byte differences and decoded active traversals are recorded. Existing parsers bounds-check reads; no new game-data parser or writer is introduced, and unknown fields remain untouched in the input copies.

The final audit completed in 2.832952 seconds. Fresh ID checking found no EXP-008 note/report/work collision. The run-index check retained the known unrelated 14 uncited runs and one dangling citation; that debt was not repaired or treated as a terrain failure.

## Confirmed: exact edit extent

- All 16 Level01 files were compared. Only `TERRAIN.ALL` and `LEVEL.DAT` differ. The other 14, including `TERR1.ALL`, `LEVEL.RAW`, `LEVEL1.DAT`, and `LEVEL2.DAT`, are byte-identical.
- TERRAIN.ALL has 189 records in both arms and remains 236,940 bytes. The complete source directory, file header, and suffix are unchanged.
- Source 99 is the only changed payload. Its allocation is `[43924,48384)`. Exactly 592 bytes differ, entirely within `[43926,44542)`.
- All other 188 source records and payloads are byte-identical. Only descriptor 99 consumes payload 99; no clone shares this changed payload.
- All ten kind-0x101 barrier sources, 178 through 187, are unchanged, including their 262 segments and unknown/trailing fields.

This confirms one changed collision source in the compared Level01 data, not one small spatial hole and not a guarantee that all runtime interactions elsewhere are unchanged.

## Confirmed: active collision loss

| Inventory | Retail | Authored |
| --- | ---: | ---: |
| Resolved active cell instances | 7,281 | 7,161 |
| Source-99 active cells | 134 | 14 |
| Source-99 groups | 14 | 14 |
| Source-99 terminator offset | 48,380 | 44,540 |

Exactly 7,147 active cells are unchanged. All 134 original source-99 cells are retired from active traversal; 14 authored cells replace them. They are not 120 individually deleted triangles plus 14 retained originals.

Of the 134 retired cells, **116 still have identical raw bytes at their original offsets**. Their presence in the file does not make them reachable: the authored terminator ends traversal earlier. This is why a byte-diff-only or raw-memory-presence check would undercount the disabled original ground.

Source-99 vertex X/Z bounding boxes, in world coordinates, are:

- Retail: X `[138080,288064]`, Z `[320224,544000]`.
- Authored: X `[128000,265600]`, Z `[416000,579200]`.

These are bounding boxes of irregular geometry, not filled rectangles or a claim about the exact uncovered area.

## Confirmed: rendering is a different partition

All 124 type-0x41 static mesh references were decoded through their full face streams in both arms. Only primary reference 160 changes its scene record, object header, and reached geometry. The other 123 references are unchanged at those compared surfaces.

- Reference 160: scene offset `8580`, object offset `18672`.
- Original geometry: offset `113136`, 92 vertices, 69 faces, terminator `115368`.
- Authored geometry: offset `332820`, 324 vertices, 524 faces, terminator `343004`.
- Total decoded faces: 6,046 retail and 6,501 authored.

The source-99 collision footprint is not the mesh-160 rendering footprint. At the earlier fall endpoint `(222481,-22529,383185)`, retail collision is source 99 / cell `45884`, while rendering projects from unchanged primary mesh 213. The authored arm has no active collision candidate there but retains that render reference. Likewise, the OG control's source-99 entry point projects onto unchanged mesh 124; its later source-99 point projects onto unchanged mesh 213. Collision and render record IDs must not be paired by assuming the records partition the world identically.

The recorded retail spawn X/Z still has projected mesh 280 in both files, plus the authored mesh 160 overhead/in that footprint in the authored arm. This does not establish the user's exact separate invisible-ground location or screen visibility. That report remains a coordinate/height/camera localization question, not a silently resolved claim that the known spawn mesh was removed.

## Coverage probes and map

One centroid was sampled per retired original cell. At 46 of those 134 centroids, the authored active-cell inventory has no projected X/Z candidate. All 46 also have overlapping supported static render geometry in projection. This is 46 sampled points, not 46 disconnected holes or proof that the entire other 88 triangles retain same-height support.

`work/experiments/EXP-20260905-008/coverage-map.svg` draws retired collision and authored collision on the left, and replaced render geometry and unchanged surroundings on the right. Coordinates are projected from decoded data, not generated artwork. Red denotes original geometry no longer active at the changed reference, teal denotes authored geometry, and grey denotes unchanged geometry. Exact offsets, vertex references, duplicate vertices and correspondence margins are retained in the private JSON inventories.

## Limitations and contradictory evidence

- This is an exhaustive file/source/cell edit inventory for the two compared Level01 trees, not a game-wide collision or runtime-behavior proof.
- The map and centroid queries are X/Z projections. They do not prove equal-height landing, triangle admission, winding visibility, texture opacity, or camera visibility.
- Twenty-eight rotated/scaled static references per arm have unchanged bytes but unresolved world projection in the existing bounded census. Their IDs and transform metadata are explicitly retained, not silently treated as absent. Other renderer dispatches and dynamic objects are not inferred to be ground.
- Other Level01 files are byte-compared, not newly reverse engineered. Extra runtime collision families outside this file are not claimed to have been semantically audited.
- The initial EXP-007 teleport transient and stale contact pointer remain limitations of that control. This offline audit does not retroactively turn it into a pristine or exact earlier-fall replay.

## Artifacts and preservation

Public summary and exact findings: `reports/terrain/EXP-20260905-008.json`.

Private complete inventories and map: `work/experiments/EXP-20260905-008/`. This includes input hashes, every source record, group boundaries/terminators, resolved descriptors, active/retired/added cells, barriers, all render references/faces, exact and near-footprint correspondences, duplicates, centroid probes, and byte ranges. The report lists artifact sizes and SHA-256 hashes. Private decoded geometry and the SVG belong under `work/`, not in Git.

No game input, memory read/write, launch, close, debugger, ptrace, save state, process stop, asset modification, tests, R2q suite, or Git operation occurred in this audit. The prior OG session was deliberately left untouched; its ownership is the last-observed EXP-007 state, not a newly checked runtime claim.

## Next discriminating implementation step

Design a non-destructive integration candidate that preserves the original source-99 active groups and original render mesh 160, while adding the authored area's collision and rendering through independently checked storage/descriptor paths. If that requires format growth beyond the established writer boundary, first prove that bounded allocation/relocation step offline rather than silently reusing another live terrain record.

Before another launch, use original PC instructions to replay the earlier fall and prove authored-to-retail exit, landing, return, and overlapping-height selection. Keep the current replacing fixture as a control. The working box/top/ramp primitives need not be re-proved merely because their prototype reused level storage.
