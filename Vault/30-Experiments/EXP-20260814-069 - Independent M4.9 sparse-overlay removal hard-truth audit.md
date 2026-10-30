---
type: experiment
id: EXP-20260814-069
date: 2026-08-14
question: Does immutable M4.9 worker commit ad1d965 fully preflight every authenticated sparse-overlay removal before any filesystem mutation?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline synthetic filesystem QA and user-owned local corpus hash/application checks
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.10 independent audit of immutable worker commit ad1d9651e60e6b3861eddf0e865fa279d93fd025; private user and mount namespace for one bind-mount topology case; no implementation, executable, original, game-runtime, or PS1 work
artifacts:
  - reimplementation/ablpc/manifest.py
  - reimplementation/ablpc/cli.py
  - tests/test_manifest.py
  - tests/test_level_dat.py
  - mods/training-primary-record-124-target-111e4.json
  - mods/training-primary-record-125-field-0c-zero.json
  - mods/chars-flick-all-from-chars3-flickd-all.json
addresses: []
file_offsets: []
result: reject-mounted-overlay-directory-can-mutate-before-ebusy
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
  - audit/hard-truth
---

# EXP-20260814-069 - Independent M4.9 sparse-overlay removal hard-truth audit

## Bounded question and immutable input

Does immutable clean M4.9 worker commit
`ad1d9651e60e6b3861eddf0e865fa279d93fd025` support every declared receipt,
source, output, topology, full-preflight, removal, source-preservation, and
accepted-baseline condition at the dedicated ordinary sparse-overlay boundary?

James confirmed exact `HEAD`, a clean tree, and the worker diff before testing.
The complete required startup sequence, exact M4.10 packet, worker evidence,
implementation, tests, tracked manifests, and documentation were reread. No
external comparative source, original, executable, or game runtime was read,
launched, or modified.

## Independently surviving evidence

An independent no-follow snapshot harness, separate receipt/hash calculations,
and synthetic data confirmed:

- 4/4 ordinary single-file, empty-output, multi-file deep/shared-directory,
  and composed overlays had byte-exact receipts, strict JSON, exact output
  hashes and topology, expected returned receipts, complete pruning/root
  removal, and unchanged sources;
- 41/41 changed/missing/type/link/receipt/source/manifest/content cases refused
  with exact complete overlay and source snapshots unchanged;
- 2/2 safe lexical root aliases removed successfully and 16/16 unsafe root,
  case, overlap, protected, topology, schema/path-drift, and staged-tree cases
  refused with exact snapshots unchanged;
- 6/6 position, `+0x0C`, and payload-target applications under schemas 1 and 2
  succeeded; all 3/3 cross-schema byte/receipt comparisons matched; and all
  3/3 receipt-order/edit-index/manifest-edit drift cases refused unchanged;
- focused manifest/LEVEL tests passed 95/95, the complete canonical suite
  passed 283/283, and the composition, receipt, and topology selectors passed
  17/17, 19/19, and 22/22 respectively.

The three tracked local manifest families each completed apply/remove twice,
for 6/6 deterministic cycles. Their receipt hashes were:

- opaque replacement:
  `ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63`;
- same-DAT composition:
  `b899907eec17020f9e7a303b9cd8b5620dc70e83051840d13d57df80b6c779ef`;
- M1 plus opaque replacement:
  `f8e144521905cc978e560e01158fae983495693f556f069773c8fac136c815b5`.

The exact source hashes before and after all six cycles were unchanged:

- `CD/LEVEL07/LEVEL1.DAT`:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`;
- `CD/CHARS/FLICK.ALL`:
  `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`;
- `CD/CHARS3/FLICKD.ALL`:
  `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.

All six overlay roots were absent afterward. These checks support the ordinary
non-mounted boundary but do not repair the falsification below.

Post-documentation closure repeated the focused suite at 95/95 and the complete
suite at 283/283. `make check` then passed Python dependency smoke checks,
283/283 canonical tests, Vault lint over 231 notes with zero errors/warnings,
the tracked-file audit with zero violations, and both diff checks. Only
Markdown documentation is part of the audit commit.

## Falsification

Inside a private user and mount namespace, the audit applied a valid one-file
manifest to `overlay/D/shared/deep/out.bin`, moved the ordinary `D` directory
to an independent temporary directory, recreated `overlay/D`, and bind-mounted
the independent directory there. The visible overlay still contained exactly
the authenticated ordinary paths and bytes:

- `.ablpc/receipt.json`;
- `D/shared/deep/out.bin`; and
- only their necessary directories.

The current `lstat`/`scandir` checks in `_validate_existing_regular_file` and
`_validate_exact_overlay_tree` treat the mounted directory as an ordinary
directory. `remove_manifest` therefore completed preflight, unlinked the
recorded output through the mount, unlinked the receipt, and pruned the child
directories. It then raised `OSError: [Errno 16] Device or resource busy` when
removing mounted `overlay/D`.

The case reproduced independently twice. Both runs began with the exact
expected visible overlay. Both ended with:

- source snapshot preserved: true;
- overlay snapshot preserved: false (only root plus mounted `D` remained);
- independent mounted-directory snapshot preserved: false (its recorded file
  and child directories were deleted).

This is a deterministic, pre-existing topology condition, not a concurrent
change after preflight. It falsifies the M4.9 claim that the complete deletion
plan is fully preflighted and that rejected removal leaves the exact overlay
unchanged. Ordinary hashes, receipt bytes, single-link checks, and no-follow
directory enumeration do not establish that every deletion-plan path belongs
to the overlay's own mount topology.

## Verdict

**REJECT.** M4.9 is not independently accepted. M4 remains active on exactly
one bounded correction, M4.11. The audit changes no implementation, manifest
schema, receipt, operation, or accepted M4.3/M4.7 claim.

## Exact corrective packet: M4.11

**Name:** Reject mounted sparse-overlay deletion-plan paths before mutation.

**Bounded question:** Can `remove_manifest` reject a pre-existing mountpoint or
mount alias anywhere in the supplied overlay deletion plan before the first
unlink, while preserving exact overlay, source, and independently mounted
directory snapshots and retaining every ordinary M4.9 baseline?

**Exact locators:** `remove_manifest`, `_validate_existing_regular_file`, and
`_validate_exact_overlay_tree` in `reimplementation/ablpc/manifest.py`; the
root/ancestor topology helpers used by removal; synthetic overlay roots and
directories in a private user/mount namespace; and every M4.10 retained
ordinary/local matrix above.

**First pass:** add one removal-preflight mount-topology guard for the overlay
root and every directory/file path in the authenticated deletion plan. Refuse
before mutation if any plan path is a mountpoint or crosses a mount alias. Add
asset-free isolated bind-mounted root/intermediate/recorded-file/receipt cases
as supported by the host, and prove exact overlay/source/external snapshots.
Re-run ordinary removal success/refusal, accepted M4 baselines, all three local
recipes twice, canonical tests, Vault lint, tracked-file, no-game-bytes, and
clean-tree gates.

**Stop rule:** do not unmount user paths; change a schema, receipt, or existing
operation; add staged-tree deletion, source restoration/deletion, backup,
trash, package, rollback, or general transactions; broaden dry-run, launch,
compatibility, N-way composition, `.ALL`, runtime, M2, PS1, or the accepted
M4.3 deterministic-preflight claim.

**Done condition:** every supported pre-existing mounted path in the exact
removal plan refuses before the first unlink with byte/type/link-complete
overlay, source, and independent target snapshots unchanged; ordinary M4.9
success/refusal matrices, accepted M4 baselines, all six local cycles, scoped
tests, documentation/tracked-file/no-game-bytes gates pass; the worker commit
is intentional and clean for a new fresh-context audit.
