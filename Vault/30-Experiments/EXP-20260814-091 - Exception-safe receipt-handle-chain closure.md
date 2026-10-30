---
type: experiment
id: EXP-20260814-091
date: 2026-08-14
question: Can receipt-chain cleanup attempt every owned descriptor exactly once despite earlier close errors while preserving primary failures and preventing cleanup-only mutation?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; synthetic asset-free descriptor-fault tests plus exact user-owned ignored local work-copy recipes
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.32 worker over M4.31 verdict 3ed0ff45969d28bc7a8a46c3e16fa8e16e6b30e5; receipt-chain release/error propagation only
artifacts:
  - reimplementation/ablpc/manifest.py
  - reimplementation/ablpc/compatibility.py
  - tests/test_manifest.py
  - Vault/30-Experiments/EXP-20260814-090 - Independent M4.30 component-acquisition hard-truth audit.md
addresses: []
file_offsets: []
result: worker-complete-exception-safe-exhaustive-receipt-chain-closure
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
---

# EXP-20260814-091 - Exception-safe receipt-handle-chain closure

## Result

**Worker-complete; exact M4.33 audit required.** Receipt-chain cleanup now
attempts the file descriptor and every directory descriptor exactly once even
when an earlier `os.close` reports an error. A pre-existing acquisition/read/
comparison failure stays primary; a cleanup-only error becomes deterministic
`ManifestError` before strict receipt parsing, source preparation, output
creation, or removal.

This correction changes only receipt-handle release/error propagation and its
synthetic tests. It does not change component acceptance, receipt or manifest
bytes/schemas, operations, mapping, guards, source/hash/output authority,
replay/removal/mount behavior, statement membership, or lifecycle scope.

## Pre-change reproduction

Before editing, an eight-descriptor synthetic chain reproduced the M4.31
failure exactly:

| Injected close | Attempts before abort | Retained descriptor delta |
|---|---:|---:|
| first | 1 | +7 |
| second | 2 | +6 |

The injected wrapper performed the target close and then reported `EIO`,
matching the conservative Linux rule that a failed close must not be retried.
All skipped descriptors were explicitly released after measurement.

## Correction

`_close_receipt_descriptors` now walks the owned file-first, reverse-directory
sequence without stopping at an earlier `OSError`, retains the first cleanup
error, and never retries a descriptor. `_close_receipt_handle_chain` delegates
to that one path. `_managed_receipt_handle_chain` supplies exception-safe
release for both retained acquisition chains:

- if the body already failed, all closes are attempted and the cleanup error
  is attached as a secondary note without replacing the body exception;
- if cleanup is the only failure, all closes are attempted and one
  deterministic `ManifestError` is raised before parsing; and
- nested reacquired/acquired cleanup preserves the inner primary while both
  chains release exhaustively.

Partial `_open_external_receipt_chain` failure uses the same exhaustive helper,
preserves its primary exception, and records any secondary cleanup error.

## Synthetic evidence

Seven new cases cover four indexed cleanup-only failures across the first,
second, and last close of the reacquired/acquired chains; partial acquisition
with primary final-`fstat` failure plus a secondary first-close failure; primary
chain-comparison failure plus one cleanup error in each retained chain; and CLI
status 2 with empty stdout. They assert:

- every owned descriptor appears once in the attempted-close sequence;
- no descriptor-count delta remains;
- receipt parsing does not begin after cleanup-only failure;
- primary exception type/message remain exact and secondary cleanup errors are
  retained as notes;
- source and ordinary-overlay snapshots remain exact; and
- output remains absent.

Focused manifest tests rise from 154 to 161; manifest + LEVEL + compatibility
rise from 216 to 223; canonical scoped tests rise from 404 to 411. The exact
M4.29 parent substitution, M4.30 adjacent component/final-file cases, strict
receipt authority, composition/M1, removal/mount, and manifest workflows all
remain green.

The manifest implementation SHA-256 becomes
`f7fd01144b99f4b93cbbb05faa382c53279114bb60b1a71b0793a755279ad111`.
Only that existing machine-authority pin changes; exact statement bytes,
five-pin membership, other four pins, scoped alignment, and nine asset-free
reads remain unchanged.

## Exact local retention

All three established user-owned local families completed two ordinary apply,
external-receipt replay, byte-identical tree comparison, and receipt-driven
removal cycles below ignored `work/`. Receipt and output hashes remain exactly
those in `EXP-20260814-090`, every replay root was removed, every external
receipt remained exact, and source hashes remained:

- Training DAT `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`;
- opaque destination `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`;
- replacement `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.

No local output, receipt, manifest, or game byte entered a tracked path.

## Final repository gates

- focused manifest: 161/161;
- combined manifest + LEVEL + compatibility: 223/223;
- final `make check`: Python doctor green, Vault lint 275 notes with zero
  errors/warnings, exact M4 statement valid with five anchors, canonical
  411/411 tests, tracked-file audit zero, and diff checks green;
- manifest implementation SHA-256 exactly
  `f7fd01144b99f4b93cbbb05faa382c53279114bb60b1a71b0793a755279ad111`;
  and
- protected roots retain only their tracked `.gitkeep`; no game byte is in the
  tracked worker surface.

## Limits and successor

A descriptor whose `close` reports an error is attempted once, not retried,
because Linux may already have released it. This is exhaustive owned-handle
cleanup, not rollback, a filesystem transaction, or post-preflight concurrency
protection.

Exact M4.33 is the required fresh-context hard-truth audit of immutable M4.32.
It must independently inject every close position across partial acquisition
and both retained chains, check attempted-close identity/order and real
descriptor deltas, preserve primary/cleanup-only behavior, retain the exact
parent/component/workflow/local/compatibility gates, and return one verdict.
M4, `KU-051`, and `KU-052` remain open pending that audit.

## Successor disposition

[[EXP-20260814-092 - Independent M4.32 receipt-chain-closure hard-truth audit]]
returns `ACCEPT`. It reproduces the direct parent's +7/+6 defect and then
passes 28/28 fresh indexed partial/nested-chain error cases with exact close
identity/order/multiplicity, zero real descriptor deltas, preserved primary
type/message, cleanup-only parse/source-preparation exclusion, and CLI silence.
All retained workflow/local/compatibility/hygiene gates pass. `KU-051` is
resolved only at that strict boundary; M4 and `KU-052` remain open. Exact
M4.34, the separate clean-derived-copy lifecycle feasibility audit, is the
sole successor.
