---
type: experiment
id: EXP-20260905-007
date: 2026-09-05
question: Does retail collision support the user-selected route and the earlier authored fall footprint?
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Wine and Gamescope, isolated retail Level01 copy
environment_version: Existing host environment; no new version census
working_directory: work/copies/EXP-20260905-007/og-game/PC/BUGS
configuration: Authorized position and facing transfer, then normal Up with read-only RAM observation
artifacts:
  - reports/terrain/EXP-20260905-007.json
  - work/experiments/EXP-20260905-007/authorization-and-plan.json
  - work/experiments/EXP-20260905-007/og-preview-02/normal-up-result.json
addresses:
  - 0x0059D910
  - 0x0059D920
  - 0x0059D930
  - 0x0059D938
  - 0x0059A5B0
  - 0x007F3D68
  - 0x00861C84
file_offsets: [43416, 44140, 44248, 45884, 47008, 47716]
result: Bounded retail control completed; selected authored floor omissions confirmed; exact earlier fall replay remains open
created: 2026-09-05
updated: 2026-09-05
tags:
  - re/experiment
  - terrain/collision
---

# EXP-20260905-007 - Retail position control and missing floor footprints

## Question and scope

The user reported leaving the authored deck and falling through visible old ground, and separately seeing retained collision where original ground rendering was absent. EXP-006 changed render tiling, not the EXP-004 collision payload. The authored source-99 payload is not retail collision: the play-area fixture replaced its active groups rather than adding an independent collision descriptor.

This control uses the user's later current slope location, not the earlier deck-edge starting location. Do not describe it as a matched replay of the earlier fall.

## Procedure and authorization

The user explicitly authorized transferring current position and facing to OG and then holding Up. [[PC Flik teleport procedure]] and [[PC autonomous game control]] govern the operation. The actual executed image is unchanged retail `97c95ba5...7b878`, not the auto-hardware image. Original Level01 TERRAIN.ALL is `62f3b73f...2a868`; LEVEL.DAT is `786b7a96...8b53`. Complete resident source-99/100 payloads and render meshes 128/160/213/280 matched those staged originals.

The selected destination `(124987,-102158,328714)` has source-98 cell `43416`. Both arms have identical source-98 directory entries and complete collision payloads; the authored game had remained stationary there. The cell footprint and bytes were recorded before transfer.

The sole authorized position write was one `process_vm_writev` with two separate 12-byte vectors at `0x0059D910` and `0x0059D920`. The intervening unknown dword was preserved. One separate eight-byte/two-vector call copied recorded dwords `766` and `763` to `0x0059D930` and `0x0059D938`. Retail initialization at `0x004389BF`/`0x004389C5`, after a `0xFFF` mask in `FUN_004388B0`, supports the angle-field widths; `FUN_0043F7E0` shows input-relative updates to the latter field. No auxiliary, velocity, contact, flags, camera, or NextLife writes occurred. Both calls had identity and compare-before-write guards, exact readback, and receipts. The one-shot authorization is consumed and must not be reused.

A read-only observer ran before and after the writes. Over 623 samples, the transferred position and heading remained exact, NextLife stayed zero, and the camera settled naturally. The old source-99 contact reference and old auxiliary coordinates remained cached. An overly strict stationary-contact gate therefore stopped before Up. This rejection is retained; it was not overwritten or reclassified as a completed movement test.

After the user explicitly approved continuing with normal input and no further writes, `normal-up-control.py` held Up for four requested seconds (4.032985 host seconds including command overhead), released it in `finally`, and observed for two further seconds. It retained 301 RAM samples and before/after captures. This is write-assisted setup followed by normal input, not a pristine or controller-reachability result.

## Observed

- Initial XYZ was `(124987,-102158,328714)`, angle dwords `766/763`; final XYZ was `(303395,-73801,405307)`.
- All 301 samples had `NextLife` at `0x0059A5B0` equal to zero. Final current, preceding, and naturally updated auxiliary positions matched. The final frame shows Flik in retail terrain/grass. This is not a claim that every sample was grounded.
- The cached contact reference initially remained source 99, file offset `47716`, from the original spawn. Its first observed refresh was at about 0.479 seconds to source 98, offset `43352`. Source transitions subsequently included 98, 5, 99, 93, 46, and 165. Alias/template offsets in the raw trace remain candidate mappings unless separately resolved.
- At about 1.264 seconds, XYZ `(191376,-96469,348189)` referenced retail source-99 cell `44140`. At about 2.351 seconds, XYZ `(249967,-96337,371497)` referenced cell `44248`.
- Exact projected-footprint queries independently find those respective retail cells, but no active parsed floor candidates at either position in the authored TERRAIN.ALL.
- At the earlier authored fall endpoint `(222481,-22529,383185)`, the retail projected candidate is source-99 cell `45884`; the authored active floor traversal has no candidate there. At the earlier deck start `(220590,-102402,435460)`, retail cell `47008` and authored deck cell `43936` cover the footprint at different heights.

These are active-traversal omissions, not a claim that every old cell's raw bytes were erased. Old bytes beyond an authored terminator can remain unreachable.

## Contradictions and limitations

Stationary position and matching facing did not imply fresh contact state. The earlier authored fall also retained its deck contact reference through airborne samples. A contact pointer alone is therefore not grounded-state evidence. The initial retail movement includes a transfer transient; it is not frame-for-frame comparable to natural arrival in the authored arm.

The exact footprint checks do not execute native triangle admission, falling movement, or landing. They establish a concrete geometry-coverage difference and support source-99 replacement as an explanation for missing old-floor support, but do not prove every detail of the earlier fall. The separate missing-render/retained-collision report has not yet been mapped face-by-face.

## Launch and lifecycle

The old EXP-006 preview was closed; its post-close audit was clean. Retail attempt 1 reached Training (internal 17): Return was sent 85.582 seconds after launch, beyond the documented 60-second chooser timeout. The later Level01 payload read failed in that wrong level. No memory writes occurred in that attempt. Its normal close and clean audit were retained.

One bounded retry delivered selector Return at 7.307 seconds and completed the established LevelSelect Right, Return, title Return route in 18.776 seconds. Internal level 1 and full hardware log markers were confirmed. The retry, not the superseded first launch, supplied the control.

The OG control remains open for the user: game PID/start `313931/10570967`, group `313689`, Gamescope `313698/10570821`, Xwayland `313729/10570853`, display `:2`, window `14680071`, prefix `work/experiments/EXP-20260905-007/og-preview-02/prefix`, sink `ablpc_mute_313689`. The generic session ledger labels the seven known processes unattributed; they belong to this explicitly pinned direct-procedure session. Do not close unrelated processes or claim a clean audit while this session is open.

## Artifacts

Public summary: `reports/terrain/EXP-20260905-007.json`.

Private evidence: `work/experiments/EXP-20260905-007/`, including destination evidence, authorization plan and consumed receipt, both entry arms, transfer receipts, 623 stationary samples, the 301-sample Up trace, captures, and selected footprint comparison. The earlier fall remains `work/experiments/EXP-20260905-006/preview/edge-fall-up-01.json`.

The prior material/tiling evidence archive is unchanged and does not contain this later runtime evidence. No assets, binaries, screenshots, memory captures, copied games, or Wine prefixes belong in Git.

## Follow-up

Replay the earlier fall in the original PC instruction model against retail and authored terrain, with explicit floor candidate/admission transitions. Plan an integrated layout that preserves the needed original active floors or deliberately replaces both their collision and render coverage, including a real exit/landing surface. Do not repair this by assuming the standalone box triangulation is broken. Map the separate invisible-ground report to exact render faces and collision cells. No new mesh or collision edits were made in this experiment.

## Later whole-Level01 audit

[[EXP-20260905-008 - Whole-Level01 collision and render coverage audit]] independently confirms the edit boundary across all sources: only payload 99 changed, retiring all 134 original active cells and replacing them with 14 authored cells; 7,147 other active cells are unchanged. Only static render reference 160 changed, while the earlier fall footprint retains render mesh 213. This strengthens the coverage explanation but does not substitute for the exact earlier-fall trajectory or remove this experiment's write-assisted setup limitation.
