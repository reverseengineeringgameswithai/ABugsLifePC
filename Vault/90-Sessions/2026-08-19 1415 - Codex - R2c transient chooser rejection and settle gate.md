---
type: session
date: 2026-08-19
agent: Codex
topic: R2c transient chooser rejection and settle gate
tags:
  - session
  - re/runtime
  - re/level-format
---

# 2026-08-19 1415 - Codex - R2c transient chooser rejection and settle gate

## Goal

Run the James-accepted RC0-F0-006 executor, preserve its fail-closed result,
and prevent startup/fade frames from being mistaken for a stable renderer
chooser in later R2c work.

## Runtime result

RC0-F0-006 passed the retail source/stage hashes, baseline-prefix mapping,
installed-layout CD identities, exact game PID/start/PGID/cwd, current `Bugs`
window, and `640x480` geometry. Its three one-second-spaced compositor frames
were not stable:

- `chooser-1.png`: two-color white/black startup transition, decoded-RGB
  SHA-256 `9124b62c96bb246f339cb4252f575402b670bf2e0dbafe3082e77a68a13d6413`;
- `chooser-2.png`: darkened transition, decoded-RGB SHA-256
  `64a124c5...94359`;
- `chooser-3.png`: the existing stable no-direction chooser, decoded-RGB
  `5b203faf...752c7`, PNG `b340afa0...6727bb`.

The first two identities are rejected transition evidence and are not in the
chooser-presence allowlist. The third does not identify renderer selection; it
only reproduces the previously accepted chooser-presence identity.

## Safety and cleanup

The gate rejected before Return. `disposition.json` records no Return attempt,
no directional input, no F0 signal, no process-memory read, and no DAT write.
Normal close failed, so the executor retained the non-clean audits and guarded
group TERM/KILL plus exact residual Wine-device cleanup provenance. Its final
audit is clean, baseline `R:` resolves to retail, and the ignored packet is
quarantined at
`work/copies/EXP-20260819-002/evidence/rejected/RC0-F0-006/`.

## Frozen correction and next action

RC0-F0-007 adds a fixed `4.000 s` no-input chooser settle with repeated exact
PID/window and pre-Return log checks. One absolute `45.000 s` deadline covers
launch through Return. Every compositor command receipt is atomically retained
immediately after capture, and image dimensions/hashes/state are retained
before the triplet verdict. Unknown, transient, black, wrong-size, unstable,
terminal-log, or deadline outcomes still stop before Return and clean up.

James rejected the first committed correction because the absolute deadline
bounded capture but not the final focus/keydown path, and because its named
transition regression used synthetic unknown frames. The follow-up extends the
same deadline through selector revalidation, activation, focus, focused-window
query, and the immediate pre-keydown gate; expiry records
`failed-before-keydown` and sends no Return. It also asserts the two exact
retained transition RGB hashes are absent from the runtime allowlist while the
known stable chooser hash remains present.

At that session checkpoint, the face-8 localizer remained prohibited until a hardware-qualified F0 result
is documented, committed, and James-accepted.

## Links

- [[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[PC autonomous game control]]
- [[2026-08-19 1243 - Codex - Anthill R2c renderer setup rejections]]
