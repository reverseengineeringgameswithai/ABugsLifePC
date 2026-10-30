---
type: experiment
id: EXP-20260814-109
date: 2026-08-14
question: Can one state-locked consistency validator close every EXP-108 lifecycle and inventory contradiction while retaining all M6 release and smoke gates?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; exact local derived PC work copy; clean tracked release source; ignored asset-free artifact/install/smoke roots
environment_version: kernel 7.0.11-200.fc44.x86_64; x86_64; Python 3.14.6; Wine 11.0 Staging; Gamescope 3.16.25-1.fc44.x86_64; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact clean HEAD 7d8594e; correction commits 46fa294 and 7d8594e; no game execution
artifacts:
  - work/releases/m6-ratchet3-a.9wXBUi/ablpc-toolkit-v1.0.0.tar
  - work/releases/m6-ratchet3-b.fDNy7n/ablpc-toolkit-v1.0.0.tar
  - work/releases/m6-ratchet3-install.KGD88w
  - work/releases/m6-ratchet3-smoke.lgyJzh/report.json
addresses: []
file_offsets: []
result: worker-complete-pending-james-reaudit
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/release
  - milestone/m6
---

# EXP-20260814-109 - M6 state-locked lifecycle consistency correction

## Subsequent disposition

Independent [[EXP-20260814-110 - Independent M6 state-locked lifecycle acceptance audit]]
returns `ACCEPT` at exact clean audited HEAD `64d8ac1`. Its reproduced
lifecycle, inventory, installed-entry-point, artifact, archive, smoke, test,
compatibility, Vault, and hygiene gates supersede this worker-only disposition
and close M6 at the documented boundary.

## Verdict

**WORKER COMPLETE; NOT MILESTONE ACCEPTANCE.** The combined `EXP-108`
correction passes locally at exact clean HEAD `7d8594e`. Only a new James
`ACCEPT` can close M6.

## Corrected boundary

- The direct Python checker's shebang supplies interpreter-start `-B`; all
  packaged entry points now resist both unset and hostile bytecode variables.
- State is admitted before release-directory creation. Missing state with a
  populated repository and missing releases with a selected state reject
  without topology changes.
- State, release manifests, and declared package files must be mode-exact
  single-link regular files. Release roots and implicit package directories
  must be non-links with exact modes and exact topology.
- Every installed version directory, including inactive and post-rollback
  retained versions, is validated on install/current/rollback. The directory
  set must exactly equal canonical state schema 2's `installed_releases` map.
- Each state lock records verified archive, release-manifest, and source-tree
  SHA-256. Verification reconstructs the canonical archive from installed
  bytes, so content plus a recomputed in-tree manifest rejects.
- State writes use unique `mkstemp` ownership and clean only their own
  temporary entry.

Concurrent replacement after inspection, other filesystems, general parent-
filesystem policy, Windows, and game execution remain explicitly outside this
boundary.

## Regression matrix

Thirty focused release tests cover:

- normal v0.9.0 -> v1.0.0 -> rollback with retained unselected validation;
- all four exact installed entry points under unset and hostile in-tree cache
  variables with a complete mode/type/link-target/content snapshot after every
  invocation;
- dangling, linked, missing, nonregular, hardlinked, and mode-drifted state;
- missing/linked/nonregular release roots and current/prior version roots
  across install/current/rollback;
- missing state with populated releases and missing releases with valid state;
- hardlinked manifest/declared files, manifest field/mode drift, extra empty
  directories, directory/root mode drift, and unlisted release-root entries;
- invalid inactive prior and missing outgoing current across every lifecycle
  operation;
- content plus recomputed manifest/tree rebaseline against the state lock;
- corrupt/appended archives, no-history, ordinary tamper, and successful
  migration/rollback baselines.

Every failure compares a full topology/mode/link-target/content snapshot.

## Exact installed entry points

One exact installed artifact ran all four entry points with
`PYTHONDONTWRITEBYTECODE=0` and `PYTHONPYCACHEPREFIX` directed inside the
selected version. All exited 0. The 38-file install snapshot remained SHA-256
`15ce25c53ec5924dbb52ba0f246e18cbe7aa594f48891cd11292abdd76ec60e4`
before and after; zero cache directory or `.pyc` appeared; repository-side
`current` passed. Canonical state is 442 bytes, mode 0644, link count 1.

## Reproducible release and smoke

| Property | Result |
|---|---|
| archive size | 399,360 bytes |
| archive SHA-256 | `68d3d31a84b01bafe6ca3711991aad7e058f95c5e72e7cc3b28799d533cb060b` |
| source-tree SHA-256 | `2644263f44558a0874d74d65f82b6f7001270d5d19b16a41b55f9a3b6b69bef9` |
| inventory | 36 source files plus one generated manifest |
| dual comparison / strict verify | byte-identical / pass |
| smoke | 21/21 files; schemas 1/1/2; 3/3 workflows; 747 entries |
| smoke report | 4,277 bytes; SHA-256 `c1fb69037def8c4093c8ede266b5ba858799705a7bd7eeb2807fa27a11b498dc` |

No residual stage remains, and no game execution/render/input/audio outcome is
claimed.

## Validation

| Gate | Result |
|---|---|
| focused release | 30/30 pass |
| canonical tests | 509/509 pass |
| M4 compatibility | valid; five anchors unchanged |
| Vault before worker evidence | 308 notes, 0 errors, 0 warnings |
| tracked protected-content audit | 0 violations |
| diff/staged diff/clean tree | pass at `7d8594e` |

## Result

Freeze exact HEAD `7d8594e` and return it to James. Any rejection becomes the
next smallest correction; only acceptance closes M6.
