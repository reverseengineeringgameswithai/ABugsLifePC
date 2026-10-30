---
type: experiment
id: EXP-20260814-100
date: 2026-08-14
question: Can the asset-free M4 checker close the exact selected-version, recursive object-order, and malformed-ID strictness failures without changing either statement or any behavior?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; asset-free checker, synthetic JSON, documentation, and tests only
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.41 worker directly above docs-only M4.40 verdict b5a8019082ee6f40930cce2984e424205c8b9ff3; no game execution or protected/game-file reads
artifacts:
  - reimplementation/ablpc/compatibility.py
  - tests/test_compatibility.py
  - reimplementation/compatibility/m4-v0.1.json
  - reimplementation/compatibility/m4-v0.2.json
  - scripts/check-m4-compatibility.py
  - Vault/30-Experiments/EXP-20260814-099 - Independent M4.39 statement and milestone-closure hard-truth audit.md
addresses: []
file_offsets: []
result: worker-complete-version-bound-canonical-statement-strictness
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/compatibility
  - milestone/m4
---

# EXP-20260814-100 - Version-bound canonical compatibility-statement strictness

## Question

Can the asset-free M4 compatibility checker close exactly the four strictness
failures in [[EXP-20260814-099 - Independent M4.39 statement and milestone-closure hard-truth audit]] while preserving both statement files, the five machine
authorities, the nine-read boundary, and every game-facing behavior?

## Configuration and limits

- Parent: docs-only M4.40 rejection `b5a8019082ee6f40930cce2984e424205c8b9ff3`.
- Scope: `reimplementation/ablpc/compatibility.py`, focused compatibility
  regressions, and evidence/documentation only.
- No statement, manifest, receipt, schema, format, operation, pin, authority,
  launcher, asset, runtime, M1, M2, PS1, or game-facing behavior change.
- No game file was read or executed. All hostile inputs were synthetic JSON in
  pytest temporary directories.

## Implementation

1. `_first_difference` now compares the exact key sequence of every object
   after its missing/extra-field checks and before recursion. Canonically
   indented attacker-ordered objects therefore remain invalid rather than
   defining their own canonical order.
2. `validate_compatibility_statement` requires `statement_id` to be a string
   before dictionary lookup. Arrays, objects, integers, and all other
   non-string values raise `CompatibilityError` instead of leaking `TypeError`.
3. `check_compatibility_statement` binds the repository-selected historical
   path to `ablpc-m4-compatibility-v0.1` and active path to
   `ablpc-m4-compatibility-v0.2`. `load_compatibility_statement` accepts the
   resulting explicit expected ID and refuses a complete valid opposite
   version before repository-authority alignment.
4. Focused regressions cover top-level and nested field reordering, complete
   active-path downgrade and historical-path upgrade, list/object/integer IDs,
   CLI status 2 with empty stdout and no traceback, and both selected versions'
   exact nine-read sequence. A separate loop mutates the type at every one of
   v0.2's 151 scalar leaves.

## Results

| Gate | Result |
|---|---|
| top-level/nested reordered objects | 2/2 deterministic refusal |
| selected active downgrade/historical upgrade | 2/2 library and 2/2 CLI refusal |
| list/object/integer statement IDs | 3/3 `CompatibilityError`; CLI list/object 2/2 status 2, empty stdout, no traceback |
| v0.2 scalar value attacks | 151/151 refusal |
| v0.2 scalar type attacks | 151/151 refusal |
| normal active/historical checks | 2/2 pass, five anchors each |
| focused compatibility | 71/71 pass |
| compatibility + manifest + LEVEL | 284/284 pass |
| canonical scoped suite | 472/472 pass |
| final `make check` | Python doctor, Vault 293/0/0, active compatibility, 472 tests, tracked audit 0 |
| diff/protected/game-byte boundary | clean; 14 documentation/README paths plus one checker and one focused test file only |

The combined count is now an exact collected result: 71 compatibility + 198
manifest + 15 LEVEL = 284. This supersedes the stale M4.39 worker count of 266
and the exact pre-correction M4.40 count of 271 without rewriting either
historical observation.

## Preserved authorities

| Artifact | Exact SHA-256 |
|---|---|
| historical v0.1 statement | `c3427d44cf32619a1f9bbcab7c51e67c0846b35d9d53eab7632ff6356c0beaf0` |
| active v0.2 statement | `dacfcab8c1d27e5a63db870f347eb08701f868ca678cafdd178913266f20ccb2` |
| launcher | `68c9171749bd7b207a15b4202193ccfddd2661fbb383deb34b1a5a5a4049977e` |
| manifest implementation | `b3480761ac2b4791ccbf1df69f88234532f27956152045b89615dd5ec5bf6d75` |

The three tracked manifest pins also remain unchanged. Each correct version
check reads exactly its one selected statement plus the same eight enumerated
asset-free authorities. Statement bytes, contents, and declared limitations
are unchanged.

## Interpretation

**Confirmed at the worker boundary:** exact M4.41 closes every M4.40
counterexample family with deterministic compatibility errors while retaining
normal v0.1/v0.2 validation and all existing evidence boundaries.

**Not yet confirmed:** M4 milestone closure. Per the ratchet, a separate
fresh-context verifier must attack the immutable worker and reconcile the
complete capability/exit-gate ledger. No implementation successor is selected
here.

## Disposition

M4.41 is worker-complete and ready for exact independent M4.42. M4 remains
active until that audit accepts the strict checker and the complete milestone
ledger.

## Auditor disposition

[[EXP-20260814-101 - Independent M4.41 selected-path identity hard-truth audit]]
returns `REJECT`. It retains M4.41's regular-file replacement, recursive-order,
typed-ID, exact-byte/pin, normal nine-read, and 71/284/472 evidence, but proves
that resolved-path selection collapses when the default active pathname links
to the historical selected file: the default checker then reports valid v0.1
with status 0. Only lexical selected-path identity plus regular non-link
selected-file correction M4.43 follows.
