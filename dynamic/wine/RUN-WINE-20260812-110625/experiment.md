# RUN-WINE-20260812-110625

- Experiment: `EXP-20260812-011`
- Manifest: `mods/training-primary-record-126-field-08-plus-512.json`
- Staged DAT SHA-256: `9513fdfb7ace1fd6179054631cb3a735b5212bb645c75640736ddbdd50ea64c0`
- Renderer: Direct3D hardware, 640×480×16
- Working directory: `/home/dev/ABLPC/work/copies/EXP-20260812-011/record-126-field-08-plus-512/PC/BUGS`

## Observed

The accepted rerun reaches `NextLife`. Frame 08 is byte-identical to the
unchanged control; the `+0x08` edit does not visibly reposition record 126.

## Artifacts

- `bugs.log`
- `manifest-receipt.json`
- `metadata.json`
- Capture bytes remain under ignored work storage.
