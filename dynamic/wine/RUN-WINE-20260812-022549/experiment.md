# RUN-WINE-20260812-022549

- Experiment: `EXP-20260812-008`
- Binary SHA-256: `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Environment: Fedora Linux 44, `wine-11.0 (Staging)`
- Working directory: `/home/dev/ABLPC/work/copies/EXP-20260812-008/record-125/PC/BUGS`
- Renderer: Direct3D hardware, 640×480×16
- Started: `2026-08-12T02:25:49.210358750-04:00`

## Procedure

Stage `mods/training-primary-record-125-candidate-far.json` and repeat the
matched Training capture procedure used for the control.

## Observed

The game log reaches `InitMainGame` and `NextLife`. Relative to the matched
hardware control, 642 pixels differ inside `24x99+616+124`, identifying a
different plant element partially visible at the right frame edge.

## Artifacts

- `bugs.log`
- `manifest-receipt.json`
- `training-record-125-far.png`
