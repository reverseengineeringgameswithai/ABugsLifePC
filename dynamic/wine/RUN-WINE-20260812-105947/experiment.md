# RUN-WINE-20260812-105947

- Experiments: `EXP-20260812-011`, control reused by `EXP-20260812-012`
- Binary SHA-256: `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Training DAT SHA-256: `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`
- Renderer: Direct3D hardware, 640×480×16
- Working directory: `/home/dev/ABLPC/work/copies/BUGS_PC-full-disc/PC/BUGS`

## Procedure

Choose the second renderer option with Down, require the Direct3D log gate,
select Training, leave the natural title pause, and request 15 native Gamescope
screenshots at approximately 0.2-second intervals.

## Observed

The unchanged game reaches `NextLife` without `INITSOFTRENDER`. Frame 08 is
byte-identical to both `EXP-20260812-011` variants. Frame 02 is the matched
control for `EXP-20260812-012`.

## Artifacts

- `bugs.log`
- `metadata.json`
- Capture bytes remain under ignored work storage; metadata records hashes.
