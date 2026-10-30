---
type: experiment
id: EXP-20260814-070
date: 2026-08-14
question: Can removal reject every supported pre-existing mountpoint in an exact sparse-overlay deletion plan before mutation while retaining ordinary removal behavior?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline synthetic filesystem QA in private user and mount namespaces plus user-owned local corpus hash/application checks
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.11 corrective worker packet only; Linux /proc/self/mountinfo topology guard; no user-path unmount, schema/receipt/operation change, staged/source deletion, rollback/transaction, runtime, M2, or PS1 work
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
result: worker-complete-mounted-deletion-plan-path-refusal
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
---

# EXP-20260814-070 - Mounted sparse-overlay deletion-plan path refusal

## Bounded question

Can exact M4.11 correct the stable bind-mount falsification from
[[EXP-20260814-069 - Independent M4.9 sparse-overlay removal hard-truth audit]]
without broadening removal: reject a pre-existing mountpoint at the overlay
root, any necessary directory, any recorded output, or the fixed receipt before
the first unlink, while preserving exact overlay, source, and independently
mounted target snapshots and every ordinary M4.9 baseline?

The recorded executable hash scopes the project. This packet reconfirmed that
hash but did not read executable contents, launch the game, modify any game
file, or consult the external PS1 tree. The local recipe checks read only an
ignored user-owned derived work copy and wrote outputs only below disposable
temporary directories.

## Correction

**Confirmed at the worker boundary:** `remove_manifest` now constructs the
complete expected sparse-overlay file and directory set before overlay
traversal. `_validate_unmounted_deletion_plan` compares these exact paths:

- the supplied resolved overlay root;
- every necessary parent directory of a recorded output or receipt;
- every recorded output; and
- fixed `.ablpc/receipt.json`.

The comparison uses mountpoints read as bytes from Linux
`/proc/self/mountinfo`. `_decode_mountinfo_path` decodes the kernel's octal
escapes before filesystem decoding, so embedded spaces, tabs, newlines, and
backslashes are compared as paths rather than mountinfo tokens. Missing,
malformed, non-absolute, or empty mountinfo fails closed with `ManifestError`.
If any planned path is a current mountpoint, removal refuses before its prior
`lstat`/`scandir`, receipt read, output hash read, or unlink phases.

This uses the kernel mount table because file type, link count, and `st_dev`
cannot discriminate a same-filesystem bind mount from the ordinary visible
tree that M4.10 authenticated. It does not unmount anything and does not add a
new deletion target.

## Isolated mount-topology evidence

`tests/mount_overlay_case.py` runs only inside a disposable private user and
mount namespace created by `unshare`. It creates a synthetic schema-2 opaque
manifest and an ordinary exact overlay, then independently places a bind mount
at each supported plan location:

| Case | Mounted plan path | Result |
|---|---|---|
| root | exact overlay root | refused before mutation |
| intermediate | necessary `D` directory above the recorded output | refused before mutation |
| output | exact recorded `D/shared/deep/out.bin` | refused before mutation |
| receipt | exact `.ablpc/receipt.json` | refused before mutation |

All 4/4 cases passed. Before calling removal, each case captured recursive
no-follow snapshots containing every relative path, type, regular-file byte
string, link count, and symlink target where applicable. After refusal, the
complete overlay, source, and independent mount-source snapshots equaled their
pre-call snapshots. The output and receipt cases used regular single-link
files with exact authenticated visible bytes, so their rejection is the mount
topology guard rather than a prior content/type/link mismatch.

The live overlay and independent-target names contain an embedded space. Linux
mountinfo represents that component with `\040`; the four passing cases
therefore also exercise decoded-path matching rather than only space-free
mountpoints. The namespace exits to release its private mounts; production code
never unmounts a user path.

## Retained ordinary and local evidence

Before documentation:

- all 84 `tests/test_manifest.py` cases passed;
- the focused manifest/LEVEL suite passed 99/99;
- the complete canonical `python -m pytest -q tests` suite passed 287/287; and
- `git diff --check` passed.

The exact ignored local source hashes remained:

- `CD/LEVEL07/LEVEL1.DAT`:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`;
- `CD/CHARS/FLICK.ALL`:
  `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`;
- `CD/CHARS3/FLICKD.ALL`:
  `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.

Three tracked manifest families each completed ordinary apply then M4.11
removal twice in disposable roots. All six returned the apply receipt, removed
the complete overlay root, retained deterministic receipt/output hashes, and
left all three source hashes unchanged:

| Case | Cycles | Receipt SHA-256 | Output SHA-256 values |
|---|---:|---|---|
| exact opaque replacement | 2/2 | `ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63` | `6e5afb4f...079a4` |
| tracked same-DAT composition | 2/2 | `b899907eec17020f9e7a303b9cd8b5620dc70e83051840d13d57df80b6c779ef` | `78cca99b...1d9a` |
| tracked M1-plus-opaque composition | 2/2 | `f8e144521905cc978e560e01158fae983495693f556f069773c8fac136c815b5` | `b8012a95...f720e`, `6e5afb4f...079a4` |

An initial local validation harness used an incorrectly transcribed full
same-DAT output digest and stopped after the first opaque cycle. Its temporary
directory was discarded and source hashes remained unchanged. The digest was
then independently printed from a fresh composed apply, corrected to
`78cca99b1993cc6deff8f89104d6f6aa8154ed7063e4ab0b56195e4321761d9a`,
and the complete six-cycle validation above passed. This failed harness is not
counted as evidence.

## Final closure validation

After all documentation updates, `make check` passed Python dependency smoke
checks, Vault lint over 233 notes with 0 errors/warnings, all 287 canonical
tests in 7.13 seconds, the tracked-file audit with 0 violations, and both diff
checks. The focused suite remained 99/99. The complete worker scope contains
16 text Python/Markdown paths only; no changed path is below `originals/`,
`media/`, or `work/`, and no game byte, mount artifact, receipt, local output,
or temporary manifest is tracked.

## Evidence classification and limitations

**Confirmed at this worker boundary:** on the tested Fedora/Linux host, the
kernel mount table identifies same-filesystem bind mounts at every exact path
that `remove_manifest` can unlink or prune. The four supported mounted plan
locations refuse before mutation with complete snapshots unchanged. Ordinary
unmounted removal and accepted composition/schema/local behavior remain green.

**Inferred pending independent M4.12:** the mountinfo-backed exact-plan check is
sufficient to close M4.10's stable pre-existing mounted-path falsification.
Fresh-context review must try to bypass plan coverage and escape decoding and
must verify fail-closed mountinfo error behavior before acceptance.

**Unknown/out of scope:** this correction intentionally depends on readable,
trusted Linux `/proc/self/mountinfo`; it does not establish Windows or other-
platform removal compatibility. A concurrent mount/topology change after the
guard, unpredictable permissions/storage/I/O, or another post-preflight race
remains non-transactional. Mounting or unmounting user paths, staged-tree
removal, source restoration/deletion, trash/backup/package management,
rollback/general transactions, receipt/schema migration, broad dry-run,
launch, compatibility, N-way composition, `.ALL`, runtime behavior, M2, and
PS1 remain outside this result.

## Disposition

M4.11 is worker-complete, not independently accepted. Exact fresh-context
M4.12 is the sole next packet. M4 remains active and M2 remains deferred.

## Exact next packet: M4.12

**Name:** Independent M4.11 mounted-plan-path hard-truth audit.

**Bounded question:** Does the immutable clean M4.11 worker commit reject every
supported pre-existing mountpoint or mount alias in the exact sparse-overlay
deletion plan before the first unlink, preserve exact overlay/source/
independent-target snapshots, fail closed when mount topology cannot be
trusted, and retain every accepted ordinary M4 baseline?

**First pass:** James must start in fresh context, reread [[START HERE]] and the
complete required Obsidian startup sequence, and inspect only the immutable
worker commit. Independently recreate same-filesystem bind mounts at the
overlay root, an intermediate planned directory, a recorded output, and the
receipt inside a private namespace; vary mountpoint path escaping and exact
plan layout; prove refusal before mutation with complete no-follow snapshots.
Audit mountinfo parsing, missing/malformed/empty topology failure, exact planned-
path coverage, ordinary unmounted removal, accepted composition/topology/
schema/receipt matrices, all three local recipes twice, canonical tests, Vault
lint, tracked-file, diff, no-game-bytes, and clean-tree gates.

**Stop rule:** do not change implementation, schema, receipt, operations, or
mount user paths outside private disposable namespaces; do not add unmounting,
staged/source deletion, backup/trash/package, rollback/general transactions,
broad dry-run/launch/compatibility, N-way composition, `.ALL`, runtime, M2,
PS1, or broaden M4.3. Reject only with one exact bounded corrective packet.

**Done condition:** return `ACCEPT` only if every M4.11 condition survives,
then name exactly one successor derived from a still-unmet written M4 exit
gate. Otherwise return `REJECT` with one actionable correction. Record the
verdict, evidence, limitations, required Vault updates, intentional docs-only
commit, and clean Git tree. Any next worker must repeat the startup refresh.

## Subsequent M4.12 disposition

[[EXP-20260814-071 - Independent M4.11 mounted-plan-path hard-truth audit]]
returns `REJECT`. The exact root/intermediate/output/receipt cases, mountinfo
parser/failure boundary, ordinary non-mounted cleanup, accepted M4 matrices,
and all six local cycles survive. The stronger claim does not: a stable mount
alias at a proper parent traversed to reach the overlay root is not one of the
exact root/descendant `planned_paths`, so cleanup can return success after
removing an independent overlay. Exact M4.13 was selected only to include the
relevant traversed proper ancestry while retaining ordinary cleanup usability
and every accepted baseline. `EXP-20260814-072` now completes that worker
correction and activates exact fresh-context M4.14.
