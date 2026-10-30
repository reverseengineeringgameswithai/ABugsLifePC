---
type: experiment
id: EXP-20260815-118
date: 2026-08-15
question: Can ordinary PC gameplay naturally produce collision material 1 near the Level03 row-6 reset anchor without debugger writes?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; Wine 11 Staging; Gamescope; retail PC executable and Level03 work copy
environment_version: rr 5.9.0; ntsync present; repository state after EXP-20260815-117
working_directory: /home/dev/ABLPC
configuration: one fresh muted/windowed Direct3D arm; ordinary keyboard input; process_vm_readv observation only
artifacts:
  - work/copies/EXP-20260815-118-natural-material1/
addresses:
  - 0x0059D9A0
result: bounded-route-negative-natural-material1-producer-open
created: 2026-08-15
updated: 2026-08-15
tags:
  - re/experiment
  - re/runtime
  - re/gameplay
  - milestone/m3
---

# EXP-20260815-118 - Natural Level03 material-1 reconnaissance

## Question

Can ordinary PC gameplay naturally produce collision result/material `1` near the loaded Level03 type-1 row-6 reset anchor, and does that event request the `NextLife` reset path without debugger writes?

## Boundaries

- PC retail executable and the control Level03 work copy were used; configuration identity is inherited from [[EXP-20260815-117 - Approved Level03 row-6 reset rerun]].
- The game ran from `work/copies/M3-level03-type1-row-control-full-disc`; `originals/` was not touched.
- Runtime PGID `534414`, game PID `534656`, muted/windowed wrapper, and derived work-copy log are recorded under `work/copies/EXP-20260815-118-natural-material1/`.
- The Direct3D arm passed all four required log gates in `direct3d-gate-late.txt` and contained no `INITSOFTRENDER` marker.
- Observation used Linux `process_vm_readv` samplers only. They did not attach, pause, set breakpoints, write target memory/registers/code, or alter execution.
- All gameplay movement was ordinary keyboard input through the game window.

## Runtime evidence

The fresh Level03 load reported internal level `3`, spawn `(-16896, 32043, 6631)`, flags `0x0008`, `NextLife=0`, counter `4`, current collision descriptor `548`, and material `0` in `level03-start-snapshot.tsv`.

A full read-only descriptor scan at a later near-spawn position reconfirmed stable material-1/tag-6 entries 570 through 578 (`material1-scan-near-spawn.txt`). Relevant entries were:

| Index | Source pointer | Tag | Material | Misindexed next-descriptor X | Y | Z |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 570 | `0x006bff2b` | 6 | 1 | 470112 | 64224 | -423840 |
| 571 | `0x006bffdf` | 6 | 1 | 471712 | 64224 | 537728 |

The source pointer, tag, and material columns are valid. EXP-131 later proves
that the helper began its 48-byte row at actual descriptor `+0x10`; its
purported X/Y/Z at row `+0x20/+0x24/+0x28` therefore belongs to descriptor
`index+1`. In particular, `(471712,64224,537728)` is descriptor 572's base,
not descriptor 571's tuple. This explicit correction preserves the raw
artifact while superseding its coordinate labels.

The ordinary route reproduced known waypoints, then established a useful route correction:

- Jump traversal reached `(308750, 43782, 398734)` beside a red mushroom and wall (`replay-03.tsv`, `replay-03.png`).
- A left turn plus ordinary jump sequence crossed onto the visibly elevated corridor at `(306880, 15377, 452405)` (`mushroom-jump-01.tsv`, `mushroom-jump-01.png`).
- Eight further jump cycles reached `(362499, 28410, 499117)` (`upper-corridor-01.tsv`). The current collision descriptor changed from 560 to 552, but its material remained `0`.
- Across the recorded approach, current collision material never became `1`, `NextLife` remained `0`, and no flag value containing reset-request bit `0x10` was observed.

One sampler limitation was discovered before evidence collection: its optional nearest-material scan began at live index 602 and therefore excluded the known entries 570-578. The independent actor coordinates, current collision index/material, flags, counter, level, and `NextLife` fields remained usable. Exact sampler sources and hashes are preserved with the ignored raw evidence.

## Result

**Confirmed negative for this route only:** the recorded ordinary-input approach reached the upper Level03 corridor near row-6 Z but did not naturally contact a material-1 descriptor and did not request the reset path.

**Confirmed route evidence:** the red-mushroom jump is a reproducible ordinary-input transition from the lower wall area near `(309k, 44k, 399k)` to the upper corridor near `(307k, 15k, 452k)`.

**Not established in this arm:** the natural producer of collision
result/material `1`, checkpoint semantics, or a natural result-1 reset.
EXP-129 later resolves the first and last items at the first grain-gate pit;
EXP-131 maps its source geometry to descriptor 572 and rejects the old
descriptor-571 coordinate premise.

## rr preflight at close

`rr 5.9.0` is installed and `kernel.perf_event_paranoid=1`, but `/dev/ntsync` is present and the `ntsync` module is loaded. This is the existing [[Runtime Tooling#The ntsync blocker for rr]], not a new root cause. No privileged module action was taken. The validated `scripts/rr-record.sh` therefore remains correctly blocked until `/dev/ntsync` is genuinely absent.

## Next discriminating experiment

Prefer a deterministic controller/input movie recorded by the user and synchronized with the read-only state trace before another long manual approach. This input-replay arm is separate from rr:

1. Have the user record a fresh Level03 controller/input movie from spawn through the red-mushroom transition.
2. Continue toward the then-hypothesized black-spider vicinity and deliberately make ordinary contact.
3. Preserve at least five seconds after damage, reset request, or recovery.
4. Trace current descriptor/material, flags, counter, and `NextLife` throughout.
5. Separately, if using `rr`, first satisfy KU-028 with the already documented explicit root/module procedure, then validate record, `rr ps`, autopilot replay, packing, and the known plant-slot replay watchpoint before using an rr trace for KU-057. rr does not replace the missing CAP-002 controller/input-movie recorder.

## Evidence

- Raw ignored evidence: `work/copies/EXP-20260815-118-natural-material1/`
- Prior accepted reset consumer discriminator: [[EXP-20260815-117 - Approved Level03 row-6 reset rerun]]
- Runtime tooling boundary: [[Runtime Tooling#The ntsync blocker for rr]]
- Open question: [[Known Unknowns]] (`KU-057`)

## 2026-08-15 superseding target result

[[EXP-20260815-129 - Natural Level03 pit material-1 and row-7 reset]] rejects
this note's proposed descriptor-571/black-spider route. In the later natural
arm, the spider used current descriptor/value `543/0`; two falls into the
single pit revealed by the first grain gate instead used `572/1`, raised flags
`0x14` with `NextLife=2`, and repeated a row-7-like reset. The bounded negative
route recorded here remains valid. EXP-131 later supplies that geometry
evidence and proves the old scanner's tuple belonged to descriptor 572, not
571.

## 2026-08-15 descriptor-layout correction

[[EXP-20260815-131 - Level03 collision geometry and M3.5 disposition]] proves
that this experiment's C scan was 16 bytes late relative to the actual
descriptor base `0x007F4590`. Its material filtering remains correct, but its
X/Y/Z labels are shifted by one descriptor. Descriptor 571's actual base is
`(470112,64224,-423840)`; descriptor 572's is
`(471712,64224,537728)`. The nine exact source regions and their bounds are
now recorded in [[PC TERRAIN ALL collision descriptor source]].
