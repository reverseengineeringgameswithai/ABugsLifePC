---
type: experiment
id: EXP-20260814-101
date: 2026-08-14
question: Does immutable M4.41 bind each selected compatibility-statement pathname to its declared version while preserving the complete accepted M4 evidence ledger?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; tracked-only disposable repository copy and asset-free documentation/tests
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: fresh-context exact M4.42 audit of immutable M4.41 worker 8a284733063e57efb83781ab0f39e998ed495cf0 with direct M4.40 parent b5a8019082ee6f40930cce2984e424205c8b9ff3; documentation-only verdict; no game execution or protected/game-file reads
artifacts:
  - reimplementation/ablpc/compatibility.py
  - scripts/check-m4-compatibility.py
  - tests/test_compatibility.py
  - reimplementation/compatibility/m4-v0.1.json
  - reimplementation/compatibility/m4-v0.2.json
  - Vault/30-Experiments/EXP-20260814-086 - M4 v0.1 milestone-closure evidence audit.md
  - Vault/30-Experiments/EXP-20260814-092 - Independent M4.32 receipt-chain-closure hard-truth audit.md
  - Vault/30-Experiments/EXP-20260814-097 - Independent M4.37 complete-tree-uniqueness hard-truth audit.md
  - Vault/30-Experiments/EXP-20260814-099 - Independent M4.39 statement and milestone-closure hard-truth audit.md
  - Vault/30-Experiments/EXP-20260814-100 - Version-bound canonical compatibility-statement strictness.md
addresses: []
file_offsets: []
result: reject-selected-active-path-resolution-collapse
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/compatibility
  - audit/hard-truth
  - milestone/m4
---

# EXP-20260814-101 - Independent M4.41 selected-path identity hard-truth audit

## Verdict

**REJECT.** Immutable M4.41 closes the exact regular-file counterexamples from
M4.40, but it does not bind the default active pathname to v0.2 when the two
selected paths resolve to one target. In a tracked-only disposable export, the
canonical active `m4-v0.2.json` pathname was replaced by a relative symbolic
link to the canonical historical `m4-v0.1.json`. The default checker followed
that link and returned status 0 with:

`M4 compatibility statement valid: ablpc-m4-compatibility-v0.1 (5 hash anchors)`

Stderr was empty. The selected active pathname therefore admitted the complete
historical contract even though M4.41 claims that pathname requires v0.2.

M4 remains active. This result does not reopen `KU-051` or `KU-052`, weaken the
accepted manifest-driven current-Linux lifecycle, or change either statement,
authority, pin, read boundary, manifest behavior, or game-facing behavior.

## Immutable linkage and boundary

- audited worker: `8a284733063e57efb83781ab0f39e998ed495cf0`;
- required direct parent: `b5a8019082ee6f40930cce2984e424205c8b9ff3`;
- initial tree: clean;
- worker diff: 16 paths, 555 insertions, 44 deletions;
- verifier changes: Markdown/README documentation only; and
- no executable, original, media, work-copy, runtime, PS1, or game byte was
  read or executed.

The complete startup packet, exact M4.42 Roadmap entry, full Decision Log and
Known Unknowns, relevant MOCs, operating/charter/environment policy, M4.27
ledger, accepted M4.33 and M4.38 evidence, EXP-099/100, M1/M4 notes, worker
session, both READMEs, both statements, complete compatibility/checker/test
files, and the exact worker diff were reviewed before the disposition.

## Independent statement and authority reconstruction

| Contract | Bytes | SHA-256 | ID / toolkit | Ordered objects | Scalar leaves |
|---|---:|---|---|---:|---:|
| historical v0.1 | 6,177 | `c3427d44cf32619a1f9bbcab7c51e67c0846b35d9d53eab7632ff6356c0beaf0` | `ablpc-m4-compatibility-v0.1` / `0.1` | 19 | 126 |
| active v0.2 | 7,677 | `dacfcab8c1d27e5a63db870f347eb08701f868ca678cafdd178913266f20ccb2` | `ablpc-m4-compatibility-v0.2` / `0.2` | 21 | 151 |

Both byte streams are canonical UTF-8 JSON with a final newline and equal the
independently decoded expected contracts. The complete ordered-object path/key
records hash to `eda2c5f31d4dd3473107727016b1491514829c924e93bdb1b0417877460ec641`
for v0.1 and `f7cbd437e616882a9679fc1b39875fa52e9381c76d82b2044eeeb7dcc347240f`
for v0.2. Their semantic delta remains exactly the statement/toolkit versions,
one appended `restore` workflow, one evidence-cited `restoration_boundary`,
and the restoration-specific split/expansion of unsupported declarations.

All five machine-authority pins independently match:

| Authority | SHA-256 |
|---|---|
| `mods/training-primary-record-124-target-111e4.json` | `315320bc524986348167ca556b178ef41fe1e8ac961e482610f8f734f34b2434` |
| `mods/level01-primary-record-261-target-3459c.json` | `358998cd326f68fcf7e10593e8ec895915b558252c300464e8fe74177280198f` |
| `mods/chars-flick-all-from-chars3-flickd-all.json` | `5aaa6e9a4fa79c303ee0920e7f87e00e87bd1dfef412a32c55e36efcc947b607` |
| `scripts/play-pristine.sh` | `68c9171749bd7b207a15b4202193ccfddd2661fbb383deb34b1a5a5a4049977e` |
| `reimplementation/ablpc/manifest.py` | `b3480761ac2b4791ccbf1df69f88234532f27956152045b89615dd5ec5bf6d75` |

## Discriminating selected-path case

`check_compatibility_statement` resolves the requested path, then resolves
both selected repository paths and takes the first matching expected ID. With
the active pathname linking to the historical pathname, both map entries
resolve to the historical target. The historical entry occurs first, so the
default active request is assigned expected v0.1 and the linked historical
bytes pass repository alignment.

The disposable input changed no statement content and no authority content.
This is not an arbitrary unselected-path case: the request used the checker's
own default active pathname. Regular-file active/historical replacement,
recursive object order, non-string ID normalization, canonical input, exact
pins, normal nine-read behavior, and the worker's 71/284/472 results remain
valuable retained evidence, but they cannot establish selected-path identity
for this case.

## Complete M4 ledger reconciliation

The accepted later evidence closes both gaps identified by M4.27:

- receipt sufficiency is supported at the strict current-receipt boundary by
  exact M4.33 / `EXP-20260814-092`; and
- one same-tree install, validation, launcher-readiness, and restoration
  lifecycle is supported only at the manifest-driven current-x86_64-Linux
  boundary by exact M4.38 / `EXP-20260814-097` and strict v0.2.

Every M4.27 required-capability row was reconciled against accepted later
evidence:

| Required capability | M4.42 disposition and exact boundary |
|---|---|
| Inspect supported formats and executable/data compatibility | **Supported, bounded.** `EXP-20260814-063/083`; prefix-only LEVEL, read-only bounded ANM, and opaque unparsed replacement remain explicit. |
| Compose declarative manifests and detect conflicting byte/field edits | **Supported.** `EXP-20260814-067`; exactly two inputs, byte-span conflict reporting, and no semantic/N-way solver. |
| Validate exact input hashes and supported format versions | **Supported.** `EXP-20260814-063/083`; schemas 1/2 and the four declared operations only. |
| Dry-run affected files, records, and byte ranges | **Supported, bounded.** `EXP-20260814-085`; one existing manifest, no persisted report/output simulation/receipt. |
| Stage a complete work copy or sparse overlay without touching originals | **Supported.** `EXP-20260814-063`; deterministic preflight with non-transactional post-preflight limits. |
| Launch the tested Wine/Gamescope configuration | **Supported, manually gated.** `EXP-20260812-007/029` and `EXP-20260814-083`; exact Fedora/Wine/Gamescope declarations, manual renderer choice/log acceptance. |
| Emit receipts sufficient to reproduce and remove a mod | **Supported at the strict current-receipt sparse boundary.** `EXP-20260814-092`; no provenance/signature, staged-tree removal, or external-receipt full-tree restoration claim. |
| Test parsers with synthetic fixtures and a user-owned local corpus | **Supported.** `EXP-20260814-063/067/077/097`; tracked fixtures plus recorded user-owned local gates, with no game bytes in CI. |
| Document limitations, unsupported fields, and runtime scope | **Open.** Both statements remain exact, but this experiment proves that the selected active pathname can successfully report historical v0.1. |

Every M4.27 exit gate was likewise reconciled:

| Exit gate | M4.42 disposition and exact boundary |
|---|---|
| At least two useful mod classes, including one beyond simple scene-position editing | **Supported.** `EXP-20260812-010/033` and `EXP-20260814-063`; guarded payload rebind plus exact opaque replacement. |
| Two independently created manifests compose or produce a deterministic conflict | **Supported.** `EXP-20260814-067`; exact two-input boundary only. |
| Install, validation, launch, and removal from one clean derived work copy | **Supported at the manifest-driven current-x86_64-Linux boundary.** `EXP-20260814-097`; exact-source `stage`, pinned-launcher dry-run validation, and same-tree `restore`, without game execution automation. |
| No original binary, asset, disc image, dump, or machine state is packaged | **Supported.** `EXP-20260814-083/085/097` plus tracked/protected/no-game-byte gates; user-owned outputs remain undistributable. |
| A versioned compatibility statement names supported hashes and Wine scope | **Open.** The contents and authorities remain exact, but selected active-path identity is not strict. |

The resulting ledger is eight of nine required capabilities and four of five
exit gates. Passing retained suites cannot close either open row while the
selected-path counterexample survives.

## Retained validation and hygiene

The immutable worker records 71/71 focused compatibility, 284/284 exact
compatibility + manifest + LEVEL, and 472/472 canonical tests. The audit's
normal `make check` reruns the canonical asset-free suite: Python doctor is
green, Vault lint reports 295 notes with zero errors/warnings, active v0.2
reports five anchors, 472/472 tests pass, tracked-file audit reports zero
violations, and diff checks pass. Final diff/MIME/protected/no-game-byte and
clean-tree gates pass on the documentation-only verdict commit. No unscoped
pytest command or launcher invocation was used.

## Sole successor: M4.43

**Name:** Lexical selected-statement identity and non-link file correction.

**Bounded question:** Can the checker determine v0.1/v0.2 from the selected
lexical repository pathname before following file content, and require both
selected statement files themselves to be regular non-link files, while
preserving statement bytes, authorities, exact pins, normal nine-read behavior,
arbitrary otherwise-valid unselected paths, and every game-facing behavior?

**Exact locators:** `HISTORICAL_STATEMENT_RELATIVE`, `STATEMENT_RELATIVE`,
`EXPECTED_STATEMENT_ID_BY_RELATIVE_PATH`, `load_compatibility_statement`, and
`check_compatibility_statement` in `reimplementation/ablpc/compatibility.py`;
selection in `scripts/check-m4-compatibility.py`; selected-path and read-count
cases in `tests/test_compatibility.py`; both exact statements; and this
experiment.

**First pass:** derive the expected version from the normalized lexical path
under the lexical repository root before any final-target resolution. For each
of the two selected paths, require final no-follow metadata to identify a
regular, non-link statement file before reading. Add synthetic active-link and
historical-link refusals plus normal active/historical path regressions with
status 2, empty stdout, deterministic stderr, and no traceback. Retain normal
one-statement-plus-eight-authority reads and arbitrary otherwise-valid
unselected statement paths.

**Stop rule:** do not change either statement, a machine pin or authority,
manifest/receipt/schema/format/operation behavior, launcher, asset/runtime,
M1/M2/PS1, platform/restoration scope, unsupported declaration, or any game-
facing behavior. Do not add a general signature, filename policy, arbitrary-
path link policy, or broader filesystem claim. Do not mark M4 complete at the
worker edge or select another successor.

**Done when:** both selected-path link directions refuse before statement
content validation; normal selected v0.1/v0.2 and arbitrary unselected exact
contracts retain their documented behavior; recursive-order, typed-ID,
canonical-input, authority, exact-five-pin, and normal nine-read regressions
pass; focused/combined/canonical and hygiene gates pass; and one clean bounded
worker commit is ready for fresh-context review.

## Worker disposition

[[EXP-20260814-102 - Lexical selected-statement identity and non-link admission]]
completes exact M4.43 at the worker boundary. Both selected link directions
refuse before reads; arbitrary unselected exact links retain prior behavior;
exact suites pass 75/288/476. Statements, pins, authorities, and all behavior
remain unchanged. Independent M4.44 owns final acceptance and M4 disposition.
