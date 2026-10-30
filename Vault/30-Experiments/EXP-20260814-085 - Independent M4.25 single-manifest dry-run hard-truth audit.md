---
type: experiment
id: EXP-20260814-085
date: 2026-08-14
question: Does immutable M4.25 truthfully derive one deterministic write-free single-manifest report from ordinary preparation while preserving every retained workflow, receipt, compatibility, and asset boundary?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; Linux 7.0.11 x86_64; synthetic asset-free temporary trees only
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact fresh-context M4.26 audit only; immutable worker 58b01d4c415d45ce98952ef0492fbdc51fe9888d over direct parent 7a07f55782bec77e25ac9af1c8aeea4e0b3d244b; no implementation/test/schema/operation/authority/asset/runtime/PS1 change
artifacts:
  - reimplementation/ablpc/manifest.py
  - reimplementation/ablpc/cli.py
  - reimplementation/ablpc/compatibility.py
  - tests/test_manifest.py
  - tests/test_level_dat.py
  - tests/test_compatibility.py
  - reimplementation/compatibility/m4-v0.1.json
addresses: []
file_offsets:
  - synthetic LEVEL DAT primary record 0x98
  - synthetic LEVEL DAT secondary record 0xCC
  - synthetic LEVEL DAT primary field +0x0C at 0xA4
  - synthetic LEVEL DAT primary payload-target field at 0x21C
result: accept-exact-m4.25-single-manifest-dry-run-boundary
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/compatibility
  - audit/hard-truth
---

# EXP-20260814-085 - Independent M4.25 single-manifest dry-run hard-truth audit

## Question

Does immutable M4.25 derive every reported path, record, hash, size, and half-
open range truthfully from the same successful single-manifest preparation,
remain write-free and success-silent on every retained failure, and preserve
apply/stage/compose/remove, receipt, compatibility-pin, and asset boundaries?

## Immutable boundary

The audit began from exact clean worker commit
`58b01d4c415d45ce98952ef0492fbdc51fe9888d`, whose direct parent is exactly
`7a07f55782bec77e25ac9af1c8aeea4e0b3d244b`. `git status --short
--untracked-files=all` was empty before inspection. The complete required
[[START HERE]] and Obsidian corpus, both READMEs, exact worker diff, and every
changed implementation/test file were read before adversarial execution.

No implementation, test, report, manifest, receipt, schema, format, operation,
guard, source-policy, launcher, authority, asset, runtime, M2, PS1, `.ALL`,
mount, package, rollback, transaction, or general dry-run surface was changed.
No game, original, media, local work-copy, or external PS1 byte was read.

## Independent report and output reconstruction

The verifier constructed a LEVEL DAT fixture directly with `struct`, without
using `dry_run_manifest` or its tests to derive expected bytes. Its independently
located primary record is at `0x98`, secondary record at `0xCC`, primary
field-`0x0C` at `0xA4`, and payload-target field at `0x21C`. Direct bytearray
patches independently produced the expected final output.

The exact report object and indented CLI bytes matched for:

- all three LEVEL operations under schemas 1 and 2;
- primary and secondary records;
- six authored edits including repeated guarded writes to the same two- and
  four-byte spans, no-op guarded values, a no-op secondary position, and a
  later secondary position change;
- authored multi-file order deliberately opposite lexical order;
- multiple edits plus whole-file replacement in one schema-2 manifest;
- empty, shorter, and longer opaque replacements, including distinct exact
  input and output half-open extents.

The expected canonical manifest identity was reconstructed by deep-copying the
manifest, lowercasing only the declared hashes, and independently serializing
sorted compact JSON. Input and output sizes and SHA-256 values were recomputed
from the original and directly patched/replacement bytes. Two CLI invocations
matched the entire expected indented JSON byte-for-byte, including the final
newline. Each library success invoked `_prepare_manifest` exactly once. An
ordinary `apply` produced the independently patched bytes.

This verifier-owned matrix passed 91 assertions across 20 named cases: six
dry-run success families, ten retained failure families, and four retained
workflow/receipt families.

## Write-free and failure evidence

Complete recursive no-follow snapshots retained path, type, mode, ownership,
link count, size, modification time, regular-file bytes, symlink targets, and
special-file identity. They were identical before and after successful
library/CLI dry-runs and every failure.

Independent traps covered `Path` write/open modes, built-in and `io` write
modes, `os.open` write flags, `os` create/rename/remove/link operations,
`shutil` copy/move/removal operations, and `tempfile` creation APIs. They
observed zero mutation attempts. CLI failures returned status 2, emitted an
`ablpc-mod:` diagnostic on stderr, and emitted exactly zero stdout bytes for:

1. invalid manifest;
2. destination input-hash mismatch;
3. replacement-hash mismatch;
4. record-guard mismatch;
5. a valid first file followed by a bad later file;
6. protected source root;
7. missing source file;
8. non-regular source path;
9. destination-source symlink escape;
10. replacement-source symlink escape.

The later-file case proves complete preparation precedes successful report
emission; the full snapshot proves the earlier valid file leaves no artifact.

## Retained workflow and receipt evidence

An ordinary replacement receipt was independently assembled and serialized as
the pre-existing indented JSON plus newline. `apply_manifest` and
`stage_manifest` returned that exact object and wrote those exact receipt
bytes. `remove_manifest` authenticated and removed the exact sparse overlay,
returned the same receipt, and preserved the source. Two disjoint schema-1/
schema-2 LEVEL manifests still composed, and applying the composed result
matched independent direct position and field patches. Static worker-diff
review confirms that ordinary receipt keys and `_receipt_bytes` were not
changed.

## Compatibility and asset evidence

An independent AST parse reconstructed exactly five pin members and values.
Raw hashing reproduced:

- `reimplementation/ablpc/manifest.py`:
  `ce66bd048e505546c002ebe8a1fdc4477822363cce8e4631618dd157a9c3d243`;
- Training manifest:
  `315320bc524986348167ca556b178ef41fe1e8ac961e482610f8f734f34b2434`;
- Level 01 manifest:
  `358998cd326f68fcf7e10593e8ec895915b558252c300464e8fe74177280198f`;
- opaque replacement manifest:
  `5aaa6e9a4fa79c303ee0920e7f87e00e87bd1dfef412a32c55e36efcc947b607`;
- launcher:
  `68c9171749bd7b207a15b4202193ccfddd2661fbb383deb34b1a5a5a4049977e`.

Direct manifest-implementation drift and each missing pinned file failed before
recipe semantic alignment. Unchanged alignment opened exactly nine unique
asset-free paths in the required order, each pin once, and reused those same
reads. The compatibility statement remains exact canonical JSON of 6,177
bytes, SHA-256
`c3427d44cf32619a1f9bbcab7c51e67c0846b35d9d53eab7632ff6356c0beaf0`.
This independent compatibility audit passed 38 assertions.

## Test and hygiene gates

- focused manifest suite: 99/99 passed;
- combined manifest/LEVEL/compatibility suite: 161/161 passed;
- canonical suite: 349/349 passed;
- `make check`: Python doctor green, Vault lint green, five-anchor compatibility
  checker green, 349 tests, tracked-file audit zero violations, diff checks
  clean;
- immutable worker diff: 19 paths, zero binary numstat entries, zero protected
  paths, zero forbidden media/game extensions, and only `text/plain` or
  `text/x-script.python` MIME classifications;
- statement, launcher, tracked manifests, assets, originals, media, work,
  runtime, and external PS1 boundaries remained untouched.

## Verdict

`ACCEPT` exact M4.25. No concrete reproducible falsification survived. The
report truthfully derives its authored paths, canonical manifest identity,
record locators, input/output bytes, hashes, sizes, and exact half-open spans
from one successful ordinary single-manifest preparation. It creates no output
or receipt, emits no success document on a retained failure, and leaves the
accepted apply/stage/compose/remove, receipt, compatibility-pin, and asset
boundaries intact.

Acceptance is deliberately narrower than general dry-run support. It does not
cover composed/N-way reports, semantic diffs, persisted reports, output-tree
simulation, runtime launch automation, packaging, rollback, transactions,
general `.ALL`, broader hosts, or a new input policy. It does not itself mark
M4 complete.

## Sole successor: M4.27

**Name:** M4 v0.1 milestone-closure evidence audit.

**Bounded question:** Do the independently accepted M4 results through M4.26
jointly satisfy every written M4 required capability and exit gate at their
stated exact boundaries, with a traceable current command/test/documentation
surface and no unsupported compatibility, asset, runtime, or transaction
claim; if not, what one exact unmet gate is the sole next packet?

**Exact locators and inputs:** [[Project Roadmap#M4 — Mod toolkit v0.1]] and
its complete M4.1–M4.26 ratchet; this audit and `EXP-20260814-060` through
`EXP-20260814-084`; [[M1 Tool Support Matrix]]; [[M4 Exact Whole-file Replacement]];
[[Wine Linux Play Baseline]]; [[Environment Status]]; both READMEs; the v0.1
compatibility statement/checker; tracked manifests and launcher; current CLI,
manifest, LEVEL DAT, compatibility, and asset-free tests; tracked-file policy.

**First pass:** build an explicit ledger with one row per written required
capability and exit gate. For every row, cite an independently accepted
experiment, the current executable command/test that retains it, its user
documentation, and its exact limitation. Re-run the complete asset-free M4/M1
and hygiene gates. Treat absent independent evidence, stale documentation,
contradictory scope, or a capability that exists only in prose as an open gate.
Do not infer closure from the number of completed packets. If every row is
supported, record the exact M4 v0.1 closure boundary; otherwise select exactly
one smallest unmet written gate as the next packet.

**Stop rule:** audit and documentation only. Do not change implementation,
tests, manifests, receipts, schemas, formats, operations, ordering, guards,
source/input policy, compatibility statement or pins, authorities, launcher,
assets, runtime, local game recipes, M2, PS1, `.ALL`, mount policy, package,
rollback, transaction behavior, or general automation. Do not execute or read
game/original/media/work-copy bytes.

**Done when:** one evidence ledger covers every written M4 capability and exit
gate without contradiction; one `ACCEPT` or `REJECT` closure verdict is
recorded across all required Vault/README surfaces; `REJECT` selects exactly
one bounded missing gate, while `ACCEPT` may mark only the documented v0.1
scope complete; all asset-free canonical/Vault/tracked/MIME/protected/no-game-
bytes/diff gates pass; one intentional docs-only commit follows this verdict;
and Git is clean.

## Disposition by M4.27

[[EXP-20260814-086 - M4 v0.1 milestone-closure evidence audit]] completes the
required 14-row ledger and returns `REJECT`. The exact M4.25 acceptance remains
unchanged. Milestone closure fails because current receipts are not sufficient
without the original manifest and because the clean-copy install/validation/
launch/removal gate is not joined. Exact M4.28 selects only strict current-
receipt replay/removal reconstruction first.
