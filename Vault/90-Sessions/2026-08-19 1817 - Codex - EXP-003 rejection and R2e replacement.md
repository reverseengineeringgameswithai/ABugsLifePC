---
type: session
date: 2026-08-19
updated: 2026-08-19
agent: Codex
status: complete
tags:
  - reverse-engineering
  - level01
  - terrain
  - runtime
---

# 2026-08-19 1817 - Codex - EXP-003 rejection and R2e replacement

## Authorized runtime

The user explicitly authorized EXP-20260819-003 D1 then D2, including only the read-only four-byte Level01 index read at `0x00861C84`. No write, signal, stopped-view read, localizer, or candidate was authorized.

The immediate pre-launch audit and git state were clean. The frozen argument-free runner launched D1. It completed all 121 live captures, then rejected at frame 1's `lower-right-structure` hash. D2 did not launch. No accepted mask was published.

The D1 packet retained the exact derived executable/retail DAT path, hardware renderer, Anthill Level01 title/index, authorized inputs/read, all timing receipts, rejected disposition, intermediate cleanup audits, clear final audit, and restored retail `R:`. James returned **ACCEPTED for the rejection and cleanup only**.

## Offline diagnostic

The argument-free consumed-run diagnostic bound all 121 captures. It found 121 unique decoded-RGB frames, no exact sampled period, 76,807 raw whole-grid variable pixels, and 90,913 radius-three pixels. Three crop sequences were invariant; `lower-right-structure` had six hashes and first changed at frame 1.

Corrected diagnostic receipt SHA-256: `d17eeda40826280448196a78770d7e1434db6d1ba92b805114597c42b2ad4583`. It verifies all four old-D2 stage/evidence paths are absent before recording that identity as unrun-obsolete.

EXP-003 remains rejected. Its old D2 identity is unrun and obsolete.

## Replacement packet

Created [[EXP-20260819-004 - R2e Anthill stable-background calibration]]. At that historical handoff it removed all cycle/period claims, pinned the three animation-safe crops, required a fixed full-frame F0 identity, built a finite D1 whole-grid variability mask with radius-three dilation and a preregistered 35% cap, and used a separate D2 process only as an exact outside-mask holdout.

The 35% cap was selected after observing the rejected diagnostic's 29.5941% dilation; the consumed run is not independent support for it. EXP-004 has fresh stage/evidence identities and requires new explicit runtime authorization after commit and James acceptance.

## Checks at handoff

- Focused suites after James's first replacement-packet audit: 162 passed.
- No EXP-004 runtime launch occurred.
- No original/game/generated asset was added to git.

## Links

- [[EXP-20260819-003 - R2d Anthill sampled phase calibration]]
- [[EXP-20260819-004 - R2e Anthill stable-background calibration]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Known Unknowns]]

## Later disposition

EXP-004 was subsequently authorized. D1 captured all 121 frames and rejected only at the phase-sensitive exact full-frame F0 gate; its three camera-control crops remained exact. D2 did not run. [[EXP-20260819-005 - R2f Anthill phase-agnostic stable-background calibration]] supersedes it with fresh identities and no full-frame phase-reference requirement.
