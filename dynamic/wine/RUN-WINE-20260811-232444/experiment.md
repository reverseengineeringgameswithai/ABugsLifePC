# RUN-WINE-20260811-232444

- Binary SHA-256: `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Environment: `wine-11.0 (Staging)`
- Prefix: `baseline`
- Working directory: `/home/dev/ABLPC/work/copies/BUGS_PC-disc`
- Wine debug channels: `+loaddll,+seh,+timestamp`
- Started: `2026-08-11T23:24:44-04:00`
- Time limit: `20 seconds`

## Procedure

Launch the PC executable from the sparse disc work copy under the clean baseline Wine prefix. Stop after 20 seconds if it remains active.

## Expected

Determine whether the executable exits immediately, reports an error, or remains alive long enough to create a window.

## Observed

- The native executable loaded at `0x00400000`.
- Wine loaded `DDRAW.dll`, `DINPUT.dll`, `DSOUND.dll`, and `wined3d.dll`.
- The user observed the game dialog: `Please insert A Bug's Life CD.`
- The process remained at the modal dialog until the 20-second limit.
- This sparse work copy did not contain the full disc content tree.

## Artifacts

- `metadata.json`
- `stdout.txt`
- `stderr.txt`
- `wine-debug.txt`

`strace.txt` is absent because the host does not currently provide `strace`.

## Capture result

- Ended: `2026-08-11T23:25:04-04:00`
- Exit status: `124`
- Outcome: `time-limit`

Interpretation: process and DirectX dependency startup succeeded, but the game stopped at its own media sentinel gate. See `EXP-20260811-004`.
