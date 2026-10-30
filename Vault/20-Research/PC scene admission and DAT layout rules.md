---
type: research
status: confirmed-bounded
created: 2026-10-29
updated: 2026-10-29
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
evidence: [EXP-20260911-002, EXP-20260911-009, EXP-20260914-003, EXP-20260914-010, EXP-20260914-011, EXP-20260914-012, EXP-20260915-001, EXP-20260916-007, EXP-20260928-001]
tags: [re/rendering, re/level-data, terrain/authoring, re/static]
---

# PC scene admission and DAT layout rules

Rules the original renderer and DAT loader impose on added or changed scene
geometry: the primary scene gate's coordinate range, object rotation, the
end-of-file footer, free texture pages, and the original layout of LEVEL06
(Cliffside). Experiments cited as plain IDs are not in this vault. They found
these rules while adding scenery to test builds.

## The primary gate narrows camera coordinates

First recorded in EXP-20260916-007 (original-PC frame replay, private files
`native-primary-gate.txt`, `0045a7f0.txt`, `camera-range.json` and
`native-frame-height.json` in `work/experiments/EXP-20260916-007/`):

- The primary gate makes a wide X/Z distance and radius test at
  `0x0044D5EA`/`0x0044D5EC`, then narrows camera-relative values at
  `0x0044D5F2..0x0044D62E` (the word reads in
  [[FUNC-97C95BA5572D-0044D430]]). The transform `0x0045A7F0` also narrows
  intermediate camera coordinates
  ([[EXP-20260916-011 - Terrain camera range guard for horizontal bands]]).
- **What goes wrong.** A large added mesh (scene 485) passed the gate with
  emitted X [−3109, 7822], Y [−404, 3280] and a signed depth crossing zero.
  Independent wide arithmetic put 182 of the added tree's 506 vertices
  outside the signed 16-bit camera range at the sampled view (arithmetic, not
  a native trace). In
  hardware the result was large horizontal bands that changed as the camera
  moved forward.
- **What fixed it.** Splitting the geometry into complete faces above and
  below a height cut placed it in separate scene records. The first wide gate
  `0x0044D5EC` then rejected the out-of-range records at both captured views,
  and hardware walks through the same area showed no bands. The split kept
  the exact world-space visual faces and collision triangles. The executable
  was unchanged.
- **What did not.** Extending a signed-depth correction in projection changed
  only one batch's XY/RHW in native replay and left the bands in the real
  game.
- **Requirement (inferred from the above).** A scene record's vertices
  should stay within signed 16-bit camera-relative range whenever the record
  passes the wide gate; otherwise split the record so that the gate rejects
  the far part.

## Object rotation

[[PC animated clover authoring]] records the object Euler words and the
native sway matrices. EXP-20260914-003 adds:

- Disassembly `0x00449C5E..0x00449CBB` reads all three object Euler words,
  builds their matrix with `0x00463C80`, and combines it with the selected
  animation matrix. `0x00455710` advances the camera-composed sway matrices at
  `0x005C0300`.
- The Euler triple is the signed-short triple at object `+0x0C/+0x0E/+0x10`
  ([[PC LEVEL DAT static mesh]]); the Y word that EXP-20260914-003 and the
  clover note call "object+14" is therefore `+0x0E` (decimal 14, inferred from
  that layout), not the mesh pointer at `+0x14`.
- Changing only the Euler Y word turns an object; its X/Z lean, scale, opaque
  fields, mesh, materials and animation selector stay. For donors whose X/Z
  angles are about a half turn, an authored heading is subtracted from the
  native Y. This keeps their lean; it is not a claim that tilted Euler
  rotations commute with an upright world yaw.
- The culling centre has to follow the exact old and new matrices; 16 stored
  units of radius allowance covered fixed-point rounding.
- Replay of 3 donors × 5 headings × 17 animation phases: every heading
  projected differently, every animated arm moved, and selector-zero controls
  stayed invariant.

## End-of-file footer

[[PC LEVEL DAT prefix]] records that the final dword is an end-relative span
read by `0x0044BB70`, that appending data must move it, and that −1 means
absent.

- **Positive footer.** It must move by the appended payload length
  (EXP-20260914-010; covered by native relocation tests).
- **Training's −1 footer.** In the original Training DAT the final
  `FFFFFFFF` overlaps the mesh terminator of secondary records 14/15 (original
  mesh 114792..115058, end of file 115060). An appender that strips the final
  four bytes as a reserved footer therefore cuts the shared terminator, and
  the original mesh then reads appended object bytes as primitives. A separate
  footer has to be supplied first. The failure was traced to `0x0045B6C4` and
  repaired in hardware (EXP-20260911-002). This is a bounded Training rule,
  not a general footer interpretation for other levels;
  [[PC custom distant terrain]] keeps the terminator for the same reason.

## Free texture pages and borrowed textures

A face's texture page is `(tag >> 8) & 31`
([[EXP-20261012-007 - Unused disc content checked offline]]). A 4-bit page's
256-entry palette is 16 rows, one per 64×64 block (`(v/64)*4 + u/64`); a page
written with only some rows left faces on the other blocks flat white in
hardware (EXP-20260928-001), and the converter's 4-bit branch is traced in
[[EXP-20261018-009 - Four-bit page palette rows]].

- **Training.** Page 21 is unused in the original Training RAW
  (EXP-20260911-009).
- **LEVEL06.** Page 21 is unoccupied in the original RAW and page 22 is unused
  (EXP-20260914-012, EXP-20260915-001).
- **Level01.** The RAW has no page 21 (EXP-20261005-001; see
  [[PC boss level routines and creature transplant limits]]).
- **A borrowed original texture.** City Entrance (LEVEL04) `LEVEL.DAT` scenes
  854/856/858 draw the gold grain on page 2, UV rectangle (64,0)–(95,63), mesh
  offsets 325632/328464/331296, tag 0x0260. The page is packet 43417 of
  `LEVEL04/LEVEL.RAW` (EXP-20260911-009).
- **Copying pages.** A page copied whole into a free slot of another level's
  RAW kept its original pixels and palette, and every existing packet and
  suffix stayed byte-exact (EXP-20260911-009).

## Original LEVEL06 layout

LEVEL06 is progression 4, engine 6, "Level Four: Dandelion Flight"; folder
LEVEL04 is City Entrance ([[PC level roster and numbering]]). From
EXP-20260914-010 to EXP-20260914-012:

- **Census.** The original map has 593 primary and 100 secondary objects,
  17,093 faces and 60 pickup markers; collision is in
  [[PC terrain collision rules for modified levels]].
- **Shared ground.** Primary objects 6–17, 20, 21, 29 and 76 share ground
  geometry, so a change to one of them must clone the shared mesh first.
  1,448 of their faces face upward.
- **Wide secondary pass.** The original secondary (distant) scenery extends
  over stored Z −22600..17516, much wider than the detailed basin around
  Z −8250..2450, so much of what is seen from the basin is secondary
  scenery (EXP-20260914-011).
- **Water.** The basin's water is seven disconnected pool envelopes within
  four coarse basin outlines. The coarse basin floors are secondary records
  18, 25, 33 and 42.
- **Muting a record.** A record can be muted while keeping its original
  payload, using the established no-draw flags; see
  [[EXP-20260906-005 - Isolated authored terrain and platform spawn]] for the
  draw-kind rule.
