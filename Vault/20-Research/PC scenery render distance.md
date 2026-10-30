---
type: research
status: confirmed-bounded
created: 2026-09-07
updated: 2026-10-29
evidence: [EXP-20260907-009]
tags: [re/rendering, terrain/authoring]
---

# PC scenery render distance

[[EXP-20260907-009 - Mushroom render distance diagnosis]] investigates nearby
mushroom pop-in observed in an authored test layout. The meshes were
already resident. Captured-camera execution of original PC instructions shows
scenes 486 and 488 passing object admission but losing all drawable faces to
the hardware mesh depth check. Short forward presses progressively expose
their faces. This is distinct from the shared-floor bound problem in
[[PC terrain visibility growth checklist]]. No installed fix is claimed.

## Controls demonstrated by static code and copied-RAM execution

| Control | EXP-009 value | Evidence and effect |
| --- | --- | --- |
| `0x005C02FC` | 1152 | Shorter scenery group distance; assigned to per-pass scratch by `0x0044D430`. |
| `0x005BA80C` | 1664 | Longer group distance. Initializer `0x0044BB70` sets it from `0x680`; shorter group subtracts `0x200`. |
| Scene byte `+0x0E`, bit `0x40` | Clear on all 28 new mushrooms (`0x19`) | `0x0044D6A7` separates groups. Offline `0x59` uses the longer group with the same mesh/transform. |
| Object byte `+0x18` | 4 on these mushrooms | `0x0044A257..0x0044A266` subtracts `8 * byte` from the active distance during this object's draw. Preserve this depth/pass adjustment. |
| `0x005B56D0` | Scratch, observed 400 after background | Not a durable scene setting: main passes and object adjustments rewrite it. |

The outer scene test at `0x0044D59F` uses truncated X/Z camera distance, the
scene radius and `5 * group_distance`; the nearer group has a second test
ending at `0x0044D6F8`. The radius is an object bound, not a replacement for
increasing mesh draw depth.

In the observed hardware quad path, `0x0045CF63..0x0045CF89` rejects a face
when all four signed camera-space depths exceed `4 * active_distance`.
For these mushrooms the effective cutoff is **4480 stored units**, or
`4 * (1152 - 8 * 4)`. Selecting the longer existing group gives **6528**,
`4 * (1664 - 8 * 4)`: approximately **45.7% farther in camera depth**.
The nominal group ratio is 44.4%; it excludes the retained object adjustment.
Stored coordinates use 32 runtime world units each. This is camera depth,
not a Euclidean distance from Flik.

## Feasible next changes, still uninstalled

*Update (2026-10-02 audit):* option 2 was later installed.
[[EXP-20260907-010 - General render distance preview]] installed a 1.5x pair,
and [[EXP-20260911-013 - Twofold distance and Training performance]] selected
the 2x pair 2304/3328; [[PC general render distance]]
owns it. The text below is the EXP-20260907-009 pre-install analysis.

1. **Mushrooms only:** set bit `0x40` on the authored mushroom scene records
   during a fresh build. At the initial captured pose this changes 4 emitting
   mushrooms to 11 in native CPU replay. Sampled scenes 486/488 change from
   zero output to 100/116 vertices, all with alpha 255. Use fresh build indices;
   the current 484..511 allocation must not become a permanent hard-coded map.
   Group selection also changes draw ordering, so a full-frame live comparison
   remains necessary.
2. **Larger general increase:** adjust the two initialized distance values
   together. Offline pairs 1728/2496 and 2304/3328 admit and emit more mushrooms
   at the same pose. They are experimental RAM values inside Unicorn only.
   The hardware immediate 1664 is at executable VA `0x0044BBA3`, file offset
   `0x4AFA3`; the software counterpart is VA `0x0044BBAF`, file `0x4AFAF`.
   The current initializer derives near = far - 512, so changing only the
   base immediate does **not** reproduce a proportional pair.

Before installing a general distance change, validate the initializer's
distance-dependent lookup writes at `0x005C0410..0x005C240E` exclusive
(4095 words), signed transform/depth ranges, draw-buffer capacities and full
frame behavior. More admitted geometry may cost performance. These are concrete
engine dependencies, not evidence that the tested values overflow them.

Report: `reports/render-distance/EXP-20260907-009.json`. Private captures,
original-code hashes, branch traces, candidate comparisons and retained first
fixture corrections are indexed there. No live memory writes, installation,
debugger attachment or GPU/performance acceptance occurred.

## Training flower panorama and entrance view

[[EXP-20260911-014 - Training flower panorama and wall cutoff]] identifies the distant flower strip as decoded type36 panorama
art (256×136). Original00405410→00404410 draws a scrolling screen quad; six
replays keep its output identical under copied XYZ/distance changes. It is
separate from secondary DAT scenery and nearby3D foliage. In the turned entrance
view, the installed2x world cutoff still removes distant garden walls. No
additional range, assets or performance claims are introduced.

EXP014's follow-up also checks13 actual3D plant meshes in the initial direction:
tested depths8185..11982 fit their13184 cutoff. This is a selected native
admission/emission result; panorama artwork and nearby3D plants are distinct.

## Corrected target: distant grass strip

[[EXP-20260911-015 - Training grass uses secondary background geometry]] binds the observed grass strip to secondary15, original page4 grass
UVs and152/152 complete live vertex matches in two views. Its camera translation
is quarter-scaled by0044D83D's secondary tail;00448D70 renders with different
admission/scratch values. Shared far still participates, so this is not unlimited
render distance. The painted flowers and13 primary plants measured in EXP014
are different objects; those results do not identify the grass strip.

## Grass boundary near and distant representations

[[EXP-20260911-016 - Training grass boundary near and distant representations]] confirms the solid original boundary has detailed primary255..261
and simplified secondary15 representations. The latter's geometry and camera
are both quarter-scaled, retaining projected placement. Close meshes/current
collision and distant draws are corroborated; background is a draw-pass label,
not proof of decorative status.
No additional range, proxy implementation or performance result is installed.
