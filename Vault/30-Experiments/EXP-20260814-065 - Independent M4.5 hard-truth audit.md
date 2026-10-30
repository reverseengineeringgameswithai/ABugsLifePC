---
type: experiment
id: EXP-20260814-065
date: 2026-08-14
question: Does immutable commit 8419402 satisfy every M4.5 exact two-input composition, conflict, existing-schema, accepted-baseline, and asset-free condition?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline independent code review, synthetic falsification, scoped tests, and user-owned local corpus hash/byte checks
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact fresh-context M4.6 audit of immutable commit 8419402 only; no implementation/schema/receipt change, N-way solver, dry-run, removal, launch, ALL parsing, compatibility inference, M2 reopening, runtime, PS1, or general rollback request
artifacts:
  - reimplementation/ablpc/manifest.py
  - reimplementation/ablpc/cli.py
  - reimplementation/ablpc/level_dat.py
  - tests/test_manifest.py
  - tests/test_level_dat.py
  - mods/training-primary-record-124-target-111e4.json
  - mods/training-primary-record-125-field-0c-zero.json
  - mods/chars-flick-all-from-chars3-flickd-all.json
addresses: []
file_offsets:
  - synthetic primary record 0 at 0x98
  - synthetic position claim [0x98,0xA4)
  - synthetic field-0c claim [0xA4,0xA6)
  - synthetic payload-target claim [0x21C,0x220)
result: reject-intra-input-edit-order-not-preserved
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
  - audit/hard-truth
---

# EXP-20260814-065 - Independent M4.5 hard-truth audit

## Verdict

**REJECT.** Immutable worker commit
`8419402ebde628988ef6abddacb71b1b03ce7286` does not satisfy the M4.5 done
condition for disjoint composition of two independently valid existing-schema
manifests. `compose_manifests` validates each input in its authored edit order,
but `_composed_file_entry_from_ranked_claims` then sorts the emitted edits by
source byte span before combined revalidation. That can reverse two edits
inside one input and destroy behavior that the ordinary existing-schema apply
path just accepted.

The falsification uses no game bytes and does not ask for semantic
reconciliation. It requires only preservation of one input manifest's existing
sequential edit contract while combining a second manifest whose exact write
claim is disjoint.

## Audit boundary and immutable inputs

The audit began and remained at clean exact commit `8419402`, whose parent is
accepted M4.4 documentation commit `1ceaed7`. Before code review or testing,
the complete [[START HERE]] startup sequence was read: full [[Current State]],
full [[Project Roadmap]], full [[Environment Status]], full [[Decision Log]],
full [[Known Unknowns]], [[Implementation MOC]], and [[Experiments MOC]]. The
complete [[Agent Operating Manual]], [[Project Charter]], exact M4.6 roadmap
packet, `EXP-20260814-063/064`, [[M4 Exact Whole-file Replacement]],
[[M1 Tool Support Matrix]], and the M4.5 worker session were also read.

Review covered the 15-path worker diff; `build_parser`/`main` in
`reimplementation/ablpc/cli.py`; `ManifestCompositionConflict`,
`compose_manifests`, `_manifest_claims`, `_composed_file_entry`,
`_composed_file_entry_from_ranked_claims`, `_prepare_manifest`, and
`_validate_manifest` in `reimplementation/ablpc/manifest.py`; exact record and
payload locators in `level_dat.py`; all 11 M4.5 tests; accepted manifest/LEVEL
and topology tests; the three tracked manifests; and the ignored user-owned
local work copy. No original, external repository, game file, implementation
code, runtime state, or receipt/schema surface was modified.

## Concrete falsification

### Setup

A synthetic DAT accepted by `LevelDat.parse` contains primary record 0 at
`0x98`, its payload-target field at `0x21C`, and valid positive target blocks
at both the original target `0x98` and replacement target `0x240`. At `0x98`,
the original first dword is zero and the word at `0x9C` is `0xFFFF`, so the
existing positive-target parser accepts that location as a zero-entry block
with an immediate terminator.

The exact schema-1 inputs are:

1. `left-valid-ordered`, whose authored order is:
   - payload-target edit `[0x21C,0x220)`, expected `0x98`, replacement
     `0x240`;
   - position edit `[0x98,0xA4)`, replacement components `(1,2,3)`.
2. `right-disjoint`, whose only edit is field `+0x0C` at `[0xA4,0xA6)`.

The three write claims are pairwise disjoint across the two inputs. Ordinary
`apply` accepts each input independently with return code zero and emits its
output. Source SHA-256 remains
`63b411bdfdaf3fdde002917f05c019a95ecb4ee7faa3f477c3a2a01b82741533`.

### Observation

`compose` fails in both CLI argument orders with return code 2, empty stdout,
and identical stderr SHA-256
`7be2276d0a188b97845208c0ce5d322fa5b47255d6ddae99ff86da376f178324`:

```text
ablpc-mod: negative payload-target command item count -32768 at 0xac
```

Code inspection supplies the cause. The left input is first accepted in its
authored payload-target-then-position order at `manifest.py:131-136`.
`_composed_file_entry_from_ranked_claims` then sorts by
`(claim.start, claim.end, input rank, edit index, canonical edit JSON)` at
`manifest.py:462-480`, moving the `0x98` position write before the `0x21C`
payload-target edit. Combined `_prepare_manifest` at `manifest.py:219-222`
replays that new order. The position write changes the bytes that the still-
pending payload-target guard parses as its expected old positive block, so the
otherwise valid input sequence now fails.

This is a direct falsification of the declared “disjoint cross-manifest spans
compose” and “existing-schema behavior remains unchanged” claims. It is also
why a multi-edit valid-input test was required by M4.6 rather than inferring
correctness from single-edit worker fixtures.

## Claims that survived independently

The rejection is isolated to intra-input sequence preservation. The following
checks passed at immutable `8419402`:

- Focused manifest/LEVEL suite: 58/58 passed.
- Complete canonical repository suite (`python -m pytest -q tests`): 246/246
  passed in 6.65 seconds. No unscoped pytest command was used.
- Independent claim/conflict matrix: 12/12 passed. It reproduced exact
  position `[record,record+12)`, field-`0x0C` `[record+12,record+14)`, and
  payload-target four-byte spans; a cross-form partial overlap; distinct,
  identical-source, and empty-destination opaque collisions; case-insensitive
  path, format, normalized hash, and replacement-source/destination conflicts;
  canonical digest/name/schema/hash behavior; reversed compact JSON; empty
  stdout; and unchanged synthetic trees.
- A separate ordinary multi-edit chain with two same-field sequential edits
  plus a disjoint position edit passed apply/stage, reversed JSON, receipt, and
  source-preservation checks. Thus intra-input overlap is not incorrectly
  compared as a cross-input conflict; the falsification is specifically the
  global span reorder of a valid sequence.
- Empty opaque destinations still conflict deterministically with overlap
  `[0,0)`; different opaque destinations with unequal replacement sizes
  compose and emit the exact replacement sizes. No size-equality assumption
  was introduced.
- Saved emitted synthetic JSON passed ordinary CLI `apply` and `stage`; both
  matched an independent `LevelDat` byte calculation, returned and wrote
  equal ordinary receipts, and preserved the source.
- Explicit M1 schema applications passed 6/6: position, field-`0x0C`, and
  payload-target operations under both schema 1 and schema 2. Cross-schema
  bytes matched 3/3.
- Independent M4.4 topology matrix: 28/28 passed. It covered all four original
  M4.2 reproductions plus requested-root symlinks/lexical normalization/files,
  planned ancestor/final symlink-directory-FIFO-regular cases, fixed and
  existing receipts, force regular/non-regular behavior, stage-source planned
  and receipt topology, and requested staged-root blockers. Rejections kept
  source/blocker snapshots unchanged and left earlier/outside/staged outputs
  absent; positive forced regular files and existing regular staged receipts
  succeeded.
- Tracked same-DAT pair reproduced worker hashes exactly: composed JSON
  `b16a7cac40149ea87d26617a43ee1c29cfc5a3aebfa4cd34f139c45852879faa`
  and output DAT
  `78cca99b1993cc6deff8f89104d6f6aa8154ed7063e4ab0b56195e4321761d9a`.
  Forward/reverse bytes, independent edit calculation, two-file sparse
  locality, and source preservation passed.
- Tracked M1-plus-opaque pair reproduced composed JSON
  `de15f8e566fb5dcfe70d8dc690a6c9dcc6f22faa70df207f37d784a138cfb485`.
  Its DAT matched independent application, its opaque output matched exact
  source hash `6e5afb4f...079a4`, sparse output contained exactly both destinations
  plus the receipt, and all three source hashes remained unchanged.
- The exact opaque recipe alone emitted the demonstrated replacement hash in
  both output and receipt, wrote only its destination plus receipt, and
  preserved both source files.
- Vault lint before verifier documentation: 221 notes, zero errors, zero
  warnings. Tracked-file audit: zero violations. Every worker-diff path is
  text; no executable, DAT, `.ALL`, `.ANM`, disc image, dump, VM image,
  capture, or other game-byte payload entered the commit.

## Limitations

- This audit does not reject the exact single-edit tracked pairs or the byte-
  overlap detector. It rejects the general M4.5 done claim because the schema
  already permits more than one edit in a file entry and the composer changes
  that accepted sequence.
- The synthetic source is intentionally adversarial but bounds-valid under the
  existing parser and manifest guards. No PC-format semantic meaning is
  inferred from it.
- No N-way ordering, arbitrary dependency solver, cross-input semantic
  reconciliation, `.ALL` parsing, compatibility rule, dry-run, removal,
  launch, runtime, M2, PS1, schema change, receipt change, or general rollback
  work was requested or performed.
- The accepted M4.3 limitation remains: unpredictable I/O or concurrent races
  after deterministic preflight are not transactional.

## Exact corrective packet: M4.7

**Name:** Preserve intra-input edit sequence in deterministic two-manifest
composition.

**Bounded question:** Can exactly two independently valid existing-schema
manifests with disjoint cross-input write claims emit deterministic reversed-
argument-identical JSON while preserving each input file entry's authored edit
order, so composition never invalidates a sequence already accepted by the
ordinary apply path?

**Exact locators and inputs:** immutable rejected commit `8419402`;
`compose_manifests` at `reimplementation/ablpc/manifest.py:66-223`;
`_EditClaim.edit_index` at lines 38-43;
`_composed_file_entry_from_ranked_claims` at lines 462-480;
`_apply_level_dat_edits` at lines 309-364; combined `_prepare_manifest` at
lines 219-222; the synthetic `0x98`/`0x21C` falsification above; existing 11
M4.5 tests; and every accepted M4.4, schema, receipt, tracked-pair, exact-
recipe, Vault, and asset-free gate.

**First pass:** add a regression that independently applies the two exact
falsification inputs, proves their cross-input claims disjoint, composes them
in both argument orders, saves the emitted JSON, and checks apply/stage against
the authored left sequence plus the independent right field edit. Replace the
global source-span reorder with one deterministic exactly-two-input ordering
that uses canonical input identity while preserving edit-index order within
each input file entry. Keep file ordering deterministic, retain exact span
conflict detection only across inputs, revalidate the combined existing-schema
manifest, and correct docs that currently promise byte-location-sorted edits.
Add adjacent regressions for a descending-offset valid input, same-span
sequential guards, empty/unequal opaque files, and deterministic selection
among multiple conflicts.

**Stop rule:** do not add more than two inputs, an arbitrary dependency/order
solver, semantic reconciliation, a schema/receipt/operation change, general
dry-run/removal/launch, `.ALL` parsing, compatibility inference, runtime, M2,
PS1, or general transaction/rollback work. If preserving the two authored
sequences requires choosing among cross-input semantic dependencies rather
than a deterministic canonical interleaving, stop and record that exact
blocker instead of broadening.

**Done condition:** the exact falsification pair composes byte-identically
under reversed arguments; saved apply and stage match the independently
calculated authored-sequence result with ordinary identical receipts and source
preservation; existing exact 12/2/4-byte and opaque conflict reports remain
byte-identical and asset-free; canonical schema/name/file ordering and all
multiple-edit adjacent cases pass; the 58 focused, 246 complete, M4.4
topology, 6/6 M1 schema, tracked local pair, exact opaque recipe, Vault, and
no-game-bytes gates remain green; docs state the exact order-preservation and
two-input limit; required Vault updates are committed intentionally; and Git
is clean for fresh-context M4.8.
