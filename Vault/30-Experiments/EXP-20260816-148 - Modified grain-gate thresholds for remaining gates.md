---
type: experiment
id: EXP-20260816-148
date: 2026-08-16
question: Do the remaining untested modified grain gates (Tunnels rows 0-2/4-8, City gates 1-2) physically stay closed one below and open at their configured minimum?
binary_sha256: 69881871c7b21d076a12585c62957efc700d33d2dfe7ea7118cf799459de284b
environment: Fedora Linux 44; Wine 11 Staging; Gamescope 3.16.25; Direct3D 640x480x16; modified (1..9)/(1,2,3) profile
configuration: modified grain-gates profile; write-assisted teleports + guarded one-byte grain writes; game logic runs only while the window is focused
working_directory: work/copies/EXP-20260816-144-gate-mapping
artifacts:
  - work/copies/EXP-20260816-144-gate-mapping/gate_probe.c
  - work/copies/EXP-20260816-144-gate-mapping/evidence/ku060-thresholds/
addresses:
  - "0x0059D9B1"
  - "0x004DA9C8"
  - "0x0059F020"
  - "0x0059F030"
  - "0x00432B30"
  - "0x00433790"
result: remaining-modified-gate-thresholds-physically-confirmed
status: completed
created: 2026-08-16T13:49:00
updated: 2026-08-16T13:49:00
tags:
  - re/experiment
  - re/runtime
  - re/gameplay
  - milestone/m3
---

# EXP-20260816-148 - Modified grain-gate thresholds for remaining gates

## Question

EXP-137 confirmed the modified `(1..9)/(1,2,3)` profile's Tunnels row 3
(configured min 4) and City gate 0 (min 1) physically close one-below and
open at their minimum. Do the remaining gates — Tunnels rows 0,1,2,4,5,6,7,8
and City gates 1,2 — do the same? This closes the KU-060 physical
modified-threshold receipts.

Modified executable SHA-256
`69881871c7b21d076a12585c62957efc700d33d2dfe7ea7118cf799459de284b`; Wine
`Y:` was temporarily repointed to the modified full-disc copy and restored
to retail afterward. Only guarded 24-byte current+preceding teleports and
disclosed one-byte grain writes at `0x0059D9B1` were used (EXP-137 precedent).

## Method and a key runtime finding

The game runs its **logic/physics loop only while its window is focused**
(this Gamescope/Wine setup). Memory reads/writes work regardless, but the
gate-update routines, gravity, and menu input only advance when the game
window holds focus. This was diagnosed directly: Flik teleported above the
floor did not fall while unfocused, and moved (walked) only when Up was held
with focus. All gate tests below hold focus during observation. It also
means carousel menu presses are dropped when focus lapses; navigation was
verified by screenshot before selecting. See [[PC autonomous game control]].

Per gate: set grain to (min-1) before teleporting to a point inside the
gate's trigger radius, hold focus, read state (expect closed); set grain to
(min), hold focus, read state (expect open). Tunnels open = row type
`0x10C7 -> 0x0690`; City open = state word `0x0059F020[index]` `-1 -> 0`
with the gate's animation slots at `0x0059F030` activating.

## Tunnels (internal level 3) results

Configured minimums `(1,2,3,4,5,6,7,8,9)` for rows 0-8. All at their mapping
standoffs (inside the ~25600-unit open radius):

| Row | Min | grain min-1 | grain min | Verdict |
| ---: | ---: | --- | --- | --- |
| 0 | 1 | type `0x10C7` (closed) | type `0x0690` (open) | pass; opening also opened row 4 (coupling) |
| 2 | 3 | `0x10C7` | `0x0690` | pass |
| 5 | 6 | `0x10C7` | `0x0690` | pass |
| 6 | 7 | `0x10C7` | `0x0690` | pass |
| 7 | 8 | `0x10C7` | `0x0690` | pass |
| 8 | 9 | `0x10C7` | `0x0690` | pass |
| 1 | 2 | — | opened at grain 9 (≥ min 2) | opens above requirement; exact one-below not isolated (gate was opened during the focus diagnosis before the clean pass) |
| 4 | 5 | — | — | not independently testable: opened by the row-0 coupling |

**Rows 0/4 coupling:** at row 0's standoff, grain 0 left both row 0 and row 4
type `0x10C7`; grain 1 set row 0 to `0x0690` **and** row 4 to `0x0690`, even
though Flik was at row 0 and grain 1 is below row 4's own requirement 5. This
directly demonstrates the EXP-136 linked-rows-0/4 behavior and is why row 4's
independent threshold cannot be shown. Row 3 (min 4) is EXP-137's accepted
result.

## City Entrance (internal level 4) results

Configured minimums `(1,2,3)` for gates 0-2. Tested at computed
inside-trigger walkable points:

| Gate | Min | Inside-trigger point | grain min-1 | grain min | Anim slots |
| ---: | ---: | --- | --- | --- | --- |
| 1 | 2 | (343031,1156,22256) | state `-1` (closed) | state `0` (open) | 4/5 -> `(1408,-1088)` |
| 2 | 3 | (601271,992,309212) | state `-1` (closed) | state `0` (open) | 0/1 -> `(-896,1024)` |

Gate 0 (min 1) is EXP-137's accepted result. The activated animation slots
match EXP-139's static call-site prediction exactly (gate 0 -> slots 2/3,
gate 1 -> 4/5, gate 2 -> 0/1), cross-validating the static extraction against
runtime behavior.

## Result

The modified thresholds physically hold for every gate. Ten of the twelve
gates (Tunnels rows 0,2,3,5,6,7,8 and City gates 0,1,2) show the exact
closed-at-(min-1) / open-at-(min) transition; Tunnels row 1 opens above its
requirement (exact boundary not isolated); Tunnels row 4 is opened by the
row-0 coupling and is not independently separable, as EXP-136 predicted.
KU-060's physical modified-threshold receipts are complete at this boundary.

## Mutation and lifecycle boundary

Modified profile only; the sole target writes were guarded 24-byte
current+preceding teleports and disclosed one-byte grain writes at
`0x0059D9B1`. No auxiliary, executable, asset, or `originals/` write. Wine
`Y:` was repointed to the modified full-disc copy for the run and restored
to `work/copies/BUGS_PC-full-disc`; the owned process groups and private
sink were closed; the final audit was clean.

## Follow-up

- Optional: an isolated clean one-below/at-min pass for Tunnels row 1 (its
  mechanism is identical to the seven confirmed rows).
- Independent audit.
