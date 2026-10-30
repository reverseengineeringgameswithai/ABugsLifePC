# RUN-WINE-20260812-140325

- Experiment: `EXP-20260812-019`
- Binary SHA-256: `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Unchanged `PLANT04.ANM` SHA-256: `32dce958…1e7ce`
- Unchanged `PLANT04.ALL` SHA-256: `486bd73c…f14a`
- Renderer: Direct3D hardware, 640×480×16
- Working directory: `work/copies/EXP-20260812-019/control/PC/BUGS`

## Procedure

Launch through `U:\PC\BUGS`, choose the second renderer option with Down,
select Training, leave the natural title pause, and capture 15 Gamescope
PipeWire frames after `NextLife`.

## Observed

The log proves both hardware markers, loads the plant 04 and 10 pairs,
completes `InitMainGame`, and reaches `NextLife` without `INITSOFTRENDER`.
The process was intentionally terminated after capture.

## Artifacts

- `bugs.log`
- `metadata.json`
- Capture bytes remain below ignored
  `work/copies/EXP-20260812-019/evidence/control-frames/`.
