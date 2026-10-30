---
type: experiment
id: EXP-20260814-078
date: 2026-08-14
question: Can one strict asset-free M4 v0.1 statement name exact demonstrated hashes, operations, current-Linux removal prerequisites, and tested Wine/Gamescope scope without claiming unsupported compatibility?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; Linux 7.0.11 x86_64; asset-free static metadata and synthetic consistency tests only
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.19 worker packet only; no game execution or game-file reads; no manifest schema, receipt, operation, apply, stage, compose, remove, launch, runtime, M2, PS1, mount-policy, or transaction change
artifacts:
  - reimplementation/compatibility/m4-v0.1.json
  - reimplementation/ablpc/compatibility.py
  - scripts/check-m4-compatibility.py
  - tests/test_compatibility.py
  - Makefile
  - mods/training-primary-record-124-target-111e4.json
  - mods/level01-primary-record-261-target-3459c.json
  - mods/chars-flick-all-from-chars3-flickd-all.json
addresses: []
file_offsets: []
result: worker-complete-versioned-exact-compatibility-statement
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/compatibility
---

# EXP-20260814-078 - Versioned exact M4 compatibility statement

## Bounded question

Can exact M4.19 publish one versioned, machine-checkable, asset-free M4 v0.1
compatibility statement that names the demonstrated executable and input hash
anchors, existing manifest schemas/formats/operations, current-x86_64-Linux
removal prerequisites, and tested Wine/Gamescope scope while explicitly
separating demonstrated, fail-closed, and unsupported boundaries?

The executable hash scopes the project, but `bugs.exe` was not inspected or
run. Neither the checker nor its tests read `originals/`, `media/`, `work/`, or
any game file. The external PS1 repository was not consulted.

## Statement and evidence boundary

**Confirmed at the M4.19 worker boundary:**
`reimplementation/compatibility/m4-v0.1.json` is canonical strict JSON with
statement schema version 1 and toolkit version `0.1`. It is 6,177 bytes and has
SHA-256
`c3427d44cf32619a1f9bbcab7c51e67c0846b35d9d53eab7632ff6356c0beaf0`.
It contains identifiers, versions, paths, hashes, capability labels, evidence
IDs, and limitations only; it contains no source payload or output bytes.

Five entries are deliberately called demonstrated hash **anchors**, not a
global parser allowlist:

| Anchor | Path | SHA-256 | Independent tracked authority |
|---|---|---|---|
| PC executable | `bugs.exe` | `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878` | `scripts/play-pristine.sh`; `EXP-20260811-001`, `EXP-20260812-007` |
| Training DAT | `CD/LEVEL07/LEVEL1.DAT` | `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22` | tracked Training manifest; `EXP-20260812-006/010` |
| Level 01 DAT | `CD/LEVEL01/LEVEL.DAT` | `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53` | tracked Level 01 manifest; `EXP-20260812-006/013` |
| opaque destination | `CD/CHARS/FLICK.ALL` | `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6` | tracked replacement manifest; `EXP-20260812-033`, `EXP-20260814-060` |
| opaque source | `CD/CHARS3/FLICKD.ALL` | `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4` | tracked replacement manifest; same evidence |

The manifest contract names schemas 1/2; `pc-level-dat-prefix-v0` with the
three existing M1 operations; `opaque-file-v0` with only
`replace-whole-file`; exact two-input composition; sparse apply, full-tree
stage, and receipt-validated sparse removal. It neither changes nor wraps the
existing manifest implementation.

The tool host is recorded exactly as Fedora Linux 44 Workstation, kernel
`7.0.11-200.fc44.x86_64`, architecture `x86_64`, and Python 3.14.6. Removal is
separately scoped to the accepted current-x86_64-Linux boundary with readable,
consistent `/proc/self/mountinfo`, `listmount(2)` reverse order, and
`statmount(2)` mapping. Any unavailable/inconsistent topology view is labeled
fail-closed. The statement retains the post-preflight non-transactional limit.

The launch scope records Wine 11.0 Staging, Gamescope
3.16.25-1.fc44.x86_64, the derived `work/copies` policy, `R:\PC\BUGS`, the
640x480 game surface, 2560x1440 default output, `fit`/`nearest`, manual Down-
then-confirm hardware selection, all four accepted positive Direct3D log
markers, and rejection of `INITSOFTRENDER`. This is a description of the
tested baseline, not new launch automation or evidence for other systems.

## Strict checker and drift matrix

`reimplementation/ablpc/compatibility.py` accepts only the exact typed v0.1
object and canonical UTF-8 JSON encoding. It rejects duplicate keys,
non-standard JSON constants, unknown/missing/reordered fields or list items,
changed versions/hashes/schemas/formats/operations/statuses/environments, and
changed unsupported declarations. It then cross-checks only tracked asset-free
authorities:

- the executable hash and launcher defaults in `scripts/play-pristine.sh`;
- exact destination/source paths and hashes, schemas, formats, and operations
  in the three declared manifests;
- schema/format/operation/receipt and current-Linux interface declarations in
  `reimplementation/ablpc/manifest.py`;
- Fedora/kernel/architecture/Python/Wine/Gamescope rows in [[Environment Status]];
- Wine/renderer statements and all four positive plus one negative log markers
  in [[Wine Linux Play Baseline]] and `reimplementation/README.md`.

`scripts/check-m4-compatibility.py` exposes the check directly, and
`make m4-compatibility` plus `make check` run it. The checker does not hash or
open the user-owned anchor files; it validates their published identifiers
against the tracked manifest/launcher evidence.

The new focused suite passes 18/18. Negative cases cover root/version/hash,
schema/operation/status/architecture/Wine/unsupported drift, duplicate JSON
keys, noncanonical encoding, and independent launcher/manifest/environment/
README authority drift. The statement bytes are also bounded below 16 KiB and
required to equal the independently encoded expected metadata exactly.

## Validation

- `python -m pytest -q tests/test_compatibility.py`: 18 passed;
- `python scripts/check-m4-compatibility.py`: exact v0.1 valid, five anchors;
- canonical `python -m pytest -q tests`: 311 passed;
- Python compilation of the checker/module/test: passed;
- final `make check`: Python doctor passed, Vault lint 249 notes with zero
  errors/warnings, compatibility check passed, 311 tests passed, tracked-file
  audit zero violations, and staged/unstaged diff checks passed.

No unscoped pytest command was used. MIME/protected-path/no-game-bytes and
clean-tree commit verification are the remaining closing gates recorded in
the session note.

## Limitations

- An unlisted game hash is not declared demonstrated by v0.1; this does not
  redefine the manifest parser as a five-hash allowlist.
- Apply/stage/compose remain the existing exact-hash tool behavior. Only
  removal carries the declared current-Linux syscall/mount-topology boundary.
- The Wine/Gamescope fields record one tested presentation. They establish no
  native-Windows, other-Wine, other-kernel/architecture/filesystem, or period-
  hardware compatibility.
- Removal is non-transactional after preflight. Staged/source removal,
  restoration, package/backup/trash/rollback/general transaction behavior,
  N-way composition, cross-input dependency resolution, `.ALL` parsing,
  general dry-run/launch/runtime automation, M2, and PS1 remain unsupported or
  outside this packet.

## Exact next packet: M4.20

**Name:** Independent M4.19 compatibility-statement hard-truth audit.

**Bounded question:** Does one fresh-context verifier independently confirm
that the immutable M4.19 worker statement is strict, asset-free, evidence-
traceable, and no broader than the accepted hash/schema/current-Linux/Wine
boundaries, while its checker rejects representative metadata and authority
drift?

**Exact locators and inputs:** immutable clean M4.19 worker commit and parent;
this experiment; `reimplementation/compatibility/m4-v0.1.json`;
`reimplementation/ablpc/compatibility.py`; checker/tests/Makefile; the three
tracked manifests; `scripts/play-pristine.sh`; [[Environment Status]];
[[Wine Linux Play Baseline]]; [[M1 Tool Support Matrix]]; [[M4 Exact Whole-file Replacement]];
`EXP-20260814-077`; both READMEs; exact worker diff.

**First pass:** independently parse and enumerate the raw statement without
trusting its checker; cross-check all five paths/hashes and every schema/
format/operation/workflow/status/environment/Wine/removal/unsupported field
against tracked metadata and accepted evidence; independently mutate at least
one field in each declaration family plus the asset-free authorities; prove
the checker does not read game roots; run focused/canonical/Vault/tracked/MIME/
no-game-bytes gates; then return one verdict.

**Stop rule:** do not modify implementation, tests, metadata, manifests,
assets, originals, work-copy sources, schema, receipt, operation, apply/stage/
compose/remove behavior, launch/runtime, M2, PS1, mount policy, or transaction
behavior. The verifier may update only required documentation/README verdict
surfaces in one intentional commit. On `REJECT`, select exactly one bounded
statement/checker correction. On `ACCEPT`, select exactly one successor from a
still-unmet written M4 exit gate/capability; do not infer M4 completion merely
from this one exit gate.

**Done when:** the immutable worker has an evidence-backed `ACCEPT` or one-
correction `REJECT`, all audit artifacts are asset-free and disposable, every
required Vault surface records the verdict and sole successor, validation is
green, and Git is clean.

## Subsequent disposition

[[EXP-20260814-079 - Independent M4.19 compatibility-statement hard-truth audit]]
returns M4.20 **REJECT**. The statement bytes, five anchors, current tracked
authorities, strict JSON/declaration-family mutation behavior, nine-read no-
game boundary, focused 18/18, and canonical 311/311 gates survive. The rejected
claim is representative authority-drift detection: effective launcher width/
filter and manifest receipt overrides, plus a contradictory Environment row,
remain accepted while the expected substrings are still present. Exact M4.21
is confined to unambiguous/effective authority extraction and regressions; it
does not change this statement, any authority value, or game-facing behavior.

[[EXP-20260814-080 - Unambiguous effective compatibility-authority declarations]]
now completes that M4.21 correction at the worker boundary. Ordered shell,
Python-AST, generated-row, and scoped-Markdown extraction rejects the exact
four M4.20 contradictions and adjacent same-class ambiguity. The statement
remains the same 6,177 bytes and SHA-256; exact M4.22 must independently audit
the immutable worker.

[[EXP-20260814-098 - Strict v0.2 restoration compatibility statement]] later
preserves this v0.1 artifact byte-for-byte at the same 6,177-byte SHA-256 and
publishes a separate strict v0.2 file. v0.2 adds only the independently
accepted current-Linux manifest/source-authenticated restoration boundary;
the five anchors/pins and nine-read asset-free contract remain exact. v0.1 is
historical evidence rather than rewritten current metadata.
