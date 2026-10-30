---
type: experiment
id: EXP-20260814-092
date: 2026-08-14
question: Does immutable M4.32 exhaustively release every owned external-receipt descriptor exactly once while preserving primary and cleanup-only failure boundaries?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; synthetic asset-free descriptor-error tests plus exact user-owned ignored local work-copy recipes
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: fresh-context exact M4.33 audit of immutable M4.32 worker e396ab0e90ede2dd29f4c7b98fd434ed867236a5 with direct M4.31 parent 3ed0ff45969d28bc7a8a46c3e16fa8e16e6b30e5; audit and documentation only
artifacts:
  - reimplementation/ablpc/manifest.py
  - reimplementation/ablpc/compatibility.py
  - tests/test_manifest.py
  - Vault/30-Experiments/EXP-20260814-089 - Component-stable external receipt acquisition.md
  - Vault/30-Experiments/EXP-20260814-090 - Independent M4.30 component-acquisition hard-truth audit.md
  - Vault/30-Experiments/EXP-20260814-091 - Exception-safe receipt-handle-chain closure.md
addresses: []
file_offsets: []
result: accepted-exhaustive-one-attempt-receipt-chain-closure
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
---

# EXP-20260814-092 - Independent M4.32 receipt-chain-closure hard-truth audit

## Verdict

**ACCEPT.** Immutable M4.32 closes the exact M4.31 descriptor-release defect.
Every descriptor owned by partial acquisition, retained acquisition, and
reacquisition receives one close attempt even when any indexed close reports
an error after releasing its descriptor. Existing body failures retain their
exact type and message; cleanup-only failure becomes deterministic
`ManifestError` before receipt parsing, source preparation, output, or removal.

This verdict resolves only
[[Known Unknowns#KU-051 (resolved at the strict current-receipt/component/closure boundary)]].
M4 remains active because
[[Known Unknowns#KU-052 (clean-derived-copy lifecycle is not jointly demonstrated)]]
is still open. Exact M4.34, a separate clean-derived-copy lifecycle feasibility
audit, is the sole successor.

## Immutable linkage and scope

- audited worker: `e396ab0e90ede2dd29f4c7b98fd434ed867236a5`;
- required direct parent: `3ed0ff45969d28bc7a8a46c3e16fa8e16e6b30e5`;
- initial tree: clean;
- worker diff: 18 paths, 685 insertions, 57 deletions;
- implementation/test review: complete worker diff and every changed
  implementation and test file, including the closure, acquisition, nested
  context, CLI, compatibility-pin, and adjacent receipt paths; and
- verifier changes: documentation only.

No implementation, test, pin, schema, operation, workflow, launcher, asset,
runtime, M2, PS1, or local work-copy byte changed.

## Parent defect reproduction

The direct parent was exported to a disposable directory and loaded as an
independent package. An eight-descriptor synthetic chain used file-first,
reverse-directory expected order `[11, 10, 9, 8, 7, 6, 5, 4]`. The wrapper
performed the selected real close and then reported `EIO`.

| Reported-error close | Exact attempted descriptors | Exact skipped descriptors | `/proc/self/fd` delta at failure |
|---|---|---|---:|
| first | `[11]` | `[10, 9, 8, 7, 6, 5, 4]` | +7 |
| second | `[11, 10]` | `[9, 8, 7, 6, 5, 4]` | +6 |

The skipped descriptors were released only after measurement. This reproduces
the immutable M4.31 rejection and confirms that the audit exercises its exact
correction.

## Independent exhaustive descriptor matrix

A fresh deep external-receipt fixture owned seven descriptors per acquisition.
The observed acquired chain was `[10, 9, 8, 7, 6, 5, 4]`; while that chain
remained retained, reacquisition owned `[17, 16, 15, 14, 13, 12, 11]`.
Therefore nested cleanup order was exactly
`[17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4]`.

Twenty-eight fresh error-path cases covered every owned position:

| Family | Indexed cases | Exact attempts per case | Multiplicity | Final descriptor delta |
|---|---:|---:|---|---:|
| partial acquisition, final-file `fstat` primary plus one close error | 7/7 | `[10, 9, 8, 7, 6, 5, 4]` | `[1, 1, 1, 1, 1, 1, 1]` | 0 in every case |
| reacquired-chain cleanup-only error | 7/7 | nested 14-descriptor order above | fourteen `1`s | 0 in every case |
| acquired-chain cleanup-only error | 7/7 | nested 14-descriptor order above | fourteen `1`s | 0 in every case |
| custom body error plus same indexed error in both nested closures | 7/7 | nested 14-descriptor order above | fourteen `1`s | 0 in every case |

The partial-acquisition open order was always `[4, 5, 6, 7, 8, 9, 10]` and
cleanup was its exact reverse. The custom body exception stayed type
`PrimaryComparison` with message `M4.33 primary comparison body` in all seven
dual-cleanup cases. It received exactly two secondary notes, ordered first for
the reacquired chain and then for the acquired chain. The partial case stayed
the original `OSError` with exact message
`[Errno 5] M4.33 primary final-file fstat` and one secondary cleanup note.

Both cleanup-only families reached neither `_parse_receipt` nor
`_prepare_receipt_authority`; source and ordinary-overlay snapshots stayed
exact and replay output stayed absent. A representative last-acquired-close
CLI failure attempted all 14 descriptors once, returned status 2, emitted
empty stdout, and left a zero descriptor delta. Ordinary success used the same
14-descriptor order and multiplicity, returned the expected receipt, created
the exact output, and also left zero delta. No failed close was retried.

## Retained component, receipt, and workflow evidence

The M4.29 parent rename/directory-link boundary and adjacent M4.30 acquisition
tests pass 15/15, including replay and removal, parent inode replacement,
component-open replacement, final hard-link/metadata changes, CLI silence,
nonregular inputs, final swaps, descriptor-read changes, and execute-only
parents. This retains the independently recorded 28/28 adjacent acquisition
cases and three reacquisition-change refusals in
[[EXP-20260814-090 - Independent M4.30 component-acquisition hard-truth audit]];
the worker changes only release/error propagation after that accepted
component boundary.

The manifest suite passes 161/161, manifest + LEVEL + compatibility passes
223/223, and the exact canonical command `.venv/bin/python -m pytest -q tests`
passes 411/411. These retain schemas 1/2, all four operations, strict bytes and
receipt mapping/recomputation, source/hash/guard/output authority, new-root
replay, authenticated removal and mount behavior, composition, M1, and all
ordinary manifest workflows.

All three exact user-owned ignored local families completed two ordinary
apply, external-receipt replay, byte-identical comparison, receipt-driven
removal, and retained manifest-driven removal cycles in disposable roots:

| Family | Cycles | Receipt SHA-256 | Replayed output SHA-256 |
|---|---:|---|---|
| exact opaque replacement | 2/2 | `ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63` | `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4` |
| same-DAT composition | 2/2 | `b899907eec17020f9e7a303b9cd8b5620dc70e83051840d13d57df80b6c779ef` | `78cca99b1993cc6deff8f89104d6f6aa8154ed7063e4ab0b56195e4321761d9a` |
| M1 plus opaque | 2/2 | `f8e144521905cc978e560e01158fae983495693f556f069773c8fac136c815b5` | DAT `b8012a95f7ec0254805bdd3cf32df2b16f2ad0926308fe8678cc2360027f720e`; opaque `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4` |

Source hashes remained Training DAT
`494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`,
opaque destination
`a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`,
and replacement
`6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.

## Compatibility and repository gates

The compatibility statement remains byte-exact at
`c3427d44cf32619a1f9bbcab7c51e67c0846b35d9d53eab7632ff6356c0beaf0`.
`make m4-compatibility` reports exactly five hash anchors. Independent tracing
observes exactly nine unique asset-free reads: the statement, three manifests,
launcher, manifest implementation, Environment Status, Wine baseline, and
reimplementation README. The manifest implementation pin remains
`f7fd01144b99f4b93cbbb05faa382c53279114bb60b1a71b0793a755279ad111`.

Final `make check`, Vault lint, tracked-file audit, diff checks, MIME review,
protected-root review, and game-byte exclusion all pass. Protected roots retain
only their tracked `.gitkeep`; the verdict commit is documentation-only and
directly atop the audited worker.

## Limits

An `os.close` that reports an error receives no retry because Linux may already
have released that descriptor. Acceptance proves exhaustive release of the
handles owned by these receipt paths; it does not establish rollback,
transaction, backup/package semantics, post-preflight concurrency protection,
universal receipt provenance, staged-tree removal, source restoration, general
runtime automation, broader platform behavior, M2, PS1, or M4 completion.

## Sole successor

Exact M4.34 is the audit-only clean-derived-copy lifecycle feasibility packet
recorded in [[Project Roadmap#M4.34 — Clean-derived-copy lifecycle feasibility hard-truth audit]].
It must decide whether the current `dry-run`/`apply`/`stage`/launcher/removal
surfaces already join install, validation, launch readiness, and removal on one
same clean derived tree. If they do not, it must identify exactly one smallest
missing join. It may not infer completion from separate trees or broaden into
general runtime automation, transaction, package, backup, or staged-tree
deletion semantics.

## Disposition by M4.34

[[EXP-20260814-093 - Clean-derived-copy lifecycle feasibility audit]] returns
`REJECT` for M4 completion. Its same-tree ledger proves complete staged/forced-
copy outputs reach the launcher boundary but fail dedicated sparse removal
unchanged, while removable apply/replay outputs are not complete game trees.
The sole active correction is exact M4.35 manifest-driven restoration of one
authenticated complete staged copy. This does not alter this note's M4.32
`ACCEPT` or resolved `KU-051` boundary.
