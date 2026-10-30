---
type: cross-port-comparison
id: XPORT-20260816-004
status: completed
confidence: medium
pc_binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
external_source_id: SRC-PS1-ABL
external_commit: 1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51
external_paths:
  - ObsidianVault/Canon/Systems/SYS_camera.md
  - ObsidianVault/Canon/Systems/SYS_cinematic_camera.md
pc_evidence:
  - EXP-20260816-161
  - EXP-20260816-162
  - EXP-20260816-164
  - EXP-20260816-165
  - EXP-20260915-005
external_evidence:
  - ObsidianVault/Canon/Systems/SYS_camera.md
  - ObsidianVault/Canon/Systems/SYS_cinematic_camera.md
created: 2026-08-16
updated: 2026-10-02
tags:
  - re/cross-port
  - re/camera
---

# XPORT-20260816-004 - Camera system shape

## Bounded question

The PC camera row has no string anchor and no import surface, so a static
census has nothing obvious to grep for. What *shape* did the camera take on
PS1, and which of those shapes give testable PC hypotheses?

The researcher observed on PC that **the camera simply follows Flik** with no
player-facing camera controls. That is PC observational evidence and is
recorded as such; everything below from the PS1 side is a hypothesis to test,
never a PC fact.

## PS1 observations (external, not PC evidence)

Read as committed blobs at commit `1186eb6e`; summarised in ABLPC's own words,
not reproduced.

- A per-frame **follow update** exists as its own function, which calls the
  movement integrator, a heading helper, and a **region query** that
  determines which collision region the camera is over.
- The world-to-view transform is a **3x3 rotation matrix** in fixed point,
  with a horizontal zoom baked into it so it is not orthonormal, and it is
  **mirrored into main RAM every frame** at two nearby addresses.
- There are **two camera sources**: the gameplay follow camera and a shared
  **setpiece/cinematic** block used for scripted moments. A per-frame
  **selector** picks between them on a flag bit and writes the winner to a
  single "current camera" location that the renderer reads.
- The setpiece block is one record with position/target/derived vectors, a
  phase field, and a caller-supplied flags field.

## PC hypotheses this seeds

Each is a search strategy, not a claim:

1. **The PC camera may query terrain or regions.** PC already has the terrain
   height query mapped (`0x004AC460` via thunk `0x00401659`,
   `0x004ACA60` via `0x00401717`). A camera would show up as an unmapped
   caller of those.
2. **There may be two camera blocks and a selector**, with one "current
   camera" the renderer reads — so look for a pair of similar structures plus
   a per-frame chooser, not a single global.
3. **There should be a per-frame world-to-view transform** the render path
   consumes.

## What PC evidence says so far

`EXP-20260816-161`, corrected by EXP-162/164, tests hypothesis 1 directly.
The terrain-height thunk has **seven** call sites: two known reset consumers,
one known City dispatcher, and four unmapped enclosing functions. Exactly two
of the four unmapped functions also read Flik's live position, but neither
query is proved to use Flik's live point. This narrows the terrain side without
identifying a camera.

PC evidence independently supports the structural parts of hypotheses 2 and
3. At `0x0041B8C0`-`0x0041B966`, bit 0 of `0x0059A5EE` selects one of two
position/angle layouts into common block `0x00599C90`. `0x00455710` turns the
common block into origin `0x005BDB8C` and 3x3 matrix `0x005B58E0`; renderer
`0x0044D430` consumes them at `0x0044D4C1`/`0x0044D4F0`. This is PC-static
evidence, not confirmation imported from PS1.

The PC's three known `D3DVT_TLVERTEX` submissions mean those paths use
game-code transforms; they do not prove universal absence of Direct3D view
state. Builder `0x00405FE0` performs its own fixed-point transform beginning
at `0x0040605F`. The PS1 GTE implementation remains structurally different,
and the PC source roles “gameplay” and “setpiece” remain Inferred.

## Differences already visible

The PS1 vault documents **manual camera controls** as a system. The researcher
reports none on PC. That is a genuine candidate port difference, but it is not
established: the PC side has only the researcher's observation, and an unused
or undiscovered control path would look the same. It is recorded as an open
question, not a difference.

## Discriminating PC experiment

First independently audit the EXP-164 static correction; no runtime arm is
needed to establish the bounded structural chain. After acceptance, the
smallest remaining PC discriminator is read-only: observe both source blocks,
selector bit `0x0059A5EE & 1`, and the common block while ordinary follow and
a known scripted view occur, then separately trace DirectInput consumers for
manual-camera state. This may classify the PC roles; PS1 names remain
hypotheses regardless.

## Later PC evidence (2026-10-02 audit pointer)

- [[EXP-20260816-165 - Independent PC view-chain correction audit]] accepted
  EXP-164, so the first step above is done.
- EXP-20260915-005 confirms one scripted
  use on PC. During a telescope tour, bit 0 of `0x0059A5EE` routes source
  `0x0059A5C0`, driven by DAT paths 11..13, into common view `0x00599C90`.
  Return restores the Flik-follow source `0x0059DD90`. See
  [[PC camera view-transform chain]].
- That is PC evidence for one event only. The general PC source roles, other
  scripted events and manual controls stay open under `KU-066`. The PS1
  observations above still confirm nothing on PC.
