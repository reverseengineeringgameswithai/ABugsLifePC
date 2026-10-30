# RUN-WINE-20260812-103136

- Experiment: `EXP-20260812-010`
- Manifest: `mods/training-primary-record-124-target-111e4.json`
- Staged DAT SHA-256: `b8012a95f7ec0254805bdd3cf32df2b16f2ad0926308fe8678cc2360027f720e`
- Renderer: Direct3D hardware, 640×480×16
- Working directory: `/home/dev/ABLPC/work/copies/EXP-20260812-010/record-124-target-111e4/PC/BUGS`

## Procedure

Stage the guarded record-124 rebind, expose its parent as `S:`, choose the
second renderer option with Down, confirm the Direct3D log gate, and capture
the same 15-frame Training sequence used for the control.

## Observed

The game reaches `NextLife`. Against phase-matched control frame 07, 2,980
pixels differ only within `61x242+369+0`, the record-124 placement region
independently isolated by `EXP-20260812-008`.

## Artifacts

- `bugs.log`
- `manifest-receipt.json`
- `metadata.json`
- Capture bytes remain under ignored work storage; hashes are in `metadata.json`.
