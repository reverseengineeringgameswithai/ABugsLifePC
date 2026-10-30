---
type: session
date: 2026-08-15
agent: Codex
status: completed
related:
  - EXP-20260815-128
  - STRUCT-PC-FLIK-POSITION-GLOBALS
  - DEC-20260815-120
created: 2026-08-15
updated: 2026-08-15
tags:
  - session/codex
  - re/runtime
  - implementation/tooling
---

# 2026-08-15 1835 - Codex - Live Flik position globals

## Scope

Launch one fresh pristine-derived PC session, enter Training, drive Flik with
ordinary keyboard input, determine the exact live position addresses, correct
the coordinate overlay, update durable Vault evidence, and finish with no
runtime or Git residue.

## Result

[[EXP-20260815-128 - Live Flik position globals]] confirms current live Flik
XYZ at `0x0059D910`/`14`/`18`. A stationary Shift jump produces the complete
signed-Y arc there, while `0x0059D920`/`24`/`28` retains the preceding distinct
tuple. The old overlay source at `0x0059D960`/`64`/`68` remains fixed at
takeoff throughout the airborne arc and is conservatively an
auxiliary/reset-coordinate triple.

This explicitly contradicts EXP-127's untested coordinate-source semantics.
That experiment remains valid for exact-target read access, translucent-window
creation, and joined cleanup. [[STRUCT-PC-FLIK-POSITION-GLOBALS]] and
[[Decision Log#DEC-20260815-120 - Bind the overlay to runtime-discriminated live position]]
record the corrected boundary.

Overlay worker 1.2.0 now reads the confirmed current triple, defaults to a
compact X/Y/Z-only panel on the owned Gamescope display, and keeps raw
diagnostics behind `--details`. The mapped Tk top-level receives the Gamescope
external-overlay and opacity properties. Companion 1.5.0 passes the target
display to the worker.

## Evidence

- `dynamic/wine/RUN-POS-20260815-181852/metadata.json`
- `dynamic/wine/RUN-POS-20260815-181852/position-trace.tsv`
- exact retail SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- static PC reads/copies in `0x004189E0`, `0x0042DDB0`, `0x004AB1A0`, and
  the type-1 reset-coordinate consumer `0x00432930`

## Validation and lifecycle

- focused overlay/companion suite: 18 passed;
- complete `make check`: Vault 368 notes, 0 errors, 0 warnings; 567 tests
  passed; five M4 hash anchors valid; tracked-file audit 0 violations;
- `git diff --check`: passed;
- exact companion, game, Wine/Gamescope group, coordinate overlay, and private
  sink were closed; post-arm process and sink audits were empty;
- Wine `Y:` restored to `/home/dev/ABLPC/work/copies/BUGS_PC-full-disc`;
- `originals/` was not modified.

## Boundary retained

The wall-clock trace does not identify an engine frame, physics tick,
coordinate unit, complete auxiliary update policy, click-through behavior, or
checkpoint semantics. KU-057 and CAP-002 remain unchanged.
