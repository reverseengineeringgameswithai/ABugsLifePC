---
type: experiment
id: EXP-20260814-089
date: 2026-08-14
question: Can stable component-by-component receipt acquisition reject the exact M4.29 parent rename/link substitution before replay or removal without changing accepted receipt semantics?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; synthetic asset-free tests plus exact user-owned ignored local work-copy recipes
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.30 worker over M4.29 verdict d0601f551cdee8a76ba8d562a2df3a74fb1a89e4; external receipt acquisition only; no receipt/schema/operation/output/removal/mount/lifecycle change
artifacts:
  - reimplementation/ablpc/manifest.py
  - reimplementation/ablpc/compatibility.py
  - tests/test_manifest.py
  - mods/chars-flick-all-from-chars3-flickd-all.json
  - mods/training-primary-record-124-target-111e4.json
  - mods/training-primary-record-125-field-0c-zero.json
addresses: []
file_offsets: []
result: worker-complete-component-stable-receipt-acquisition
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
---

# EXP-20260814-089 - Component-stable external receipt acquisition

## Result

**Worker-complete; independent M4.31 audit required.** Exact M4.30 now opens
the external receipt's root, every lexical parent, and the final file relative
to retained directory descriptors. It refuses the exact M4.29 parent
rename/directory-link substitution before receipt parsing, source preparation,
output creation, or removal.

This changes only external receipt acquisition and its exact tests. Receipt
bytes, schemas, four operation families, reconstruction, source/hash/guard
authority, replay output, removal/mount semantics, and every manifest-driven
workflow remain unchanged.

## Pre-change reproduction

Before editing, the exact M4.29 fixture was repeated twice. After ordinary
lexical/placement checks but immediately before final file open, the checked
parent was renamed below a synthetic protected `originals/` directory and the
original pathname became a directory symlink to the moved parent. Both runs
retained the same single-link regular receipt inode and produced:

- `accepted=True`;
- parent path is a symlink;
- resolved receipt path is below the synthetic protected root; and
- replay output was created.

This independently confirmed the packet began from the rejected boundary.

## Component-stable acquisition

`_open_external_receipt_chain` now performs these bounded steps:

1. open the filesystem root as a directory descriptor;
2. inspect each next lexical component without following links;
3. open that component relative to the retained parent with
   `O_PATH | O_DIRECTORY | O_NOFOLLOW | O_CLOEXEC` and compare type,
   device, and inode to the inspection;
4. inspect and open the final single-link regular file relative to the retained
   final parent, then compare type, link count, device, inode, size, mtime, and
   ctime before and after reading;
5. revalidate protected/source/output placement; and
6. independently reacquire the complete lexical chain while the first chain
   remains open, requiring identical directory device/inode pairs and final
   file metadata before parsing receipt bytes.

All acquired descriptors close on both success and failure. This establishes
the exact component identity and no-link boundary requested by M4.30. It does
not claim a general filesystem transaction or protection against changes
after the completed deterministic preflight.

## Synthetic and retained evidence

Eight added focused cases cover:

- exact parent rename plus protected directory-link substitution for both
  `replay` and `remove-receipt`, with unchanged source/overlay snapshots;
- replacement by a different real parent inode after the first acquisition;
- parent inode replacement between component inspection and open;
- final-file hard-link-count and metadata changes at open;
- ordinary replay through an execute-only parent using Linux `O_PATH`
  directory handles; and
- CLI status 2, empty stdout, absent output, and unchanged source for the exact
  link substitution.

The manifest suite rises from 146 to 154 tests; manifest + LEVEL +
compatibility rises from 208 to 216; the canonical scoped suite rises from 396
to 404. The new component cases and all retained strict receipt, mapping,
schema, operation, source/guard/hash, output, removal, mount, composition, M1,
and compatibility cases pass.

The manifest implementation SHA-256 is now
`091a0431c24637fd8e4618bd09b208ac856c3312c3ebe5f1fb6ba7dcdff0f503`.
Only that already-declared compatibility pin changes. The exact 6,177-byte
statement, five-member pin set, other four pin values, scoped semantic checks,
and nine unique asset-free reads remain unchanged.

## Exact user-owned local receipts

The three established tracked local manifest families each completed two
ordinary apply, external-receipt replay, exact tree comparison, and
receipt-driven removal cycles in disposable directories below ignored
`work/`. Every replayed root was removed, every external receipt remained
exact, and the source hashes stayed:

- Training DAT:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`;
- opaque destination:
  `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`;
- opaque replacement:
  `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.

| Family | Cycles | Receipt SHA-256 | Replayed output SHA-256 |
|---|---:|---|---|
| exact opaque replacement | 2/2 | `ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63` | `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4` |
| same-DAT composition | 2/2 | `b899907eec17020f9e7a303b9cd8b5620dc70e83051840d13d57df80b6c779ef` | `78cca99b1993cc6deff8f89104d6f6aa8154ed7063e4ab0b56195e4321761d9a` |
| M1 plus opaque | 2/2 | `f8e144521905cc978e560e01158fae983495693f556f069773c8fac136c815b5` | DAT `b8012a95f7ec0254805bdd3cf32df2b16f2ad0926308fe8678cc2360027f720e`; opaque `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4` |

No game byte, local receipt, temporary manifest, or local output entered a
tracked path.

## Final repository gates

- focused manifest: 154/154;
- combined manifest + LEVEL + compatibility: 216/216;
- final `make check`: Python doctor green, Vault lint 271 notes with zero
  errors/warnings, exact M4 statement valid with five anchors, canonical
  404/404 tests, tracked-file audit zero, and diff checks green;
- manifest implementation SHA-256 exactly
  `091a0431c24637fd8e4618bd09b208ac856c3312c3ebe5f1fb6ba7dcdff0f503`;
  and
- protected roots retain only their tracked `.gitkeep`; no game byte is in the
  tracked worker surface.

## Limits and disposition

The receipt remains an operational authority under the exact-source model,
not a signature, provenance proof, migration format, or universal reorder
detector. Deterministic validation failures complete before mutation;
post-preflight I/O and concurrent changes remain non-transactional. Replay
still requires a new sparse root, and receipt removal still excludes staged
trees and sources.

M4.30 does not resolve `KU-051` by itself. Exact M4.31 must independently
falsify the immutable worker, including the original parent substitution,
adjacent component/final-file races, strict receipt mapping, removal/mount
boundaries, exact local recipes, compatibility reads, and repository hygiene.
M4, `KU-051`, and `KU-052` remain open pending that verdict.

## Independent disposition

Exact M4.31 returns `REJECT` in
[[EXP-20260814-090 - Independent M4.30 component-acquisition hard-truth audit]].
The verifier independently confirms the parent rename/link and adjacent
component/final-file acceptance corrections, retained 154/216/404 tests, six
local cycles, five pins, and nine reads. It rejects only this experiment's
statement that all acquired descriptors close on failure: one injected close
error stops `_close_receipt_handle_chain` and skips the remaining descriptors,
reproducibly retaining seven or six. Exact M4.32 owns only exception-safe
exhaustive receipt-chain closure. M4, `KU-051`, and `KU-052` remain open, and
the clean-derived-copy lifecycle remains unselected.
