---
type: experiment
id: EXP-20260814-071
date: 2026-08-14
question: Does immutable M4.11 worker commit b91712f cover a pre-existing mount alias in the proper path ancestry used to reach an exact sparse-overlay root?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline filesystem QA and user-owned local corpus hash/application checks
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.12 independent audit of immutable worker commit b91712fb4cfa7412f867239292c0c3bc7e97828a; documentation closure used no namespace or mount commands; no implementation, executable, original, game-runtime, or PS1 work
artifacts:
  - reimplementation/ablpc/manifest.py
  - tests/test_manifest.py
  - tests/mount_overlay_case.py
  - mods/training-primary-record-124-target-111e4.json
  - mods/training-primary-record-125-field-0c-zero.json
  - mods/chars-flick-all-from-chars3-flickd-all.json
addresses: []
file_offsets: []
result: reject-proper-parent-mount-alias-not-covered
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
  - audit/hard-truth
---

# EXP-20260814-071 - Independent M4.11 mounted-plan-path hard-truth audit

## Bounded question and immutable input

Does immutable clean M4.11 worker commit
`b91712fb4cfa7412f867239292c0c3bc7e97828a` reject every supported
pre-existing mountpoint or mount alias traversed by exact sparse-overlay
removal before mutation, including an alias in the proper path ancestry used
to reach the overlay root?

James confirmed exact `HEAD`, a clean tree, and the worker diff before review.
The complete required startup chain, exact M4.12 packet, `EXP-20260814-069/070`,
worker session, implementation and M1 notes, MOCs, READMEs, cleanup code, tests,
and tracked manifests were reread. No external comparative source, original,
executable, game runtime, or implementation was read, launched, or changed.

## Independently surviving evidence

The worker's exact-root and descendant-plan implementation is supported at its
declared ordinary boundary:

- `_linux_mount_points` reads Linux `/proc/self/mountinfo`, rejects missing,
  malformed, non-absolute, duplicate-ID, or rootless topology, and decodes the
  kernel path escapes accepted by `_decode_mountinfo_path`;
- `_validate_unmounted_deletion_plan` compares the resolved overlay root, every
  necessary overlay directory, every recorded output, and the fixed receipt
  before `_validate_existing_regular_file`, `_validate_exact_overlay_tree`,
  receipt/output reads, or unlink;
- 12/12 pure-function mountinfo decoding and fail-closed parser checks passed
  without invoking a namespace or mount command, covering all four supported
  escapes plus valid, empty, malformed, non-decimal, non-absolute, invalid-
  escape, duplicate-ID, and rootless tables;
- 32/32 ordinary non-mounted removal tests, 17/17 composition tests, and 28/28
  topology/schema/receipt selectors passed;
- the focused manifest/LEVEL suite passed 95/95 and the complete canonical
  suite passed 283/283, with exactly the four namespace-backed mounted-path
  cases deselected because this documentation closure was forbidden to invoke
  namespace or mount commands; and
- the exact opaque, same-DAT composed, and M1-plus-opaque local families each
  applied and removed twice in ordinary disposable directories. All six
  overlay roots disappeared and all three source hashes remained unchanged.

The local receipts remained:

- opaque replacement:
  `ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63`;
- same-DAT composition:
  `b899907eec17020f9e7a303b9cd8b5620dc70e83051840d13d57df80b6c779ef`;
- M1 plus opaque replacement:
  `f8e144521905cc978e560e01158fae983495693f556f069773c8fac136c815b5`.

The unchanged source hashes were:

- `CD/LEVEL07/LEVEL1.DAT`:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`;
- `CD/CHARS/FLICK.ALL`:
  `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`;
- `CD/CHARS3/FLICKD.ALL`:
  `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.

These checks preserve every accepted ordinary M4 baseline. They do not repair
the falsification below.

## Falsification

The prior James review used a disposable QA helper to construct an exact
ordinary overlay whose overlay root and descendants were not mountpoints, but
whose proper parent directory was a pre-existing alias to an independent
parent containing that overlay. The visible manifest/source/receipt/output
state was otherwise exact. Cleanup returned success and removed the overlay
through the alias from the independent parent.

Root independently repeated that same disposable layout once and observed the
same result. Across the two reproductions:

- source snapshot preserved: true;
- removal returned success: true;
- visible overlay snapshot preserved: false; and
- independent-target snapshot preserved: false.

The QA helper and all temporary data were deleted after the review, and Git
remained clean. The topology existed before preflight and did not change during
cleanup, so this is one stable filesystem-layout condition rather than a
concurrent race.

Static inspection explains the bypass. `_resolved_root` resolves the supplied
overlay path, but `_validate_unmounted_deletion_plan` constructs
`planned_paths` from only that exact overlay root and its expected descendant
directories/files. It never compares the proper parent directories traversed
to reach the overlay root with the mount table. A mount alias at such a proper
parent therefore matches no checked plan path even though every later overlay
operation traverses it.

## Verdict

**REJECT.** M4.11 is not independently accepted. The exact root,
intermediate, output, receipt, parsing, ordinary-removal, composition, schema,
receipt, and local-recipe baselines survive; the universal mounted-plan-path
claim does not. M4 remains active on exactly one bounded correction, M4.13.
No implementation, schema, receipt, operation, or accepted M4.3/M4.7 boundary
changes in this audit.

## Exact corrective packet: M4.13

**Name:** Include traversed overlay-root ancestry in mount-topology preflight.

**Bounded question:** Can `remove_manifest` include the proper path ancestry
traversed to reach the supplied/resolved overlay root in its pre-deletion
topology check, so a pre-existing alias at a proper parent refuses before the
first unlink while ordinary cleanup beneath normal filesystem ancestry remains
usable and every accepted baseline is retained?

**Exact locators:** `remove_manifest`, `_resolved_root`,
`_reject_output_symlink_components`, `_validate_output_root_topology`,
`_validate_unmounted_deletion_plan`, and `_linux_mount_points` in
`reimplementation/ablpc/manifest.py`; the existing root/intermediate/output/
receipt cases in `tests/mount_overlay_case.py` and `tests/test_manifest.py`;
the proper-parent-alias falsification in this experiment; and every ordinary,
composition, topology, schema, receipt, and local matrix above.

**First pass:** add one asset-free regression reproducing an exact overlay
whose own root and descendants are unmounted while one proper parent traversed
to reach it is an alias to an independent parent. Capture complete no-follow
overlay, source, and independent-target snapshots. Extend only removal's
mount-topology preflight input to cover the relevant traversed proper ancestry,
and prove refusal occurs before overlay traversal or unlink. Preserve an
ordinary-overlay positive control under normal root/filesystem mount ancestry,
the four existing exact mounted-path refusals, mountinfo parsing/failure
behavior, all ordinary refusal/success cases, and all six local cycles.

**Stop rule:** do not unmount user paths; introduce a general mount-ownership
or portability policy; change a schema, receipt, operation, or deletion target;
add staged/source deletion, restoration, backup, trash, package, rollback, or
general transactions; broaden dry-run, launch, compatibility, N-way
composition, `.ALL`, runtime, M2, PS1, or the accepted M4.3 claim. If the
proper-parent alias cannot be rejected without making ordinary cleanup
unusable or entering one of those expansions, stop and record that exact
blocker.

**Done condition:** the proper-parent-alias case refuses before the first
unlink with exact overlay/source/independent-target snapshots unchanged; an
ordinary overlay beneath normal filesystem ancestry still removes completely;
the four existing exact mounted-path cases, mountinfo failure/parser cases,
ordinary M4.9 success/refusal matrices, accepted M4 baselines, all six local
cycles, scoped tests, Vault lint, tracked-file, diff, no-game-bytes, and clean-
tree gates pass; documentation states only this ancestry correction; and the
intentional worker commit is clean for fresh-context M4.14 review.

## Subsequent M4.13 disposition

[[EXP-20260814-072 - Traversed overlay-root ancestry mount-alias refusal]]
completes the exact corrective worker packet. The reproduced proper-parent
alias now refuses before overlay content traversal or unlink with visible-
overlay/source/independent-target snapshots unchanged. Exact mounted root/
descendant cases remain green, and normal root, `/home`, `/tmp`, and same-path
filesystem mounts remain usable. M4.13 is worker-complete, not independently
accepted; exact fresh-context M4.14 is active.
