---
type: experiment
id: EXP-20260813-038
date: 2026-08-13
question: Which exact retained candidates produce differing 0x80-stride arena intervals during matched Direct3D control/replacement/control arms?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; Wine 11.0 Staging; Gamescope; GNU GDB 17.1
environment_version: gdb-harness 1.2.0; watch/result schema 3
working_directory: /home/dev/ABLPC
configuration: Fresh Direct3D control/replacement/control; candidate indices 0-7 and 9-23; read-only post data watch; zero-post fail-closed metadata only
artifacts:
  - dynamic/wine/EXP-20260813-038-comparison.txt
  - dynamic/wine/RUN-GDB-20260813-101022
  - dynamic/wine/RUN-GDB-20260813-102253
  - dynamic/wine/RUN-GDB-20260813-102505
  - dynamic/wine/RUN-GDB-20260813-102626
addresses:
  - 0x0044C898
  - 0x0044C89E
  - 0x0044C8A5
  - 0x0044C8AB
  - 0x0044F8E0
  - 0x0044F9DD
  - 0x0044F9F1
  - 0x005B18E0
  - 0x008082C8
  - 0x0081BC28
  - 0x0081C138
result: bounded-negative-zero-active-arena-records-all-candidates
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/dynamic
  - re/resources
  - re/rendering
---

# EXP-20260813-038 - Per-entry submission-arena negative

## Question

During matched Direct3D control/replacement/control arms, which members of
exact candidate set `{0-7, 9-23}` produce differing intervals in the
`0x80`-stride arena rooted through `0x0081BC28`?

## Approval and bounds

The user's explicit M2.25 instruction supplied the approval required by
[[Agent Operating Manual]] for read-only hardware points and execution
control. The experiment never wrote target memory, registers, code, or game
files; never armed `0x0044D794/0x0044D79A`; retained no arena payload bytes;
consulted no PS1 source; and stopped on every signal, order, identity,
survival, or arena-state contradiction.

## Inputs and procedure

- Reverified exact executable SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Reused fresh exact M2.20 staging: unchanged `FLICK.ALL` SHA-256
  `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`
  in both controls and equal-size replacement SHA-256
  `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.
- Extended the read-only GDB harness to schema 3 with ordered bounded
  submission capture, SHA-256-only output metadata, exact address/capacity
  checks, terminal contradictions, and a synthetic fixture regression.
- Rejected execution-breakpoint preflight `RUN-GDB-20260813-101022` after one
  stop at `0x0044C898` was followed by same-PC `SIGSEGV`. The hardened harness
  deleted its points, detached, and proved target survival; the arm supplies
  tooling evidence only.
- Used one hardware access watch at header pointer global `0x005B18E0` in
  accepted arms. The exact loop read at `0x0044C8A5` reports stop PC
  `0x0044C8AB`, current entry in `ESI`, and a boundary after return
  `0x0044C89E`. Intervening native instructions restore `EDI`, pop the call
  argument, and load the watched global; none touches the arena globals.
- Required one warmup rollover and one complete ordered 24-entry cycle.
  Retained rows only for exact candidates `{0-7, 9-23}`.
- The `zero_post` mode accepted only coherent
  `(counter, capacity, base) = (0, 0, 0)`. Native `0x0044F8E0` checks counter
  against capacity before its allocator sequences and only increments the
  counter; it has no reset/decrement. Therefore an accepted all-zero post
  proves exact pre/post zero and an empty interval. Any active/inconsistent
  state failed closed.

## Expected discriminator

A candidate with a replacement interval count or digest differing from both
controls would shrink the exact 23-entry set. Equal intervals would retain a
bounded negative. Any active state outside the configured bounds, signal,
order failure, or survival failure would reject the arm.

## Observed

Accepted runs are `RUN-GDB-20260813-102253` (control A),
`RUN-GDB-20260813-102505` (replacement), and
`RUN-GDB-20260813-102626` (control B). Each reports:

- exact process/executable ownership;
- `capture_complete` after 55 data-watch stops;
- one installed and deleted watchpoint, verified cleanup, and detach;
- no target signal;
- five resumed/untraced post-detach survival samples;
- one complete candidate table with 23 rows.

Every row in every arm has `pre_counter=0`, `post_counter=0`,
`record_count=0`, `byte_count=0`, and SHA-256(empty)
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
Zero arena payload bytes were read or retained. The exact differing-emission
set is empty.

Every 1,480-line game log proves 640x480x16 Direct3D, the exact selected
`.ANM/.ALL` loads, `End InitMainGame`, and `NextLife`, with no
`INITSOFTRENDER`. Removing only clock calibration lines makes the three logs
byte-identical with SHA-256
`d5370bc4284a1b89ad06ed454d8ceebc8d89620f63dc605bdf362329b6987692`.

## Independent checks

- Native disassembly confirms the exact `0x0044C89E-0x0044C8AB` post-return
  instruction window does not touch the arena globals.
- Native disassembly independently confirms capacity checks before allocator
  sequences and increment-only counter updates in `0x0044F8E0`.
- All three accepted results independently reproduce the complete 23-row
  zero table, cleanup/detach, and five-sample survival receipt.
- The synthetic fixture proves both paired digest capture and coherent
  zero-post capture without retaining payload bytes.

## Confirmed

- Every M2.24 candidate call returns with the candidate arena inactive in all
  three accepted Direct3D arms.
- No candidate produces a differing record interval or digest in that arena;
  the exact changed-emission set is empty.
- The conditional static arena path shared with `0x0045A7F0` is not active for
  these calls in the tested Direct3D start-state trajectory.

## Inferred

The arena's prior “hardware submission” semantic label is not supported as
the active explanation for M2.20's Direct3D-visible difference. The structure
remains a confirmed shared conditional output arena, but renderer ownership
must be reconciled before stronger naming.

## Contradictions and limitations

- The conditional static convergence from `EXP-20260813-036` remains true,
  but the runtime arena is uninitialized during the exact accepted Direct3D
  window. Static reachability did not establish active runtime emission.
- Hardware execution breakpoint `0x0044C898` is another same-PC continuation
  fault on this Wine/GDB setup. Cleanup/survival proves safe rejection, not
  safe continuation.
- This result does not rule out non-arena effects inside `0x0044F8E0`, other
  retained-entry consumers, copied/persistent state, another renderer path,
  pixel attribution, M1 placement identity, or `.ALL` semantics.

## Result and follow-up

M2.25 is complete with a bounded negative. M2.26 should statically reconcile
renderer dispatch: trace which initialization/consumer path is active under
the proven Direct3D selector, determine why the conditional `0x80` arena
remains inactive, and identify the nearest alternate PC-native path capable of
carrying retained-entry differences. Do not begin general `.ALL` tooling,
semantic naming, PS1 comparison, or further live instrumentation unless the
static discriminator leaves one exact approved question.
