---
type: experiment
id: EXP-20260907-022
date: 2026-09-07
created: 2026-09-07
updated: 2026-10-29
status: prototype-live-rejected
environment: Wine Gamescope hardware Direct3D, Blender Flatpak, offline Unicorn x86
question: Can an authored layout split its terrain into independent native scene/collision chunks, and why did the live trial freeze?
result: Native seam, wall and frame gates pass for four chunk descriptors, but the live trial freezes because MOS.ALL entry37's 100-byte stream at 0x0076F971 overlaps renderer scratch 0x0076F9A0..AF and original 0x0044F8E0 loops on the corrupted selector; restoring the reference bytes offline reaches the 0x3C branch
binary_sha256: 3a2e6ca8463752463751c5eefc031e109d17e1ddaa9dc079615446b1f0454a77
evidence: [EXP-20260907-017, EXP-20260907-019, EXP-20260907-021]
tags: [experiment, terrain/authoring, re/rendering]
---

> Successor: [[EXP-20260907-023 - Dedicated asset arena and terrain chunk acceptance]] repairs the reproduced overlap using dedicated storage. This note preserves the rejected EXP-022 arm.

# Terrain chunk prototype and model stream freeze

A live trial of an authored Level01 layout with its terrain split into four
separately bounded native scene/collision chunks **failed live acceptance**: the
game froze. The freeze mechanism is a native model stream overlapping renderer
scratch, not the chunk geometry itself. This packet does not identify EXP-020's
exit cause.

## Chunk layout and native requirements

Whole visible faces and collision triangles were partitioned by exact X/Z
centroid at stored X8192/Z19456. Each chunk is recentered with preserved world
vertices/UVs/colours/opaque bytes, a separate visibility bound, relocated native
DAT pointers and a paired kind-6 collision record; the original source99 trailer
and unrelated bytes are retained. The existing exit helper still uses
descriptor99, so cuts through its supporting region reject.

| Region | Scene | File collision source | Origin in stored coordinates | Bound |
| --- | --- | --- | --- | --- |
| 0,1 | 160 | 99 | 1024,-4791,22991 | 12104 |
| 0,0 | 484 | 189 | 1024,-4548,15360 | 12633 |
| 1,0 | 485 | 190 | 9984,-3945,15360 | 7256 |
| 1,1 | 486 | 191 | 9984,-4143,23040 | 6551 |

Bounded native checks (paths relative to `work/experiments/EXP-20260907-022/`):

- `native-seams.json`:62 floor edges crossed in both directions,124 paired
  trajectories, eight steps each; maximum position difference0. Five landing
  probes and the unchanged exit helper's positive/negative checks pass.
- `native-wall-seams.json`:24 paired grounded/airborne pushes across12 shared
  wall edges, identical resulting positions.
- `native-frames.json`:12 paired camera/animation contexts execute original PC
  scene admission/drawing/flush instructions. All four chunks draw; batches
  have finite vertices, valid indices and at most500 vertices. Six D3D COM
  calls are stubbed; this proves neither GPU pixels nor full-game performance.
- Three contexts omit22 triangles compared with artificially inflated bounds.
  `origin-diagnosis.json` separates bounds from origin rounding. The first
  XY-only comparison (`culled-packets-xy-only.json`) fails; the retained corrected
  `culled-packets.json` shows every omitted triangle has entirely negative
  projected depth. No pixel-equivalence claim is made.
- `resident-chunks.json` verifies every chunk's exact resident mesh/collision,
  origin and bound. File collision source indices are not runtime descriptor
  indices: `source-descriptor-map.json` independently resolves payload
  pointers99→99,189→178,190→179,191→180. The first verifier incorrectly
  equated the two and rejected; this is a corrected measurement, not an asset
  repair.
- `focused-01.log`:35 focused tests; `make-check.log`:1178 selected source
  tests pass.

These checks omit ongoing actor rendering; the live failure below prevents
promoting the chunk arm despite their passes.

## Confirmed live freeze and native discriminator

Trial game713424/start9526810/group713166 entered level1. It subsequently
stayed at250077,-112732,371131 with contact descriptor179. The passive40-second
observation contains1970 identical-position samples and247 frames. A separately
recorded normal Up3s hold also produces no movement. The precise inputs before
observation are not established; the title-key guard had already rejected because
main-game initialization had completed. Do not claim a fully agent-controlled
route to this pose.

The frozen window was also reported independently. Flik body18 remains exactly
its436 original bytes at0x007683F1,29691 bytes before scratch. That successful
check misses another model's corruption.

`stalled/perf-samples.json` records79 read-only Linux CPU-clock samples of the
same guarded thread:51 at0x004509DE and28 at0x0044F918. No ptrace, breakpoint,
process stop or live write was used. The sampled ESI is0x0076F9A1. A read-only,
non-atomic image/stack capture supports offline replay; the process was stuck
throughout the observations, but the capture is not described as atomic.

Original PC `0x0044F8E0` reads entry+0x20. Entry37 at0x005AA1F0 points to a
100-byte stream at0x0076F971; its second0x30-byte record overlaps renderer
scratch0x0076F9A0..AF. The reference stream is byte-exact with
`PC/BUGS/CD/CHARS/MOS.ALL` offset0x7E8, file SHA-256
`4ba6f2f466f73eccd1f6d0bef2a86ebe851a29ac27da2463a61bfd5c64619c72`.
`stalled/stream-source.json` records that match. All13 differing bytes are inside
that scratch interval. EXP-017 independently establishes native renderer stores
to that interval; this trial did not trace the original write live.

Static instructions at0x0044F915/918/921/924 and0x004509DB/DE/E0 repeatedly test
an unsupported nonzero selector without advancing ESI. The saved sample has
selector0xEB (masked0x68). `stalled/loop-replay.json` executes10000 original PC
instructions and repeats the same eight-instruction loop1250 times. Replacing
only the100-byte stream with the exact source/reference bytes **offline** reaches
the accepted0x3C branch at0x0044F92A after16 instructions. No full frame or
permanent runtime repair is claimed. This confirms the immediate freeze
mechanism; the complete allocation topology remains unknown.

## Remaining storage question

`preview-01/close-receipt.json` records normal close followed by guarded owned
signals; `post-trial-audit.log` is clean. The earlier single-mesh build is
**not a complete storage-safety repair**: its reference entry49 pointer is
0x0076F99F, so the same scratch range still lies among later loaded model data
(`restored-state/image.bin`). Whether and when that entry is drawn is not
established here. A compiler size cap and a Flik-only comparison cannot certify
all arena occupants.

Next: identify all loaded stream/allocation intervals, prove storage separation
for every affected occupant, then rerun full actor rendering and sustained chunk
traversal. Do not suppress unknown opcodes or merely raise the size cap. Exact
EXP-020 instability remains a separate unknown.

Tracked index: `reports/terrain/EXP-20260907-022.json`. No original assets,
private captures or game binaries are committed; no PS1 evidence is consulted.
