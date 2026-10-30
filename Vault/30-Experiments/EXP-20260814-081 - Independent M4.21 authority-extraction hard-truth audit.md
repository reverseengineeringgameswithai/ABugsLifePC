---
type: experiment
id: EXP-20260814-081
date: 2026-08-14
question: Does immutable M4.21 reject representative ambiguity across every already-claimed compatibility authority while preserving the exact statement, nine-read asset-free boundary, and retained M4/M1 gates?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; Linux 7.0.11 x86_64; asset-free tracked sources and synthetic temporary copies only
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact fresh-context M4.22 audit of immutable fb015804f50758d9999e655e01e5abc61707646f only; documentation-only verdict; no game/original/media/work-copy/PS1 access and no implementation, test, metadata, authority, manifest, launcher, schema, receipt, operation, workflow, runtime, mount-policy, or transaction change
artifacts:
  - reimplementation/compatibility/m4-v0.1.json
  - reimplementation/ablpc/compatibility.py
  - tests/test_compatibility.py
  - scripts/play-pristine.sh
  - reimplementation/ablpc/manifest.py
  - mods/training-primary-record-124-target-111e4.json
  - mods/level01-primary-record-261-target-3459c.json
  - mods/chars-flick-all-from-chars3-flickd-all.json
addresses: []
file_offsets: []
result: reject-residual-effective-mutation-and-duplicate-manifest-key-bypasses
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - audit/hard-truth
---

# EXP-20260814-081 - Independent M4.21 authority-extraction hard-truth audit

## Question and immutable boundary

Does immutable M4.21 actually reject every exact M4.20 counterexample and
representative adjacent ambiguity for all already-claimed launcher, Python,
Environment, Wine-baseline, README, and manifest authorities, while retaining
the exact statement, exactly nine asset-free reads, and every accepted M4/M1
gate?

The audit began with exact clean worker commit
`fb015804f50758d9999e655e01e5abc61707646f`, whose direct parent is
`e20a44d9c6455f9004026e6f9b17020aae8da809`. The complete required startup
corpus, exact worker diff, checker/tests, statement, launcher, manifest
implementation, three tracked manifests, Environment/Wine authorities, both
READMEs, and M4/M1 notes were read before attack work. The external PS1 tree
was not consulted. No game, original, media, work-copy, log, dump, or runtime
file was read or executed. Every mutation existed only in a disposable
asset-free temporary copy.

## Independent reconstruction

Independent strict parsing, without importing the compatibility checker,
reproduced a canonical UTF-8 statement of exactly 6,177 bytes, SHA-256
`c3427d44cf32619a1f9bbcab7c51e67c0846b35d9d53eab7632ff6356c0beaf0`,
10 top-level fields, 126 scalar leaves, and no duplicate keys. It reproduced:

- the five path/hash/role/status/evidence anchors headed by unchanged
  `bugs.exe` SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`;
- schemas 1/2, the two formats, three M1 operations plus exact whole-file
  replacement, four workflows, fail-closed policy, and
  `.ablpc/receipt.json`;
- Fedora 44, kernel `7.0.11-200.fc44.x86_64`, x86_64, Python 3.14.6,
  current-Linux removal interfaces, the non-transactional limit, exact
  Wine/Gamescope presentation, four positive renderer markers,
  `INITSOFTRENDER` rejection, and all seven unsupported families.

Separate strict manifest parsing reproduced the two schema-1 DAT anchors and
the schema-2 `FLICK.ALL <- FLICKD.ALL` anchor. Independent line/token and AST
censuses reproduced the checked launch assignments, literal command array,
derived-copy guard, receipt and Linux mount constants, schemas, formats, and
operations. Direct section/block reads reproduced the six generated doctor
rows and every keyed Wine/README declaration. The checked-in authorities are
therefore aligned; the rejection concerns what drift the checker accepts.

## Attack matrix

All four exact M4.20 attacks now reject:

1. later direct `OUTPUT_WIDTH=1`;
2. later direct `FILTER=linear`;
3. later direct `_RECEIPT_RELATIVE` assignment;
4. a second generated `Kernel` row.

Direct missing/changed declarations, supported parameter-expansion writes,
extra literal command options, Python duplicate constants/format additions,
generated-block marker and row ambiguity, duplicate/changed scoped Wine and
README declarations, and direct tracked-manifest hash/path drift also reject.
Nine independent statement attacks covering missing/changed/extra/reordered,
duplicate-key, noncanonical, non-standard-number, malformed, and invalid-UTF-8
forms reject.

The broader 31-case independent authority matrix nevertheless returned 10
false successes. The following minimized examples are ordinary effective
language operations or machine-readable ambiguity, not unrelated prose:

- after numeric validation, `OUTPUT_WIDTH[0]=1` changes the Bash scalar to
  `1`, while `OUTPUT_WIDTH+=1` changes it to `25601`; both pass alignment;
- after the literal array, `COMMAND+=( -S stretch -F linear )` appends four
  effective arguments, and `COMMAND[4]=320` changes the checked surface width;
  both pass;
- after the derived-copy guard, `GAME_DIR[0]=/tmp` changes the effective game
  directory and bypasses the already-completed guard, yet passes;
- `globals()["_RECEIPT_RELATIVE"] = PurePosixPath(".ablpc", "other.json")`
  changes the receipt binding but is outside the selected assignment AST;
- EOF rebindings of `_validate_manifest` and `_validate_file_entry` to lambdas
  leave the one checked `FunctionDef` in the AST while replacing its effective
  module binding; both pass;
- conflicting duplicate `schema_version` or destination `sha256` keys in the
  Training manifest pass when the expected value is last, because the tracked-
  manifest loader silently applies JSON last-key-wins behavior.

`bash -n` accepts each mutated full launcher. A separate asset-free Bash
semantic check returned `indexed=1`, `compound=25601`, `game_dir=/tmp`, and
the appended command tokens. A separate Python semantic check returned
`.ablpc/other.json` and the rebound validator result. These provide execution-
language evidence independent of the checker's successful return.

## Retained boundaries and gates

A read-tracing wrapper around the unchanged checker observed exactly nine
unique reads, in order: statement bytes; three manifest texts; launcher;
manifest implementation; Environment Status; Wine baseline; and
reimplementation README. All nine resolve inside the repository and none is
below `originals/`, `media/`, or `work/`.

The retained results are:

- focused `tests/test_compatibility.py`: 36/36 passed;
- canonical scoped `tests`: 329/329 passed;
- exact checker: v0.1 valid with five anchors;
- statement: still 6,177 bytes with the exact SHA-256 above;
- final `make check`: Python doctor, Vault lint, exact checker, 329 tests,
  tracked-file audit, and both diff checks passed;
- final changed-path/MIME/protected/no-game-byte audit: documentation-only
  UTF-8/plain-text paths, zero protected paths, and no statement, authority,
  manifest, implementation, test, asset, original, media, or work diff.

## Verdict

**REJECT.** M4.21 fixes the exact substring counterexamples and improves the
declarative Markdown/generated-row surfaces, but its shell and Python
extractors establish only selected initial syntax, not the effective bindings
or command array after later legal mutations. Its tracked-manifest path also
accepts duplicate declarations. That contradicts M4.21's done condition that
every claimed authority scalar come from one unambiguous/effective
declaration. Passing focused/canonical tests cannot override an independently
reproduced accepted counterexample.

## Exact correction: M4.23

**Name:** Closed-world machine-authority byte pins.

**Bounded question:** Can the asset-free checker use its same existing reads
to require exact SHA-256 for only the five executable or machine-readable
authority files, before retaining the current semantic and scoped declaration
checks, so every observed post-declaration mutation/rebinding and duplicate-
manifest-key ambiguity rejects without building a general Bash/Python
analyzer or changing authority behavior?

**Exact locators and inputs:** immutable M4.21 worker and this audit;
`validate_repository_alignment`, `_validate_recipe_alignment`,
`_require_text`, `_require_shell_assignments`, `_require_launcher_structure`,
and `_require_manifest_contract` in `reimplementation/ablpc/compatibility.py`;
`tests/test_compatibility.py`; exact authority digests:

- `scripts/play-pristine.sh`:
  `68c9171749bd7b207a15b4202193ccfddd2661fbb383deb34b1a5a5a4049977e`;
- `reimplementation/ablpc/manifest.py`:
  `6ed013863347646aa058340576820236334930401d1c92c2d3894002e2fcc4ad`;
- Training manifest:
  `315320bc524986348167ca556b178ef41fe1e8ac961e482610f8f734f34b2434`;
- Level 01 manifest:
  `358998cd326f68fcf7e10593e8ec895915b558252c300464e8fe74177280198f`;
- whole-file manifest:
  `5aaa6e9a4fa79c303ee0920e7f87e00e87bd1dfef412a32c55e36efcc947b607`.

**First pass:** add regressions for exactly six minimized accepted families:
post-validation indexed scalar mutation, post-literal command append, post-
guard game-directory mutation, `globals()` receipt rebinding, validator-name
rebinding, and conflicting duplicate manifest key with expected value last.
Then digest the already-read raw bytes for the five files exactly once and
fail before semantic alignment on any mismatch. Retain the source-aware
checks as explanatory cross-checks and retain the scoped declarative
Environment/Wine/README checks.

**Stop rule:** change only the compatibility checker, its synthetic asset-free
regressions, and required documentation. Do not change statement bytes or
fields, launcher, manifest implementation, tracked manifests, Environment/
Wine/README authority facts, general manifest-loader input policy, schema,
receipt, formats, operations, workflows, apply/stage/compose/remove, assets,
runtime, M2, PS1, mount policy, transaction behavior, or general prose scope.
Do not add another file read or broaden the pin set beyond these five machine
authorities.

**Done when:** the unchanged repository validates; all six minimized accepted
families and the exact four M4.20 attacks reject; the five digests above are
reproduced from the same existing reads; the exact 6,177-byte statement, 126
fields, declarative authority checks, exactly-nine-read asset-free boundary,
focused/canonical M4/M1, Vault/tracked/MIME/protected/no-game-bytes/diff gates
remain green; and one intentional worker commit is ready for fresh-context
review.

## Subsequent disposition

[[EXP-20260814-082 - Closed-world machine-authority byte pins]] completes exact
M4.23 at the worker boundary. The checker hashes only the five listed machine
authorities from their same reads before semantic alignment, and the six
counterexample families in this audit now reject. Direct pins pass 5/5,
focused/full suites pass 47/340, the statement remains exact, and tracing
remains nine asset-free reads. Exact M4.24 is the required independent audit;
this disposition does not erase or weaken the M4.22 rejection.
