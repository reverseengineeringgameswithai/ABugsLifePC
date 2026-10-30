---
type: experiment
id: EXP-20260814-083
date: 2026-08-14
question: Does immutable M4.23 fail closed on any byte drift in exactly five pinned machine authorities before semantic alignment while preserving the exact statement, scoped human checks, nine-read no-game boundary, and all retained gates?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; Linux 7.0.11 x86_64; asset-free tracked sources and isolated synthetic copies only
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.24 audit only; immutable worker 33e0bfc39e05267789f2b375acee2248f97f2053 over direct parent 7f3cec8540fb2ba081e1fdb7a6f07c6d4bd268d1; no implementation, test, statement, pin, authority, asset, runtime, M2, PS1, mount, transaction, prose-scope, or input-policy change
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
result: accept-m4-23-exact-five-same-read-machine-authority-pins
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/compatibility
---

# EXP-20260814-083 - Independent M4.23 machine-authority-pin hard-truth audit

## Verdict

**ACCEPT.** Immutable worker commit
`33e0bfc39e05267789f2b375acee2248f97f2053`, directly over required parent
`7f3cec8540fb2ba081e1fdb7a6f07c6d4bd268d1`, satisfies every exact M4.24 done
condition. Preflight found that exact HEAD/parent pair and a clean tree before
any audit action.

## Independent reconstruction

The verifier parsed the statement with an independent duplicate-key rejecting
JSON loader and did not import or use `EXPECTED_MACHINE_AUTHORITY_SHA256` to
derive expected bytes. The checked-in statement is canonical JSON, exactly
6,177 bytes, SHA-256
`c3427d44cf32619a1f9bbcab7c51e67c0846b35d9d53eab7632ff6356c0beaf0`,
with 10 top-level keys, five hash anchors, three tracked recipes, and 126
scalar leaves.

The three manifest paths were derived from the parsed tracked recipes, the
launcher from the parsed Wine/Gamescope scope, and the manifest implementation
from the written M4.23 contract. Hashing those raw files independently yielded:

| Machine authority | Independently computed SHA-256 |
|---|---|
| `scripts/play-pristine.sh` | `68c9171749bd7b207a15b4202193ccfddd2661fbb383deb34b1a5a5a4049977e` |
| `reimplementation/ablpc/manifest.py` | `6ed013863347646aa058340576820236334930401d1c92c2d3894002e2fcc4ad` |
| `mods/training-primary-record-124-target-111e4.json` | `315320bc524986348167ca556b178ef41fe1e8ac961e482610f8f734f34b2434` |
| `mods/level01-primary-record-261-target-3459c.json` | `358998cd326f68fcf7e10593e8ec895915b558252c300464e8fe74177280198f` |
| `mods/chars-flick-all-from-chars3-flickd-all.json` | `5aaa6e9a4fa79c303ee0920e7f87e00e87bd1dfef412a32c55e36efcc947b607` |

An independent AST read then found exactly those five keys and no extras in
the implementation mapping; all five recorded values matched the independently
computed bytes.

## Adversarial evidence

Every mutation used a fresh asset-free temporary copy of all eight repository-
alignment sources. A verifier-owned sentinel replaced
`_validate_recipe_alignment` during machine attacks. All nine machine-source
attacks raised `SHA-256 drifted` without reaching that sentinel:

1. post-validation `OUTPUT_WIDTH[0]=1`;
2. post-literal `COMMAND+=( -S stretch -F linear )`;
3. post-guard `GAME_DIR[0]=/tmp`;
4. `globals()["_RECEIPT_RELATIVE"]` rebinding;
5. `_validate_manifest` name rebinding;
6. conflicting duplicate tracked-manifest `schema_version` with expected last;
7. M4.20 competing `OUTPUT_WIDTH=1`;
8. M4.20 competing `FILTER=linear`;
9. M4.20 competing `_RECEIPT_RELATIVE`.

The tenth predecessor attack, a second contradictory generated Kernel row,
passed the five unchanged pins and rejected at the retained scoped Environment
semantic check. The exact predecessor matrix is therefore 10/10 rejected: six
M4.22 families plus four M4.20 attacks.

Appending one byte-changing newline independently to each pinned authority
also rejected 5/5 before recipe semantic alignment. Removing each pin in a
fresh copy produced a wrapped `cannot read evidence source` failure 5/5 before
semantic alignment. Separate Environment, Wine-baseline, and reimplementation-
README mutations rejected 3/3 through their retained scoped checks while
remaining deliberately outside the pin set.

## Read and gate evidence

Verifier-owned `Path.read_bytes`/`Path.read_text` instrumentation observed
exactly nine calls and nine unique paths on the unchanged repository, in this
order:

1. compatibility statement;
2. Training manifest;
3. Level 01 manifest;
4. opaque whole-file manifest;
5. launcher;
6. manifest implementation;
7. Environment Status;
8. Wine Linux Play Baseline;
9. reimplementation README.

Each of the five machine authorities was opened exactly once and its accepted
bytes were reused. Reads below `originals/`, `media/`, or `work/`: zero.

- focused compatibility suite: 47/47 passed;
- combined M4/M1 manifest, LEVEL DAT, and compatibility slice: 152/152 passed;
- canonical suite: 340/340 passed;
- `make check`: Python doctor green, Vault lint green, compatibility checker
  green with five anchors, 340 tests, tracked-file audit zero violations, and
  diff checks clean;
- immutable worker diff: 18 text/Python paths, zero binary entries, zero
  protected paths, zero forbidden media extensions, and zero statement or
  authority paths changed;
- no game, runtime, local work-copy, original, media, external PS1, or
  protected byte was read, copied, executed, or modified.

## Scope and limitations

Acceptance is exactly the M4.23 compatibility-alignment boundary. The five
pins are not a manifest-loader allowlist or general input policy. Human-edited
authorities remain scoped checks. No new hash, platform, parser, schema,
receipt, format, operation, workflow, launch, runtime, mount, rollback,
transaction, package, `.ALL`, M2, or PS1 claim follows.

M4 is not complete: its written required capability to dry-run changes and
report affected files, records, and byte ranges remains unmet. Exact
[[Project Roadmap#M4.25 — Deterministic single-manifest dry-run report]] is the
sole successor.

## Subsequent disposition

[[EXP-20260814-084 - Deterministic single-manifest dry-run report]] completes
that exact M4.25 worker packet. One existing manifest now reports deterministic
authored paths/records, hashes/sizes, and half-open ranges from ordinary
preparation with exact snapshots and 99/161/349 tests. Only the independently
recomputed manifest implementation pin changed; five-pin/nine-read
compatibility survives. Exact M4.26 owns independent acceptance, so this does
not yet establish M4.25 or milestone completion.
