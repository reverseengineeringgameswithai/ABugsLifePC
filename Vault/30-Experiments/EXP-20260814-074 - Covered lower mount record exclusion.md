---
type: experiment
id: EXP-20260814-074
date: 2026-08-14
question: Can ancestry-alias classification ignore a covered lower mount record while retaining every visible alias and exact mounted-plan refusal?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline synthetic filesystem QA in disposable private user and mount namespaces plus user-owned local corpus hash/application checks
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.15 corrective worker packet only; removal-only mountinfo visibility filtering; no executable, original, asset, runtime, M2, PS1, schema, receipt, operation, deletion-target, unmount, staged/source deletion, or transaction change
artifacts:
  - reimplementation/ablpc/manifest.py
  - tests/test_manifest.py
  - tests/mount_overlay_case.py
  - mods/training-primary-record-124-target-111e4.json
  - mods/training-primary-record-125-field-0c-zero.json
  - mods/chars-flick-all-from-chars3-flickd-all.json
addresses: []
file_offsets: []
result: worker-complete-covered-lower-record-exclusion
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
---

# EXP-20260814-074 - Covered lower mount record exclusion

## Bounded question

Can exact M4.15 close the one M4.14 false positive: when a lower bind alias at
the overlay-parent pathname is covered by a distinct ordinary top filesystem,
can removal use the retained mountinfo parent/stack relation to ignore the
hidden lower record, remove an authenticated overlay from the visible top
filesystem, and preserve the source and hidden independent target without
weakening any prior mounted-path refusal?

The executable hash scopes the project, but `bugs.exe` was neither inspected
nor run. No original, game asset, external PS1 material, runtime state,
manifest schema, receipt, operation, deletion target, or source/staged-tree
behavior changed. All mount operations occurred only in disposable private
user and mount namespaces and namespace exit released them.

## Correction

**Confirmed at the M4.15 worker boundary:** `_mount_alias_points` now removes
covered records before either candidate or source alias comparison. A mount is
covered only when another retained mountinfo entry names its mount ID as
`parent_id` and has the same normalized mountpoint. This is the exact relation
observed in the M4.14 falsification: the visible stacked mount names the hidden
lower mount as its parent at the shared pathname. All other mount ID/device/
filesystem-root/path classification remains unchanged.

Filtering both sides is material. It removes a hidden lower alias candidate,
and it also prevents a hidden lower source path from falsely making another
visible same-device mount look like an alias. An uncovered newer mount whose
filesystem root is reachable through an older visible same-device path remains
classified exactly as in M4.13. Exact overlay-root and descendant mountpoints
remain unconditionally refused before traversal or unlink.

This is not a general mount-ownership or portability policy. It is one Linux
mountinfo visibility correction for same-path stacks already represented by
the retained parent relation.

## Private-namespace and pure evidence

The new `stacked` namespace case creates an independent hidden parent and a
marker, bind-mounts that parent at the future overlay-parent pathname, then
covers the lower bind with a distinct `tmpfs` at that exact pathname. It
records the empty visible top filesystem, creates an authenticated sparse
overlay there, and captures complete recursive no-follow metadata/byte
snapshots of the source, hidden target, visible top parent, and overlay.

Removal succeeds and returns the ordinary receipt. The overlay disappears,
the visible top parent returns exactly to its pre-overlay snapshot, and the
source plus hidden independent target remain byte- and metadata-identical.
The existing uncovered proper-parent alias and exact mounted root,
intermediate, output, and receipt cases still refuse before mutation with
their complete snapshots unchanged. All six private-namespace cases pass.

The pure classifier matrix also includes both false-positive orientations:
a hidden lower alias candidate covered by a distinct top filesystem and a
hidden lower source path that would otherwise taint a visible ordinary mount.
Neither enters the alias set. Ordinary root/filesystem/subvolume/same-path/
different-device controls remain clean, while uncovered subdirectory and
whole-filesystem-root aliases remain classified.

## Retained ordinary and local gates

Before documentation, the focused manifest/LEVEL suite passed 102/102 and the
complete canonical `python -m pytest -q tests` suite passed 290/290. The
targeted mount set passed 7/7: one pure classifier, five retained refusal
families, and the new successful stacked case.

All three tracked user-owned local families applied and removed twice in
disposable ordinary directories. Every overlay disappeared, both cycles
produced equal receipt/output hashes, and the exact source hashes remained
unchanged:

| Family | Cycles | Receipt SHA-256 | Output SHA-256 values |
|---|---:|---|---|
| exact opaque replacement | 2/2 | `ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63` | `6e5afb4f...079a4` |
| tracked same-DAT composition | 2/2 | `b899907eec17020f9e7a303b9cd8b5620dc70e83051840d13d57df80b6c779ef` | `78cca99b...1d9a` |
| tracked M1-plus-opaque composition | 2/2 | `f8e144521905cc978e560e01158fae983495693f556f069773c8fac136c815b5` | `6e5afb4f...079a4`, `b8012a95...f720e` |

The unchanged source SHA-256 values are `494d2818...d5a22` for Training
`LEVEL1.DAT`, `a2f23220...f4ac6` for `FLICK.ALL`, and
`6e5afb4f...079a4` for `FLICKD.ALL`.

## Validation and limits

The correction changes only the mount-alias classifier and asset-free tests.
It does not change exact-plan mountpoint refusal, receipt or output
authentication, tree validation, deletion order/targets, source preservation,
composition, or M1 byte behavior. Final `make check` passes dependency smoke
checks, Vault lint over 241 notes with 0 errors/warnings, all 290 canonical
tests, and tracked-file audit with 0 violations. The 18-path worker scope is
entirely text, contains only three Python implementation/test paths plus
Markdown/README documentation, changes no path below `originals/`, `media/`,
`work/`, or `mods/`, and passes diff/no-game-bytes review.

Concurrent mount or I/O changes after preflight, non-Linux portability beyond
existing fail-closed behavior, unmounting, staged-tree or source deletion/
restoration, backup/trash/package management, rollback/general transactions,
receipt/schema migration, broad dry-run, launch, compatibility, N-way
composition, `.ALL`, runtime behavior, M2, and PS1 remain unknown or out of
scope.

## Disposition and exact next packet

At this worker disposition, M4.15 was worker-complete, not independently
accepted, and M4.16 was the exact fresh-context verifier; M2 remained deferred.

**Name:** Independent M4.15 covered-stack hard-truth audit.

**Bounded question:** Does immutable M4.15 exclude only covered lower records
from ancestry alias classification, allow complete authenticated removal on
the visible ordinary top filesystem with source/hidden-target preservation,
and retain every uncovered alias, exact-path, parser/failure, ordinary,
accepted M4, local, and asset-free baseline?

**First pass:** James must reread the complete startup sequence, inspect the
immutable clean worker commit, independently reproduce the hidden-lower/
ordinary-top case with complete no-follow snapshots, and adversarially test
same-path multi-stack order plus hidden candidate and hidden source records.
Reproduce the uncovered exact proper-parent alias and four exact root/
descendant refusals. Retain ordinary/subvolume/same-path/different-device,
subdirectory/whole-root/nested, escape/parser/failure, removal, composition,
topology/schema/receipt, six local, canonical-test, Vault/tracked-file/diff/
no-game-bytes gates.

**Stop rule:** do not change implementation, unmount user paths, introduce a
general mount-ownership or portability policy, change schema/receipt/
operations or deletion targets, add staged/source deletion, restoration,
backup/trash/package, rollback/transactions, or broaden dry-run, launch,
compatibility, N-way composition, `.ALL`, runtime, M2, PS1, or M4.3. Return
`REJECT` only with one exact bounded correction.

**Done condition:** return `ACCEPT` only if every M4.15 condition survives,
then name exactly one successor from a still-unmet written M4 exit gate.
Otherwise return `REJECT` with one actionable correction. Record evidence,
limitations, required Vault updates, intentional documentation-only commit,
and a clean Git tree. Any next worker repeats the startup refresh.

## Subsequent independent disposition

[[EXP-20260814-075 - Independent M4.15 covered-stack hard-truth audit]]
preserves this covered-lower correction, stacked ordinary-top removal, every
retained refusal, and all ordinary/local baselines, but returns M4.16
`REJECT`. Linux reused freed numeric mount ID 1081 for a newer uncovered bind
alias while its still-mounted source held ID 1082. `_mount_alias_points`
treated numeric ID order as creation order and omitted the alias; authenticated
removal returned success and changed the independent mounted target. Exact
corrective M4.17 is the sole next packet.
