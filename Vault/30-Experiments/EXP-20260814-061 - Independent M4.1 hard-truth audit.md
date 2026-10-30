---
type: experiment
id: EXP-20260814-061
date: 2026-08-14
question: Does immutable commit 7879db6 satisfy every declared M4.1 schema, hash, preflight, containment, locality, receipt, compatibility, and distribution condition?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline independent code review, synthetic tests, and user-owned local corpus check
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: M4.2 audit of immutable commit 7879db6 only; no implementation change, game launch, ALL parsing, compatibility inference, PS1, or game-byte distribution
artifacts:
  - reimplementation/ablpc/manifest.py
  - tests/test_manifest.py
  - tests/test_level_dat.py
  - mods/chars-flick-all-from-chars3-flickd-all.json
  - work/mod-builds/M4-2-audit-overlay-20260814/.ablpc/receipt.json
addresses: []
file_offsets: []
result: reject-incomplete-output-plan-preflight-and-receipt-containment
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
  - audit/hard-truth
---

# EXP-20260814-061 - Independent M4.1 hard-truth audit

## Verdict

**REJECT.** Immutable clean worker commit
`7879db6f3d2d6a89d9448282fdcdc1c7e6d546d5` does not satisfy M4.1's declared
complete-preflight and output-containment conditions. The schema, exact-hash,
ordinary sparse/staged locality, deterministic receipt, M1 compatibility,
exact local recipe, and no-game-bytes results survive, but one bounded output-
plan defect permits a receipt write outside the requested output root and
permits deterministic late failures after earlier output mutation.

## Audit boundary and method

The audit began from a clean tree at exact commit `7879db6`. The complete
required startup sequence, `DEC-20260814-055`, exact M4.1/M4.2 roadmap packets,
`EXP-20260814-060`, [[M4 Exact Whole-file Replacement]],
[[M1 Tool Support Matrix]], `EXP-20260812-033`, and `EXP-20260813-049` were
read before testing.

Review covered the schema, implementation, CLI, documentation, tracked exact
manifest, synthetic tests, source/destination hash and collision handling,
source/output root containment, sparse/staged writes, receipts, schema-1 and
schema-2 M1 behavior, the ignored local corpus, and the commit's tracked-file
boundary. No original, executable, source asset, or runtime state was changed.
No game was launched, no `.ALL` byte was interpreted, and no PS1 evidence was
consulted.

## Validation reproduced

- Focused manifest/LEVEL tooling: 40 tests passed.
- Complete repository suite: 228 tests passed.
- Vault lint before audit edits: 213 notes, zero errors, zero warnings; final
  audit-state lint: 215 notes, zero errors, zero warnings.
- Tracked-file audit before and after audit edits: zero violations.
- Independent schema-2 synthetic application of all three existing M1
  operations: 3/3 passed with source preservation.
- Ignored local exact recipe: both source-tree hashes matched the documented
  destination and replacement hashes; sparse output contained only
  `CD/CHARS/FLICK.ALL` and `.ablpc/receipt.json`; output equaled the
  replacement source; both source-tree files remained unchanged; both output
  files were ignored by `/work/mod-builds/`.
- Commit-content audit: every path added or changed by `7879db6` is text; the
  commit adds no game executable, `.ALL`, `.ANM`, DAT, disc image, memory
  dump, virtual disk, or other game-byte payload.

These checks independently support the worker's exact manifest hashes,
byte-exact ordinary output, deterministic receipt fields/order, source
preservation on the demonstrated recipe, strict schema-1 rejection of the new
format, schema-2 retention of all three M1 operations, CLI documentation, and
asset-free distribution claims.

## Concrete falsification

All four reproductions used only synthetic bytes in temporary directories.
They identify one defect: the implementation does not preflight the complete
planned output topology, including the fixed receipt and every destination
ancestor, before it starts writing.

### 1. Fixed receipt escapes through an existing symlink

With a valid one-entry schema-2 manifest, a safe source tree, an existing
output root, and `output/.ablpc` symlinked to an outside directory,
`apply_manifest` returned success, wrote the replacement destination inside
the output, and wrote `receipt.json` into the outside directory. The outside
receipt SHA-256 was
`a9772bfff225076cbacdc5a03be25bccd7ab0cd957162062e28bbc78fb21e4d7`.

The load-bearing code is exact:

- `apply_manifest` preflights only prepared manifest destinations at
  `reimplementation/ablpc/manifest.py:55-58`;
- `_validate_output_destinations` calls `_safe_output_file` only for those
  destinations at lines 427-433;
- `_write_prepared` constructs fixed path `.ablpc/receipt.json` at line 213
  and passes it directly to `_atomic_write` at line 214; and
- `_atomic_write` follows/uses the parent at lines 461-470 without applying
  `_safe_output_file` or an equivalent containment check.

This contradicts output symlink containment and the claim that sparse output
writes only inside the requested root.

### 2. A later destination-parent blocker leaves an earlier file written

A valid two-entry schema-2 manifest used destinations `A/one.bin` and
`B/two.bin`. The existing output contained a regular file at `B`, so the
second destination's parent could not be created. `_validate_output_destinations`
accepted the whole plan because `B/two.bin` itself did not exist. Application
then wrote `A/one.bin`, raised raw `FileExistsError` for `B`, left the first
replacement in place, and emitted no receipt.

This contradicts the declared complete preflight and late-failure atomicity.
It also demonstrates that the problem is not limited to the reserved receipt
path.

### 3. A staged receipt-parent blocker leaves a changed staged tree

A valid source tree containing a regular file at `.ablpc` passed manifest/hash
preflight. `stage_manifest` copied the tree, changed the destination, then
raised raw `FileExistsError` while trying to create
`.ablpc/receipt.json`. The staged tree remained present with the replacement
already applied and no receipt. The original source destination remained
unchanged.

The exact order is `copytree` at line 77 followed by `_write_prepared` at line
78. This contradicts the claimed staged complete-preflight boundary.

### 4. `--force` accepts a directory destination and fails after an earlier write

A valid two-entry schema-2 apply used `--force` with the second destination
already present as a directory. `_validate_output_destinations` accepted it
because `force=True` bypasses the only existence rejection without checking
file type. Application wrote the first destination, then `os.replace` raised
raw `IsADirectoryError` at the second. The first replacement remained, the
directory remained, and no receipt existed.

This is the force-mode instance of the same incomplete output-plan preflight,
not a separate feature request.

## Claims that survive the audit

**Confirmed:** schema 2 is strict and retains schema 1; both exact file hashes
are checked before ordinary output; replacement sources escaping the source
root through a symlink are rejected; lexical protected roots, unsafe manifest
paths, case-insensitive same paths, duplicate destinations, and a replacement
source colliding with any manifest destination are rejected; the ordinary
new-output sparse/staged and receipt cases are byte-exact and deterministic;
all three M1 operations work under schema 2; the tracked exact local recipe
resolves and applies; and commit `7879db6` distributes no game bytes.

**Not confirmed:** complete output-plan preflight, output receipt containment,
or no-partial-output behavior for deterministic destination/receipt topology
failures. These are declared M4.1 done conditions, so the surviving claims do
not permit `ACCEPT`.

## Exact corrective packet: M4.3

**Name:** Complete planned-output containment preflight correction.

**Exact locators and inputs:** immutable worker commit `7879db6`;
`apply_manifest` lines 38-58; `stage_manifest` lines 61-78;
`_write_prepared` lines 201-215; `_safe_output_file` and
`_validate_output_destinations` lines 417-433; `_atomic_write` lines 461-473;
the four synthetic reproductions above; existing tests in
`tests/test_manifest.py` and `tests/test_level_dat.py`; and the exact ignored
local manifest/corpus check from this audit.

**Bounded question:** Can `apply` and `stage` validate containment and the
deterministically writable filesystem topology of every planned destination
plus `.ablpc/receipt.json` before any output mutation, while retaining the
exact schema-2 replacement, schema-1/schema-2 M1 behavior, and local recipe?

**First pass:** build one complete output plan before writing. Validate the
fixed receipt with the same or stronger containment rules as manifest
destinations; reject symlinked or non-directory ancestors, directory/symlink
destinations even under `--force`, and stage-source topology that would make
the copied receipt path unwritable. Add regressions for the outside-receipt
symlink, later destination-parent blocker, forced directory destination, and
staged `.ablpc` blocker, with
explicit assertions that no earlier destination, outside receipt, receipt, or
staged tree is left behind. Re-run the existing focused/full suites, all three
schema-2 M1 operations, and the exact ignored local recipe.

**Stop rule:** do not change manifest schema or receipt fields, add general
transaction/rollback semantics for unpredictable I/O failures, add
composition/dry-run/removal/launch features, parse `.ALL`, infer compatibility
or identity, launch the game, reopen M2, or consult PS1. If a requested fix
requires one of those expansions, stop and record the exact blocker.

**Done condition:** all four reproductions fail closed with `ManifestError`
before any output mutation or outside-root write; ordinary sparse/staged,
force-file replacement, deterministic receipt, schema-1/schema-2 M1, and exact
local-corpus checks remain green; docs narrow complete-preflight claims to the
tested deterministic topology boundary; the required Vault updates are
committed; and Git is clean for the next independent ratchet round.
