---
type: experiment
id: EXP-20260905-006
environment: "Fedora Linux 44; Python 3.14.6; Unicorn 2.1.4; offline original PC relocation; existing user game preserved"
result: "512-unit atlas-local tiling passes offline gates and a fresh PC cold-load preview; complete resident mesh and unchanged collision verified; user visual approval pending"
date: 2026-09-05
status: runtime-preview-closed
question: Can the accepted playable area's textures repeat at a bounded world scale without changing collision or breaking native DAT relocation?
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
tags:
  - re/terrain
  - re/rendering
  - re/experiment
updated: 2026-10-02
---

# World-scale terrain tiling and checked mesh growth

## Scope and result

The user accepted [[EXP-20260905-005 - Original wall texture regions and colour inputs]]'s
combined wall appearance and requested the next authoring step: repeated textures
and enough render space to support them. This is an offline candidate on the
existing deck/ramp/box, not a second layout, live visual acceptance, or generic
level repacker. No R2q or full repository suite was run.

**Confirmed offline:** 34 new regressions pass in 0.50 seconds. The expanded
terrain-only gate passes 185/185 in 27.33 seconds. Original PC relocation
instructions pass all six comparison checks. Collision is byte-identical.

Evidence: `reports/terrain/EXP-20260905-006.json`,
`reports/terrain/EXP-20260905-006-relocation.json`, and private receipts under
`work/experiments/EXP-20260905-006/`.

## Native allocation discriminator

The existing primary160 render allocation is 2,234 bytes, with 1,730 used by
EXP-005. The 504 remaining bytes cannot hold the selected denser tile mesh.
Other nearby original meshes are still occupied; they are not treated as free
space and are not overwritten.

**Confirmed static:** original PC `FUN_0044bb70` loads object+0x14, adds the
DAT base, and stores the relocated pointer at `0x0044BD1A` through
`0x0044BD21`. At `0x0044BECA` it reads the file's final signed dword;
`0x0044BF0C` subtracts it from base+file_size, and `0x0044BF18` stores the
result in `0x005B7100`. It copies 256 bytes from that result+0x18 at
`0x0044BF25`. Ghidra was used as a search surface and corroborated with fresh
retail disassembly, preserved privately as `relocator-disassembly.txt`.

Consequently, a blind append would invalidate the end-relative location. The
selected writer adds a new mesh immediately before a replacement final dword,
keeps every old payload at its existing offset, and increases that final span
by the file growth. Its other old-file change is the selected object's known
geometry pointer. Unknown trailing-data contents are preserved, not renamed.

| Field | Before | Candidate |
| --- | --- | --- |
| File bytes | 332824 | 343012 |
| primary160 scene offset | 8580 | unchanged |
| Object offset | 18672 | unchanged |
| Geometry pointer field | 18692 | unchanged location |
| Geometry target | 113136 | 332820 |
| Final-word location | 332820 | 343008 |
| End-relative span | 8300 | 18488 |
| Trailing-data base | 324524 | unchanged |
| New mesh / padding | none | 10186 / 2 bytes |

**Independent instruction evidence:** `scripts/terrain-texture-tiling-probe.py`
runs the retail `0x0044BB70` instructions in isolated Unicorn memory with a
2,000,000-instruction limit. Source and candidate both return. The trailing
pointers and copied table agree, the changed geometry pointer is correct, the
new mesh remains exact, and all old relocated bytes outside the selected
pointer and displaced footer agree. This is not execution inside the live game
or proof of the file-read allocation path.

## Tile authoring choice

The first candidate uses 512 stored units (16,384 world units) per tile. This
is configurable in the bounded builder, not a claim about a universal original
tile size. One original floor donor spans irregular edges, not a fixed square.

Ground uses projected X/Z; vertical walls use height for U and their horizontal
axis for V. Every clipped face stays within page0 U0..63,V192..255 for ground
or U64..127,V192..255 for walls. Repetition resets within those atlas regions;
it does not wrap into neighboring terrain tiles. Texture/palette assets are
unchanged. The warm EXP-005 colour inputs are retained/interpolated separately.

The encoder splits each input quad along its existing 0-2 corner diagonal
before clipping to tile boundaries. Output uses the established arity bit,
tag0x0061, rather than claiming that subdivision alone repeats textures.
The result has 324 vertices and 524 triangles: 390 ground and 134 wall.
Unknown vertex+6/+7/+11 are preserved and mixed unidentified values reject.
Exact clipping uses rational coordinates; int16 encoding introduces at most
1/2 stored unit per coordinate in this candidate. Thus exact original triangle
boundaries are retained before quantization, not a claim of zero render-plane
error after rounding. The banked collision bytes and original mesh remain intact.

## Files and regressions

- Builder: `reimplementation/ablpc/terrain_texture_tiling.py`.
- CLI: `scripts/terrain-texture-tiling.py`.
- Original-instruction probe: `scripts/terrain-texture-tiling-probe.py`.
- Regressions: `tests/test_terrain_texture_tiling.py`.
- Fixture: `work/copies/EXP-20260905-006/fixture`.
- Fresh, unlaunched game: `work/copies/EXP-20260905-006/game`.

Source DAT SHA256:
`b9da33f9fa8a8227e78ed72fe6870f187e8065a04039b6de4ebcd72f719d6241`.
Candidate DAT SHA256:
`99fbff1754fc43979542de40e56c04d10d7af4fccde8d13e919853b679429a21`.
Unchanged TERRAIN.ALL SHA256:
`1ff3af9f0b5b2c2957bde8e877e1d988054455f3e1be18f8ea0e6cb57875d16b`.
New mesh SHA256:
`b759d335984bd132a589c0beae6c287d6cbb3d09b57128f890c46d04ea5867b4`.

Tests cover synthetic positive meshes, atlas boundaries and repeated origins,
negative coordinates, retained diagonals, tint interpolation, unknown fields,
counts/references/terminators, invalid trailer spans, aligned growth with and
without trailing data, two private tile densities, input hashes, exact collision
and old-payload preservation, and original-instruction relocation.

## Runtime boundary and next action

No launch, input, capture, live memory access, debugger operation or close was
performed. The EXP-005 user game remains open: game299378/start10038768,
group299129, display`:2`. The end audit matches all seven original processes
and sink module536870916. Its generic ledger reports `clean:false` because
these authoritative-procedure processes are not registered there; they are
explicitly accounted for, not unexplained leftovers.

Next ask to switch the open preview to the fresh EXP-006 game, then use
[[PC autonomous game control]], hardware/CD gates, exact loaded file/mesh
checks and normal-input inspection. Check texture scale, seams, disappearance,
depth/occlusion and performance from the deck, ramp and top. Do not claim a
render regression is impossible because collision was preserved. No old live
memory-write or process-stop authorization carries forward.

After this visual candidate is accepted, the next composition milestone is a
different connected route made from the proven pieces. Standalone packaging,
arbitrary geometry and all-view guarantees remain open.

## Preservation

The private EXP-005/006 packet contains 104 files and excludes game copies,
Wine prefixes and scratch. Archive comparison against its sources passed.

- `work/snapshots/terrain-20260905-material-tiling-evidence.tar.gz`: 5404866 bytes,
  SHA256 `d69a817bcaab45a7bf816bd85ce751e46c404e72a7671680c5612a206864c906`.
- `work/snapshots/terrain-20260905-material-tiling-evidence.manifest.tsv`: 14368 bytes,
  SHA256 `8644b12bf40b6cb14b268feadd85bf83ca62f0a26a37439b65443a98d26f737b`.

See [[2026-09-05 - Codex - Terrain texture tiling and mesh growth]], DEC-245,
[[New-level authoring roadmap (terrain, collision, materials)]].

## Later user-authorized cold-load preview

The user requested the switch after the offline bank. The EXP-006 preview, now closed for EXP-007, was opened
in Level01, group309445/game309701/start10311098. EXP-005 closed with an exact
clean audit before the fresh launch. All renderer/CD gates pass; complete
read-only mesh/collision comparisons pass, including all10,186 new mesh bytes.
The live trailing-data pointer is DAT base6596791+324524=6921315, corroborating
the offline preservation calculation. The natural-spawn capture shows repeated
ground and the warm wall; no movement sweep or all-view/performance result.
User aesthetic approval remains pending. Earlier unlaunched/no-runtime wording
above describes the immutable offline bank, not this current handoff.
See `reports/terrain/EXP-20260905-006-runtime.json` and
2026-09-05 - Codex - Tiled terrain user preview. No tests were rerun for the
launch, and its new receipts are not part of the earlier104-file archive.

## Runtime follow-up and preview closure: EXP-007

The user reported general playability as good, then reported falling through retained old scenery after stepping off and invisible terrain with retained collision elsewhere. The preview was closed with a clean audit for [[EXP-20260905-007 - Retail position control and missing floor footprints]]; it is no longer the live session. The retail control confirms selected active-floor omissions caused by the inherited source-99 replacement. Tiling did not change that collision payload. Do not turn general user approval into a claim that outside-deck layout coverage is complete.
