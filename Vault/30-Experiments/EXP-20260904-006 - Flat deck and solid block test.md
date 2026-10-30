---
type: experiment
id: EXP-20260904-006
date: 2026-09-04
status: completed-bounded
question: Can an isolated flat deck and obvious raised block test authored collision without the native spawn slope?
environment: Fedora 44; Wine 11 Staging; Gamescope; accepted auto-hardware Direct3D build
result: flat traversal and two live jump-off-return cycles pass; earlier slope-patch defect remains unresolved
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
created: 2026-09-04
updated: 2026-09-05
tags: [re/experiment, re/collision, re/rendering]
---

# EXP-20260904-006 - Flat deck and solid block test

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


## Correction and bounded result

The user reported falling through EXP-005's patch when walking forward and back,
and difficulty distinguishing its small lift from the native Level01 slope.
This is failed manual acceptance, with no captured numerical trajectory of that
reported failure. The exact cause is **unknown**. EXP-005's measured height and
pixel effects remain valid; they did not establish reliable reverse traversal
or a complete grouping. Do not call that patch fixed or generally usable.

**Confirmed for this new fixture:** a flat deck at Level01's normal spawn X/Z,
well above its native ground, supports original and live movement at constant
height. A clearly raised rectangular block has top and side collision. Original
instruction controls remove those responses when the new top or sides are
removed. Two live jumps land on the block and both departures land on the deck;
return approaches stay on the deck and are stopped by the side. Both loaded
collision and render prefixes match the authored files.

This is a fresh synthetic test fixture, not a repair of EXP-005's shared edges
or a generalized renderer/collision grouping algorithm. Other native objects
remain and can overlap parts of the deck. The deck's finite outer edge is open;
walking off it intentionally leaves the fixture.

## Authoring and evidence

`scripts/terrain-deck-probe.py` reuses existing TerrainAll and LevelDat parsers,
EXP-002/003/004's original loader/movement reference, and R1's mesh grammar.
No PS1 comparison, new runtime wrapper framework, or movement reimplementation.

All coordinates below are stored units (world coordinate scale32). The deck is
X4000..8300, Z13000..18100, visible Y−3200. The block is X5100..5750,
Z15550..16250, visible topY−3392: a distinct6,144-world-unit rise. Collision
floor/top planes are96 stored units above the visible surfaces; the original
floor contact response places Flik approximately on the visible Y. Block sides
extend from that collision top to96 units below the visible deck. These offsets
are part of this tested fixture, not a proven universal collision-skin rule.

Two fixed spans are replaced, retaining file lengths and all other bytes except
one explicit culling-center update:

- TERRAIN.ALL source99 payload begins43924. Replace530 bytes with12 one-cell
  groups: two floor triangles, two top triangles and eight side triangles,
  followed by the negative terminator. Directory/source records and remaining
  payload bytes stay unchanged. Each cell has axis-aligned normal, directed
  edges, explicit group X/Z bounds and enclosing cell X/Y/Z admission bounds.
- LEVEL.DAT primary160 geometry begins113136. Replace394 bytes with24 vertices,
  one tag`0x60` group of six quads, and terminator`0xffff`. Vertex attributes and
  face fields use the original mesh's templates. Only scene record8580's first
  three dwords additionally change, to center `(6150,-3296,15550)`; original
  positive radius4442, flags and pointers are retained. Other meshes are unchanged.

Static terminator evidence: retail `0x0045A8B0` compares the next group word
against−1 and `0x0045A8B4` exits to`0x00460266`. Vertex count and12-byte stride
are the previously confirmed R1 grammar. Raw instructions are retained in
`reports/terrain/EXP-20260904-006-renderer-head.asm`. This exercise validates
one new single-group stream, not every multi-group/tag variant.

The collision plane/edge/winding and signed admission fields are the previously
bounded original consumers at`0x004AA4D0` and`0x004AB1A0`, documented in EXP-001/002.
The new independent geometric construction is checked by those unchanged
instructions after real loading/bucket initialization. All12 groups remain in
source99; no new source records or reserved dynamic descriptors are introduced.

| File | SHA-256 |
| --- | --- |
| Retail TERRAIN.ALL | `62f3b73f21630eb19c04e585a92e1f3e32a76fdcb6ec36bae18f9c1ec3a2a868` |
| Deck TERRAIN.ALL | `26f3e0235533419a80b2a0eff18f423fadc20617a6c2ed2be445abeae87b35d5` |
| Retail LEVEL.DAT | `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53` |
| Deck LEVEL.DAT | `364d665aa2935f1a7aed3694e849ab6bc292af376fde33c44ff4ddbbac967bae` |

Retail executable hash is in frontmatter. The live auto-hardware build is
`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`.

## Original-instruction controls

Five cases in the report establish contact by landing with flags initially0:

- Flat-deck round trip returns exactly to`(208000,-102403,464000)` and keeps
  Y−102403 throughout40 movement steps.
- Approaching the block at deck height stops X at or above its right side184000;
  reversing moves away along the deck.
- Landing on top yields`(173600,-108547,508800)`. Leaving right drops to the
  deck; returning stops at`(184540,-102401,508800)` outside the block.
- Removing only side groups allows entry inside the block footprint at deck
  height: final`(174591,-102402,510397)`.
- Removing only top groups prevents the initial top landing; subsequent gravity
  steps land on the retained deck atY−102403.

These are synthetic motion requests through original instructions, not complete
player-input/gravity replay. The controls deliberately retain the broad deck as
a catch floor and leave all other source records untouched.

## Live observations

The earlier user floor-play session was closed with pinned process identities
and a clean audit. Scientific EXP-006 game PID/start38125/934393, group37881,
reached Level01 with all six required hardware markers, owned XTEST focus and
mapped movement-code checks. Source99's complete530-byte new collision prefix
and primary160's394-byte render prefix (including faces and terminator) match
the staged files. The scene center/radius/flags also match loaded bytes. Read
pointers are descriptor99+0x10 and LEVEL.DAT base global`0x005BA240`.

Flik starts at`(197108,-102400,492895)` on the flat deck. Up approaches the block;
Up+Shift_L jumps onto it. Down leaves it; subsequent approaches return without
falling through the deck. Recorded landing endpoints:

| Event | Current XYZ at `0x0059D910` |
| --- | --- |
| First top landing | `(178822,-108545,515160)` |
| First return to deck | `(209467,-102402,487124)` |
| Second top landing | `(182185,-108546,511196)` |
| Second return to deck | `(206687,-102400,492371)` |

The last two side/return settle windows remain at deck height within the small
integer contact variation. Camera-relative input means reversing key names is
not an exact world-path replay; full traces are retained. An additional camera
turn moved farther from the starting view, so the scientific arm was closed
cleanly and a fresh user handoff was launched from spawn.

One live scientific arm is claimed, with two repeated jump/return cycles.
Negative controls are offline original-instruction runs, not live negative arms.
No live memory writes, teleport, save states, debugger attachment or freezing.
No R2q/historical mappings changed; CAP-010 and independent audit remain open.

## Artifacts, checks and next step

- `reports/terrain/EXP-20260904-006.json`:757,745 bytes;
  SHA-256`4112cc7f8400f006319d603501326b1af115bccee33888c4e8cfc6022a94a91c`.
  Contains exact authoring metadata, five offline cases, live traces, source
  hashes, screenshot/receipt locators, owned process, clean close audit and limits.
- Companion renderer assembly, final runtime-operator and design snapshots in
  `reports/terrain/`. The operator gained deck/drive actions during this work;
  snapshots are final versions, not immutable source archives for each action.
- Raw receipts/screenshots and log snapshot under`work/experiments/EXP-20260904-006`;
  authored assets under`work/copies/EXP-20260904-006/deck`.
- 188 focused tests pass in36.66s, including11 new deck cases. Full `make check`
  and independent review were not run; no commit was made.

The user subsequently confirmed block landing/contact, but reported a visibility
problem while standing on the lower deck behind it. See [[EXP-20260904-007 - Deck visibility and inherited depth offset]]
for the user images, read-only corroboration and unlaunched depth-offset candidate.
Keep this fixture as a repeatable collision testbed. Resolve the old
slope patch's shared-edge/return failure separately before resuming general
terrain deformation or declaring its grouping correct.
