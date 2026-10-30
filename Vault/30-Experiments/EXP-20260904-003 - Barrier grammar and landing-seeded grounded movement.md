---
type: experiment
id: EXP-20260904-003
date: 2026-09-04
question: What is the kind-0x101 barrier grammar, and how do real obstacles respond after original instructions establish grounded contact?
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux; Python 3.14.6; Unicorn 2.1.4; offline isolated memory
status: completed-offline-not-independently-audited
result: canonical-barrier-reader-and-bounded-grounded-response-demonstrated
tags: [re/collision, re/experiment]
---

# EXP-20260904-003 - Barrier grammar and landing-seeded grounded movement

## Prior work reused, new work bounded

The user explicitly requested barrier decoding and grounded movement before a
writer, while avoiding repeated research. A search for `004aae30`, `004a9ba0`,
`004a95e0`, `007f3d3c` and barrier-format references in Vault/code/tests found
the EXP-001/002 leads and no existing barrier parser or grounded test packet.

Reused unchanged: the terrain directory/parser, original loader and bounds /
bucket setup, height model, EXP-001 response/descriptor findings, and EXP-002
real triangle/barrier locators. `scripts/terrain-retail-probe.py` remains
SHA-256 `52ae78064bea79ec14de8f65e2529aa1b272b147b37e92599e4a9b0f24ec6980`;
its report remains
`87392d332e5550cef104728887dfcae8fc5a776bd9c434283167d996cd47df3c`.
R2q was neither modified nor run. No collision writer was built.

New work: decode kind`0x101` block metadata, add a lossless read-only parser,
compare its geometric candidate predictions with original instructions, then
test the grounded branches from contacts produced by original landing calls.
No game, live debugger, memory poke, mapping, screenshot or external PS1 source
is involved. CPU context, scratch and image data remain private to Unicorn.

## Reproducibility

```bash
.venv/bin/python scripts/terrain-barrier-probe.py
.venv/bin/python -m pytest -q tests/test_terrain_barriers.py tests/test_terrain_barrier_probe.py tests/test_terrain_retail_probe.py tests/test_terrain_collision_probe.py tests/test_terrain_all.py tests/test_terrain_height.py
```

- Report: `reports/terrain/EXP-20260904-003.json`,200,240 bytes, SHA-256
  `10ae67083823eec74f6fe5b8d4b08dce7af57d4da00e172b37c9349346eaf6e6`.
- Probe: `scripts/terrain-barrier-probe.py`, SHA-256
  `ede60a7dfe65faff8a778c8db5092d6ca657cfad25a64261fbe6ef5694fa7df8`.
- Reader: `reimplementation/ablpc/terrain_barriers.py`, SHA-256
  `b0e1537efb35f72e618b92ff5b2ff36384d0634861e86adb06ffdd75a41885f2`.
- Report includes every corpus source hash and the unchanged supporting-script /
  parser / predecessor-report hashes. No executable bytes, complete geometry
  arrays or memory dumps are published.
- Regression: **154 passed in5.27s**,49 new tests, no skips. Existing105 tests
  remain regression checks, not newly claimed research. Full repository suite
  and independent audit are not claimed.

## Confirmed: barrier layout and original collector agreement

The bounded format is documented in [[PC TERRAIN ALL barrier strips]]. Source
kind`0x101` contains `magic,u16 segment_count,u16 unknown`, then N+1 connected
12-byte X/middle/Z points. Four middle dwords store each full16-segment block's
X minimum/span and Z minimum/span. A short final block starts with an INT32_MIN
middle-word sentinel. Remaining middle/header/trailer bytes stay unknown and
preserved. Bounds are conservative, not necessarily tight.

Static evidence: loader `004a860f..004a862a`; count and block reads
`004ab626..004ab673`; endpoint overlap/copies `004ab680..004ab70a`; stride/list
advance `004ab71b..004ab73a`. The format matches all18 retail terrain-family
files: **65 strips,6,722 segments,396 bounded blocks,62 sentinel tails**.
Every stored bounded block covers its17 endpoints. Payload sizes are exactly
`8 + 12*(N+1)` in the corpus; upper header words are zero and trailers empty.
The reader preserves nonzero unknown header words and trailers in synthetic tests.

The new collector tests reuse original loaded lists for Level01/Level03, clear
triangle tags only in emulated memory to isolate the segment path, run
`004ab1a0` through **stop `004ab740` before response**, and record actual
source pointers at `004ab6ca`. The decoded test oracle uses geometric endpoint
overlap and the original padded block window, rather than copying decompiler
code into a production solver. **108 real query cases** compare exact ordered
admission and byte-exact candidate copies. Each covers one of the first/middle/
last segments of a strip, with requested delta0, +2048X, or -16000Z.

Five small hand-packed, in-memory strips with4/16/17/32/33 segments check full
blocks and sentinel tails. They set unknown header`+6` to `0xbeef`, which the
collector ignores. The original code admits exactly the first16 passing pairs
when more qualify (`007fc8e8` counts32 endpoints). A far-query negative rejects
all candidates. This proves a **traversal-order capacity limit**, not that
every possible real query has at most16 nearby walls. The real query set's
largest observed admission is15 pairs. No file writer or game-facing fixture
is created by these synthetic bytes.

## Confirmed: original landing establishes grounded contact

Each grounded case begins with flags`[0,0]`, zero contact, a synthetic position
above a real surface and requested delta`(0,2048,0)`. The original full
coordinator establishes flags`[1,1]` and a real descriptor/cell pointer; no
manually invented grounded pointer is supplied. A subsequent movement call
keeps this exact landed state. Controls apply only after the same landing.

| Surface seed | Original landed position | Contact descriptor / file cell |
| --- | --- | --- |
| Flat triangle | `(-176384,-80096,-342006)` | 110 /87884 (`0x1574c`) |
| Floor beside barrier | `(110445,-121018,-129784)` | 104 /62004 (`0xf234`) |
| Floor beside steep triangle | `(-9471,-88641,250925)` | 114 /106336 (`0x19f60`) |

All cells are in Level01. Inputs came from the established terrain coordinates
and height model; the landing output is original-instruction evidence. Full
requested and observed states are in the report. This is synthetic gameplay
state, not a recording of a user's movements.

The grounded selector is byte1 of the flags argument (`004ab20f..004ab225`,
`004ab7f0..004ab83e`). With it set, the coordinator first calls `004aae30`
against the existing support cell, then `004a9ba0` to examine other collision
candidates, including the same `004a95e0` segment routine. Raw return sites
`004ab80d`, `004ab823` and `004ab843` distinguish support, grounded response
and nongrounded response. No callee is stubbed.

## Confirmed: ten grounded/control cases

**Flat floor:** requested`(+256,0,0)` produces exactly+256X with constant Y and
flags`[1,1]`; -256X does the converse. A requested`(0,-2048,0)` with the ground
flag retained is projected to zero velocity and leaves position unchanged.
Clearing only that flag after the identical original landing instead moves
upward2048 units and finishes`[0,0]`, without entering the grounded helpers.
This is a flag-control experiment, **not a claim about the game's jump input**.

The flat contact settles at plane Y+3072 in this fixture. The existing reset
height helper's `rest_y` uses plane Y+2944 at a different consumer boundary.
Do not substitute either value for the other or rewrite the accepted reset
model based on this distinction.

**Grounded barrier crossing:** requested`(0,0,-2048)` after the barrier-floor
landing produces `(110280,-121089,-129357)`. The grounded response returns2;
segment pair0 wins at `004a9787`. The coordinator then re-enters the nongrounded
path, hits the supporting floor, and ends grounded again. Removing only
`007f3d3c` after the identical landing produces
`(110479,-120635,-131756)` with no return2 and no segment hit. This endpoint is
not the raw requested endpoint because the floor is sloped. The moving-away
control also has no return2. These results isolate barrier response from slope
projection rather than treating every position change as a wall hit.

**Grounded steep-triangle crossing:** requested`(2048,0,0)` after landing on
descriptor114 produces `(-7879,-88421,250264)`. The original grounded nearest-
candidate update at `004a9df3` selects source87/cell1000, returns2 and finishes
the coordinator call with flags`[0,0]`. Clearing only descriptor87's tag after
the same landing produces `(-7456,-88391,250998)` and flags`[1,1]` without
return2. Moving away also avoids that return. Thus the EXP-002 steep triangle
is demonstrably handled from a grounded entry, not just from an airborne one.
The differing final contact states are fixture results, not universal claims
about all walls.

Static corroboration: the grounded response excludes the cached support cell
from its other-triangle scan, selects a nearest hit at `004a9df3..004a9e1d`,
calls the segment routine at `004a9e7a`, and distinguishes its response using
normal-Y threshold **-8192** (`004a9f1e..004a9f2b`). Coordinator return handling
is `004ab848..004ab875`. General slope classification, corner interaction and
every contact-state transition are not exhausted by these fixtures.

## Disposition and next boundary

The requested canonical barrier decoding and bounded grounded tests are
complete. KU-080 now has grounded and nongrounded original-instruction evidence
for both collision families. KU-079 and whole-render-subtree KU-081 do not
advance from this packet. The existing directory, height model and EXP-002
results were reused without re-deriving their conclusions.

Next is a bounded collision-authoring fixture design using the now-demonstrated
triangle, barrier and contact rules. A future writer must preserve point order,
explicit closing endpoints, bounds/sentinels and the16-pair collection limit;
it must distinguish reset heights from movement contact heights. Broader
normalization/overflow limits, noncanonical source variants and live authored
surface acceptance remain unresolved. This packet provides no writer, live
authorization, R2q activation or independent-review acceptance. See DEC-228.
