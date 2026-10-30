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

# Version-bound canonical statement strictness

## Goal

Execute exact M4.41 after the independent M4.40 rejection, changing only the
bounded compatibility-checker strictness and its tests/documentation.

## Result

- Bound the selected historical/active statement paths to exact v0.1/v0.2.
- Required expected object-key order recursively.
- Converted non-string IDs into ordinary `CompatibilityError` failures.
- Added full cross-version, reordered-object, typed-ID, status-2/no-traceback,
  151-value, 151-type, and two-version nine-read regressions.
- Preserved both statement hashes, all five pins, the launcher and manifest
  authorities, and every game-facing behavior.
- Passed 71 focused, 284 combined, and 472 canonical tests. No game file was
  read or executed.
- Final `make check` passed with Vault 293 notes/zero findings, the active
  five-anchor statement, 472 tests, and zero tracked-file violations.

## Durable evidence

See [[EXP-20260814-100 - Version-bound canonical compatibility-statement strictness]],
[[Project Roadmap#M4.41 — Version-bound canonical statement strictness correction]],
and `DEC-20260814-095`.

## Handoff

M4 remains active. Exact M4.42 is a fresh-context, documentation-only hard-
truth audit of the immutable worker and complete M4 evidence ledger. The
worker selects no implementation successor and does not mark M4 complete.
