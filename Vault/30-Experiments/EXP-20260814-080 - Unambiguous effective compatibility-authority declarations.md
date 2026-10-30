---
type: experiment
id: EXP-20260814-080
date: 2026-08-14
question: Can the asset-free M4 v0.1 checker reject competing effective declarations for every authority scalar it already claims while preserving the exact statement and game-facing behavior?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; Linux 7.0.11 x86_64; asset-free tracked sources and synthetic temporary copies only
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.21 correction only; no statement, authority, manifest, launcher, game, original, media, work-copy, runtime, M2, PS1, mount-policy, transaction, schema, receipt, operation, or workflow change
artifacts:
  - reimplementation/ablpc/compatibility.py
  - tests/test_compatibility.py
  - reimplementation/compatibility/m4-v0.1.json
  - scripts/play-pristine.sh
  - reimplementation/ablpc/manifest.py
addresses: []
file_offsets: []
result: pass-worker-unambiguous-authority-alignment
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/compatibility
---

# EXP-20260814-080 - Unambiguous effective compatibility-authority declarations

## Question

Can exact M4.21 replace substring-only alignment with source-aware extraction
for every authority scalar already claimed by the M4 v0.1 checker, reject the
four M4.20 counterexamples, and retain the exact statement, nine-read asset-
free boundary, and all existing behavior?

## Boundary

The worker began from clean exact audit commit
`e20a44d9c6455f9004026e6f9b17020aae8da809` after the complete required
startup refresh. Only `reimplementation/ablpc/compatibility.py`, its synthetic
tests, and required documentation changed. The following remain byte-exact:

- canonical 6,177-byte `reimplementation/compatibility/m4-v0.1.json`, SHA-256
  `c3427d44cf32619a1f9bbcab7c51e67c0846b35d9d53eab7632ff6356c0beaf0`;
- launcher and all authority values;
- `reimplementation/ablpc/manifest.py` and all three tracked manifests;
- schema, receipt, operations, workflows, apply/stage/compose/remove, mount,
  transaction, and game-facing behavior;
- all original, media, work-copy, runtime, M2, and external PS1 surfaces.

No game file was read or executed. All mutated authority copies are synthetic,
asset-free pytest temporary trees.

## Implementation

**Confirmed at the M4.21 worker boundary:** the checker no longer treats an
expected substring as sufficient evidence of an effective declaration.

- Launcher extraction enumerates the exact ordered assignments to the already-
  claimed executable hash, default/argument/normalization game directory,
  output width and height, and filter. It rejects extra assignments and the
  supported indirect assignment forms. The Gamescope command array separately
  yields one 640x480 game surface and one `fit`/filter pair; the derived-copy
  guard and renderer instruction are anchored uniquely.
- Python AST extraction requires one exact assignment for the receipt path,
  `LISTMOUNT_REVERSE`, statmount masks/order fields, and mountinfo path. It
  derives schemas 1/2, the two existing formats, the three M1 operations, and
  `replace-whole-file` from the relevant validator structures rather than
  from unrelated string literals.
- The Environment authority is limited to the one generated doctor block and
  requires one exact row for Fedora, kernel, architecture, Python, Wine, and
  Gamescope.
- The Wine baseline and reimplementation README are split at unique Markdown
  headings. Existing compatibility declarations use unique keyed lines or
  scoped unique phrases, including output/filter, manual renderer selection,
  all four positive markers, and `INITSOFTRENDER` rejection. This is bounded
  declaration extraction, not general natural-language contradiction solving.

## Regression matrix

The focused suite expands from 18 to 36 passing cases. It first rejects all
four exact M4.20 attacks:

1. `OUTPUT_WIDTH=1` after `OUTPUT_WIDTH=2560`;
2. `FILTER=linear` after `FILTER=nearest`;
3. a second `_RECEIPT_RELATIVE` assignment to `.ablpc/other.json`;
4. a contradictory second generated `Kernel` row.

Adjacent cases reject competing height and game-directory assignments,
parameter-expansion and `unset` writes, extra Gamescope surface/scaler options,
a widened source-root case arm, duplicate mount constants, extra format
declarations, duplicate Wine rows, contradictory Wine-baseline declarations,
and contradictory README compatibility declarations. The prior strict JSON,
17 declaration-family mutation, malformed/noncanonical, direct authority, and
tracked-manifest cases remain present.

## Results

- unchanged repository alignment: pass;
- exact M4 compatibility CLI: v0.1 valid with five anchors;
- focused `tests/test_compatibility.py`: 36/36 passed;
- final canonical scoped `tests`: 329/329 passed;
- read trace: exactly nine reads, exactly the statement, three manifests,
  launcher, manifest implementation, Environment Status, Wine baseline, and
  reimplementation README;
- protected read roots `originals/`, `media/`, and `work/`: zero;
- final `make check`: Python doctor green, Vault lint 253 notes with zero errors
  and zero warnings, five-anchor checker green, 329 tests, tracked-file audit
  zero violations, and both diff checks passed;
- all 18 changed/new paths are Markdown/plain text or Python source;
- protected implementation authorities, manifests, assets, originals, media,
  and work paths have no diff; statement, launcher, and manifest implementation
  hashes remain exact.

## Limitations

- This is a static asset-free alignment correction, not a shell or Python
  security sandbox and not a generalized prose-consistency engine.
- It does not harden symlink/nonregular statement inputs; M4.20 explicitly
  left that outside M4.21.
- It does not add a supported hash, platform, workflow, operation, launch
  automation, dry-run capability, package format, `.ALL` parser, M2 evidence,
  mount policy, rollback, or transaction guarantee.
- Worker success is not independent acceptance. Exact M4.22 must audit the
  immutable commit from fresh context.

## Exact next packet: M4.22

**Name:** Independent M4.21 authority-extraction hard-truth audit.

**Bounded question:** Does immutable M4.21 actually reject every exact M4.20
counterexample and representative adjacent ambiguity for all already-claimed
launcher, Python, Environment, Wine-baseline, README, and manifest authorities,
while the statement, nine-read no-game boundary, and all retained M4/M1 gates
remain exact?

**Exact locators and inputs:** intentional clean M4.21 worker commit and its
direct parent; this experiment; `EXP-20260814-078/079`; exact worker diff;
statement/checker/tests; launcher; manifest implementation; three tracked
manifests; Environment Status; Wine baseline; both READMEs; M4/M1 notes; all
M4.21 stop/done conditions.

**First pass:** independently reconstruct the statement hash/fields and every
claimed authority value without trusting the checker. Reproduce the four exact
rejected attacks, then attack each extraction family with missing, changed,
duplicate, reordered, indirect, or adjacent competing declarations as
applicable. Verify Python-AST semantics, shell assignment/command/guard
boundaries, generated-block scoping, Markdown-section scoping, the three
manifest anchors, exactly nine asset-free reads, and focused/canonical/Vault/
tracked/MIME/protected/no-game-bytes/diff gates.

**Stop rule:** audit only; do not change implementation, tests, metadata,
authorities, manifests, launcher, assets, schema, receipt, operations,
workflows, apply/stage/compose/remove, runtime, M2, PS1, mount policy,
transaction behavior, prose scope, or input-type policy. A rejection records
one exact bounded correction and changes documentation only.

**Done when:** one independent evidence-backed `ACCEPT` or `REJECT` is recorded
across all required Vault/README surfaces in a docs-only commit directly after
the worker; Git is clean. `ACCEPT` selects exactly one remaining written M4
gate/capability or a bounded milestone-closure audit rather than assuming M4
complete. `REJECT` selects exactly one correction with stop/done conditions.

## Subsequent disposition

[[EXP-20260814-081 - Independent M4.21 authority-extraction hard-truth audit]]
returns M4.22 **REJECT**. The four exact M4.20 attacks, scoped declarative
sources, exact statement, 36/329 suites, and nine-read boundary survive, but
standard post-declaration Bash indexed/compound/array writes, Python global or
validator rebinding, and conflicting duplicate tracked-manifest keys remain
accepted. Exact M4.23 is confined to same-read byte pins for the launcher,
manifest implementation, and three tracked manifests; it does not change this
worker's authority values or any game-facing behavior.

[[EXP-20260814-082 - Closed-world machine-authority byte pins]] completes that
bounded M4.23 worker correction. All six residual families now reject by exact
same-read digest while this experiment's source-aware checks remain as cross-
checks. Exact M4.24 still owns independent acceptance.
