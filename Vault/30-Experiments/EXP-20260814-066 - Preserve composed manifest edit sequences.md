---
type: experiment
id: EXP-20260814-066
date: 2026-08-14
question: Can deterministic exactly-two-input composition preserve each independently valid input file entry's authored edit sequence?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline implementation, synthetic regression tests, and user-owned local corpus hash/byte checks
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.7 corrective worker packet only; no schema/receipt/operation change, N-way solver, semantic reconciliation, dry-run, removal, launch, ALL parsing, compatibility inference, runtime, M2, PS1, or general rollback work
artifacts:
  - reimplementation/ablpc/manifest.py
  - tests/test_manifest.py
  - reimplementation/README.md
  - mods/training-primary-record-124-target-111e4.json
  - mods/training-primary-record-125-field-0c-zero.json
  - mods/chars-flick-all-from-chars3-flickd-all.json
addresses: []
file_offsets:
  - synthetic primary record 0 at 0x98
  - synthetic position claim [0x98,0xA4)
  - synthetic field-0c claim [0xA4,0xA6)
  - synthetic payload-target claim [0x21C,0x220)
result: worker-complete-authored-edit-sequence-preservation
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
---

# EXP-20260814-066 - Preserve composed manifest edit sequences

## Result

**Worker-complete; independent M4.8 review required.** Exact M4.7 closes the
M4.6 falsification without widening composition. For every combined
destination, `_composed_file_entry_from_ranked_claims` now orders edits by the
already deterministic canonical input rank and then by that input file entry's
original edit index. It no longer sorts edits by claimed source byte span.

Destination files remain sorted by normalized Windows path. Exact claims are
still compared only across the two inputs, conflicts retain their deterministic
earliest-overlap selection, and the combined existing-schema manifest still
passes ordinary `_validate_manifest` and `_prepare_manifest` revalidation.
Thus a genuine cross-input guard dependency still fails closed rather than
being reordered or semantically reconciled.

This worker result does not independently accept the M4 composition exit gate.
Fresh-context M4.8 must audit the immutable clean worker commit under
`DEC-20260814-055` and `DEC-20260814-061`.

## Exact falsification closure

The new bounds-valid synthetic fixture reproduces M4.6's exact locators:

- primary record 0 and position claim `[0x98,0xA4)`;
- adjacent independent field-`0x0C` claim `[0xA4,0xA6)`; and
- payload-target field claim `[0x21C,0x220)`.

The left input's authored sequence changes the payload target from valid old
block `0x98` to valid block `0x240`, then changes the record position. The
right input changes only the disjoint field bytes. Both inputs apply
independently. Their left-to-right and right-to-left compositions now emit
byte-identical canonical JSON, and the payload-target edit precedes the
position edit in the result regardless of CLI argument order.

Saving and loading the emitted JSON, ordinary sparse `apply`, and full-tree
`stage` all produce the independently calculated authored-sequence bytes. The
ordinary receipts are equal and the synthetic source remains byte-identical.
This directly closes the previous combined-revalidation failure rather than
removing revalidation.

## Adjacent order and conflict regressions

Five new focused tests cover the corrective boundary:

1. the exact `0x98`/`0xA4`/`0x21C` falsification with independent input
   applications and saved apply/stage equality;
2. one valid input whose authored field edit precedes a lower-offset position
   edit, proving descending source offsets remain in input order;
3. two sequential same-span field guards inside one input plus a disjoint
   second input, proving intra-input overlaps are not reclassified as
   cross-input conflicts and retain their guard chain;
4. an empty opaque same-destination conflict at overlap `[0,0)` plus distinct
   opaque destinations with unequal replacement sizes; and
5. two inputs with both position and field conflicts, proving both argument
   orders select the same earliest overlap.

The correction changes no claim interval, schema, operation, receipt field,
path rule, source-hash guard, or output-topology behavior.

## Validation

- Focused manifest/LEVEL suite: 63/63 passed.
- Complete canonical suite (`python -m pytest -q tests`): 251/251 passed in
  6.72 seconds before Vault closure.
- `git diff --check`: passed before Vault closure.
- No unscoped pytest command was used.

Final `make check` after Vault closure passes: Python smoke imports, Vault lint
at 225 notes with zero errors/warnings, the canonical 251-test suite in 6.23
seconds, tracked-file audit with zero violations, and staged/unstaged diff
checks.

The user-owned local work-copy check reconfirms exact source hashes:

- Training LEVEL DAT:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`;
- opaque destination:
  `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`;
- opaque replacement source:
  `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.

The tracked same-DAT pair remains byte-identical under reversed inputs with
composed JSON SHA-256
`b16a7cac40149ea87d26617a43ee1c29cfc5a3aebfa4cd34f139c45852879faa`
and output DAT SHA-256
`78cca99b1993cc6deff8f89104d6f6aa8154ed7063e4ab0b56195e4321761d9a`.
The M1-plus-opaque pair retains composed JSON SHA-256
`de15f8e566fb5dcfe70d8dc690a6c9dcc6f22faa70df207f37d784a138cfb485`,
LEVEL output SHA-256
`47b7f45e39137f7decdd4ca94db2ef663ee868e6d506bc88511569ded74d7c00`,
and exact opaque replacement output hash `6e5afb4f...079a4`. Sparse locality
and all three source hashes remain unchanged.

The exact opaque recipe also passes two independent sparse applications with
byte-identical receipts and outputs, exact replacement hash
`6e5afb4f...079a4`, destination/source preservation, and only the destination
plus fixed receipt in each output.

No executable, DAT, `.ALL`, `.ANM`, original, runtime capture, dump, virtual
disk, or other game-byte artifact is added to Git. The local sparse outputs
remain outside the repository.

## Limitations

This is exactly-two-input deterministic composition with canonical whole-input
grouping per destination. It does not solve cross-input semantic dependencies,
find an arbitrary edit order, accept N inputs, change manifest or receipt
schemas, parse `.ALL`, infer resource compatibility or identity, dry-run,
remove, or launch a mod, establish runtime evidence, reopen M2, consult PS1,
or add transaction/rollback semantics. The accepted M4.3 limitation for
unpredictable I/O and concurrent races remains unchanged.

## Exact next packet

Run fresh-context M4.8 against the clean immutable M4.7 worker commit.
Reproduce the exact order-sensitive pair and every adjacent multiple-edit
case, actively test cross-input canonical interleaving and combined
revalidation, and preserve all M4.5 conflict/canonical, M4.4 topology,
schema/receipt, tracked local, exact opaque recipe, Vault, and asset-free
gates. Return `ACCEPT` only if every M4.7 done condition survives and then name
one exact next M4 packet from a still-unmet written exit gate; otherwise return
`REJECT` with one exact bounded correction.

## Independent M4.8 disposition

Fresh-context [[EXP-20260814-067 - Independent M4.7 hard-truth audit]] returns
`ACCEPT` for immutable commit
`f7ce96200e3c741e195e81e4089e1f3d262deee0`. It independently reproduces the
exact pair, both canonical rank orientations, a three-edit authored chain plus
one independent shared-destination edit, the complete conflict/collision
matrix, saved apply/stage and receipt equality, 28/28 accepted topology cases,
6/6 schema applications, both tracked local pairs, the exact opaque recipe,
and the asset-free boundary. A genuine cross-input guard dependency fails
closed identically in both argument orders, confirming that no semantic solver
was introduced. M4.9 receipt-validated sparse-overlay removal is the single
selected successor.
