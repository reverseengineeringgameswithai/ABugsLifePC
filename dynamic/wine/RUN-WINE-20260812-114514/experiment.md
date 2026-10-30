# RUN-WINE-20260812-114514

- Experiment: `EXP-20260812-013`
- Input: unchanged `CD/LEVEL01/LEVEL.DAT`
- DAT SHA-256: `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`
- Renderer: Direct3D hardware, 640×480×16
- Working directory: `/home/dev/ABLPC/work/copies/BUGS_PC-full-disc/PC/BUGS`

## Observed

The hardware-gated `ant hill` menu selection loads
`R:\PC\BUGS\cd\level01\level.dat`, completes `InitMainGame`, and enters
`NextLife`. This is the unchanged matched control.

## Artifacts

- `bugs.log`
- `metadata.json`
- Capture bytes remain under ignored work storage.
