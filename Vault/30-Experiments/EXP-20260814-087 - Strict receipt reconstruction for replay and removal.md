---
type: experiment
id: EXP-20260814-087
date: 2026-08-14
question: Can one exact ordinary current receipt plus its exact source reconstruct an existing-schema manifest and replay or remove the same dedicated sparse overlay without the original manifest?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; synthetic asset-free tests plus exact user-owned ignored local work-copy recipes
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.28 worker over parent 2067da8022667c604ac5ac30a08122f271074a2f; current receipt/manifest schemas and operations only; no game execution, originals/media/PS1 access, schema redesign, staged-tree deletion, launch, package, rollback, or transaction behavior
artifacts:
  - reimplementation/ablpc/manifest.py
  - reimplementation/ablpc/cli.py
  - reimplementation/ablpc/compatibility.py
  - tests/test_manifest.py
  - mods/chars-flick-all-from-chars3-flickd-all.json
  - mods/training-primary-record-124-target-111e4.json
  - mods/training-primary-record-125-field-0c-zero.json
addresses: []
file_offsets: []
result: worker-complete-strict-receipt-replay-and-removal
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
---

# EXP-20260814-087 - Strict receipt reconstruction for replay and removal

## Result

**Worker-complete.** One byte-exact ordinary receipt emitted by the current
tool, together with the exact source files it authenticates, now reconstructs
one equivalent existing-schema manifest and drives a new dedicated sparse
overlay or removal of that exact overlay without the original manifest.

The new bounded commands are:

```bash
./scripts/ablpc-mod replay RECEIPT \
  --source-root SOURCE --output-root NEW_OVERLAY
./scripts/ablpc-mod remove-receipt RECEIPT \
  --source-root SOURCE --overlay-root OVERLAY
```

`replay` requires a new output root. `remove-receipt` shares the accepted
manifest-driven removal preflight and deletion implementation. Existing
`apply`, `stage`, `compose`, `dry-run`, and manifest-driven `remove` behavior
is unchanged.

## Reconstruction and validation boundary

The external receipt loader opens one single-link regular file with
`O_RDONLY | O_CLOEXEC | O_NOFOLLOW | O_NONBLOCK`, rejects symlinked ancestors
and protected/source/output placement, compares the opened device/inode to the
pre-open `lstat`, and rejects changes in type, links, identity, size, mtime, or
ctime across the read. It then requires strict UTF-8 JSON with no duplicate
keys or invalid constants and exact ordinary `_receipt_bytes` encoding.
Malformed deep nesting is converted to `ManifestError` rather than escaping as
`RecursionError`.

Root, file, and operation key sets are exact. Schema and edit indices are
integer-not-boolean; edit indices must be contiguous authored positions; all
input, output, and replacement hashes are exact lowercase SHA-256; files and
edits are nonempty; paths remain subject to the existing safe-path and
case-insensitive collision rules. The current operation family uniquely maps
back to the current format:

| Receipt operation | Reconstructed current manifest format/fields |
|---|---|
| `set-scene-record-position` | `pc-level-dat-prefix-v0`; section, index, position |
| `set-scene-record-field-0c` | `pc-level-dat-prefix-v0`; section, index, expected/value |
| `set-scene-record-payload-target-offset` | `pc-level-dat-prefix-v0`; section, index, expected/target offsets |
| `replace-whole-file` | schema 2 `opaque-file-v0`; source path and replacement hash become the manifest replacement-source authority |

The reconstructed value passes the ordinary `_validate_manifest` and
`_prepare_manifest` paths. The complete receipt is then recomputed from exact
source bytes, operation guards, replacement bytes, authored order, and output
hashes; byte equality with the supplied external receipt is required before
any output creation or deletion preflight.

## Synthetic and retained evidence

Forty-seven added focused cases take the manifest suite from 99 to 146. They
cover schemas 1/2; all three LEVEL operations; empty, shorter, and longer
opaque replacement; a no-op; composed multi-file input; strict root/file/edit
fields; lowercase and mismatched hashes; edit indices; safe and duplicate
paths; malformed, duplicate-key, compact, CRLF, BOM, reordered, and deeply
nested JSON; new-root-only replay; nonregular/hard-linked/symlinked/FIFO
receipt inputs; descriptor inode/type and during-read drift; receipt placement;
later-file preparation failure; external and overlay drift; exact snapshots;
and success/failure CLI output.

The final asset-free gates are:

- manifest focused: 146/146;
- manifest + LEVEL + compatibility: 208/208;
- canonical `python -m pytest -q tests`: 396/396;
- strict M4 compatibility statement: five anchors valid;
- Vault lint: 267 notes, zero errors, zero warnings;
- tracked-file audit: zero violations.

The manifest authority SHA-256 changes only because of M4.28 implementation:
`59c275c5a6d7f539b4664130102035d90ecc6c0d587a09e90688115268e0e240`.
Only that one existing pin changes. The exact statement bytes, other four
pins, semantic alignment, and exactly-nine asset-free read boundary remain.

## Exact user-owned local receipts

The three established tracked local manifest families each completed two
ordinary-receipt mint, receipt-only replay, and receipt-only removal cycles in
disposable directories. Both cycles were identical, each replayed tree was
byte-identical to its ordinary sparse overlay, every replayed root was removed,
the external receipt remained exact, and the three source hashes stayed:

- Training DAT:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`;
- opaque destination:
  `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`;
- opaque replacement source:
  `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.

| Family | Cycles | Receipt SHA-256 | Replayed output SHA-256 |
|---|---:|---|---|
| exact opaque replacement | 2/2 | `ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63` | `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4` |
| same-DAT two-manifest composition | 2/2 | `b899907eec17020f9e7a303b9cd8b5620dc70e83051840d13d57df80b6c779ef` | `78cca99b1993cc6deff8f89104d6f6aa8154ed7063e4ab0b56195e4321761d9a` |
| M1 plus opaque composition | 2/2 | `f8e144521905cc978e560e01158fae983495693f556f069773c8fac136c815b5` | DAT `b8012a95f7ec0254805bdd3cf32df2b16f2ad0926308fe8678cc2360027f720e`; opaque `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4` |

No game byte entered a tracked path.

## Hard limits

The receipt is an operational authority under the exact-source model, not a
signature or provenance proof. It cannot prove who authored it, recover the
original manifest text or composed inputs, authenticate unreferenced source
files, or universally distinguish commuting edits that were reordered and
renumbered into another valid ordinary authority. No such broader tamper claim
is made.

Deterministic parse, validation, source/hash/guard, recomputation, and topology
failures complete before mutation. Sequential writes and unlinks remain
non-transactional for post-preflight I/O failures and concurrent races. Replay
does not accept an existing output root, and receipt-driven removal does not
delete staged trees or sources.

M4 is not complete. [[Known Unknowns#KU-052 (clean-derived-copy lifecycle is not jointly demonstrated)]]
remains open.

## Sole successor: M4.29

Exact M4.29 is a fresh-context independent hard-truth audit of the immutable
M4.28 worker. It must independently derive the receipt-to-manifest mapping,
attempt malformed/ambiguous authority, descriptor/path, source/guard/hash,
output topology, removal/mount, deterministic/local, compatibility-read, and
retained workflow falsifications, then return one verdict. The audit changes
documentation only. Acceptance may close `KU-051` and select the separate
clean-derived-copy lifecycle gate as the sole next packet; it may not mark M4
complete.

## Independent disposition

[[EXP-20260814-088 - Independent M4.28 receipt-reconstruction hard-truth audit]]
returns `REJECT`. Both current receipt-to-manifest mappings, 80/80 strict input
cases, 146/208/396 tests, 37 selected removal/mount/topology cases, all six
local cycles, five pins, and nine reads survive. The one falsification changes
an already checked receipt parent into a directory link before final file
acquisition while retaining the same regular, single-link receipt inode; 2/2
repetitions accept and create output through the changed parent location.
Exact M4.30 is the sole correction for stable component-by-component receipt
acquisition. `KU-051`, `KU-052`, and M4 remain open.
