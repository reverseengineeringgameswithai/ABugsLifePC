---
type: experiment
id: EXP-20260814-077
date: 2026-08-14
question: Does immutable commit 67ea161 satisfy every exact M4.17 current-Linux mount-generation-order, fail-closed, covered-stack, retained-baseline, and asset-free condition?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; Linux 7.0.11 x86_64; independent static audit, synthetic syscall and mount-table fault injection, disposable private user/mount namespaces, scoped tests, and user-owned local corpus hash/application checks
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact fresh-context M4.18 audit of immutable commit 67ea1618a7d3ad741c81d3eaaa1d32d99874631b only; documentation-only verdict; no implementation, test, schema, receipt, operation, deletion-target/order, original, asset, runtime, M2, PS1, portability, transaction, dry-run, launch, or compatibility change
artifacts:
  - reimplementation/ablpc/manifest.py
  - tests/mount_overlay_case.py
  - tests/test_manifest.py
  - tests/test_level_dat.py
  - mods/chars-flick-all-from-chars3-flickd-all.json
  - mods/training-primary-record-124-target-111e4.json
  - mods/training-primary-record-125-field-0c-zero.json
  - /usr/include/linux/mount.h
  - /usr/include/asm/unistd_64.h
addresses: []
file_offsets:
  - statmount.size +0x00
  - statmount.mask +0x08
  - statmount.sb_dev_major/minor +0x10/+0x14
  - statmount.mnt_id +0x28
  - statmount.mnt_id_old/mnt_parent_id_old +0x38/+0x3C
result: accept-current-linux-mount-generation-order
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
  - audit/hard-truth
---

# EXP-20260814-077 - Independent M4.17 mount-order hard-truth audit

## Verdict

**ACCEPT.** Immutable worker commit
`67ea1618a7d3ad741c81d3eaaa1d32d99874631b` satisfies every exact M4.17 done
condition. Independent static review, injected syscall/table failures, and a
separately authored private-namespace reproduction found no surviving reused-
ID bypass, sequence/mapping acceptance, mountinfo inconsistency, covered-stack
regression, ordinary-removal regression, local-recipe drift, source mutation,
or tracked game-byte payload.

The accepted result is deliberately narrow. On this current x86_64 Linux host,
removal uses kernel `LISTMOUNT_REVERSE` unique-ID order and `statmount` legacy-
ID/parent/device data to authenticate the mountinfo snapshot before traversing
the overlay. Legacy IDs remain identity and parent-stack joins, not age. This
does not establish other architectures, older kernels, general mount
ownership, or broad portability.

## Audit boundary and immutable inputs

The audit confirmed exact `HEAD`
`67ea1618a7d3ad741c81d3eaaa1d32d99874631b`, exact parent
`1b28f60cfc6d8c4354bee0625cf478cfcd2c2564`, and a clean tree before review.
Before substantive work, James reread `AGENTS.md`, full [[START HERE]], full
[[Current State]], full [[Project Roadmap]], full [[Environment Status]], full
[[Decision Log]], full [[Known Unknowns]], the relevant implementation,
experiment, and reverse-engineering MOCs, [[Agent Operating Manual]], and
[[Project Charter]]. The complete M4.18 packet,
[[EXP-20260814-075 - Independent M4.15 covered-stack hard-truth audit]],
[[EXP-20260814-076 - Mount generation order for ancestry aliases]],
[[M4 Exact Whole-file Replacement]], [[M1 Tool Support Matrix]], the M4.17
worker session, both READMEs, the exact worker diff, and every changed
implementation/test file were also read in full.

Review covered `_MountEntry`, the 24-byte `_MountIdRequest`, syscall/flag/
buffer constants, `_linux_mount_entries`, `_linux_mount_order_by_old_id`,
`_linux_unique_mount_ids_later_first`, `_linux_statmount_basic`,
`_mount_alias_points`, `_validate_unmounted_deletion_plan`, the removal call
order, and every new worker test. No implementation, test, manifest, original,
work-copy source, external repository, or game asset was changed. The external
PS1 tree was not consulted, and `bugs.exe` was not run or inspected.

## Current x86_64 Linux ABI and ordering evidence

The host reported Linux `7.0.11-200.fc44.x86_64`; `long` and pointers are
64-bit. `/usr/include/asm/unistd_64.h` assigns `statmount` and `listmount`
syscalls 457 and 458. `/usr/include/linux/mount.h` defines the accepted request
v0 size as 24 bytes even though the current v1 structure appends `mnt_ns_id` at
32 bytes. The worker's request field offsets are exactly `0/4/8/16`, its root
selector is `LSMT_ROOT`, its reverse flag is 1, and its requested stat mask is
`STATMOUNT_SB_BASIC | STATMOUNT_MNT_BASIC == 3`.

The same header places the parsed fixed results at the offsets listed in this
note and defines `LISTMOUNT_REVERSE` as later mounts first. Independent review
of Linux v7.0 `fs/namespace.c:5984-6045` confirms that a zero cursor begins at
the namespace's last mount node, reverse continuation resumes below
`last_mnt_id`, and iteration follows the reverse order. Lines 6082-6128 bound
the syscall, reject unsupported flags, hold the namespace topology read lock
for one call, and return the number copied. This independently supports the
worker's strict descending checks and `parameter = current[-1]` pagination.
The host's real table returned 33 unique IDs in strict reverse order and 33
entries with unique orders `1..33`.

`statmount` independently joins each non-reused unique ID to the legacy old
ID, legacy parent ID, and device pair. The worker accepts only a result large
enough for fields through `+0x3C`, no larger than its 512-byte buffer, carrying
both requested mask groups, returning the exact requested unique ID, and
containing a positive old ID. It then requires a one-to-one old-ID map, exact
old-ID set equality, parent/device equality, and a byte-exact second
`/proc/self/mountinfo` read. Static request layout, constants, bounds, and
unpack offsets all match the current UAPI.

## Independent fail-closed fault injection

A separately authored disposable Python harness outside the repository
intercepted only the syscall and mountinfo boundaries. Valid single-page,
forced cross-page, and empty list results were checked first. Eight listmount
attacks then failed closed: syscall error, count above 256, zero ID, duplicate
within a page, ascending order, cross-page duplicate, cross-page order
reversal, and a repeated/non-progressing cursor value. The forced valid case
filled one 256-ID page and verified that the next request used the last ID.

One valid stat result established every request field and returned tuple.
Six attacks failed closed: syscall error, 63-byte short result, 513-byte
oversize result, either requested mask group missing, mismatched returned
unique ID, and zero old ID. Empty enumeration and duplicate old-ID mapping
also failed closed.

Mountinfo cross-checking accepted one exact table, then rejected eight
independent conditions: initial read error, second read error, a one-byte table
change, missing mapping, extra mapping, parent mismatch, major-device mismatch,
and minor-device mismatch. The retained parser decoded all four supported
escapes (`\\011`, `\\012`, `\\040`, and `\\134`) and rejected 16 empty,
separator/field-count, non-decimal/zero/duplicate-ID, device, relative-path,
invalid/truncated-escape, and rootless cases. Every failure occurred before an
overlay traversal or unlink.

## Independent legacy-ID reuse reproduction

A second independently authored helper, not the tracked worker helper, ran in
one disposable `unshare --user --map-root-user --mount --fork` process. It
mounted a scratch `tmpfs`, mounted the independent source next, created the
authenticated sparse overlay there, unmounted only the scratch, then made a
later bind alias to the still-mounted source. Namespace exit released all
surviving mounts; no user path was unmounted.

The scratch held old ID 1081, the independent source held old ID 1082, and the
later alias reused old ID 1081. An independent raw `listmount` implementation
used batch size 2 to force 18 pages over 35 mounts. Independent `statmount`
mapping agreed exactly with the current mountinfo old-ID set, parent IDs, and
devices. Reverse position 0 was the alias and position 1 the source, proving
that explicit generation order retained the later candidate despite
`1081 < 1082`.

Complete recursive no-follow snapshots recorded relative path, type, mode,
UID, GID, link count, device, inode, size, complete regular-file bytes and
SHA-256, and symlink targets for the source, independent target, alias view,
and overlay. A guard replacing `_validate_exact_overlay_tree` would have
failed if overlay traversal began. `remove_manifest` instead raised the exact
ancestry-alias refusal; the guard was never reached, and all four post-call
snapshots were identical to their pre-call values.

## Covered-stack, alias, removal, and schema results

The pure classifier passed all 120 input-tuple permutations of a five-record
alias/control set. Thirteen additional cases covered two- and three-level
same-path stacks, hidden candidate, hidden source, visible top alias, ordinary
root/filesystem/subvolume/same-path/different-device records, and uncovered
subdirectory, whole-root, and nested aliases. Zero and duplicate order values
failed closed. Thus M4.15's covered-lower filtering applies to both comparison
sides, while a currently visible top alias remains classified.

All seven tracked private-namespace cases passed independently: proper
ancestor, exact root, intermediate directory, output, receipt, reused lower
ID, and the accepted stacked ordinary top. The first six refused unchanged;
the stacked visible overlay removed completely with its source and hidden
target exact.

The ordinary non-mounted removal selector passed 32/32, composition passed
17/17, and the broad topology/schema/receipt/symlink/blocker/force selector
passed 37/37. Explicit position, field-`0x0C`, and payload-target applications
under schema 1 and schema 2 passed 6/6, with cross-schema output bytes equal
3/3; each overlay also removed and each source remained exact. The focused
manifest/LEVEL suite passed 105/105, and the complete canonical
`python -m pytest -q tests` suite passed 293/293 in 6.75 seconds. No unscoped
pytest command was used.

## Tracked local and asset-free results

All three tracked user-owned local families applied and removed twice in
disposable ordinary directories. Each overlay disappeared, both cycles were
identical, and the exact source hashes remained:

- Training DAT:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`;
- opaque destination:
  `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`;
- opaque replacement source:
  `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.

| Family | Cycles | Receipt SHA-256 | Output SHA-256 |
|---|---:|---|---|
| exact opaque replacement | 2/2 | `ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63` | `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4` |
| tracked same-DAT composition | 2/2 | `b899907eec17020f9e7a303b9cd8b5620dc70e83051840d13d57df80b6c779ef` | `78cca99b1993cc6deff8f89104d6f6aa8154ed7063e4ab0b56195e4321761d9a` |
| tracked M1-plus-opaque composition | 2/2 | `f8e144521905cc978e560e01158fae983495693f556f069773c8fac136c815b5` | `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`, `b8012a95f7ec0254805bdd3cf32df2b16f2ad0926308fe8678cc2360027f720e` |

Before verdict documentation, Vault lint reported 245 notes with zero errors
or warnings and tracked-file audit reported zero violations. The 18-path
worker diff contains only Markdown/README text and three Python source/test
paths; MIME inspection found only text. Git tracks only `.gitkeep` under
protected source/media roots and no executable, DAT, `.ALL`, `.ANM`, disc
image, dump, VM image, capture, or other game-byte payload. Temporary audit
scripts and outputs lived under one explicit `/tmp/ablpc-m418-james-qa-*`
directory outside the repository and were removed after use.

After all required verdict surfaces were updated, the complete canonical suite
passed 293/293, Vault lint reported 247 notes with zero errors
or warnings, tracked-file audit reported zero violations, and staged/unstaged
diff checks passed. Final MIME/protected-path/no-game-bytes review found only
documentation/README text in the verdict scope.

## Limitations

- Acceptance is exact to current x86_64 Linux with the verified
  `listmount(2)`/`statmount(2)` ABI and readable trustworthy mountinfo. An
  unavailable syscall or any incomplete/inconsistent result fails closed.
- The result is an ancestry-alias classifier, not a general definition of
  mount ownership, user intent, filesystem trust, or cross-platform support.
- Concurrent topology changes are detected only across the bounded preflight
  snapshot. Unpredictable permission, storage, or I/O failures and changes
  after preflight remain non-transactional.
- Staged-tree/source removal or restoration, backup/trash/package management,
  generalized transactions, broad dry-run, launch, compatibility, N-way
  composition, `.ALL` parsing, runtime, M2, PS1, and M4.3 remain outside this
  acceptance.

## Exact next packet: M4.19

**Name:** Versioned exact compatibility statement.

**Unmet exit gate:** “A versioned compatibility statement names supported
hashes and Wine scope.”

**Bounded question:** Can the repository publish one versioned, asset-free M4
v0.1 compatibility statement that names the exact supported executable and
input hashes, existing schema/operation boundaries, current x86_64 Linux
removal prerequisites, and tested Wine/Gamescope scope, while distinguishing
demonstrated behavior from fail-closed or unsupported configurations?

**Exact locators and inputs:** the M4 exit gate in [[Project Roadmap]];
[[M1 Tool Support Matrix]]; [[M4 Exact Whole-file Replacement]];
[[Wine Linux Play Baseline]]; [[Environment Status]]; the executable, Training
DAT, Level 01 DAT, `FLICK.ALL`, and `FLICKD.ALL` hashes already recorded in
accepted experiments; `scripts/play-pristine.sh`; the schema validator and
three tracked manifests; and the current-Linux removal boundary accepted here.

**First pass:** define one explicit M4 v0.1 statement version and a
machine-checkable metadata representation containing only identifiers,
versions, paths, hashes, capabilities, and limitations. Cross-check every
listed hash against the tracked manifests or existing evidence, name the
tested Python/Linux/Wine/Gamescope scope without inferring other platforms,
separate portable apply/stage behavior from current-Linux-only removal, and
make documentation and CLI-facing guidance agree. Add asset-free consistency
tests for the metadata/version/hash/capability declarations.

**Stop rule:** do not run or modify the game, claim untested Windows/Wine/
kernel/filesystem compatibility, change manifest schema/receipt/operations,
alter apply/stage/remove behavior, add launch orchestration or broad dry-run,
package game bytes, parse `.ALL`, add N-way composition, reopen M2, consult
PS1, or introduce general mount/transaction policy. Stop with one exact
contradiction if existing accepted evidence cannot support a listed field.

**Done when:** one versioned asset-free statement names every exact supported
hash and tested Wine/current-Linux scope, all fields trace to accepted evidence
or tracked metadata, automated checks reject drift or unsupported values,
docs clearly preserve every limitation above, canonical/Vault/tracked/MIME/
no-game-bytes gates pass, and an intentional clean worker commit is ready for
fresh-context independent review.

## Subsequent disposition

[[EXP-20260814-078 - Versioned exact M4 compatibility statement]] completes
the exact M4.19 worker packet with canonical strict JSON, five demonstrated
hash anchors, existing schema/operation/workflow limits, current-Linux removal
prerequisites, tested Wine/Gamescope scope, 18 drift tests, and 311 canonical
tests. It changes no game-facing behavior and activates only fresh-context
M4.20 independent audit.
