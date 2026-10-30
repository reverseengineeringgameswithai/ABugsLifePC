# RUN-WINE-20260812-150528

- Experiment: `EXP-20260812-020`
- Binary SHA-256: `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Unchanged Training DAT SHA-256: `494d2818…d5a22`
- Renderer: Direct3D hardware, 640×480×16
- Working directory: `work/copies/EXP-20260812-020/control/PC/BUGS`

## Procedure

Launch through `W:\PC\BUGS`, send Down once to the exact game window and
confirm the second renderer option, select Training, leave the natural title
pause, then capture 15 Gamescope PipeWire frames after `NextLife`.

## Observed

The log proves both hardware markers, requests plant 04 and plant 10 pairs,
completes `InitMainGame`, and reaches `NextLife` without `INITSOFTRENDER`.
The process was intentionally terminated after capture.

## Artifacts

- `bugs.log`
- `metadata.json`
- Capture bytes remain ignored below
  `work/copies/EXP-20260812-020/evidence/control/frames/`.
