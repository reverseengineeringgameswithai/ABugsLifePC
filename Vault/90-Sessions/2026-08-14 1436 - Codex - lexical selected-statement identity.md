---
type: session
date: 2026-08-14
agent: Codex
status: completed
tags:
  - session
  - implementation/modding
  - implementation/compatibility
---

# Lexical selected-statement identity

## Goal

Execute exact M4.43 after M4.42's selected-path link rejection.

## Result

- Derived selected v0.1/v0.2 identity from normalized lexical repository paths.
- Required each selected final statement entry to be a regular non-link file
  before any content read.
- Rejected both selected link directions through library and CLI contracts,
  while retaining v0.1/v0.2 unselected exact-link behavior.
- Passed 75 focused, 288 combined, and 476 canonical tests.
- Final `make check` passed with Vault 297 notes/zero findings, active
  five-anchor validation, 476 tests, and zero tracked-file violations.
- Preserved both statements, five pins, nine-read normal checks, authorities,
  unsupported declarations, and all game-facing behavior.

## Durable evidence and handoff

See [[EXP-20260814-102 - Lexical selected-statement identity and non-link admission]],
`DEC-20260814-097`, and
[[Project Roadmap#M4.43 — Lexical selected-statement identity and non-link file correction]].
M4 remains active on fresh audit/docs-only M4.44; the worker does not declare
completion or select an implementation successor.
