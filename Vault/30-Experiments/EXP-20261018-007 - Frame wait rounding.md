---
type: experiment
id: EXP-20261018-007
date: 2026-10-18
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Static disassembly (capstone) of retail bugs.exe, compared with the timer rates measured in EXP-20260930-002's hardware arms; no game launch
question: Why does the gameplay timer advance 30.5–30.9 frames per wall second, not 30 (EXP-20260930-002)?
result: The frame wait 0x00405AD0 loops until 1000 / (elapsed ms + 1) ≤ the target. Gameplay sets the target to 30 every frame, and the integer division passes at 32 ms (1000 / 33 = 30), so frames last at least 32 ms. That caps the rate at 31.25 fps, and the measured 30.52–30.88 are 32.4–32.8 ms frames. Under Direct3D the half-rate mode never applies, because the frame-begin routine clears it every frame
status: complete-bounded
created: 2026-10-18
updated: 2026-10-29
evidence: [EXP-20260930-002, EXP-20260907-028, EXP-20260816-143]
tags: [experiment/static, re/timing]
---

# EXP-20261018-007 - Frame wait rounding

## Question

EXP-20260930-002 measured the gameplay timer at
30.52, 30.53 and 30.88 frames per wall second. It inferred, without tracing,
that "the excess over 30 comes from the millisecond rounding in the frame
wait `00405AD0`". This is one of the small closures in section 7 of
[[Next Tasks]].

## The wait

`0x00405AD0`, the flip at the end of a frame:

1. **Target** (`0x00405AD0`–`0x00405AFA`): `esi` = the frame-rate target
   `0x004F1710`. If the half-rate flag `0x005C2410` is 1, odd frames (bit 0
   of the frame counter `0x0081C1E8`) do not wait (`esi = −1`) and even
   frames use half the target.
2. **Present.** The flip for the selected renderer.
3. **Wait** (`0x00405B49`–`0x00405B91`). With `timeGetTime` (IAT
   `0x00864884`), it loops:

   ```text
   do  rate = 1000 / (|timeGetTime() − [0x004ED714]| + 1)
   while rate > target
   ```

   `0x004ED714` is the timestamp the frame-begin routine `0x00405BE0` stores
   at `0x00405C07`.

## The target and the half-rate flag

- **Target writers.** A skip-data sweep of all of `.text` finds 12 writes
  to `0x004F1710`. That replaces a first list from a linear sweep that
  stopped at `0x004269AB`.
  - **30, once:** `0x0040FFC0`, the entry of the per-frame gameplay routine
    (which calls the M1 coordinator `0x0044D430`).
  - **60, eleven times:** CallOptions `0x0041032D`, `0x004162D0`,
    `0x0042D562`, `0x0042E067`, `0x0042E15B`, `0x0042E64B`, the controls
    screen `0x00430DFA`, Options_Scr `0x00441D3B`, the level select
    `0x00443B5D` and `0x0049AE1C`. These are menu and screen routines.
- **Half-rate flag writers.**
  - `0x0041FF93`, in the capability probe `0x0041F990`, sets the flag to 1
    when the measured CPU speed is at most 200 MHz. Under Wine the log reads
    "CPU clock speed is 165.425152 MHZ", so it is set.
  - `0x0040FD20` clears it (`ebx = 0` from `0x0040FD34`, stored at
    `0x0040FE7F`) whenever the render selector `0x0059F7F0` is 2, Direct3D.
    Every frame-begin calls `0x0040FD20` (thunk `0x00401CD5` at
    `0x00405CAB`), and it also advances the frame counter
    (`0x0040FF0C`–`0x0040FF1B`).

  So a hardware arm runs every gameplay frame against target 30.

## The arithmetic

The integer test passes when `1000 / (e + 1) ≤ 30`. That first holds at
`e + 1 = 33` (1000/33 = 30), so the loop ends once 32 ms have passed. The
shortest frame is 32 ms, a cap of 31.25 frames per second.

The measured rates, 30.52–30.88 per second, are frames of 32.4–32.8 ms:

- the 32 ms floor;
- the `timeGetTime` millisecond step;
- the work between the wait's exit and the next timestamp.

A Speed Run limit of 1,800 frames therefore takes at least 57.6 s, which
matches the "about 58–59 s" of EXP-20260930-002.

## Side finding: F1–F5 in the frame-begin routine

`0x0040FD20` reads the DirectInput keyboard state (`0x00598A10` + scan
code, EXP-20260817-181) for scan codes `0x3B`–`0x3F`, F1 to F5. It acts on
a key edge latched by `0x004C4148`:

| Key | Action |
|---|---|
| F1 | toggles `0x004D8428` |
| F2 | toggles `0x004D842C` |
| F3 | steps `0x004C4140` down toward 0, only while word `0x0059A5F0` is 0 |
| F4 | steps it up to 4, with the same condition |
| F5 | toggles the half-rate flag, which Direct3D clears again each frame |

What the three globals control, and whether the `cheat` launch argument
matters, was not traced.

## A contradiction found on the way

EXP-20260930-001 states that "the results
screen runs at a 60 fps cap (`00441D3B` stores 0x3C)". But `0x00441D3B` is
inside Options_Scr `0x00441D20`
([[EXP-20261018-006 - Controls configuration screen and action bits]]).
None of the twelve writers lies in the results routine `0x00442E70`, so that
screen's target may be whatever value was set last.

- **Resolved the same day: the cap is 60, set elsewhere.** The trace:
  - the results routine `0x00442E70` is called once, from `0x004448B9` in
    the dispatcher `0x004447C0`;
  - that dispatcher is called once, from `0x00410364` in CallOptions
    `0x00410310` ("ROUTINE : ---Start CallOptions---");
  - CallOptions writes 60 to the target at `0x0041032D`, before that call.

  The only writer of 30, the gameplay routine `0x0040FFC0` (thunk
  `0x004014E2`), is called only from the outer loop at `0x0043DC27`, never
  inside CallOptions. So the results screen runs at target 60, as
  EXP-20260930-001 said, but because of `0x0041032D`, not `0x00441D3B`.

## Confirmed, inferred, unknown

- **Confirmed (static, matching EXP-20260930-002's measurement).**
  - The wait's test.
  - The 30 target in gameplay.
  - The 32 ms floor and 31.25 fps cap.
  - The Direct3D reset of half-rate mode.
- **Inferred.** The split of the extra 0.4–0.8 ms between timer granularity
  and per-frame work.
- **Unknown.** What F1–F4's globals do. Software-renderer timing, where
  half-rate mode would apply on this host, was not considered.

## Consequences

- **Time limits.** Any limit counted in gameplay frames runs about 2–4 %
  faster than 30 per second on this host. The native rule allows up to
  31.25. A time limit should therefore be stated in frames or with that
  tolerance.
