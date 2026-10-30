# RUN-WINE-20260812-103354

- Experiment: `EXP-20260812-010`
- Manifest: `mods/training-primary-record-125-target-1319c.json`
- Staged DAT SHA-256: `b8ea00be86de53a9b659a20f8b0023369e687c9309b61dd61fe8496393d90ed9`
- Renderer: Direct3D hardware, 640×480×16
- Working directory: `/home/dev/ABLPC/work/copies/EXP-20260812-010/record-125-target-1319c/PC/BUGS`

## Procedure

Stage the guarded record-125 rebind, expose its parent as `S:`, choose the
second renderer option with Down, confirm the Direct3D log gate, and capture
the same 15-frame Training sequence used for the control.

## Observed

The game reaches `NextLife`. Against phase-matched control frame 07, 1,076
pixels differ only within `24x127+616+101`, overlapping the record-125
placement region independently isolated by `EXP-20260812-008`.

## Artifacts

- `bugs.log`
- `manifest-receipt.json`
- `metadata.json`
- Capture bytes remain under ignored work storage; hashes are in `metadata.json`.
