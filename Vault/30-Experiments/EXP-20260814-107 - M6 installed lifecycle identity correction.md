---
type: experiment
id: EXP-20260814-107
date: 2026-08-14
question: Can the exact EXP-106 installed-wrapper and installed-path contradictions be corrected without widening M6 or changing M4/game-facing behavior?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; exact local derived PC work copy; clean tracked release source; synthetic asset-free lifecycle repositories and ignored install roots
environment_version: kernel 7.0.11-200.fc44.x86_64; x86_64; Python 3.14.6; Wine 11.0 Staging; Gamescope 3.16.25-1.fc44.x86_64; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact clean implementation commit 580a1cb; source game tree work/copies/BUGS_PC-full-disc/PC/BUGS; Wine prefix work/wine/baseline; no executable launch; generated release/install/smoke evidence ignored under work/releases
artifacts:
  - work/releases/m6-corrective-a.bH4gh1/ablpc-toolkit-v1.0.0.tar
  - work/releases/m6-corrective-b.18ZNok/ablpc-toolkit-v1.0.0.tar
  - work/releases/m6-corrective-install.lcOCzz
  - work/releases/m6-corrective-smoke.7mhLZ1/report.json
addresses: []
file_offsets: []
result: worker-complete-pending-independent-audit
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/release
  - implementation/compatibility
  - milestone/m6
---

# EXP-20260814-107 - M6 installed lifecycle identity correction

## Subsequent disposition

Independent [[EXP-20260814-108 - Independent M6 lifecycle consistency hard-truth audit]]
supersedes this worker verdict with `REJECT`. The original three failures close,
but adjacent bytecode, topology, state, manifest, mode, and retained-version
consistency attacks remain. See `EXP-108` for the exact correction boundary.

## Verdict

**WORKER COMPLETE; NOT MILESTONE ACCEPTANCE.** The exact corrective packet from
`EXP-20260814-106` passes at clean implementation commit `580a1cb`. M6 remains
Active pending a fresh-context James audit.

## Bounded correction

- `scripts/ablpc-mod`, `scripts/ablpc-release`, and `scripts/m6-smoke` set
  `PYTHONDONTWRITEBYTECODE=1` and invoke the selected interpreter with `-B`.
- `scripts/check-m4-compatibility.py` sets `sys.dont_write_bytecode` before its
  first package import.
- `_install_state()` now uses `lstat()` directly: only true `ENOENT` means
  absent state; dangling links, other links, and nonregular entries reject.
- A shared directory-entry check admits the install root, `releases/`, and
  each selected version only as lexical non-link directories. Install,
  current, and rollback call it before installed inventory traversal.
- The machine/user documentation names the final-entry boundary and explicitly
  excludes concurrent replacement after inspection and unlisted filesystems.

No release schema/inventory membership, M4 authority/behavior, manifest schema,
game data, originals, launcher behavior, smoke scope, Windows state, M1/M2/M3/
M5, or PS1 evidence changed.

## Installed entry-point discriminator

One exact v1.0.0 artifact was installed under
`work/releases/m6-corrective-install.lcOCzz`. With `ABLPC_PYTHON`,
`PYTHONDONTWRITEBYTECODE`, and `PYTHONPYCACHEPREFIX` all removed externally,
the following installed entry points each exited 0:

1. `scripts/ablpc-mod --help`;
2. `scripts/ablpc-release current --install-root <absolute-root>`;
3. `scripts/m6-smoke --help`;
4. `scripts/check-m4-compatibility.py` through its system-Python shebang.

The complete install tar snapshot remained SHA-256
`a0ff1cc9be5c299e414dd6a3e53e1149da18969fcd584da125e5ff803bd095d2`
before and after all four calls. The tree retained 38 files, zero `.pyc`, zero
`__pycache__`, and repository-side `current` verification passed afterward.

The canonical regression independently copies all 36 exact package sources to
a fresh temporary Git repository, commits them, builds and installs that exact
package, removes all three external bytecode-control variables, invokes all
four entry points, and compares a mode/type/link-target/byte snapshot after
every call.

## State and path failure matrix

Every case below raises `ReleaseError` before lifecycle state mutation and
preserves a full snapshot including file bytes/modes, directories/modes, and
symlink targets:

| Attack | Operations covered |
|---|---|
| dangling `state.json` | install |
| linked `releases/` root | install, current, rollback |
| linked current selected-version root | install, current |
| linked prior selected-version root outside `releases/` | rollback |

This closes the three exact `EXP-20260814-106` failures plus their adjacent
install/current/rollback forms. It is a final-entry pre-mutation boundary, not
a post-inspection concurrency or general parent-filesystem guarantee.

## Reproducible artifact

Two independent clean-source builds are byte-identical:

| Property | Result |
|---|---|
| archive size | 389,120 bytes |
| archive SHA-256 | `7a1ede974edb637e58d87be10626e8cd0f00573e1b54492300466f5e9be2fcd2` |
| source-tree SHA-256 | `fa6a3ee49493a93175ef66a58103a0dc9815a65969574a4dbbc0920f382c85ea` |
| inventory | 36 tracked source files plus one generated manifest |
| strict verification | pass for both archives |
| byte comparison | exact |

The changed identities follow only from the bounded package-source correction
and truthful documentation. The source allowlist membership remains exact.

## Primary-host smoke result

The exact Fedora 44/kernel/Python/Wine/Gamescope smoke matrix remains `PASS`:

- all 21 PC `LEVEL*.DAT` files admit;
- Training schema 1, Level 01 schema 1, and Training character schema 2 pass;
- all three complete stage -> launcher-dry-run -> restore cases pass;
- source/stage inventories remain exact at 747 entries;
- no disposable smoke stage remains;
- the report is 4,122 bytes at SHA-256
  `1a8a3b5775f8d8f17c5110c4079401037e9bd6f5e36244be8891bf280227323e`.

The game was not executed; no rendered, gameplay, input, or audio result is
claimed.

## Validation

| Gate | Result |
|---|---|
| focused release tests | 13/13 pass |
| focused release plus smoke | 16/16 pass |
| canonical tests | 492/492 pass |
| M4 compatibility | valid; five anchors unchanged |
| Vault before worker evidence | 306 notes, 0 errors, 0 warnings |
| tracked protected-material audit | 0 violations |
| shell syntax, diff, staged diff | pass |
| clean implementation tree | commit `580a1cb` |

## Interpretation

- **Confirmed:** the exact code behavior, synthetic failure snapshots,
  installed-artifact entry-point results, artifact identities, smoke result,
  and validation gates above.
- **Inferred:** none required for the worker verdict.
- **Unknown/unsupported:** post-inspection concurrency, alternate filesystems,
  parent-filesystem policy beyond the admitted final entries, Windows, game
  execution, gameplay/input/render/audio outcomes, and unlisted hashes remain
  outside the packet.

## Result

Freeze this worker result and hand its exact clean commit to fresh-context
James. Only James `ACCEPT` can close M6; any surviving contradiction becomes
the next smallest correction.
