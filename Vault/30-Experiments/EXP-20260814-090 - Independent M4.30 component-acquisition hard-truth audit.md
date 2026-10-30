---
type: experiment
id: EXP-20260814-090
date: 2026-08-14
question: Does immutable M4.30 retain one stable no-link receipt component chain and release every acquired descriptor on every success and failure path?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; synthetic asset-free tests plus exact user-owned ignored local work-copy recipes
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: fresh-context exact M4.31 audit of immutable M4.30 worker cd7c3edc81f92af20d7c71b796829e73b240bd5f with direct M4.29 parent d0601f551cdee8a76ba8d562a2df3a74fb1a89e4; audit and documentation only
artifacts:
  - reimplementation/ablpc/manifest.py
  - reimplementation/ablpc/compatibility.py
  - tests/test_manifest.py
  - Vault/30-Experiments/EXP-20260814-087 - Strict receipt reconstruction for replay and removal.md
  - Vault/30-Experiments/EXP-20260814-088 - Independent M4.28 receipt-reconstruction hard-truth audit.md
  - Vault/30-Experiments/EXP-20260814-089 - Component-stable external receipt acquisition.md
addresses: []
file_offsets: []
result: rejected-exception-unsafe-receipt-chain-closure
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
---

# EXP-20260814-090 - Independent M4.30 component-acquisition hard-truth audit

## Verdict

**REJECT.** Immutable M4.30 closes the exact M4.29 parent-link acceptance
bypass and every independently injected component/final-file acceptance case,
but it does not satisfy its explicit descriptor-ownership claim. If one
`os.close` reports an error while `_close_receipt_handle_chain` releases the
reacquired chain, the helper stops immediately and skips every remaining
descriptor. The first-close injection leaves seven descriptors open; the
next-close injection leaves six. The first result reproduced 2/2 in separate
fresh processes.

This verdict selects exactly one smallest correction: exception-safe,
exhaustive receipt-handle-chain release. It does not change receipt content,
mapping, validation, replay, removal, mount policy, compatibility pins, or the
separate clean-derived-copy lifecycle.

## Immutable linkage and scope

- audited worker: `cd7c3edc81f92af20d7c71b796829e73b240bd5f`;
- required direct parent: `d0601f551cdee8a76ba8d562a2df3a74fb1a89e4`;
- initial tree: clean;
- worker diff: 18 paths, 957 insertions, 118 deletions;
- implementation review: all 2,042 lines of `manifest.py`, all 876 lines of
  `compatibility.py`, all 3,541 lines of `test_manifest.py`, and the complete
  immutable worker diff; and
- audit changes: documentation only.

The audit did not modify implementation, tests, compatibility statement or
pins, schemas, operations, launcher, assets, protected content, local work
copies, runtime, M2, or the external PS1 repository.

## Exact parent-change reconstruction

The M4.29 parent rename/directory-link substitution was independently rebuilt
for both `replay` and `remove-receipt`. Each fixture captured complete no-follow
snapshots of source, lexical receipt parent, moved protected target, overlay,
and output. The attack ran during final receipt acquisition: the lexical parent
was renamed below a synthetic `originals/` root and replaced by a directory
symlink to the moved parent.

Both 2/2 calls rejected with `ManifestError` at protected placement
revalidation. In each case:

- the source and overlay snapshots were exact before/after matches;
- replay output remained absent;
- the lexical parent was the injected symlink;
- the moved target retained the original parent snapshot and receipt; and
- no source preparation, replay write, or removal occurred.

The replay fixture retained source snapshot
`e3b21dd11c6aebf4c2be90dd415fa336d93594a5e80bbb5b870103e63020fc22`
and overlay snapshot
`a50239c2562dd587c69a8911d9cafcf25881196a3c21c94148bb8a994bdf2e0a`.
The removal fixture retained source snapshot
`c44c1599d18469e6577c204566cd3fe5532cb2ef8f55bfb0960f4a54ac20844c`
and overlay snapshot
`20bc3632c2b17e2bb9a4b582c0ef467f67b328195fc8a5da65bf604fa124e979`.
These digests cover type, mode, link count, size, device/inode identity,
symlink target, and regular-file content without following links.

## Independent acquisition matrix

Twenty-eight fresh synthetic cases exercised ordinary absolute, relative, deep,
and execute-only-parent success plus missing final, parent link, final link,
FIFO, hard link, malformed/duplicate parsing, missing/non-directory parent
after placement, component inode/device/type disagreement, final inode/type/
metadata/content change, component stat/open error, final/root open error,
initial/post-read/reacquisition `fstat` error, `fdopen` error, and close error.

- expected accept/reject behavior: 28/28;
- source and ordinary-overlay snapshot preservation: 28/28;
- zero descriptor-count delta: 27/28; and
- the sole failure: injected close error, output absent and trees unchanged,
  but seven acquired descriptors retained.

Three separate post-read reacquisition cases replaced the visible parent with a
new directory, installed a directory link, or changed final metadata. All 3/3
rejected before output. The worker's eight new focused tests also pass 8/8.

## Reproducible rejection

`_close_receipt_handle_chain` closes the file and then each directory in reverse
order without protecting later closes from an earlier `OSError`.
`_open_external_receipt_chain` has the same stop-on-first-close cleanup shape
on acquisition failure. In the independently injected reacquired-chain path:

| Injection | Result | Descriptor delta | Mutation |
|---|---|---:|---|
| first close reports `EIO`, run 1 | raw `OSError`, rejected | +7 | none |
| first close reports `EIO`, run 2 | raw `OSError`, rejected | +7 | none |
| second close reports `EIO` | raw `OSError`, rejected | +6 | none |

The ordinary success and every injected stat/open/read/reacquisition error that
reached current cleanup had zero descriptor delta. The defect is therefore
localized to close-error handling, not general component acquisition. Linux
may release the descriptor whose own close reports a late error; that does not
release the six later descriptors the current helper never attempts to close.
This directly contradicts `EXP-20260814-089`'s statement that all acquired
descriptors close on both success and failure.

## Retained authority and workflow evidence

All three exact user-owned local families completed two ordinary apply,
external-receipt replay, byte-identical tree comparison, receipt-driven
removal, and retained manifest-driven removal cycles in disposable `/tmp`
directories. Every 6/6 cycle kept the external receipt exact, removed both
overlay roots, and preserved source hashes.

| Family | Cycles | Receipt SHA-256 | Replayed output SHA-256 |
|---|---:|---|---|
| exact opaque replacement | 2/2 | `ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63` | `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4` |
| same-DAT composition | 2/2 | `b899907eec17020f9e7a303b9cd8b5620dc70e83051840d13d57df80b6c779ef` | `78cca99b1993cc6deff8f89104d6f6aa8154ed7063e4ab0b56195e4321761d9a` |
| M1 plus opaque | 2/2 | `f8e144521905cc978e560e01158fae983495693f556f069773c8fac136c815b5` | DAT `b8012a95f7ec0254805bdd3cf32df2b16f2ad0926308fe8678cc2360027f720e`; opaque `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4` |

Source hashes remained Training DAT
`494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`,
opaque destination
`a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`,
and replacement source
`6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.

The focused manifest suite passes 154/154, manifest + LEVEL + compatibility
passes 216/216, and the canonical scoped suite passes 404/404. This retains
schemas 1/2, all four operations, strict bytes and receipt mapping,
source/hash/guard/output authority, replay/removal/mount behavior, composition,
M1, and all manifest workflows.

The compatibility statement remains byte-exact at
`c3427d44cf32619a1f9bbcab7c51e67c0846b35d9d53eab7632ff6356c0beaf0`,
the exact five pins pass, and independent tracing observes exactly nine unique
asset-free reads: statement, three manifests, launcher, manifest implementation,
Environment Status, Wine baseline, and reimplementation README. The manifest
pin remains
`091a0431c24637fd8e4618bd09b208ac856c3312c3ebe5f1fb6ba7dcdff0f503`.

## Sole successor packet

Exact M4.32 owns only exception-safe receipt-handle-chain closure.

- **Locators:** `_close_receipt_handle_chain`; the exception cleanup in
  `_open_external_receipt_chain`; and the acquired/reacquired cleanup in
  `_load_external_receipt` in `reimplementation/ablpc/manifest.py`, plus the
  adjacent receipt tests in `tests/test_manifest.py`.
- **First pass:** reproduce the +7/+6 skipped-descriptor cases before editing.
  Make one owned-chain cleanup path attempt exactly one close for every file and
  directory descriptor even when an earlier close reports an error. Preserve
  the primary acquisition/read/reacquisition error; if cleanup itself is the
  only failure, report it deterministically and fail before parsing/source
  preparation. Add indexed close-error regressions for initial acquisition
  cleanup and both retained chains, with call-order, descriptor-attempt,
  snapshot, CLI-silence, and ordinary-success assertions.
- **Stop rule:** change only receipt-chain release/error propagation, exact
  synthetic tests, a manifest pin only if implementation bytes change, and
  documentation. Do not change component acceptance, receipt/manifest bytes,
  schemas, operations, mapping, guards, source/hash/output authority,
  replay/removal/mount behavior, statement membership, launcher, staged trees,
  assets, runtime, M2, PS1, transactions, or the clean-copy lifecycle.
- **Done when:** the exact first/second-close failures reproduce before the fix
  and afterward every owned descriptor receives one close attempt, later
  descriptors are never skipped, primary errors are retained, cleanup-only
  errors fail deterministically before mutation, ordinary and all retained
  gates above pass, one clean worker commit is ready for fresh-context audit,
  and M4, `KU-051`, and `KU-052` remain open.

## Limits

The result does not reopen the exact M4.29 parent acceptance bypass: that attack
is corrected at the worker boundary. It does not establish a general filesystem
transaction, post-preflight concurrency protection, authorship, provenance,
staged-tree removal, source restoration, package/backup/rollback behavior,
general launch/runtime automation, broader platform support, M2, PS1, or M4
completion. Because the verdict is `REJECT`, `KU-051` remains open and the
clean-derived-copy lifecycle is not selected.

## Successor disposition

[[EXP-20260814-091 - Exception-safe receipt-handle-chain closure]] completes
the exact M4.32 worker boundary. The +7/+6 baseline is reproduced before the
correction; indexed partial/reacquired/acquired cleanup now attempts each owned
descriptor once with zero final delta, primary errors remain primary, cleanup-
only failure precedes parsing, 161/223/411 tests pass, and all six local cycles
retain prior hashes. Exact M4.33 remains the required independent audit, so
this note's `REJECT`, `KU-051`, `KU-052`, and M4 remain open.
