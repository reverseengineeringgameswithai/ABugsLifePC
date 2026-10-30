---
type: session
date: 2026-08-11
agent: Codex
tags:
  - session/codex
  - re/static
---

# 2026-08-11 2316 - Codex - PC-native baseline mapping

## Agent

Codex

## Goal

Create the durable project charter and establish the first PC-native map of imports, high-value strings, initialization, file access, and DirectX setup before any PS1 comparison.

## Files inspected

- `static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json`
- PE triage metadata for `BIN-97c95ba5572dce63`
- Ghidra program `bugs.exe` at seven focused addresses

## Experiments inspected

- `EXP-20260811-001`
- `EXP-20260811-002`

## Changes made

- Added [[Project Charter]] with mission, evidence hierarchy, phases, hygiene rules, and a PC-first cross-port gate.
- Added categorized import and high-value-string reports.
- Added seven address-based function dossiers.
- Added `EXP-20260811-003`.
- Updated agent entry points, MOCs, known unknowns, and [[Current State]].

## Conclusions

- The PC executable now has a defensible first-pass platform map.
- The runtime entry path, whole-file loader candidate, low-level runtime open wrapper, DirectDraw resolution path, and broader Direct3D setup path are separated.
- No PS1-derived evidence was needed or used.

## New hypotheses

- `0x0043DA40` is the first WinMain-like game initialization candidate.
- `0x004AE240` is a general whole-file loader into caller-owned storage.
- `0x00423A20` is the central Direct3D device setup function.

## Contradictions discovered

The current Ghidra evidence exporter reports zero external imports, while independent PE parsing reports 150. This is an exporter coverage limitation, documented in the import report.

## Tests run

No repository test suite was run. Focused Ghidra headless decompilation and independent PE import extraction were executed as static-analysis procedures.

## Unresolved questions

- Exact role and immediate callees of `0x0043DA40`.
- Actual runtime content-root choice.
- First files loaded and their caller addresses.
- Actual DirectDraw/Direct3D device, mode, and fallback selected under Wine and Windows 98.
- Exact C runtime/toolchain version.

## Recommended next action

Run a controlled baseline Wine startup capture tied to a new experiment, without wrappers or compatibility overrides.

## Git commit if applicable

None.
