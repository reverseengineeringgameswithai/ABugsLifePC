---
type: experiment
id: EXP-20260815-128
date: 2026-08-15
question: Which retail PC addresses retain Flik's live XYZ, and does 0x0059D960 follow airborne motion?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; Wine 11 Staging; Gamescope 3.16.25; Direct3D 640x480x16; Training
configuration: pristine retail derived work copy; read-only process_vm_readv at nominal 20 ms; Shift_L jump and Right movement
artifacts:
  - dynamic/wine/RUN-POS-20260815-181852/metadata.json
  - dynamic/wine/RUN-POS-20260815-181852/position-trace.tsv
  - scripts/coordinate-overlay.py
addresses:
  - "0x0059D910"
  - "0x0059D920"
  - "0x0059D960"
  - "0x004189E0"
  - "0x0042DDB0"
  - "0x004AB1A0"
result: current-live-position-confirmed-and-overlay-source-corrected
created: 2026-08-15
updated: 2026-08-15
tags:
  - re/experiment
  - re/runtime
  - re/gameplay
  - implementation/tooling
---

# EXP-20260815-128 - Live Flik position globals

## Question

Which exact retail PC globals track Flik's current X/Y/Z during ordinary
movement and a jump, and why did the coordinate overlay remain unchanged while
Flik was airborne?

## Controlled arm

One fresh pristine derived PC tree was launched through the pinned companion.
The renderer log selected Hardware, `Direct3D 640x480x16`, and Training reached
its initial `NextLife`. The only gameplay inputs were the user-supplied PC
controls: stationary `Shift_L` for a jump and `Right` for ground movement.

`RUN-POS-20260815-181852` sampled three candidate triples with read-only
`process_vm_readv` at a nominal 20 ms interval and retained distinct value
transitions. It did not attach a debugger, pause the process, set breakpoints,
or write target memory. The metadata binds the arm to exact retail SHA-256
`97c95ba5...878`, PID `88917`, process group `88662`, Gamescope PID `88671`,
and private sink `ablpc_mute_88662`.

## Confirmed runtime result

| Role | X | Y | Z | Evidence |
| --- | --- | --- | --- | --- |
| current live Flik position | `0x0059D910` | `0x0059D914` | `0x0059D918` | full visible jump arc and ground movement |
| retained preceding distinct position | `0x0059D920` | `0x0059D924` | `0x0059D928` | each changed tuple equals the preceding distinct current tuple in this trace |
| auxiliary/reset-coordinate triple | `0x0059D960` | `0x0059D964` | `0x0059D968` | frozen at takeoff throughout the airborne arc; follows or converges on ground |

At takeoff all three triples were `(-11434,13959,-15512)`. During the
stationary jump, current Y followed this visible arc while X/Z stayed fixed:
`13959 -> 11143 -> 8583 -> ... -> -2937 -> ... -> 8583 -> 13959`.
The preceding triple followed one distinct update behind. The auxiliary triple
remained exactly `(-11434,13959,-15512)` until landing. Thus upward movement
decreases signed Y in this controlled Training arm.

After landing, `Right` changed current X/Y/Z continuously. The auxiliary
triple generally followed or converged with ground movement, explaining why a
ground-only smoke could make it appear to be the live position. Candidate
`0x005BA810` was also rejected: it shared X/Z and an offset Y at rest but froze
during the jump rather than tracking the airborne arc.

## Independent static evidence

Disassembly of the same exact retail binary supplies a second evidence form:

- `0x00418A5E`, `0x00418A64`, and `0x00418AF4` read current Z/X/Y from the
  `0x0059D910` triple. `0x00418B07`, `0x00418B0D`, and `0x00418B13`
  conditionally copy it into the `0x0059D960` triple.
- `0x0042DDE8` reads auxiliary X, then `0x0042DDF3` and `0x0042DDF9` seed
  current and preceding X. The same pattern occurs for Y at
  `0x0042DE26`/`0x0042DE2B` and Z at `0x0042DE54`/`0x0042DE5A`.
- `0x004AB8B1`, `0x004AB8BB`, and `0x004AB8C6` read the preceding X/Y/Z
  triple in function `0x004AB1A0`.
- Function `0x00432930` writes selected type-1 reset-row X/Z into the
  auxiliary triple and recomputes its Y. EXP-116/117 therefore established an
  auxiliary/reset-coordinate consumer, not the live airborne position.

See [[STRUCT-PC-FLIK-POSITION-GLOBALS]] for the consolidated structure.

## Contradiction and correction

[[EXP-20260815-127 - Read-only PC coordinate overlay]] accepted read access,
identity gating, window creation, and cleanup, but its selector-screen smoke
did not exercise movement. Its claim that `0x0059D960` was live actor XYZ is
falsified by this jump. The implementation now reads `0x0059D910`; EXP-127
remains valid only for its read-only and lifecycle boundaries.

## Inference and unknowns

The value relationship supports describing `0x0059D920` as a retained
preceding position. Exact engine-tick, physics-step, render-frame, and
collision-sample cadence are not established by the wall-clock sampler.

`0x0059D960` is conservatively an auxiliary/reset-coordinate triple because
static reset paths write it and runtime shows that it is not live airborne
position. Its complete ownership, ground-update conditions, and all consumers
remain unknown. Coordinate units and world-axis names beyond observed signed
X/Y/Z behavior are also not claimed.

## Outcome

The overlay source is corrected to current live Flik X/Y/Z at `0x0059D910`,
`0x0059D914`, and `0x0059D918`. The default overlay displays only those three
values; conservative raw diagnostics remain opt-in through `--details`.
