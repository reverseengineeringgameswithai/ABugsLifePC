---
type: executable
id: BIN-97c95ba5572dce63
sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
source_iso_sha256: b0c3da82688c511f920a5559bdc3dcb8354d253182790a239665c8cd080d9ed9
source_path: bugs.exe
size: 1069056
platform: Windows PC
architecture: Intel i386 PE32
status: confirmed
confidence: high
evidence:
  - EXP-20260811-001
  - EXP-20260811-003
  - EXP-20260811-004
  - reports/disc/BUGS_PC-initial-census.md
created: 2026-08-11
updated: 2026-10-02
tags:
  - re/executable
---

# BIN-97c95ba5572dce63 - bugs.exe

## Identity

- SHA-256: `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Size: 1,069,056 bytes
- Disc path: `bugs.exe`
- Working-copy path: `work/copies/BUGS_PC-disc/bugs.exe`
- Triage path: `static/pe/BIN-97c95ba5572dce63/`

## Confirmed

- `EXP-20260811-001`: installer metadata names `bugs.exe` as `EXE_ENTRY` and declares `RUN_SOURCE=HD`.
- `file(1)` identifies this exact hash as an Intel i386 PE32 Windows GUI executable with six sections.
- `EXP-20260811-002`: Ghidra 12.1.2 loaded it as `x86:LE:32:default:windows`, completed auto-analysis, and exported reviewable evidence.
- Imported libraries: `DDRAW.DLL`, `DINPUT.DLL`, `DSOUND.DLL`, `GDI32.DLL`, `KERNEL32.DLL`, `OLE32.DLL`, `USER32.DLL`, and `WINMM.DLL`.

## Inferred

- This is the leading primary game-executable candidate.
  *Update (2026-10-02 audit):* confirmed by a second, runtime form.
  [[EXP-20260811-004 - Wine launch and CD sentinel gate]] ran the unchanged
  hash-verified copy from the installed layout to visible play under Wine,
  and every later runtime experiment uses this hash or a derivative of it.

## Unknown

- Installed-file equivalence.
- Executable version resource.
- Compiler and linker provenance. Ghidra's applied `windows_vs12_32` archive is not compiler-version evidence.
- Image base, entry-point behavior, section purpose, imported-symbol roles, and subsystem relationships.
  *Partly answered since:* image base `0x00400000`
  (`static/pe/BIN-97c95ba5572dce63/rabin2-info.json`, `baddr`); entry VA
  `0x004B1670` dispatching toward `0x0043DA40` and a first import
  categorization (`static/imports/BIN-97c95ba5572dce63/import-categories.md`)
  in [[EXP-20260811-003 - PC-native import string and function map]]. Section
  purpose and complete subsystem relationships remain open.
- Runtime behavior and Wine/Win98 compatibility. *Wine:* runs under Wine
  ([[EXP-20260811-004 - Wine launch and CD sentinel gate]]); see
  [[Environment Status]] for the current runtime. Win98 compatibility remains
  untested here.
- Relationship to PS1 code or data.

## Related experiments

- [[EXP-20260811-001 - PC disc census and executable identification]]
- [[EXP-20260811-002 - Ghidra static baseline]]
- [[EXP-20260811-003 - PC-native import string and function map]]
- [[EXP-20260811-004 - Wine launch and CD sentinel gate]]

## Next discriminating experiment

Categorize imported symbols and high-value strings, then select a bounded set of address-based initialization candidates without semantic renaming.

Done 2026-08-11 in [[EXP-20260811-003 - PC-native import string and function map]]; this
section is historical.
