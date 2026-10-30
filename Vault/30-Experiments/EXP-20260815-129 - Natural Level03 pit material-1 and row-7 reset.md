---
type: experiment
id: EXP-20260815-129
date: 2026-08-15
question: Does the first Level03 grain-gate pit naturally produce collision value 1, flag 0x10, and a nearest type-1 row reset?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; Wine 11 Staging; Gamescope 3.16.25; Direct3D 640x480x16; Level03 Tunnels
configuration: user-driven ordinary input; corrected current XYZ; nominal 50 ms process_vm_readv; one explicitly authorized grain byte write 1 to 10
artifacts:
  - dynamic/wine/RUN-KU057-20260815-184629/metadata.json
  - dynamic/wine/RUN-KU057-20260815-184629/selected-events.tsv
  - dynamic/wine/RUN-KU057-20260815-184629/runtime-log-markers.txt
addresses:
  - "0x0059D910"
  - "0x0059D9A0"
  - "0x0059D9A4"
  - "0x0059D9B1"
  - "0x0059A5B0"
  - "0x007F3D68"
  - "0x007F45A0"
  - "0x0041C6C0"
  - "0x00432930"
  - "0x00432B30"
result: natural-material1-upstream-confirmed-row7-repeat-row6-natural-selection-open
created: 2026-08-15
updated: 2026-10-02
tags:
  - re/experiment
  - re/runtime
  - re/gameplay
  - milestone/m3
---

# EXP-20260815-129 - Natural Level03 pit material-1 and row-7 reset

## Question

Does ordinary contact with the pit revealed by Level03's first grain gate
naturally produce collision result/material `1`, set reset-request bit `0x10`,
and return Flik through the nearest type-1 coordinate row? Is the nearby black
spider the same producer?

## Runtime and write boundary

One exact retail-derived Level03 session ran through the pinned companion in
Hardware/Direct3D mode. The corrected `0x0059D910` position triple and raw
state were sampled with read-only `process_vm_readv` at a nominal 50 ms.

The user explicitly requested that the live grain count be changed to 10. The
helper reverified exact retail SHA-256, CWD, PID `114541`, process group
`114288`, and the current count before one `process_vm_writev` call wrote one
byte at `0x0059D9B1`: decimal `1 -> 10`. Readback was 10. No other target write,
executable edit, asset edit, save edit, debugger attach, pause, or breakpoint
occurred. The write unlocked access; pit and spider events remained ordinary
user input. This is therefore not an unchanged-state grain-gate arm.

## Grain-gate result

The user identified the visible obstruction as the first grain gate and
confirmed it lowered at count 10. [[EXP-20260815-136 - Tunnels and City Entrance grain-gate requirements]]
later corrects this note's original static-producer attribution. Visible
Tunnels is internal Level03 and dispatches to `0x00432B30`, whose resident row
3 has retail requirement 10 at `0x004DAA0C`; its X/Z `(509676,510143)` is
approximately 16,420 units from this trace's first-gate position. Function
`0x00433790` instead belongs to internal Level04/City Entrance. The former
`0x00433790` attribution is rejected while the observed count-10 outcome is
retained.

The runtime trace crossed from approximately `(493260,30190,509766)` to
`(499439,31731,541382)`. Current collision changed `552 -> 543`, both with
value 0; `NextLife` stayed 0. The gate's animation field was not identified.

## Spider control

The user visually confirmed that the black spider delivered the fatal hit.
The captured final state was:

- current position `(533535,29515,639927)`;
- flags `0x0006`, `NextLife=2`, and counter `-1`;
- current collision descriptor/value `543/0`;
- subsequent counter restoration to 4.

The PC log independently recorded `Level done variable is 2.` and `NextLife.`
The first sampled post-reset X/Z `(522629,649284)` does not equal any of the 18
authored type-1 X/Z rows. This accepts a natural spider damage/death
progression but rejects the spider as the material-1 producer in this arm.

## First pit fall

The first fall began above the pit near `(501522,31785,540782)`. At the
captured below-floor transition:

- current position was `(494438,68730,526143)`;
- current descriptor/value was exactly `572/1`;
- flags were `0x0014`, including reset-request bit `0x10`;
- `NextLife=2` while the raw counter stayed 3.

The next sampled stable position was `(497247,31299,547255)`, with
`NextLife=0`, counter 4, and collision `543/0`.

Level03 type-1 row 7 is raw `(15539,0,17102)` at file offset `0x4B0`, giving
scaled X/Z `(497248,547264)`. The first post-reset sample differs by only
`(-1,-9)`. At material contact, row 7's squared X/Z distance was `453,992,741`,
versus `1,084,822,693` for row 6. This agrees with the confirmed nearest-row
selection at `0x00432930`. The sampler did not capture the exact write instant,
so the nine-unit residual is retained rather than silently normalized.

## Gate-side repeat

The user returned to the same single pit and fell from the side nearest the
lowered grain gate. The second below-floor transition independently repeated:

- current position `(505717,66713,526449)`;
- descriptor/value `572/1`;
- flags `0x0014` and `NextLife=2`;
- first sampled post-reset position exactly matching the earlier
  `(497247,31299,547255)` sample.

At this contact, row 7 again remained nearer: squared distance `504,988,186`
versus row 6's `1,068,067,930`. The pit geometry funneled both tested entry
approaches to Z about 526k and therefore selected row 7 twice. Repeating this
same pit is not a useful row-6 discriminator.

## Static/runtime join

The natural event supplies the previously missing upstream PC evidence:

- collision helper `0x004ACF90` reads signed descriptor word `+0x1E`
  (corrected 2026-10-02: `0x004ACFB0` is `movsx eax, word [edx + 0x007F45BE]`,
  descriptor base `0x007F4590` + `0x2E`, so the word is `+0x2E`);
- call site `0x004408EA` passes fourth argument 1 after result 1;
- `0x0041C8CC` ORs `0x14` into flags for a nonzero argument other than 2;
- `0x00432930` gates on bit `0x10` and selects the nearest type-1 X/Z row.

Runtime captured descriptor value 1, flags `0x14`, `NextLife=2`, and a repeated
row-7-like endpoint in that exact order. This is independent PC-native support
for the complete natural pit-reset chain.

## Contradictions and limits

The earlier descriptor-571/black-spider hypothesis is rejected for this arm.
The spider used descriptor/value `543/0`; both pit falls used `572/1`.
EXP-131 later proves the earlier scanner was 16 bytes misaligned: the tuple
then attributed to descriptor 571 is descriptor 572's base. Walking above it
did not produce value 1 because a descriptor base is not necessarily a
reachable surface point; the source payload supplies the actual bounds.

Confirmed only at this Level03 pit boundary: value 1 is a natural pit-reset
result, `0x14` requests the nearest type-1 reset path, and row 7 is the selected
authored coordinate row for both tested entries. This does not prove every
value-1 descriptor is a pit, every type-1 consumer is a respawn path, or that
row 6 is naturally selected. `KU-057` remains open only for an ordinary
material-1 contact inside row 6's nearest-region or an explicit milestone
disposition of that narrower requirement.

## Lifecycle

The observer, overlay, exact game/Wine/Gamescope group, and private sink were
closed. Targeted process and sink audits were empty, and Wine `Y:` was restored
to `/home/dev/ABLPC/work/copies/BUGS_PC-full-disc`.
