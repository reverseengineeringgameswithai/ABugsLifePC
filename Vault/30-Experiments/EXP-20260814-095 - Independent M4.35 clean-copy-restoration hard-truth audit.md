---
type: experiment
id: EXP-20260814-095
date: 2026-08-14
question: Does immutable M4.35 authenticate the complete current-Linux staged-tree restoration boundary before mutation?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; fresh synthetic trees, private mount namespaces, and exact user-owned ignored local recipe checks
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.36 audit of immutable M4.35 worker 51aea1a1ca59790f62ded58e2122be088a8b53a1 and direct M4.34 parent a8012745183124d5ed84fe915a5867cbb2b8146b; no game execution or implementation/test/pin/statement/launcher/asset change
artifacts:
  - reimplementation/ablpc/manifest.py
  - tests/test_manifest.py
  - tests/mount_overlay_case.py
  - reimplementation/compatibility/m4-v0.1.json
  - Vault/30-Experiments/EXP-20260814-093 - Clean-derived-copy lifecycle feasibility audit.md
  - Vault/30-Experiments/EXP-20260814-094 - Manifest-driven clean-copy restoration.md
addresses: []
file_offsets: []
result: reject-complete-tree-windows-case-collision-accepted
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - audit/hard-truth
---

# EXP-20260814-095 - Independent M4.35 clean-copy-restoration hard-truth audit

## Verdict

**REJECT exact M4.35 acceptance.** The ordinary lifecycle, complete-tree
content checks, mount/alias checks, and retained gates survive, but the source
and staged-game inventories accept two distinct Linux paths that are equal
under the project's Windows-path normalization. A fresh source containing
both `unrelated/Case.bin` and `unrelated/case.bin` stages and restores
successfully. The post-restore independent oracle is equal to the source, so
the failure is not byte restoration; it is admission of an ambiguous Windows
game tree.

`KU-052` and M4 remain open. The compatibility statement remains unchanged.
The sole successor is exact M4.37, a case-insensitive complete-tree path-
uniqueness correction before restoration mount traversal or mutation.

## Immutable and safety boundary

The audit began with an empty `git status --short`, exact HEAD
`51aea1a1ca59790f62ded58e2122be088a8b53a1`, and exact direct parent
`a8012745183124d5ed84fe915a5867cbb2b8146b`. The full startup packet, M4.36
roadmap contract, both parent experiments, decision/unknown/MOC state, M1/M4
notes, launcher and Wine baseline, both READMEs, complete worker diff, and
every changed implementation/test file were reviewed before testing.

No game was executed. The only launcher action was `--dry-run`. No original,
media, PS1, protected-root, implementation, test, pin, statement, launcher,
manifest, receipt, schema, operation, or local game-copy byte changed. All
synthetic and derived outputs were isolated and removed.

## Independent oracle and parent reproduction

The separate oracle recursively uses no-follow metadata, records every
relative file/directory path, rejects nonordinary entries, requires file link
count one, and compares file size and SHA-256. It does not reuse the worker's
inventory or equivalence helpers.

The M4.34 parent mismatch was reproduced first. `stage` created a complete
source-derived tree, then dedicated sparse `remove` refused its unrelated
content with `overlay contains extra content: S (directory)`. Complete source
and staged-tree snapshots remained exact.

Eleven independently built ordinary restoration cases passed the oracle:
empty, short, and longer opaque replacements; schemas 1 and 2 across position,
field-`0x0C`, and payload-target operations; multi-output opaque; and composed
same-DAT M1. All restored trees equaled their sources and removed `.ablpc`.

## Refusal and mutation evidence

Eighteen fresh ordinary attacks refused before tool mutation with complete
source/game snapshots exact: source destination and replacement drift, output
and unrelated game drift, extra and missing paths, receipt and manifest drift,
reserved `.ablpc`, game symlink/FIFO/hardlink, same/overlapping roots, and
protected source/output roots. Character-device creation was denied by the
host even inside a mapped-root user namespace; mounted-path and general
nonregular refusal remain covered independently, but no unmounted device node
claim is made.

Five deterministic inode swaps were injected between inventory and stable
read for source output, source unrelated, game output, receipt, and game
unrelated files. All 5/5 raised `changed during restoration preflight`; the
separate path/type/content oracle stayed exact and no recorded destination or
receipt was restored or removed. CLI success returned status 0 and receipt
JSON with empty stderr. Extra-content failure returned status 2, empty stdout,
prefixed stderr, and exact source/game snapshots.

The four worker namespace cases for game root, recorded output, receipt, and
unrelated file pass 4/4. Four fresh extensions also pass:

- an uncovered proper-parent bind alias refuses with source and independent
  target exact;
- a mounted unrelated directory refuses unchanged;
- a distinct ordinary top mount correctly hides a lower same-path alias and
  allows ordinary stage-to-restore; and
- a released mountinfo ID was reused (`1189`, source mount `1190`) by a later
  proper-parent alias, whose explicit later order still causes refusal.

The environment forbids an unmounted device-node fixture. This is recorded as
an environmental limitation, not counted as a pass.

## Reproducible rejection

`_regular_tree_inventory` stores exact `PurePosixPath` keys at
`reimplementation/ablpc/manifest.py:1680-1710`. Complete-tree expected/actual
sets are likewise compared by exact host spelling at lines 1766-1812. Neither
path rejects two entries with the same case-folded spelling. In contrast, the
manifest contract uses `_normalized_windows_path`, and the PC content census
already rejects case-insensitive duplicate paths at
`reimplementation/ablpc/content_census.py:76-91`.

A source containing ordinary single-link files at both
`unrelated/Case.bin` and `unrelated/case.bin`, with different bytes, passed
`stage_manifest`. `restore_manifest` returned success, removed its receipt,
and left a game oracle exactly equal to that ambiguous source. A second
`CON`/`con` collision reproduced the same acceptance. This is a complete-tree
admission gap at the Windows game boundary, not a claim about general Windows
reserved-device names.

## Exact local and retained gates

One disposable exact tree below `work/copies/` completed `stage`, launcher
`--dry-run`, and `restore` without executing the game. The staged receipt hash
was `ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63`,
the replacement output hash was
`6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`,
and the launcher reported the exact executable hash. The independent oracle
matched all 722 files and 26 directories before/after; source remained exact,
`.ablpc` disappeared, and cleanup completed.

All six sparse local cycles passed with prior hashes: opaque receipt/output
`ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63` /
`6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`;
same-DAT receipt/output
`b899907eec17020f9e7a303b9cd8b5620dc70e83051840d13d57df80b6c779ef` /
`78cca99b1993cc6deff8f89104d6f6aa8154ed7063e4ab0b56195e4321761d9a`;
and M1-plus-opaque receipt
`f8e144521905cc978e560e01158fae983495693f556f069773c8fac136c815b5`
with DAT
`b8012a95f7ec0254805bdd3cf32df2b16f2ad0926308fe8678cc2360027f720e`
and opaque
`6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.
Source hashes remained Training DAT
`494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`,
opaque destination
`a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`,
and replacement
`6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`;
no output survived.

Manifest/M1/compatibility tests pass 250/250; canonical tests pass 438/438.
The exact five machine pins and exactly nine asset-free reads reproduce. Final
Vault lint, compatibility, tracked-file, diff, and no-game-bytes gates are
recorded by the verdict commit.

## Limits

This rejection neither disputes the exact 722-file local success nor expands
the restoration contract. It does not claim POSIX metadata equivalence,
provenance, authorship, external-receipt full-tree restoration, whole-tree or
source deletion, package, backup, rollback, transaction, post-preflight
concurrency, broader platforms, runtime behavior, M2, or PS1 correspondence.

## Sole successor

Exact M4.37 is **case-insensitive complete-tree path uniqueness**. Before
restoration mount traversal, reads, writes, or unlinks, derive one normalized
Windows key for every source inventory entry and fail closed if two distinct
file/directory paths share it. Apply the same invariant to the staged-game
expected/actual comparison, including file/directory and ancestor collisions;
retain the reserved `.ablpc` rule. Reproduce `Case.bin`/`case.bin` and nested
file/directory collisions with complete source/game snapshots exact, then
retain every M4.36 success, refusal, namespace, local, pin/read, canonical, and
hygiene gate. Do not alter manifests, receipts, schemas, operations, sparse
removal, launcher, statement, assets, runtime, M2, PS1, or broaden to general
Windows reserved-name policy. Stop after one worker commit and exact M4.38
verifier packet.

## Disposition

[[EXP-20260814-096 - Complete-tree case-insensitive path uniqueness]] now
implements the sole correction at the worker boundary and activates only
fresh-context M4.38. This audit's `REJECT` remains the parent disposition;
[[EXP-20260814-097 - Independent M4.37 complete-tree-uniqueness hard-truth audit]]
subsequently accepts the corrected immutable worker and resolves `KU-052`
only at the demonstrated current-Linux lifecycle. M4 remains active on exact
M4.39 statement alignment.
