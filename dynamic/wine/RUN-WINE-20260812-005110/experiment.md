# RUN-WINE-20260812-005110

- Binary SHA-256: `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Environment: `wine-11.0 (Staging)`
- Prefix: `baseline`
- Working directory: `/home/dev/ABLPC/work/mod-builds/training-disc-root/PC/BUGS`
- Wine debug channels: `-all`
- Started: `2026-08-12T00:51:10-04:00`

## Procedure

Run the recorded argv under Wine with the configured Wine debug channels and optional syscall capture.

## Expected

The three-record manifest output reaches gameplay and produces a visible difference from the control.

## Observed

The software renderer reached `NextLife`; the cropped game capture lacks the central foreground flower cluster visible in the control while other reference scene elements remain. This is the modified arm of `EXP-20260812-006`.

## Artifacts

- `metadata.json`
- `stdout.txt`
- `stderr.txt`
- `wine-debug.txt`
- `bugs.log`
- `training-records-124-126-far.png`
- Syscall capture: `disabled`

## Capture result

- Ended: `2026-08-12T00:51:55-04:00`
- Exit status: `58`
- Game log copied: `1`

Exit status 58 is intentional termination after capture. Interpretation: `EXP-20260812-006`.
