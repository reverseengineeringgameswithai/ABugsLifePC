---
type: experiment
id: EXP-20260814-084
date: 2026-08-14
question: Can one existing exact-hash manifest be fully prepared and reported with deterministic affected-file, record, hash, size, and half-open byte-range evidence without writing an output tree or receipt?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; Linux 7.0.11 x86_64; synthetic asset-free temporary source trees only
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.25 single-manifest dry-run packet only; no game/original/media/work-copy/runtime/PS1 access and no apply/stage/compose/remove/launch, manifest/receipt schema, operation, format, input-policy, mount, package, rollback, or transaction change
artifacts:
  - reimplementation/ablpc/manifest.py
  - reimplementation/ablpc/cli.py
  - reimplementation/ablpc/compatibility.py
  - tests/test_manifest.py
  - tests/test_level_dat.py
  - tests/test_compatibility.py
addresses: []
file_offsets: []
result: pass-worker-deterministic-write-free-single-manifest-report
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/compatibility
---

# EXP-20260814-084 - Deterministic single-manifest dry-run report

## Question

Can exact M4.25 expose the ordinary single-manifest preparation path as a
write-free deterministic report that names every affected path, input/output
hash and size, authored edit, existing LEVEL DAT record, and exact half-open
destination range, while leaving all accepted workflows and evidence
boundaries unchanged?

## Boundary

The worker began from exact clean M4.24 verdict commit
`7a07f55782bec77e25ac9af1c8aeea4e0b3d244b` after the complete required
[[START HERE]] and Obsidian refresh. Only the manifest library, CLI, the one
required manifest-implementation compatibility pin, synthetic tests, and
required documentation changed.

No game file, original, media, local work-copy, runtime artifact, or external
PS1 source was read or executed. All source bytes used by this experiment are
independently generated pytest fixtures under temporary directories.

## Implementation

**Confirmed at the M4.25 worker boundary:**

- `dry_run_manifest(manifest, source_root)` resolves the source root through
  the existing protected-root policy and invokes `_prepare_manifest` once. A
  later invalid file therefore prevents any report from being returned.
- `ablpc-mod dry-run MANIFEST --source-root ROOT` loads the existing schema-1
  or schema-2 manifest, returns only the library report as indented JSON, and
  prints no success output on failure.
- Report schema 1 identifies the canonical normalized manifest by its existing
  schema version, name, and canonical SHA-256. Files and edits remain in
  authored order.
- Each file reports path, existing format, input/output SHA-256, and input/
  output byte size. The output hash is computed from the exact bytes already
  produced in memory by ordinary preparation.
- Each LEVEL DAT edit reports edit index, operation, section, record index,
  record offset, and a `start`/`end` half-open destination range. The exact
  spans are 12 bytes for candidate-center position, two bytes for field
  `+0x0C`, and four bytes for the payload-target field selected by the parsed
  reference.
- `replace-whole-file` reports its source path plus distinct half-open input
  and output extents, so unequal or empty sizes are representable without
  claiming an in-place byte correspondence.

The report metadata is carried only in the internal prepared result. The
ordinary receipt dictionary and serialized receipt bytes are unchanged.
Apply, stage, compose, and remove call the same existing functions and do not
consume the report.

## Synthetic evidence

The focused manifest suite expands from 90 to 99 tests. The added cases prove:

- all three LEVEL operations under both manifest schemas, with exact authored
  order, record offset, and ranges `0x21C–0x220`, record `+0x00–+0x0C`, and
  record `+0x0C–+0x0E`;
- exact independently computed output bytes/hashes and source-tree equality;
- unequal-size opaque replacement with distinct input/output extents;
- authored two-file report order;
- two CLI runs produce byte-identical JSON and an exact complete filesystem
  snapshot;
- a later replacement-hash failure, destination-input-hash failure, record-
  guard failure, and protected source root all return status 2, emit empty
  stdout, and preserve exact complete snapshots.

The combined manifest/LEVEL/compatibility suite passes 161/161 before
documentation. The canonical scoped suite passes 349/349. Existing tests
continue to cover invalid schemas/operations/paths, symlink escapes, sequential
guards, composition, apply/stage receipts, removal, and source preservation
through the same retained preparation path.

## Compatibility evidence

Changing `reimplementation/ablpc/manifest.py` necessarily changes exactly one
of M4.23's five machine authorities. Independent raw hashing produced the new
manifest implementation SHA-256
`ce66bd048e505546c002ebe8a1fdc4477822363cce8e4631618dd157a9c3d243`.
Only that expected digest changed. The other four pin values and membership
are exact.

The strict compatibility suite passes 47/47. An independent source parse and
raw rehash reproduces all 5/5 pins. Unchanged alignment still performs exactly
nine unique reads—one statement, five machine authorities, and three scoped
human authorities—with zero reads below `originals/`, `media/`, or `work/`.
The compatibility statement remains exactly 6,177 bytes, SHA-256
`c3427d44cf32619a1f9bbcab7c51e67c0846b35d9d53eab7632ff6356c0beaf0`.

## Final gates

- `make check`: Python doctor green; Vault lint 261 notes with zero errors and
  zero warnings; five-anchor compatibility checker green; canonical tests
  349/349; tracked-file audit zero violations;
- focused manifest 99/99 and combined manifest/LEVEL/compatibility 161/161;
- `git diff --check`: clean;
- changed/new paths before staging: 19, limited to Markdown/plain text, Python
  source/tests, and the root/reimplementation READMEs;
- statement, launcher, three tracked manifests, Environment/Wine authority
  facts, assets, originals, media, work, runtime, and external PS1 paths:
  unchanged.

## Limitations

- This report covers exactly one already-supported manifest and source root.
  It does not compose manifests, order N inputs, reconcile semantic intent, or
  simulate an output tree.
- The ranges are declared destination write spans, not a semantic diff or a
  claim that every byte within a span changes value.
- No report is persisted; stdout is the sole CLI result. No output directory,
  receipt, package, rollback point, or transaction is created.
- No manifest/receipt schema, format, operation, guard, ordering, source
  policy, launcher, runtime, M2, `.ALL`, mount, or compatibility scope changes.
- Worker success is not independent acceptance. Exact M4.26 must audit the
  immutable commit from fresh context.

## Exact next packet: M4.26

**Name:** Independent M4.25 single-manifest dry-run hard-truth audit.

**Bounded question:** Does immutable M4.25 derive every reported path, record,
hash, size, and half-open range truthfully from the same successful single-
manifest preparation, remain write-free and success-silent on every retained
failure, and preserve apply/stage/compose/remove, receipt, compatibility-pin,
and asset boundaries?

**Exact locators and inputs:** intentional clean M4.25 worker commit and direct
parent; this experiment; `EXP-20260814-082/083`; exact worker diff;
`dry_run_manifest`, `_PreparedFile`, `_prepare_manifest`,
`_apply_level_dat_edits`, `_apply_whole_file_replacement`, `_receipt_for` in
`reimplementation/ablpc/manifest.py`; `build_parser`/`main` in
`reimplementation/ablpc/cli.py`; the single refreshed manifest pin;
`tests/test_manifest.py`, `tests/test_level_dat.py`, and
`tests/test_compatibility.py`; M4/M1 notes; every M4.25 stop/done condition.

**First pass:** James must begin in fresh context, reread [[START HERE]] and
the complete required Obsidian startup sequence, verify exact immutable HEAD,
direct parent, and clean Git, then independently derive expected report bytes
without trusting the library. Exercise all four operations across schemas 1/2,
primary/secondary records, same-span sequential guards, no-op values, multiple
authored files/edits, and empty/unequal opaque files. Independently instrument
filesystem mutation surfaces and compare complete no-follow snapshots on
success and invalid/hash/guard/later-file/protected/symlink failures. Verify
stdout determinism/silence, unchanged receipt bytes and accepted workflows,
the new manifest digest, exact other four pins/five membership/nine reads,
focused/canonical/Vault/tracked/MIME/protected/no-game-bytes/diff gates.

**Stop rule:** audit only. Do not change implementation, tests, report,
manifest/receipt schemas, formats, operations, order, guards, source policy,
apply/stage/compose/remove/launch, statement, pin membership/semantics,
authorities, assets, runtime, local game recipes, M2, PS1, `.ALL`, mount,
package, rollback, transaction, or general dry-run scope. A rejection records
one exact bounded correction and changes documentation only.

**Done when:** one independent evidence-backed `ACCEPT` or `REJECT` is
recorded across every required Vault/README surface in a docs-only commit
directly after the worker, and Git is clean. `ACCEPT` selects exactly one
remaining written M4 gate/capability or a bounded milestone-closure audit;
`REJECT` selects exactly one correction with locators, first pass, stop rule,
and done condition.

## Subsequent disposition

[[EXP-20260814-085 - Independent M4.25 single-manifest dry-run hard-truth audit]]
returns `ACCEPT` for exact worker
`58b01d4c415d45ce98952ef0492fbdc51fe9888d` over direct parent
`7a07f55782bec77e25ac9af1c8aeea4e0b3d244b`. Independent direct-byte/report
reconstruction, 91 assertions across 20 cases, zero trapped writes, exact
success/failure snapshots, exact retained receipts/workflows, 38 compatibility
assertions, nine reads, and 99/161/349 tests preserve every M4.25 done
condition. This accepts only the bounded single-manifest report and activates
[[Project Roadmap#M4.27 — M4 v0.1 milestone-closure evidence audit]] without
inferring milestone completion.
