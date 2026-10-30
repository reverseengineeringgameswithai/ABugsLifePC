---
type: experiment
id: EXP-20260911-014
date: 2026-09-11
binary_sha256: f55c3612f60fb1fba373c55d8cab6afcac96cf00d4156c542963234aa58b7059
environment: Owned muted Wine Gamescope hardware Direct3D; original PC code on read-only captured state
question: Why do distant flowers remain visible when closer custom Training walls disappear?
result: Flowers are panorama artwork; the turned entrance view exceeds the finite 2x world distance limits
status: confirmed-bounded
created: 2026-09-11
updated: 2026-09-11
tags: [re/rendering, modding/training]
---

# Training flower panorama and wall cutoff

> Target clarification: [[EXP-20260911-015 - Training grass uses secondary background geometry]] identifies the user's cropped grass strip
> as secondary15. This note's panorama and13-primary-plant measurements concern
> other objects; they do not explain that grass strip's visibility.

**Confirmed:** the distant flower strip is Training's sky panorama. It is a
256×136 indexed image, decoded type36 record29 at RAW offset289474, SHA256
`2a5fd67af8f9cca8cdfbeee4fadf4867940d8c742d2f8202b26d075e0acdd54d`.
Its petals/stems match the user's forward and reverse hardware views. This
identifies the distant strip specifically, not every nearby grass/flower mesh.
For the painted flowers, the secondary-DAT hypothesis is superseded by the
decoded image/native panorama execution. The later cropped grass target uses
secondary scenery, a distinct engine pass identified in EXP015.

## Current runtime and input

Same muted EXP013 game91321/start5734777, group91091, hardware path. EXE SHA256
`f55c3612f60fb1fba373c55d8cab6afcac96cf00d4156c542963234aa58b7059`;
Training DAT `d5ed5105a41814ae7a0acfc1d25793eb589428494373dd98046a67542a995bcc`.
No launch/close, external RAM write, suspension or project/build change.
Read-only captures bracket the key observations; they are non-atomic.

One requested1ms Down XTest tap acknowledged in1.073017ms. Sampled Flik XYZ,
camera matrix and translation remain unchanged. The user then explicitly
approved one35ms tap; acknowledgement35.092451ms. This turns the view from
panorama phase6300 to8337. Flik moves from(17990,-21756,278757) to
(18041,-21688,278964). No further gameplay keys are sent. Acknowledgement time
is not proof of exact input duration as consumed by the game.

## PC evidence

Retail SHA256 `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
Resident code equals retail in recorded panorama and distance-gate regions.
Original00405410 scrolls the panorama by camera heading;00404410 emits one
screen-space quad (4 vertices/6 indices). Six copied-state native cases cover
both captured views, each unchanged, translated and with stock distance values.
Changing copied Flik/camera XYZ or distance globals leaves that view's complete
panorama submission identical. Turning changes panorama phase/UVs. Thus its
apparent distance is artwork, not ordinary world-geometry distance.

The turned view's custom walls use existing0x59 far-group flags with2304/3328.
The quad cutoff is13312 stored units. Scene298 passes admission but rejects
21/24 tested front quads at0045CF63..0045CF89 (depth range13222..16166).
Scenes299..307 fail the outer distance branch0044D5EC. Forced single-scene
projection shows, for example, scene300's16 front quads at18867..19893; all
would also exceed13312. Forced results for rejected scenes do not imply live
submission. This entrance view is farther from the garden end than EXP013's
platform benchmark. The2x change fixes that earlier view but has finite reach.

## Evidence and limits

Asset-free report `reports/render-distance/EXP-20260911-014.json` hashes private
captures, native probe scripts/results, code checks, decoded image and key
receipts. The legacy extractor's exact12-byte trailer check fails on this mod's
9-byte trailer; all decoded records pass original-decoder bounds/coverage. The
trailer is retained as unparsed evidence, not silently rewritten or normalized.

Native replay is CPU evidence, not GPU emulation. No further distance increase,
background wall proxy, performance trial or design bank is installed. A visual
wall proxy could be investigated separately; it would need camera/parallax and
occlusion validation. [[PC general render distance]] retains EXP013's measured
scope. [[2026-09-11 - Codex - Explain distant flowers and Training walls]] owns validation and closure.

## Follow-up: actual 3D plants in the initial direction

The user's follow-up asks whether the initial foliage fits2x. **Confirmed at
native admission/emission scope:**13 scaled primary plant meshes whose projected
bounds overlap the opening (screen X150..365/Y195..247) pass admission and emit
geometry. Scenes124..129,131..135,175,205 have tested front-quad depths
8185..11982, below their13184 cutoff: `4 * (3328 - 8 * 4)` including their
original object bias. Their far-group flags remain unchanged. These selected
meshes emit zero vertices at stock distance in the copied-state comparison.

This is distinct from the painted flower strip, which has no ordinary world
distance. Earlier panorama identification does not classify every visible plant
as backdrop. The projection overlap selects candidates; no new GPU occlusion
proof or exhaustive grass inventory is claimed. `initial-foliage.py` and
`initial-foliage.json` in the private EXP014 packet are hashed by the report.
No fresh live access, input, write, settings change or benchmark occurs.
