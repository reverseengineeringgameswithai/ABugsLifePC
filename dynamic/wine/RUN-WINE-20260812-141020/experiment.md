# RUN-WINE-20260812-141020

- Experiment: `EXP-20260812-019`
- Binary SHA-256: `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Staged `PLANT04.ANM` / source `PLANT10.ANM` SHA-256: `12d2550e…b5194`
- Staged `PLANT04.ALL` / source `PLANT10.ALL` SHA-256: `0c0f244b…714a`
- Renderer: Direct3D hardware, 640×480×16
- Working directory: `work/copies/EXP-20260812-019/replacement/PC/BUGS`

## Procedure

Launch through `V:\PC\BUGS`, choose the second renderer option with Down,
select Training, leave the natural title pause, and capture 15 Gamescope
PipeWire frames after `NextLife`.

## Observed

The log proves both hardware markers, loads the substituted plant 04 paths and
the native plant 10 pair, completes `InitMainGame`, and reaches `NextLife`
without `INITSOFTRENDER`. The process was intentionally terminated after
capture. A preceding software-path launch was rejected by the renderer gate
and is not represented by this run ID or retained log.

## Artifacts

- `bugs.log`
- `metadata.json`
- Capture bytes remain below ignored
  `work/copies/EXP-20260812-019/evidence/replacement-frames/`.
