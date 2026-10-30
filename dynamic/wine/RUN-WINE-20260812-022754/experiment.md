# RUN-WINE-20260812-022754

- Experiment: `EXP-20260812-008`
- Binary SHA-256: `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Environment: Fedora Linux 44, `wine-11.0 (Staging)`
- Working directory: `/home/dev/ABLPC/work/copies/BUGS_PC-full-disc/PC/BUGS`
- Renderer: Direct3D hardware, 640×480×16
- Started: `2026-08-12T02:27:54.757982606-04:00`

## Procedure

Run the unchanged work-copy DAT through the same renderer selection, Training
selection, natural title pause, capture timing, Gamescope PipeWire source, and
normalization used by the three variants.

## Observed

The game log reaches `InitMainGame` and `NextLife`. This is the matched visual
control for the three individual mutations.

## Artifacts

- `bugs.log`
- `training-hardware-control.png`
