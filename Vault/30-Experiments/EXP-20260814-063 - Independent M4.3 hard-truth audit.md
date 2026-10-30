---
type: experiment
id: EXP-20260814-063
date: 2026-08-14
question: Does immutable commit adcceda satisfy every M4.3 deterministic planned-path/type, no-mutation, schema/M1, receipt, and exact-recipe correction condition?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline independent code review, synthetic tests, and user-owned local corpus hash/byte checks
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact fresh-context M4.4 audit of immutable commit adcceda only; no implementation/schema/receipt change, game launch, ALL parsing, compatibility inference, M2 reopening, PS1, or general rollback request
artifacts:
  - reimplementation/ablpc/manifest.py
  - tests/test_manifest.py
  - tests/test_level_dat.py
  - mods/chars-flick-all-from-chars3-flickd-all.json
addresses: []
file_offsets: []
result: accept-deterministic-planned-path-type-preflight-correction
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
  - audit/hard-truth
---

# EXP-20260814-063 - Independent M4.3 hard-truth audit

## Verdict

**ACCEPT.** Immutable clean worker commit
`adccedaba084e5bcd24faf54f5f0c28728ac2f58` survives exact M4.4 review.
Every invalid deterministic planned-destination and fixed-receipt topology
tested by M4.3 fails with `ManifestError` before output mutation, while
ordinary sparse/staged behavior, force replacement of regular files,
schema-1/schema-2 M1
behavior, deterministic receipts, the exact user-owned recipe, and the
asset-free tracked boundary remain intact.

This acceptance is deliberately narrow. It confirms deterministic planned-
path/type preflight, not transaction or rollback behavior for permission or
storage changes, unrelated `copytree`/I/O failures, hardware faults, or
concurrent filesystem races after preflight.

## Audit boundary and immutable inputs

The audit began from a clean tree at exact commit `adcceda`, whose parent is
the M4.2 audit commit `18b4368c115869198368607f14e1904bc26e1e72`.
Before testing, the complete startup sequence, Project Charter, Agent
Operating Manual, M4 roadmap packets, decision and unknown registers,
Implementation/Experiments MOCs, `EXP-20260814-061/062`, [[M4 Exact Whole-file Replacement]], [[M1 Tool Support Matrix]], and the M4.3 session were read.

The immutable diff changes 14 tracked paths. All are text: 13 `text/plain`
files and one Python source file. Review covered `apply_manifest`,
`stage_manifest`, `_write_prepared`, `_safe_output_file`,
`_validate_output_plan`, `_validate_staged_output_plan`,
`_validate_planned_file`, `_resolved_root`, and `_atomic_write` in
`reimplementation/ablpc/manifest.py`, the seven worker regressions, CLI/docs,
the exact manifest, existing M1 tests, and the ignored local corpus. No
original, game file, executable, or runtime state was changed.

## Independent falsification matrix

All topology cases used synthetic bytes inside disposable temporary
directories. Every rejected case snapshotted the complete source and existing
blocker topology before the call, compared it byte/type/link-identically
afterward, and asserted the relevant earlier destination, outside receipt,
fixed receipt, or staged root absent.

### Original M4.2 reproductions: 4/4 pass

1. Existing `output/.ablpc` symlink: rejected before the manifest destination;
   neither the destination nor outside `receipt.json` exists afterward.
2. Later regular-file ancestor `output/B` in a two-destination plan: rejected
   before `A/one.bin`; blocker and source are unchanged and no receipt exists.
3. Later forced directory destination: rejected before the first destination;
   the directory and source are unchanged and no receipt exists.
4. Source `.ablpc` regular file before `stage`: rejected before `copytree`;
   the staged root is absent and the complete source snapshot is unchanged.

### Adjacent topology cases: 22/22 pass

- Requested output root: direct symlink, lexical `missing/../alias` symlink,
  symlinked ancestor, final regular file, and regular-file ancestor all reject
  without mutation or outside creation.
- Planned path: a symlinked destination ancestor, forced final symlink, forced
  final FIFO, and existing regular final destination without `--force` all
  reject with source and blocker topology unchanged.
- Fixed receipt: forced final symlink, forced final directory, and existing
  regular receipt without `--force` all reject before the manifest
  destination. With `--force`, an existing regular receipt is replaced
  successfully and agrees with the returned receipt.
- `--force`: an existing regular manifest destination is replaced
  successfully; directory, symlink, and FIFO destinations remain rejected.
- Stage source: planned-ancestor symlink, planned final symlink, fixed-receipt
  ancestor symlink, and fixed-receipt final directory all reject before the
  staged root exists. An existing regular source receipt is allowed, remains
  unchanged in the source, and is replaced by the generated receipt only in
  the staged tree.
- Requested staged root: lexical-normalized root symlink and regular-file
  ancestor reject without copied output.
- Receipt determinism: a fresh output and a forced output with an existing
  regular receipt emit byte-identical receipt JSON.

The complete independent topology matrix is 26/26. The result supports the
worker's use of lexical normalization plus explicit output-root symlink
inspection, `lstat`-based planned-ancestor/final-type checks, receipt inclusion
in the plan, stage-source topology checks before `copytree`, and receipt
containment defense in `_write_prepared`.

## Compatibility and exact-recipe validation

- Focused manifest/LEVEL suite: 47/47 passed.
- Complete scoped repository suite (`python -m pytest -q tests`): 235/235
  passed in 6.75 seconds.
- Explicit M1 applications: all three operations passed under both schema 1
  and schema 2, 6/6 total, with source preservation and written/returned
  receipt agreement. Each operation's two schema outputs was byte-identical,
  3/3.
- Exact ignored local recipe: both source hashes matched the documented
  `a2f23220...f4ac6` destination and `6e5afb4f...079a4` replacement hashes.
  Two independent sparse outputs were byte-identical to the replacement
  source, contained only `CD/CHARS/FLICK.ALL` and
  `.ablpc/receipt.json`, emitted byte-identical receipts, and left both source
  hashes unchanged. No `.ALL` byte was interpreted.
- Vault lint before audit notes: 217 notes, zero errors, zero warnings. Final
  audit-state lint: 219 notes, zero errors, zero warnings.
- Tracked-file audit: zero violations. `media/` and `originals/` track only
  their `.gitkeep` files; the worker diff contains no executable, `.ALL`,
  `.ANM`, DAT, disc image, dump, VM image, capture, or other game-byte payload.

An initial unscoped `python -m pytest -q` invocation was not a valid full-
suite result: pytest followed ignored Wine-prefix symlinks outside ABLPC and
began collecting external paths. It was terminated, its output was discarded,
and no external source or result contributes to this audit. The evidence above
comes only from the canonical scoped `tests/` command, PC-native implementation
review, synthetic fixtures, and the bounded user-owned local hash/byte recipe.
A read-only external-repository status check afterward showed a dirty working
tree; whether any listed item predated the invalid invocation cannot be
established from this audit. Nothing there was inspected further, cleaned, or
changed intentionally.

## Documentation boundary

The worker-facing README and durable M4/M1/roadmap/decision/unknown notes all
scope the correction to deterministic planned-path/type topology. They
explicitly state that unexpected permissions, storage exhaustion, unrelated
copy/I/O failure, hardware faults, and concurrent races can leave partial
output. Historical references to the rejected M4.1 complete-preflight claim
remain labeled as rejected history. No reviewed surface claims a general
transaction or rollback guarantee.

## Exact next packet: M4.5

**Name:** Deterministic two-manifest composition and byte-conflict report.

**Unmet M4 exit gate:** Two independently created manifests can be composed or
produce a clear, deterministic conflict report.

**Bounded question:** Can exactly two independently authored existing
schema-1/schema-2 manifests be resolved against one immutable source tree and
combined into one existing-schema manifest when their claimed destination
write spans are disjoint, while any overlapping byte claim or opaque whole-
file collision fails before manifest emission with a deterministic asset-free
conflict report?

**Exact locators and inputs:** `build_parser` and `main` at
`reimplementation/ablpc/cli.py:20-110`; `load_manifest`, `_prepare_manifest`,
`_validate_manifest`, `_apply_level_dat_edits`, `_validate_output_plan`, and
`_write_prepared` in `reimplementation/ablpc/manifest.py`; `SceneRecord.offset`,
`PayloadTargetReference`, `set_record_payload_target_offset`,
`set_record_position`, and `set_record_field_0c` at
`reimplementation/ablpc/level_dat.py:37-54,322-424`; existing tests in
`tests/test_manifest.py` and `tests/test_level_dat.py`; same-file disjoint
tracked inputs `mods/training-primary-record-124-target-111e4.json` and
`mods/training-primary-record-125-field-0c-zero.json`; different-file schema-2
input `mods/chars-flick-all-from-chars3-flickd-all.json`; and synthetic
same-byte/opaque-file collision fixtures.

**First pass:** add `compose LEFT RIGHT --source-root ROOT` for exactly two
input manifests. Verify both independently against the same exact source bytes;
normalize Windows paths and source hashes; canonicalize input order independent
of CLI argument order by validated canonical-JSON digest; and derive half-open
claimed write spans only from the existing offset-located operations
(`position`: 12 bytes, `field-0c`: 2 bytes, payload-target field: 4 bytes,
opaque replacement: the whole destination).
Merge same-file entries only when format/hash agree and spans are disjoint;
select schema 2 iff either input is schema 2; derive the combined manifest name
from the ordered canonical-input digest; sort files/edits canonically; and emit
the existing-schema combined manifest as deterministic JSON on stdout.
Reject any overlapping span, opaque replacement sharing a destination, case-
insensitive collision, existing replacement-source/destination collision,
source-hash/format/path mismatch, or unsupported edit before manifest emission;
leave stdout empty on failure. The stderr conflict report must be deterministic
JSON that canonically names both input manifests, the normalized destination,
and exact half-open overlapping span without game bytes. Prove that saving the
emitted JSON and applying/staging it produces expected bytes and the ordinary
receipt through the accepted M4.4 path, while single-manifest behavior remains
unchanged.

**Stop rule:** do not accept more than two input manifests, add an arbitrary
dependency/order solver, reinterpret semantic fields, change existing schema
or receipt fields, add a general dry-run/removal/launch capability, parse
`.ALL`, infer compatibility or identity, launch the game, reopen M2, or consult
PS1. Stop and record one exact blocker if deterministic composition requires
one of those expansions.

**Done condition:** synthetic disjoint same-file and different-file pairs
compose byte-identically under reversed input order; applying and staging the
combined existing-schema manifest matches independently calculated byte-local
results with source preservation; overlapping M1 spans and any opaque same-
destination pair yield byte-identical deterministic conflict reports, empty
stdout, and no filesystem output; existing focused/full, schema-1/schema-2 M1,
exact replacement, receipt, topology, Vault, and
no-game-bytes gates remain green; docs state the exact two-manifest limit; the
worker records an intentional commit and clean tree for independent M4.6.
