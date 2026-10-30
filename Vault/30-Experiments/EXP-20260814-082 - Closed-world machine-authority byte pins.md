---
type: experiment
id: EXP-20260814-082
date: 2026-08-14
question: Can the asset-free M4 checker close the observed effective-language and duplicate-key bypasses by pinning exactly five already-read machine authorities without changing the statement, authorities, behavior, or nine-read boundary?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; Linux 7.0.11 x86_64; asset-free tracked sources and synthetic temporary copies only
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.23 correction only; no statement, authority, manifest, launcher, game, original, media, work-copy, runtime, M2, PS1, mount-policy, transaction, schema, receipt, operation, workflow, or general input-policy change
artifacts:
  - reimplementation/ablpc/compatibility.py
  - tests/test_compatibility.py
  - reimplementation/compatibility/m4-v0.1.json
  - scripts/play-pristine.sh
  - reimplementation/ablpc/manifest.py
  - mods/training-primary-record-124-target-111e4.json
  - mods/level01-primary-record-261-target-3459c.json
  - mods/chars-flick-all-from-chars3-flickd-all.json
addresses: []
file_offsets: []
result: pass-worker-five-same-read-machine-authority-pins
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/compatibility
---

# EXP-20260814-082 - Closed-world machine-authority byte pins

## Question

Can exact M4.23 reject the six residual effective-language and duplicate-key
bypass families found by M4.22 by hashing only the five machine authorities
already read by the compatibility checker, while preserving the exact
statement, human-edited scoped checks, nine-read asset-free boundary, and all
game-facing behavior?

## Boundary

The worker began from clean exact audit commit
`7f3cec8540fb2ba081e1fdb7a6f07c6d4bd268d1` after the complete required
[[START HERE]] and Obsidian refresh. Only
`reimplementation/ablpc/compatibility.py`, its synthetic tests, and required
documentation changed. The following remain byte-exact:

- canonical 6,177-byte `reimplementation/compatibility/m4-v0.1.json`, SHA-256
  `c3427d44cf32619a1f9bbcab7c51e67c0846b35d9d53eab7632ff6356c0beaf0`;
- `scripts/play-pristine.sh`, `reimplementation/ablpc/manifest.py`, and the
  three tracked manifests listed below;
- Environment Status, Wine baseline, and reimplementation README authority
  values;
- schema, receipt, formats, operations, workflows, apply/stage/compose/remove,
  launcher, mount, transaction, and game-facing behavior;
- all original, media, work-copy, runtime, M2, and external PS1 surfaces.

No game file was read or executed. Every rejected mutation is an asset-free
pytest temporary copy.

## Implementation

**Confirmed at the M4.23 worker boundary:** repository alignment now reads the
raw bytes of exactly five executable or machine-readable authorities once,
compares their SHA-256 digests before semantic alignment, and reuses those
same bytes for strict manifest parsing and launcher/Python contract checks.

| Authority | Required SHA-256 |
|---|---|
| `scripts/play-pristine.sh` | `68c9171749bd7b207a15b4202193ccfddd2661fbb383deb34b1a5a5a4049977e` |
| `reimplementation/ablpc/manifest.py` | `6ed013863347646aa058340576820236334930401d1c92c2d3894002e2fcc4ad` |
| `mods/training-primary-record-124-target-111e4.json` | `315320bc524986348167ca556b178ef41fe1e8ac961e482610f8f734f34b2434` |
| `mods/level01-primary-record-261-target-3459c.json` | `358998cd326f68fcf7e10593e8ec895915b558252c300464e8fe74177280198f` |
| `mods/chars-flick-all-from-chars3-flickd-all.json` | `5aaa6e9a4fa79c303ee0920e7f87e00e87bd1dfef412a32c55e36efcc947b607` |

This pin set is closed and local to statement alignment. It is not a manifest-
loader allowlist and does not make these five files a general input policy.
The source-aware checks from M4.21 remain explanatory cross-checks. Generated
Environment and scoped Wine/README declarations retain their existing
structured checks and are not byte-pinned.

## Regression matrix

The focused suite expands from 36 to 47 passing tests. Five direct tests
recompute every published pin from the checked-in raw bytes. Six regressions
copy the complete asset-free authority set, make one mutation, and require
SHA-256 drift rejection for:

1. post-validation Bash indexed scalar mutation;
2. post-literal command-array append;
3. post-guard game-directory mutation;
4. Python `globals()` receipt rebinding;
5. validator-name rebinding;
6. a conflicting duplicate manifest key whose expected value is last.

The exact four M4.20 attacks and all earlier strict-statement, direct-drift,
source-aware, generated-row, and scoped-Markdown regressions remain present
and pass. The canonical scoped suite expands from 329 to 340 passing tests.

## Results

- unchanged repository alignment: pass;
- exact M4 compatibility CLI: v0.1 valid with five anchors;
- focused `tests/test_compatibility.py`: 47/47 passed;
- canonical scoped `tests`: 340/340 passed;
- independently recomputed statement and five authority hashes: exact;
- read trace: exactly nine reads in the retained order—statement, three
  manifests, launcher, manifest implementation, Environment Status, Wine
  baseline, and reimplementation README;
- protected read roots `originals/`, `media/`, and `work/`: zero;
- final `make check`: Python doctor green, Vault lint 257 notes with zero
  errors/warnings, five-anchor checker green, 340 tests, and tracked-file audit
  zero violations;
- final diff/MIME audit: 18 changed/new paths, all Markdown/plain text or
  Python source; `git diff --check` clean;
- no statement, authority, manifest, launcher, Environment/Wine/README fact,
  asset, original, media, work, or external PS1 file changed.

The final staged protected/no-game-bytes, intentional-commit, and clean-tree
checks are recorded in the session note and worker commit after staging.

## Limitations

- This is a closed-world consistency guard for five exact checked-in
  authorities, not a Bash/Python security analyzer or general JSON policy.
- Updating one pinned authority intentionally requires reviewing and updating
  its expected digest and the compatibility evidence together.
- Human-edited Environment/Wine/README sources remain scoped declarative
  checks rather than whole-file pins.
- No new supported hash, platform, workflow, operation, runtime, launch,
  dry-run, package, `.ALL`, M2, mount, rollback, or transaction claim follows.
- Worker success is not independent acceptance. Exact M4.24 must audit the
  immutable commit from fresh context.

## Exact next packet: M4.24

**Name:** Independent M4.23 machine-authority-pin hard-truth audit.

**Bounded question:** Does immutable M4.23 fail closed on any byte drift in
exactly the five pinned machine authorities before semantic alignment, reject
the six M4.22 bypass families and exact four M4.20 attacks, and preserve the
exact statement, scoped human-authority checks, nine-read no-game boundary,
and every retained M4/M1 gate?

**Exact locators and inputs:** intentional clean M4.23 worker commit and its
direct parent; this experiment; `EXP-20260814-078` through `EXP-20260814-081`;
exact worker diff; `EXPECTED_MACHINE_AUTHORITY_SHA256`,
`_read_machine_authorities`, `_load_tracked_manifest`, and
`validate_repository_alignment` in `reimplementation/ablpc/compatibility.py`;
`tests/test_compatibility.py`; statement; five pinned authorities; three
scoped human-readable authorities; M4/M1 notes; every M4.23 stop/done gate.

**First pass:** James must begin in fresh context, reread [[START HERE]] and
the complete required Obsidian startup sequence, verify exact immutable HEAD,
direct parent, and clean Git, then independently recompute the statement and
five authority hashes without importing the expected-pin mapping. Reproduce
all six exact M4.22 bypasses and four exact M4.20 attacks in isolated copies;
mutate each pinned file directly; verify digest failure occurs before semantic
alignment; confirm unchanged semantic/scoped checks, strict statement, exactly
nine asset-free reads, zero protected reads, focused/canonical and all hygiene
gates.

**Stop rule:** audit only. Do not change implementation, tests, statement,
pins, authorities, manifests, launcher, Environment/Wine/README facts, assets,
schema, receipt, operations, workflows, apply/stage/compose/remove, runtime,
M2, PS1, mount policy, transaction behavior, prose scope, or input policy. A
rejection records one exact bounded correction and changes documentation only.

**Done when:** one independent evidence-backed `ACCEPT` or `REJECT` is
recorded across all required Vault/README surfaces in a docs-only commit
directly after the worker and Git is clean. `ACCEPT` selects exactly one
remaining written M4 gate/capability or a bounded milestone-closure audit;
`REJECT` selects exactly one correction with locators, first pass, stop rule,
and done condition.

## Subsequent disposition

[[EXP-20260814-083 - Independent M4.23 machine-authority-pin hard-truth audit]]
returns `ACCEPT` on immutable worker
`33e0bfc39e05267789f2b375acee2248f97f2053`. Independent reconstruction found
the canonical 6,177-byte statement, five exact hashes, and a pin set of exactly
five/no extras. All ten predecessor attacks, five direct mutations, five
missing-pin cases, three scoped human checks, exactly nine reads, 47/152/340
tests, and every hygiene gate survive. This accepts only the M4.23 boundary;
exact deterministic single-manifest dry-run report M4.25 is the sole successor.
