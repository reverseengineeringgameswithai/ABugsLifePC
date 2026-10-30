---
type: cross-port-comparison
id: XPORT-20260816-003
status: completed
confidence: high
pc_binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
external_source_id: SRC-PS1-ABL
external_commit: 1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51
external_paths:
  - ObsidianVault/Canon/Systems/
pc_evidence:
  - Subsystem Coverage Map
external_evidence:
  - ObsidianVault/Canon/Systems/ (115 SYS_*.md notes at the cited commit)
created: 2026-08-16
updated: 2026-08-16
tags:
  - re/cross-port
  - research/provenance
---

# XPORT-20260816-003 - Subsystem inventory seeding

## Bounded question

The ABLPC roadmap tracks capability milestones and [[Subsystems MOC]] indexes
found PC evidence, but neither enumerates the subsystems the game plausibly
contains, so blank areas are invisible when choosing the next packet. Can the
external PS1 project's subsystem taxonomy seed such an inventory **without**
importing any PS1 claim about the PC port?

This records the seeding event behind [[Subsystem Coverage Map]] so its only
quantitative provenance claim is reproducible rather than a bare number.

## External source and exact reads

`SRC-PS1-ABL` at commit `1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51`, branch
`master`, matching the snapshot already recorded in
[[External Source Registry]]. The working tree was dirty (147 entries), so
**only committed blobs were read**, per the registry's standing requirement.

Reproduce the count with:

```bash
git ls-tree -r --name-only HEAD ObsidianVault/Canon/Systems/ \
  | sed 's|.*/||' | grep -c '^SYS_'
```

which returns **115** at that commit. Directory-level counts read the same
way: `Canon` 808 notes, of which `Canon/Systems` holds 242 (the 115 `SYS_*`
plus `Finding_-_*`, `Asset_-_*`, `Core_-_*`, and `Gameplay_-_*` families),
alongside `Canon/Functions` 507 and `Canon/Memory` 40.

Nothing was copied, linked, vendored, or written. The external repository was
unchanged before and after: same `HEAD`, same 147 dirty entries.

## What was taken

Only the **existence and rough grouping of subsystem names** — that the PS1
build has notes for camera, enemy AI, an event VM, audio banks, FMV playback,
movement controllers, and so on. Those names were condensed by ABLPC into 18
rows and rewritten; no PS1 note was reproduced, and no PS1 address, offset,
field, constant, format, or behaviour entered ABLPC.

## What was explicitly not taken

No per-system PS1 claim. In particular the coverage map's PC status column
cites **PC evidence only**, and every row without a PC anchor is recorded as
unknown on PC — including whether the PC port organises that area the same way
at all. The PS1 side supplies candidate *questions*, never answers.

## Similarities and differences

Not applicable at this granularity: this seeding compares no specific
structure, function, or format. It is an inventory of where to look. Any
actual PS1/PC correspondence must be recorded as its own comparison under
[[Cross-Port Evidence Policy]] with a discriminating PC experiment.

## What remains unknown

Whether the PC port contains an analogue of each named subsystem, and whether
its organisation resembles the PS1 build in any respect. Both are open for
every Untouched row.

## Discriminating PC experiment

Per row, the smallest PC-native discriminator is the "top open question"
column of [[Subsystem Coverage Map]] — for example, locating camera state in
the PC image, or finding whether a PC event/trigger stream exists. Each
becomes a normal PC packet under the roadmap's rules; none is closed by PS1
material.
