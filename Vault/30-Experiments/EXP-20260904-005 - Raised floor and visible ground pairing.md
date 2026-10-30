---
type: experiment
id: EXP-20260904-005
date: 2026-09-04
status: completed-bounded
question: Can a raised collision floor support live movement and be paired with visible ground?
environment: Fedora 44; Wine 11 Staging; Gamescope; accepted auto-hardware Direct3D build
result: six-cell height translation and fixed visible-ground companion confirmed; boundary stitching open
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
created: 2026-09-04
updated: 2026-09-05
tags: [re/experiment, re/collision, re/rendering]
---

# EXP-20260904-005 - Raised floor and visible ground pairing

## Subsequent EXP-003 result (2026-09-05)

[[EXP-20260905-003 - Shared floor return discriminator and stitched patch]]
reproduces the rigid EXP-005 return fall numerically and with normal live input.
The original-instruction witness distinguishes a vertical discontinuity and
entry from beneath a one-sided plane from an XZ gap or Y-window-only cause. A
connected six-cell star with paired render heights passes finite modeled and
live return paths. This is a successor experiment, not a change to this original
fixture or a universal authoring rule; its prop-confounded and blocked routes
remain explicitly open. Earlier unresolved wording below describes this note's
historical checkpoint, not the new experiment's result.


## Result and scope

**PC confirmed, bounded:** changing six Level01 collision-cell origins raises
the original-instruction landing/walking response and live spawn Y by exactly
2,048 world units. A nearby 17-vertex LEVEL.DAT edit also changes visible ground
under an identical camera and actor position. Restoring only LEVEL.DAT restores
all 21,630 pixels in a selected static ground region; the paired edit changes
12,057 of those pixels. This supplies a fresh visible-ground causal example on
the accepted auto-hardware build, independently of the banked R2q procedure.

This is a rigid floor-group translation and a fixed visual companion. It is
**not** a seamless ramp, general terrain writer, full geometry/collision join,
independent audit, or retail-build R2 closure. The render mesh has extra vertices
and different boundaries; surrounding render faces blend toward unchanged
vertices while collision retains a step. Nearby prop mesh128 is unchanged.

## Authorization and reused evidence

The user confirmed EXP-004's barrier in person, then authorized the proposed
raised-floor/ramp and runtime step with “okay, go for that.” The completed user
play session was closed before these new arms, with a clean audit. Its close
receipt is `work/experiments/EXP-20260904-005/user-session-close.txt`.

Reuse EXP-001/002 original-instruction loading/movement, EXP-003 grounded contact,
EXP-004 scoped input/read operator, the existing height model, and R1's decoded
static-mesh reader/setter. No PS1 source was consulted. No historical R2q arm or
baseline-prefix mapping was used or changed. No live memory writes, teleport,
save-state operations, breakpoints or process freezing occurred.

## Files and exact edits

Retail executable SHA-256:
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
Live auto-hardware executable SHA-256:
`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`.

| File | SHA-256 |
| --- | --- |
| Retail Level01 TERRAIN.ALL | `62f3b73f21630eb19c04e585a92e1f3e32a76fdcb6ec36bae18f9c1ec3a2a868` |
| Raised TERRAIN.ALL | `0b808506390bed5ab3241e0a600a05a9df38726e18e38acd367323259fbc14a6` |
| Retail Level01 LEVEL.DAT | `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53` |
| Paired LEVEL.DAT | `6f36981636766ae6af52e65b13af53a862985d47dfce835c59a1a7ef351d93e9` |

TERRAIN.ALL source99 is kind6, non-template/non-clone, with payload offset43924.
Group47640 is204 bytes: 12-byte header plus six32-byte cells. At each cell+8,
subtract64 from signed h0; the cells and original values are:

| Cell offset | Original h0 | Raised h0 |
| --- | ---: | ---: |
| 47652 | -1 | -65 |
| 47684 | 53 | -11 |
| 47716 | 55 | -9 |
| 47748 | 90 | 26 |
| 47780 | 56 | -8 |
| 47812 | 125 | 61 |

Only these six two-byte fields may change. Normals, edge vectors, X/Z bounds,
relative Y admission windows, source directory and unknown bytes are preserved.
The original height consumer `0x004ACC3E–0x004ACC7D` uses h0 in plane height;
movement's relative Y admission window at cell+0x1c/+0x1d is read relative to h0
at `0x004AB527–0x004AB547`. A rigid Y translation preserves those relationships.
This operation adds no vertical side triangles and does not weld adjoining cells.

The visual fixture subtracts64 from signed vertex+2 in primary static meshes:
160 vertices8,9,10,11,15,23,27,36; 213 vertices107,108; and
280 vertices26,27,28,29,96,97,103. Exact field offsets and expected values are in
the report and `scripts/terrain-floor-visual-fixture.py`. Existing guarded
`LevelDat.set_static_mesh_vertex_component` performs each edit. Objects have
zero rotations. Selection began with object XYZ plus local vertex XYZ near the
six collision triangles, including extra render vertices inside the patch.
The approximately+100 stored Y separation is **descriptive inference**, not a
confirmed collision-offset generation rule or a general coordinate matcher.

## Original-instruction results

`scripts/terrain-floor-authoring-probe.py` constructs the unchanged EXP-002/003
reference with explicit original/modified source bytes. Each arm establishes
contact by an original landing call, then takes75 synthetic motion steps
`(-900,512,700)`. This is not a live input replay or a full player/gravity model.

- Spawn floor plane changes from−336 to−2384.
- Landings are `(196955,2755,492920)` and `(196955,707,492920)`, flags1/1.
- Through step22, X/Z and contact flags match exactly and Y differs by−2048.
- Both lose contact when leaving the patch at step22. Retail lands on unchanged
  cell47544 at step23; the raised arm remains airborne at23/24, then lands on
  that same cell at25. The extra drop is explained by the raised surface.
- An unrelated original grounded-floor case is identical between the arms.

The scoped writer rejects unsupported kinds, clones/templates, non-upward floor
normals, bad indices/types, malformed payloads, int16 origin overflow and signed
world-Y overflow. Synthetic preservation/inverse tests and supported groups in
both Level01 and Level03 are exercised. Existing parsers remain unchanged.

## Live comparison

Fedora44, Wine11.0 Staging, Gamescope, Direct3D640×480, isolated EXP-005 prefix.
Every arm has the six required hardware markers, guarded process identity,
owned nested display/window, and mapped movement-code verification. Normal
navigation is Training carousel → Right → Return → Level One title → Return.
Movement uses Up; jump uses Shift_L held approximately0.15s. All process memory
is read-only. Raw receipts, screenshots, game logs, prefix and copied assets
remain under `work/experiments/EXP-20260904-005/` and
`work/copies/EXP-20260904-005/`.

| Arm | Game PID/start | Group | Files differing from retail control |
| --- | --- | --- | --- |
| raised | 32464/767931 | 32221 | TERRAIN.ALL |
| control | 33031/784354 | 32787 | none |
| paired | 33610/795574 | 33366 | TERRAIN.ALL and LEVEL.DAT |
| raised2 | 34698/811665 | 34445 | TERRAIN.ALL |

All2,251 file paths are compared per arm, excluding the game log. The four
scientific arms each closed with clean process/sink/session audits.

**Collision:** descriptor99 at `0x007F4590 + 99*48`, payload pointer+0x10,
leads to the exact204-byte edited group in every raised arm and the original
group in control. Flik current XYZ at `0x0059D910` starts at
`(197091,686,492897)` raised versus `(197091,2734,492897)` control.
In the initial Up walks,41 raised samples match a control sample at equal X/Z
(25 distinct positions, through approximately0.816s); every Y difference is
−2048. Equal-XZ matching avoids treating wall-clock sample indices as game ticks.
Both walks proceed beyond the patch to later terrain descriptors. The offline
contact transition gives the explicit edge/drop discriminator; live traces alone
do not establish an exact grounded-bit interpretation.

**Jump:** paired and raised2 execute a stationary jump and settle on source99.
Their final25 samples respectively hold `(196449,706,493272)` and
`(196398,705,493315)`. Apex Y differs (−10834 versus−12178); approximately timed
key holds do not prove deterministic identical jump inputs or trajectories.
Both subsequently walk across the level. Do not silently equate those arcs.

**Visible ground:** R1's static chain is scene+0x10 → object+0x14 → vertex
array; original dispatcher reads/calls at `0x00449B2C/0x00449B32` reach
`0x0045A7F0`. In paired and restored arms, live scene/object pointers and the
complete vertex arrays of all three meshes match the staged files. The measured
LEVEL.DAT base is6596791 (`0x0064A8B7`); read-only global `0x005BA240` agrees in
the restored arm. The unchanged static consumer plus this live pointer/data and
frame intervention establishes the bounded link; no live draw-PC trace is claimed.

Raised, paired and raised2 stationary captures all have exactly the same current
XYZ,18 camera-matrix bytes at `0x005B58E0`, and translation at `0x005BDB8C`:
`(219643,-14938,475235)`. In rectangle `[24,350,230,455]`, raised versus raised2
has0/21,630 changed pixels; raised versus paired has12,057/21,630 changed pixels.
The rectangle is foreground ground left of Flik and excludes the large stalk.
It was selected after seeing the first two arms, before the restored capture;
this is exploratory localization, not a blinded preselected mask. Animated
actors elsewhere differ; whole-renderer-state equality is not claimed.

## Artifacts and validation

- `reports/terrain/EXP-20260904-005.json`: asset-free offline steps, live traces,
  exact ownership, loaded-byte hashes, file comparison, screenshots/receipt
  hashes, visual region counts, limitations and test command/output.
- `reports/terrain/EXP-20260904-005-runtime-operator.txt`: final operator source
  snapshot; mesh/jump actions were added after the first two arms. Receipts
  retain each actual command; this is not an immutable per-action source archive.
- `reports/terrain/EXP-20260904-005-runtime-design.txt`: initial bounded plan
  and dated-order render/region extensions.
- `scripts/terrain-floor-authoring-probe.py` and
  `scripts/terrain-floor-visual-fixture.py`: reproducible fixed fixtures; optional
  writes require a new file under work/copies and never overwrite.
- **177 focused tests pass in32.94s**, including28 new floor/visual cases. Full
  `make check` was not run; no commit was made. Lightweight gates are recorded
  in the session note. No independent review is claimed.

Report:673,440 bytes, SHA-256
`ff6acfb9aa81fea8f2f5f1425ee592d291ddd4abedc3fe3cb0a727e51e362cbe`.

## Subsequent manual failure report

In the handed-off paired version, the user reports that walking up and then back
makes Flik fall through the floor. They also report that the pre-existing slope
makes the small visual lift hard to distinguish. This is a failed manual
acceptance case, not yet an independently reproduced numerical trajectory.
Earlier forward walks, jumps and pixel effects do not establish reverse traversal
or a fully reliable grouping. EXP-006 tests a flat deck and clearly raised block
as a separate fixture; it does not retroactively fix or validate this patch.

## Next discriminating experiment

Use this verified spawn location and mesh mapping to build a connected floor
patch whose boundary treatment agrees in both datasets. Explicitly enumerate
shared collision corners and all touching render faces/duplicate vertices,
including nearby prop attachments before deciding which should move. Choose a
small gentle ramp, recompute changed normals and bounds from demonstrated PC
rules, then test landing, uphill/downhill crossing and boundary transitions in
the original routines and live game. Keep this rigid fixture as the regression
baseline; do not restart barrier/loader or unrelated R2q calibration research.
