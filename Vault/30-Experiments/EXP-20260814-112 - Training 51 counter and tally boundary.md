---
type: experiment
id: EXP-20260814-112
date: 2026-08-14
question: Does the PC Training grain counter retain and display 51, and what smallest exact executable patch preserves the original 50-grain completion milestone while allowing a 51-of-50 end tally?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; Wine 11 Staging; Gamescope; native GDB; complete ignored user-owned PC content copy
environment_version: kernel 7.0.11-200.fc44.x86_64; Wine 11.0 Staging; Gamescope 3.16.25-1.fc44.x86_64; GDB 17.1; Python 3.14.6
working_directory: /home/dev/ABLPC
configuration: complete M3.1 candidate plus exact three-byte executable patch; hardware Direct3D 640x480x16
artifacts:
  - dynamic/wine/EXP-20260814-112-receipt.md
  - static/exports/BIN-97c95ba5572dce63/M3-training-grain-counter-tally-static-trace.md
  - work/copies/M3-training-51-counter-full-disc/evidence/accepted-transition-49-to-50-gdb.txt
  - work/copies/M3-training-51-counter-full-disc/evidence/accepted-transition-50-to-51-gdb.txt
  - work/copies/M3-training-51-counter-full-disc/evidence/accepted-post-51-hud-gdb.txt
  - work/copies/M3-training-51-counter-full-disc/evidence/final-accepted-tally-51-complete-gdb.txt
  - work/copies/M3-training-51-counter-full-disc/evidence/final-accepted-tally-visible-51.png
addresses:
  - 0x00416890
  - 0x00417720
  - 0x00439E90
  - 0x00442E70
  - 0x00599ABE
  - 0x0059D9B1
file_offsets:
  - 0x422CB
  - 0x422CF
  - 0x42327
result: accepted-retained-displayed-51-with-original-50-milestone
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - re/dynamic
  - re/gameplay
  - re/executable-patch
  - milestone/m3
---

# EXP-20260814-112 - Training 51 counter and tally boundary

## Question

Does the PC Training grain path retain and display a 51st pickup, and what is
the smallest reversible executable patch that lets the end-of-level tally
retain 51 without losing the original 50-grain completion/emblem event?

## Inputs

- retail `bugs.exe`: 1,069,056 bytes, SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- M3.1 Training `LEVEL1.DAT`: 115,076 bytes, SHA-256
  `20d0f9b143a4fceeb058d5ce81680b3e6317995abc3d5ac4103fc85e79b5fd40`
- accepted patched `bugs.exe`: 1,069,056 bytes, SHA-256
  `8ececefbe1e5747322bd635830f4125500c087d3769094b79545bd7a7b6a4456`

All game bytes remained in ignored work copies. `originals/` was not modified.

## Independent population checks

Exact inverse transformations produced 49-, 50-, 51-, and 52-record Training
tables with structurally consistent type-`0x3F` counts 61 through 64. The 49
and 52 arms are parser-level boundary checks only; they were not presented as
runtime display results. Exact sizes and hashes are in the runtime receipt.

## Pickup and HUD result

Static flow shows that `0x00417720` increments byte counter `0x0059D9B1` and
then compares the result with exactly 50. Controlled PC runtime transitions
independently establish the branch semantics:

- `49 -> 50` reaches the exact-50 event at `0x00417DCF`;
- `50 -> 51` reaches the non-equality path at `0x00417E92` and retains 51.

At retained count 51, `0x00416890` builds digit cache word `0x0105`, bytes
`(5,1)`, and calls the two digit draws. This resolves the in-level HUD
boundary without changing the executable.

## Tally boundary and exact patch

`0x00442E70` separately clamps the end-of-level tally to 50 and awards the
completion state only for exact equality. The accepted recipe changes exactly
three bytes:

| File offset | VA | Original | Replacement |
|---:|---:|---:|---:|
| `0x422CB` | `0x00442ECB` | `0x32` | `0x33` |
| `0x422CF` | `0x00442ECF` | `0x32` | `0x33` |
| `0x42327` | `0x00442F27` | `0x75` (`JNE`) | `0x72` (`JB`) |

The first two edits retain 51 in the tally. The branch edit changes the
completion condition from exactly 50 to unsigned count at least 50. It leaves
the original exact-50 pickup event, tally sound/event, `/50` denominator, and
completion/emblem render path unchanged.

## Runtime acceptance

The exact candidate passes the Direct3D/640x480x16 Training load gates. The
final controlled tally starts at retained count 51 and zero completion flags,
then:

- takes the completion path at the patched branch;
- sets the completion flag to 1;
- reaches the bright completion/emblem path at animated count 50;
- continues the tally to retained/displayed count 51;
- visibly renders `51/50` with the completion UI.

This combines PC static control flow, controlled memory/breakpoint evidence,
and a visible behavioral outcome.

## Corrected inference and rejected candidate

`EXP-20260814-111` reported the literal-50 write in `0x00439E90` as a Training
counter clamp. The static cap exists, but a 30-second breakpoint window after
the Training `49 -> 50` transition did not reach its write. Restoring its
original literal still allowed 51 in the in-level counter, HUD, and final
tally. Its Training applicability is therefore reclassified as unconfirmed.

A preliminary candidate that changed that unrelated literal and kept the
original tally `JNE` is rejected: it made an unnecessary fourth byte change
and count 51 did not set the completion state. A separate early breakpoint
method that faulted Wine in the hot tally loop is also rejected; the clean
accepted run used a dynamically installed post-count-50 breakpoint.

## Asset-free implementation

- `reimplementation/ablpc/training_grain_counter_mod.py` applies the exact
  source/output-hash-locked three-byte recipe and proves its inverse.
- `scripts/make-training-51-counter-cap` restricts input and output to
  `work/copies/`, refuses overwrite, and preserves executable mode.
- `tests/test_training_grain_counter_mod.py` covers exact unknown-byte
  preservation, inverse reconstruction, wrong-source rejection, overlap
  rejection, and the public recipe's asset-free rejection boundary.

## Result

**Accepted.** M3.2 is complete at a `51/50` bonus boundary: 51 records are
collectible, the live counter and HUD retain/display 51, the final tally
retains/displays 51, and the original 50-grain completion/emblem milestone is
preserved. Redesigning the denominator or emblem artwork is deliberately out
of scope; either would be a separate authored game-design mod.

## Follow-up

Choose another concrete gameplay behavior for the next bounded M3 packet.
Do not continue changing the 50-grain emblem or goal presentation solely to
expand this already discriminated counter boundary.
