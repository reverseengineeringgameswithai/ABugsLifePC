---
type: experiment
id: EXP-20260815-121
date: 2026-08-15
question: Does the first user-recorded companion movie reproduce hardware selection, Training entry, and Training completion in a fresh pristine PC process?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; Wine 11.0; Gamescope; exact-window X11 keyboard movie 1.0.0
environment_version: input-movie.py a168485131bc54e7c8bdff5cf43f0be17310f0fed77d75d5cb32d3d538ebbeee
working_directory: /home/dev/ABLPC
configuration: pristine PC work copy; research/windowed/muted; one disclosed pre-replay Down; immutable manual-delay movie 49261fa3efc66dd3ec5c2b56ad0733b4ff02dadd6bbd023be42198916eeb73f9
artifacts:
  - dynamic/wine/RUN-INP-REC-20260815-145456/metadata.json
  - dynamic/wine/RUN-INP-REP-20260815-150349/metadata.json
result: input-dispatch-accepted-gameplay-diverged-at-level-select
created: 2026-08-15
updated: 2026-08-15
tags:
  - re/experiment
  - implementation/tooling
  - input/replay
  - cap/CAP-002
---

# EXP-20260815-121 - First companion route replay divergence

## Question

Does the first live companion recording reproduce the user's observed route
from hardware selection through Training completion in one fresh pristine PC
process?

## Inputs and boundary

- The user described the recording route as hardware acceleration, Training,
  and level completion.
- The path copied from the companion after recording,
  `work/copies/input-movies/input-20260815-145546.input-movie.json`, did not
  exist. The accepted record receipt identifies the actual create-only output
  as `input-20260815-145429.input-movie.json`; after success, the companion had
  advanced its editable field to the next unused filename.
- The actual movie validates as schema 1, SHA-256
  `49261fa3efc66dd3ec5c2b56ad0733b4ff02dadd6bbd023be42198916eeb73f9`,
  schedule SHA-256
  `e93b9574b121768a20b7113ab95d2eee6c308e8d093bee2290a10b6eabb17960`,
  306 paired events, 49,446,914,276 ns duration, and manual-delay anchor.
- The movie under `work/` is not a Git artifact. Only its asset-free record and
  replay receipts are retained.
- No debugger write, game/file mutation, PS1 evidence, or movie edit was used.

## Static movie observation

The first event is Return down at `5,336,396,012` ns; the second Return begins
at `6,729,063,035` ns. There is no Down before either event. The first recorded
Down is sequence 108 at `23,314,798,101` ns, followed by two later gameplay or
menu Down pairs. Therefore the renderer-selector Down described by the user is
absent from the immutable movie.

**Confirmed:** input before the manual-delay anchor is not present in this
movie. **Inferred:** the user highlighted Hardware during the companion's
three-second arming interval, then Return became the first post-anchor event.
The current GUI does not expose an anchor-reached transition, so the exact
moment of the omitted Down was not independently timestamped.

## Discriminating replay

The first fresh window the user saw at the software selector had not yet begun
movie dispatch; target discovery was still pending. It is not counted as a
replay arm.

For the actual replay, a fresh exact retail-PC process was identified as PID
19114, process group 18873, nested display `:2`, focused 640x480 window
14680071. One disclosed exact-window Down was sent before replay, solely to
restore the missing Hardware highlight. The movie remained byte-identical;
its first Return confirmed the selected renderer.

`RUN-INP-REP-20260815-150349` then accepted:

- 306/306 events dispatched;
- schedule and movie hashes exact;
- all held keys released;
- maximum absolute dispatch drift 17,771,362 ns; and
- no input-layer failure.

The fresh work-copy `bugs.log`, SHA-256
`b26a80451ca4747f54ae68a5cbc2bd2a58989ec73191f677660d45cdaffe0aea`,
contained the independent hardware gates at lines 74-76 and 127:

- `Native software render mode is FALSE`;
- `RenderMode set to Direct3d render mode`;
- `Screen mode 640x480x16 selected`; and
- `Starting Direct3D renderer`.

The same log reached `LevelSel` and `--- Start LevelSelect ---`, but its only
packet-data load was `level00/level.raw`; it contained no Training level load.
The user independently observed the selection moving back and forth in
Flik's Journey without entering the level.

## Result

**Confirmed:** exact-window replay dispatch works for this movie, and the
disclosed missing-Down compensation reaches the hardware renderer. It does not
reproduce Training entry or completion.

**Strong inference:** the second and later menu inputs are tied to elapsed time
from a manual button/countdown anchor rather than a repeatable game state. The
second Return is only about 1.393 seconds after renderer confirmation; in the
fresh process it can be consumed before Level Select is ready. With no later
Return in the movie, subsequent arrows can move the menu but cannot enter
Training. This explains both the accepted input receipt and divergent visible
outcome without treating dispatch acceptance as gameplay acceptance.

**Unknown:** which exact game-ready marker and neutral delay will make the
complete route repeatable. A fresh log-anchored record/replay pair is required.

## Companion lifecycle observations

Terminal Ctrl-C landed inside Tk's polling callback, produced a
`KeyboardInterrupt` traceback, and left verified Gamescope reaper processes
and a private `ablpc_mute_*` sink after the group leader changed state. Each
residue was removed by exact PID/process-group/module identity, and the final
host process/sink audit was clear. The GUI Close action itself was not
falsified by this arm; the finding is specific to terminal interruption and
group-leader-dependent fallback cleanup.

## Required correction boundary

Before using the companion for KU-057:

1. record and replay from the same fresh game-state/log milestone rather than
   independent manual delays;
2. make the anchor/countdown state explicit and prevent setup input from being
   silently omitted;
3. distinguish the last saved movie from the next output filename;
4. expose a safe replay workflow that establishes hardware mode before the
   movie anchor; and
5. make signal cleanup retain and terminate the exact owned process group even
   if its original leader exits.

No correction was implemented in this diagnostic packet.

## Links

- Companion implementation packet:
  [[EXP-20260815-120 - PC input movie companion controls]]
- Recorder contract and limitations: [[PC input movies]]
- Capability gap:
  [[Reverse Engineering Capability Gaps#CAP-002 — Deterministic PC input movies]]
