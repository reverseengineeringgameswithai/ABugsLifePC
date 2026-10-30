---
type: experiment
id: EXP-20260814-106
date: 2026-08-14
question: Does exact clean M6 survive independent archive, smoke, installed-wrapper, rollback, path-identity, and failure-boundary attacks?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; exact local derived PC work copy; asset-free tracked release source; fresh disposable build, install, lifecycle, and tar-adversary roots
environment_version: kernel 7.0.11-200.fc44.x86_64; x86_64; Python 3.14.6; Wine 11.0 Staging; Gamescope 3.16.25-1.fc44.x86_64; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact tracked-clean HEAD 61ab0f9400173e6137c93bae4e7ccb8cf00349e4; M6 implementation commits f4e94e482217ff2dd0996334aae91a4fbe2d93b5 and 5daee2bc78f2fb35e06aa3e8b444b5e413f37a4c are ancestors; no tracked audit edits; no game execution
artifacts:
  - work/releases/hardtruth-a.ZWW1Ot/ablpc-toolkit-v1.0.0.tar
  - work/releases/hardtruth-b.pQNeOr/ablpc-toolkit-v1.0.0.tar
  - work/releases/hardtruth-smoke.mdvyhs/report.json
  - work/releases/hardtruth-wrapper.rirLa9/state.json
  - work/releases/hardtruth-wrapper-env.z9hYBS/state.json
  - work/releases/hardtruth-lifecycle.7pamqua1
  - work/releases/hardtruth-path.0y_rnjxy
  - work/releases/hardtruth-state.p3l2ditq
  - work/releases/hardtruth-tar.9i5_t3xz
addresses: []
file_offsets: []
result: reject-installed-lifecycle-identity
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/release
  - implementation/compatibility
  - milestone/m6
  - audit/hard-truth
---

# EXP-20260814-106 - Independent M6 release hard-truth audit

## Verdict

**REJECT.** Exact M6 retains its deterministic asset-free archive, primary-
Linux launcher-readiness smoke, M4 compatibility, protected-content, and
repository-hygiene evidence. It does not satisfy the failure/rollback exit
gate: ordinary installed-tool use invalidates the declared complete inventory,
installed release roots can be substituted by symlinks, and dangling install
state is not admitted fail-closed.

M6 returns to Active. No successor milestone begins.

## Method and independence

A fresh-context verifier first read the required Vault system, charter,
roadmap, implementation, decision, and unknown notes. It kept tracked files
read-only and attacked exact clean HEAD
`61ab0f9400173e6137c93bae4e7ccb8cf00349e4` through two independent builds,
strict tar variants, the declared smoke matrix, fresh real and synthetic
installs, installed entry points, selection/rollback failures, and installed
path substitutions. All generated evidence remained ignored under `work/`.

## Retained release and smoke evidence

| Property | Independent observation |
|---|---|
| archive size | 378,880 bytes in both builds |
| archive SHA-256 | `1527281c60d1dd13ad0342a4cef9c8851d882a1cc1301083962f323ed64b62a0` |
| source-tree SHA-256 | `423eb946c35b2cc37a2642f9fb69e09304481972529ae63959e18c97dafeada7` |
| inventory | 36 source files plus one generated canonical manifest |
| build comparison | byte-identical; strict verification passes |
| tar topology | 37 unique sorted ASCII regular members under one root |
| metadata | fixed owner/group/epoch; 32 mode-0644 and 5 mode-0755 entries |
| protected content | no protected or forbidden path admitted; tracked audit 0 violations |

Reversed-member, PAX-encoded, duplicate, double-slash, symlink, Unicode-
renamed, appended-content, and corrupt variants all reject. The exact Fedora
matrix admits all 21 `LEVEL*.DAT` files and passes all three declared cases
with schemas 1, 1, and 2. All 747 source/stage entries restore exactly, no
stage remains, and the 3,978-byte report has SHA-256
`2f015813cf9c2891ba46881d3c48c8bc980578948d248540b4bd386a64237eb1`.
The game was not executed.

## Defect 1 - Ordinary installed use changes the complete inventory

A fresh exact v1.0.0 installation succeeded. Invoking its installed
`scripts/ablpc-release current --install-root <absolute-root>` through the
declared system Python 3.14.6 exited 2 with
`installed release contains missing or extra files`.

Importing the installed package created five unlisted files below
`reimplementation/ablpc/__pycache__/` with observed sizes 741, 10,794, 26,936,
51,907, and 5,336 bytes. Both the topology and content snapshots changed. On a
second fresh exact install, setting `PYTHONDONTWRITEBYTECODE=1` externally made
the same installed-wrapper command pass, created zero `.pyc` files, and left
repository-side inventory verification passing. This discriminates wrapper-
level bytecode suppression as the smallest correction and directly falsifies
the isolated-installed-wrapper claim in `EXP-20260814-105`.

## Defect 2 - Installed release path identity is not authenticated

After a valid synthetic v0.9.0 to v1.0.0 installation, the verifier moved the
prior version directory outside `INSTALL_ROOT/releases` and replaced its
lexical entry with a directory symlink. Rollback accepted it: the prior entry
was a symlink resolving outside `releases/`, selection changed to v0.9.0, and
`state.json` changed. Replacing the entire `releases/` directory with a
symlink likewise made `current` accept v1.0.0.

These cases contradict the claimed immutable-version-under-`releases/` and
tampered-prior fail-closed boundary. The lifecycle must authenticate both the
lexical `releases/` entry and the selected version entry as real non-link
directories before traversing installed inventory.

## Defect 3 - Dangling state identity is treated as absence

With a pre-existing dangling `state.json` symlink, installation succeeded,
replaced the link with a regular state file, and selected v1.0.0. The current
`exists()` check loses dangling-link identity before the later `lstat()`
boundary. State admission must inspect the directory entry without following
it and reject before mutation.

## Retained lifecycle and validation evidence

- Repository-side exact install/current succeeds.
- Ordinary synthetic v0.9.0 to v1.0.0 to rollback succeeds and retains both
  version directories.
- Corrupt, appended, no-history, and ordinary tampered-prior cases reject with
  snapshot preservation.
- Dirty/untracked files outside the tracked release allowlist are accepted;
  dirty or untracked selected sources reject, matching the declared boundary.
- M4 v0.1/v0.2 statements, implementation, three smoke manifests, launcher,
  and five compatibility anchors match the pre-M6 authority bytes.
- `make check` passes with Vault 304 notes, 0 errors, 0 warnings; 486 tests;
  five M4 anchors; and 0 tracked-file violations.
- Diff checks and the tracked-clean gate pass at the audited HEAD.

These positives do not repair the three installed-lifecycle contradictions.
Game execution, rendered/audio behavior, automated input, Windows, alternate
filesystems, concurrency, and unlisted environments remain untested.

## Exit-gate ledger

| M6 exit gate | Disposition |
|---|---|
| Reproducible tracked-source artifacts without protected material | **Supported:** independently reproduced exact archive/tree identities and adversarial verification. |
| Documented primary-Linux smoke matrix | **Supported at launcher-readiness scope:** exact 21-file, three-case, 747-entry result. |
| Failure and rollback paths exercised | **Open:** normal installed use and three path/state identity attacks contradict complete inventory and fail-closed claims. |
| Windows 98 controlled claims or explicit untested label | **Supported by explicit absence:** Windows remains named untested. |

## Smallest corrective packet

1. Suppress bytecode generation in every shipped Python entry point and prove
   ordinary installed invocation preserves the complete inventory.
2. Admit `state.json` through non-following identity inspection so dangling or
   linked state rejects before mutation.
3. Require the lexical `releases/` and selected-version entries to be real
   directories, not links, before inventory traversal.
4. Add exact full-snapshot regressions for all three failure families and
   retain the exact build, archive, smoke, M4, protected-content, test, Vault,
   diff, and clean-tree results.
5. Request a fresh-context hard-truth audit before closing M6.

## Result

`REJECT`: reopen M6 only for the installed-wrapper inventory and installed
state/root identity correction. Do not advance to another roadmap milestone.
