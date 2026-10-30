---
type: experiment
id: EXP-20260811-002
date: 2026-08-11
question: Can the exact PC executable candidate be reproducibly imported, analyzed, and exported from Ghidra without semantic mutation?
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora host, Ghidra headless
environment_version: Ghidra 12.1.2; Temurin 21.0.12+8 LTS
working_directory: /home/dev/ABLPC
configuration: Default Ghidra PE auto-analysis; no PDB; no semantic renaming
artifacts:
  - reports/ghidra/BIN-97c95ba5572dce63-import.log
  - reports/ghidra/BIN-97c95ba5572dce63-export.log
  - reports/ghidra/BIN-97c95ba5572dce63-baseline.md
  - static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json
addresses: []
file_offsets: []
result: succeeded
created: 2026-08-11
updated: 2026-08-11
tags:
  - re/experiment
  - re/static-analysis
---

# EXP-20260811-002

## Question

Can the exact PC executable candidate be reproducibly imported, analyzed, and exported from Ghidra without semantic mutation?

## Procedure

1. Create an ignored project named `ABLPC_BUGS_97c95ba5` under `work/ghidra/`.
2. Import the exact `bugs.exe` candidate from `work/copies/BUGS_PC-disc/`.
3. Run default Ghidra PE auto-analysis.
4. Export address-based functions, call relationships, references, strings, imports, and decompiler text using `ExportEvidence.java`.

## Expected

Ghidra should load the PE, complete baseline analysis, and produce reviewable evidence without changing the original or assigning speculative semantic names.

## Observed

- Portable Executable load succeeded with language/compiler model `x86:LE:32:default:windows`.
- Eight imported libraries were identified: DirectDraw, DirectInput, DirectSound, GDI32, KERNEL32, OLE32, USER32, and WinMM.
- Auto-analysis completed successfully in approximately 41 seconds.
- No PDB was found in configured locations.
- The JSON evidence export completed successfully.

## Interpretation

### Confirmed

The exact candidate hash has a reproducible Ghidra baseline and reviewable export. See `reports/ghidra/BIN-97c95ba5572dce63-baseline.md`.

### Inferred

The library set is consistent with a native Windows multimedia game using DirectDraw, DirectInput, and DirectSound, but no particular engine architecture is yet established.

### Unknown

Imported-symbol roles, entry-point behavior, function semantics, data formats, and PS1 correspondence remain unknown.

## Result

Succeeded.

## Follow-up

Categorize imports and high-value strings, retaining address-based names and separating platform scaffolding from game-specific candidates.
