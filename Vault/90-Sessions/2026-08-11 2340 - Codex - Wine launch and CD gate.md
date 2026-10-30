---
type: session
date: 2026-08-11
agent: Codex
tags:
  - session/codex
  - re/dynamic
  - environment/wine
---

# 2026-08-11 2340 - Codex - Wine launch and CD gate

## Agent

Codex

## Goal

Launch the original PC executable under Wine, explain the CD-insertion dialog, and test a non-patching path past the gate.

## Files inspected

- Ghidra functions `0x00403B90`, `0x00418FA0`, `0x004190D0`, `0x004A3540`, `0x004ADC30`, and `0x004AE240`
- Wine run metadata/debug logs
- Game-generated `bugs.log`
- User-provided transcript as an external hypothesis source

## Experiments inspected

- `EXP-20260811-003`

## Changes made

- Initialized the baseline Wine prefix.
- Created a full ignored ISO-derived work copy.
- Tested directory-backed CD-ROM mappings.
- Used the game's `log` command-line option.
- Created `EXP-20260811-004`, two function dossiers, and a runtime analysis report.
- Repaired the malformed first-run note.
- Preserved the observed dialog screenshot.

## Conclusions

- The executable launches under Wine.
- The media dialog is a failed `cd.txt` load, not an unexplained loader failure.
- `0x004ADC30` scans for the first CD-ROM drive, but the Wine directory mapping was not accepted.
- Current-directory fallback tried the wrong path at disc root.
- The unchanged executable passes the gate from the derived `PC\BUGS` layout and reaches DirectX/window/level loading.

## New hypotheses

- The derived `PC\BUGS` tree approximates the installed runtime layout.
- A block-device-backed CD mapping may take the intended CD path.
- Remaining issues are graphics/audio compatibility rather than the media sentinel.

## Contradictions discovered

Wine reported the mapped volume label and sentinel correctly through `cmd`, but the game logged `No CD-ROM found.` The mapping's visible filesystem identity and `GetDriveTypeA` acceptance are therefore distinct.

## Tests run

- Seven bounded Wine runs.
- Focused Ghidra string-xref and decompiler inspections.
- Game internal log capture.
- Hash comparison of the executable work copy.

## Unresolved questions

- First stable rendered state reached.
- Effect of WineD3D pixel-format warnings.
- Effect of Quartz/DirectSound failures.
- Behavior after running the retail installer.
- Behavior with a real CD block device and in Windows 98.

## Recommended next action

Capture and classify the first visible state from the successful installed-layout baseline.

## Git commit if applicable

`fe4ca44 research: document Wine launch and CD sentinel behavior`

## Post-session confirmation

The user visually confirmed a working game state from the derived `PC\BUGS` layout. Full playability, audio correctness, rendering fidelity, and long-session stability remain untested.
