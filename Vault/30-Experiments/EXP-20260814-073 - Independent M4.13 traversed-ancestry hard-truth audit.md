---
type: experiment
id: EXP-20260814-073
date: 2026-08-14
question: Does M4.13 distinguish a visible ordinary parent filesystem from a hidden lower stacked alias while retaining exact proper-parent alias refusal?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline synthetic filesystem QA in disposable private user and mount namespaces plus user-owned local corpus hash/application checks
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.14 independent audit of immutable commit 4c0989ed7389556991aaa05bfe83d757b62c7d69; documentation-only verdict; no executable, original, asset, runtime, M2, PS1, schema, receipt, operation, or implementation change
artifacts:
  - reimplementation/ablpc/manifest.py
  - tests/test_manifest.py
  - tests/mount_overlay_case.py
  - mods/training-primary-record-124-target-111e4.json
  - mods/training-primary-record-125-field-0c-zero.json
  - mods/chars-flick-all-from-chars3-flickd-all.json
addresses: []
file_offsets: []
result: rejected-hidden-stacked-alias-misclassifies-visible-ordinary-ancestry
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
  - audit/hard-truth
---

# EXP-20260814-073 - Independent M4.13 traversed-ancestry hard-truth audit

## Verdict and bounded question

M4.14 returns **REJECT** against immutable clean worker commit
`4c0989ed7389556991aaa05bfe83d757b62c7d69`.

M4.13 does reject the exact proper-parent mount alias before overlay traversal
or unlink, and its exact-path, parser/failure, ordinary-removal, accepted M4,
local, and asset-free baselines survive. Its alias set nevertheless includes a
hidden lower stacked mount record even after a distinct ordinary filesystem
covers that record at the identical proper-parent pathname. Removal therefore
misclassifies the currently visible ordinary ancestry and refuses a valid exact
overlay. That falsifies the complete M4.13 classification claim.

The executable hash scopes the project, but `bugs.exe` was neither inspected
nor run. No original, game asset, external PS1 source, or implementation/test/
asset file was modified. All mount operations occurred only in disposable
private user and mount namespaces and namespace exit released them.

## Surviving exact evidence

An independently authored private-namespace case recreated the exact M4.12
proper-parent topology. An authenticated overlay beneath an independent parent
was reached through a sibling bind-mounted parent alias. `_mount_alias_points`
named that proper parent and `remove_manifest` raised
`overlay root ancestry contains a mount alias`. Complete recursive no-follow
snapshots included relative paths, file type/mode, uid/gid, link count, device,
inode, size, regular-file bytes and SHA-256, and symlink targets. Source,
visible overlay, and independent-target snapshots were identical before and
after refusal; the overlay remained.

The adversarial pure matrix preserved ordinary root, filesystem, subvolume,
same-path nested-mount, and different-device records. It classified exact
subdirectory, whole-filesystem-root, and nested aliases; respected older/newer
mount-ID direction; and demonstrated the stacked lower-record result described
below. A separate parser matrix decoded all four supported mountinfo escapes
(`\\011`, `\\012`, `\\040`, and `\\134`) and failed closed on 13 empty,
malformed, non-decimal, zero-ID, bad-device, duplicate-ID, relative, invalid/
truncated-escape, rootless, and read-error cases.

All five tracked private-namespace cases passed: proper ancestor, exact root,
intermediate directory, output, and receipt. The ordinary non-mounted removal,
composition, and topology/schema/receipt selectors passed 32/32, 17/17, and
28/28. The focused manifest/LEVEL suite passed 101/101; the complete canonical
`python -m pytest -q tests` suite passed 289/289.

All three tracked local families applied and removed twice in disposable
ordinary directories. Every overlay disappeared, both cycles produced equal
receipts and outputs, and the three source hashes remained unchanged:

| Family | Cycles | Receipt SHA-256 | Output SHA-256 values |
|---|---:|---|---|
| exact opaque replacement | 2/2 | `ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63` | `6e5afb4f...079a4` |
| tracked same-DAT composition | 2/2 | `b899907eec17020f9e7a303b9cd8b5620dc70e83051840d13d57df80b6c779ef` | `78cca99b...1d9a` |
| tracked M1-plus-opaque composition | 2/2 | `f8e144521905cc978e560e01158fae983495693f556f069773c8fac136c815b5` | `6e5afb4f...079a4`, `b8012a95...f720e` |

The unchanged source hashes were `494d2818...d5a22` for Training
`LEVEL1.DAT`, `a2f23220...f4ac6` for `FLICK.ALL`, and
`6e5afb4f...079a4` for `FLICKD.ALL`.

## One concrete falsification

In one disposable namespace, the QA case first bind-mounted an independent
directory at the future overlay-parent pathname. It then mounted a distinct
ordinary `tmpfs` at that exact pathname, covering the lower alias, and created
an authenticated exact sparse overlay on the visible top filesystem.
Mountinfo retained both records at the same pathname:

- lower record: mount ID 1081, parent ID 1076, device `0:53`, filesystem root
  below the independent directory;
- visible top record: mount ID 1082, parent ID 1081, device `0:73`, filesystem
  root `/`.

The visible overlay ancestry was therefore the ordinary top filesystem; the
lower bind alias was hidden. `_mount_alias_points` still added the shared
pathname because it classifies each record independently and reduces the
result to pathnames without accounting for record visibility. Consequently
`remove_manifest` raised `overlay root ancestry contains a mount alias` and
left the ordinary overlay in place. Complete recursive no-follow snapshots of
the source, hidden independent target, visible ordinary top parent, and overlay
were all identical before and after the refusal.

This is one reproducible false-positive classification, not a concurrency or
portability objection. It contradicts M4.13's required ordinary-filesystem
ancestry boundary while preserving its safe no-mutation refusal behavior.

## Exact corrective packet M4.15

**Name:** Ignore covered lower mount records in ancestry-alias classification.

**Bounded question:** Can removal classify a proper-parent alias from the
currently visible/topmost mount record at that pathname, so a hidden lower
alias covered by a distinct ordinary filesystem does not make ordinary exact
overlay cleanup unusable, while retaining the exact proper-parent alias and
every exact-path, parser/failure, ordinary, accepted M4, local, and asset-free
baseline?

**Exact locators:** `_MountEntry.parent_id`, `_linux_mount_entries`,
`_mount_alias_points`, and `_validate_unmounted_deletion_plan` in
`reimplementation/ablpc/manifest.py`; the five cases in
`tests/mount_overlay_case.py` and `tests/test_manifest.py`; the exact M4.12
alias in [[EXP-20260814-071 - Independent M4.11 mounted-plan-path hard-truth audit]];
the worker evidence in
[[EXP-20260814-072 - Traversed overlay-root ancestry mount-alias refusal]];
and this experiment's same-path stacked-record falsification.

**First pass:** add one asset-free private-namespace regression that installs
a lower proper-parent bind alias, covers it at the identical mountpoint with a
distinct ordinary filesystem, creates an authenticated overlay on the visible
top filesystem, and captures complete recursive no-follow snapshots of source,
hidden target, visible top parent, and overlay. Use mountinfo's retained stack/
parent relation to exclude covered lower records from the ancestry alias set.
The ordinary top overlay must remove completely, while the hidden target and
source remain exact. In the same pass prove the uncovered exact proper-parent
alias still refuses before traversal/unlink and retain subdirectory, whole-
root, nested, same-path, different-device, mount-ID, embedded-escape, and fail-
closed parser controls.

**Stop rule:** do not unmount user paths, introduce a general mount-ownership
or portability policy, change schema/receipt/operations or deletion targets,
add staged/source deletion, restoration, backup/trash/package, rollback or
transactions, or broaden dry-run, launch, compatibility, N-way composition,
`.ALL`, runtime, M2, PS1, or M4.3. Stop with one exact blocker if current
mountinfo cannot distinguish the visible top record within this boundary.

**Done condition:** the stacked ordinary-top case removes its authenticated
overlay completely with source and hidden-target snapshots unchanged; the
uncovered exact proper-parent alias and four exact root/descendant mount cases
still refuse unchanged before traversal/unlink; all classifier/parser,
ordinary removal, accepted composition/topology/schema/receipt, six local,
canonical-test, Vault/tracked-file/diff/no-game-bytes, and clean-tree gates
pass; and an intentional implementation/test worker commit is clean for a
fresh-context verifier. No broader mount or deletion claim follows.

## Limits

Concurrent mount or I/O changes after preflight, non-Linux portability beyond
existing fail-closed behavior, unmounting, staged-tree or source deletion/
restoration, backup/trash/package management, rollback/general transactions,
receipt/schema migration, broad dry-run, launch, compatibility, N-way
composition, `.ALL`, runtime behavior, M2, and PS1 remain unknown or out of
scope. Exactly M4.15 is active; no other successor is selected.

## Subsequent worker disposition

[[EXP-20260814-074 - Covered lower mount record exclusion]] completes exact
M4.15 at the worker boundary. A lower record is removed from alias comparison
only when a same-mountpoint covering entry names it through `parent_id`; this
applies to both candidate and source records. The exact lower-bind/ordinary-top
overlay now removes completely with source and hidden target unchanged, while
the uncovered ancestor and four exact planned-path mounts still refuse.
Exact fresh-context M4.16 is the sole next packet.
