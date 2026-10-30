---
type: implementation
status: implemented
created: 2026-09-07
updated: 2026-10-29
evidence: [EXP-20260907-009, EXP-20260907-010]
tags: [implementation/modding, re/rendering]
---

# PC general render distance

[[EXP-20260907-010 - General render distance preview]] installed a 1.5x pair
(near/far 1728/2496) in a derived executable.
[[EXP-20260911-013 - Twofold distance and Training performance]] later ran the
2x pair 2304/3328 live; two60s trials show31.23/31.25 FPS with similar CPU.
Other-level performance is unmeasured.

`reimplementation/ablpc/render_distance.py` holds named original/default values
(`DEFAULT` is the 1.5x pair), input bounds, initializer identity and patch
receipts. Near/far 1152/1664 reproduce the original executable. Apply it to
pinned clean inputs: applying twice to an already modified executable rejects,
as does a changed or truncated initializer.

## PC mechanism and scope

Original `0x0044BB70` initializes both distance groups and a 4095-word lookup
at `0x005C0410..0x005C240E` exclusive. The guarded edit changes three immediate
fields (five differing bytes total) in the derived executable:

| Immediate VA / file offset | Original | Installed | Purpose |
| --- | --- | --- | --- |
| `0x0044BBA3` / `0x4AFA3` | 1664 | 2496 | Hardware far initialization |
| `0x0044BBAF` / `0x4AFAF` | 1664 | 2496 | Software far initialization |
| `0x0044BBC1` / `0x4AFC1` | -512 | -768 | Derive near from far |

RAM near `0x005C02FC` is 1728; far `0x005BA80C` is 2496. Native initialization
and the complete live lookup table match. Changing only the far immediate would
produce the wrong near value for proportional scaling. Do not poke per-pass
scratch `0x005B56D0`: original draw code repeatedly rewrites it.

[[PC scenery render distance]] supplies original scene-admission and polygon-depth
evidence. Terrain's zero object bias gives nominal camera-depth cutoff
6656 → 9984 stored units (+50%); mushrooms retain byte `+0x18 = 4`, giving
4480 → 6784 (+51.4%). These are camera depths, not distances from Flik.
Both global groups change without assigning different groups to mushrooms.
The far global also feeds original secondary/background admission in `0x0044D430`.
Geometry, object bias and render code are retained; exact background admission
is not asserted unchanged. No sky/horizon geometry changes.
All 721 staged data files are byte-identical to the preceding layout build.

## Validation and further expansion

48 focused tests, six original-PC initializer
cases (stock/1.5×/2×, software/hardware), and eight primary frame replays pass.
Each replay runs all 29 active terrain/mushroom objects through original admission,
projection, emission, automatic flush and counter reset, checking finite vertices
and packet/index capacities. Live code, globals and full lookup match the
stage. These captures do not establish a controlled FPS result.

The next proportional setting is 2304/3328 (2× original, 33.3% farther than this
version). Its initializer and selected mushroom replay have passed offline;
it has not received this version's general-frame, live GPU or performance checks.
The validator permits only the investigated original-to-2× envelope, enforces
near < far, lookup bounds and signed depth limits. That is not live acceptance
of every permitted pair. Beyond 2× needs fresh static/native bounds work before
relaxing the guard. EXP-20260911-013 later ran the 2x pair live (above).

[[EXP-20260911-012 - Training corner render distance diagnosis]]: wall scenes
flagged `0x59` already use the longer group, yet a far corner that passes scene
admission loses its quads beyond9984 stored units at 1.5x;2x raises the cutoff
to13312 and restores it in native copied-state replay.

Authoritative authored index: `reports/render-distance/EXP-20260907-010.json`.
Private fixtures, raw captures and exact receipts stay under its experiment root.

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
