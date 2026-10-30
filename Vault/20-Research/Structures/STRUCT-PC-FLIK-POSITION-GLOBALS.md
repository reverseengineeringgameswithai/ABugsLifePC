---
type: structure
id: STRUCT-PC-FLIK-POSITION-GLOBALS
status: confirmed
confidence: high
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
base_address: "0x0059D910"
evidence:
  - EXP-20260815-128
  - EXP-20260815-130
related:
  - FUNC-97C95BA5572D-00432930
created: 2026-08-15
updated: 2026-08-15
tags:
  - re/structure
  - re/gameplay
---

# PC Flik position globals

## Summary

The exact retail PC executable retains Flik's current signed X/Y/Z in one
global triple, a preceding distinct position in a second triple, and an
auxiliary/reset-coordinate value in a third. The roles are separated by a
controlled Training jump, ordinary ground movement, and static reads/copies in
the same binary.

## Layout

| Address | Width | Confirmed role |
| --- | --- | --- |
| `0x0059D910` | signed 32-bit | current Flik X |
| `0x0059D914` | signed 32-bit | current Flik Y |
| `0x0059D918` | signed 32-bit | current Flik Z |
| `0x0059D920` | signed 32-bit | retained preceding X |
| `0x0059D924` | signed 32-bit | retained preceding Y |
| `0x0059D928` | signed 32-bit | retained preceding Z |
| `0x0059D960` | signed 32-bit | auxiliary/reset-coordinate X; not live airborne X |
| `0x0059D964` | signed 32-bit | auxiliary/reset-coordinate Y; not live airborne Y |
| `0x0059D968` | signed 32-bit | auxiliary/reset-coordinate Z; not live airborne Z |

## Evidence

[[EXP-20260815-128 - Live Flik position globals]] records the current triple's
full visible jump arc and ground movement. During that arm, every changed
preceding tuple equaled the preceding distinct current tuple. The auxiliary
triple remained at takeoff coordinates throughout the airborne arc, then
followed or converged with ordinary ground movement.

Static evidence independently supports the separation. Function `0x004189E0`
reads the current triple and conditionally copies it into the auxiliary triple.
Function `0x0042DDB0` seeds both current and preceding triples from the
auxiliary value. Function `0x004AB1A0` reads the preceding triple. Function
[[FUNC-97C95BA5572D-00432930]] writes type-1 row-derived reset coordinates to
the auxiliary triple.

[[EXP-20260815-130 - Write-assisted Level03 teleport safety boundary]] adds a
runtime mutation discriminator. After current and preceding were set equal to
the known walkable Level03 point `(501696,30092,494016)`, the unmodified game
copied that point into auxiliary about 10 ms later. It did the same for an
unsupported pit tuple before entering a repeating `NextLife=2` fall. This
confirms that auxiliary may follow equal stable-looking current/preceding
state; it does not establish the exact predicate or engine-frame cadence.

## Limits

“Preceding” is confirmed as a value relationship across the retained distinct
runtime samples. The exact engine-tick, physics-step, collision, or render
cadence is inferred and remains unknown. The auxiliary triple's complete
semantic role and update policy are also unknown; `reset-coordinate` is
supported for the tested type-1 consumer, but `checkpoint` is not.

For runtime mutation safety and evidence wording, see
[[PC Flik teleport procedure]].
