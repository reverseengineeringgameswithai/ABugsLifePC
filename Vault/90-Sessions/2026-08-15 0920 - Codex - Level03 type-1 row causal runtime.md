---
type: session
agent: Codex
date: 2026-08-15
status: completed-with-open-natural-trigger
tags:
  - m3
  - runtime
  - checkpoint
  - level-dat
---

# Level03 type-1 row causal runtime

Experiment: [[EXP-20260815-116 - Level03 type-1 row discriminator]]
Receipt: [[EXP-20260815-116-receipt]]
Implementation: [[Level03 type-1 row discriminator]]

## Objective

Test the Level03 type-1 row-6 X discriminator against the PC executable and obtain an independent hard-truth review.

## Work completed

- Launched an exact control full-disc copy and a one-byte candidate full-disc copy through the project launcher with private audio sinks.
- Confirmed renderer, visible `tunnels` menu selection, internal level ID `3`, Level03 log paths, executable identity, live type-1 pointer, and live row-6 values.
- Replayed a controller route into the row-6-nearest region for both arms.
- Isolated the `NextLife` dispatcher and Level03 coordinate consumer statically at `0x0043DC88..0x0043DCA6`, `0x0042DDB0..0x0042DDC7`, and `0x00432930..0x004329E3`.
- Demonstrated that `level_done=2` alone logs `NextLife` but does not reposition the actor.
- Reproduced the missing natural-path prerequisites with two disclosed debugger writes and captured exact control and candidate reset coordinates.
- Observed the predicted runtime delta: row-6 X `+128` caused reset X `+4096`, with reset Z unchanged.
- Preserved only asset-free durable evidence; screenshots and raw traces remain ignored under `work/`.
- Removed all owned runtime groups/sinks and restored the original Wine `y:` mapping.

## Boundary

The row-to-reset consumer is causally confirmed on PC. A natural enemy-death receipt is not confirmed. KU-057 remains open for the upstream natural producer and a reproducible no-write death trigger.

## Evidence

- [[EXP-20260815-116-receipt]]
- `bugs.exe` addresses `0x00432930`, `0x0042DDB0`, `0x0043DC88`
- Level03 DAT physical offset `0x4A4`
- Candidate SHA-256 `4894b6159e5a36a37fb9a3f50243cdd816fa4e7f28e169bcadf45b48792d4c12`
