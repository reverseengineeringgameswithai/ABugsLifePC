---
type: experiment
id: EXP-20260814-103
date: 2026-08-14
question: Does immutable M4.43 preserve lexical selected-version identity, refuse selected nonregular final entries before content reads, retain unselected exact contracts, and close the final M4 compatibility row without inference?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; tracked-only disposable repository copies and asset-free documentation/tests
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: fresh-context exact M4.44 audit of immutable M4.43 worker 6659f865960d56b0ccafcdd44bffd7e96a5333a8 with direct parent 18a3a4c2fbf2bb9fcba4920526b5ed7649391edd; documentation-only verdict; no game execution or protected/game-file reads
artifacts:
  - reimplementation/ablpc/compatibility.py
  - scripts/check-m4-compatibility.py
  - tests/test_compatibility.py
  - reimplementation/compatibility/m4-v0.1.json
  - reimplementation/compatibility/m4-v0.2.json
  - Vault/30-Experiments/EXP-20260814-086 - M4 v0.1 milestone-closure evidence audit.md
  - Vault/30-Experiments/EXP-20260814-092 - Independent M4.32 receipt-chain-closure hard-truth audit.md
  - Vault/30-Experiments/EXP-20260814-097 - Independent M4.37 complete-tree-uniqueness hard-truth audit.md
  - Vault/30-Experiments/EXP-20260814-101 - Independent M4.41 selected-path identity hard-truth audit.md
  - Vault/30-Experiments/EXP-20260814-102 - Lexical selected-statement identity and non-link admission.md
addresses: []
file_offsets: []
result: accept-m4-at-documented-current-linux-asset-free-boundary
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/compatibility
  - audit/hard-truth
  - milestone/m4
---

# EXP-20260814-103 - Independent M4.43 selected-path and milestone-closure hard-truth audit

## Verdict

**ACCEPT.** Immutable M4.43 selects historical v0.1 and active v0.2 from the
normalized lexical repository pathname, requires either selected final entry
to be a regular non-link before any content read, and preserves the existing
behavior of arbitrary otherwise-valid unselected exact contracts. No concrete
counterexample survives the independent path/type/read, statement, authority,
CLI, suite, ledger, or hygiene gates.

The last M4.27 compatibility-publication capability and exit-gate rows are now
supported. M4 is **Complete**, strictly at the documented asset-free,
manifest/source-authenticated current-x86_64-Linux boundary. This does not
claim unlisted hashes or untested systems, N-way composition, general dry-run
or launch/runtime automation, whole staged-tree/source deletion, external-
receipt full-tree restoration, provenance, POSIX metadata equality, backup,
rollback, packaging, transactions, general Windows path policy, or post-
preflight concurrency guarantees. No successor milestone is activated.

## Immutable linkage and boundary

- audited worker: `6659f865960d56b0ccafcdd44bffd7e96a5333a8`;
- required direct parent: `18a3a4c2fbf2bb9fcba4920526b5ed7649391edd`;
- initial tree: clean;
- worker diff: 16 paths, 327 insertions, 36 deletions;
- verifier changes: Markdown/README documentation only; and
- no executable, original, media, work-copy, runtime, PS1, or game byte was
  read or executed.

The complete startup packet, exact M4.44 Roadmap entry, full Decision Log and
Known Unknowns, relevant MOCs, operating/charter/environment policy, M4.27
ledger, accepted M4.33/M4.38 evidence, EXP-101/102, M1/M4 notes, worker session,
both READMEs, both statements, complete compatibility/checker/test files, and
the exact worker diff were reviewed before disposition.

## Independent selected-path and read matrix

All cases used tracked-only disposable exports and synthetic temporary paths.

| Case | Result |
|---|---|
| normal selected active and historical paths | exact v0.2/v0.1 accepted |
| normalized dot and preserved dot-dot lexical aliases | exact selected version retained for both paths |
| complete regular-file cross-version replacement | rejected in both directions with the required selected ID |
| active link to historical / historical link to active | rejected before any `Path.read_bytes` call |
| selected dangling link | rejected before any `Path.read_bytes` call for both versions |
| selected directory, FIFO, or Unix socket | all six cases rejected before any `Path.read_bytes` call without blocking |
| selected-link/nonregular CLI | status 2, empty stdout, deterministic stderr, no traceback |
| arbitrary unselected exact regular files | v0.1 and v0.2 accepted through library and CLI |
| arbitrary unselected exact final links | v0.1 and v0.2 accepted through library and CLI |
| normal read boundary | exact selected statement followed by the eight enumerated authorities, once each and in order, for both versions |

The direct parent defect was also reproduced independently: replacing its
default active pathname with a relative link to the historical selected file
returned status 0, empty stderr, and valid v0.1. The immutable worker rejects
that same direction and the reverse direction at final no-follow metadata.

This confirms only final-entry admission on the declared current Linux host.
Concurrent replacement after metadata admission and broader parent-topology
claims remain outside M4.43, as documented in `DEC-20260814-097`.

## Independent statement and authority reconstruction

| Contract | Bytes | SHA-256 | ID / toolkit | Ordered objects | Scalar leaves |
|---|---:|---|---|---:|---:|
| historical v0.1 | 6,177 | `c3427d44cf32619a1f9bbcab7c51e67c0846b35d9d53eab7632ff6356c0beaf0` | `ablpc-m4-compatibility-v0.1` / `0.1` | 19 | 126 |
| active v0.2 | 7,677 | `dacfcab8c1d27e5a63db870f347eb08701f868ca678cafdd178913266f20ccb2` | `ablpc-m4-compatibility-v0.2` / `0.2` | 21 | 151 |

Both byte streams are canonical UTF-8 JSON with a final newline. Rotating the
first field to the end of every one of the 19/21 object paths rejects; every
one of the 126/151 scalar leaves rejects independent value and type drift.
Duplicate keys, malformed syntax, non-finite constants, noncanonical encoding,
and list/object/integer/boolean/null IDs all take the ordinary CLI status-2,
stderr-only, no-traceback path.

An independent reconstruction confirms the complete semantic delta is exactly:
the statement/toolkit versions, one appended `restore` workflow, one evidence-
cited `restoration_boundary` inserted before the unchanged Wine/Gamescope
scope, and the restoration-specific split/expansion of unsupported entries.
The five statement anchors are unchanged between versions.

All five machine-authority pins independently match:

| Authority | SHA-256 |
|---|---|
| `mods/training-primary-record-124-target-111e4.json` | `315320bc524986348167ca556b178ef41fe1e8ac961e482610f8f734f34b2434` |
| `mods/level01-primary-record-261-target-3459c.json` | `358998cd326f68fcf7e10593e8ec895915b558252c300464e8fe74177280198f` |
| `mods/chars-flick-all-from-chars3-flickd-all.json` | `5aaa6e9a4fa79c303ee0920e7f87e00e87bd1dfef412a32c55e36efcc947b607` |
| `scripts/play-pristine.sh` | `68c9171749bd7b207a15b4202193ccfddd2661fbb383deb34b1a5a5a4049977e` |
| `reimplementation/ablpc/manifest.py` | `b3480761ac2b4791ccbf1df69f88234532f27956152045b89615dd5ec5bf6d75` |

## Complete M4 ledger reconciliation

Accepted later evidence closes both gaps identified by M4.27: exact M4.33 /
`EXP-20260814-092` supports receipt sufficiency only at the strict current-
receipt boundary, and exact M4.38 / `EXP-20260814-097` supports one same-tree
lifecycle only at the manifest-driven current-x86_64-Linux boundary. M4.44
closes only the final compatibility-publication row.

| Required capability | Final disposition and exact boundary |
|---|---|
| Inspect supported formats and executable/data compatibility | **Supported, bounded.** `EXP-20260814-063/083`; prefix-only LEVEL, read-only bounded ANM, and opaque unparsed replacement remain explicit. |
| Compose declarative manifests and detect conflicting byte/field edits | **Supported.** `EXP-20260814-067`; exactly two inputs, byte-span conflict reporting, no semantic/N-way solver. |
| Validate exact input hashes and supported format versions | **Supported.** `EXP-20260814-063/083`; schemas 1/2 and the four declared operations only. |
| Dry-run affected files, records, and byte ranges | **Supported, bounded.** `EXP-20260814-085`; one existing manifest, no persisted report/output simulation/receipt. |
| Stage a complete work copy or sparse overlay without touching originals | **Supported.** `EXP-20260814-063`; deterministic preflight with non-transactional post-preflight limits. |
| Launch the tested Wine/Gamescope configuration | **Supported, manually gated.** `EXP-20260812-007/029` and `EXP-20260814-083`; exact Fedora/Wine/Gamescope declarations, manual renderer choice/log acceptance. |
| Emit receipts sufficient to reproduce and remove a mod | **Supported at the strict current-receipt sparse boundary.** `EXP-20260814-092`; no provenance/signature, staged-tree removal, or external-receipt full-tree restoration claim. |
| Test parsers with synthetic fixtures and a user-owned local corpus | **Supported.** `EXP-20260814-063/067/077/097`; tracked fixtures plus recorded user-owned local gates, with no game bytes in CI. |
| Document limitations, unsupported fields, and runtime scope | **Supported, bounded.** Exact v0.1/v0.2, `EXP-20260814-099/101/103`, five pins, lexical selected identity, final-entry admission, explicit unsupported list, and exact Wine/Gamescope scope. |

| Exit gate | Final disposition and exact boundary |
|---|---|
| At least two useful mod classes, including one beyond simple scene-position editing | **Supported.** `EXP-20260812-010/033` and `EXP-20260814-063`; guarded payload rebind plus exact opaque replacement. |
| Two independently created manifests compose or produce a deterministic conflict | **Supported.** `EXP-20260814-067`; exact two-input boundary only. |
| Install, validation, launch, and removal from one clean derived work copy | **Supported at the manifest-driven current-x86_64-Linux boundary.** `EXP-20260814-097`; exact-source `stage`, pinned-launcher dry-run validation, and same-tree `restore`, without game execution automation. |
| No original binary, asset, disc image, dump, or machine state is packaged | **Supported.** `EXP-20260814-083/085/097/103` plus tracked/protected/no-game-byte gates; user-owned outputs remain undistributable. |
| A versioned compatibility statement names supported hashes and Wine scope | **Supported, bounded.** Exact v0.1/v0.2 content, path/version selection, five anchors/pins, eight aligned authorities, and explicit unsupported scope survive independent M4.44 attacks. |

The final ledger is nine of nine required capabilities and five of five exit
gates. The result combines independently accepted evidence at its recorded
boundaries; it does not infer a broader platform or workflow.

## Validation and hygiene

| Gate | Result |
|---|---|
| focused compatibility | 75/75 pass |
| compatibility + manifest + LEVEL | 288/288 pass |
| canonical `.venv/bin/python -m pytest -q tests` | 476/476 pass |
| `make m4-compatibility` | active v0.2 valid with five anchors |
| final `make check` | Python doctor, Vault lint, active statement, canonical tests, tracked audit, and diff checks pass |
| final diff/MIME/protected-path/no-game-byte/clean-tree | pass on one documentation-only verdict commit |

No unscoped pytest command, launcher, executable, or game input was invoked.

## Disposition

M4.44 closes the final compatibility row and marks M4 Complete only at the
boundary above. `KU-051` and `KU-052` remain resolved only at their exact
receipt and manifest-driven lifecycle scopes. All unsupported declarations
remain unsupported. M2 remains Deferred, M3 and M6 remain Planned, M5 remains
Deferred, and this audit does not select or begin another milestone.
