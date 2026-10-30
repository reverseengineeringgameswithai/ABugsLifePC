---
type: experiment
id: EXP-20260814-060
date: 2026-08-14
question: Can schema 2 express the exact accepted FLICK.ALL <- FLICKD.ALL copy as a byte-exact fail-closed user-work-copy operation without regressing M1?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline implementation, synthetic tests, and user-owned local corpus check
environment_version: Python 3.14; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: M4.1 exact opaque whole-file replacement only; no game launch, ALL parsing, asset inclusion, compatibility inference, or cross-port evidence
artifacts:
  - reimplementation/ablpc/manifest.py
  - tests/test_manifest.py
  - mods/chars-flick-all-from-chars3-flickd-all.json
  - Vault/40-Implementation/M4 Exact Whole-file Replacement.md
  - work/mod-builds/M4-1-local-check-overlay-20260814/.ablpc/receipt.json
addresses: []
file_offsets: []
result: worker-complete-byte-exact-fail-closed-pending-independent-m4-2-audit
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
---

# EXP-20260814-060 - Exact whole-file replacement manifest boundary

## Question

Can the existing manifest/staging workflow express the exact accepted
`CHARS/FLICK.ALL <- CHARS3/FLICKD.ALL` copy as an asset-free, byte-exact,
fail-closed operation over files already present in a user's derived work copy,
while preserving deterministic receipts and every M1 operation?

## Inputs and boundary

- Exact executable compatibility anchor, not executed in this packet:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Destination `CD/CHARS/FLICK.ALL` SHA-256:
  `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`.
- Replacement source `CD/CHARS3/FLICKD.ALL` SHA-256:
  `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.
- `EXP-20260812-033` supplies unchanged-executable Direct3D acceptance and the
  bounded visible result. `EXP-20260813-049` supplies the asset-free
  instruction/distribution boundary. [[M1 Tool Support Matrix]] supplies the
  existing schema, staging, and receipt contract.

No original, executable, game asset, work-copy file, or runtime state was
modified. No `.ALL` byte was interpreted. No game was launched. No PS1 source
was consulted.

## Implementation

Manifest schema 2 accepts `format: opaque-file-v0` with exactly one
`replace-whole-file` edit. The destination entry supplies its safe relative
path and exact input hash; the edit supplies a distinct safe in-work-copy
source path and exact replacement hash.

Application now preflights every entry before creating or changing the output.
It reads replacement bytes only from the source work tree. Sparse application
writes only destination paths and the receipt. Full staging copies the work
tree to a new destination and changes only the named destination, preserving
the replacement source. The receipt records input, replacement, and output
hashes.

Schema 1 is unchanged. Schema 2 also accepts existing M1 file formats and edit
operations, including a mixed synthetic manifest.

## Synthetic discriminator matrix

| Case | Result |
|---|---|
| Byte-exact sparse replacement | Accepted; output equals replacement bytes |
| Deterministic receipt | Two independent outputs have byte-identical receipt JSON |
| Wrong destination hash | Rejected before output creation |
| Wrong replacement hash | Rejected before output creation |
| Later-entry wrong hash | Entire manifest rejected before any earlier write |
| Unsafe target/source paths | Traversal, redundant components, backslash, drive/colon, internal metadata path rejected |
| Source symlink escape | Rejected outside the source root |
| Same source/destination | Rejected case-insensitively |
| Source/destination collision | Rejected across the complete manifest |
| Full staging | Source/unrelated files retained; only destination changed |
| Existing M1 operations | Schema 1 tests pass; schema 2 mixed manifest accepted |
| CLI application | Accepted with schema-2 JSON receipt |

## Local corpus check

The ignored user-owned tree
`work/copies/BUGS_PC-full-disc/PC/BUGS` resolves the exact expected destination
and replacement hashes. Applying the tracked manifest to ignored sparse output
`work/mod-builds/M4-1-local-check-overlay-20260814` produced:

- only `CD/CHARS/FLICK.ALL` and `.ablpc/receipt.json`;
- destination output SHA-256
  `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`;
- byte identity between output destination and work-copy replacement source;
  and
- unchanged source-tree destination and replacement hashes after application.

`git check-ignore` confirms that the local output is excluded by
`/work/mod-builds/`. No asset or receipt containing asset bytes is tracked.

## Confirmed

- The exact M2.20 pair can be represented as a schema-2 manifest with no game
  bytes.
- Both exact source-tree hashes are required before output, and both source
  files remain unchanged.
- Synthetic sparse and staged paths are byte-exact and fail closed at the
  declared hash/path/collision boundary.
- Receipts carry exact input/replacement/output hashes deterministically.
- Existing M1 schema-1 behavior remains accepted, and schema 2 can retain M1
  operations.
- The local corpus resolves and applies the tracked exact recipe without
  committing either `.ALL` file.
- The complete repository suite passes 228 tests; Vault lint reports 213 notes
  with zero errors/warnings, and the tracked-file audit reports zero violations.

## Not confirmed

- General `.ALL` layout, field semantics, identity, compatibility, or invalid-
  file behavior.
- Safety or usefulness of any source/destination pair other than the exact
  demonstrated pair.
- Game launch or removal behavior in this implementation packet.
- Completion of M4's composition, dry-run, launch, removal, or compatibility-
  statement exit gates.

## Result and follow-up

M4.1 is worker-complete at its exact declared boundary. Under the user-required
serial ratchet, this worker does not select or execute another technical M4
packet. Exact offline M4.2 must independently attempt to falsify the schema,
preflight, staging, receipt, compatibility, and distribution claims. It must
either accept M4.1 and name one exact next M4 packet grounded in the remaining
exit gates, or reject it with one bounded corrective packet.
