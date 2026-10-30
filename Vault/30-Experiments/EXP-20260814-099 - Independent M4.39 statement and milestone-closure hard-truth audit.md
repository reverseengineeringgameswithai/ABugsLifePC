---
type: experiment
id: EXP-20260814-099
date: 2026-08-14
question: Does immutable M4.39 preserve historical v0.1, publish only the accepted v0.2 restoration boundary, and satisfy every final M4 gate under exact strictness and authority attacks?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; asset-free repository, synthetic metadata, and disposable tracked-tree audit only
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact audit/docs-only M4.40 of immutable worker 3394f2decaceaf3ea88e679a65a600ecdfb99cb5 above direct docs-only M4.38 verdict d00bba6b7c74bd969e9afad55efe276cb5de3e8b; no game execution or protected/game-file reads
artifacts:
  - reimplementation/compatibility/m4-v0.1.json
  - reimplementation/compatibility/m4-v0.2.json
  - reimplementation/ablpc/compatibility.py
  - scripts/check-m4-compatibility.py
  - tests/test_compatibility.py
  - Vault/30-Experiments/EXP-20260814-086 - M4 v0.1 milestone-closure evidence audit.md
  - Vault/30-Experiments/EXP-20260814-097 - Independent M4.37 complete-tree-uniqueness hard-truth audit.md
  - Vault/30-Experiments/EXP-20260814-098 - Strict v0.2 restoration compatibility statement.md
addresses: []
file_offsets: []
result: reject-m4-closure-version-binding-and-object-order-strictness-open
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/compatibility
  - audit/hard-truth
---

# EXP-20260814-099 - Independent M4.39 statement and milestone-closure hard-truth audit

## Verdict

**REJECT.** Immutable M4.39 preserves the accepted statement bytes, five
machine-authority pins, nine-read asset-free boundary, restoration truth, and
retained M4 behavior. It does not satisfy exact M4.40 strictness or the final
compatibility-statement exit gate.

Three coupled statement-selection/canonical-validation defects survive:

1. a canonically indented object with reordered fields is accepted because
   `_first_difference` compares mapping membership/value but not mapping order,
   and the loader re-encodes the attack in its attacker-supplied order;
2. the default `m4-v0.2.json` path accepts the complete valid v0.1 artifact and
   returns success as v0.1, while the explicit historical v0.1 path likewise
   accepts complete v0.2, because selected paths are not bound to version IDs;
3. a JSON object or array in `statement_id` reaches dictionary lookup and
   raises uncaught `TypeError`, rather than the checker's declared
   `CompatibilityError`/status-2 failure path.

The worker documentation also records 266 combined compatibility/manifest/
LEVEL tests. The exact three-file collection is 58 compatibility + 198
manifest + 15 LEVEL = **271**, and all 271 pass. This is a stale evidence count,
not a behavioral failure, but M4.40 does not silently preserve it.

M4 remains active. This audit changes documentation only and selects exactly
one corrective packet, M4.41. It does not change either statement, checker,
test, pin, authority, manifest, launcher, or game-facing file.

## Immutable gate and review boundary

The first repository read found:

- clean exact HEAD `3394f2decaceaf3ea88e679a65a600ecdfb99cb5`;
- exact direct parent `d00bba6b7c74bd969e9afad55efe276cb5de3e8b`;
- exact worker tree `a431aa8960db3c984c2e8c6ee6241e19d327d23f`.

The complete startup policy, full Roadmap/Decision Log/Known Unknowns, relevant
MOCs, M4.27 ledger, EXP-078/086/094/097/098, M4/M1 notes, root 1336 session,
both READMEs, Environment/Wine authority, both statements, checker, full
compatibility implementation/tests, complete 1,355-line worker diff, and every
worker-touched implementation/test/metadata file were read before disposition.

No executable or game file was inspected or run. No path below `originals/`,
`media/`, or `work/` was read. The only disposable repository copy came from
`git archive` of the tracked immutable worker.

## Independent statement reconstruction

The reconstruction parsed raw bytes with a separately authored duplicate-key
hook and non-standard-constant rejection. It did not import either expected-
statement constant.

| Contract | Bytes | SHA-256 | Scalar leaves | Ordered top-level keys |
|---|---:|---|---:|---|
| historical v0.1 | 6,177 | `c3427d44cf32619a1f9bbcab7c51e67c0846b35d9d53eab7632ff6356c0beaf0` | 126 | 10 |
| active v0.2 | 7,677 | `dacfcab8c1d27e5a63db870f347eb08701f868ca678cafdd178913266f20ccb2` | 151 | 11 |

Both tracked files are strict UTF-8 and equal their own `json.dumps(...,
indent=2) + "\n"` encoding. `git diff --exit-code` against the exact parent
proves v0.1 was not changed by M4.39.

The ordered v0.1 top keys are `statement_schema_version`, `statement_id`,
`toolkit_version`, `status_vocabulary`, `hash_anchors`, `manifest_contract`,
`tested_tool_environment`, `removal_boundary`, `tested_wine_gamescope_scope`,
and `unsupported`. v0.2 inserts only `restoration_boundary` between the removal
and Wine/Gamescope objects.

Both statements independently enumerate the exact same five anchors:

| ID | Path | SHA-256 |
|---|---|---|
| `pc-executable` | `bugs.exe` | `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878` |
| `training-level-dat` | `CD/LEVEL07/LEVEL1.DAT` | `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22` |
| `level01-level-dat` | `CD/LEVEL01/LEVEL.DAT` | `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53` |
| `flick-all-destination` | `CD/CHARS/FLICK.ALL` | `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6` |
| `flickd-all-source` | `CD/CHARS3/FLICKD.ALL` | `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4` |

v0.1 workflows are `apply`, `stage`, `compose`, and `remove`. v0.2 adds only
`restore` with scope
`manifest-and-source-authenticated-complete-staged-tree-on-declared-linux-environment`.
The structural delta is exactly the statement/toolkit version scalars, that one
workflow append, one `restoration_boundary` object, and the necessary split of
the old combined unsupported restoration wording. No anchor, recipe, schema,
format, operation, environment, removal, or Wine/Gamescope value changes.

The v0.2 unsupported list still excludes unlisted hashes as demonstrated
anchors; untested Windows/Wine/kernel/architecture/filesystems; general `.ALL`
identity; N-way/cross-input solving; whole staged-tree/source deletion;
external-receipt full-tree restoration; rollback/backup/trash/package/general
transactions; provenance/POSIX metadata equality; general Windows path policy;
general mod dry-run/launch/runtime automation; and post-preflight concurrency
guarantees.

## Restoration truth audit

The added fields match `EXP-20260814-094/097` and the exact accepted manifest
implementation pin. `restore_manifest` takes an existing manifest and exact
source, inventories the source before preparation, rejects source `.ablpc`,
prepares exact outputs/ordinary receipt, authenticates the complete staged game
tree, and then writes only recorded destinations from retained exact source
bytes before removing the receipt and empty metadata directory.

`_regular_tree_inventory` permits directories and regular single-link files,
rejects links/nonregular/multi-link entries, and requires every relative POSIX
path to be unique under `casefold()` before descending into ambiguous siblings.
`_validate_complete_staged_tree` requires exact path/type membership and exact
content for unrelated files, exact recomputed output hashes for destinations,
and byte-exact ordinary receipt data. `_validate_unmounted_restoration_plan`
uses the retained mountinfo/listmount/statmount view for every expected game
path and proper ancestry; missing, malformed, changed, or inconsistent topology
fails closed. Mutation remains sequential and non-transactional after
preflight.

Nothing in the statement implies external-receipt full-tree restoration,
staged/source deletion, other platforms/filesystems, provenance, POSIX
metadata equality, backup/rollback/package/transaction behavior, general
launch/runtime automation, general Windows path policy, or a concurrency
guarantee. The implementation itself was not changed by M4.39.

## Strictness attacks

Direct independently generated value drift at all **151** v0.2 scalar leaves
rejects. Direct type drift at all leaves also fails to accept, but 150 use the
declared `CompatibilityError` path and the unhashable `statement_id` case leaks
`TypeError`.

The following independently generated attacks reject normally:

- missing and extra fields;
- reordered workflows, interfaces, and unsupported lists;
- duplicate nested keys;
- unknown statement and anchor IDs;
- changed scalar types/values outside the unhashable-ID error defect;
- compact whitespace, CRLF, UTF-8 BOM, invalid UTF-8, and `NaN`;
- v0.1/v0.2 field hybrids;
- restoration authority overstatement; and
- removal of the external-receipt unsupported declaration.

The exact accepted counterexamples are:

```text
reordered object fields with indent-2/newline encoding -> accepted
default m4-v0.2 path containing complete v0.1 bytes -> status 0, reports v0.1
explicit m4-v0.1 path containing complete v0.2 bytes -> status 0, reports v0.2
object-valued statement_id -> status 1, empty stdout, traceback, uncaught TypeError
```

These are asset-free statement/checker cases. They do not touch manifest or
game behavior.

## Authority and read boundary

Independent raw hashing confirms exactly five machine authorities and no M4.39
change to any of them:

| Authority | SHA-256 |
|---|---|
| Training manifest | `315320bc524986348167ca556b178ef41fe1e8ac961e482610f8f734f34b2434` |
| Level 01 manifest | `358998cd326f68fcf7e10593e8ec895915b558252c300464e8fe74177280198f` |
| opaque replacement manifest | `5aaa6e9a4fa79c303ee0920e7f87e00e87bd1dfef412a32c55e36efcc947b607` |
| launcher | `68c9171749bd7b207a15b4202193ccfddd2661fbb383deb34b1a5a5a4049977e` |
| manifest implementation | `b3480761ac2b4791ccbf1df69f88234532f27956152045b89615dd5ec5bf6d75` |

All five direct and missing/drift classes fail on the SHA-256 pin before a
semantic-alignment sentinel can run. Independent Environment, Wine baseline,
and reimplementation README mutations fail in their scoped semantic checks.

Both normal version checks read exactly nine unique tracked paths in exact
order: one selected statement, three manifests, launcher, manifest
implementation, Environment Status, Wine baseline, and reimplementation
README. There are no duplicates and no protected or game-like paths.

## M4.27 ledger reconciliation

The original nine-capability/five-exit-gate ledger remains the controlling
closure test.

| Ledger row | M4.40 disposition |
|---|---|
| inspect supported formats/compatibility | retained at bounded LEVEL/ANM/anchor scope |
| compose declarative manifests/conflicts | retained at exact two-input authored-order scope |
| validate hashes/formats | retained for schemas 1/2 and four operations |
| deterministic single-manifest dry-run | independently accepted by M4.26 |
| stage/apply without originals mutation | independently accepted with nontransactional limit |
| tested Wine/Gamescope launch | retained as manual exact-scope launcher evidence |
| receipt sufficient for reproduce/remove | closed by M4.28 through accepted M4.33 strict current-receipt chain |
| synthetic and user-owned corpus tests | retained; no corpus bytes enter this audit |
| versioned limitations/runtime statement | **open** on the strictness/version-binding defects above |
| two useful mod classes | retained |
| two manifests compose/conflict | retained |
| same-tree install/validate/launch/remove | closed only by accepted M4.38 manifest-driven current-Linux stage/dry-run/restore lifecycle |
| no original/game package | retained by tracked audit and byte review |
| versioned hash/Wine statement | **open** until M4.41 closes exact checker strictness |

The receipt and same-tree gaps that caused M4.27 rejection are genuinely
closed by independently accepted evidence. The final statement row is not.
M4 cannot be marked complete by passing test totals while that written gate is
falsified.

## Validation and hygiene

- focused compatibility: 58/58 passed;
- exact compatibility + manifest + LEVEL command: 271/271 passed;
- canonical `.venv/bin/python -m pytest -q tests`: 459/459 passed;
- both normal checker invocations: valid expected v0.2 and historical v0.1;
- final pre-commit Vault lint: 291 notes, zero errors/warnings;
- tracked-file audit: zero violations;
- five pins, statement hashes, worker no-authority diff, read trace, diff
  checks, MIME/protected-path/no-game-byte review: retained.

No unscoped pytest command was used. Green retained gates do not override the
four exact documentation/checker falsifications.

## Sole corrective packet: M4.41

**Name:** Version-bound canonical statement strictness correction.

**Bounded question:** Can the compatibility checker bind the active and
historical selected statement paths to their exact version IDs, require the
expected object-key order recursively, and reject non-string/unhashable
`statement_id` through its ordinary error path, while preserving both statement
files, all authorities/pins/reads, semantic alignment, and every M4 behavior?

**Exact locators:** `validate_compatibility_statement`, `_first_difference`,
`load_compatibility_statement`, and `check_compatibility_statement` in
`reimplementation/ablpc/compatibility.py`; CLI selection in
`scripts/check-m4-compatibility.py`; `tests/test_compatibility.py`; both exact
statement files; and the stale combined-count documentation named above.

**First pass:** add explicit expected-version selection for the default v0.2
and historical v0.1 checks; reject full valid cross-version replacement at
those selected paths; compare object key sequences recursively; convert every
non-string/unhashable ID into `CompatibilityError`; add top/nested reordered-
field, complete downgrade/upgrade, list/object-ID, and CLI status-2/no-traceback
regressions. Correct the combined compatibility/manifest/LEVEL evidence count
from 266 to exact 271.

**Stop rule:** do not change either statement byte, any machine pin or
authority, manifest/receipt/schema/format/operation, input/hash/output policy,
apply/stage/compose/dry-run/replay/remove/restore behavior, mount policy,
launcher, asset, runtime, M1/M2/PS1, platform scope, or unsupported declaration.
Do not start M3, M5, or M6 and do not mark M4 complete at the worker edge.

**Done when:** the four counterexample families reject through deterministic
checker errors, both correct version invocations retain one statement plus the
same eight authority reads, all 151 value/type attacks and every retained
authority test pass, exact 58/271/459 or resulting explicitly collected totals
are recorded accurately, all hygiene gates pass, and one clean bounded worker
commit is ready for fresh-context audit. No second successor is selected here.

## Worker disposition

[[EXP-20260814-100 - Version-bound canonical compatibility-statement strictness]]
completes exact M4.41 at the worker boundary. The four counterexample families
now reject deterministically; both normal versions retain nine reads; all 151
value and 151 type attacks reject; exact suites pass 71/284/472. Statements,
pins, authorities, and behavior remain unchanged. Independent M4.42 owns final
acceptance and milestone disposition.
