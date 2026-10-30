---
type: experiment
id: EXP-20260814-094
date: 2026-08-14
question: Can an exact staged complete tree be authenticated against its manifest and clean source, restored without weakening sparse removal, and refused unchanged on every deterministic mismatch?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; synthetic fixtures, private mount namespaces, and one exact user-owned ignored full-tree lifecycle dry-run
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.35 worker directly above M4.34 verdict a8012745183124d5ed84fe915a5867cbb2b8146b; no game execution, original/media/PS1 access, or sparse-removal/receipt/schema/launcher change
artifacts:
  - reimplementation/ablpc/manifest.py
  - reimplementation/ablpc/cli.py
  - reimplementation/ablpc/compatibility.py
  - tests/test_manifest.py
  - tests/mount_overlay_case.py
  - Vault/30-Experiments/EXP-20260814-093 - Clean-derived-copy lifecycle feasibility audit.md
addresses: []
file_offsets: []
result: worker-complete-manifest-driven-full-tree-restoration
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - implementation/manifest
---

# EXP-20260814-094 - Manifest-driven clean-copy restoration

## Worker result

Exact M4.35 is worker-complete. The new command is:

```text
ablpc-mod restore MANIFEST --source-root SOURCE --game-root ROOT
```

It recomputes the unchanged ordinary manifest preparation and receipt from the
exact source. Before the first write or unlink it inventories source and game
without following links, requires regular single-link files, rejects reserved
source `.ablpc` content, and requires the complete game tree to be path/type/
content-equal to source except for recorded destinations and the one ordinary
receipt. Every recorded game destination must match the recomputed output hash
and the receipt must match ordinary stage bytes exactly.

The current-Linux mount preflight now has a shared internal core with unchanged
sparse-removal messages/behavior. Restoration supplies every source-derived
game directory/file plus the receipt, so a mountpoint at the game root, a
recorded output, the receipt, or even an unrelated retained file refuses before
tree traversal or mutation. Proper-parent mount aliases also fail closed.

Success writes only the exact source bytes for recorded destinations, removes
`.ablpc/receipt.json`, removes the now-empty `.ablpc`, returns the authenticated
receipt, and leaves the same complete game root content-equivalent to the clean
source. It never writes the source or deletes the game root.

## Exact boundary and implementation locators

- `restore_manifest` in `reimplementation/ablpc/manifest.py` owns the new
  manifest/source/game entry point and success mutation list.
- `_regular_tree_inventory` rejects symlink, FIFO/nonregular, and multi-link
  file topology without following links.
- `_read_stable_tree_file` normalizes read errors and rejects deterministic
  file identity/type/size/time changes during preflight.
- `_validate_complete_staged_tree` owns exact whole-tree path/type/content,
  output-hash, and ordinary-receipt equality.
- `_validate_unmounted_restoration_plan` reuses the accepted Linux mount
  enumeration/ordering classifier over every expected full-tree path.
- `reimplementation/ablpc/cli.py` adds only the `restore` parser/dispatch.

Existing `remove` and `remove-receipt` remain dedicated sparse deletion. No
manifest/receipt byte, schema, format, edit operation, source/hash/guard/output
authority, apply/stage/replay behavior, launcher policy, or statement
membership changes. Only the closed-world manifest implementation pin changes,
to `4707c93e5d57b7d8b833547bb3c5d7e5c0b735ba1c772ceb3e43a5546e2b004d`.

## Synthetic and namespace evidence

Twenty-seven focused test instances cover more than one behavior in the
multi/composed and CLI cases:

| Family | Result |
|---|---|
| exact opaque staged tree | restores to source content; source exact; receipt metadata absent |
| schemas 1/2 × position, field-`0x0C`, payload-target | 6/6 restore to source content |
| two-output opaque and exactly-two-input composed M1 trees | 2/2 restore to source content |
| unrelated extra/missing/changed/symlink/FIFO/hardlink | 6/6 refuse with complete source/game snapshots exact |
| source, manifest name, output, receipt authority drift | 4/4 refuse unchanged |
| reserved `.ablpc` and source symlink/FIFO/hardlink | 4/4 refuse unchanged |
| CLI success plus extra-content failure | success returns receipt; failure status 2/empty stdout and exact snapshots |
| private-namespace game root/output/receipt/unrelated bind mount | 4/4 refuse with source/game/external snapshots exact |

Focused `tests/test_manifest.py` passes 188/188. Manifest + LEVEL +
compatibility passes 250/250. Canonical `.venv/bin/python -m pytest -q tests`
passes 438/438. These totals retain existing component-stable receipt input,
exhaustive descriptor closure, schemas/operations, dry-run, apply/stage/replay,
sparse removal/mount handling, composition, and M1 behavior.

Final `make check` reports Vault lint 281 notes with zero errors/warnings, the
valid five-anchor statement, 438/438 canonical tests, and zero tracked-file
violations. The statement remains exact at SHA-256
`c3427d44cf32619a1f9bbcab7c51e67c0846b35d9d53eab7632ff6356c0beaf0`;
the same five machine authorities and nine asset-free reads remain in scope.

## Exact full-tree local lifecycle

One disposable tree below `work/copies/` used the exact tracked opaque manifest
and the user-owned 722-file/26-directory source. `stage` produced receipt
SHA-256
`ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63`
and replacement output SHA-256
`6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.

`scripts/play-pristine.sh --dry-run --game-dir ...` returned status 0, printed
the command, and reported the exact accepted executable SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
The game was not executed. `restore` returned the same receipt, removed
`.ablpc`, and left all 722 file path/size/content-hash/link tuples and 26
directory paths equal to the source snapshot. The source snapshot remained
exact and the disposable tree was removed.

All three retained local sparse families also completed twice with their prior
receipt/output hashes:

- opaque receipt
  `ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63`
  and output
  `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`;
- same-DAT receipt
  `b899907eec17020f9e7a303b9cd8b5620dc70e83051840d13d57df80b6c779ef`
  and output
  `78cca99b1993cc6deff8f89104d6f6aa8154ed7063e4ab0b56195e4321761d9a`;
  and
- M1+opaque receipt
  `f8e144521905cc978e560e01158fae983495693f556f069773c8fac136c815b5`
  with outputs
  `b8012a95f7ec0254805bdd3cf32df2b16f2ad0926308fe8678cc2360027f720e`
  and `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.

Source hashes remain exact at Training DAT
`494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`,
opaque destination
`a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`,
and replacement
`6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`;
no disposable output remains.

## Limits

The validator proves path/type/content equivalence, not POSIX permission/time
metadata equivalence or provenance/authorship. Source trees with `.ablpc`,
symlinks, nonregular files, or multi-link files are outside this exact command.
Like accepted apply/stage/remove, deterministic preflight is complete but
unexpected post-preflight permission, storage, or concurrent I/O failure is
not transactional and can leave partial restoration.

This worker does not add external-receipt full-tree restoration, whole staged-
tree deletion, source deletion, backup, rollback, package, transaction, general
launch automation, game runtime evidence, broader platform support, M2, or
PS1. The v0.1 statement remains conservatively unchanged until independent
acceptance; it still lists staged/source restoration among unsupported
surfaces. M4 and `KU-052` therefore remain open at the worker boundary.

## Sole successor

Exact M4.36 is the independent hard-truth audit of immutable M4.35. It must
reproduce the parent full-tree extra-content refusal, independently derive and
attack the worker's complete-tree equivalence/mount/mutation plan, repeat the
actual local stage/launcher-dry-run/restore lifecycle without executing the
game, retain sparse/local/compatibility/canonical gates, and return one verdict.
`ACCEPT` may resolve `KU-052` for this exact manifest-driven current-Linux
boundary, but must select a separate compatibility-statement alignment packet
before M4 completion because the machine statement deliberately remains
conservative at the unverified worker edge.

## Independent disposition

[[EXP-20260814-095 - Independent M4.35 clean-copy-restoration hard-truth audit]]
returns `REJECT`. It retains the parent's full-tree refusal, the ordinary and
drift/mutation boundaries, eight namespace cases, the exact 722-file local
lifecycle, all six sparse cycles, five pins/nine reads, and 188/250/438 tests.
The omitted boundary is case-insensitive complete-tree path uniqueness:
distinct source/game files `Case.bin` and `case.bin` coexist and restore
successfully. M4 and `KU-052` remain open; exact M4.37 owns only that
correction, and the compatibility statement remains unchanged.
