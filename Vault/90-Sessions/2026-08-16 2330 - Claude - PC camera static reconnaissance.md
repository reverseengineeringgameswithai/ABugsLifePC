---
type: session
date: 2026-08-16
agent: Claude
status: superseded-by-exp164
tags: [session, re/camera, research/coverage]
---

# PC camera static reconnaissance

## Goal

Open the camera coverage row, at the researcher's direction.

## Result

**Historical worker result: rejected by EXP-162 and corrected by EXP-164.**
[[EXP-20260816-161 - PC camera static reconnaissance]] is no longer live
authority for coverage or transform placement.

Unlike audio, the camera row has no string anchor and no import surface, so
there was nothing to follow. The D3DApp provenance and known TL-vertex sites
survive, but the transform conclusion does not: `0x00405FE0` transforms
locally from `0x0040605F`, and three known TL-vertex sites do not prove global
absence of Direct3D view state. Correct native tracing finds the two-source
selector through `0x00599C90` and `0x00455710` into matrix `0x005B58E0`.
The terrain census leaves four unmapped functions after the known City
dispatcher is removed; two enclosing functions read Flik position.

## Cross-port handling

The researcher suggested probing the PS1 vault. Its camera notes were read as
committed blobs at the registry commit and recorded in
[[XPORT-20260816-004 - Camera system shape]] as **hypotheses**, never as
confirmation — the policy is explicit that PS1 cannot confirm a PC fact, and
the researcher's word "confirm" was held to that line. PC instructions now
independently support the two-source/selector and render-consumed-transform
shapes; their PS1 semantic labels still do not carry over.

## Next

EXP-165 accepts the EXP-164 static correction. Retain manual PC controls as
Unknown rather than asserting there are none; a future separately authorized
read-only source/selector/input discriminator may classify the remaining
semantics.
