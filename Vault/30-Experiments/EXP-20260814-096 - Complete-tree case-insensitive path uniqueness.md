---
type: experiment
id: EXP-20260814-096
date: 2026-08-14
question: Can exact M4.37 reject Windows-case-equivalent complete-tree paths before restoration reads or mutation while preserving the accepted lifecycle?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; synthetic fixtures, private mount namespaces, and exact user-owned ignored local recipe checks
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.37 correction directly above docs-only M4.36 verdict 7180e4a7d41e125307a2b32a3f1f6cb726d20b3d; no game execution or receipt/schema/operation/sparse/mount/launcher/statement/asset/runtime/M2/PS1 change
artifacts:
  - reimplementation/ablpc/manifest.py
  - reimplementation/ablpc/compatibility.py
  - tests/test_manifest.py
  - reimplementation/compatibility/m4-v0.1.json
  - Vault/30-Experiments/EXP-20260814-095 - Independent M4.35 clean-copy-restoration hard-truth audit.md
addresses: []
file_offsets: []
result: worker-complete-case-insensitive-complete-tree-uniqueness
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
---

# EXP-20260814-096 - Complete-tree case-insensitive path uniqueness

## Result

Exact M4.37 is worker-complete. Restoration now assigns every source and
staged-game file or directory one project-standard case-folded relative-path
key and rejects a second distinct path with the same key. Source inventory and
reserved-metadata validation now precede manifest preparation, so a source
collision fails before manifest-source content reads, mount-plan inspection,
stable content reads, writes, or unlinks. Staged-game collisions fail during
the no-follow inventory after the retained mount/alias safety preflight and
before any file-content read or mutation.

This is only path uniqueness under the repository's existing `casefold()`
model. It does not add Windows reserved-device-name handling, trailing-name
canonicalization, a new manifest rule, or a general portability claim.

## Parent reproduction and correction

Before the implementation change, eight new parameterized instances failed as
expected:

- all four source-tree shapes—file/file, directory/directory, file/directory,
  and nested ancestor—were accepted and restored; and
- all four staged-game shapes were rejected only as exact-spelling extra
  content rather than as Windows-case ambiguity.

The correction adds one case-folded-key map to `_regular_tree_inventory`.
That inventory already observes every directory and ordinary file without
following links, so the same invariant covers source and staged-game trees and
all file/directory combinations without changing path spelling in receipts or
the final source/game oracle. Source inventory is acquired once before
`_prepare_manifest` and passed into `_validate_complete_staged_tree`; the
existing stable metadata comparisons still detect later changes.

All eight regressions now pass. Complete recursive source/game snapshots are
identical across each refusal. Test traps prove source collisions do not reach
manifest preparation, mount-plan inspection, content reads, atomic writes, or
unlink; staged-game collisions do not reach content reads, atomic writes, or
unlink. The established `.ablpc` reserved-source test remains green.

Two additional uppercase-first directory cases instrument `os.scandir` for
source and staged-game trees. The inventory validates all siblings before
recursing, so neither spelling of the ambiguous directory is descended into.
This prevents a colliding directory alias from becoming an order-dependent
traversal surface.

## Retained automated and topology gates

- focused restoration/manifest tests: 198/198;
- combined manifest/M1/compatibility tests: 260/260;
- canonical repository tests: 448/448;
- tracked restoration mount/order selector: 6/6;
- strict compatibility checker: five anchors valid;
- statement bytes remain 6,177-byte canonical JSON at SHA-256
  `c3427d44cf32619a1f9bbcab7c51e67c0846b35d9d53eab7632ff6356c0beaf0`;
- only the manifest implementation pin changes, to
  `b3480761ac2b4791ccbf1df69f88234532f27956152045b89615dd5ec5bf6d75`.

The collision correction does not touch the accepted mount/alias code. The
four tracked restore mount namespaces and explicit mount-order classifier
cases pass in the selector above; M4.36's four additional proper-parent,
unrelated-directory, hidden-stack, and reused-ID cases remain retained
evidence for the unchanged code and are required again by independent M4.38.

## Exact local lifecycle and sparse retention

One disposable tree below `work/copies/` repeated the exact user-owned local
lifecycle without executing the game. The clean source contains 722 files and
26 directories including its root. `stage` emitted receipt SHA-256
`ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63`
and opaque output SHA-256
`6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.
The pinned launcher `--dry-run` returned status zero and reported executable
SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
`restore` returned the same receipt, removed `.ablpc`, left the staged tree
content-equal to source, and preserved the complete source snapshot. The
temporary tree was removed automatically.

All three retained sparse families applied and removed twice with absent
output roots and unchanged source hashes. Their exact receipt/output hashes
remain:

| Family | Receipt SHA-256 | Output SHA-256 |
|---|---|---|
| opaque | `ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63` | `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4` |
| same-DAT composition | `b899907eec17020f9e7a303b9cd8b5620dc70e83051840d13d57df80b6c779ef` | `78cca99b1993cc6deff8f89104d6f6aa8154ed7063e4ab0b56195e4321761d9a` |
| M1 plus opaque | `f8e144521905cc978e560e01158fae983495693f556f069773c8fac136c815b5` | DAT `b8012a95f7ec0254805bdd3cf32df2b16f2ad0926308fe8678cc2360027f720e`; opaque `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4` |

Source hashes remain Training DAT
`494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`,
opaque destination
`a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`,
and replacement
`6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.

## Closure validation

Final `make check` reports Python/tool doctor green, Vault lint 285 notes with
zero errors/warnings, the valid five-anchor compatibility statement, 448/448
canonical tests, and zero tracked-file violations. Diff checks pass; all
implementation/test/documentation changes are text/Python, protected roots are
unchanged, and no disposable local output remains.

## Limits and next packet

M4.37 changes no manifest/receipt bytes or schemas, formats, operations,
sparse workflow, source/hash/output authority, mount policy, launcher,
statement membership, asset, runtime, M2, or PS1 surface. It adds no
transaction, rollback, backup, whole-tree deletion, provenance, POSIX metadata
equality, or post-preflight concurrency guarantee. No game was executed.

M4 and `KU-052` remain open until fresh-context M4.38 independently attempts
to falsify this exact worker. Acceptance may resolve only the demonstrated
manifest-driven current-Linux clean-copy lifecycle and select a separate
compatibility-statement alignment packet; it may not mark M4 complete while
the statement still declares restoration unsupported.

## Disposition

[[EXP-20260814-097 - Independent M4.37 complete-tree-uniqueness hard-truth audit]]
returns `ACCEPT` for this immutable worker after stronger independent
collision, bind-mounted sibling-order, namespace, local, compatibility, and
hygiene attacks. `KU-052` resolves only at the demonstrated current-Linux
manifest-driven lifecycle. M4 remains active on exact M4.39 statement
alignment because unchanged v0.1 still declares restoration unsupported.
