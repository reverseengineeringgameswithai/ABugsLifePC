---
type: experiment
id: EXP-20260814-075
date: 2026-08-14
question: Does M4.15 retain every uncovered ancestry alias when Linux reuses a numerically lower mount ID for a newer bind mount?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline synthetic filesystem QA in disposable private user and mount namespaces plus user-owned local corpus hash/application checks
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.16 independent audit of immutable commit d9b2fcd1b32a4ae543603b0c30ff1201a532af07; documentation-only verdict; no executable, original, asset, runtime, M2, PS1, schema, receipt, operation, implementation, or test change
artifacts:
  - reimplementation/ablpc/manifest.py
  - tests/test_manifest.py
  - tests/mount_overlay_case.py
  - mods/training-primary-record-124-target-111e4.json
  - mods/training-primary-record-125-field-0c-zero.json
  - mods/chars-flick-all-from-chars3-flickd-all.json
addresses: []
file_offsets: []
result: rejected-mount-id-reuse-bypasses-uncovered-alias-refusal
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
  - audit/hard-truth
---

# EXP-20260814-075 - Independent M4.15 covered-stack hard-truth audit

## Verdict and bounded question

M4.16 returns **REJECT** against immutable clean worker commit
`d9b2fcd1b32a4ae543603b0c30ff1201a532af07`.

M4.15 correctly excludes covered lower records from both sides of ancestry
alias comparison. Its exact lower-bind/ordinary-top case, two- and three-level
same-path stacks, hidden candidate and source records, visible top alias,
exact-path refusals, parser/failure cases, ordinary removal, accepted M4, local,
and asset-free baselines survive. One uncovered alias nevertheless escapes
classification when Linux reuses a freed numerically lower mount ID for a
newer bind mount. Removal then succeeds through that alias and mutates the
independent mounted target. This falsifies the required “every uncovered
alias” and mount-ID-order conditions.

The executable hash scopes the project, but `bugs.exe` was neither inspected
nor run. No original, game asset, external PS1 source, or implementation/test/
asset file was modified. Every mount and the one deliberate unmount were
confined to disposable paths inside a private user/mount namespace; namespace
exit released the remaining mounts.

## Surviving exact evidence

An independently authored lower-bind/ordinary-top case captured complete
recursive no-follow snapshots of source, hidden target, visible top parent,
and overlay: relative paths, type/mode, uid/gid, link count, device, inode,
size, exact regular-file bytes and SHA-256, and symlink targets. Removal
succeeded, the overlay disappeared, the visible parent returned to its empty
pre-overlay snapshot, and source plus hidden target stayed exact. The same
properties survived a three-level same-path stack. A visible top alias over a
lower ordinary mount refused unchanged.

Pure tuple-order matrices passed for all permutations of hidden candidates,
hidden sources, visible top aliases, and three-level stacks. Ordinary root,
filesystem, subvolume, same-path, and different-device controls stayed clean;
uncovered subdirectory, whole-root, and nested aliases classified. The parser
decoded all four supported escapes (`\\011`, `\\012`, `\\040`, `\\134`) and
failed closed on 15 read, empty, separator, field-count, ID, duplicate-ID,
relative-path, escape, root, and device failures.

All six tracked private-namespace cases passed in isolation: proper ancestor,
exact root, intermediate directory, output, receipt, and stacked ordinary top.
Ordinary removal, composition, and topology/schema/receipt selectors passed
32/32, 17/17, and 33/33. The focused manifest/LEVEL suite passed 102/102; the
complete canonical `python -m pytest -q tests` suite passed 290/290. One
focused run launched concurrently with the canonical suite reproduced an
unexpected ancestor-case success; its isolated rerun passed. This is
corroborating mount-ID-allocation evidence, not the verdict's sole basis.

All three tracked local families applied and removed twice in disposable
ordinary directories. Every overlay disappeared, both cycles produced exact
receipt/output hashes, and the sources retained these SHA-256 values:
`494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`
for Training `LEVEL1.DAT`,
`a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`
for `FLICK.ALL`, and
`6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`
for `FLICKD.ALL`.

| Family | Cycles | Receipt SHA-256 | Output SHA-256 values |
|---|---:|---|---|
| exact opaque replacement | 2/2 | `ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63` | `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4` |
| tracked same-DAT composition | 2/2 | `b899907eec17020f9e7a303b9cd8b5620dc70e83051840d13d57df80b6c779ef` | `78cca99b1993cc6deff8f89104d6f6aa8154ed7063e4ab0b56195e4321761d9a` |
| tracked M1-plus-opaque composition | 2/2 | `f8e144521905cc978e560e01158fae983495693f556f069773c8fac136c815b5` | `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`, `b8012a95f7ec0254805bdd3cf32df2b16f2ad0926308fe8678cc2360027f720e` |

## One concrete falsification

Inside one disposable private namespace, the QA case mounted a scratch `tmpfs`
and observed mount ID 1081, then mounted an independent source `tmpfs` and
observed mount ID 1082. It built an exact authenticated sparse overlay below
that source. It unmounted only the disposable scratch mount, then bind-mounted
the still-mounted independent source at a different proper-parent alias path.
Linux reused freed mount ID 1081 for this newly created uncovered alias:

- alias candidate: mount ID 1081, parent ID 1076, device `0:74`, root `/`;
- visible source: mount ID 1082, parent ID 1076, device `0:74`, root `/`.

The alias was newer in creation order but numerically smaller. Static evidence
at `_mount_alias_points` is the condition
`source.mount_id >= candidate.mount_id: continue`, which treats numeric mount
ID order as an age order. It therefore skipped the source/candidate pair and
omitted the uncovered alias. `remove_manifest` returned success and removed
the authenticated overlay through the alias. The complete source work-copy
snapshot stayed exact, but complete independent-target, alias-view, and
overlay snapshots changed. This is one stable preflight-classification defect,
not a concurrent mutation, general ownership objection, or portability claim.

## Exact corrective packet M4.17

**Name:** Refuse uncovered ancestry aliases despite mount-ID reuse.

**Bounded question:** Can `remove_manifest` refuse an uncovered proper-parent
alias when a newly created bind reuses a numerically smaller freed mount ID
than the still-mounted visible same-device source, before traversal/unlink with
complete snapshots unchanged, while retaining M4.15 covered-lower filtering
and every accepted baseline?

**Exact locators:** `_MountEntry.mount_id`, `_MountEntry.parent_id`,
`_MountEntry.major`, `_MountEntry.minor`, `_MountEntry.root`,
`_MountEntry.mount_point`, `_linux_mount_entries`, `_mount_alias_points`, and
`_validate_unmounted_deletion_plan` in `reimplementation/ablpc/manifest.py`;
the six namespace cases in `tests/mount_overlay_case.py` and
`tests/test_manifest.py`; the exact ID-reuse reproduction above;
[[EXP-20260814-071 - Independent M4.11 mounted-plan-path hard-truth audit]]
through [[EXP-20260814-074 - Covered lower mount record exclusion]]; and all
accepted M4/M1/local baselines.

**First pass:** add one asset-free private-namespace regression that allocates
a disposable scratch `tmpfs` with the lower mount ID, mounts an independent
source next, builds its authenticated overlay, unmounts only the disposable
scratch inside that private namespace, and bind-mounts the source to an alias.
Require the candidate's reused ID to be numerically lower than the source ID,
capture complete recursive no-follow source/independent-target/alias/overlay
snapshots, and require refusal before traversal/unlink with every snapshot
unchanged. Remove numeric mount-ID-as-age dependence from the exact ancestry
classification or fail closed on the ambiguity, while preserving same-path
parent-stack filtering on both candidate and source. Re-run tuple permutations,
two- and multi-level stacks, hidden candidate/source, visible top alias,
ordinary and uncovered controls, all namespace/parser/removal/accepted/local/
canonical/hygiene gates. If current mountinfo cannot discriminate safely
without falsely refusing required ordinary positive controls, stop with that
exact blocker; do not broaden general mount policy.

**Stop rule:** do not change schema, receipt, operation, deletion target, or
deletion order; do not unmount any user path outside disposable private
namespaces; do not add general mount ownership/portability, staged/source
deletion/restoration, backup/trash/package, rollback/transactions, broad dry-
run/launch/compatibility, N-way composition, `.ALL`, runtime, M2, PS1, or M4.3.
Change only the bounded ancestry classifier, its asset-free regression, and
required documentation.

**Done condition:** the reused-lower-ID uncovered alias refuses before
traversal/unlink with exact source/independent-target/alias/overlay snapshots
unchanged; the stacked ordinary-top overlay still removes completely with
source and hidden target exact; normal-ID uncovered ancestor, visible top
alias, and four exact root/descendant mounts refuse unchanged; every pure,
parser, ordinary, accepted M4, local, canonical, Vault, tracked-file, diff,
MIME/no-game-bytes, and clean-tree gate passes; and an intentional clean worker
commit is ready for fresh-context verification.

## Limits

Concurrent mount or I/O changes after preflight, non-Linux portability beyond
existing fail-closed behavior, unmounting outside the exact disposable
regression, staged-tree or source deletion/restoration, backup/trash/package
management, rollback/general transactions, receipt/schema migration, broad
dry-run, launch, compatibility, N-way composition, `.ALL`, runtime behavior,
M2, and PS1 remain unknown or out of scope. Exactly corrective M4.17 is active;
no later successor is selected.

## Subsequent worker disposition

[[EXP-20260814-076 - Mount generation order for ancestry aliases]] completes
exact corrective M4.17 at the worker boundary. Current Linux later-first unique
mount enumeration plus statmount old-ID/parent/device mapping replaces the
reusable numeric-ID age comparison and fails closed on inconsistent snapshots.
The exact reused-lower-ID alias now refuses before traversal/unlink with all
four snapshots exact, while M4.15 covered-stack behavior and every retained
baseline survive. Exact fresh-context M4.18 is the sole next packet.
