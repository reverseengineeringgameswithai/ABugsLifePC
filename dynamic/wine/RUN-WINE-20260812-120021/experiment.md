# RUN-WINE-20260812-120021

- Experiment: `EXP-20260812-013`
- Manifest: `mods/level01-primary-record-261-candidate-far.json`
- Staged DAT SHA-256: `ef43ee54e9283bac7280251dad9ad664b35ec02aa63ef9494bd36037f5b10384`
- Renderer: Direct3D hardware, 640×480×16
- Working directory: `/home/dev/ABLPC/work/copies/EXP-20260812-013/record-261-candidate-far/PC/BUGS`

## Observed

The accepted run loads Level 01 and reaches `NextLife`. Eleven same-index
frames are byte-identical to the unchanged control, including frame 03; moving
record 261's first candidate-center component outside the tested region has no
visible effect at the starting camera.

## Artifacts

- `bugs.log`
- `manifest-receipt.json`
- `metadata.json`
- Capture bytes remain under ignored work storage.
