---
type: experiment
id: EXP-20260811-003
date: 2026-08-11
question: Which PC-native imports, strings, and address-based functions provide the first defensible map of process initialization, file access, and DirectX setup?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora host
result: first-pass-pc-native-map
tags:
  - re/experiment
  - re/static
---

# EXP-20260811-003 - PC-native import, string, and function map

## Question

Which PC-native imports, strings, and address-based functions provide the first defensible map of process initialization, file access, and DirectX setup?

## Binary SHA-256

`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`

## Environment

Fedora host using Ghidra 12.1.2 headless analysis and radare2/rabin2 PE metadata.

## Environment version

See [[Environment Status]].

## Working directory

`/home/dev/ABLPC`

## Configuration

- Ghidra project: `work/ghidra/ABLPC_BUGS_97c95ba5.gpr`
- Program: `bugs.exe`
- Analysis used existing project data with no semantic renames.
- PS1 repository was not inspected or used for conclusions.

## Procedure

1. Read PE image base, entry RVA, architecture, subsystem, and import table.
2. Categorize high-priority imports by platform role.
3. Search the Ghidra evidence export for high-value path, media, and DirectX strings.
4. Rank functions by direct call/string evidence.
5. Decompile only the selected addresses and record callers, callees, and referenced strings.
6. Create dossiers that separate confirmed operations, inferred roles, and unknowns.

## Expected

A bounded PC-native map with enough evidence to define runtime experiments and to gate future cross-port comparisons.

## Observed

- PE entry VA is `0x004B1670`; it performs runtime startup and dispatches toward `0x0043DA40`.
- The PE contains 150 import records.
- DirectX creation/enumeration imports include DirectDraw, DirectInput, and DirectSound entry points.
- `0x0041F990` creates an `Examining Machine` window and enumerates/selects DirectDraw/Direct3D candidates.
- `0x004129A0` combines message processing, display-mode transitions, and content-root path construction.
- `0x004AE240` constructs a path and reads a complete file into a supplied destination.
- `0x004B8B50` is low-level Win32/runtime file-descriptor support, not presently a game-specific loader.
- `0x00411D00` is a DirectDraw resolution/surface setup candidate.
- `0x00423A20` is a broader Direct3D device/surface/viewport setup candidate.
- `0x004671D0` references level DAT/RAW families and calls the loader path.

## Artifacts

- `static/imports/BIN-97c95ba5572dce63/import-categories.md`
- `static/strings/BIN-97c95ba5572dce63/high-value-strings.md`
- Function dossiers `FUNC-97C95BA5572D-004B1670`, `0041F990`, `004129A0`, `004AE240`, `004B8B50`, `00411D00`, and `00423A20`
- Existing Ghidra export: `static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json`
- Existing PE triage: `static/pe/BIN-97c95ba5572dce63/`

## Addresses

`0x004B1670`, `0x0043DA40`, `0x0041F990`, `0x004129A0`, `0x004AE240`, `0x004B8B50`, `0x00411D00`, `0x00423A20`, `0x004671D0`

## File offsets

Not established in this experiment.

## Interpretation

The first PC-native platform map is sufficient to choose targeted runtime breakpoints. It is not proof of full subsystem boundaries, source names, structure layouts, or runtime-selected devices.

## Result

Completed. The next research phase should obtain PC runtime evidence before using PS1 comparison for any specific unknown.

## Follow-up

Capture a baseline Wine startup run and record the transition from `0x0043DA40` through capability selection, content-root selection, initial file loads, and DirectX setup.
