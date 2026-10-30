---
type: implementation
status: implemented-bounded
created: 2026-09-07
updated: 2026-10-29
evidence: [EXP-20260907-012, EXP-20260914-003]
tags: [implementation/modding, terrain/authoring]
---

# PC animated clover authoring

EXP-20260907-012 adds original Anthill three-leaf clover scenery to an
authored level as independent appended scene/object records.

## PC-confirmed evidence

Authoritative retail EXE SHA256:
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
Original Level01 DAT SHA256:
`786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`.
Donors are primary341 (large),397 (slender),384 (tilted), sharing geometry
at file offset178748/0x2BA3C:37 vertices,23 quads, including three leaf quads
using command0x62. Saved original-camera PC projection localizes these objects
against the visible clovers. Asynchronous original vertex-packet XYZW matches
were zero for these moving donors; do not claim a phase-matched packet capture.

Scene0x19 retains the scaled scenery path. At0x00449C93..0x00449CBB, object+25
low five bits select matrix `0x005C0300 + 32*((selector-1)>>2)` when nonzero;
zero uses the camera matrix. The three retained donors select13,13,1, using
matrix slots3/3/0. Original0x00455710 updates four camera-composed matrices.
Aligned disassembly, Ghidra queries,17 native animation phases and25 passive
original samples provide independent evidence. The native selector-zero
control stays geometrically invariant while the retained selector moves.
This is a bounded demonstrated native sway, not a new general wind model.

The EXP-20260907-012 compiler preserves the mesh, transform, material/UVs, depth/pass,
visibility bound, animation selector and unknown object bytes while appending
independent scene/object records. Existing pointers/footer use the demonstrated
PC relocation grammar, tested against original and modified DATs. No game
assets are embedded in source. The compiler adds animated decoration only:
no clover collision shell or actor logic is authored. Retail clover collision
behavior has not been established by this work. Read final offsets from the
completed DAT: later insertions rebase earlier ones.

## Authored heading successor

EXP-20260914-003 adds optional heading0–4095 through the native object+14 Euler word.
The three donor lean angles require the recorded sign convention; culling-center
rotation uses exact old/new native matrices, with16 units of rounding allowance.
The mesh and selector stay exact. Three donors, five headings and17 native phases
show distinct orientations with continuing sway, and selector-zero controls are
invariant. Live fixed-camera samples show both used animation slots changing.
