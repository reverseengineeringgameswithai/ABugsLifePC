---
type: experiment
id: EXP-20260811-001
date: 2026-08-11
question: Which file on the PC disc is the primary game-executable candidate?
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora host
environment_version: Fedora 44
working_directory: /home/dev/ABLPC
configuration: Read-only 7-Zip ISO listing; selected files extracted to ignored work/copies area
artifacts:
  - reports/disc/BUGS_PC-iso-filesystem.txt
  - reports/disc/BUGS_PC-initial-census.md
  - static/pe/BIN-97c95ba5572dce63/
addresses: []
file_offsets: []
result: candidate identified
created: 2026-08-11
updated: 2026-08-11
tags:
  - re/experiment
  - re/executable
---

# EXP-20260811-001

## Question

Which file on the PC disc is the primary game-executable candidate?

## Binary SHA-256

`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`

## Procedure

1. List `originals/BUGS_PC.ISO` without mounting or modifying it.
2. Separate bundled DirectX, installer, registration, and support executables from title-specific candidates.
3. Extract only `bugs.exe`, `AUTOPLAY.EXE`, `AUTORUN.INF`, `install.ini`, `SETUP.INI`, and `PC/BUGS/CD/CD.TXT` into `work/copies/BUGS_PC-disc/`.
4. Read the launch/configuration text and hash the executable copies.
5. Run the non-modifying PE triage workflow on the `bugs.exe` copy.

## Expected

Installer or autorun metadata will distinguish the title executable from setup/support programs.

## Observed

- `AUTORUN.INF` launches `autoplay.exe`.
- `install.ini` declares `RUN_SOURCE=HD`, `APPNAME=A Bug's Life`, configured `VERSION=1.0`, and `EXE_ENTRY=bugs.exe`.
- `bugs.exe` is an Intel i386 PE32 Windows GUI executable with six sections.
- Full measurements are in `reports/disc/BUGS_PC-initial-census.md`.

## Interpretation

### Confirmed

The installer designates `bugs.exe` as its executable entry and designates `AUTOPLAY.EXE` as a separate autorun path. The extracted `bugs.exe` copy has the recorded hash and PE classification.

### Inferred

Root `bugs.exe` is the primary game-executable candidate.

### Unknown

It is not yet demonstrated that an installed `bugs.exe` is byte-identical to the root disc file. Configured installer version `1.0` is not yet confirmed as an executable version resource.

## Result

Candidate identified. See [[BIN-97c95ba5572dce63 - bugs.exe]].

## Follow-up

Interpret the generated PE triage, import this exact hash into a new Ghidra project, and establish a static baseline before applying PS1-derived hypotheses.
