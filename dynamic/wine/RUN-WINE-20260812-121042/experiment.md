# RUN-WINE-20260812-121042

- Experiment: `EXP-20260812-013`
- Manifest: `mods/level01-primary-record-261-target-3459c.json`
- Staged DAT SHA-256: `80649462f3e5e4010218ba04a20e2356ea981b5e29b651dacd7ecf4bff39965b`
- Renderer: Direct3D hardware, 640×480×16
- Working directory: `/home/dev/ABLPC/work/copies/EXP-20260812-013/record-261-target-3459c/PC/BUGS`

## Observed

The guarded `0x3703C -> 0x3459C` rebind is accepted, loads Level 01, and
reaches `NextLife`. Frames 03, 04, 07, and 08 are byte-identical to the
unchanged control, so the edit has no visible effect at the starting camera.

## Artifacts

- `bugs.log`
- `manifest-receipt.json`
- `metadata.json`
- Capture bytes remain under ignored work storage.
