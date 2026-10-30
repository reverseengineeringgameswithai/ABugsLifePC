# Project-local Ghidra

| Field | Value |
|---|---|
| Installed version | 12.1.2, public build 20260605 |
| Download/source | Official NSA Ghidra GitHub release |
| Archive SHA-256 | `b62e81a0390618466c019c60d8c2f796ced2509c4c1aea4a37644a77272cf99d` |
| Java version | Eclipse Temurin 21.0.12+8 LTS, project-local JDK |
| Install date | 2026-08-11 |
| Launch command | `scripts/ghidra-gui.sh` |
| Headless command | `scripts/ghidra-headless.sh ...` |
| PyGhidra command | `scripts/pyghidra.sh` |

PyGhidra 3.1.0 and JPype1 1.5.2 are installed in the isolated, Git-ignored `tools/ghidra/.venv`. Downloaded contents and databases are Git-ignored. Game projects belong in `work/ghidra/`. Use `scripts/ghidra-export.sh` to export reviewable evidence into `static/exports/`; do not use direct database mutation as the main agent workflow.
