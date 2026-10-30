# BUGS_PC initial disc census

- Experiment: `EXP-20260811-001`
- Source ISO: `originals/BUGS_PC.ISO`
- ISO SHA-256: `b0c3da82688c511f920a5559bdc3dcb8354d253182790a239665c8cd080d9ed9`
- ISO size: 533,114,880 bytes
- ISO label: `BUGS_PC`
- Filesystem listing: `reports/disc/BUGS_PC-iso-filesystem.txt`
- Working-copy root: `work/copies/BUGS_PC-disc/`

## Confirmed

- `AUTORUN.INF` contains `OPEN=autoplay.exe`; `AUTOPLAY.EXE` is the disc autorun launcher.
- `install.ini` identifies the application as `A Bug's Life`, declares `RUN_SOURCE=HD`, declares configured title `VERSION=1.0`, and names `EXE_ENTRY=bugs.exe`.
- The root `bugs.exe` working copy is 1,069,056 bytes.
- `file(1)` identifies it as an Intel i386 PE32 GUI executable for Windows 4.00 with six sections.
- Working-copy `bugs.exe` SHA-256: `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Working-copy `AUTOPLAY.EXE` SHA-256: `f1531c6ba8d81c1bbaa56a2537bf4a4fce9ad2a3ce13e8dd82a80d74625a04ee`.
- Automated PE triage was generated under `static/pe/BIN-97c95ba5572dce63/`.

## Inferred

- Root `bugs.exe` is the leading game-executable candidate because the installer names it as `EXE_ENTRY` and distinguishes it from the autorun launcher.

## Unknown

- Whether installation copies root `bugs.exe` byte-for-byte or transforms/replaces it has not been demonstrated.
- The executable's own version resource, linker/compiler provenance, image base, entry point, imports, and runtime behavior have not yet been interpreted.
- Game-data files required for a baseline run have not yet been selected or copied.

No source file under `originals/` was modified.
