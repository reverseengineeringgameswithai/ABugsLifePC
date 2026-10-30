---
type: experiment
id: EXP-20260815-137
date: 2026-08-15
question: Do modified Tunnels row 3 and City Entrance gate 0 remain closed one below their configured minimum and physically open at the exact minimum?
status: accepted-by-independent-audit
binary_sha256: 69881871c7b21d076a12585c62957efc700d33d2dfe7ea7118cf799459de284b
environment: Fedora Linux 44; Wine 11 Staging; Gamescope 3.16.25; Direct3D 640x480x16
configuration: Tunnels rows 0..8 set to 1..9; City Entrance gates 0..2 set to 1,2,3
artifacts:
  - dynamic/wine/EXP-20260815-137-receipt.md
  - work/copies/EXP-20260815-137-grain-gate-runtime/evidence/hashes.sha256
addresses:
  - "0x00432B30"
  - "0x00433790"
  - "0x004DA9C8"
  - "0x0059A5B0"
  - "0x0059D910"
  - "0x0059D920"
  - "0x0059D960"
  - "0x0059D9B1"
  - "0x0059F020"
  - "0x0059F030"
  - "0x00861C84"
result: independently-accepted-row3-and-gate0-threshold-boundaries
created: 2026-08-15
updated: 2026-08-15
tags: [re/experiment, re/runtime, mod/gameplay]
---

# EXP-20260815-137 - Modified grain-gate threshold behavior

## Question and authority

Does the EXP-136 `(1..9)`/`(1,2,3)` work-copy profile produce a physical
closed/open boundary at Tunnels row 3's configured minimum 4 and City Entrance
gate 0's configured minimum 1?

The researcher explicitly approved both below-minimum/exact-minimum arms and
delegated the individual mutation approvals. The PC executable and PC runtime
are the only behavioral authorities. No PS1 source was consulted.

## Method boundary

Every accepted arm used the exact modified executable SHA-256
`69881871c7b21d076a12585c62957efc700d33d2dfe7ea7118cf799459de284b`
and positively recorded video-memory 640x480 Direct3D initialization, the
relevant level load, `---End InitMainGame---`, and `NextLife`.

The helper bounds checks every exact read and guards writes by PID, internal
level, current grain, fixed address, width, and readback. Position setup wrote
only the 12-byte current XYZ plus 12-byte preceding XYZ at `0x0059D910` and
`0x0059D920`. Grain setup wrote only one byte at `0x0059D9B1`. No auxiliary,
gate-state, animation, life, register, code, asset, or original-media write was
used. Full identities, mutations, snapshots, frames, hashes, and cleanup are
in `dynamic/wine/EXP-20260815-137-receipt.md`.

## Tunnels result

The setup point `(501696,30092,494016)` is the known walkable Level03 floor
accepted in EXP-130. It is within `0x00432B30` row 3's opening radius:
shifted X/Z distance squared was 4,993, below the exact 10,000 comparison.

| Condition | Grain | Row 3 requirement | Row 3 type | NextLife | Visible gate |
| --- | ---: | ---: | --- | ---: | --- |
| below minimum | 3 | 4 | `0x10C7` | 0 | closed/upright |
| exact minimum, settled | 4 | 4 | `0x0690` | 0 | open/lowered |

The only between-condition target write was grain `3 -> 4`. All position
triples remained `(501696,30092,494016)`. This joins the configured resident
requirement and `0x00432B30` static comparison to a discriminating live state
and physical transition for row 3.

## City Entrance result

Ordinary route-finding, including researcher input at the first gate, saved
approach point `(-92603,1098,-181281)`. That point visibly frames the closed
gate but is just outside the trigger boundary, so it is retained as route
evidence, not used as the same-position threshold control. With grain 1, one
short ordinary forward step first triggered at
`(-87622,917,-182181)`.

A fresh accepted hardware arm used that ordinary-proven walkable trigger
point for one guarded current-plus-preceding position setup. With no movement
between conditions:

| Condition | Grain | City state | Animation 2/3 | NextLife | Visible gate |
| --- | ---: | --- | --- | ---: | --- |
| below minimum | 0 | `(-1,-1,-1)` | `0/0` | 0 | closed |
| exact minimum, 120 ms | 1 | `(28,-1,-1)` | `-128/+128` | 0 | opening |
| exact minimum, settled | 1 | `(0,-1,-1)` | `-1024/+1024` | 0 | open |

The only between-condition target write was grain `0 -> 1`; current,
preceding, and auxiliary all remained exactly
`(-87622,917,-182181)`. This joins the configured gate-0 lookup and
`0x00433790` static comparison to a discriminating live state and physical
transition. The gate graphic still says `10`; that visible asset was not
changed and does not reflect the executable minimum.

## Rejected arm and renderer correction

One attempted corrected City arm was rejected before any target write. Its
early driver-selection lines named Direct3D, but the later log entered
`SYSTEM MEMORY ONLY`, 320x200, and `INITSOFTRENDER`, and the surface was visibly
320x200. This proves the early selection summary alone is insufficient. The
replacement arm required `VIDEO MEMORY ONLY`, `Mode set to 640x480`, and
`Starting Direct3D renderer` in addition to the selection summary. The durable
startup gate is corrected in [[START HERE]].

## Result and limits

Worker result: Tunnels row 3 and City Entrance gate 0 each remain physically
closed below their configured minimum and physically open at the exact
minimum. The exact resident state/animation transitions and visible frames
agree. [[EXP-20260815-138 - Independent modified grain-gate threshold audit]]
later accepts only these two tested mechanisms.

This does not establish the visible ordering or behavior of Tunnels rows
0–2/4–8, independent presentation of linked rows 0/4, City gates 1/2, another
executable version, persistence in saved data, or automatic changes to the
retail numeral graphic. Both same-position setups are write-assisted and do
not establish controller reachability; the City trigger point was first
reached ordinarily.

## Independent disposition

James independently rehashed the complete 69-file `evidence/` manifest,
reconstructed the earlier helper source to its stated SHA-256, rebuilt the
final helper byte-for-byte, reproduced the exact executable profile and
inverse in memory, reviewed the modified x86 consumers, inspected all accepted
frames/snapshots and the rejected controls, and reran focused/full gates.
[[EXP-20260815-138 - Independent modified grain-gate threshold audit]] returns
**ACCEPT** for Tunnels row 3 and City gate 0 without widening any limitation
above. It also corrects the tracked runtime receipt's manifest description:
`hashes.sha256` covers the 69 files in `evidence/`; the packet-root helper
source and binary are pinned separately.
