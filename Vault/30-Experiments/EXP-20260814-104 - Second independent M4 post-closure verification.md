---
type: experiment
id: EXP-20260814-104
date: 2026-08-14
question: Does a second independent verification find any in-scope contradiction to M4 closure as recorded at exact post-closure HEAD?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; asset-free tracked sources and synthetic temporary trees only
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: independent post-closure verification of 33c7c25cd867830af2621f6b7254dc7d8d80bdba over direct parent 6659f865960d56b0ccafcdd44bffd7e96a5333a8; initially clean; documentation-only disposition; no game execution or protected/game-file reads
artifacts:
  - reimplementation/ablpc/compatibility.py
  - scripts/check-m4-compatibility.py
  - tests/test_compatibility.py
  - reimplementation/compatibility/m4-v0.1.json
  - reimplementation/compatibility/m4-v0.2.json
  - Vault/30-Experiments/EXP-20260814-086 - M4 v0.1 milestone-closure evidence audit.md
  - Vault/30-Experiments/EXP-20260814-092 - Independent M4.32 receipt-chain-closure hard-truth audit.md
  - Vault/30-Experiments/EXP-20260814-097 - Independent M4.37 complete-tree-uniqueness hard-truth audit.md
  - Vault/30-Experiments/EXP-20260814-103 - Independent M4.43 selected-path and milestone-closure hard-truth audit.md
addresses: []
file_offsets: []
result: accept-second-independent-confirmation-of-bounded-m4-closure
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/compatibility
  - audit/hard-truth
  - milestone/m4
---

# EXP-20260814-104 - Second independent M4 post-closure verification

## Verdict

**ACCEPT.** A fresh reconstruction at exact post-closure HEAD finds M4 still
supports all nine required capabilities and all five exit gates at the stated
asset-free, exact-hash, manifest/source-authenticated current-x86_64-Linux
boundary. No in-scope contradiction survives. This confirms, rather than
broadens, `EXP-20260814-103`; no successor milestone is activated.

Post-`lstat` replacement/concurrency and a general parent-filesystem policy are
not accepted features. Unlisted hashes, untested systems, N-way composition,
general dry-run/launch/runtime automation, whole staged-tree/source deletion,
external-receipt full-tree restoration, provenance, POSIX metadata equality,
backup, rollback, packaging, transactions, and general Windows path policy
also remain unsupported.

## Independent statement and selected-path results

- v0.1 remains 6,177 canonical bytes at
  `c3427d44cf32619a1f9bbcab7c51e67c0846b35d9d53eab7632ff6356c0beaf0`;
  v0.2 remains 7,677 canonical bytes at
  `dacfcab8c1d27e5a63db870f347eb08701f868ca678cafdd178913266f20ccb2`.
- Independent traversal counts 19/21 ordered objects and 126/151 scalar
  leaves. All 40 single-object rotations, 277 scalar-value changes, and 277
  scalar-type changes reject. Six non-string ID types and eight duplicate,
  malformed, non-finite, or noncanonical JSON classes take the ordinary CLI
  status-2, stderr-only, no-traceback path.
- The semantic delta is exactly the statement/toolkit version, appended
  `restore` workflow, inserted restoration boundary, and restoration-specific
  unsupported split/expansion. The five anchors are unchanged.
- Both selected versions accept as normal absolute and relative paths and
  through lexical dot/dot-dot forms. Both selected link directions, dangling
  links, directories, FIFOs, and Unix sockets reject before any statement
  content read; cross-version regular bytes reject after exactly one read.
- Same-version hard-linked selected content accepts and opposite-version hard-
  linked content rejects. Exact final regular entries below parent-directory
  or repository-root links accept, while opposite-version bytes still reject.
  This confirms the explicit final-entry boundary and does not promote a
  general parent-topology policy.
- Arbitrary unselected exact v0.1/v0.2 regular and linked paths retain library
  and CLI acceptance. Both normal selected versions read exactly the selected
  statement followed by the same eight authorities, once each and in order.
- All five machine-authority hashes match their pinned values.

The separately authored temporary-tree harness completed 663 assertions.

## Reconstructed M4 ledger

| Required capability | Independent disposition |
|---|---|
| Inspect supported formats and executable/data compatibility | **Supported, bounded:** accepted prefix-only LEVEL, bounded read-only ANM, and opaque exact replacement evidence (`EXP-20260814-063/083`). |
| Compose manifests and detect conflicting edits | **Supported:** exactly two manifests and byte-span/opaque conflict reporting, without N-way or semantic solving (`EXP-20260814-067`). |
| Validate input hashes and format versions | **Supported:** exact hashes, schemas 1/2, two formats, and four operations only (`EXP-20260814-063/083`). |
| Dry-run affected files, records, and ranges | **Supported, bounded:** one existing manifest and no output simulation, persistence, or receipt (`EXP-20260814-085`). |
| Stage a complete copy or sparse overlay without touching originals | **Supported:** accepted deterministic preflight, with post-preflight failure/concurrency explicitly non-transactional (`EXP-20260814-063`). |
| Launch the tested Wine/Gamescope configuration | **Supported, manually gated:** pinned launcher scope plus manual renderer/log acceptance (`EXP-20260812-007/029`; `EXP-20260814-083`). |
| Emit receipts sufficient to reproduce and remove a mod | **Supported at the strict current-receipt sparse boundary:** no provenance or full-tree receipt restoration (`EXP-20260814-092`). |
| Test parsers with synthetic fixtures and a user-owned corpus | **Supported:** tracked asset-free tests plus recorded local gates (`EXP-20260814-063/067/077/097`). |
| Document limitations, unsupported fields, and runtime scope | **Supported, bounded:** exact v0.1/v0.2, lexical selected identity, final-entry admission, pins, Wine scope, and explicit unsupported list (`EXP-20260814-099/101/103/104`). |

| Exit gate | Independent disposition |
|---|---|
| Two useful mod classes, including one beyond position editing | **Supported:** guarded payload rebind and opaque whole-file replacement (`EXP-20260812-010/033`; `EXP-20260814-063`). |
| Two independently created manifests compose or conflict deterministically | **Supported:** exact two-input boundary (`EXP-20260814-067`). |
| Install, validate, launch-readiness check, and remove from one clean derived copy | **Supported only for exact-source `stage`, pinned-launcher dry-run, and same-tree manifest/source `restore` on current Linux (`EXP-20260814-097`).** |
| No original/game/machine-state material is packaged | **Supported:** tracked/protected/MIME/no-game-byte gates; user-owned outputs remain undistributable. |
| Versioned compatibility statement names hashes and Wine scope | **Supported, bounded:** both exact statements, five anchors/pins, eight aligned authorities, selected-path/version enforcement, and explicit unsupported scope. |

The reconstructed total is 9/9 capabilities and 5/5 exit gates without
combining evidence beyond its recorded boundary.

## Validation

| Gate | Result |
|---|---|
| independent synthetic matrix | 663 assertions pass |
| focused compatibility | 75/75 pass |
| compatibility + manifest + LEVEL | 288/288 pass |
| canonical `.venv/bin/python -m pytest -q tests` | 476/476 pass |
| `make m4-compatibility` | active v0.2 valid with five anchors |
| `make check` | Python doctor, Vault, compatibility, canonical tests, and tracked audit pass |
| diff/MIME/protected-path/no-game-byte/clean-tree | pass on the documentation-only verdict commit |

No unscoped pytest command, launcher, executable, original, media, work-copy,
PS1 source, or game input was read or executed.
