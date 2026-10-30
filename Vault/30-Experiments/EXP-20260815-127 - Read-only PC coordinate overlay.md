---
type: experiment
id: EXP-20260815-127
date: 2026-08-15
question: Can an owned retail PC session display live coordinates in a translucent companion without debugger mutation or lifecycle residue?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; Wine 11 Staging; Gamescope; Tk; retail derived work copy
configuration: companion 1.4.0 --coordinates; process_vm_readv at 100 ms; selector-screen smoke
artifacts:
  - scripts/coordinate-overlay.py
  - scripts/play-pristine-with-inputs.py
result: live-smoke-accepted-read-only-overlay-and-cleanup
created: 2026-08-15
updated: 2026-08-15
tags:
  - re/experiment
  - re/runtime
  - implementation/tooling
---

# EXP-20260815-127 - Read-only PC coordinate overlay

## Question

Can the exact launcher-owned retail PC process feed a translucent coordinate
window without attaching a debugger, modifying game state, selecting another
process, or leaving runtime residue?

## Implementation and offline validation

`scripts/coordinate-overlay.py` 1.0.0 verifies the retail executable hash,
work-copy CWD, exact process group, and PID start time. It uses only
`process_vm_readv`. Companion 1.4.0 adds a View menu/button and automatic
`--coordinates` startup while retaining the pinned `play-pristine.sh` launch
authority.

Focused tests cover signed X/Y/Z and state decoding, bounded collision-index
follow-up reads, malformed `/proc` identity, option bounds, declared read-only
capabilities, exact command construction, and companion behavior. The focused
suite passed 17/17 before the live arm.

Accepted implementation SHA-256 values are
`c5a458aa...8e39` for `coordinate-overlay.py` and
`c3668646...d41` for companion 1.4.0.

## Live smoke

The companion launched one pristine derived PC tree with:

- companion PID/PGID `69217`;
- owned game PGID `69219`;
- retail game PID `69474`;
- coordinate overlay PID/PGID `69567`;
- private sink `ablpc_mute_69219`.

Automatic discovery created `ABLPC Coordinates` at `+24+24`, size 266×160.
The overlay remained live beyond its five-failure close threshold. An
independent call through the same implementation returned coherent
selector-screen values: X/Y/Z `0/0/0`, level `1`, flags `0`, `NextLife` `0`,
state counter `0`, collision index/value `0/0`. This confirms live read access
and decoding at that instant, not gameplay semantics or atomic frame
synchronization.

Ctrl+C to the companion closed the overlay and exact launcher group. Final
process and sink audits were empty, and Wine `Y:` was restored to the pre-smoke
target.

## Result and limits

**Accepted:** exact-target read-only sampling, translucent companion creation,
automatic startup, and joined cleanup work on the tested host.

**Not claimed:** click-through, compositor-independent topmost/opacity,
internal-frame synchronization, atomicity between the gather read and
collision follow-up, semantic identification of raw state fields, or any
resolution of `KU-057`/CAP-002.

## Superseded coordinate-source claim

This selector-screen smoke accepted read access and lifecycle behavior, but it
did not exercise ground or airborne motion.
[[EXP-20260815-128 - Live Flik position globals]] falsifies the original
actor-coordinate interpretation:
`0x0059D960` stayed fixed at takeoff while `0x0059D910` followed Flik's full
visible jump arc. The current live XYZ source is `0x0059D910`/`14`/`18`;
`0x0059D960`/`64`/`68` is an auxiliary/reset-coordinate triple.

EXP-127 remains authority for exact-target `process_vm_readv`, translucent
window creation, and joined cleanup only. Coordinate semantics and the
corrected overlay source are authority of EXP-128.

After documentation, the complete repository gate passes 566 tests; Vault
lint reports 365 notes with zero errors/warnings, all five M4 compatibility
anchors pass, and the tracked-file audit reports zero violations.

See [[PC coordinate overlay]] for usage and the complete boundary.
