---
type: experiment
id: EXP-20260814-097
date: 2026-08-14
question: Does immutable M4.37 reject every complete-tree path collision in the project casefold model before unsafe restoration reads or mutation while retaining the accepted lifecycle?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; synthetic fixtures, private mount namespaces, and exact user-owned ignored local recipe checks
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: immutable M4.37 worker 8e73a7f5d513bb2534ed16b74ce1027e2d643039 with exact direct docs-only M4.36 parent 7180e4a7d41e125307a2b32a3f1f6cb726d20b3d; audit and documentation only; launcher dry-run only; no game execution
artifacts:
  - reimplementation/ablpc/manifest.py
  - reimplementation/ablpc/compatibility.py
  - tests/test_manifest.py
  - tests/mount_overlay_case.py
  - reimplementation/compatibility/m4-v0.1.json
  - scripts/play-pristine.sh
  - Vault/30-Experiments/EXP-20260814-095 - Independent M4.35 clean-copy-restoration hard-truth audit.md
  - Vault/30-Experiments/EXP-20260814-096 - Complete-tree case-insensitive path uniqueness.md
addresses: []
file_offsets: []
result: accept-exact-m4.37-complete-tree-casefold-uniqueness
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
---

# EXP-20260814-097 - Independent M4.37 complete-tree-uniqueness hard-truth audit

## Verdict

**ACCEPT.** Immutable worker
`8e73a7f5d513bb2534ed16b74ce1027e2d643039`, directly above docs-only M4.36
verdict `7180e4a7d41e125307a2b32a3f1f6cb726d20b3d`, satisfies exact M4.38.
No surviving counterexample reaches staged-tree content reads or restoration
mutation, and no retained M4.36 lifecycle, mount, sparse, compatibility, M1,
or hygiene boundary is weakened.

This acceptance resolves `KU-052` only for the demonstrated manifest-driven
current-x86_64-Linux lifecycle: exact-source `stage`, pinned-launcher
`--dry-run` validation, and exact-manifest/source `restore` of that same
complete derived tree. It does not establish automatic runtime launch,
external-receipt full-tree restoration, staged-tree/source deletion, backup,
rollback, package, transaction, provenance, POSIX metadata equality, or a
post-preflight concurrency guarantee. M4 remains active because the unchanged
v0.1 compatibility statement still declares restoration unsupported.

## Immutable gate and parent reproduction

The first read found exact HEAD `8e73a7f5d513bb2534ed16b74ce1027e2d643039`,
exact direct parent `7180e4a7d41e125307a2b32a3f1f6cb726d20b3d`,
and empty short/porcelain Git status. The complete startup packet, full
Roadmap and exact M4.38 packet, full Decision Log and Known Unknowns, relevant
MOCs, operating/charter/environment state, EXP-095/096, M4/M1 notes, root
1249 session, launcher, both READMEs, complete worker diff, and all 7,509 lines
of the changed compatibility/manifest/test files were reviewed before testing.

A disposable `git archive` of the exact parent independently reconstructed
ordinary files `UNRELATED/Case.bin` and `UNRELATED/case.bin`. Parent `stage`
created the complete tree and parent `restore` returned success, removed
`.ablpc`, preserved the source, and left the staged tree exactly equal to the
ambiguous source. No checkout or HEAD change was used.

## Independent casefold and traversal oracle

The separate oracle recursively uses no-follow directory-entry metadata,
classifies every file/directory/symlink/nonregular entry, records regular-file
link count and SHA-256, and assigns `relative.as_posix().casefold()` without
calling the worker inventory. It found the expected collision in every attack
and no collision in the unique mixed-case controls.

Thirty-six fresh current-worker cases passed: nine shapes across source and
staged-game trees in both authored/creation orientations. They include root
and nested sibling file/file, directory/directory, both file/directory
orientations, nested leaf and ancestor cases, plus Unicode `Straße`/`STRASSE`
file and directory pairs within the established project `casefold()` model.
All refuse deterministically with complete recursive source/game snapshots
exact. Source cases trap all manifest preparation, mount planning, content
reads, atomic writes, unlinks, and directory removals. Staged-game cases allow
the retained source preparation and mount preflight, but trap every staged or
stable restoration content read, write, unlink, and directory removal.

Every sibling key is validated before descent. Four stronger private-namespace
cases make one of the colliding `CASE`/`case` directories a bind-mounted
independent tree, for source and staged-game collisions with the mount in both
the lexically first and lexically second spelling. Neither ambiguous branch is
visited. Complete source, game, and external snapshots remain exact in all
four cases. A unique `MiXeD/Leaf.BIN` plus unpaired Unicode path restores and
matches the independent content oracle; POSIX permission/time equality remains
explicitly outside the claim.

## Retained refusals and namespace families

The checked-in ordinary controls pass 33/33 across schemas 1/2, all three M1
operations, multi-file/composed restoration, `.ablpc`, source/manifest/output/
receipt and unrelated drift, symlink, FIFO, hard-link, collision, branch-order,
and CLI behavior. Three exact root relationships—same root, game below source,
and source below game—refuse unchanged. Five injected same-byte inode swaps at
source output, source unrelated, staged output, staged receipt, and staged
unrelated paths all raise the stable-read identity error; the independent
path/type/content oracle remains exact and the receipt remains present.

All eight M4.36 private-namespace families pass with complete snapshots or the
specified success oracle:

- staged game root, recorded output, receipt, and unrelated-file mounts refuse
  unchanged at 4/4;
- a proper-parent alias and mounted unrelated directory refuse unchanged;
- a distinct ordinary top mount hides the lower same-path alias and ordinary
  restoration succeeds without touching the hidden tree; and
- freed mountinfo ID `1185` is reused by a later alias below still-mounted
  source ID `1186`; explicit later order identifies the `1185` alias and
  refuses it unchanged.

As in M4.36, unmounted character-device creation is denied by the environment,
even in a mapped-root namespace. This is not counted as an unmounted-device
pass. Two actual bind-mounted `/dev/null` character-device cases, one in each
source/game tree, independently refuse as nonregular with exact snapshots.

## Exact local lifecycle and sparse retention

One disposable directory below `work/copies/` repeats the exact user-owned
lifecycle without executing the game. The clean source has 722 files and 26
directories including root and a collision-free independent oracle digest of
`76513235f30d3096760e0f49ea751bc195589f348c1903b16887b71f21f83346`.
`stage` creates 723 files and 27 directories including receipt metadata.
Receipt SHA-256 is
`ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63`,
and the opaque output is
`6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.
The pinned launcher `--dry-run` returns zero and verifies executable SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
`restore` returns the same receipt, removes `.ablpc`, leaves the game oracle
equal to source, preserves the complete source snapshot, and cleanup removes
the disposable tree.

All six retained sparse apply/remove cycles pass twice per family with absent
output roots and unchanged source hashes:

| Family | Receipt SHA-256 | Output SHA-256 |
|---|---|---|
| opaque | `ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63` | `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4` |
| same-DAT composition | `b899907eec17020f9e7a303b9cd8b5620dc70e83051840d13d57df80b6c779ef` | `78cca99b1993cc6deff8f89104d6f6aa8154ed7063e4ab0b56195e4321761d9a` |
| M1 plus opaque | `f8e144521905cc978e560e01158fae983495693f556f069773c8fac136c815b5` | DAT `b8012a95f7ec0254805bdd3cf32df2b16f2ad0926308fe8678cc2360027f720e`; opaque `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4` |

Training DAT, opaque destination, and replacement source retain exact SHA-256
`494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`,
`a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`,
and `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.

## Compatibility, tests, and hygiene

The five exact machine pins pass, including manifest implementation SHA-256
`b3480761ac2b4791ccbf1df69f88234532f27956152045b89615dd5ec5bf6d75`.
Independent read tracing observes exactly nine unique tracked asset-free paths:
the statement, three manifests, launcher, manifest implementation,
Environment Status, Wine baseline, and reimplementation README. The unchanged
statement remains 6,177 bytes at SHA-256
`c3427d44cf32619a1f9bbcab7c51e67c0846b35d9d53eab7632ff6356c0beaf0`
and still contains `staged-tree-or-source-removal-and-restoration` in its
unsupported list.

Focused manifest/restoration, combined manifest/M1/compatibility, and canonical
suites pass 198/198, 260/260, and 448/448. Final `make check`, Vault lint,
tracked-file, diff/MIME, protected-root, and no-game-byte gates pass after the
documentation-only verdict commit; Git is clean.

## Sole successor

Only exact M4.39 follows: publish a new strict M4 v0.2 compatibility statement
that preserves v0.1 as historical evidence and adds only the independently
accepted manifest-driven restoration boundary. It may align the checker,
tests, and scoped human documentation, but may change no manifest behavior,
receipt/schema/operation, hash/input authority, sparse or mount behavior,
launcher, asset/runtime/M2/PS1 surface, or unsupported deletion/transaction/
automation claim. M4 is not complete at this M4.38 edge.

## Successor disposition

[[EXP-20260814-098 - Strict v0.2 restoration compatibility statement]]
completes that exact worker packet. Historical v0.1 remains byte-identical;
canonical v0.2 adds only this audit's accepted restoration boundary; five pins,
exactly nine asset-free reads, and every unsupported limit survive. M4 remains
active pending exact independent M4.40 rather than completing at the worker
edge.
