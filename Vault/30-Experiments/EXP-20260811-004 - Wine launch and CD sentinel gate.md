---
type: experiment
id: EXP-20260811-004
date: 2026-08-11
question: Does the original PC executable launch under baseline Wine, why does it display the CD-insertion dialog, and can the gate be passed without modifying executable bytes?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Wine
result: launched-and-cd-gate-explained
tags:
  - re/experiment
  - re/dynamic
  - environment/wine
---

# EXP-20260811-004 - Wine launch and CD sentinel gate

## Question

Does the original PC executable launch under baseline Wine, why does it display the CD-insertion dialog, and can the gate be passed without modifying executable bytes?

## Binary SHA-256

`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`

## Environment

Fedora host, `wine-11.0 (Staging)`, project baseline prefix.

## Environment version

See [[Environment Status]].

## Working directory

Negative media-root test: `R:\`

Successful fallback-layout test: `R:\PC\BUGS`

## Configuration

- Full ISO-derived copy: 2,249 files under ignored `work/copies/BUGS_PC-full-disc`.
- Wine mapping: `R:` directory-backed drive, registry type `cdrom`, label `BUGS_PC`.
- Verified sentinel: `R:\PC\BUGS\CD\CD.TXT`.
- Successful test executable: unchanged hash-verified copy at `R:\PC\BUGS\bugs.exe`.
- No DLL overrides, wrappers, executable patches, or compatibility hacks.
- `strace` unavailable on the host.
- User-provided external transcript used only to propose a drive-scan hypothesis.

## Procedure

1. Initialize the clean baseline Wine prefix.
2. Launch the work-copy executable with focused Wine module/exception logging.
3. Extract the complete immutable ISO into ignored `work/copies/`.
4. Map the derived tree as `R:`, mark it `cdrom`, set label `BUGS_PC`, and verify the sentinel from Wine.
5. Retry and capture the observed dialog.
6. Locate dialog and `cd.txt` cross-references in Ghidra.
7. Decompile the gate at `0x00403B90` and drive selector at `0x004ADC30`.
8. Use the executable's `log` argument to capture selected root and file path.
9. Place an unchanged executable copy in the derived `PC\BUGS` layout and retry.

## Expected

Either reach application initialization or obtain sufficient static/runtime evidence to explain the blocking media check.

## Observed

- The native executable and DirectX dependency DLLs load under Wine.
- The original game dialog `Please insert A Bug's Life CD.` appears when `cd.txt` loading returns zero.
- The directory-backed `R:` mapping is not accepted by the game's `GetDriveTypeA` scan.
- The game then attempts current-directory fallback path `R:\\cd\cd.txt`, which does not exist at disc root.
- Running the same executable hash from `R:\PC\BUGS` makes fallback path `R:\PC\BUGS\CD\CD.TXT` succeed.
- The game proceeds through DirectDraw/Direct3D selection, selects 640×480×16 fullscreen mode, creates a Windows event/window, and loads `level00\level.raw`.
- Wine reports pixel-format, DirectSound/Quartz, and software-blit compatibility errors after the gate.

## Artifacts

- `reports/wine/EXP-20260811-004-cd-check-analysis.md`
- `dynamic/wine/RUN-WINE-20260811-232444/`
- `dynamic/wine/RUN-WINE-20260811-232940-CDROM-R/observed-dialog.png`
- `dynamic/wine/RUN-WINE-20260811-233536-GAME-LOG/bugs.log`
- `dynamic/wine/RUN-WINE-20260811-233626-INSTALLED-LAYOUT/bugs.log`
- [[FUNC-97C95BA5572D-00403B90]]
- [[FUNC-97C95BA5572D-004ADC30]]
- [[FUNC-97C95BA5572D-004AE240]]

## Addresses

`0x00403B90`, `0x00403C8C`, `0x00403C9E`, `0x00403CA3`, `0x004ADC30`, `0x004ADC73`, `0x004ADD0F`, `0x004AE240`

## File offsets

Not established.

## Interpretation

The CD dialog is not evidence of a generic DRM failure. It is the direct consequence of the content-root selector and a failed `cd.txt` read. Wine's directory-backed type override did not satisfy the drive scan, but the binary's current-directory fallback works from the expected content layout.

## Result

Completed. The executable launches and the CD gate is explained and bypassed without patching by using a correct derived working layout.

## Follow-up

Determine the first stable visible state and isolate the significance of WineD3D pixel-format and Quartz/DirectSound errors.

## Human confirmation

After the installed-layout run, the user visually confirmed that the game was working. This confirms successful visible execution past the CD gate. The observation does not yet establish complete playability, correct audio, rendering fidelity, or long-session stability.

## Uncited setup probes (added 2026-10-12)

Three run folders from this session were cited nowhere. They sit between
`RUN-WINE-20260811-232444` and `RUN-WINE-20260811-233536-GAME-LOG`:

- `RUN-WINE-20260811-232606-WINDOW-PROBE`: window and process listing.
- `RUN-WINE-20260811-232802-CDROM`: CD-ROM drive setup.
- `RUN-WINE-20260811-233235-CD-PROBE`: CD probe.

They are setup probes, not experimental arms. This note's conclusions do not
rest on them.
