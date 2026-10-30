---
type: session
date: 2026-08-19
agent: Codex
topic: R2c auto-hardware F0 pivot
tags:
  - session
  - re/runtime
  - re/level-format
---

# 2026-08-19 1530 - Codex - R2c auto-hardware F0 pivot

## Navigation-only feasibility

At the user's direction, the established `play-pristine.sh --auto-hardware`
route passed all six Direct3D markers and reached Anthill Level01 with exactly
`Right`, `Return`, `Return`. That run was not preregistered as F0. It was closed
and retained an accounted normal-close, launch-group, residual-device, and
final-clear lifecycle. It must never be promoted or reused as an arm.

## Accepted design pivot

James accepted a new build-scoped protocol design. Retail staged assets remain
exact, but the actual executed image for F0 and later localizer arms is the
canonical accepted auto-hardware cache, hash `1e1d5099...a9c41f`. The executor
must never claim the staged retail `bugs.exe` was executed. It proves the exact
two transform spans, nine changed bytes, every other byte equal, and an exact
inverse to retail hash `97c95ba5...27b878`.

The argument-free `scripts/r2c-f0-auto-hardware.py` owns fresh paths, mapping,
audits, launch, build/PID/window/log identity, the exact three navigation keys,
title-keyup `t0`, exact-PID `SIGSTOP` at `t0 + 3.300000000 s`, stopped-task
states, bounded read-only snapshots, three compositor captures, exact-PID
`SIGCONT`, cleanup, and retail-link restoration. F0 accepts only the frozen
retail reference image: PNG `4a5bfde1...f62f88b`, decoded RGB
`b8290da...b6451`.

James's prelaunch audit found that the first executor revision stored rather
than validated the Level01 title, left a numeric-PID race before `SIGSTOP`, did
not continuously guard window focus, and could classify unresolved cleanup as
rejected. The corrected executor requires the exact Level01 and
`ClearLoadScreen` log identities, one of two independently reviewed title-image
hash pairs, an immediate identity guard before the level-index read, `pidfd`
signals, continuous same-window focus, and pending evidence on cleanup or
restoration failure. Authorization is now recorded unambiguously as exactly
three read-only ranges: pre-title `(0x00861c84, 4)` and stopped
`(0x005b58e0, 18)` plus `(0x005bdb8c, 12)`. No memory write is authorized.

A second prelaunch audit found that the production evidence destination parents
were absent even though the first lifecycle fixture created them, and that the
inherited selector queries were unbounded during the freeze interval. The
executor now creates and validates its own canonical `accepted/` and
`rejected/` parents before requiring fresh final paths. Every ownership/focus
subprocess is bounded by the remaining freeze deadline; a timeout occurs before
any signal and the lifecycle test proves cleanup and `R:` restoration run.

The first post-acceptance command attempt did not launch: the clean pre-audit
was followed by a wrapper import failure for nonexistent `scripts/_bootstrap`.
No stage or game process existed and no runtime action occurred. The wrapper
now uses the same `__file__`-relative `reimplementation/` bootstrap as the
working RC0 executor, with a direct subprocess entry-point regression that
cannot reach launch because it supplies a rejected extra argument.

The next launch became `F0-AH-001` and passed the exact build/assets/drive and
complete Direct3D gates. It rejected before input when the first exact main
window query returned zero results immediately after the sixth marker. The
packet contains no input, signal, memory-read, capture, or DAT-write receipt;
cleanup and the immediate post-close audit are clear. James accepted the run as
a main-window readiness race, not an auto-hardware failure. The committed
successor uses fresh `-002` stage/evidence identities, polls zero-window states
only within the existing absolute launch deadline, rejects every nonzero wrong
or ambiguous identity, and retains a final log snapshot before cleanup.

`F0-AH-002` reached the full renderer gate but rejected before input on two
same-PID X11 window IDs. Its final log and cleanup are retained and James-
accepted. Audit showed the implementation counted every same-PID Wine window
before inspecting which was the main `Bugs` window. The fresh `-003` design
receipts all IDs/names/geometries/owners before verdict, treats non-`Bugs`
windows as retained helpers, rejects malformed named-`Bugs` windows, and counts
only exact main candidates for zero/one/multiple readiness.

`F0-AH-003` then retained 485 polls through the fixed deadline. They consistently
show same-PID XID `14680071`, `640x480`, titled `Loading - A Bugs Life`, plus a
1x1 `Default IME`; the hardware log reached LevelSelect. No runtime action was
sent. James accepted the rejection and identified the exact-`Bugs` title rule
as false. The fresh `-004` branch pins the loading-titled XID, replaces every
inherited rediscovery guard, permits only `Loading - A Bugs Life`/`Bugs` on that
same XID, and receipts each title transition before the next action.

James's `-004` prelaunch audit found one stale Current State paragraph and one
receipt-order gap for process-identity drift. The stale `-003 gate now` wording
is historical. A drift attempt now writes expected/current process identity,
retained XID, `process-identity-drift` disposition, and the skipped-observation
reason before rejecting; its regression proves no window query or input follows.

`F0-AH-004` passed the retained-XID gate and sent Right/Return, but rejected on
index `0` while the final log still showed Level00/LevelSelect and no Level01 or
ClearLoadScreen. James accepted its cleanup and classified it as navigation
readiness, not an index-read race. The fresh `-005` branch adds exact
LevelSelect plus fixed no-input settle before Right and log-driven
Level01/ClearLoadScreen readiness before title validation or the single index
read; failed log gates cannot reach title Return or `SIGSTOP`.

James's `-005` prelaunch audit found that success-path guard/settle work could
overrun a just-observed marker deadline and that marker receipts were written
after those fallible operations. Marker observations are now atomically retained
as validation-pending first. Every later guard and the fixed settle are bounded
by the same deadline with explicit post-operation checks; expiry prohibits the
next input, capture, read, or signal.

`F0-AH-005` passed those navigation gates and captured the genuine Level One
title, but its full-frame PNG `9a6f8495...1fd797` / decoded RGB
`c528d5e4...15dac` differed from both reviewed whole-frame identities because
of ordinary nonidentity animation. The fail-closed whole-frame rule rejected
before the level-index read, title Return, signal, stopped read, or DAT write.
James accepted that disposition and cleanup and rejected whole-frame
allowlisting as the correction.

The then-fresh `F0-AH-006` gate uses two bounds-checked decoded-RGB regions that are
exact across the independently reviewed A1/B, A2, and `-005` title frames:
`360x150+275+120` hashes to `da63e765...1eddb3`, and `590x70+25+285` hashes to
`0ae2bd62...48efe`. Full-frame hashes remain evidence only. Regressions cover
arbitrary pixels outside both regions, a one-pixel change inside either region,
wrong dimensions/crop bounds, and the rule that region failure prevents the
index read and every later runtime action. No screenshot or game asset is
tracked.

`F0-AH-006` passed the complete navigation/title/index and pidfd freeze path.
All 17 tasks stopped, four authorized view snapshots remained byte-identical,
and its three stopped frames were identical. It rejected only because derived
PNG `05f5691c...506ad1c` / RGB `2ea65643...23b9d26c` did not equal retail R2b
phase `4a5bfde1...f62f88b` / `b8290da...b6451`. James accepted the rejection,
resume, cleanup, and no-write boundary.

An exact offline receipt over retail A1/B/A2 frame 14 and all three `-006`
captures records four identical decoded-RGB camera/terrain regions. The fresh
`-007` gate requires all four plus exact triplicate reproduction of the
derived `-006` frame. A second derived whole-frame variant ends hash extension
and blocks localization pending a state predicate or dynamic-pixel mask.

`F0-AH-007` reached title Return and index `1`. The packet has 80 total main-
window guard receipts, of which 70 (`011` through `080`) are post-`t0` freeze-
interval iterations; the first 10 are earlier navigation/title/input guards.
Final identity completed with `4.346 ms` remaining, and the subsequent full XID
guard consumed most of that budget before geometry launched with a `0.255 ms`
timeout. The 70 focus iterations remained in memory, so no aggregate focus
receipt survived. No stopped read or frame exists; James
accepted the cleanup and classified this as a consumed scheduler rejection,
not the planned derived-frame test.

Fresh `-008` stops periodic samples at `deadline-0.060`, bounds the complete
final identity/window/focus guard to `deadline-0.003`, and reserves the final
3 ms only for pidfd signal scheduling. It atomically retains every successful
focus sample and an explicit `signal_sent=false` receipt for any pre-signal
failure. Deterministic-clock regressions reproduce the observed 64 ms boundary,
guard overrun, durable earlier samples, no-signal/no-read failure, and a
successful signal inside the unchanged 1 ms timing limit.

## Boundary

No runtime/debugger write or DAT write is added. Localizer creation remains
blocked until F0 is documented, committed, and James-accepted. A positive
localizer result is scoped to build `1e1d...c41f`; retail confirmation remains
mandatory for retail R2 or visible-ground promotion. The one-byte candidate
requires a later packet and fresh authorization.

## Links

- [[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[PC automatic Direct3D startup candidate]]
- [[PC autonomous game control]]
