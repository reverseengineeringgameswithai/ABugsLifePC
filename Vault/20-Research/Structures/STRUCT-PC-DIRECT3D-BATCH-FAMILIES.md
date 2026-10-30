---
type: structure
id: STRUCT-PC-DIRECT3D-BATCH-FAMILIES
status: inferred
confidence: high
created: 2026-08-13
updated: 2026-10-02
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
evidence: [EXP-20260813-039, EXP-20260813-040, EXP-20260813-041, EXP-20260813-042, EXP-20260813-043, EXP-20260813-044]
related: [FUNC-97C95BA5572D-00405FE0, FUNC-97C95BA5572D-00407450, FUNC-97C95BA5572D-0044F8E0]
tags: [re/structure, re/rendering, re/direct3d]
---

# PC Direct3D batch families

## Scope

This dossier records only the two fixed-root Direct3D batch families reached
from selector-2 `0x0044F8E0`. Names are structural. No primitive, asset,
material, source-field, or general `.ALL` semantics are assigned.

## Confirmed layout

Both roots expose 32 pages. Page selection is bounded to `0..31` by native
masks in the exact caller/builder paths.

| structural field | root via `0x004C4108` | root via `0x004C410C` |
|---|---:|---:|
| exact root value | `0x004F1730` | `0x00511510` |
| vertex pointer | `root + page*4` | `root + page*4` |
| vertex count | `root + 0x104 + page*2` | `root + 0x104 + page*2` |
| inline index page | `root + 0x186 + page*0x7D0` | `root + 0x186 + page*0x2580` |
| index count | `root + 0x1FD56 + page*2` | `root + 0x4B186 + page*2` |
| bounded index capacity | 1,000 words | 4,800 words |

`0x00405FE0` appends four `0x20`-byte vertex records and six indices.
`0x00407450` appends three vertices and three indices. Both precheck vertex
count `>493` and flush before appending. A measured addition `(V,I)` therefore
decomposes structurally as `B4=(I-V)/2` and `B3=(V-4*B4)/3`, where `B4/B3`
count completed append paths, not all function entries.

## Flush/reset boundary

- Family `0x004C4108` flushes through `0x004056A0`. The marker write at
  `0x00405831` produces a data-watch stop at `0x00405838`, before index and
  vertex resets at `0x0040583E/0x0040584D`.
- Family `0x004C410C` flushes through `0x004058D0`. The marker write at
  `0x004059A5` produces a stop at `0x004059AB`, before resets at
  `0x004059B7/0x004059C8`.
- Register `ESI` retains the page at both pre-reset stops. Native disassembly
  exposes no other reset/flush callee inside the two builders.

## Runtime evidence

[[EXP-20260813-040 - Direct3D retained-entry batch provenance]] records fresh
accepted hardware-rendered control/replacement/control arms. For exact
retained-entry candidates `{0-7, 9-23}`, every selected addition uses root
`0x004C4108`, page 16; the second family remains zero and no selected entry
flushes in-call. Replacement counts outside both controls select exact set
`{1,2,4,5,6,7,9,10,14,15,18,19,20}`.

[[EXP-20260813-041 - Changed-record form localization]] reuses only the
retained metadata and proves that all 145 changed records in that set reach a
selected builder. Per-form count envelopes retain 124 exact records; three
single-record append outcomes are individually discriminated and 121 remain
unresolved.

[[EXP-20260813-042 - Per-record Direct3D append discriminator]] maps the exact
successful count writes and earlier no-append returns, then records fresh
count-only outcomes for all 124 candidates. Only entry 7/file offset
`0x0A6C`/form `0x3C` differs outside both controls (`0/1/0`). The three older
single-record patterns do not reproduce, so they remain arm-specific rather
than source-stable.

[[EXP-20260813-043 - Exact 0A6C builder-input localization]] proves all 12
source differences at exact record `0x0A6C` first enter the builder after its
successful count write. Four three-byte groups supply four separate
byte-derived dwords at appended vertex-record `+0x10`. No changed byte
distinguishes admission; that boundary instead retains non-source per-frame
state.

[[EXP-20260813-044 - Exact 0A6C admission-state localization]] reduces that
exact path's physical non-source union to 23 locations, at most 22 active on
one path, and its source-derived mode-2 rejection chain to 12 ordered logical
slots. Existing safe pre-call and entry-post/count boundaries can support a
payload-free first-reject receipt without changing this structure or adding
an execution point.

[[EXP-20260813-045 - Exact 0A6C admission evaluator fixtures]] implements and
fixture-validates that exact receipt. It changes no batch-layout claim and
adds no live predicate evidence.

The experiment retains only counts, addresses, order, and SHA-256 metadata;
no protected batch payload bytes are stored. Count provenance does not prove
which record or source byte causes the bounded visible result.

## Evidence

- [[EXP-20260813-039 - Direct3D renderer-path reconciliation]]
- [[EXP-20260813-040 - Direct3D retained-entry batch provenance]]
- [[EXP-20260813-041 - Changed-record form localization]]
- [[EXP-20260813-042 - Per-record Direct3D append discriminator]]
- [[EXP-20260813-043 - Exact 0A6C builder-input localization]]
- [[EXP-20260813-044 - Exact 0A6C admission-state localization]]
- [[EXP-20260813-045 - Exact 0A6C admission evaluator fixtures]]
- `static/exports/BIN-97c95ba5572dce63/M2-direct3d-batch-provenance-preflight.md`

## Next question

M2.32's offline exact-evaluator gate is complete. Any live matched capture
requires fresh explicit authority and the locked schema-6 envelope.

*Update (2026-10-02 audit):* that live capture was later authorized and run.
[[EXP-20260813-046 - Exact 0A6C live admission receipt]] completed M2.32, and
[[EXP-20260813-048 - Exact 0A6C consecutive-cycle live receipt]] completed
M2.33; neither is cited as changing the batch layout above.
[[EXP-20260813-059 - Independent M2.41 disposition hard-truth audit]] then left
M2 deferred, so there is no open next question on this structure.
