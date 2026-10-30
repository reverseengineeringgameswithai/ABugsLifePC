---
type: experiment
id: EXP-20260812-007
date: 2026-08-12
question: Can the unchanged Direct3D game be presented fullscreen on the Linux host without changing its 4:3 aspect ratio?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Wine and Gamescope on Fedora Linux
environment_version: wine-11.0-staging; gamescope-3.16.25-1.fc44
result: aspect-preserving-hardware-baseline
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/dynamic
  - environment/wine
---

# EXP-20260812-007 - Gamescope hardware presentation baseline

## Question

Can the unchanged Direct3D game be presented fullscreen on the 2560×1440 Linux host without changing its 4:3 aspect ratio?

## Configuration

- Executable: `BIN-97c95ba5572dce63`, unchanged SHA-256 `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Working directory: `work/copies/BUGS_PC-full-disc/PC/BUGS`
- Prefix: `work/wine/baseline`
- Host: Fedora 44, Wine 11 staging, Gamescope `3.16.25-1.fc44`
- Gamescope: nested 640×480, output 2560×1440, `fit` scaler, `nearest` filter, fullscreen
- Game arguments: `log cheat mpeg` for research navigation

## Procedure

1. Launch the unchanged executable with the exact command recorded in `RUN-WINE-20260812-013633`.
2. At the game's renderer selector, choose the second option, hardware acceleration.
3. Enter Training and retain the game log.
4. Capture the compositor-visible selector and gameplay frames through PipeWire.
5. Measure each 2560×1440 frame's non-black bounds with ImageMagick `-trim`.
6. Compare the renderer log with the retained software run `RUN-WINE-20260812-000215`.

## Observed

### Confirmed

- `RUN-WINE-20260812-013633/renderer-evidence.txt` records `RenderMode set to Direct3d`, `Screen mode 640x480x16 selected`, and `Starting Direct3D renderer` from the game-generated log.
- The separately retained software log at `dynamic/wine/RUN-WINE-20260812-000215/bugs.log` records `D3DAPPCREATE : Mode set to 320x200`, `SOFTRENDER : Screen set to 320x200`, and `InitSoftWindow(320,200)`.
- Both hardware-selector and hardware-gameplay compositor captures had a 2560×1440 canvas and measured non-black bounds of 1920×1439 at approximately X=319, consistent within one captured row with an aspect-preserving 1920×1440 4:3 fit. Evidence: `RUN-WINE-20260812-013633/presentation-measurement.txt`.
- The user visually confirmed that the hardware-acceleration selection corrected the unexpectedly low-resolution gameplay presentation.

### Inferred

- The much smaller software-mode gameplay seen inside a 640×480 nested surface is explained by the game's independently logged 320×200 software renderer rather than by Linux reducing a 640×480 hardware frame.
- Browser scaling and video compression are plausible contributors to the softer appearance of comparison footage, but the comparison video's renderer, capture chain, and source settings were not available for verification.

### Unknown

- Whether nearest or linear presentation better matches a specific period monitor, Windows driver, or comparison video.
- Whether WineD3D introduces subtler rendering differences from period Windows hardware after resolution and presentation filtering are controlled.

## Artifacts

- `dynamic/wine/RUN-WINE-20260812-013633/metadata.json`
- `dynamic/wine/RUN-WINE-20260812-013633/renderer-evidence.txt`
- `dynamic/wine/RUN-WINE-20260812-013633/presentation-measurement.txt`
- `dynamic/wine/RUN-WINE-20260812-000215/bugs.log`
- `dynamic/wine/RUN-WINE-20260812-000634/bugs.log`

## Interpretation

**Confirmed for the tested Linux host:** use the game's hardware-acceleration option as the primary play and visual-research mode. Gamescope `fit` presents the resulting 640×480 Direct3D surface at host-display height while retaining 4:3. The `nearest` versus `linear` filter is a presentation preference and does not change the aspect-ratio policy.

The software renderer remains useful as a diagnostic comparison, not the normal Linux play baseline.

## Result

Completed. The configuration is encoded by `scripts/play-pristine.sh` and documented in [[Wine Linux Play Baseline]].

## Follow-up

If exact historical rendering becomes material, capture the same stationary scene under the future Windows 98 reference environment and compare it against Wine with identical 640×480 output and recorded filtering.
