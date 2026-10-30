---
type: experiment
id: EXP-20260814-093
date: 2026-08-14
question: Can one current tool-created clean derived tree complete manifest installation, exact validation, launcher preflight, and supported removal without combining different trees?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; fresh synthetic complete trees plus exact user-owned ignored local recipe checks
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M4.34 audit of immutable M4.33 verdict 1ddb12850a48e4501d60688c6071c7ce2fed8ba1 and direct M4.32 worker e396ab0e90ede2dd29f4c7b98fd434ed867236a5; no game execution or implementation/test/schema/receipt/launcher change
artifacts:
  - reimplementation/ablpc/manifest.py
  - reimplementation/ablpc/cli.py
  - scripts/play-pristine.sh
  - reimplementation/compatibility/m4-v0.1.json
  - Vault/30-Experiments/EXP-20260814-086 - M4 v0.1 milestone-closure evidence audit.md
  - Vault/30-Experiments/EXP-20260814-092 - Independent M4.32 receipt-chain-closure hard-truth audit.md
addresses: []
file_offsets: []
result: reject-m4-closure-no-current-full-tree-restoration-join
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/modding
  - audit/hard-truth
---

# EXP-20260814-093 - Clean-derived-copy lifecycle feasibility audit

## Verdict

**REJECT M4 completion.** No current tool-created output tree satisfies all
four required lifecycle verbs on that same tree. The two complete-tree routes
are structurally launchable when placed below `work/copies/`, but authenticated
removal rejects their required unrelated game content. The two supported
removal routes are exact dedicated sparse trees and therefore lack the
executable and the rest of the game.

The sole smallest missing join is manifest/source-authenticated restoration of
one complete `stage`-produced derived game tree. This is not a reason to weaken
the accepted exact sparse-tree check, broaden the launcher, delete a staged
tree, or combine evidence from separate outputs.

## Immutable and safety boundary

The audit began from clean exact HEAD
`1ddb12850a48e4501d60688c6071c7ce2fed8ba1`, the documentation-only M4.33
`ACCEPT` verdict directly above worker
`e396ab0e90ede2dd29f4c7b98fd434ed867236a5`. The complete startup sequence,
M4.34 packet, M4.27 ledger, M4.33 evidence, `KU-052`, manifest/CLI/launcher
implementation, compatibility statement, M1/M4 notes, Wine baseline, and both
READMEs were reviewed.

The executable was not run. Synthetic fixtures used the explicit non-game
placeholder SHA-256
`d1c7309fa6d62415b764fe87beaa1363baebbb5c524fde502fd0aa20236d8c18`.
No original, media, protected root, external PS1 source, implementation, test,
schema, operation, receipt, pin, compatibility statement, launcher, or local
game-copy byte changed. All synthetic roots were isolated and removed.

## Independent four-route same-tree ledger

One schema-2 synthetic manifest replaced `CD/DATA/BASE.BIN` from the distinct
exact source `CD/DATA/REPLACEMENT.BIN`. The complete source also contained
`bugs.exe`, `config.ini`, and unrelated `CD/UNRELATED/KEEP.DAT`. A write-free
dry run returned report schema 1 and output SHA-256
`8323e5787d0d13fc0830d538d1013f24bef8226949caa9af521e9bf5809f7e2d`.
Every install route returned the same ordinary receipt and the recorded output
matched that hash.

| Same output tree | Install and exact validation | Launcher preflight on that tree | Supported removal on that tree | Verdict |
|---|---|---|---|---|
| `stage` below an isolated `work/copies/` path | Complete tree; exact output/receipt; synthetic executable byte-identical to source | Passed the `work/copies` and executable-presence gates, then refused only the deliberately wrong synthetic executable hash; `stage` preserves a real accepted source executable identically | `remove` returned status 2 with empty stdout: `overlay contains extra content: CD/DATA/REPLACEMENT.BIN`; complete no-follow tree snapshot unchanged | Complete and structurally launcher-ready, not removable |
| ordinary sparse `apply` | Exact six-entry topology: root, `.ablpc`, receipt, `CD`, `CD/DATA`, and one output | `bugs.exe` absent, so not a complete launch input | Manifest-driven removal returned status 0 and removed the root completely | Removable, not launchable |
| `apply --force` into a full clean copy | Complete tree; exact output/receipt; synthetic executable byte-identical to source | Passed the `work/copies` and executable-presence gates, then refused only the synthetic executable hash | Same status-2/empty-stdout extra-content refusal; complete no-follow snapshot unchanged | Complete and structurally launcher-ready, not removable |
| strict receipt replay | Receipt byte-equal to all other routes; same dedicated sparse topology | `bugs.exe` absent, so not a complete launch input | Receipt-driven removal returned status 0, removed the root completely, and preserved the external receipt | Removable, not launchable |

The source's complete no-follow snapshot remained exact across the matrix. The
documented `work/mod-builds/` stage location was also passed to launcher dry
run and refused at status 2 with empty stdout specifically because it is
outside `work/copies/`. This documentation/path mismatch is real but not the
causal blocker: `stage` already permits a new root below `work/copies/`; that
same complete tree still lacks a supported removal/restoration operation.

## Why existing removal must not be reused

`remove_manifest` and `remove_receipt` authenticate a dedicated sparse tree:
the only permitted entries are recorded outputs, the ordinary receipt, and
their necessary directories. They then unlink those outputs and the receipt
and remove the empty root. A complete game tree necessarily violates the
no-extra-content contract, and deleting only its modified destination would
leave the game incomplete rather than unmodified. Accepting extra content or
pointing this deletion operation at a complete tree would weaken an
independently accepted safety boundary.

The missing action is restoration, not sparse deletion: authenticate the
complete derived tree against the exact clean source and ordinary receipt,
replace only recorded destinations with their exact source bytes, remove the
receipt, and leave the same full tree equivalent to the clean source.

## Retained gates

The exact canonical suite passes 411/411. `make m4-compatibility` reports the
unchanged `ablpc-m4-compatibility-v0.1` statement with five hash anchors. All
three exact user-owned local families completed two ordinary apply, external-
receipt replay, byte-equality, receipt-driven removal, and manifest-driven
removal cycles in disposable roots:

| Family | Cycles | Receipt SHA-256 | Replayed output SHA-256 |
|---|---:|---|---|
| exact opaque replacement | 2/2 | `ab0cb8dddab84d75f7e6fd22ee203becaf49d529cb615eadaeb84046d0261a63` | `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4` |
| same-DAT composition | 2/2 | `b899907eec17020f9e7a303b9cd8b5620dc70e83051840d13d57df80b6c779ef` | `78cca99b1993cc6deff8f89104d6f6aa8154ed7063e4ab0b56195e4321761d9a` |
| M1 plus opaque | 2/2 | `f8e144521905cc978e560e01158fae983495693f556f069773c8fac136c815b5` | DAT `b8012a95f7ec0254805bdd3cf32df2b16f2ad0926308fe8678cc2360027f720e`; opaque `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4` |

The source hashes remained Training DAT
`494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`,
opaque destination
`a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`,
and replacement
`6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.
No local output survived. Final `make check` reports Vault lint 279 notes with
zero errors/warnings, the exact five-anchor compatibility statement, 411/411
canonical tests, and zero tracked-file violations.

## Limits

This is a structural lifecycle audit, not a game run or new runtime claim. It
does not establish a general full-tree validator, provenance, authorship,
package, backup, rollback, transaction, post-preflight concurrency protection,
receipt-only full-tree restoration, staged-tree deletion, source deletion,
launcher automation, broader platform support, M2, or PS1 correspondence.

## Sole successor

Exact M4.35 is manifest-driven clean-copy restoration. It must add one bounded
`restore MANIFEST --source-root SOURCE --game-root ROOT` path for an exact
`stage`-produced complete tree. Before mutation it must recompute the ordinary
receipt/output from the manifest and exact source, require a complete no-follow
tree equivalent to source except for recorded outputs and the receipt, require
those outputs/receipt exact, and reject unsafe topology or drift with complete
snapshots unchanged. Success restores only recorded destinations from source,
removes the receipt and empty `.ablpc`, preserves the source, and leaves the
same complete game root content-equivalent to the clean source. It must not
change sparse removal, receipt bytes/schemas, launcher policy, or claim
transaction/rollback behavior.

## Disposition by M4.35

[[EXP-20260814-094 - Manifest-driven clean-copy restoration]] completes the
selected worker. The new manifest-driven path authenticates the complete
source/game tree and every expected mount path before restoring only recorded
destinations and removing receipt/empty `.ablpc`. Twenty-seven focused
instances, 188/250/438 suites, six retained sparse local cycles, and one exact
722-file launcher-dry-run lifecycle pass. This note's M4.34 `REJECT` remains
the parent baseline; exact M4.36 must independently accept the correction.
