---
type: experiment
id: EXP-20260814-105
date: 2026-08-14
question: Can M6 reproducibly release the completed M4 toolkit, pass the primary-Linux clean-copy matrix, and preserve state across migration and rollback failures without protected content or broader compatibility claims?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; exact local derived PC work copy; asset-free tracked release source and synthetic temporary install repositories
environment_version: kernel 7.0.11-200.fc44.x86_64; x86_64; Python 3.14.6; Wine 11.0 Staging; Gamescope 3.16.25-1.fc44.x86_64; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact M6 final clean HEAD 5daee2bc78f2fb35e06aa3e8b444b5e413f37a4c; source game tree work/copies/BUGS_PC-full-disc/PC/BUGS; Wine prefix work/wine/baseline; complete staged copies below disposable work/copies/m6-smoke-*; no executable launch
artifacts:
  - reimplementation/release/m6-v1.0.0.json
  - reimplementation/M6-RELEASE.md
  - reimplementation/ablpc/release.py
  - reimplementation/ablpc/smoke.py
  - tests/test_release.py
  - tests/test_smoke.py
  - work/releases/a/ablpc-toolkit-v1.0.0.tar
  - work/releases/b/ablpc-toolkit-v1.0.0.tar
  - work/m6-smoke-report.json
addresses: []
file_offsets: []
result: accept-exact-asset-free-primary-linux-release-boundary
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - implementation/release
  - implementation/compatibility
  - milestone/m6
---

# EXP-20260814-105 - M6 asset-free release lifecycle

## Subsequent disposition

Independent [[EXP-20260814-106 - Independent M6 release hard-truth audit]]
supersedes this experiment's milestone-closure verdict with `REJECT`. The
archive and smoke results below remain reproduced, but the isolated installed-
wrapper and complete failure/rollback claims do not survive normal bytecode,
linked release-root, and dangling-state attacks. M6 is Active again.

## Verdict

**ACCEPT.** M6 satisfies all four exit gates at one explicitly
bounded result: an asset-free toolkit release and a launcher-readiness smoke
matrix on the named primary x86_64 Fedora Linux configuration. M6 is Complete
at this boundary.

The result does not establish game execution, automated renderer/menu/level/
gameplay input, rendered output, audio playback or measurement, game-file
backup/rollback, Windows behavior, non-x86_64 behavior, other Wine/Gamescope/
kernel/filesystem versions, unlisted hashes, provenance signing, or external
publication.

## Question

Can the completed M4 source produce one reproducible protected-material-free
release, validate representative clean-copy workflows across both manifest
schemas, and migrate/roll back installed toolkit versions while all failure
paths preserve their declared state?

## PC and contract anchors

- PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Original disc SHA-256:
  `b0c3da82688c511f920a5559bdc3dcb8354d253182790a239665c8cd080d9ed9`.
- Training `CD/LEVEL07/LEVEL1.DAT` SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`.
- Level 01 `CD/LEVEL01/LEVEL.DAT` SHA-256:
  `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`.
- M4 v0.1/v0.2 SHA-256:
  `c3427d44cf32619a1f9bbcab7c51e67c0846b35d9d53eab7632ff6356c0beaf0`/
  `dacfcab8c1d27e5a63db870f347eb08701f868ca678cafdd178913266f20ccb2`.
- Final clean implementation HEAD:
  `5daee2bc78f2fb35e06aa3e8b444b5e413f37a4c`.

## Pre-closure contradiction and correction

The first worker commit `f4e94e4` validated member paths, types, sizes, modes,
hashes, and tar metadata. Adversarial review found one concrete contradiction:
a standard tar reader may stop at valid end markers and ignore subsequently
appended undeclared bytes. Member-only verification could therefore accept an
archive that carried bytes outside its declared inventory.

Corrective commit `5daee2b` makes verification reconstruct the complete
canonical tar from the strict archived spec/inventory/content and require the
input archive to match those bytes exactly. It also caps archive/member/spec/
state sizes, rejects noncanonical member spellings, checks installed inventory
order and state IDs, and adds exact Fedora distribution/kernel admission.
Appended-byte verification and install now reject with the existing install
snapshot unchanged. No protected bytes were used in this discriminator.

## Reproducible release result

Two sequential builds into distinct ignored directories from the same clean
tracked HEAD produced byte-identical output:

| Property | Observed |
|---|---|
| archive name | `ablpc-toolkit-v1.0.0.tar` |
| archive size | 378,880 bytes |
| archive SHA-256 | `1527281c60d1dd13ad0342a4cef9c8851d882a1cc1301083962f323ed64b62a0` |
| source-tree SHA-256 | `423eb946c35b2cc37a2642f9fb69e09304481972529ae63959e18c97dafeada7` |
| declared source files | 36 |
| generated files | one canonical `RELEASE-MANIFEST.json` |
| byte comparison | exact match |

The builder independently proves every declared input is tracked and unchanged
from HEAD. Strict verification reconstructs the exact paths, sorted inventory,
fixed epoch, root owner/group, `0644`/`0755` modes, sizes, hashes, and complete
tar encoding. It rejects protected top-level paths, forbidden game/media
suffixes, links, nonregular entries, duplicate/unsafe/noncanonical paths,
missing/extra content, metadata drift, content drift, appended bytes, and
contract disagreement. `scripts/audit-tracked-files.py` reports 0 violations.

## Primary-Linux clean-copy matrix

The exact admitted host is Fedora Linux 44 Workstation, kernel
`7.0.11-200.fc44.x86_64`, x86_64, Python 3.14.6, Wine 11.0 Staging, and
Gamescope package `3.16.25-1.fc44.x86_64`. The matrix first validates the known
executable, four selected data hashes, active M4 v0.2, and all 21 PC
`LEVEL*.DAT` files.

| Case | Schema | Complete workflow | Result |
|---|---:|---|---|
| Training record-124 target rebind | 1 | stage -> launcher dry-run -> restore | PASS |
| Level 01 record-261 target rebind | 1 | stage -> launcher dry-run -> restore | PASS |
| Training character whole-file replacement | 2 | stage -> launcher dry-run -> restore | PASS |

Each stage is a disposable complete tree under `work/copies/`. The launcher
verifies the executable and constructs the exact 1280x960 windowed research,
640x480 game-surface, `fit`/`nearest`, private-null-sink command. Each restore
returns the expected receipt and the restored tree equals the original
747-entry directory/file-size/file-hash inventory. The source inventory also
remains exact after all three cases, and all disposable stage trees are gone.
The report is 3,978 bytes at SHA-256
`2f015813cf9c2891ba46881d3c48c8bc980578948d248540b4bd386a64237eb1`.

This is launcher readiness only. The game was not executed. Hardware selection
remains manual, and a separate live run still requires all four Direct3D log
markers and no `INITSOFTRENDER`.

## Migration, rollback, and failure results

- A verified real v1.0.0 artifact installs in an isolated temporary root, its
  installed `ablpc-mod` and `ablpc-release` wrappers run through system
  `python3` without the repository venv, and its complete installed inventory
  verifies.
- A synthetic clean tracked v0.9.0 -> v1.0.0 sequence retains v0.9.0 in the
  rollback list; rollback verifies and selects it while leaving both immutable
  version directories present.
- Corrupt archive, canonical archive plus appended bytes, no-history rollback,
  and tampered-prior rollback each reject. Exact state/install snapshots remain
  unchanged in every declared failure case.
- Toolkit rollback modifies only canonical asset-free `state.json`; it never
  reads or changes a game tree and is not game backup or rollback.

## Validation

| Gate | Result |
|---|---|
| release/smoke focused tests | 10/10 pass |
| migration/corrupt/no-history/tampered-prior focused rerun | 3/3 pass |
| canonical `.venv/bin/python -m pytest -q tests` | 486/486 pass |
| M4 v0.2 compatibility | valid, five anchors unchanged |
| Vault lint | 304 notes, 0 errors, 0 warnings with closure notes |
| tracked protected-material audit | 0 violations |
| two clean-source artifact builds | exact byte match |
| strict artifact verification | pass |
| primary-host three-case smoke matrix | 3/3 pass |
| isolated installed artifact wrappers | pass without repository venv |
| diff, staged diff, and clean-tree gates | pass before closure notes |

## Exit-gate ledger

| M6 exit gate | Disposition |
|---|---|
| Reproducible tracked-source artifacts without protected material | **Supported:** exact dual-build hash/size/tree identity, canonical verification, and tracked audit. |
| Documented primary-Linux smoke matrix | **Supported at launcher-readiness scope:** exact admitted host, 21/21 parsers, three schemas/scopes workflows, complete inventories. |
| Failure and rollback paths exercised | **Supported for asset-free toolkit selection:** successful two-version rollback and four snapshot-preserving failure families. |
| Windows 98 controlled claims or explicit untested label | **Supported by explicit absence:** no Windows run or claim; Windows 98 and modern Windows are named untested. |

## Interpretation

- **Confirmed:** the exact release bytes, source-tree digest, allowlist,
  primary-host matrix, clean-copy restoration, installed wrappers, and bounded
  toolkit rollback/failure results above.
- **Inferred:** none needed for the M6 verdict.
- **Unknown/untested:** every limitation named in the machine contract and
  verdict remains outside this experiment.

## Result

`ACCEPT`: close M6 only at the exact asset-free primary-Linux release and
launcher-readiness boundary. No successor milestone begins.
