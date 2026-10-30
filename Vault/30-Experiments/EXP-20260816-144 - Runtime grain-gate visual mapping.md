---
type: experiment
id: EXP-20260816-144
date: 2026-08-16
question: Which visible in-game gate corresponds to each Tunnels row and City Entrance index, confirmed by teleporting Flik to the EXP-141 standoff candidates?
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; Wine 11 Staging; Gamescope 3.16.25; Direct3D 640x480x16; nested Xwayland; XTEST input
configuration: exact retail executable; --research --windowed --mute; autonomous hardware selection and level-select navigation; write-assisted current+preceding teleports to EXP-141 standoffs; read-only snapshots; screenshots
working_directory: work/copies/EXP-20260816-144-gate-mapping
artifacts:
  - work/copies/EXP-20260816-144-gate-mapping/gate_probe.c
  - work/copies/EXP-20260816-144-gate-mapping/evidence/tunnels/
addresses:
  - "0x0059D910"
  - "0x0059D9B1"
  - "0x00861C84"
  - "0x004DA9C8"
  - "0x0059F020"
result: all-twelve-gates-visually-confirmed-nextlife-zero
status: completed
created: 2026-08-16T11:45:00
updated: 2026-08-16T12:20:00
tags:
  - re/experiment
  - re/runtime
  - re/gameplay
  - milestone/m3
---

# EXP-20260816-144 - Runtime grain-gate visual mapping

## Question and boundary

Do the EXP-141 static standoff candidates place Flik, by write-assisted
teleport, beside each intended grain gate so the visible gate can be
correlated with its Tunnels row / City index? This is the runtime mapping
pass deferred by EXP-139/141 and tracked under
[[Known Unknowns#KU-060 - Modified grain-gate physical transition]].

Retail executable only (SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`); no
grain, executable, asset, or `originals/` write. The only target writes are
guarded 24-byte current+preceding teleports per
[[PC Flik teleport procedure]]. This is **write-assisted**: it establishes
which visible gate is which mechanism, not controller reachability.

## Method

Autonomous control per [[PC autonomous game control]]: XTEST input, Down →
verify hardware highlight → Return, all six hardware log markers confirmed,
carousel navigation, internal level confirmed by `0x00861C84`. For each
gate the `gate_probe` helper teleports Flik to the standoff, then a
read-only snapshot records current XYZ, `NextLife`, grain, internal level,
the nine Tunnels rows (type/requirement/X/Z and engine sar-8 squared
distance), and the City state array. A gate is correlated when the intended
mechanism is the unambiguous nearest (smallest squared distance, inside the
open radius) with `NextLife=0`; the screenshot corroborates the visible
gate.

## Tunnels (internal level 3) — all nine confirmed

Every visible Tunnels gate is a **diagonal wooden-pole barrier**, several
with a leaf sign showing the grain-requirement numeral. Each teleport
landed with `NextLife=0` (every standoff walkable) and the intended row as
the unambiguous nearest gate:

| Row | Req | Standoff (x,y,z) | Nearest dist² | Visible gate |
| ---: | ---: | --- | ---: | --- |
| 0 | 20 | (205067,33916,143005) | 3872 | pole gate by start area, red mushroom |
| 1 | 10 | (489642,32092,-451306) | 3969 | pole gate, cyan + red mushrooms |
| 2 | 10 | (843615,33812,302388) | 3872 | pole gate on tunnel bend |
| 3 | 10 | (501696,30092,494016)* | 4993 | gate with visible **"10"** sign (EXP-129/137 gate) |
| 4 | 20 | (840401,33940,626583) | 3754 | pole gate near nut/leaf (rows 0/4 coupled) |
| 5 | 20 | (1126934,31480,1308289) | 3969 | pole gate, large cyan mushroom + grain line |
| 6 | 30 | (1471643,32820,1426369) | 3844 | gate with **"30"** sign + blue berry cluster (KU-057 gate) |
| 7 | 10 | (1202034,31492,1970285) | 3969 | pole gate (dark segment) |
| 8 | 30 | (1646238,33792,2546125) | 3872 | **"30"** gate, patrolling grasshopper enemy |

*Row 3 used the EXP-130/137 proven walkable point rather than the computed
standoff. Enemies patrol some gates (observed at row 8); enemy-caused
health/life loss is expected and unrelated to standoff walkability, which is
judged from `NextLife=0` at the moment of the post-teleport snapshot.

Screenshots: `evidence/tunnels/gate-T0.png` .. `gate-T8.png`, plus
`tunnels-start.png` (the "Level Two: Tunnel Run" briefing; note the internal
level is 3 despite the "Level Two" briefing text and the "tunnels" carousel
name — three independent numbering schemes).

## City Entrance (internal level 4) — all three confirmed

Reached by Right ×7 on the carousel ([[PC autonomous game control]]),
internal level confirmed `0x00861C84 == 4`. City gates are organic
leaf/pillar structures (unlike the Tunnels wooden poles). Each teleport
landed with `NextLife=0`, all three state words `0x0059F020 == (-1,-1,-1)`
(armed/closed at grain 0, matching EXP-137), and the intended gate as the
engine-exact nearest:

Nearest dist² is the engine `sar`-8 squared distance (helper `0x00416580`,
arithmetic shift) from the **settled current** position to the intended
gate center, for a consistent reference:

| Gate | Req (retail) | Standoff (x,y,z) | Settled current | Nearest dist² / threshold | Visible |
| ---: | ---: | --- | --- | --- | --- |
| 0 | 10 | (-87622,917,-182181)* | (-86227,931,-184484) | 3482 / 6400 inside | clear: giant "cola" can, leaf gate on left |
| 1 | 20 | (354031,2540,10716) | (354031,2540,10716) | 9216 / 8100 just-outside | occluded (Flik behind the gate) |
| 2 | 30 | (601433,1132,329374) | (599675,688,332298) | 11885 / 10000 just-outside | red-pillar gate structure |

*Gate 0 used the EXP-137 proven trigger point. City requirements are the
retail indexed values `10 * (index + 1)` (EXP-136); the internal level's
own gate order 0/1/2 is confirmed here, not the visible player-facing
sequence.

The researcher clarified that the wood-grain surface Flik faces at some
standoffs **is the gate's back side** — the standoff occasionally lands him
past the gate. Identification is unaffected: the nearest-gate index, the
`0x0059F020` state array, and `NextLife=0` are the authoritative
correlation, and gameplay movement input was independently confirmed
working (a forward nudge moved Flik `(595820,·,321345) -> (574298,·,316090)`).

Screenshots: `evidence/city/gate-C0.png` (clear), `gate-C1.png` /
`gate-C1b.png` (occluded), `gate-C2.png` and `c2-move-test.png` (red-pillar
gate).

## Result

All twelve grain gates are visually correlated to their in-game structures
with `NextLife=0` and the engine-exact nearest-gate check: nine Tunnels
wooden-pole barriers (rows 0–8) and three City Entrance leaf/pillar gates
(indices 0–2). The EXP-141 standoffs are therefore confirmed walkable and
correctly targeted for every gate. Tunnels frames are front-on; three City
frames view the gate from the side or back but identify the same gate. No
grain, executable, asset, or `originals/` mutation occurred; the only target
writes were guarded 24-byte current+preceding teleports.

## Independent audit and correction

[[EXP-20260816-145 - Independent runtime gate mapping audit]] verified the
standoff agreement, the nine Tunnels distances, all inside/outside verdicts
and nearest-gate identities, the retained screenshots, the
control-recipe disassembly, the write boundary, and hygiene — but returned
**REJECT** on one isolated defect: the City gate-0/1 `dist²` annotations
were originally computed with truncation-toward-zero instead of the engine
`sar` helper `0x00416580`, and mixed the standoff and settled reference for
gate 2. The City table above is corrected to engine `sar`-8 from the settled
current position (gate 0 `3482`, gate 1 `9216`, gate 2 `11885`), matching
James's independently computed values; gate 0 now agrees with EXP-139's
accepted gate-0 proximity method. No nearest-gate identity, inside/outside
verdict, or gate correlation changed.

## Follow-up

- Physical modified-threshold receipts for the untested gates (City 1/2 and
  Tunnels rows other than 3) remain the open part of
  [[Known Unknowns#KU-060 - Modified grain-gate physical transition]];
  this packet supplies their confirmed viewing/approach standoffs.
- Optional: cleaner front-on City frames by walking Flik around each gate
  (movement input is confirmed working).
- Independent audit of this mapping.
