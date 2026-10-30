---
type: session
date: 2026-08-14
agent: Codex
topic: Training 51 counter and tally boundary
updated: 2026-08-14
tags:
  - session
  - milestone/m3
  - re/gameplay
---

# Training 51 counter and tally boundary

## Goal

Continue the user-confirmed M3.1 Training mod into the smallest rigorous
counter/completion packet: test smaller and larger populations, discriminate
`49 -> 50 -> 51`, preserve the original 50-grain completion/emblem behavior,
and patch only what the PC runtime proves necessary.

## Work completed

- Refreshed the required START HERE, state, environment, roadmap, charter,
  operating-manual, and relevant gameplay/implementation notes.
- Produced exact-inverse 49-, 50-, 51-, and 52-record DAT population arms.
  Only the 51 arm was used for runtime conclusions; 49 and 52 remain parser
  boundary checks.
- Traced PC pickup function `0x00417720`, HUD function `0x00416890`, candidate
  cap function `0x00439E90`, and end tally `0x00442E70`.
- Proved the exact-50 pickup event fires for `49 -> 50`, while `50 -> 51`
  takes the non-equality path and retains 51.
- Proved the unmodified in-level HUD caches bytes `(5,1)` for count 51.
- Rejected a preliminary fourth edit in `0x00439E90`: its cap was not reached
  in the controlled Training window and is not needed for retained 51.
- Rejected the original exact-equality tally branch because count 51 then
  failed to set the completion state.
- Accepted a three-byte tally patch at file offsets `0x422CB`, `0x422CF`, and
  `0x42327`; exact inverse reconstructs the retail executable.
- In the final clean runtime, retained count 51 set completion flag 1, reached
  the bright completion/emblem path at animated count 50, continued to 51,
  and visibly rendered `51/50`.
- Added the asset-free exact patch module, work-copy-only CLI, and synthetic
  regression tests.

## Evidence

- [[EXP-20260814-112 - Training 51 counter and tally boundary]]
- `dynamic/wine/EXP-20260814-112-receipt.md`
- `static/exports/BIN-97c95ba5572dce63/M3-training-grain-counter-tally-static-trace.md`
- [[FUNC-97C95BA5572D-00416890]]
- [[FUNC-97C95BA5572D-00417720]]
- [[FUNC-97C95BA5572D-00439E90]]
- [[FUNC-97C95BA5572D-00442E70]]
- [[Decision Log#DEC-20260814-109 - Complete M3.2 at the 51-of-50 bonus boundary]]

## Contradictions and method corrections

M3.1 correctly identified a literal-50 cap in `0x00439E90` but inferred it as
a Training boundary before runtime provenance. M3.2 did not observe it after
the controlled transition, and retail bytes at that site coexist with a live
and tallied 51. The Training attribution is withdrawn, while the static cap
and unknown function identity remain recorded.

An early software breakpoint installed in the hot tally loop caused a Wine
page fault at `0x00443442`. That arm is rejected. The accepted final run
installed the breakpoint only after observing the bright path at count 50 and
then reached animated count 51 without the fault.

## Scope decision

M3.2 ends at `51/50`: the 51st grain is a bonus beyond the original goal. The
original exact-50 event, denominator, and completion/emblem presentation remain
intact. Emblem artwork or goal redesign is a separate mod, not unfinished RE
in this packet.

## Cleanup

Every owned game, Wine, Gamescope, reaper, GDB, and private sink instance was
closed by exact ownership identity. The Wine `Y:` mapping was restored to the
prior M3.1 complete-tree candidate. Generated game bytes and captures remain
ignored under `work/`. A final audit found one waiting owned
`gnome-screenshot` helper and its shell wrapper; both exact PIDs closed after
`TERM`, and the subsequent process/sink audit was empty.

## Validation

- exact real-binary recipe reapplication: 3 bytes changed, output SHA-256
  `8ececefbe1e5747322bd635830f4125500c087d3769094b79545bd7a7b6a4456`,
  inverse exact;
- focused M3.1/M3.2 tests: 8 passed;
- `make check`: Python doctor passed; Vault 326 notes/0 errors/0 warnings;
  M4 compatibility five anchors valid; 517 tests passed; tracked audit 0;
- `git diff --check`: passed.

## Next packet

Ask for another concrete gameplay change and choose the smallest corresponding
M3 stream. Do not extend the Training counter/emblem work without a distinct
goal.
