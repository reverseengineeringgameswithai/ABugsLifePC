# RUN-WINE-20260812-110202

- Experiment: `EXP-20260812-011`
- Manifest: `mods/training-primary-record-126-field-04-plus-512.json`
- Staged DAT SHA-256: `1c7ccb3c21ec4bacf0733ed54466da93d451bd30f671a42eb04c43fc38c69952`
- Renderer: Direct3D hardware, 640×480×16
- Working directory: `/home/dev/ABLPC/work/copies/EXP-20260812-011/record-126-field-04-plus-512/PC/BUGS`

## Observed

The game reaches `NextLife`. Frame 08 is byte-identical to the unchanged
control; the `+0x04` edit does not visibly reposition record 126.

## Artifacts

- `bugs.log`
- `manifest-receipt.json`
- `metadata.json`
- Capture bytes remain under ignored work storage.
