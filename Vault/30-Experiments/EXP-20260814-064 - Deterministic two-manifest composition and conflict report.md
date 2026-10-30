---
type: experiment
id: EXP-20260814-064
date: 2026-08-14
question: Can exactly two existing manifests compose deterministically at disjoint destination-byte spans or fail with an asset-free exact conflict report before output?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline implementation, synthetic regression tests, and user-owned local corpus hash/byte checks
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.5 worker packet only; exactly two existing schema-1/schema-2 manifests; no schema/receipt redesign, N-way solver, dry-run, removal, launch, ALL parsing, compatibility inference, M2 reopening, runtime, or PS1
artifacts:
  - reimplementation/ablpc/manifest.py
  - reimplementation/ablpc/cli.py
  - tests/test_manifest.py
  - tests/test_level_dat.py
  - mods/training-primary-record-124-target-111e4.json
  - mods/training-primary-record-125-field-0c-zero.json
  - mods/chars-flick-all-from-chars3-flickd-all.json
addresses: []
file_offsets: []
result: worker-complete-exact-two-manifest-composition-and-conflict-boundary
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
---

# EXP-20260814-064 - Deterministic two-manifest composition and conflict report

## Result

**Worker-complete; independent M4.6 review required.** `ablpc-mod compose LEFT
RIGHT --source-root ROOT` now accepts exactly two existing schema-1/schema-2
manifests. It validates the existing schema, canonicalizes SHA-256 text,
orders the inputs by canonical-JSON digest, executes each manifest's complete
guards independently against the same source tree, and emits one deterministic
existing-schema manifest only when all cross-manifest destination-byte claims
are disjoint.

Reversing `LEFT` and `RIGHT` produces byte-identical stdout. The combined name
is derived from the two ordered canonical-input digests; files are sorted by
normalized Windows path and edits by exact half-open byte span plus canonical
input/order tie breakers. Schema 2 is selected iff either input is schema 2.
No game byte is embedded in the emitted manifest.

This worker result does not self-accept M4's composition exit gate. Exact
fresh-context M4.6 must attempt to falsify the immutable worker commit under
`DEC-20260814-055`.

> [!correction]
> Independent `EXP-20260814-065` rejected the complete result because the
> byte-span sort above could reverse one input's authored edit order. Exact
> M4.7 `EXP-20260814-066` replaces that ordering at the worker boundary with
> canonical input rank followed by original edit index. The M4.5 claims in
> this note remain historical worker evidence until M4.8 independently audits
> the correction.

## Exact byte-claim boundary

`compose_manifests` derives claims from the already bounds-checked PC-native
`LevelDat` structure and only the four existing operation forms:

- `set-scene-record-position`: `[record.offset, record.offset + 12)`;
- `set-scene-record-field-0c`: `[record.offset + 0x0C, record.offset + 0x0E)`;
- `set-scene-record-payload-target-offset`:
  `[payload_offset + target_field_offset, +4)` using the exact
  `PayloadTargetReference`; and
- `replace-whole-file`: `[0, original destination size)`, with any opaque
  same-destination pair rejected regardless of source equality.

Same normalized destinations merge only when their exact path spelling,
normalized source hash, and format agree and every claim from one input is
disjoint from every claim in the other. Existing intra-manifest edit order is
retained as a tie breaker; the combined manifest is validated and applied in
memory again after canonical sorting.

## Conflict boundary

`ManifestCompositionConflict` carries one deterministic report containing
only:

- `error: manifest-composition-conflict`;
- canonical input manifest names and canonical-JSON SHA-256 values;
- the normalized Windows destination;
- a stable conflict kind; and
- an exact `[start, end]` half-open overlap, or `null` where the conflict is a
  path/hash/format relationship rather than two byte intervals.

The CLI writes that compact JSON object to stderr, leaves stdout empty, and
returns 2. Synthetic coverage includes 12-byte position overlap, 2-byte
field-`0x0C` overlap, 4-byte payload-target overlap, opaque whole-destination
collision, case-insensitive destination spelling, cross-manifest replacement-
source/destination collision, same-destination format mismatch, and declared
source-hash mismatch. The two principal conflict cases are byte-identical
under reversed CLI arguments and leave the complete synthetic filesystem tree
and source hashes unchanged.

## Successful composition validation

Synthetic same-file composition combines adjacent position and field-`0x0C`
claims. Synthetic different-file composition combines a schema-1 M1 edit with
schema-2 opaque replacement. In both cases:

- reversed input order emits byte-identical canonical output;
- independently calculated byte-local output equals both sparse `apply` and
  full-tree `stage` output;
- the ordinary existing receipt is emitted without schema changes; and
- source files remain byte-identical.

The focused manifest/LEVEL suite passes 58/58 (47 accepted baseline tests plus
11 M4.5 tests). The complete scoped repository suite passes 246/246. The
accepted M4.3 output-topology, force, receipt, schema-1, schema-2, and single-
manifest tests remain in that passing focused boundary.

## User-owned local corpus check

Only tracked manifests, ignored user-owned source files, output hashes, and
byte comparisons were used. No `.ALL` byte was interpreted or retained.

The exact same-file tracked pair
`training-primary-record-124-target-111e4.json` plus
`training-primary-record-125-field-0c-zero.json` emits byte-identical forward/
reverse JSON at SHA-256
`b16a7cac40149ea87d26617a43ee1c29cfc5a3aebfa4cd34f139c45852879faa`.
Sparse application contains only the combined `CD/LEVEL07/LEVEL1.DAT` and
receipt; its exact output hash is
`78cca99b1993cc6deff8f89104d6f6aa8154ed7063e4ab0b56195e4321761d9a`.

The different-file pair
`training-primary-record-125-field-0c-zero.json` plus the exact schema-2
`chars-flick-all-from-chars3-flickd-all.json` emits byte-identical forward/
reverse JSON at SHA-256
`de15f8e566fb5dcfe70d8dc690a6c9dcc6f22faa70df207f37d784a138cfb485`.
Its sparse application contains exactly the combined LEVEL DAT, replaced
`CD/CHARS/FLICK.ALL`, and receipt. The LEVEL DAT is byte-identical to applying
the field manifest independently, at SHA-256
`47b7f45e39137f7decdd4ca94db2ef663ee868e6d506bc88511569ded74d7c00`.
The opaque output is exact replacement-source hash
`6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.
The original LEVEL DAT, destination `.ALL`, and replacement-source `.ALL`
hashes remain unchanged.

## Limitations

This is exactly two-manifest byte-claim composition. It does not reconcile
semantic intent, solve N-way dependencies or edit order, expose byte ranges as
a dry-run interface, remove or launch a mod, change manifest/receipt schemas,
parse `.ALL`, infer compatibility or identity, establish new runtime evidence,
or alter M2. The accepted M4.3 non-transactional limitation for unpredictable
I/O and concurrent races remains unchanged.

## Exact next packet

Run fresh-context M4.6 against the clean immutable worker commit. Independently
audit canonical input identity/order, every exact claim calculation, reversed-
argument success/conflict determinism, mismatch/collision rejection, empty-
stdout/no-output failure behavior, apply/stage equivalence, the two local
tracked pairs, all accepted M4.4 gates, Vault/tracked boundaries, and docs.
Return `ACCEPT` only if every M4.5 done condition survives and name one exact
next packet from a still-unmet M4 exit gate. Otherwise return `REJECT` with one
bounded corrective packet.
