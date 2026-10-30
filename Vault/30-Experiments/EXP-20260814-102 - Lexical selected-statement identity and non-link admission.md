---
type: experiment
id: EXP-20260814-102
date: 2026-08-14
question: Can selected M4 compatibility-statement identity derive from the lexical repository path while selected links refuse before content reads and arbitrary unselected exact links retain prior behavior?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; asset-free checker, synthetic temporary paths, documentation, and tests only
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.43 worker directly above docs-only M4.42 verdict 18a3a4c2fbf2bb9fcba4920526b5ed7649391edd; no game execution or protected/game-file reads
artifacts:
  - reimplementation/ablpc/compatibility.py
  - tests/test_compatibility.py
  - reimplementation/compatibility/m4-v0.1.json
  - reimplementation/compatibility/m4-v0.2.json
  - Vault/30-Experiments/EXP-20260814-101 - Independent M4.41 selected-path identity hard-truth audit.md
addresses: []
file_offsets: []
result: worker-complete-lexical-selected-path-non-link-admission
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/compatibility
  - milestone/m4
---

# EXP-20260814-102 - Lexical selected-statement identity and non-link admission

## Question and boundary

Exact M4.42 proved that resolved-target comparison lets the default active path
link to the historical selected file and validate v0.1. M4.43 asks only whether
lexical selected-path identity plus final non-link regular-file admission closes
that case without changing arbitrary unselected paths or any M4 behavior.

The executable hash above is provenance only. No executable, game asset,
original, media, work copy, runtime, or PS1 source was read or executed.

## Change

`check_compatibility_statement` now normalizes the requested path and repository
root lexically with `abspath`, without following the final target, and selects
v0.1/v0.2 only by equality with the two lexical repository paths. When a path
is selected, `lstat` must report a regular file before any content read; a link
or other nonregular final entry raises `CompatibilityError`. Unselected paths
retain the existing loader behavior and are not subjected to a new link policy.

Synthetic regressions cover both selected link directions, place a read trap
on the selected link, and require library refusal plus CLI status 2, empty
stdout, deterministic stderr, and no traceback. Separate v0.1/v0.2 unselected
links remain valid, while the existing normal selected/read-count, version-
swap, key-order, typed-ID, canonical-input, and authority cases remain green.

## Results

| Gate | Result |
|---|---|
| active link to historical / historical link to active | 2/2 refuse before content read |
| selected-link CLI contract | 2/2 status 2, empty stdout, no traceback |
| arbitrary unselected exact links | v0.1 and v0.2 both retain acceptance |
| normal selected statements | v0.1/v0.2 valid; exactly nine reads each |
| focused compatibility | 75/75 pass |
| compatibility + manifest + LEVEL | 288/288 pass |
| canonical scoped suite | 476/476 pass |
| final `make check` | Python doctor, Vault 297/0/0, active five-anchor statement, 476 tests, tracked audit 0 |

Both statement bytes/hashes, all five authority pins, the launcher, manifest
implementation, restoration boundary, unsupported declarations, and all game-
facing behavior are unchanged.

## Interpretation and disposition

**Confirmed at the worker boundary:** M4.43 closes exactly the M4.42 selected-
link contradiction and preserves the explicitly unselected-path behavior.

**Not yet confirmed:** final compatibility publication and M4 closure. Exact
fresh-context M4.44 must audit the immutable worker and the already reconciled
eight-of-nine/four-of-five ledger. M4 remains Active; no implementation
successor is selected here.
