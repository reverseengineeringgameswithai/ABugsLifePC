# RUN-WINE-20260812-111403

- Experiment: `EXP-20260812-012`
- Manifest: `mods/training-primary-record-125-field-0c-zero.json`
- Staged DAT SHA-256: `47b7f45e39137f7decdd4ca94db2ef663ee868e6d506bc88511569ded74d7c00`
- Renderer: Direct3D hardware, 640×480×16
- Working directory: `/home/dev/ABLPC/work/copies/EXP-20260812-012/record-125-field-0c-zero/PC/BUGS`

## Observed

The accepted rerun reaches `NextLife`. Matched frame 02 differs only within
`25x109+615+158`, where record 125's partially visible animated content is
excluded after its positive `+0x0C` bound is reduced to zero.

## Artifacts

- `bugs.log`
- `manifest-receipt.json`
- `metadata.json`
- Capture bytes remain under ignored work storage.
