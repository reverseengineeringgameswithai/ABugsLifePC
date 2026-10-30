---
type: experiment
id: EXP-20260814-072
date: 2026-08-14
question: Can sparse-overlay removal reject an alias mount in the proper ancestry traversed to the overlay root while retaining ordinary filesystem-mount cleanup?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline synthetic filesystem QA in private user and mount namespaces plus user-owned local corpus hash/application checks
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.13 corrective worker packet only; removal-only mountinfo ancestry-alias classification; no user-path unmount, general mount-ownership policy, schema/receipt/operation change, staged/source deletion, rollback/transaction, runtime, M2, or PS1 work
artifacts:
  - reimplementation/ablpc/manifest.py
  - tests/test_manifest.py
  - tests/mount_overlay_case.py
  - reimplementation/README.md
  - mods/training-primary-record-124-target-111e4.json
  - mods/training-primary-record-125-field-0c-zero.json
  - mods/chars-flick-all-from-chars3-flickd-all.json
addresses: []
file_offsets: []
result: worker-complete-proper-ancestry-mount-alias-refusal
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
---

# EXP-20260814-072 - Traversed overlay-root ancestry mount-alias refusal

## Bounded question

Can exact M4.13 close the proper-parent alias falsification from
[[EXP-20260814-071 - Independent M4.11 mounted-plan-path hard-truth audit]]
without rejecting ordinary cleanup merely because `/`, `/home`, `/tmp`, or
another normal filesystem mount lies above the overlay: include only relevant
alias-like mount records in the proper ancestry traversed to the overlay root,
then refuse before overlay content traversal or unlink with complete snapshots
unchanged?

The executable hash scopes the project but executable contents were not read or
run. No original, game file, runtime state, or external PS1 material was
modified or consulted. Local checks read only the ignored user-owned derived
work copy and wrote disposable temporary overlays.

## Correction

**Confirmed at the M4.13 worker boundary:** mountinfo parsing now retains each
record's mount ID, device pair, filesystem root, and mountpoint. Exact overlay-
root and descendant-plan mountpoints retain M4.11's unconditional refusal.
For proper overlay-root ancestry only, `_mount_alias_points` identifies a newer
mount record whose filesystem root is already reachable through an older mount
record on the same device but whose computed earlier visible path differs from
the new mountpoint. That is the stable path-alias topology in M4.12.

The guard deliberately does not reject an ordinary filesystem boundary merely
for being mounted. Synthetic classification retains normal root, `/home`
subvolume, `/tmp` filesystem, and same-path nested filesystem records, while
classifying both a mounted subdirectory alias and a whole-filesystem-root alias.
`_validate_unmounted_deletion_plan` compares those alias mountpoints with every
proper parent of the resolved overlay root before the prior overlay tree,
receipt, output-hash, or unlink phases.

This is not a general mount-ownership or portability policy. It is one Linux
mountinfo discriminator for a filesystem location that is already visible at
an older path and then re-exposed at a different proper-parent path.

## Exact private-namespace evidence

`tests/mount_overlay_case.py` adds one `ancestor` case. It first creates an
ordinary authenticated overlay under an independently snapshotted parent, then
binds that parent onto a sibling alias parent and supplies the descendant
`overlay root` path to removal. The exact overlay root, its necessary
directories, recorded output, and receipt are not mountpoints; only the proper
parent used to reach them is the alias.

The case refuses with `ManifestError` containing
`overlay root ancestry contains a mount alias`. Complete recursive no-follow
snapshots of the visible overlay, source, and independent parent remain exactly
equal before and after the call. The same helper retains the four M4.11 cases:
exact mounted root, intermediate directory, output, and receipt. All five
private-namespace cases pass, including embedded-space mountinfo escape
decoding. Namespace exit releases only disposable private mounts; production
code never unmounts a path.

## Ordinary and local positive controls

Ordinary removal below the host's normal `/tmp` mount ancestry remains usable:
single, empty-output, multi-file, and composed synthetic overlays remove
completely, and every retained refusal snapshot stays unchanged. Before
documentation, the focused manifest/LEVEL suite passed 101/101 and the
complete canonical suite passed 289/289.

The exact ignored local source hashes remained:

- `CD/LEVEL07/LEVEL1.DAT`:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`;
- `CD/CHARS/FLICK.ALL`:
  `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`;
- `CD/CHARS3/FLICKD.ALL`:
  `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.

All three tracked families completed apply/remove twice in disposable ordinary
directories. Each pair produced identical receipt/output hashes, removed its
overlay root, and left the three source hashes unchanged:

| Family | Cycles | Receipt SHA-256 | Output SHA-256 values |
|---|---:|---|---|
| exact opaque replacement | 2/2 | `ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63` | `6e5afb4f...079a4` |
| tracked same-DAT composition | 2/2 | `b899907eec17020f9e7a303b9cd8b5620dc70e83051840d13d57df80b6c779ef` | `78cca99b...1d9a` |
| tracked M1-plus-opaque composition | 2/2 | `f8e144521905cc978e560e01158fae983495693f556f069773c8fac136c815b5` | `6e5afb4f...079a4`, `b8012a95...f720e` |

## Validation and limitations

Final `make check` passed dependency smoke checks, Vault lint over 237 notes
with 0 errors/warnings, all 289 canonical tests in 6.70 seconds, and tracked-
file audit with 0 violations. The focused suite remains 101/101. Both diff
checks and a 19-path MIME audit pass; the worker scope contains only Python,
Markdown, and README text, no path below `originals/`, `media/`, or `work/`,
and no game byte or temporary mount/output artifact. The intentional worker
commit leaves Git clean.

**Confirmed:** the exact M4.12 proper-parent alias now refuses before overlay
content traversal or unlink with all three snapshots unchanged. Exact M4.11
root/descendant mountpoints still refuse, normal host filesystem-mount ancestry
still permits ordinary complete cleanup, and all retained M4/local behavior is
green.

**Inferred pending M4.14:** the mount-ID/device/root/path relation is sufficient
for this exact traversed-ancestry correction. Fresh-context review must try to
falsify both alias classification and the ordinary-filesystem positive boundary.

**Unknown/out of scope:** concurrent mount or I/O changes after preflight,
unreadable/non-Linux mount topology beyond fail-closed refusal, unmounting,
staged-tree or source deletion/restoration, backup/trash/package management,
rollback/general transactions, receipt/schema migration, broad dry-run,
launch, compatibility, N-way composition, `.ALL`, runtime behavior, M2, and
PS1 remain outside this result.

## Disposition and exact next packet

M4.13 is worker-complete, not independently accepted. M4 remains active on
exact fresh-context M4.14 only; M2 remains deferred.

**Name:** Independent M4.13 traversed-ancestry hard-truth audit.

**Bounded question:** Does immutable M4.13 reject the exact proper-parent
mount alias before overlay traversal/unlink without misclassifying ordinary
filesystem ancestry, while preserving every exact-path, parser/failure,
ordinary removal, accepted M4, local, and asset-free baseline?

**First pass:** James must reread the complete startup sequence, inspect the
immutable clean worker commit, independently reproduce the proper-parent alias
with exact snapshots, and adversarially audit mount ID/device/root/path
classification for ordinary root/filesystem mounts, subdirectory and whole-
root aliases, embedded escapes, stacked/nested records, and fail-closed parser
behavior. Re-run all five private-namespace cases, ordinary success/refusal,
accepted composition/topology/schema/receipt matrices, all three local recipes
twice, canonical tests, Vault/tracked-file/diff/no-game-bytes gates.

**Stop rule:** do not change implementation, unmount user paths, introduce a
general mount-ownership/portability policy, change schema/receipt/operations or
deletion targets, add staged/source deletion, restoration, backup/trash/
package, rollback/transactions, or broaden dry-run, launch, compatibility,
N-way, `.ALL`, runtime, M2, or PS1. Reject only with one exact bounded
correction.

**Done condition:** return `ACCEPT` only if every M4.13 claim survives, then
name exactly one successor from a still-unmet written M4 exit gate. Otherwise
return `REJECT` with one actionable correction. Record evidence, limitations,
required Vault updates, intentional documentation-only commit, and a clean Git
tree. Any next worker repeats the startup refresh.

## Subsequent independent disposition

[[EXP-20260814-073 - Independent M4.13 traversed-ancestry hard-truth audit]]
preserves the exact uncovered proper-parent refusal and every retained
baseline, but returns M4.14 `REJECT`. A lower bind alias covered at the same
proper-parent pathname by a distinct ordinary top filesystem remains in the
pathname alias set, causing false refusal of the visible ordinary overlay.
Exact corrective M4.15 is active only on excluding covered lower records.
