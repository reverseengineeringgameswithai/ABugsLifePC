---
type: experiment
id: EXP-20260814-062
date: 2026-08-14
question: Can apply and stage reject the four deterministic M4.2 output-topology failures before any output mutation while preserving the exact replacement boundary?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline implementation, synthetic regression tests, and user-owned local corpus check
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact corrective M4.3 only; no manifest or receipt schema change, game launch, ALL parsing, compatibility inference, M2 reopening, PS1, or general rollback system
artifacts:
  - reimplementation/ablpc/manifest.py
  - tests/test_manifest.py
  - tests/test_level_dat.py
  - mods/chars-flick-all-from-chars3-flickd-all.json
addresses: []
file_offsets: []
result: worker-complete-four-deterministic-output-topology-reproductions-closed
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
  - audit/correction
---

# EXP-20260814-062 - Complete planned-output containment preflight correction

## Result

**Worker-complete; subsequently accepted by independent M4.4.** The exact M4.3
correction closes all four synthetic failures from
[[EXP-20260814-061 - Independent M4.1 hard-truth audit]] before output
mutation. Each case now raises `ManifestError`; no earlier destination,
outside receipt, receipt, or staged tree remains. The exact schema-2
replacement, schema-1/schema-2 M1 operations, deterministic receipt, ordinary
sparse/staged behavior, forced regular-file replacement, and ignored local
recipe remain green.

This worker result did not self-accept M4.1 or M4.3. Fresh-context
`EXP-20260814-063` subsequently attempted to falsify it under the serial
ratchet in `DEC-20260814-055` and returned `ACCEPT` at the deterministic
planned-path/type boundary.

## Implementation boundary

`apply_manifest` at `reimplementation/ablpc/manifest.py:42-62` computes every
result and calls `_validate_output_plan` before creating or changing the sparse
output. That plan contains every prepared manifest destination plus fixed
`_RECEIPT_RELATIVE = .ablpc/receipt.json`.

`_validate_planned_file` at lines 499-526 uses `lstat` so it does not follow
the topology it is validating. It rejects:

- a symlinked or non-directory planned ancestor;
- a symlink, directory, or other non-regular planned destination;
- an existing regular sparse destination or receipt unless `--force` is
  explicit; and
- deterministic inspection failures as `ManifestError`.

`_reject_output_symlink_components` at lines 565-573 additionally rejects a
symlink in the requested output-root path before `_resolved_root` can erase
that fact through canonicalization. `--force` permits replacement only when
the existing planned destination and receipt are regular files.

`stage_manifest` at lines 65-84 validates both the new game-root topology and
the source topology that `copytree` will reproduce for every planned
destination and receipt. A source `.ablpc` file, symlinked planned ancestor,
or non-regular planned destination therefore fails before `copytree` creates
the staged root.

`_write_prepared` at lines 207-221 routes the fixed receipt back through
`_safe_output_file` as defense in depth. Receipt fields and ordering are
unchanged.

## Four corrective regressions

All regressions use only synthetic bytes and explicit no-output assertions in
`tests/test_manifest.py`.

1. `test_apply_preflights_receipt_symlink_before_any_output` constructs
   `output/.ablpc -> outside`. Application raises `ManifestError` before the
   destination write, and no outside `receipt.json` exists.
2. `test_apply_preflights_later_parent_blocker_before_any_output` constructs a
   two-entry plan with regular file `output/B` blocking later parent
   `B/two.bin`. Application raises `ManifestError`; `A/one.bin` and the receipt
   are absent.
3. `test_apply_force_rejects_later_directory_before_any_output` makes the
   second forced destination a directory. Application raises `ManifestError`
   before the first destination is written; the directory is unchanged and no
   receipt exists.
4. `test_stage_preflights_receipt_parent_blocker_before_copy` puts a regular
   `.ablpc` file in the source tree. Staging raises `ManifestError`; the staged
   root is absent and the source files are unchanged.

`test_apply_force_replaces_existing_regular_file` preserves the positive
force boundary. `test_apply_force_rejects_symlink_destination_before_output`
covers the required forced-symlink rejection, and
`test_apply_rejects_symlinked_output_root_before_any_output` covers the
adjacent requested-root symlink case, including lexical `..` normalization.

## Validation

- Focused manifest/LEVEL suite: 47 passed (40 retained plus seven M4.3 tests).
- Complete repository suite: 235 passed.
- Vault lint before this note: 215 notes, zero errors, zero warnings.
- Tracked-file audit before this note: zero violations.
- Explicit schema-2 M1 application check: position, guarded payload-target,
  and guarded field-`0x0C` operations passed 3/3 with source preservation and
  receipt/output-hash agreement. Schema-1 coverage remains in the focused and
  complete suites; no operation or receipt field changed.
- Final exact ignored local recipe under
  `/tmp/ablpc-m4-3-final.BrgRDC/overlay`:
  - destination input hash
    `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`;
  - replacement source and output hash
    `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`;
  - output byte-identical to the replacement source;
  - sparse output contains only `CD/CHARS/FLICK.ALL` and
    `.ablpc/receipt.json`;
  - CLI stdout receipt equals the written receipt; and
  - both source-tree hashes remain exact.

## Limitations

**Confirmed only at the deterministic planned-path/type boundary:** every
manifest destination and fixed receipt is containment/type-preflighted, and
the stage source is checked for the topology those planned writes will inherit.

**Not a transaction or rollback system:** unexpected permission changes,
storage exhaustion, unrelated `copytree` failures, hardware/I/O faults, or a
concurrent filesystem race after preflight can still fail after some output
mutation. M4.3 does not claim otherwise. It adds no manifest capability,
`.ALL` meaning, general compatibility, runtime result, or M2 evidence.

## Historical next packet

Run M4.4: a fresh-context James hard-truth audit of the clean M4.3 worker
commit. Reproduce the four cases independently, inspect adjacent output-root,
planned-ancestor, destination, receipt, staging, and `--force` topology cases,
re-run the focused/full/M1/local-recipe gates, and verify that documentation
does not claim general transactional rollback. Return `ACCEPT` only if every
M4.3 done condition survives; otherwise return `REJECT` with one exact bounded
corrective packet.

## Subsequent independent result

`EXP-20260814-063` completes M4.4 with `ACCEPT`: the four original and 22
adjacent topology cases pass with explicit no-mutation checks, focused/full
suites pass 47/47 and 235/235, schema-1/schema-2 M1 applications pass 6/6, and
the exact recipe passes twice with deterministic receipts and source
preservation. Exact M4.5 is now active on two-manifest composition/conflict
reporting.
