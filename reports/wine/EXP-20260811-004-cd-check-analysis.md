# Wine launch and CD-check analysis

## Subject

- Experiment: `EXP-20260811-004`
- Binary: `BIN-97c95ba5572dce63`
- SHA-256: `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Environment: `wine-11.0 (Staging)`
- Prefix: `work/wine/baseline`

## Confirmed static path

At `0x00403B90`:

1. Command-line options are parsed.
2. Configuration state is initialized.
3. `0x004ADC30` selects a content root.
4. `0x004AE240("cd.txt", local_buffer)` attempts a whole-file read.
5. A zero return displays `Please insert A Bug's Life CD.` with `MessageBoxA`.
6. The failure path calls the process-exit routine.

At `0x004ADC30`:

1. The current directory is recorded.
2. `GetDriveTypeA(NULL)` checks the current drive.
3. If it is not `DRIVE_CDROM` (5), the function scans `C:\` through `Z:\`.
4. The scan stops at the first drive returning 5.
5. If no drive returns 5, the content-root flag remains in the current-directory mode.
6. The scan does not verify `CD.TXT` before accepting a CD-ROM drive.

Evidence: focused Ghidra cross-references and decompilation in `EXP-20260811-004`.

## Confirmed runtime behavior

### Directory-backed CD-ROM attempt

Wine was configured with:

- Drive: `R:`
- Type override: `cdrom`
- Volume label: `BUGS_PC`
- Verified file: `R:\PC\BUGS\CD\CD.TXT`

The game still displayed the media dialog.

With the executable's own `log` option, `RUN-WINE-20260811-233536-GAME-LOG` recorded:

```text
LOADING : App run from R:\.
LOADING : No CD-ROM found.
LOAD : Loading file R:\\cd\cd.txt.
FATAL ERROR - Failed to load file R:\\cd\cd.txt - error was No such file or directory.
```

This confirms that Wine's directory mapping and registry type override did not cause the game's `GetDriveTypeA` path to accept `R:` as CD-ROM. The failure is path-root selection, not corrupt `CD.TXT`.

### Installed-layout work copy

An unchanged, hash-verified executable copy was placed under the derived work-copy path `R:\PC\BUGS` and run from that directory. No executable bytes were patched.

`RUN-WINE-20260811-233626-INSTALLED-LAYOUT` recorded:

```text
LOADING : App run from R:\PC\BUGS.
LOADING : No CD-ROM found.
LOAD : Loading file R:\PC\BUGS\cd\cd.txt.
INFO Direct3D - Hardware driver >>>Direct3D HAL, Wine D3DDevice using WineD3D and OpenGL<<< selected
INFO Screen mode 640x480x16 selected.
EVENT : Event >>>WINDOWS<<< create function called.
LOAD : Loading file R:\PC\BUGS\cd\level00\level.raw.
```

This confirms that the fallback current-directory path gets past the media sentinel when the executable is run from the expected `PC\BUGS` layout.

## Run inventory

| Run ID | Purpose | Result |
|---|---|---|
| `RUN-WINE-20260811-232444` | First sparse-copy launch | Native executable and DirectX DLLs loaded; media dialog observed |
| `RUN-WINE-20260811-232606-WINDOW-PROBE` | Quiet process/window probe | `xwininfo` unavailable; no useful window evidence |
| `RUN-WINE-20260811-232802-CDROM` | Initial `D:` directory mapping | Invalidated by Wine removing the conflicting `D:` link during device discovery |
| `RUN-WINE-20260811-232940-CDROM-R` | Verified `R:` label and sentinel | Same media dialog; screenshot retained |
| `RUN-WINE-20260811-233235-CD-PROBE` | Wine file/drive/mount trace | Shows host mount-manager discovery; trace is noisy and not sufficient alone |
| `RUN-WINE-20260811-233536-GAME-LOG` | Built-in game log at disc root | Confirmed no CD-ROM selected and failed `R:\\cd\cd.txt` |
| `RUN-WINE-20260811-233626-INSTALLED-LAYOUT` | Unchanged executable in `PC\BUGS` | Passed sentinel, initialized DirectX, created window, loaded level data |

## External lead

A user-provided transcript proposed that the game chooses the first drive for which `GetDriveTypeA` returns 5 and then assumes it is the game disc. That lead was treated as a hypothesis.

The exact scan behavior was independently confirmed in this PC binary at `0x004ADC30`. In the current Wine run, however, the game reported that it found no CD-ROM at all. The external transcript did not establish the runtime result.

## Interpretation

### Confirmed

- The executable launches under Wine.
- The original media dialog is a failed `cd.txt` load at `0x00403B90`.
- `0x004ADC30` scans for the first Win32 CD-ROM drive without checking content first.
- The current Wine directory/type mapping is not accepted as `DRIVE_CDROM` by this game path.
- The current-directory fallback works when an unchanged executable copy is run from the derived `PC\BUGS` layout.
- The game then reaches DirectDraw/Direct3D selection, window creation, and level-data loading.

### Inferred

- The disc's `PC\BUGS` tree is an expected installed/runtime layout or is compatible with one.
- A real block-device/ISO mount exposed as a Wine CD-ROM would likely take the CD-root branch, but this has not been demonstrated.

### Unknown

- Whether running the original installer under Wine creates the same working layout.
- Why the Wine 11 directory-backed type override is not reflected in this executable's `GetDriveTypeA` result.
- Whether a real loop-mounted ISO or physical optical drive passes the scan without layout fallback.
- The first visible rendered state reached in the installed-layout run.
- Impact of WineD3D pixel-format warnings and Quartz/DirectSound failures.

## Safety

No original file was modified. No executable was patched. All extraction, executable copying, Wine prefix changes, and runtime artifacts are confined to ignored work/generated paths.

## Human observation

The user subsequently confirmed that the installed-layout run produced a working game state. Scope remains limited: this does not yet confirm audio correctness, rendering fidelity, input coverage, or stability beyond the observed run.
