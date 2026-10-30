---
type: implementation
status: active
updated: 2026-10-02
tags:
  - implementation/tooling
  - re/dynamic
  - milestone/m3
---

# PC coordinate overlay

## Purpose

`scripts/coordinate-overlay.py` 1.2.0 is a read-only live display for the exact
retail PC `bugs.exe`. It shows Flik's current X/Y/Z without attaching a
debugger, pausing execution, setting breakpoints, or writing target memory.

**Later (2026-08-15):** the current file is 1.3.0. It also accepts the
EXP-20260815-136 grain-gates profile hash and adds an opt-in `--gates`
nearest-mechanism readout; the default display is unchanged. See
[[PC grain gate threshold mod#Gate mapping pass support]] and
[[EXP-20260815-140 - Independent static gate geometry and overlay audit]].

The normal entry point remains the existing companion:

```bash
scripts/play-pristine-with-inputs.py --research --windowed --mute --coordinates
```

`make coordinate-caps` prints the machine-readable read-only scope.

The **View → Show Coordinate Overlay** menu and the matching button can also
open or close it after the owned 640×480 game window is discovered.

## Display contract

The default window shows only:

- current live Flik X/Y/Z from `0x0059D910`/`0x0059D914`/`0x0059D918`.

`--details` additionally shows the conservative raw diagnostics retained from
the first version:

- internal level value from `0x00861C84`;
- raw actor flags from `0x0059D9A0`;
- raw `NextLife` value from `0x0059A5B0`;
- the signed state counter at `0x0059D9A4`;
- current collision index from `0x007F3D68`;
- the current descriptor's signed value at offset `0x1E` when the index is in
  the bounded `0..4095` range.

The neighboring `0x0059D920` triple retains the preceding distinct position in
the EXP-128 trace. The old `0x0059D960` source is an auxiliary/reset-coordinate
triple and is deliberately not displayed as current position. Only current
X/Y/Z, the executable addresses, and the raw field labels are confirmed.
`STATE` and collision `VALUE` deliberately avoid names such as health,
material, damage, hazard, or checkpoint unless a separate experiment supports
them.

## Safety and identity

- `evidence_lib.ownership_proof` requires the known retail executable SHA-256
  and a CWD under the selected `work/copies/` game tree.
- The companion passes the exact launcher-owned PID and process group.
- PID start time and process group are rechecked before each sample, so PID
  reuse closes the overlay instead of changing targets.
- `process_vm_readv` is the only target operation. Six base ranges share one
  gather read; the index-dependent collision value is a bounded follow-up
  read and can race that first sample. This is a display aid, not an atomic
  evidence capture.
- Five consecutive read failures close the overlay. Companion session cleanup
  also terminates the exact isolated overlay group.

## UI behavior and limits

Default overlay mode requests translucency (`0.78`) and always-on-top, removes
window chrome, and starts inside the owned Gamescope display at `+12+12` with
a compact 158×106, 15-point X/Y/Z panel. The Gamescope external-overlay atom
and opacity are applied to the mapped Tk top-level as well as its child window.
Left-drag moves it, double-click toggles ordinary window chrome/opacity, and
right-click, Escape, or Ctrl+Q closes only the overlay. `--mode window` is the
decorated fallback.

Click-through is not claimed. Host compositor policy can still affect
topmost/opacity behavior, so the window remains movable rather than
intercepting a large game area.

## Validation

[[EXP-20260815-127 - Read-only PC coordinate overlay]] accepts the original
read-only target-selection and cleanup contract, but its selector-screen smoke
did not validate coordinate semantics.
[[EXP-20260815-128 - Live Flik position globals]] corrects the source after a
controlled Training jump and ground
movement, and independently relates the three triples through static PC
instructions. The focused overlay/companion suite passes 18 tests.

Accepted implementation hashes at EXP-128 are (the 1.3.0 overlay file is now
`d44ff02a3d48ab08507b4915d1d8a2fc06be3dff665ec33106f097f29aa142bb`, commit
`9615514`):

- `scripts/coordinate-overlay.py`:
  `448225e650ca0a2686630538cc72786435c5a14054c01c549b6edd648fc15f66`;
- `scripts/play-pristine-with-inputs.py` 1.5.0:
  `3c4e54d508f8f26c7c21290a7110976f40d646630618611e5a29c37c69d9e369`.

The complete repository gate and final Vault counts are recorded in the
corresponding session note. M4's immutable compatibility anchors and the
tracked-file audit remain required unchanged gates.
