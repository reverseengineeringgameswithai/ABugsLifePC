---
type: experiment
id: EXP-20260814-076
date: 2026-08-14
question: Can explicit Linux later-mount order refuse an uncovered ancestry alias after legacy mount-ID reuse without weakening covered-stack and ordinary removal behavior?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; Linux 7.0.11; offline synthetic filesystem QA in disposable private user and mount namespaces plus user-owned local corpus hash/application checks
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.17 corrective worker packet only; removal-only ancestry ordering; no executable, original, asset, runtime, M2, PS1, schema, receipt, operation, deletion-target, staged/source deletion, or transaction change
artifacts:
  - reimplementation/ablpc/manifest.py
  - tests/test_manifest.py
  - tests/mount_overlay_case.py
  - mods/training-primary-record-124-target-111e4.json
  - mods/training-primary-record-125-field-0c-zero.json
  - mods/chars-flick-all-from-chars3-flickd-all.json
addresses: []
file_offsets: []
result: worker-complete-mount-generation-order
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
---

# EXP-20260814-076 - Mount generation order for ancestry aliases

## Bounded question

Can exact M4.17 close the one M4.16 bypass: when a newer uncovered bind alias
reuses a freed legacy mount ID numerically below its still-mounted source, can
removal use an explicit non-reused Linux mount ordering to refuse before
overlay traversal or unlink with source, independent target, alias view, and
overlay snapshots exact, while retaining M4.15 covered-record filtering and
every accepted removal, composition, M1, and asset-free boundary?

The executable hash scopes the project, but `bugs.exe` was neither inspected
nor run. No original, game asset, external PS1 material, runtime state,
manifest schema, receipt, operation, deletion target, or source/staged-tree
behavior changed. The only explicit unmount was the disposable scratch
`tmpfs` inside the private regression namespace; namespace exit released the
remaining mounts.

## Correction and static evidence

**Confirmed at the M4.17 worker boundary:** `/proc/self/mountinfo` legacy IDs
are still retained for parent-stack and device/root/path classification, but
they are no longer treated as creation age. The local Linux UAPI at
`/usr/include/linux/mount.h` defines `LISTMOUNT_REVERSE` as “List later mounts
first”, exposes unique mount IDs through `listmount(2)`, and maps each unique
ID back to `mnt_id_old`, `mnt_parent_id_old`, and device identity through
`statmount(2)`. The local manual also records that glibc supplies no wrappers,
so the bounded Linux implementation calls syscalls 457/458 through `ctypes`.

`_linux_mount_entries` now enumerates the complete later-first unique-ID list,
assigns an explicit increasing `mount_order`, and maps every entry back to its
legacy ID. It bounds every returned batch and stat buffer, rejects empty,
duplicate, non-progressing, or invalid order, requires both requested
`STATMOUNT_SB_BASIC` and `STATMOUNT_MNT_BASIC` results, and verifies unique ID,
old ID, old parent ID, and major/minor device identity. It then requires the
legacy-ID set and metadata to equal mountinfo and rereads mountinfo byte-for-
byte before accepting the snapshot. Missing syscall support, permission/read
errors, malformed results, or a table change fail closed before traversal.
`_mount_alias_points` retains M4.15 same-path parent-stack filtering, but its
earlier/later comparison now uses only `mount_order`.

This is one current-Linux removal classifier correction, not general mount
ownership or cross-platform policy. It changes no deletion target or order.

## Private-namespace and pure evidence

The new `reuse` case creates a scratch `tmpfs`, records its lower legacy mount
ID, mounts an independent source `tmpfs` next, and creates an authenticated
sparse overlay below that source. It unmounts only the scratch mount, then
bind-mounts the still-mounted source at a distinct alias parent. The case
requires the alias to reuse the scratch ID, requires that reused alias ID to be
numerically below the source ID, and independently requires the kernel-derived
alias order to be later than the source order.

Removal through the alias refuses with `overlay root ancestry contains a mount
alias`. Complete recursive no-follow snapshots of the work-copy source,
independent mounted target, alias view, and overlay are byte/type/link/metadata
identical before and after. Pure tests repeat the inverted legacy-ID pair in
both tuple orders, proving classification depends on the explicit order rather
than input tuple or old numeric ID.

The targeted mount family passes 10/10: three pure classifier expansions, six
private-namespace refusal cases (normal uncovered ancestor, exact root,
intermediate, output, receipt, and reused-lower-ID ancestor), and the M4.15
covered lower bind plus ordinary top filesystem success. The successful
stacked case still removes its visible overlay completely and preserves its
source and hidden independent target.

## Retained ordinary and local gates

Before documentation, the focused manifest/LEVEL suite passed 105/105 and the
complete canonical `python -m pytest -q tests` suite passed 293/293.

All three tracked user-owned local families applied and removed twice in
disposable ordinary directories. Every overlay disappeared, both cycles
produced equal receipt/output hashes, and the exact source hashes remained
unchanged:

| Family | Cycles | Receipt SHA-256 | Output SHA-256 values |
|---|---:|---|---|
| exact opaque replacement | 2/2 | `ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63` | `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4` |
| tracked same-DAT composition | 2/2 | `b899907eec17020f9e7a303b9cd8b5620dc70e83051840d13d57df80b6c779ef` | `78cca99b1993cc6deff8f89104d6f6aa8154ed7063e4ab0b56195e4321761d9a` |
| tracked M1-plus-opaque composition | 2/2 | `f8e144521905cc978e560e01158fae983495693f556f069773c8fac136c815b5` | `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`, `b8012a95f7ec0254805bdd3cf32df2b16f2ad0926308fe8678cc2360027f720e` |

The unchanged source SHA-256 values are
`494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`
for Training `LEVEL1.DAT`,
`a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`
for `FLICK.ALL`, and
`6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`
for `FLICKD.ALL`.

An initial local harness accidentally selected the accepted record-125 field
manifest rather than the established record-124 target manifest for the mixed
family. Its expected receipt assertion stopped in a disposable directory after
the opaque and same-DAT families had passed; the context cleanup removed all
outputs and application had only read the source. A corrected fresh mixed
run then passed 2/2 with the established receipt/output hashes above, and all
three source hashes were reconfirmed unchanged. The mistaken selection is not
counted as mixed-family evidence.

## Validation and limits

The correction changes only Linux ancestry-alias ordering and asset-free
tests. It does not change exact-plan mountpoint refusal, receipt/output/tree
authentication, deletion order/targets, source preservation, composition, or
M1 byte behavior. Final `make check` passes dependency smoke checks, Vault
lint over 245 notes with 0 errors/warnings, all 293 canonical tests, tracked-
file audit with 0 violations, and both diff checks. The worker scope contains
only three Python implementation/test paths plus Markdown/README text, changes
no path below `originals/`, `media/`, `work/`, or `mods/`, and passes MIME/no-
game-bytes review.

Non-Linux portability and kernels lacking these current Linux interfaces
retain fail-closed behavior and are not a compatibility claim. Concurrent
mount or I/O changes after preflight, staged-tree or source deletion/
restoration, backup/trash/package management, rollback/general transactions,
receipt/schema migration, broad dry-run, launch, compatibility, N-way
composition, `.ALL`, runtime behavior, M2, and PS1 remain unknown or out of
scope.

## Disposition and exact next packet

M4.17 is worker-complete, not independently accepted. Exact M4.18 is the sole
next packet; M2 remains deferred.

**Name:** Independent M4.17 mount-generation-order hard-truth audit.

**Bounded question:** Does immutable M4.17 use an exact fail-closed Linux
later-mount order to reject the reused-lower-ID uncovered alias before
traversal/unlink with all four snapshots exact, while preserving covered-stack
visibility, every ordinary/refusal boundary, and all accepted M4/M1/local
behavior?

**First pass:** James must start in fresh context, reread [[START HERE]] and the
complete required Obsidian startup sequence, inspect only the immutable clean
worker commit, and independently recreate the legacy-ID reuse case with
complete no-follow snapshots. Independently audit `listmount` later-first
pagination and `statmount` unique-to-old-ID mapping, including syscall/read
failure, empty/duplicate/out-of-order/non-progressing results, malformed masks
or IDs, set/parent/device mismatch, and mountinfo change during preflight.
Re-run tuple permutations, two-/multi-level covered stacks, hidden candidate/
source, visible top alias, normal uncovered aliases, ordinary mounts, every
namespace/parser/removal/accepted M4/M1/local/canonical/hygiene gate, and the
asset-free boundary.

**Stop rule:** do not change implementation or tests, unmount user paths,
introduce general mount ownership/portability, change schema/receipt/
operations/deletion targets or order, add staged/source deletion/restoration,
backup/trash/package, rollback/transactions, or broaden dry-run, launch,
compatibility, N-way composition, `.ALL`, runtime, M2, PS1, or M4.3. Return
`REJECT` only with one exact bounded correction.

**Done condition:** return `ACCEPT` only if every M4.17 condition survives,
then name exactly one successor from a still-unmet written M4 exit gate.
Otherwise return `REJECT` with one actionable correction. Record the verdict,
evidence, limitations, required Vault updates, intentional documentation-only
commit, and clean Git tree. Any next worker repeats the startup refresh.

## Subsequent M4.18 disposition

[[EXP-20260814-077 - Independent M4.17 mount-order hard-truth audit]] returns
`ACCEPT` against immutable commit
`67ea1618a7d3ad741c81d3eaaa1d32d99874631b`. Independent current-x86_64 UAPI
and kernel-source review confirms the request/result ABI and reverse
pagination. Adversarial syscall, sequence, stat-result, old-ID mapping,
parent/device, mountinfo-change, and parser cases all fail closed. A separately
authored private namespace reproduces scratch/source/later-alias old IDs
1081/1082/1081, places the later alias first in independent reverse
enumeration, refuses before overlay traversal, and preserves all four complete
snapshots. Covered-stack behavior and every tracked namespace, ordinary,
composition, topology/schema/receipt, M1, local, canonical, Vault, tracked-
file, MIME, and no-game-bytes gate survive. Exact M4.19, the versioned exact
compatibility statement derived from the still-unmet written M4 exit gate, is
now the sole active packet.
