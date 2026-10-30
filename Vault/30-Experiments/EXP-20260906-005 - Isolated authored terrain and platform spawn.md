---
type: experiment
id: EXP-20260906-005
date: 2026-09-06
created: 2026-09-06
updated: 2026-10-29
status: native gate accepted; live read-only check completed; control preserved
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 43 offline authoring, native PC instruction probes, and isolated Wine runtime preview
question: "What must be kept, and what can be emptied, to remove the original Level01 terrain, collision and scenery draws from the file pair, and where does the initial spawn position come from?"
result: "Terminate non-clone triangle streams but keep descriptor kinds and directory (native init counts the slots); clear the low three draw-kind bits to mute scene records (dispatchers 004498F0/00448D70 have no case); spawn X/Z/heading come from executable table 0x004DC7E8 via 0043E6B0; native gate 10/10 and live loaded-byte match"
tags: [re/experiment, terrain/collision, terrain/authoring]
---

# EXP-20260906-005 - Isolated authored terrain and platform spawn

## Summary

Removing the original Level01 landscape, collision and scenery draws while keeping only the EXP-004 authored platform/box/ramp/sides works when the original slots are emptied rather than deleted: non-clone triangle streams get an immediate signed-negative terminator, descriptor kinds and the directory stay intact because native initialization counts the slots, and scene records are muted by clearing their low three draw-kind bits. The initial spawn position is executable data, not a DAT row: X/Z/heading come from the per-level table at 0x004DC7E8. The corrected native gate accepts 10/10 arms and a live read-only check matched the loaded bytes.

This experiment does not claim a new level container, universal mesh rule, or completed authoring tool. EXP-20260906-004 is the untouched control.

The 2026-09-06 experiment/run directories contained 001 through 004 before allocation. New private files are under `work/copies/EXP-20260906-005`; evidence is under `work/experiments/EXP-20260906-005`. No original assets, protected stash, old experiments, or running process were changed. No full suite or R2q test was run.

## Implementation and exact provenance

Module: `reimplementation/ablpc/terrain_isolated.py`. Builder: `scripts/terrain-isolated-area.py`. Native driver: `scripts/terrain-isolated-area-probe.py`. Synthetic/preservation regressions: `tests/test_terrain_isolated.py`.

The input pair is the hash-pinned EXP-004 fixture. Its mixed source 99 contains 134 original cells followed by 36 authored cells. Exact authored 44-byte groups at old offsets 48380..49920 are copied to active offsets 43924..45464, stride 44; corresponding cells begin at group+12. The new active terminator is 45508. Normals, edge words, bounds, clearance and all other authored group bytes are unchanged. The 20 EXP-004 side groups retain the 48-stored-unit outward trial, not a newly established body radius.

Other nonclone triangle streams in both Level01 TERRAIN.ALL and BITS/PLANTTER.ALL receive an immediate signed-negative terminator. Clone identities and kinds remain intact and inherit their emptied templates. Do not zero descriptor kinds or compact the directory: native initialization counts these slots before reserving later runtime descriptors. Twelve high-kind streams (ten 0x101 and two 0x104) retain their opaque bodies but no longer carry the 0x12345678 registration marker. The PC loader at 0x004A8410 independently establishes the link gate; suppressing registration does not identify the opaque 0x104 payload semantics. Directory offset 224156 and file sizes are unchanged.

Mesh 160 contained five original command groups/69 faces followed by the authored 524-face play area, 30-face connector and 253-face side skin. Only the authored command suffix is active now: 807 faces, command start 353260, terminator 362956. The 615 vertices remain in place, including 92 unreferenced original vertices; unknown suffixes, UV/material fields, geometry pointer 345876, culling radius 8560 and footer stay unchanged.

The other 483 primary and all 140 secondary scene records retain their loader layout bits, pointers and data, but their low three draw-kind bits are cleared. The original dispatchers 0x004498F0 and 0x00448D70 have no matching draw case for the resulting modes. Native relocation still traverses their preserved object layouts. This is active draw suppression, not erasure of private archaeological bytes or a claim that an unidentified flag means hidden. Original actor/collectible definitions, sky, level scripts and shared texture/model data are retained.

## Spawn: executable data, not a DAT row

Static evidence in `spawn_static4.json` establishes that initial placement calls 0x0043E6B0 from 0x0042E5C0. It loads X/Z/heading from the per-level executable table at 0x004DC7E8, then calls height query 0x004AC460. This is not the Level03 type-1 reset selector.

Level01's row is VA 0x004DC7F4, private auto-hardware executable file offset 0xDB3F4 (898036). The builder changes only its first eight bytes: X/Z (197108,492895) to (192000,448000). Heading 3505 is preserved. No Y, code instruction or running memory is patched. Stored X/Z (6000,14000) is well inside the authored platform.

The separate discriminator executes the original initializer and observes current, preceding and auxiliary coordinates all equal (192000,-102528,448000). The existing native landing arms settle on the platform at Y=-102400. The initial-spawn-and-settle arm itself was first not accepted, for the test-setup reason below, and was accepted after the correction.

## Validation and contradiction retained

- Affected regression suite: **53 passed in 0.14 s**, synthetic collision/PE/span bounds and unknown-byte preservation plus the private render control.
- Focused five-file terrain gate: **72 passed in 26.90 s**, four workers/loadfile, repo-local scratch, failed-only retention.
- Native matrix: **9 accepted arms, 1 unaccepted arm in 3.226762077 s**. Overall result remains false.
- Native loader/initializer reaches exactly **36 active cell instances**, all authored source 99; no other loaded descriptor reaches a cell. The 0x101/0x104 linked heads are zero.
- Native DAT relocation and authored command traversal pass. Muted primary records in both draw passes and muted secondary records reach none of the watched transform/draw entries.
- Three ramp lanes pass downhill and uphill return between stored Z=14000 and 11100 without a leg reset. The foot-to-old-ground route is deliberately not an acceptance criterion now.
- Box uphill/downhill/return, top landing and step-off onto the new deck pass. A platform-edge path remains airborne outside the new area; there is intentionally no old floor underneath.
- Native height queries at five outside footprints, including the earlier missing-floor comparison points, return the no-surface sentinel. This finite negative test complements, rather than replaces, the exhaustive loaded-cell census.

**Probe bug, not hidden as a pass:** `native_initial_spawn_and_settle` failed its heading assertion. The new driver copied only the changed X/Z words into the offline model; that model begins with zeroed static data, so its unchanged heading word was never seeded. `spawn-discriminator.json` records the all-zero initial 12-byte row, the X/Z-only setup, heading zero and the correct platform coordinates. The real output executable preserves heading 3505, as the compare-guarded writer and regression establish. After the disclosed setup correction was approved, the probe loads the complete file-backed12-byte row, preserving heading3505. `work/experiments/EXP-20260906-005/native-validation-02.json` records **10/10 accepted in3.295094101s**; the initial failed report is retained.

## Outputs and receipts

`reports/terrain/EXP-20260906-005.json` is the asset-free summary. Complete patch offsets, hashes and source/scene inventories are in private `build.json`. Output hashes:

- TERRAIN.ALL: `961ff444fd875e80ce9e721e9f7fa264a7bea9059b54049d6145acc9154fb2db`
- LEVEL.DAT: `3461dff75763670f54607efc6829c952158dc7876651c6a3f1088d0bcb0658af`
- PLANTTER.ALL: `c7fadbec78ac2c35f880c0dd5025e86a12604482c01dd93be38a90f6ad2d0cc9`
- Private spawn executable: `9d406ac0a1319ba58c9637eb51a45f499c2a0f901c674ce36e5d1d7aebb35ffe`

The executable is derived from the banked auto-hardware image, not mislabeled as unchanged retail. The PC instruction model uses retail code; its setup writes are offline only. No old live-write/teleport authorization was consumed.

## Runtime check

A fresh file-loaded run (game109048/start1545038, group108790) used all three modified assets and the separately pinned executable. Read-only evidence matched the full authored source99 payload and full807-face mesh,623 suppressed original scene draw modes, and the file-backed spawn row. Two additional kind110 descriptors pointed to the same empty template stream; `preview-01/dynamic-template-coverage.json` preserves this bounded observation, not a claim about every actor collision system. Exact live initial placement was not observed. The user reported that berries stop at an edge while Flik can fall off.

An initial startup discriminator incorrectly rejected a320x200 mode-enumeration line despite the six positive640x480 hardware markers. Its shell batch continued and sent one brief Right press after the game was already in Level1; do not claim a pristine startup route. Runtime details: `reports/terrain/EXP-20260906-005.json` and EXP-005 `preview-01/` receipts.

Remaining actor placements are not removed by this terrain-only change.
