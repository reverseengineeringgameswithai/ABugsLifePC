---
type: experiment
id: EXP-20260814-079
date: 2026-08-14
question: Does immutable commit 742b0bf satisfy every exact M4.19 compatibility-statement strictness, evidence-traceability, authority-drift, asset-free, and retained-boundary condition?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; Linux 7.0.11 x86_64; static/read tracing, independent raw-JSON reconstruction, and disposable asset-free mutation copies only
environment_version: Python 3.14.6; pytest 9.1.1; Wine 11.0 Staging; Gamescope 3.16.25-1.fc44.x86_64; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact fresh-context M4.20 audit of immutable commit 742b0bf0bcc0b454cdeebb030a2eb1131ac0ac48 only; documentation-only verdict; no game/original/media/work-copy/PS1 access and no implementation, test, metadata, manifest, Makefile, asset, schema, receipt, operation, workflow, launch, runtime, M2, mount-policy, or transaction change
artifacts:
  - reimplementation/compatibility/m4-v0.1.json
  - reimplementation/ablpc/compatibility.py
  - scripts/check-m4-compatibility.py
  - tests/test_compatibility.py
  - scripts/play-pristine.sh
  - reimplementation/ablpc/manifest.py
  - mods/training-primary-record-124-target-111e4.json
  - mods/level01-primary-record-261-target-3459c.json
  - mods/chars-flick-all-from-chars3-flickd-all.json
addresses: []
file_offsets: []
result: reject-ambiguous-authority-declaration-checks
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - audit/hard-truth
---

# EXP-20260814-079 - Independent M4.19 compatibility-statement hard-truth audit

## Verdict

**REJECT.** Immutable worker commit
`742b0bf0bcc0b454cdeebb030a2eb1131ac0ac48` does publish the claimed canonical
6,177-byte statement, and the checked-in authorities currently agree with it.
The strict object validator, five hash anchors, existing contract fields,
current host/removal boundary, asset-free read set, focused 18/18 tests, and
canonical 311/311 tests all survive independent review.

One exact done claim does not survive: the checker does not reject
representative authority drift for most launcher, implementation, and
environment declarations. In a disposable copy, James inserted
`OUTPUT_WIDTH=1` immediately after the checked `OUTPUT_WIDTH=2560` assignment.
The shell's effective default became 1, but `validate_repository_alignment`
returned success because it requires only that the old text fragment occur
somewhere. Adjacent effective `FILTER=linear` and `_RECEIPT_RELATIVE =
PurePosixPath(".ablpc", "other.json")` overrides, and a contradictory second
kernel row, also passed. This falsifies the M4.19 claim that the checker rejects
representative launcher/implementation/environment authority drift.

Exactly one bounded correction is selected: **M4.21 must make every claimed
authority declaration unambiguous and effective, and add regressions for the
exact override/contradiction class.** It must preserve the statement bytes and
all game-facing/tool behavior. Input-type hardening, generalized prose
consistency, new compatibility claims, and any schema/runtime behavior remain
outside that correction.

## Immutable boundary and mandatory review

The audit began with exact `HEAD`
`742b0bf0bcc0b454cdeebb030a2eb1131ac0ac48`, exact direct parent
`8ddddf4376491d92373a08f9d35f46cbe1c13ebb`, tree
`67dc1bef41655c09e7c52553823acfeb86a840e6`, and a clean worktree. The worker
diff contains 21 paths, 1,355 insertions, and 36 deletions.

Before substantive work, James read in full `AGENTS.md`, [[START HERE]],
[[Current State]], [[Project Roadmap]], [[Environment Status]], [[Decision Log]],
[[Known Unknowns]], the implementation/experiment/reverse-engineering MOCs,
[[Agent Operating Manual]], [[Project Charter]],
[[EXP-20260814-077 - Independent M4.17 mount-order hard-truth audit]],
[[EXP-20260814-078 - Versioned exact M4 compatibility statement]],
[[M4 Exact Whole-file Replacement]], [[M1 Tool Support Matrix]],
[[Wine Linux Play Baseline]], the M4.19 worker session, both READMEs, the exact
worker diff, and every changed/new implementation, test, metadata, checker,
and Makefile path.

No game, executable, original, media, or work-copy source was run, opened, or
inspected. The external PS1 tree was not consulted. All authored attack inputs
lived in disposable `/tmp/ablpc-m420-james-*` trees and were destroyed by their
temporary-directory contexts. No implementation, test, metadata, manifest,
Makefile, asset, schema, receipt, operation, workflow, removal, launch,
runtime, M2, mount-policy, or transaction behavior changed.

## Independent raw statement reconstruction

An independent `json.loads` pass with its own duplicate-key hook and rejected
non-standard constants measured:

- exact size: 6,177 bytes;
- exact SHA-256:
  `c3427d44cf32619a1f9bbcab7c51e67c0846b35d9d53eab7632ff6356c0beaf0`;
- 10 ordered top-level keys and 126 scalar leaves;
- five hash anchors, two formats, four workflows, three tracked recipes,
  three status terms, and seven unsupported declarations;
- canonical UTF-8 JSON equal byte-for-byte to an independent
  `json.dumps(..., indent=2) + "\n"` encoding;
- zero duplicate keys.

The worker validator rejected 17/17 independent declaration-family mutations:
statement schema, statement identity, toolkit version, status vocabulary,
anchor hash, anchor evidence, manifest schemas, format, operation, workflow,
failure policy, receipt path, tracked recipe, tool environment, removal
boundary, Wine/Gamescope scope, and unsupported boundary. It also rejected
missing, malformed, duplicate-key, noncanonical, and directory statement
inputs. A canonical statement reached through a symlink was accepted; this is
recorded as an input-type limitation, not a second M4.21 correction.

## Five anchors and authority/evidence trace

Independent raw parsing reconstructed all five exact paths and hashes:

| Anchor | Path | SHA-256 | Independent tracked authority |
|---|---|---|---|
| PC executable | `bugs.exe` | `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878` | one exact `EXPECTED_EXE_SHA256` assignment in `scripts/play-pristine.sh` |
| Training DAT | `CD/LEVEL07/LEVEL1.DAT` | `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22` | Training tracked manifest destination |
| Level 01 DAT | `CD/LEVEL01/LEVEL.DAT` | `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53` | Level 01 tracked manifest destination |
| `FLICK.ALL` destination | `CD/CHARS/FLICK.ALL` | `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6` | opaque tracked manifest destination |
| `FLICKD.ALL` source | `CD/CHARS3/FLICKD.ALL` | `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4` | opaque tracked manifest replacement source |

The executable hash occurs in `EXP-20260811-001` and `EXP-20260812-007`;
Training path/hash occur in `EXP-20260812-006` and `EXP-20260812-010`; Level
01's exact hash is recorded by `EXP-20260812-013`; and the opaque hashes are
recorded by `EXP-20260812-033` and `EXP-20260814-060`. The Level 01 entry's
`EXP-20260812-006` citation supports the common parser/layout lineage, not the
exact Level 01 identity. Likewise, these five entries are demonstrated
compatibility anchors. They are not a parser allowlist: `load_manifest` still
accepts structurally valid caller-supplied exact hashes outside this metadata
set.

The three manifests independently reproduce their schema, format, operation,
destination path/hash, and opaque source path/hash fields. Static source review
confirms schemas 1/2; `pc-level-dat-prefix-v0` and `opaque-file-v0`; the three
M1 operations and `replace-whole-file`; public apply, stage, compose, and
remove functions; exactly-two-input composition; `.ablpc/receipt.json`; and
the current-Linux mountinfo/listmount/statmount constants. The accepted
M4.18 evidence supplies the fail-closed removal classification and explicit
post-preflight non-transactional limit. These are existing implemented
boundaries, not authority added by the statement.

## Exact host and Wine/launcher scope

The live non-game host commands independently returned:

- `Fedora Linux 44 (Workstation Edition)`;
- kernel `7.0.11-200.fc44.x86_64`;
- architecture `x86_64`;
- Python `3.14.6`;
- `wine-11.0 (Staging)`;
- RPM `gamescope-3.16.25-1.fc44.x86_64`.

The unchanged launcher contains exactly one occurrence each of the executable
hash, derived-work-copy root rule, `OUTPUT_WIDTH=2560`,
`OUTPUT_HEIGHT=1440`, `FILTER=nearest`, Gamescope `640x480`, `fit` scaler, and
manual hardware-selection guidance. [[Wine Linux Play Baseline]] records all
four required positive markers and `INITSOFTRENDER` rejection. The experiments
record the selected Direct3D mode and renderer-start markers; the baseline
normalizes the complete accepted log-marker gate. This audit did not inspect a
game log or infer another Wine, kernel, architecture, filesystem, or platform.

## Authority mutation matrix and falsification

Eleven direct missing/malformed/nonregular or value-replacement attacks were
rejected: missing launcher; malformed Training manifest; destination/source
hash drift in all three manifests; launcher executable-hash drift; manifest
receipt-fragment removal; Environment Python drift; Wine-baseline marker
removal; README checker-path removal; and a launcher directory in place of a
file. These demonstrate that the current checker catches absence and direct
replacement of its expected fragments.

The independently authored falsification used a complete asset-free copy of
the nine checker inputs and changed only:

```sh
OUTPUT_WIDTH=2560
OUTPUT_WIDTH=1
```

The second assignment is the effective shell default before argument parsing,
but `_require_fragments` still finds `OUTPUT_WIDTH=2560`; the checker returned
success. Three adjacent attacks isolated the same defect class and also
returned success:

- `FILTER=linear` immediately after the checked `FILTER=nearest`;
- a second Python assignment changing `_RECEIPT_RELATIVE` immediately after
  the checked receipt assignment;
- a contradictory second `Kernel` authority row after the checked exact row.

The executable-hash declaration alone receives a unique full-line regex check.
The other claimed launcher, manifest-implementation, Environment, Wine, and
README values are generally substring-presence checks. The checked-in sources
are currently consistent; the falsification is specifically that the claimed
drift gate can accept an effective or ambiguous override.

## Asset-free read proof and retained gates

A read-tracing wrapper around the canonical check observed exactly nine unique
reads: statement bytes; three manifest texts; launcher text; manifest
implementation text; Environment Status; Wine baseline; and reimplementation
README. Every resolved path remained inside the repository and none was below
`originals/`, `media/`, or `work/`. Static tracing reaches `load_manifest` only
for the three tracked JSON manifests and does not call prepare/apply/stage/
compose/remove or hash any game path. The focused tests create only synthetic
temporary repositories from those tracked asset-free inputs.

Pre-documentation retained results were:

- focused `tests/test_compatibility.py`: 18/18 passed;
- canonical `tests`: 311/311 passed in 6.66 seconds;
- compatibility checker: v0.1 valid, five anchors;
- Vault lint: 249 notes, zero errors and zero warnings;
- tracked-file audit: zero violations;
- worker and unstaged/staged diff checks: passed;
- exact worker MIME review: Markdown/README/Python/Makefile text and one JSON
  metadata file only;
- protected-path diff: empty; tracked protected roots contain only `.gitkeep`;
- no-game-bytes gate: passed through the tracked-file audit and independent
  path/MIME review.

No unscoped pytest command was used. Normal green tests do not cure the
falsification because no worker regression introduces an expected fragment
followed by an effective competing declaration.

After verdict documentation, final `make check` passed Python doctor, Vault
lint at 251 notes with zero errors/warnings, the five-anchor compatibility
check, canonical 311/311 tests in 6.35 seconds, tracked-file audit at zero
violations, and its staged/unstaged diff checks. Final MIME/protected/no-game-
bytes review found only Markdown/README text in the audit delta, and the
implementation/test/metadata/manifest/Makefile/launcher tree remained
byte-identical to immutable M4.19.

## Limitations

- This was an asset-free statement/checker audit. It did not rerun the game,
  inspect game files/logs, or reconfirm the already accepted runtime outcomes.
- A canonical statement or identical authority reached through a symlink is
  accepted by the loader. Tracked-file/diff review protects the present tree,
  but regular/non-symlink input enforcement is not selected for M4.21.
- The correction is not a generalized natural-language contradiction solver.
  It is confined to unique, effective extraction of the exact declaration
  fields the v0.1 checker claims to align.
- All prior limitations remain: no global hash allowlist, general `.ALL`
  compatibility, other platform scope, N-way/dependency composition, staged/
  source removal, rollback/package/transaction semantics, broad dry-run,
  launch/runtime automation, M2, or PS1 authority.

## Exact correction: M4.21

**Name:** Unambiguous effective compatibility-authority declarations.

**Bounded question:** Can the asset-free checker require one unambiguous,
effective value for every v0.1 authority declaration it claims to align, so
the exact `OUTPUT_WIDTH` override and adjacent launcher/filter,
manifest-receipt, and Environment-row contradictions fail closed while the
unchanged repository remains valid?

**Exact locators and inputs:** immutable M4.19 worker and this audit;
`validate_repository_alignment`, `_require_fragments`, and the executable-hash
uniqueness precedent in `reimplementation/ablpc/compatibility.py`;
`tests/test_compatibility.py`; `scripts/play-pristine.sh`;
`reimplementation/ablpc/manifest.py`; [[Environment Status]];
[[Wine Linux Play Baseline]]; `reimplementation/README.md`; the three tracked
manifests; and the unchanged v0.1 JSON statement.

**First pass:** extract each claimed scalar from a declaration-bearing source
with a source-appropriate exact parser or anchored unique match. Require
exactly one effective launcher assignment, one relevant implementation
assignment/constant, and one authoritative environment row for each claimed
field. Add the exact width override plus filter, receipt, and kernel-row
regressions before generalizing only to the remaining already-claimed fields.
Retain every direct-drift, strict-JSON, manifest, no-game-read, and canonical
test.

**Stop rule:** do not alter the statement bytes or declared scope, manifest
schema/receipt/operations/workflows, apply/stage/compose/remove behavior,
launcher behavior, Environment/Wine facts, README guidance, assets, originals,
work-copy sources, runtime, M2, PS1, mount policy, transaction behavior, or
add broad prose analysis/input-type hardening. Change only checker extraction/
alignment logic and its asset-free regressions plus required documentation.

**Done when:** the unchanged repository still validates; the exact width
falsification and the three adjacent same-class attacks fail; every claimed
authority scalar is obtained from one unambiguous/effective declaration;
17/17 statement-family attacks, all direct authority attacks, strict canonical
JSON, the nine-read no-game boundary, focused/canonical/Vault/tracked/MIME/
protected/no-game-bytes/diff gates remain green; and one intentional worker
commit is ready for fresh-context review.

## Subsequent disposition

[[EXP-20260814-080 - Unambiguous effective compatibility-authority declarations]]
completes exact M4.21 at the worker boundary. The four falsifications above and
adjacent same-class cases now reject through ordered shell, Python-AST,
generated-row, and scoped-Markdown extraction. Final focused/full suites pass
36/329, the statement remains byte-identical, and
the checker still reads exactly nine tracked asset-free inputs. This is not an
independent acceptance; exact fresh-context M4.22 is active.
