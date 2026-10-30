# RUN-WINE-20260812-022649

- Experiment: `EXP-20260812-008`
- Binary SHA-256: `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Environment: Fedora Linux 44, `wine-11.0 (Staging)`
- Working directory: `/home/dev/ABLPC/work/copies/EXP-20260812-008/record-126/PC/BUGS`
- Renderer: Direct3D hardware, 640×480×16
- Started: `2026-08-12T02:26:49.936660504-04:00`

## Procedure

Stage `mods/training-primary-record-126-candidate-far.json` and repeat the
matched Training capture procedure used for the control.

## Observed

The game log reaches `InitMainGame` and `NextLife`. Relative to the matched
hardware control, 8,265 pixels differ inside `109x250+438+0`; the prominent
flower and its stalk are absent.

## Artifacts

- `bugs.log`
- `manifest-receipt.json`
- `training-record-126-far.png`
