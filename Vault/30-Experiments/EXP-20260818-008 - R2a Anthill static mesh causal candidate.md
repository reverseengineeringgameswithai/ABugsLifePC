---
type: experiment
id: EXP-20260818-008
date: 2026-08-18
question: Can the corpus-wide R0/R1 result be reduced to one exact, near-zero translated-component Anthill Level01 causal candidate without creating or launching a modified game file?
status: complete
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
pc_binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: offline static analysis; retail work copy; no game process
inputs:
  - "LEVEL01/LEVEL.DAT sha256:786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53"
  - "primary[81] record:0x1B58 object:0x4860 geometry:0x188CC"
evidence:
  - "[[EXP-20260818-006 - R0 the static mesh format and where visible ground lives]]"
  - "[[EXP-20260818-007 - R1 static mesh consumer, round trip, and causal candidate]]"
  - "[[EXP-20260812-013 - Level 01 target rebind no visible start effect]]"
  - "[[EXP-20260819-001 - R2b Anthill static mesh causal runtime]]"
result: One guarded Anthill byte candidate is fully specified offline; the explicitly linked later R2b follow-up was causally inconclusive.
tags:
  - re/experiment
  - re/level-format
  - re/runtime
---

# EXP-20260818-008 - R2a Anthill static mesh causal candidate

## Scope

This is the offline target-selection half of R2. It does **not** redo R0 or R1:
the format grammar was validated over all 21 retail DATs and the consumer is
executable-wide. It replaces Level03 as the **primary** causal target because
Anthill has an established repeatable hardware-D3D start capture. The exact
Level03 candidate in [[EXP-20260818-007 - R1 static mesh consumer, round trip, and causal candidate]]
remains a fallback.

No derived DAT was written. No game, Wine, Gamescope, debugger, emulator,
runtime memory write, or runtime memory read was started for this packet.

## Retail identity and bounded census

The menu-to-file mapping is PC-runtime confirmed by
[[EXP-20260812-013 - Level 01 target rebind no visible start effect]]:
`ant hill` loads `LEVEL01/LEVEL.DAT`.

- Retail path:
  `work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL01/LEVEL.DAT`
- Size: 332,824 bytes.
- SHA-256:
  `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`.
- Primary records: 484; primary type-`0x41` instances: 124.
- Secondary records: 140; secondary type-`0x41` instances: 0.

The existing parser reconstructs this file's payloads under the already
accepted 21-DAT / 2,543-payload R1 census. This packet does not create a second
grammar.

## Candidate chain

All offsets are zero-based in the exact retail DAT.

| Item | Exact value |
| --- | --- |
| section / record | primary / 81 |
| record offset | `0x1B58` |
| record center components | `(-263,-3476,-1249)` |
| record `+0x0C` / flags / object | `4528 / 0x0041 / 0x4860` |
| object translation | `(-8192,-8192,-8192)` |
| object Euler components | `(0,0,0)` |
| object bytes `+0x12/+0x13` | `8 / 192` |
| geometry pointer | `0x188CC` |
| vertices | 83 at `0x188D0` |
| tag / faces | `0x0060` / 10 |
| face array | `0x18CB8` |
| payload end | `0x18D58` |

The record's object-translated component bounds under the zero-rotation object
addition are `component-00=-2514..1988`,
`component-02=-3824..-3129`, and
`component-04=-3500..1002`. Adjacent candidates 76 and 52 continue the
same component-00 band into negative and positive component-04 respectively.
This makes record 81 the strongest near-zero translated-component test; it is
still not proof of visibility, axis semantics, or world scale.

## Reference-sharing census

The candidate is unique at both reference layers in this exact Level01 DAT:

- all primary and secondary type-`0x41` references: 124;
- references to object `0x4860`: exactly one,
  `primary[81] @ 0x1B58`;
- references to geometry `0x188CC`: exactly one, through that same object
  and record;
- all primary and secondary records, regardless of masked dispatch: object
  pointer `0x4860` occurs exactly once.

Thus this file edit reaches one scene instance, and vertex 25 reaches one face
inside its unique geometry payload. This is file-local evidence; it does not
generalize sharing rules to another DAT.

## One-face vertex selection

Face 8 at `0x18D38` contains vertex byte offsets
`(300,312,264,324)`, or vertex indices `(25,26,22,27)`. Its exact
16 bytes are:

`2c013801080144013fc000c000ff3fff`

Using simple zero-rotation object addition, its four object-translated
component tuples are:

- vertex 25: `(0,-3205,1000)`;
- vertex 26: `(-500,-3163,1000)`;
- vertex 22: `(-500,-3135,500)`;
- vertex 27: `(0,-3167,500)`.

This is an approximately 500-by-500, shallow quad near zero on translated
components 00 and 04. Vertex 25 is referenced by **face 8 only**. Combined
with the unique object and geometry reference census, the edit can directly
deform only this one decoded face in this Level01 scene.

## Exact guarded candidate

Vertex 25 starts at `0x189FC` with exact bytes:

`00207b13e8230000b8a09000`

Its signed component `+0x02` is `4987` (`7B 13`). The candidate
sets it to `7035` (`7B 1B`), a `+2048` delta. The compare-before-
write guard and locality contract are:

- require source SHA-256
  `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`;
- require `0x189FE..0x189FF == 7B 13`;
- change only physical byte `0x189FF: 13 → 1B`;
- require derived SHA-256
  `c76586991cb4cede5d58a3cae8278aca80ba2082130dcf33062b698334db0a4c`.

The existing guarded API invocation is:

`LevelDat.parse(data).set_static_mesh_vertex_component("primary", 81, 25, 2, 4987, 7035)`.

It was evaluated in memory to establish the one-byte diff and expected hash;
the returned bytes were not written to disk.

## Pre-registered prediction and competing outcomes

**Object-translated component prediction:** because the object Euler
components are zero, simple vertex-plus-object arithmetic changes the selected
tuple from `(0,-3205,1000)` to `(0,-1157,1000)`. The proven
delta is `+2048` on the second consumer input component. Axis semantics,
world scale, and a claim that these integers are PC world coordinates remain
open. The other three face corners and every other source byte remain fixed.

**Screen hypothesis, not fact:** the selected quad lies near zero on translated
components 00 and 04, while the accepted EXP-013 start frame shows a broad
floor region. If those components correspond to the start area's lateral and
depth axes, the changed corner should produce one localized wedge/spike in
that visible floor. The archived frame contains no camera transform, so exact
pixels and screen direction are deliberately not claimed.

Pre-registered interpretations:

| Observation | Interpretation |
| --- | --- |
| one localized corner/wedge moves and A1/A2 agree | joins the static decode to a user-visible Anthill surface; candidate visible-ground identity confirmed at this bounded face |
| localized movement appears elsewhere or along another screen direction | consumer causality supported; coordinate/screen hypothesis contradicted and must be corrected |
| no change while the selected quad is independently shown in view | rejects this visible-face candidate |
| no change without proving the quad is in view | ambiguous camera/selection result; does not reject type `0x41` |
| widespread corruption, crash, or unrelated geometry change | reject the candidate/grammar application; do not promote ground identity |
| game merely loads | no causal evidence |

## Authorized R2b procedure

Do not start until the user gives fresh explicit authorization for this exact
derived-file experiment. No runtime memory or debugger writes are required or
requested.

Use [[PC autonomous game control]] directly. `scripts/game-session.py` and
its companions remain fixture-only until CAP-010 and cannot supply runtime
evidence for this gate.

### Renderer chooser calibration prerequisite

No A1, B, or A2 arm may begin until a separate retail-control calibration has
established and committed the exact renderer input sequence. The calibration is
not an experimental arm and must use this fail-closed procedure:

1. Require a clear `make session-audit`, the unchanged retail executable hash,
   and the retail Anthill Level01 DAT hash before launch.
2. Launch the control work copy by the same process-isolated procedure used by
   the arms. Send no input until two consecutive one-second-spaced chooser
   captures are byte-identical. The captures may show both renderer labels; they
   prove only visual stability, not which choice is selected.
3. For calibration `C0`, send no directional input. Invoke `xdotool keydown
   Return`, request a host `sleep 0.180`, then invoke `xdotool keyup Return`.
   The `0.180 s` value is the requested sleep between separate XTEST sender
   calls, not a claim about the measured keydown-to-keyup interval. Retain both
   wall-clock and monotonic timestamps around the calls.
4. Classify `C0` as hardware only if the log contains all six Direct3D markers
   in arm step 6 below and none of its rejection markers. Classify it as software
   only if the log contains `SYSTEM MEMORY ONLY`, `INITSOFTRENDER`, or a 320x200
   gameplay surface. Any incomplete or contradictory gate is indeterminate.
5. Send no carousel or gameplay input. Close the process and require a clear
   immediate post-close `make session-audit`.
6. Record the calibration label, hashes, captures, exact input receipt, and
   retained log. Commit the result and replace arm step 5 below with the exact
   proven sequence before launching A1. If `C0` is software or indeterminate,
   freeze a separate follow-up calibration rather than inferring another input.

Calibration `CAL-C0-001` followed that procedure on the retail control work
copy. Chooser captures 2 and 3 were byte-identical at SHA-256
`b340afa0d45b447907869ffc9c45967b10999badd70835379af86ae5226727bb`.
With no directional input, the frozen `Return` command sequence produced
`SYSTEM MEMORY ONLY`,
`D3DAPPCREATE : Mode set to 320x200`, and `INITSOFTRENDER`; C0 therefore
classifies as software. Its requested sleep was `0.180 s`; the receipt's wall
timestamps measure `0.238666780 s` from keydown record to keyup record. No
carousel or gameplay input was sent, the process was closed, and the immediate
post-close audit was clear.

Follow-up calibration `C1` is frozen as follows. Repeat C0 steps 1 and 2 on a
fresh retail-control launch. Focus the owned nested window, invoke `xdotool
keydown Down`, request `sleep 0.180`, then invoke `xdotool keyup Down`; request
`sleep 1.000` and retain a chooser capture. Then invoke `xdotool keydown Return`,
request `sleep 0.180`, and invoke `xdotool keyup Return`. Apply the same complete log-only
classification in C0 step 4, send no carousel or gameplay input, close, and
require the immediate post-close audit. No other input is permitted. If C1 is
hardware, commit its receipts and replace arm step 5 with this exact sequence;
otherwise freeze a new calibration rather than selecting another input post hoc.

Calibration `CAL-C1-001` followed that frozen sequence. Its chooser stability
hash was again
`b340afa0d45b447907869ffc9c45967b10999badd70835379af86ae5226727bb`.
The retained log contains all six arm-step-6 Direct3D markers, including
`VIDEO MEMORY ONLY`, `Mode set to 640x480`, and `Starting Direct3D renderer`,
with no software rejection marker. C1 therefore classifies as hardware. No
carousel or gameplay input was sent; the process was closed and its immediate
post-close audit was clear. The requested sleep for each key was `0.180 s`.
Receipt wall timestamps measure `0.238507618 s` from Down keydown record to
keyup record and `0.239506415 s` from Return keydown record to keyup record;
these are measured command intervals, not exact physical key-hold claims.

### Fixed launch and input recipe for every arm

1. Create fresh retail-derived A1, B, and A2 work trees; never use
   `M3-training-51-grains`. Preserve A1/A2 at the retail DAT hash.
2. Generate B through the guarded API; require the exact derived hash and emit
   a receipt containing both hashes, the guard, and the one-byte diff.
3. Execute the lifecycle literally and retain all six audit outputs:
   `audit → launch A1 → close A1 → audit → audit → launch B → close B →
   audit → audit → launch A2 → close A2 → audit`. Every audit is
   `make session-audit`. Do not launch an arm unless its immediately preceding
   pre-launch audit is clear and accounted. Do not begin the next arm unless
   the preceding arm's post-close audit is clear and accounted.
4. Launch each arm detached only after its own accepted pre-launch audit, using the authoritative
   `setsid ./scripts/play-pristine.sh --research --windowed --mute`
   procedure. Bind only to the 640x480 game window and Xwayland owned by that
   process group; record PID, display, cwd, and executable hash.
5. For every key input below, use the same mechanism as C1: invoke `xdotool
   keydown KEY`, request host `sleep 0.180`, then invoke `xdotool keyup KEY`.
   The `0.180 s` value always means the requested intervening sleep, not the
   delivered interval. Retain wall-clock and monotonic timestamps around every
   keydown and keyup call. Send no input until two consecutive one-second-spaced
   chooser captures are byte-identical. Focus the owned nested window, send
   `Down` through that mechanism, request `sleep 1.000`, and retain a chooser
   capture. Then send `Return` through the same mechanism. This is the
   sequence proven by `CAL-C1-001`; do not use the patched `--auto-hardware`
   executable, and require the unchanged retail executable hash above.
6. Require all six log markers: `Native software render mode is FALSE`,
   `RenderMode set to Direct3d render mode`,
   `Screen mode 640x480x16 selected`,
   `OnlySystemMemory status VIDEO MEMORY ONLY`,
   `D3DAPPCREATE : Mode set to 640x480`, and
   `INIT : Starting Direct3D renderer`. Reject `SYSTEM MEMORY ONLY`,
   `INITSOFTRENDER`, or a 320x200 gameplay surface.
7. At the carousel, send `Right` once through the step-5 mechanism, request
   `sleep 1.000`, and screenshot the centered `Anthill` label. Then send
   `Return` through the step-5 mechanism. Reject a dropped or extra carousel move.
8. Require the log path `level01\\level.dat` and `Start ClearLoadScreen`.
   The latter is the natural blocking `Level One` title, not a completed-init
   marker: capture and verify that title before sending its `Return`. Require
   internal level index 1 by the authoritative read-only check. During the wait
   for the title, follow
   [[PC autonomous game control#The game runs only while focused]]: on the owned nested display,
   rediscover the current visible game window if its title or ID changes and
   re-issue `xdotool windowactivate --sync` plus `windowfocus --sync` at least
   once per second. Record each focus action and send no key input. Reject a
   foreign/ambiguous window or a load that fails to reach the title boundary.
9. Focus the nested game window, send `Return` through the step-5 mechanism, and
   define key-up as monotonic `t0`. Send no further input during capture.
10. Request 15 native Gamescope 640x480 PNGs at absolute monotonic deadlines
    `t0 + 0.500 + 0.200*n` seconds for `n=0..14`. Record requested
    and actual timestamps. Reject a missing/wrong-sized frame, focus loss,
    unexpected log transition, or a deadline error over `0.050 s`. Require
    `End ClearLoadScreen`, `---End InitMainGame---`, and the first following
    `NextLife` in the arm log; these occur only after the title `Return`.
11. Close the owned process group and private sink after each arm, then
    immediately run and retain that arm's post-close `make session-audit`.
    Require no unaccounted process or sink. A failed/unclear post-close audit
    stops the experiment and forbids the next launch.

### Fixed comparison and decision rule

Use all 45 decoded RGB frames; do not hand-select a favorable frame.

1. A pixel is **control-stable** only when its RGB value is identical in every
   one of the 30 A1+A2 frames.
2. Reject the run set unless at least 75% of the 307,200 pixels are
   control-stable and at least one of the 225 A1/A2 cross-arm frame pairs is
   byte-identical. These are camera/phase agreement gates, not evidence of the
   candidate.
3. A pixel is **candidate-stable-changed** only when all 15 B frames share one
   identical RGB value, the pixel is control-stable, and the B value differs
   from the control value.
4. A positive visual arm requires at least one 8-connected component of 25 or
   more candidate-stable-changed pixels, with the component visible as one
   localized surface wedge/corner in every B frame and absent from every
   A1/A2 frame. Record the full mask, component sizes/bounds, and an overlay;
   do not erase smaller components.
5. Reject causal promotion if stable changed pixels form multiple unrelated
   scene regions, if the largest component is under 25 pixels, if only animated
   pixels differ, or if human inspection cannot relate the retained component
   to one localized surface deformation.
6. Zero candidate-stable-changed pixels is a bounded no-change. Without an
   independent camera transform showing this quad in view, it remains
   ambiguous and does not reject type `0x41`.

If this fixed start capture is inconclusive, stop rather than improvising a
different edit or route. A camera sweep requires a new pre-registered packet.

## R2b outcome

The authorized A1/B/A2 hardware-Direct3D run was completed in
[[EXP-20260819-001 - R2b Anthill static mesh causal runtime]]. All three arms
passed the frozen procedural gates, but the ordered comparison stopped at the
control-agreement gate: only `108 / 307200` pixels were identical across all 30
control frames, versus the preregistered `0.75` requirement. The result is
causally inconclusive. It is not a candidate rejection, no-effect result, or
visible-ground confirmation. R1 remains complete and R2 remains open.

## Readiness history

The offline packet was complete before launch. The user then gave fresh explicit
authorization for the work-copy write and exact runtime run, while expressly
excluding runtime memory and debugger writes. The packet must still not promote
RGB, UV, tag/material semantics, world scale, all type-`0x41` meshes, or a
general terrain encoder.

## Rejected setup history

The 2026-08-19 setup run `RUN-WINE-20260819-003708` is not an experimental
arm. (2026-10-12: no run folder with this ID exists under `dynamic/`,
`reports/` or `work/`, and `make run-orphans` reports the citation as
dangling. This paragraph is the only surviving record of the run.) Its pre-input capture was blank and unstable. The attempted `Down`
sequence ended visibly on `software`; after `Return`, the log reported
`SYSTEM MEMORY ONLY` and `320x200`. This proves that specific sequence reached
the software path, but does **not** prove that an untouched stable chooser
defaults to hardware. No carousel or gameplay input was sent. The corrected
step 5 above was frozen before any accepted A1/B/A2 arm.

Setup observation `CAL-SETUP-NODIRECTION-001` is also not an experimental arm.
No input was sent. Its second and third one-second-spaced chooser captures were
byte-identical with SHA-256
`b340afa0d45b447907869ffc9c45967b10999badd70835379af86ae5226727bb`.
Both captures show `software` and `hardware acceleration` in the same styling
without a discriminating selection indicator. The process was closed and its
immediate post-close session audit was clear. This observation establishes the
visual-stability condition used by calibration, but not a selected renderer.

`R2B-A1-001` was rejected after the calibrated renderer gate and verified
`training` start because the one-second post-`Right` screenshot request used a
relative output path and produced no durable file. No level-selection `Return`
or gameplay input was sent; its immediate post-close audit was clear.

`R2B-A1-002` and `R2B-A1-003` were rejected after the calibrated renderer gate,
verified `training` -> `anthill` carousel transition, and exact retail Level01
DAT load path. Both reached `Start ClearLoadScreen`; A1-003 also retained 240
successful focus actions on the sole owned window. Existing
[[EXP-20260813-048 - Exact 0A6C consecutive-cycle live receipt]] and
[[EXP-20260812-033 - Character ALL replacement visible outcome]] establish
that this line is the natural title waiting for its start key and that
`End ClearLoadScreen`, `End InitMainGame`, and `NextLife` follow that key. The
attempts were therefore incomplete operator rejections, not game stalls. No
title `Return` or gameplay input was sent; both immediate post-close audits
were clear. Steps 8-10 now express the evidence-backed ordering.

## Links

- [[PC LEVEL DAT static mesh]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Known Unknowns#KU-079 - The render-geometry command grammar (the LEVEL.DAT draw-command stream)]]
- [[EXP-20260819-001 - R2b Anthill static mesh causal runtime]]
