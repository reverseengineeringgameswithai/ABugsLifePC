---
type: experiment
id: EXP-20260905-004
date: 2026-09-05
question: Do authored ramp cells joining a deck to the banked box top let the original PC movement code carry Flik up onto the box and back down?
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Original PC instructions offline; one fresh isolated file-loaded Direct3D Wine copy with normal XTEST input and read-only capture
result: Yes; six paired routes through original movement entry 004AB1A0 and two normal-input live ascent/descent cycles pass deck -> ramp -> top -> ramp -> deck, top jump/landing and west step-off pass, and the closed-east-wall control blocks the same walk
created: 2026-09-05
updated: 2026-10-29
---

# Playable ramp and box area

## Summary

Authored ramp cells added to the EXP-002 banked box pair connect a broad deck,
a gentle ramp and the box top under the original PC movement code. Flik reaches
the ramp from the normal Level01 spawn, walks up onto the box without jumping,
turns around and walks back down. Two live cycles pass, followed by a normal top
jump/landing and a west step-off onto the deck. The closed-east-wall control
blocks the same walk, so the result is ramp access, not standing on an existing
box.

The test copy is `work/copies/EXP-20260905-004/game/`; it is a local test area,
**not** a replacement Level01 or a connection to the distant retail landscape.
The earlier EXP-003 source100/prop route is still separate and open. No
universal terrain, diagonal or material rule follows.

## Evidence and geometry

`reports/terrain/EXP-20260905-004.json` contains exact geometry/offsets, source
hashes, modeled deltas and states, live input/contact traces, captures' hashes,
loaded-byte checks and audits. The complete model report, including per-call
instruction/candidate/plane-sign observations, stays hash-pinned under
`work/experiments/EXP-20260905-004/offline.json`. Private images, assets and
prefixes are not in Git. Snapshot provenance is in
`reports/terrain/EXP-20260905-004-preservation.json`.

Reuse the exact EXP-002 alternate-4x4 pair, not a re-derived box:
TERRAIN.ALL `26f3e0235533419a80b2a0eff18f423fadc20617a6c2ed2be445abeae87b35d5`,
LEVEL.DAT `572d244f1cc053ef29d2c343e4311a6ff20237c2259c5e84867bade53d57c247`.

Stored-coordinate layout:

| Piece | Extent |
| --- | --- |
| Broad deck | X4000..8300, Z13000..18100, visible Y-3200 |
| Banked box top | X5100..5750, Z15550..16250, visible Y-3392 |
| Ramp | X5750..7150, Z15550..16250, rising192 over run1400 |

Positive Y is downward. The banked collision-to-visible vertical offsets are
retained: floor/top collision is visibleY-96; side bottoms extend to deckY+96.
The broad deck continues beneath the box/ramp as a catch floor, not a newly
retessellated Boolean union. The ramp and top meet at identical rim coordinates;
the ramp foot meets the broad deck plane.

Source99 origin remains (7420,-109,13471), payload offset43924, capacity4460.
Fourteen marker-1/single-cell groups plus terminator occupy618 bytes. Deck and
top primitives are retained; the old east wall is replaced by two ramp triangles,
with expanded north/south side profiles and the west wall retained. Only the
established normal, vertex/delta and admission-bound fields are encoded. All
surrounding source bytes remain unchanged. Exact 32-byte-cell offsets and
vertices are in the report.

Primary160 still uses object18672, scene record8580 and geometry113136. Its
sixteen alternate-diagonal top quads, corner/UV pairings and vertex suffixes
remain intact. Moving the lower east rim and subdividing side/ramp quads produces
61 vertices and49 quads (1526 bytes), with matching raised-surface rims/midrows.
The deck itself is not split to match every lower rim vertex.

This exceeds the older first-group-only1336-byte budget, but fits the2234-byte
**complete known mesh stream** independently checked in EXP-003 through the
original ffff terminator at115368. No unidentified adjacent allocation is used.
The new stream is also walked by the original PC consumer with emission disabled.
This proves bounded stream traversal, not every renderer view. Object depth
byte+0x12 remains0; other instance/object/material fields and bytes beyond the
new prefix are preserved.

Authored TERRAIN.ALL SHA-256:
`1ff3af9f0b5b2c2957bde8e877e1d988054455f3e1be18f8ea0e6cb57875d16b`.
Authored LEVEL.DAT SHA-256:
`54d1ae4d96a4d926b806584cc669e791c3f6565688ec4aa491a987b0c2f56aab`.

## Original-PC instruction gate

Use the banked original movement entry004AB1A0 and reference loader. Three
Z lanes (15675,15900,16125 stored) at each horizontal step speed512 and900 world
units give six paired routes, twelve directional legs. Each leg has explicit
source99 cell transitions deck -> ramp -> top or top -> ramp -> deck. All reach
the expected surface, finish with native flags[1,1], and have longest airborne
runs of1. Representative top Y is -108547..-108544; deck Y -102403..-102400.

The natural-spawn approach, ramp/top landings, settling and west step-off also
pass. The unchanged banked closed-east-wall control blocks the same intended
walk onto the top, discriminating actual ramp access from merely standing on
an existing box. This is synthetic motion through original instructions, not an
input movie or a replacement full-game physics model.

One preliminary adapter call used deckY-2048 and failed the banked landing
assertion. The gate uses EXP-006's existing deckY-1024 landing seed. This is a
recorded setup rejection; no candidate geometry was changed for it.

## Fresh runtime comparison

All2251 staged files are hashed against the source tree; only TERRAIN.ALL and
LEVEL.DAT differ. The runtime image is the guarded auto-hardware cache SHA-256
`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`, distinct
from the original offline instruction image. Six hardware markers and both
R-drive identities pass before input. The exact PID/start/group/cwd/window and
compositor socket peer are checked. Native loaded collision and render prefixes
match staged files before and after the route.

The fresh owned group is271112; Gamescope271129 uses gamescope-0. Launch,
discovery and close receipts pin all process identities. A private copied prefix
maps R: only to this playable game copy; historical mappings are unchanged.

Normal spawn is near (197108,-102400,492895). Three ground approach legs reach
XZ (197091,480000), (240000,480000), then (240000,508800). Each ascent targets
(173600,508800); descent returns toward(240000,508800). Each leg is capped at
8 seconds with guaranteed key releases and deck/below-floor guards.

| Live leg | Samples | Observed surface sequence | Release Y |
| --- | ---: | --- | ---: |
| uphill1 | 59 | deck -> ramp -> top | -108546 |
| downhill1 | 60 | top -> ramp -> deck | -102400 |
| uphill2 | 52 | deck -> ramp -> top | -108546 |
| downhill2 | 62 | top -> ramp -> deck | -102401 |

The maximum measured below-floor residual across those legs is0 world units
against the upper applicable source99 plane+3200; the guard does not mistakenly
use the lower catch deck underneath the ramp. Live contact globals are not a
newly validated grounded-bit contract. Feedback inputs, post-release coasting,
state reads and screenshots are asynchronous, not frame-matched.

An additional normal ascent precedes Shift_L held0.15seconds and a2.5-second
jump trace:124 samples, Y range-121409..-108545, settled top contact at
(176082,-108546,510770). The west step-off returns to deck cell43980 near
(151592,-102400,508649). The packet totals554 sampled route/jump states and
13 native captures, including menus. These are finite contact/view examples,
not an all-view occlusion guarantee. Unchanged retail plants/scenery remain.

No live memory writes, teleport, ptrace, STOP/CONT, register reads, save states
or debugger control were used. No PS1 evidence was consulted.

## Validation

New targeted regressions:19 passed in17.29seconds. The seven-file terrain gate
(the original five files plus floor-patch and play-area regressions):118 passed
in26.51seconds. Bounds/overflow rejection, synthetic cell fields, two-file byte
preservation, top/opaque-field preservation, mesh-edge conformity and original
movement controls are covered. **No R2q or full `make check` run.** Prelaunch
and post-close unrestricted session audits are clean. Originals and prior
checkpoint snapshots remain unchanged.

General terrain authoring, arbitrary layout coverage and EXP-003's
prop-confounded retail seam route remain open.

Links: [[EXP-20260905-002 - Box movement and occluding-view validation]],
[[EXP-20260905-003 - Shared floor return discriminator and stitched patch]],
[[New-level authoring roadmap (terrain, collision, materials)]],
[[2026-09-05 1804 - Codex - Playable ramp and box area]].
