---
type: experiment
id: EXP-20260904-002
date: 2026-09-04
question: Can original PC instructions load real terrain, admit real collision candidates, and distinguish triangle response from the high-kind segment path offline?
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux; Python 3.14.6; Unicorn 2.1.4; isolated offline address space
result: real-triangle-and-XZ-segment-response-demonstrated-at-nongrounded-slot0-boundary
status: completed-offline-not-independently-audited
tags: [re/collision, re/experiment]
---

# EXP-20260904-002 - Retail collision admission and separate XZ barriers

## Scope and reproduction

**Confirmed at the offline instruction boundary:** the original movement
coordinator admits a real Level01 steep triangle and changes movement against
it. A separate kind-`0x101` source supplies X/Z segments that also change
movement. Removing each relevant geometry family from private emulated memory
removes its response. Neither result required screenshot calibration.

This is not a live game experiment. The full original loader `004a8410` and
movement coordinator `004ab1a0`, including their executed callees, run without
stubs. The initializer is explicitly a slice, `004a89f8..004a908f` exclusive:
it includes bounds, spatial buckets, reserved slots, and template-tag clearing,
but excludes filename setup and the final collectible initializer. No original
file changes, Wine/game launches, live process-memory actions, or external PS1
consultation occur. No collision replacement or exporter is admitted.

`scripts/terrain-retail-probe.py` uses the hash-checked `.text` loader from
`scripts/terrain-collision-probe.py`. All image memory other than `.text`
starts zero. The two original preloaded-buffer branches are selected by
`007f3d60` and `007f2d2c`; the template map starts at the original all-`-1`
state. The data files are mapped to private Unicorn memory, where the original
loader links their high-kind records. Synthetic position, velocity, contact
slot0, and **nongrounded** entry flags drive movement. Image, scratch memory,
and CPU context are restored for every case; source payloads are hash-checked
unchanged after each movement call. Execution must reach the exact stop within
3,000,000 instructions / ten seconds. Ordered PC hashes are actual sequential
PC streams, not the predecessor's frequency histograms.

Reproduce in the workspace:

```bash
.venv/bin/python scripts/terrain-retail-probe.py
.venv/bin/python -m pytest -q tests/test_terrain_retail_probe.py tests/test_terrain_collision_probe.py tests/test_terrain_all.py tests/test_terrain_height.py
```

Artifact: `reports/terrain/EXP-20260904-002.json`, SHA-256
`87392d332e5550cef104728887dfcae8fc5a776bd9c434283167d996cd47df3c`.
Script SHA-256:
`52ae78064bea79ec14de8f65e2529aa1b272b147b37e92599e4a9b0f24ec6980`.
The report additionally hashes the helper, parser, and executable `.text` and
records full source hashes. It contains 22 movement cases and two loading /
initialization cases, measurements and source locators only, without assets or
memory dumps. Focused regression: **105 passed in 4.03s**, including 35 new
tests; none skipped. No independent agent review or full repository-suite
acceptance is claimed.

## Confirmed: real-file census and template locality

Sources are read from `work/copies/BUGS_PC-full-disc/PC/BUGS/`:

| Source | SHA-256 | Source records | Stored triangle cells | Lateral-dominant normal | Exactly vertical normal |
| --- | --- | ---: | ---: | ---: | ---: |
| `CD/LEVEL01/TERRAIN.ALL` | `62f3b73f21630eb19c04e585a92e1f3e32a76fdcb6ec36bae18f9c1ec3a2a868` | 189 | 6,379 | 2,541 | 0 |
| `CD/LEVEL03/TERRAIN.ALL` | `b878c378c924fbdb45e450f4314808fdd3506f8685da2c3f255b7e316f4a2d9c` | 592 | 6,074 | 2,604 | 72 |
| `CD/BITS/PLANTTER.ALL` | `0a0cf7fa9e110eef8e2112760dcbefaa433b391ca613a3d673ee0327767eb468` | 14 | 453 | 214 | 2 |

Counts include only stored, non-clone payloads of kinds6/7/8. They are not
instantiated-triangle counts or admitted candidates. “Lateral-dominant” means
only `max(abs(nx),abs(nz)) > abs(ny)`, not a game slope threshold. Level01
contains 85 clone records; Level03 contains 463. High kinds stay opaque to the
triangle parser: Level01 has ten `0x101` records and one `0x104`; Level03 has
two `0x101` and one `0x104`; PLANTTER has one `0x104`.

Original loader and initializer results:

| Terrain source + PLANTTER | Loaded / N | Template indices, then cleared | Reserved indices | Nonempty buckets |
| --- | ---: | --- | --- | ---: |
| Level01 | 191 | 178..190 | 191..222 | 20 |
| Level03 | 602 | 589..601 | 602..633 | 33 |

The bucket member lists contain every loaded descriptor exactly once, including
the templates that are subsequently tag-cleared. Every mapped template comes
from PLANTTER source records0..12. Object types map to PLANTTER records as
`1→0, 2→6, 4→7, 5→8, 6→9, 7→10, 8→11, 9→12, 10→1, 11→2, 12→3, 13→4, 14→5`.
These mappings are original loader outputs, not manual template substitutions.

Independent static corroboration: source `+0x1a` supplies the signed index
stored at `007f29a6 + 2*index` by `004a858d`; the render-side reader uses
`007f29e8 + 2*object_type`, hence the observed source value is
`object_type+33`. `004a9019..004a906d` records N, reserves32 slots, and clears
mapped templates. Together with EXP-001's direct-store proof, the twenty
render-side direct destinations are **191..210** for this Level01 load and
**602..621** for Level03, disjoint from their static records and templates.
This is a two-file result, not universal high-watermark or whole-render-subtree
independence. The regression also compares original descriptor bases, payload
identities and X/Z bounds against the independently written height model for
all eligible terrain descriptors in both files.

## Confirmed: real steep triangle causes lateral response

Selected source: Level01 record87, source-group file offset988 (`0x3dc`),
cell1000 (`0x3e8`), normal `(-8178,-595,-14184)`, base
`(14752,-99200,247648)`. Synthetic starts use its integer centroid and the
coordinator's `0xc80` actor-Y offset. The original bounds and bucket traversal
admits eight cells from descriptors114,87,106. Hook `004aa715` identifies the
winning-time update at **source87/cell1000**; the coordinator completes its
own response iterations and final position stores.

| Crossing | Start | Requested delta | Unconstrained endpoint | Original coordinator endpoint |
| --- | --- | --- | --- | --- |
| X | `(-9611,-86539,251232)` | `(2048,0,0)` | `(-7563,-86539,251232)` | `(-8164,-86582,250188)` |
| Z | `(-8587,-86539,250208)` | `(0,0,2048)` | `(-8587,-86539,252256)` | `(-9569,-86609,250551)` |

For each axis: clearing only descriptor87's tag leaves four other admitted
cells but reaches the unconstrained endpoint; clearing all triangle tags also
does so. Moving away reaches its requested endpoint. Removing the high-kind
segment list leaves the positive response identical. All these interventions
change private emulator memory only. The positive cases make two full
`004aa4d0` calls; no segment pair is admitted. Raw instruction evidence is
`004ab4f7..004ab565` (cell admission), `004aa5c3..004aa743` (plane crossing,
inclusion, nearest update), and `004ab87b..004ab8a4` (coordinator position stores).

The link to Flik's live writer remains the prior independent evidence in
EXP-001: `004ab889 -> 0059d910` was seen in EXP-20260818-001/002. This new
experiment uses synthetic positions and does not establish that the user can
reach this cell naturally or that the branch fired in those old gameplay traces.

## Confirmed: separate kind-0x101 X/Z barrier path

The full loader's `004a860f..004a862a` links high-kind payloads into heads at
`007f3938 + 4*kind`; kind`0x101` selects `007f3d3c`. The movement coordinator
reads this head at `004ab5b7`. It copies segment candidates to `007f2a28`, with
the endpoint count at `007fc8e8`, and `004a95e0` tests them. This path is distinct
from the triangle pointer/descriptor arrays.

At synthetic `(110544,Y,-129568)` moving `(0,0,-2048)`, the original collector
admits four pairs, all byte-bound to Level01 source179, beginning at offsets
219640/219652/219664/219676. The first pair (file `0x359f8`) wins at the
`004a9787` nearest-time update. The output is `(110402,Y,-129376)` rather than
the unconstrained `(110544,Y,-131616)`.

The result is identical in X/Z at **Y=-200000,0,+200000**. Removing the segment
head reaches the unconstrained endpoint; clearing all triangle tags leaves
the positive response unchanged; moving away reaches its requested endpoint.
No triangle is admitted in any of these twelve cases. Raw `004a95e0` uses
segment X/Z and a horizontal normal for its crossing and endpoint checks.

**Bounded interpretation:** kind`0x101` supplies oriented X/Z barriers in this
nongrounded path, with no height discrimination in the tested response. A
triangle-only exporter would omit an observed collision mechanism. This does
not prove that every high-kind record is a wall or that all gameplay states
use identical response rules.

The middle dwords of the source's 12-byte entries are **not safe to call world
Y**: the collector reads some as block bounds/sentinels, and source179's first
one is `0x80000000`. Keep them opaque until the full block grammar is decoded.
The report binds copied six-dword pairs to exact source bytes; it does not
publish their contents or introduce a segment parser/writer.

## Confirmed static field narrowing; remaining work

Cell `+0x0e/+0x14` are Y edge components in `004aa650..004aa666`'s inclusion
arguments. The previously unresolved word`+0x1c` is consumed as **two signed
bytes**: at `004ab527..004ab547`, the lower contributes `byte*64 + h0` to the
local Y admission minimum, and the upper contributes `byte*64` to the span,
with the movement-radius padding added by the collector. These are static
consumer roles, not general material semantics or an authored-format proof.

**Inferred engineering direction:** use the original loader, admission, and
response routines as an offline reference for synthetic authored fixtures.
Keep triangle surfaces, X/Z barrier records and dynamic template instances
distinct until each encoding is understood. This permits fast collision work
independently of the visible-mesh calibration chain.

**Unknown:** grounded branch (`004aae30`/`004a9ba0`), full kind`0x101` block
grammar and capacity behavior, authored-input acceptance, complete render-call
subtree/payload effects, materials and visible ground. Next: decode the
segment block metadata and add grounded-contact controls with this same
harness, then prepare a minimal collision authoring fixture. Live authoring
acceptance and KU-079 remain separate gates. See DEC-227 / [[Project Roadmap]].
