---
type: experiment
id: EXP-20260814-068
date: 2026-08-14
question: Can an ordinary sparse overlay be removed only after its supplied manifest, exact source tree, byte-exact receipt, output hashes, and complete tree topology all agree?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline implementation, synthetic tests, and user-owned local corpus hash/application checks
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.9 worker packet only; no staged-tree removal, source restoration/deletion, receipt or manifest schema change, general rollback/transaction system, dry-run, launch, compatibility, ALL parsing, runtime, M2, or PS1 work
artifacts:
  - reimplementation/ablpc/manifest.py
  - reimplementation/ablpc/cli.py
  - tests/test_manifest.py
  - reimplementation/README.md
  - mods/training-primary-record-124-target-111e4.json
  - mods/training-primary-record-125-field-0c-zero.json
  - mods/chars-flick-all-from-chars3-flickd-all.json
addresses: []
file_offsets: []
result: worker-complete-receipt-validated-sparse-overlay-removal
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
---

# EXP-20260814-068 - Receipt-validated sparse-overlay removal

## Bounded question

Can a dedicated sparse overlay produced by ordinary `apply` be removed only
when a supplied existing-schema manifest and exact source root recompute the
same ordinary receipt, every recorded output is still a regular file with the
recomputed output hash, and the overlay tree contains no other entry?

The recorded executable SHA-256 above scopes the project, but this packet did
not read, launch, or modify the executable. It used synthetic bytes and an
ignored user-owned work copy only.

## Implementation

**Confirmed at the worker boundary:** `remove MANIFEST --source-root SOURCE
--overlay-root ROOT` now calls `remove_manifest`. Before any deletion it:

1. resolves and validates distinct, non-containing source/overlay roots under
   the accepted protected-root and output-symlink rules;
2. validates the supplied existing-schema manifest and recomputes every output
   plus the ordinary receipt through `_prepare_manifest`;
3. requires every recorded output and `.ablpc/receipt.json` to exist as single-
   link regular files below non-symlink directory ancestors;
4. walks the overlay without following symlinks and requires its complete entry
   set to equal only the recorded outputs, fixed receipt, and necessary
   directories;
5. parses the receipt as strict UTF-8 JSON, rejects duplicate keys and non-JSON
   constants, requires exact recomputed JSON data, and requires the byte-exact
   deterministic encoding emitted by ordinary `apply`; and
6. hashes every recorded output and requires the recomputed output SHA-256.

Only after all six gates pass does it unlink the recorded output files and
receipt, prune the authenticated empty directories deepest-first, and remove
the empty overlay root. The returned JSON is the same recomputed receipt that
authenticated the deletion. No source path is an unlink target.

`_write_prepared` now calls shared `_receipt_for` and `_receipt_bytes` helpers;
the receipt structure and byte encoding are unchanged. No manifest schema,
receipt field, or existing operation changed.

## Synthetic evidence

Thirty-two new parameter-expanded removal cases raise the focused manifest/
LEVEL total from 63 to 95. They cover:

- successful single-file, empty-output, two-file/shared-directory, and
  composed-manifest overlays with complete root removal and exact source
  snapshots;
- changed or missing recorded outputs;
- recorded output and receipt symlinks, FIFOs, hard links, and missing receipt;
- destination- and replacement-source drift after `apply`;
- extra regular files, empty directories, symlinks, and FIFOs;
- receipt schema, manifest name, path, edit detail, input hash, output hash,
  and unexpected-field mismatches;
- malformed JSON, duplicate receipt keys, and semantically equal but non-
  ordinary receipt encoding;
- refusal to remove a staged full tree because its copied content is extra;
- symlinked and protected overlay roots; and
- the public CLI success path.

Every rejection captures the altered overlay and source trees before removal,
then proves exact snapshot equality afterward. Symlink snapshots retain their
link targets; FIFO snapshots use `lstat` and never read from the FIFO. Thus the
negative cases test absence of partial deletion rather than merely checking an
exception type.

Validation results before documentation:

- `python -m pytest -q tests/test_manifest.py tests/test_level_dat.py`: 95
  passed;
- `python -m pytest -q tests`: 283 passed in 6.72 seconds;
- `git diff --check`: passed.

## Exact user-owned local checks

The ignored work copy reproduced these source hashes before and after all
checks:

- `CD/LEVEL07/LEVEL1.DAT`:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`;
- `CD/CHARS/FLICK.ALL`:
  `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`;
- `CD/CHARS3/FLICKD.ALL`:
  `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.

Three manifest families each completed ordinary apply then M4.9 removal twice
inside ignored temporary roots. Every returned receipt equaled its apply
receipt, both runs were deterministic, every overlay root was absent afterward,
and all three source hashes were unchanged:

| Case | Receipt SHA-256 | Output SHA-256 values |
|---|---|---|
| exact opaque replacement | `ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63` | `6e5afb4f...079a4` |
| tracked same-DAT composition | `b899907eec17020f9e7a303b9cd8b5620dc70e83051840d13d57df80b6c779ef` | `78cca99b...1d9a` |
| tracked M1-plus-opaque composition | `f8e144521905cc978e560e01158fae983495693f556f069773c8fac136c815b5` | `6e5afb4f...079a4`, `b8012a95...f720e` |

No local output, game byte, receipt file, or temporary manifest was added to
Git.

## Final closure validation

After the durable-note updates and the hard-link refusal correction:

- final `make check` passed with 283 scoped tests in 6.05 seconds;
- Vault lint passed on 229 notes with 0 errors and 0 warnings;
- the tracked-file audit reported 0 violations;
- the focused/full suite counts remained 95/283;
- all three exact local manifest families passed another 2/2 apply/remove
  reproduction with absent overlay roots and unchanged source hashes; and
- `git diff --check` passed before the intentional worker commit.

## Evidence classification

**Confirmed at this worker boundary:** ordinary current-version sparse
overlays can be removed completely after exact manifest/source recomputation,
byte-exact receipt validation, regular-file output hash validation, and an
exact no-extra-content tree check. Recorded outputs and the receipt must also
have one hard link, preventing removal from changing an external inode's link
count. The covered mismatch/topology cases fail before deletion with exact
snapshots unchanged.

**Inferred:** the ordinary receipt is sufficient authentication for this
dedicated current-version sparse-overlay boundary when combined with exact
source recomputation, output hashes, and complete tree topology. Independent
M4.10 must try to falsify this inference before it becomes accepted.

**Unknown/out of scope:** unpredictable permission/storage/I/O changes or
concurrent races after preflight are not transactional; a failure there can
still occur after an earlier unlink. Staged-tree removal, restoration of source
bytes, trash/backup/package management, arbitrary rollback, older receipt
migration, dry-run, launch, compatibility, N-way composition, `.ALL` semantics,
runtime behavior, M2, and PS1 remain outside this result.

## Disposition

M4.9 is worker-complete, not independently accepted. Exact fresh-context M4.10
is the sole next packet. M4 remains active.

**Subsequent audit:** [[EXP-20260814-069 - Independent M4.9 sparse-overlay removal hard-truth audit]]
returns `REJECT`. A pre-existing bind-mounted
intermediate overlay directory passes current complete-tree/type preflight;
removal deletes through the mount and removes the receipt before final pruning
fails `EBUSY`. Exact M4.11 is active on mounted deletion-plan refusal before
the first unlink.

## Exact next packet: M4.10

**Name:** Independent M4.9 sparse-overlay removal hard-truth audit.

**Bounded question:** Does the immutable clean M4.9 worker commit support every
receipt/source/output/tree/preflight/removal/source-preservation and accepted-
baseline claim at the exact dedicated sparse-overlay boundary, and—if so—what
one still-unmet M4 exit-gate packet is the smallest successor?

**First pass:** James must start in fresh context, reread [[START HERE]] and the
complete required startup sequence, and inspect only the immutable worker
commit. Independently construct ordinary single-, multi-, empty-output-, and
composed-manifest sparse overlays. Recompute receipt/output results separately;
verify byte-exact receipt, strict JSON, output hashes, complete topology,
deep/shared directory pruning, complete root removal, returned receipt, and
source snapshots. Actively falsify missing/changed/hard-linked/symlink/FIFO
outputs and receipt, manifest/source drift, receipt type/schema/name/path/edit/
hash/order/extra/duplicate/encoding changes, extra file/directory/symlink/FIFO,
case/topology/root aliasing, protected/overlapping roots, and staged-tree
refusal. Every rejected case must prove complete pre/post snapshot equality.
Re-run the focused/full suites, accepted composition/topology/schema/receipt
matrices, all three exact local remove recipes twice, Vault lint, tracked-file,
diff, no-game-bytes, and clean-tree checks.

**Stop rule:** do not change implementation, schema, receipt, or operations;
add staged-tree deletion, source restoration/deletion, backup/trash/package or
general transaction behavior; begin broad dry-run, launch, or compatibility;
accept N-way composition; parse `.ALL`; launch the game; reopen M2; consult
PS1; or broaden the accepted M4.3 deterministic-preflight claim. Reject only
with one exact bounded corrective packet.

**Done condition:** return `ACCEPT` only if every M4.9 condition survives, then
name exactly one successor derived from a still-unmet written M4 exit gate.
Otherwise return `REJECT` with one actionable correction. Record the verdict,
evidence, limitations, required Vault updates, intentional documentation-only
commit, and clean Git tree.
