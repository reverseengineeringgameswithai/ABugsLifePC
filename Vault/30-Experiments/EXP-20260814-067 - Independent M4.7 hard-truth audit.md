---
type: experiment
id: EXP-20260814-067
date: 2026-08-14
question: Does immutable commit f7ce962 satisfy every M4.7 canonical exactly-two-input, authored-sequence, combined-revalidation, accepted-baseline, and asset-free condition?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline independent code review, synthetic falsification, scoped tests, and user-owned local corpus hash/byte checks
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact fresh-context M4.8 audit of immutable commit f7ce962 only; no implementation/schema/receipt change, N-way solver, dry-run, removal implementation, launch, ALL parsing, compatibility inference, M2 reopening, runtime, PS1, or general rollback request
artifacts:
  - reimplementation/ablpc/manifest.py
  - reimplementation/ablpc/cli.py
  - reimplementation/ablpc/level_dat.py
  - tests/test_manifest.py
  - tests/test_level_dat.py
  - mods/training-primary-record-124-target-111e4.json
  - mods/training-primary-record-125-field-0c-zero.json
  - mods/chars-flick-all-from-chars3-flickd-all.json
addresses: []
file_offsets:
  - synthetic primary record 0 at 0x98
  - synthetic position claim [0x98,0xA4)
  - synthetic field-0c claim [0xA4,0xA6)
  - synthetic payload-target claim [0x21C,0x220)
result: accept-authored-edit-sequence-preservation
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
  - audit/hard-truth
---

# EXP-20260814-067 - Independent M4.7 hard-truth audit

## Verdict

**ACCEPT.** Immutable worker commit
`f7ce96200e3c741e195e81e4089e1f3d262deee0` satisfies every exact M4.7 done
condition. Independent adversarial probes found no surviving intra-input edit
reorder, canonical argument-order difference, claim/conflict defect, combined-
revalidation bypass, receipt/output difference, topology regression, schema
regression, local-recipe drift, source mutation, or tracked game-byte payload.

The accepted capability is deliberately narrow: exactly two existing schema-1
or schema-2 manifests are grouped by canonical input identity while each input
file entry retains its authored edit-index order. Files remain normalized-
Windows-path sorted, cross-input claims remain exact, and the combined manifest
is still revalidated through the ordinary existing-schema path. This is not an
N-way or semantic dependency solver.

## Audit boundary and immutable inputs

The audit resolved short hash `f7ce962` to the full hash above, confirmed that
`HEAD` matched it, and confirmed a clean `## main` worktree before review. Its
parent is `f0a44b39b0a46a5f5c8270519c59bb5e67c796ab`. Before substantive work,
the complete [[START HERE]] sequence was reread: full [[Current State]], full
[[Project Roadmap]], full [[Environment Status]], full [[Decision Log]], full
[[Known Unknowns]], and the relevant implementation, experiment, reverse-
engineering, and file-format MOCs. The complete [[Agent Operating Manual]],
[[Project Charter]], exact M4.8 roadmap packet, `EXP-20260814-063/064/065/066`,
[[M4 Exact Whole-file Replacement]], [[M1 Tool Support Matrix]], and the M4.7
worker session were also reread.

Review covered the complete 15-path worker diff and the exact implementation at
`compose_manifests` (`manifest.py:66-223`),
`_composed_file_entry_from_ranked_claims` (`manifest.py:462-478`), combined
`_prepare_manifest` (`manifest.py:219-222`), sequential LEVEL application
(`manifest.py:309-364`), the CLI boundary, all manifest/LEVEL tests, the three
tracked manifests, and the ignored user-owned local work copy. The only worker
implementation change removes global span ordering and retains the key
`(input_rank, edit_index, canonical_edit_json)`. No implementation code,
original, external repository, game file, runtime state, schema, receipt, or
operation was modified by this audit. The external PS1 tree was not inspected
or touched.

## Exact authored-sequence reproduction

An independent asset-free synthetic DAT reproduced the exact M4.6 locators:
primary record 0 at `0x98`, position claim `[0x98,0xA4)`, independent field
claim `[0xA4,0xA6)`, and payload-target claim `[0x21C,0x220)`. One input edits
the payload target before the lower-offset position; the other edits only the
disjoint field.

Both inputs applied independently. Their cross-input claims were exactly
disjoint. Both compose argument orders emitted identical canonical JSON and
preserved the authored payload-target-then-position sequence. Saving and
loading that JSON, sparse `apply`, and full-tree `stage` produced bytes equal
to an independent authored-order calculation. Returned and on-disk ordinary
receipts were equal, and all source bytes remained unchanged.

The canonical grouping check then forced the two-edit input to canonical rank
zero and canonical rank one in separate cases. Both passed. A separate shared-
destination case retained a three-edit authored chain plus one independent
edit, including descending offsets and sequential same-span guards. Multiple
destinations remained sorted as `CD/A.DAT`, `CD/B.DAT`, and `CD/Z.DAT` while
the four shared-destination edits remained whole-input grouped in both rank
orientations. These probes cover more than the two-edit regression without
changing the exactly-two-manifest boundary.

## Combined revalidation remains fail-closed

An independent cross-input guard-dependency probe made the position input
canonical-first. Each input applied alone and the claims were disjoint, but the
canonical combined order changed bytes needed by the other input's later
payload-target guard. Both CLI argument orders returned 2, kept stdout empty,
and emitted identical stderr:

```text
ablpc-mod: negative payload-target command item count -32768 at 0xac
```

The stderr SHA-256 was
`7be2276d0a188b97845208c0ce5d322fa5b47255d6ddae99ff86da376f178324`.
The source remained unchanged. Thus combined `_prepare_manifest` is still
active and the composer does not silently solve, reorder, or reconcile a
genuine cross-input dependency. During probe construction, a first position
tuple `(9,8,7)` happened to leave the old block structurally valid and was not
discriminating; the exact `(1,2,3)` tuple invalidated it and produced the
required fail-closed observation.

## Conflict, opaque, schema, and topology results

The independent composition matrix passed 6/6 grouped probe families:

1. exact order-sensitive application/composition/save/apply/stage/receipt and
   source-preservation behavior;
2. canonical whole-input grouping with the sequence-sensitive input at either
   canonical rank;
3. multiple destinations, three authored edits, four total shared-destination
   edits, descending offsets, and same-span sequential guards;
4. deterministic empty opaque same-destination conflict at `[0,0)` plus exact
   unequal replacements on distinct destinations;
5. deterministic earliest multiple-conflict selection plus case-insensitive
   path, format, source-hash, and replacement-source/destination collision
   reports under reversed arguments; and
6. the cross-input guard dependency above, failing closed identically in both
   argument orders.

Exact position, field, payload, and opaque claims survived. Conflict objects
retained exact canonical input identities, normalized destination, kind, and
half-open overlap where applicable, with empty stdout and no game bytes. The
focused manifest/LEVEL suite passed 63/63; the complete scoped canonical suite
passed 251/251 in 6.40 seconds. No unscoped pytest command was used.

The independently reconstructed M4.4 topology matrix passed 28/28, including
the four original cases and adjacent requested-root, destination, receipt,
stage-source, symlink, non-directory, FIFO, regular-file, and `--force`
cases. Rejecting cases preserved complete source and blocker snapshots and
left earlier, outside, receipt, and staged outputs absent. Positive missing-
root and permitted regular-file cases succeeded. Explicit M1 applications
passed 6/6—position, field-`0x0C`, and payload target under both schemas—with
3/3 byte-identical cross-schema results.

## Tracked local and asset-free results

The ignored user-owned work copy reproduced these exact source hashes:

- Training LEVEL DAT:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`;
- opaque destination:
  `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`;
- opaque replacement source:
  `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.

The tracked same-DAT pair remained reversed-order identical with composed JSON
SHA-256 `b16a7cac40149ea87d26617a43ee1c29cfc5a3aebfa4cd34f139c45852879faa`
and output DAT SHA-256
`78cca99b1993cc6deff8f89104d6f6aa8154ed7063e4ab0b56195e4321761d9a`.
Independent byte calculation, sparse locality, and source preservation passed.

The M1-plus-opaque pair retained composed JSON SHA-256
`de15f8e566fb5dcfe70d8dc690a6c9dcc6f22faa70df207f37d784a138cfb485`,
LEVEL output SHA-256
`47b7f45e39137f7decdd4ca94db2ef663ee868e6d506bc88511569ded74d7c00`,
and exact opaque output hash `6e5afb4f...079a4`. Locality and all three source
hashes passed. The exact opaque recipe passed twice with equal receipts, exact
output bytes, sparse locality, and source preservation.

Before verifier documentation, Vault lint reported 225 notes with zero errors
or warnings and tracked-file audit reported zero violations. The worker diff
contained 14 `text/plain` paths and one Python source path. Git tracks only the
`.gitkeep` placeholders under `originals/` and `media/`; the ignored local
original remains outside the tracked set. No executable,
DAT, `.ALL`, `.ANM`, disc image, dump, VM image, capture, or other game-byte
payload entered the worker commit or this audit.

After all required Vault surfaces were updated, the complete scoped canonical
suite passed 251/251 in 6.38 seconds, Vault lint reported 227 notes with zero
errors or warnings, tracked-file audit reported zero violations, and staged/
unstaged diff checks passed. The intentional audit changes remain documentation
only.

## Limitations

- Acceptance is exact to two inputs, canonical whole-input grouping per
  destination, retained authored per-input sequence, and ordinary combined
  existing-schema revalidation. Cross-input guard dependencies can still make
  a disjoint pair fail closed.
- It does not accept N inputs, find an arbitrary dependency order, reconcile
  semantic intent, change schemas/receipts/operations, parse `.ALL`, infer
  compatibility or identity, launch the game, establish runtime behavior,
  reopen M2, consult PS1, or add general rollback/transaction semantics.
- The accepted M4.3 limitation remains: unpredictable I/O, storage,
  permissions, unrelated copy failures, or concurrent races after deterministic
  preflight are not transactional.

## Exact next packet: M4.9

**Name:** Receipt-validated sparse-overlay removal.

**Bounded question:** Can a sparse overlay produced by ordinary `apply` be
removed from its existing receipt only when that receipt exactly matches the
result recomputed from a supplied existing-schema manifest and exact source
root, and every recorded output is a regular file with the recomputed output
hash, while refusing symlinks, non-regular/missing/changed files, malformed or
forged receipts, extra overlay content, unsafe/protected roots, and any source-
tree mutation?

**Exact locators and inputs:** the still-unmet M4 exit gate “Install,
validation, launch, and removal are documented and tested from a clean derived
work copy”; `build_parser`/`main` in `reimplementation/ablpc/cli.py:27-138`;
`apply_manifest`, `_prepare_manifest`, `_write_prepared`, `_safe_relative_path`,
`_validate_output_plan`, and `_validate_planned_file` in
`reimplementation/ablpc/manifest.py:226-246`, `271-306`, `498-512`,
`675-694`, `724-740`, and `790-817`; the ordinary schema-1/schema-2 receipt
shape; accepted M4.3
topology boundary; accepted exact M4.7 composition boundary; the three tracked
manifests above; and synthetic sparse overlays only.

**First pass:** add
`remove MANIFEST --source-root SOURCE --overlay-root ROOT` for dedicated
sparse overlays only. Parse and strictly validate the existing receipt;
recompute the expected ordinary receipt through `_prepare_manifest` against
the exact source root and require exact equality; require exact on-disk hashes
for every recomputed output; require the overlay tree to contain exactly the
receipt, recorded destination files, and their necessary directories; and
fully preflight one deletion plan before deleting anything. Delete only those
validated files, then prune their empty directories and the empty overlay
root. Add asset-free synthetic single-file, multi-file, composed-manifest,
changed/missing/symlink/FIFO/extra-content/receipt-mismatch cases and exact
local temporary-overlay checks with all source hashes unchanged. Do not change
the manifest or receipt schema.

**Stop rule:** do not delete or restore any source-tree file; remove a staged
full game tree; build a trash, backup, rollback, package-manager, or generalized
transaction system; add broad dry-run, launch, or compatibility work; change a
schema, receipt, or existing operation; accept N-way composition; parse `.ALL`;
infer compatibility; launch the game; reopen M2; consult PS1; or broaden the
accepted M4.3 deterministic-preflight claim. Stop and record one exact blocker
if the ordinary receipt cannot authenticate the bounded sparse-overlay plan
without one of those expansions.

**Done condition:** synthetic single-, multi-, and composed-manifest overlays
remove completely only when receipt/manifest metadata, exact output hashes, and
tree topology agree; every changed, missing, symlink, FIFO, extra-content, or
receipt/schema/name/path/edit/hash mismatch fails before deletion with exact
tree snapshots unchanged; exact user-owned local temporary overlays remove
while all source hashes remain unchanged; existing focused/full, composition,
topology, schema, receipt, exact-recipe, Vault, tracked-file, and no-game-bytes
gates remain green; the bounded removal workflow and limitations are
documented; required Vault updates are intentionally committed; and Git is
clean for fresh-context review.

## Subsequent worker disposition

[[EXP-20260814-068 - Receipt-validated sparse-overlay removal]] completes M4.9
at the worker boundary with 32 new parameter-expanded cases, 95/283 focused/
full tests before documentation, and three exact local apply/remove families
passing twice with unchanged source hashes. Exact M4.10 fresh-context review is
active; this note's M4.7 acceptance remains unchanged.
