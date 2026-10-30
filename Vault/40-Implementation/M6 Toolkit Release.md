---
type: implementation
status: accepted
updated: 2026-10-02
tags:
  - implementation/release
  - implementation/compatibility
  - milestone/m6
---

# M6 Toolkit Release

**Status (2026-10-02 audit):** M6 is Complete at its documented boundary.
[[EXP-20260814-110 - Independent M6 state-locked lifecycle acceptance audit]]
returned `ACCEPT`, and [[Project Roadmap]] lists M6 as Complete. The sections
below are the dated audit trail; their open/rejected wording describes the
state before that acceptance.

## Reopened boundary

`DEC-20260814-100` activates M6 and `DEC-20260814-101` records its initial
acceptance. Independent `EXP-20260814-106` supersedes closure with `REJECT` at
the installed lifecycle boundary. The reproducible asset-free artifact,
primary-host smoke, M4 compatibility, and explicit unsupported labels remain
intact; installed-tool inventory stability and installed path identity do not.

The machine contract is `reimplementation/release/m6-v1.0.0.json`. It names:

- executable and disc provenance hashes;
- exact selected PC data hashes;
- manifest schemas 1 and 2;
- exact M4 v0.1/v0.2 statement hashes;
- the primary x86_64 Linux/Python/Wine/Gamescope environment;
- three clean-copy smoke cases covering Training, Level 01, and schema 2;
- explicit renderer, display, input, audio, platform, filesystem, and Windows
  limitations.

## Release lifecycle

The builder admits only sorted, unique, regular non-link files from its clean
tracked allowlist. It fixes tar path order, epoch, owner/group, mode, and a
canonical path/size/hash inventory. Verification rejects unlisted content,
unsafe paths, links/nonregular entries, forbidden game/media suffixes, metadata
drift, byte drift, and contract disagreement.

Installation is intended to extract a verified archive to a new immutable
version directory and atomically record the selected version in canonical
`state.json`. The current implementation does not yet uphold that boundary:
normal installed wrapper use can create unlisted bytecode, linked release
roots are followed, and dangling `state.json` is treated as absent (closed by
EXP-20260814-109 and accepted by EXP-20260814-110, below). Neither
path reads, copies, backs up, restores, deletes, or otherwise changes game
files.

## Smoke boundary

The primary matrix checks the known executable and selected data hashes, the
active exact M4 v0.2 statement, and every one of the 21 PC `LEVEL*.DAT` files.
For each declared case it creates a disposable complete stage under
`work/copies/`, validates the hash-checking Wine/Gamescope launcher command,
restores through the accepted manifest/source M4 path, and compares a complete
file inventory to the clean source. It removes only its disposable temporary
copies after the case.

The automated result is launcher readiness and exact clean-copy restoration,
not execution, gameplay, renderer selection, input automation, audio output,
or a rendered compatibility claim. The four Direct3D log markers and
`INITSOFTRENDER` exclusion remain mandatory for separately controlled live
runs.

## Evidence status

- **Confirmed before M6:** supported PC hashes, M4 schemas/workflows, Wine/
  Gamescope launcher boundary, and M4 closure are cited in
  `EXP-20260814-103/104` and their predecessors.
- **M6 retained evidence:** two exact clean-source builds, canonical archive
  verification, the exact primary-host smoke matrix, M4 compatibility, and
  repository hygiene are independently retained in
  [[EXP-20260814-106 - Independent M6 release hard-truth audit]].
- **M6 rejected boundary:** installed wrapper execution changes the declared
  inventory; linked `releases/` and selected-version roots are accepted; and
  dangling `state.json` is replaced. Failure/rollback closure therefore
  remains open.
- **Unknown/untested:** Windows 98, modern Windows, non-x86_64 Linux, other
  versions/filesystems, automated gameplay, and all unlisted input hashes.

## Exact corrective boundary

- Suppress bytecode generation in every shipped Python entry point and prove
  ordinary installed use preserves the complete inventory.
- Inspect `state.json` without following or losing dangling links; reject any
  non-regular or linked identity before mutation.
- Require `releases/` and the selected version directory to be real directory
  entries rather than links before inventory traversal.
- Add full-snapshot regressions for all three cases, then retain every exact
  build, archive, smoke, M4, protected-content, and hygiene result before a
  fresh-context acceptance audit.

## Worker correction evidence

[[EXP-20260814-107 - M6 installed lifecycle identity correction]] is complete
at implementation commit `580a1cb`:

- three packaged shell entry points set `PYTHONDONTWRITEBYTECODE=1` and invoke
  Python with `-B`; the direct Python compatibility entry point disables
  bytecode before importing the package;
- state admission distinguishes true absence from dangling/nonregular identity
  with `lstat`;
- install/current/rollback authenticate lexical `releases/` and selected-
  version final entries as non-link directories before inventory traversal;
- one exact installed artifact runs all four entry points with external
  bytecode controls removed and preserves the complete 38-file snapshot;
- six focused failure surfaces covering dangling state, linked release root,
  and linked selected/current/prior versions reject without snapshot drift;
- two 389,120-byte builds match at `7a1ede97...fcd2`, source tree
  `fa6a3ee4...c85ea`; the exact 21-file/three-case smoke report is
  `1a8a3b57...323e`; and 492 tests plus all retained gates pass.

This is worker-complete, not milestone acceptance. M6 remains Active for a
fresh-context James audit.

## First James rejection and second worker correction

[[EXP-20260814-108 - Independent M6 lifecycle consistency hard-truth audit]]
rejects `EXP-107` at exact HEAD `23ff833`. The original three failures close,
but a 55-case matrix exposes 20 improper successes and 12 snapshot changes;
9/10 adjacent inventory attacks pass; and a hostile in-tree bytecode prefix
writes 30 files before the direct Python script can disable caching.

[[EXP-20260814-109 - M6 state-locked lifecycle consistency correction]] closes
that combined worker boundary at clean HEAD `7d8594e`:

- the direct checker requests `-B` in its interpreter shebang;
- existing state/release topology is validated before any directory creation;
- canonical state and installed files are single-link, package/release topology
  and directory/file modes are exact, and all retained versions validate on
  every lifecycle operation;
- canonical state schema 2 records each version's verified archive, manifest,
  and tree digests, preventing content-plus-in-tree-manifest rebaselining;
- safe unique state temporaries never remove a pre-existing collision;
- 30 focused release and 509 canonical tests pass; dual artifact, hostile-
  cache entry point, exact smoke, M4, Vault, protected-content, and clean-tree
  gates pass.

Independent [[EXP-20260814-110 - Independent M6 state-locked lifecycle acceptance audit]]
returns `ACCEPT` at exact clean audited HEAD `64d8ac1`. James reproduces 55/55
lifecycle and 10/10 installed-inventory refusals with complete snapshots
unchanged, bytecode-free execution of every installed entry point, matching
`68d3d31a...060b` artifacts, all 13 strict archive refusals, exact smoke
`c1fb6903...98dc`, 509 tests, five M4 anchors, Vault 312/0/0, and clean tracked
state. M6 is Complete only at the documented asset-free Fedora/Wine launcher-
readiness and local-state-trust boundary. Every listed unsupported surface
remains unsupported.

## User-facing documentation

See `reimplementation/M6-RELEASE.md` and the root `README.md`.
