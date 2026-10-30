---
type: experiment
id: EXP-20260812-005
date: 2026-08-12
question: Can the unchanged PC executable reach playable training-level rendering under Wine, and which renderer is suitable for the Linux modding baseline?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Wine
environment_version: wine-11.0-staging
result: playable-training-baseline
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/dynamic
  - environment/wine
---

# EXP-20260812-005 - Wine training baseline

## Question

Can the unchanged PC executable reach playable training-level rendering under Wine, and which renderer is suitable for the Linux modding baseline?

## Procedure

1. Run the unchanged executable with `log cheat mpeg` from the known-good derived `R:\PC\BUGS` layout.
2. At the driver selector, test its default software renderer and its Direct3D hardware renderer.
3. Select Training from the cheat-enabled level selector and advance to gameplay.
4. Retain the built-in log and screenshots.

## Observed

- `RUN-WINE-20260812-000215` entered the software renderer at 320×200 and loaded `level07\level1.dat`.
- `RUN-WINE-20260812-000634` logged `INIT : Starting Direct3D renderer.`, initialized 640×480, loaded the same file, and displayed playable training gameplay.
- The hardware screenshot shows Flik, a second ant, a training sign, terrain, vegetation, and a seed-like object. This establishes a stable visual comparison target; it does not identify their DAT records.
- Both capture processes were intentionally terminated after evidence collection, so exit status 1 is not evidence of an application failure.

## Artifacts

- `dynamic/wine/RUN-WINE-20260812-000215/bugs.log`
- `dynamic/wine/RUN-WINE-20260812-000215/training-baseline.png`
- `dynamic/wine/RUN-WINE-20260812-000634/bugs.log`
- `dynamic/wine/RUN-WINE-20260812-000634/training-hardware-playable.png`

## Addresses

`0x00403B90`, `0x004A7600`

## Interpretation

Confirmed under Wine 11 staging: Windows 98 is not required for the current edit-test loop. The Direct3D path is the primary visual baseline; the software renderer remains a useful cross-check.

## Result

Completed. The unchanged PC game reaches visible, playable training-level rendering under Wine.

## Follow-up

Automate a deterministic input/capture sequence without depending on desktop focus and distinguish the remaining audio warnings from rendering behavior.
