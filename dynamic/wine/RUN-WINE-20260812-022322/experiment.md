# RUN-WINE-20260812-022322

- Experiment: `EXP-20260812-008`
- Binary SHA-256: `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Environment: Fedora Linux 44, `wine-11.0 (Staging)`
- Working directory: `/home/dev/ABLPC/work/copies/EXP-20260812-008/record-124/PC/BUGS`
- Renderer: Direct3D hardware, 640×480×16
- Started: `2026-08-12T02:23:22.061627562-04:00`

## Procedure

Stage `mods/training-primary-record-124-candidate-far.json`, map its parent to
`S:`, select hardware acceleration and Training, press a key at the Training
title, and capture the first stationary scene through Gamescope PipeWire.

## Observed

The game log reaches `InitMainGame` and `NextLife`. Relative to the matched
hardware control, 2,942 pixels differ inside `52x241+369+0`, identifying a
distinct thin, top-clipped plant element.

## Artifacts

- `bugs.log`
- `manifest-receipt.json`
- `training-record-124-far.png`
