# BIN-97c95ba5572dce63 Ghidra baseline

- Experiment: `EXP-20260811-002`
- Binary SHA-256: `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Binary MD5 reported by Ghidra: `01028a9f85a0732f964786d0cd7d339d`
- Ghidra: 12.1.2
- Java: Eclipse Temurin 21.0.12+8 LTS
- Project: `work/ghidra/ABLPC_BUGS_97c95ba5`
- Reviewable export: `static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json`
- Import log: `reports/ghidra/BIN-97c95ba5572dce63-import.log`
- Export log: `reports/ghidra/BIN-97c95ba5572dce63-export.log`

## Confirmed

- Ghidra loaded the file with its Portable Executable loader.
- Ghidra selected `x86:LE:32:default:windows`.
- Imported libraries recorded during load: `DDRAW.DLL`, `DINPUT.DLL`, `DSOUND.DLL`, `GDI32.DLL`, `KERNEL32.DLL`, `OLE32.DLL`, `USER32.DLL`, and `WINMM.DLL`.
- Auto-analysis completed and the project saved successfully.
- The reviewable evidence exporter completed, covering address-based function metadata, callers, callees, data references, strings, imports, and decompiler text.
- Ghidra did not find a PDB in its configured locations.

## Cautions

- Ghidra applied its `windows_vs12_32` data-type archive. This is analyzer configuration, not evidence that the 1998 executable was built with Visual Studio 2013/VS12.
- Missing imported library files in the Ghidra project do not mean the game cannot load them on Windows; only external symbol linkage inside this isolated project was unavailable.
- Auto-generated function boundaries and decompiler output remain evidence to review, not confirmed source structure.

## Next bounded task

Categorize imported symbols and high-value strings, then identify a small set of address-based candidate initialization functions without assigning semantic names.
