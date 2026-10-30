---
type: session
date: 2026-08-11
agent: Codex
status: complete
tags:
  - session/research
  - re/executable
---

# Initial PC disc census

## Agent

Codex

## Goal

Identify the primary PC game-executable candidate without modifying the original ISO.

## Files inspected

- `originals/BUGS_PC.ISO` through a read-only 7-Zip listing
- Extracted working copies of `AUTORUN.INF`, `install.ini`, `SETUP.INI`, `PC/BUGS/CD/CD.TXT`, `AUTOPLAY.EXE`, and `bugs.exe`

## Experiments inspected

- [[EXP-20260811-001 - PC disc census and executable identification]]

## Changes made

Created a minimal ignored working copy, generated PE triage, established the Ghidra baseline/export, added the executable dossier and experiment reports, and updated the durable research state.

## Conclusions

- Confirmed: installer metadata names `bugs.exe` as `EXE_ENTRY` and autorun separately launches `AUTOPLAY.EXE`.
- Confirmed: the candidate hash and PE classification recorded in [[BIN-97c95ba5572dce63 - bugs.exe]].
- Inferred: root `bugs.exe` is the primary game executable.

## New hypotheses

None. No PS1 evidence was used.

## Contradictions discovered

None.

## Tests run

Non-modifying ISO listing, SHA-256 hashing, `file(1)` classification, multi-tool PE triage, Ghidra auto-analysis, and reviewable evidence export.

## Unresolved questions

Installed-file equivalence, executable version resources, static dependencies, and runtime behavior.

## Recommended next action

Categorize imports and high-value strings, then create bounded address-based initialization function dossiers.

## Git commit if applicable

Not committed in this session.
