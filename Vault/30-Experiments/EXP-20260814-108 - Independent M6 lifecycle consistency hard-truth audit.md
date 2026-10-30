---
type: experiment
id: EXP-20260814-108
date: 2026-08-14
question: Does the first M6 correction remain fail-closed across hostile interpreter startup, the complete state/release/version lifecycle matrix, and adjacent installed inventory identity?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; exact clean tracked worker; ignored exact artifact, install, lifecycle, inventory, tar-adversary, and smoke roots
environment_version: kernel 7.0.11-200.fc44.x86_64; x86_64; Python 3.14.6; Wine 11.0 Staging; Gamescope 3.16.25-1.fc44.x86_64; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact clean audited HEAD 23ff833; implementation commit 580a1cb; tracked files read-only; no game execution
artifacts:
  - work/releases/james-m6-audit.bebhFb/build-a/ablpc-toolkit-v1.0.0.tar
  - work/releases/james-m6-audit.bebhFb/build-b/ablpc-toolkit-v1.0.0.tar
  - work/releases/james-m6-audit.bebhFb/lifecycle-matrix-report.json
  - work/releases/james-m6-audit.bebhFb/inventory-adjacency-report-2.json
  - work/releases/james-m6-audit.bebhFb/tar-adversary-report.json
  - work/releases/james-m6-audit.bebhFb/smoke-report.json
addresses: []
file_offsets: []
result: reject-installed-lifecycle-consistency
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/release
  - milestone/m6
  - audit/hard-truth
---

# EXP-20260814-108 - Independent M6 lifecycle consistency hard-truth audit

## Verdict

**REJECT.** James independently confirms that the three exact `EXP-106`
failures close at clean HEAD `23ff833`, but the claimed complete installed
lifecycle does not survive adjacent deterministic cases. M6 remains Active.

## Retained evidence

- Two exact 389,120-byte artifacts match at SHA-256
  `7a1ede974edb637e58d87be10626e8cd0f00573e1b54492300466f5e9be2fcd2`.
- Their 36-file source tree remains `fa6a3ee4...c85ea`; archive inventory is
  37 unique sorted ASCII regular members, 32 mode-0644 and 5 mode-0755.
- Thirteen strict tar variants covering appended data/zeros, truncation,
  order, PAX, duplicate, link, extra/missing, spelling, mode, content, and root
  identity all reject.
- Exact smoke remains 21/21 and 3/3 with 747 entries; its 4,122-byte report is
  SHA-256 `1a8a3b57...323e`.
- Normal installed entry points with external bytecode variables unset preserve
  inventory, and the original linked/dangling final-entry cases reject.

## Hostile interpreter-start contradiction

With `PYTHONPYCACHEPREFIX` directed inside the selected release, the direct
compatibility script's system interpreter creates 30 startup `.pyc` files
before in-script `sys.dont_write_bytecode` executes. The entry point itself
returns success, but repository-side `current` then rejects the changed
inventory. Shell entry points using interpreter `-B` remain stable. The direct
entry point must request `-B` in its shebang.

## Lifecycle matrix

James's synthetic v0.9.0/v1.0.0/v1.1.0 matrix records 55 cases:

| Result | Count |
|---|---:|
| proper rejection | 35 |
| improper success | 20 |
| full snapshot changed | 12 |

Concrete failure families are:

- moving a populated `releases/` root away before install creates a new empty
  lexical directory, then fails on the missing current version;
- moving `state.json` away lets install treat a populated repository as fresh,
  select v1.1.0, and discard prior selection/history;
- a two-link regular `state.json` is accepted by install/current/rollback;
- rollback accepts missing/dangling/nonregular/linked outgoing current roots;
- install and current accept equivalently invalid inactive prior roots;
- the accepting install/rollback families change full install/external-target
  snapshots.

## Installed inventory adjacency

Nine of ten attacks return success. Extra regular content is the sole rejected
control. Accepted cases are an extra empty directory, a hardlinked declared
file, a hardlinked release manifest, release-manifest mode/version/path/epoch
drift, nested directory mode drift, and selected-version root mode drift.

These are direct contradictions to complete installed topology/mode/content
verification and manifest identity, not concurrency or alternate-filesystem
questions.

## Smallest combined correction

1. Request interpreter `-B` before direct-script startup.
2. Validate stored state and existing release-root consistency before creating
   any topology; absent state may accompany only an absent/empty repository.
3. Require canonical single-link state, manifest, and package files plus exact
   implicit directories/modes.
4. Validate outgoing current, every rollback-history entry, and every retained
   installed version symmetrically for install/current/rollback.
5. Bind installed content to a state-held verified archive/manifest/tree lock
   so an in-tree manifest cannot self-authorize a new baseline.
6. Re-run this exact matrix and every retained M6 gate under James.

## Result

`REJECT`: advance only the combined installed-lifecycle consistency correction.
