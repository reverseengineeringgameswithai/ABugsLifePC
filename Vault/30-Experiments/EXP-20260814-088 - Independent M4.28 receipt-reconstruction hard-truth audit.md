---
type: experiment
id: EXP-20260814-088
date: 2026-08-14
question: Does immutable M4.28 make one exact ordinary current receipt plus exact source sufficient for strict sparse replay and removal without the original manifest across every claimed input, topology, retained-workflow, compatibility, and local boundary?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; synthetic asset-free tests plus exact user-owned ignored local work-copy recipes
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: independent documentation-only M4.29 audit of immutable worker fe13e302012442e8ed5c12391b9bb4f63159f490 with direct parent 2067da8022667c604ac5ac30a08122f271074a2f; no implementation, test, manifest, asset, launcher, runtime, M2, or PS1 changes
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
result: rejected-parent-component-change-before-receipt-open
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
  - audit/hard-truth
---

# EXP-20260814-088 - Independent M4.28 receipt-reconstruction hard-truth audit

## Verdict

**REJECT M4.28 acceptance.** The current receipt content is sufficient to
reconstruct the current manifest boundary, and every retained ordinary matrix
passed, but the external receipt loader does not keep the checked parent path
stable through final file acquisition. A parent directory can change into a
filesystem link after the component and placement checks but before the final
`open`. If that changed parent still reaches the same single-link receipt
inode, final-file identity and descriptor metadata remain exact, so replay is
accepted and creates output through a parent location that the strict input
checks did not approve.

This is one bounded file-consistency failure. It does not falsify the receipt-
to-manifest field mapping, source/hash/guard recomputation, sparse output
bytes, authenticated removal implementation, current-Linux mount checks, or
compatibility statement. `KU-051` therefore remains open, `KU-052` remains
open, and M4 remains Active.

## Immutable linkage and scope

The audit began and ended its behavior checks at exact worker
`fe13e302012442e8ed5c12391b9bb4f63159f490`, whose direct parent is
`2067da8022667c604ac5ac30a08122f271074a2f`. Git was clean at preflight. The
complete 1,935-line worker diff, all changed implementation/test files, both
READMEs, the complete required startup corpus, M4.28/M4.29 roadmap packets,
`EXP-20260814-086`, `EXP-20260814-087`, the worker session, relevant MOCs, and
the M1/M4 implementation notes were read before the verdict.

The audit changed documentation only. It did not modify an implementation,
test, manifest, receipt, schema, compatibility file, launcher, asset, runtime,
M2, or PS1 surface, and it did not run the game.

## Independent reconstruction model

The expected mapping was derived independently and matched the implementation
for both format families:

| Ordinary receipt authority | Equivalent current manifest authority |
|---|---|
| root `schema_version`, `manifest_name`, authored `files` order | unchanged schema; `manifest_name` becomes `name`; file order retained |
| file `path`, `input_sha256` | manifest `path`, `sha256` |
| file `output_sha256` | no manifest field; must be reproduced by ordinary preparation |
| LEVEL position edit | drop only contiguous `edit_index`; retain operation/section/index/position |
| LEVEL field-`0x0C` edit | drop only contiguous `edit_index`; retain operation/section/index/expected/value |
| LEVEL payload-target edit | drop only contiguous `edit_index`; retain operation/section/index/expected/target offsets |
| whole-file replacement edit | drop `edit_index`; retain operation/source path; `replacement_sha256` becomes `source_sha256` |

Operation family selects only the current `pc-level-dat-prefix-v0` or schema-2
`opaque-file-v0` format. Two direct mapping cases matched exactly, and 80/80
independently constructed wrong-schema, empty, unknown/missing/extra-field,
type, Boolean-index, noncontiguous-index, range, hash, path, duplicate-path,
mixed-family, and schema-1 opaque cases rejected.

The exact authority has inherent limits consistent with the worker's written
boundary. It does not recover original manifest formatting or composed input
files, establish authorship, or distinguish every commuting edit/file order
that can itself be minted as a different valid ordinary receipt. Exact source,
guard, output hash, authored receipt order, and full ordinary-byte
recomputation still discriminate every non-equivalent case exercised here.

## Reproducible parent-component falsification

The exact deterministic fixture used only synthetic bytes in a disposable
`/tmp/ablpc-m429-falsification-*` tree:

1. apply one schema-2 opaque replacement and copy its ordinary receipt to
   `external/receipt.json`, outside source and output;
2. let `_load_external_receipt` finish its lexical component `lstat`, final
   regular/single-link checks, `resolve(strict=True)`, and placement checks;
3. immediately before its final `os.open`, move the already checked
   `external/` directory below a disposable protected-name parent and replace
   the original `external/` component with a directory link to that moved
   directory;
4. allow the unchanged `os.open` and descriptor checks to continue.

Both independent repetitions returned:

```text
accepted=True symlink_ancestor=True protected_after_check=True output_created=True
```

The receipt file itself retained the same device/inode, regular-file type,
single-link count, size, mtime, and ctime, so the final descriptor checks could
not observe the parent change. `O_NOFOLLOW` applies to the final receipt
component only; it does not make already checked parent components stable.
This contradicts the worker's strict claim that filesystem-link parents and
protected/source/output placement are rejected across the external input
acquisition boundary.

The fixture made the parent change deliberately to place the check at a
deterministic instruction boundary. This result does not claim that every
possible concurrent filesystem change has been classified.

## Passing retained evidence

The failure is narrow. All other required matrices passed:

- focused manifest suite: 146/146;
- manifest + LEVEL + compatibility: 208/208;
- independently selected removal/mount/topology matrix: 37/37;
- canonical `python -m pytest -q tests`: 396/396;
- direct current-format mappings: 2/2;
- independent strict schema/field/type/index/hash/path cases: 80/80 rejected;
- deterministic parent-change reproductions: 0/2 rejected, the sole verdict
  failure.

The focused suite retains schemas 1/2, all four operations, no-op, empty and
unequal whole-file extents, same-file and multi-file composition, malformed
and nonordinary bytes, duplicates, source/guard/output mismatch, later-file
failure, nonregular/single-link receipt checks, new-root topology, exact source
and output snapshots, overlay drift/tree checks, CLI silence, and ordinary
apply/stage/compose/dry-run/manifest-remove behavior. The 37-case selector
retains exact-root/ancestor/descendant mount refusal, ordinary mounted and
unmounted removal behavior, hard-link/type/hash/source drift, extra-tree,
receipt mismatch, staged-tree, and protected/symlink root rejection.

## Exact local and compatibility evidence

All three authorized user-owned local families completed two ordinary apply,
external-receipt replay, receipt-driven removal, and retained manifest-driven
removal cycles in disposable directories. In every 6/6 cycle, replay stdout
and removal stdout were byte-identical to the external ordinary receipt, the
ordinary and replayed sparse trees were hash-identical, both overlays were
removed, and source hashes were unchanged.

| Family | Cycles | Receipt SHA-256 | Replayed output SHA-256 |
|---|---:|---|---|
| exact opaque replacement | 2/2 | `ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63` | `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4` |
| same-DAT two-manifest composition | 2/2 | `b899907eec17020f9e7a303b9cd8b5620dc70e83051840d13d57df80b6c779ef` | `78cca99b1993cc6deff8f89104d6f6aa8154ed7063e4ab0b56195e4321761d9a` |
| M1 plus opaque composition | 2/2 | `f8e144521905cc978e560e01158fae983495693f556f069773c8fac136c815b5` | DAT `b8012a95f7ec0254805bdd3cf32df2b16f2ad0926308fe8678cc2360027f720e`; opaque `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4` |

Source hashes remained `494d2818...a22` for Training DAT,
`a2f23220...4ac6` for the opaque destination, and `6e5afb4f...079a4` for the
replacement source. No local output entered a tracked path.

The exact compatibility statement remains canonical at SHA-256
`c3427d44cf32619a1f9bbcab7c51e67c0846b35d9d53eab7632ff6356c0beaf0`
with statement ID `ablpc-m4-compatibility-v0.1` and five anchors. Independent
tracing observed exactly nine unique tracked reads: the statement; three
tracked manifests; launcher; manifest implementation; Environment Status;
Wine baseline; and reimplementation README. The exact five machine pins are:

| Machine authority | SHA-256 |
|---|---|
| `scripts/play-pristine.sh` | `68c9171749bd7b207a15b4202193ccfddd2661fbb383deb34b1a5a5a4049977e` |
| `reimplementation/ablpc/manifest.py` | `59c275c5a6d7f539b4664130102035d90ecc6c0d587a09e90688115268e0e240` |
| `mods/training-primary-record-124-target-111e4.json` | `315320bc524986348167ca556b178ef41fe1e8ac961e482610f8f734f34b2434` |
| `mods/level01-primary-record-261-target-3459c.json` | `358998cd326f68fcf7e10593e8ec895915b558252c300464e8fe74177280198f` |
| `mods/chars-flick-all-from-chars3-flickd-all.json` | `5aaa6e9a4fa79c303ee0920e7f87e00e87bd1dfef412a32c55e36efcc947b607` |

## Repository hygiene

Before the intentional verdict commit, Vault lint reports 269 notes with zero
errors and zero warnings, the tracked-file audit reports zero violations, and
`git diff --check` passes. The verdict scope is exactly 16 documentation/
README paths and MIME inspection reports plain text only. Git tracks only
`.gitkeep` under `originals/` and `media/`; no local output, receipt, executable,
DAT, `.ALL`, `.ANM`, disc image, dump, virtual disk, or other game byte entered
the verdict diff. Final scoped tests and `make check` are rerun after all note
updates and before commit.

## Limitations

- The verdict is exact to the deterministic parent-component change above;
  it is not a general transaction or filesystem-concurrency result.
- Stable descriptor bytes explain why source and output reconstruction remain
  correct in the fixture; they do not satisfy the stronger documented parent-
  path and placement rejection boundary.
- Sequential post-preflight writes/unlinks, staged-tree removal, source
  restoration, package/backup/rollback, general dry-run or launch automation,
  broader platform support, M2, PS1, and M4 completion remain outside scope.

## Sole successor: M4.30

Exact M4.30 is the only selected correction. External receipt acquisition must
open and validate every parent component and the final receipt through stable
directory handles, or the smallest equivalent component-by-component no-link
mechanism. It must bind type/device/inode and placement validation to that
stable acquired chain, reject the exact parent rename/link substitution before
source preparation, output creation, or removal, retain exact before/after
source/output snapshots, and preserve every passing M4.28 gate above.

M4.30 may change only the external receipt acquisition helper, its exact
synthetic regression tests, the resulting one compatibility pin if required,
and documentation. It may not change receipt/manifest bytes or schemas,
mapping, operations, source/guard/output authority, replay/output/removal/mount
semantics, staged-tree behavior, launcher, assets, runtime, M2, or PS1. A new
fresh-context verifier remains required after that worker.

## Successor disposition

[[EXP-20260814-089 - Component-stable external receipt acquisition]] completes
the exact M4.30 worker boundary with retained relative no-link directory
descriptors and equal whole-chain reacquisition before parsing. The original
bypass and adjacent component/final-file changes now reject; 154/216/404 tests
and all six exact local cycles pass. Exact M4.31 remains the required
independent audit, so this note's `REJECT` disposition, `KU-051`, `KU-052`, and
M4 remain open until that verdict.
