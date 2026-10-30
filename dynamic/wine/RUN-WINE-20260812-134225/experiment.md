# RUN-WINE-20260812-134225

- Experiment: `EXP-20260812-018`
- Binary SHA-256: `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Staged `PLANT04.ANM` SHA-256: `12d2550e…b5194`
- Unchanged `PLANT04.ALL` SHA-256: `486bd73c…f14a`
- Renderer: Direct3D hardware, 640×480×16
- Working directory: `work/copies/EXP-20260812-018/replacement/PC/BUGS`

## Procedure

Launch through `T:\PC\BUGS`, choose the second renderer option with Down,
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
  `work/copies/EXP-20260812-018/evidence/replacement/`.
