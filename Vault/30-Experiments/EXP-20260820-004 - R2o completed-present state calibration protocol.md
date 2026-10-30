---
type: experiment
id: EXP-20260820-004
title: R2o completed-present state calibration protocol
date: 2026-08-20
environment: Auto-hardware D1-AH-001/-002/-003 consumed as pre-attach rejections; D1-AH-004 consumed as a first-trap task-census rejection; exact-census -005 amendment offline and unauthorized
binary_sha256: 1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f
question: Can two fresh unmodified Anthill Level01 controls reproduce exact coherent R2n state tuples and visible completed-frame sequences when each sample is bound to one successful DirectDraw presentation?
status: rejected
result: D1-AH-004 reached one exact outer-entry hardware breakpoint, then rejected before selection or scientific reads because the owned-task census changed; D2 did not launch; the later authorized -005 D1 repeated task-census drift, so R2o retries stopped and EXP-20260820-005 (R2p) became the active pickup
created: 2026-08-20
updated: 2026-10-02
tags:
  - experiment
  - pc
  - anthill
  - level01
  - static-analysis
  - camera
  - runtime-pending
---

# EXP-20260820-004 - R2o completed-present state calibration protocol

## Purpose

[[EXP-20260820-003 - R2n PC state-equivalence read candidates]] bounded exact
state ranges at two coherent instruction phases after R2m rejected wall-clock
alignment. R2o freezes the next discriminator: prove whether those exact
state tuples and a rendered image sequence reproduce across two independent
unmodified controls when each image is tied to a successful DirectDraw
presentation in the same normal update invocation.

This is not a localizer or candidate experiment. It creates no DAT and can
make no face-visibility, terrain, material, collision, causality, no-effect,
or retail-behavior claim.

## Static authority and executable scope

The complete native trace is
`static/exports/BIN-97c95ba5572dce63/R2O-completed-present-boundary.md`.
It establishes this order in a normal `0x0040FFC0` invocation:

```text
0x0040FFCF exact normal-branch operand read
0x00414585 upstream snapshot
0x0041458F generated-view snapshot
0x00405F6C successful EndScene return
0x004248F1 successful fullscreen Flip return
  or 0x004249C4 successful windowed Blt return
0x0040FFE3 outer normal-branch completion
```

`0x0040FFE3` alone is insufficient. It counts only after the exact branch
operand is read as zero at `0x0040FFCF` and exactly one
successful Flip/Blt return with all static gates below in the same guarded
PID, start tick, TID, and enclosing invocation. The six relevant native byte
ranges are byte-identical between retail SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
and executed auto-hardware SHA-256
`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`;
their exact hashes are in the static trace.

The result is build-scoped to the auto-hardware hash. Identical cited
instructions and a later matching control sequence would still not substitute
for a retail-executable intervention.

## Frozen arms and paths

Run two independent fresh processes in exact order `D1`, close/audit, then
`D2`. Both use the retail installed-layout assets and exact retail Anthill
Level01 DAT SHA-256
`786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`.
Both execute the same canonical nonsymlink auto-hardware cache above through
the accepted `play-pristine.sh --auto-hardware` route. No arm may share a
process, stage, evidence directory, debugger instance, or capture.

| Arm | Fresh stage | Pending evidence | Terminal namespaces |
|---|---|---|---|
| D1 | `work/copies/EXP-20260820-004/D1-auto-hardware-retail-005` | `work/copies/EXP-20260820-004/evidence/pending/D1-AH-005` | `evidence/accepted/D1-AH-005` or `evidence/rejected/D1-AH-005` |
| D2 | `work/copies/EXP-20260820-004/D2-auto-hardware-retail-005` | `work/copies/EXP-20260820-004/evidence/pending/D2-AH-005` | `evidence/accepted/D2-AH-005` or `evidence/rejected/D2-AH-005` |

Every final path must be canonical, nonsymlink, under the experiment root,
ignored by git, and initially absent. A later argument-free executor must pin
these literals and accept no path, hash, arm-order, count, timing, address, or
comparison override. The executor is implemented and tested offline; runtime remains authorization-gated, and
it is offline work and does not authorize launch.

## Common launch and navigation gates

Each arm inherits the accepted F0 auto-hardware identity, transform/inverse,
full-disc `R:`, CD sentinel/path, exact PID/start/PGID/cwd/window, complete
six-marker Direct3D, `640x480`, Level01 load, ClearLoadScreen, title-region,
and input-receipt gates from
[[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]].
The exact navigation is guarded `Right`, `Return`, `Return`, each using direct
XTEST `keydown`, requested host sleep `0.180 s`, and `keyup` in `finally`.
Before title Return, the sole setup read is little-endian
`uint32[0x00861C84] == 1`. After title Return no gameplay input is permitted.

The launcher and evidence packet must retain exact staged-retail and executed-
cache hashes before launch, after process discovery, before debugger attach,
before each resume, and before close. Hardware classification uses only the
complete six game-log markers with no software/mixed terminal marker. Host GPU
identity is outside this packet.

After the title Return completes, the executor must establish focus readiness
before debugger attachment. For at most exactly `2.000 s`, it may repeatedly
revalidate the exact PID/start/PGID and sole retained `640x480` game-window
XID, issue only `xdotool windowactivate --sync <XID>` and
`xdotool windowfocus --sync <XID>`, then require
`xdotool getwindowfocus == <XID>`. Each attempt is retained atomically. The
poll interval is `0.050 s`; each subprocess is capped at the smaller of
`0.500 s` and the remaining deadline. These are window-manager operations,
not game-key input. Identity/window drift rejects immediately; lack of focus
by the deadline rejects before `ptrace`, debug-register change, or any R2o
process-memory read. The existing complete process/window/focus/hash/`R:`
guard then runs immediately before attachment.

Every readiness and final pre-attach focus command must execute through the
display-scoped runner with exact `DISPLAY` from the retained
`runtime-identity-confirmed.json` discovery receipt. The receipt must bind the
same X display, Gamescope display, PID, start tick, PGID, and stage cwd on every
attempt. Missing, changed, forged, or unscoped display provenance rejects and
retains a summary before attachment. No fallback to the host display is
permitted.

Run `make session-audit` immediately before each launch and after every close.
D2 cannot launch unless D1's final post-close audit is clear and baseline
`R:` is restored to the exact retail full-disc tree.

## Exact read and execution-control set

No action in this section is currently authorized. A future authorization
must enumerate it explicitly.

### Process-memory reads

| Phase | Address | Width | Use |
|---|---|---:|---|
| pre-title | `0x00861C84` | 4 | require Level01 index `1` |
| `0x00414585` | `0x0059A5EE` | 1 | retain byte; compare bit 0 only |
| `0x00414585` | `0x00599C90` | 18 | selected common input |
| `0x00414585` | `0x0059D910` | 12 | live Flik coordinates only |
| `0x0041458F` | `0x005B58E0` | 18 | generated matrix |
| `0x0041458F` | `0x005BDB8C` | 12 | origin dwords |
| `0x0041458F` | `0x005BDBAC` | 18 | renderer-consumed matrix copy |
| `0x0040FFCF` | `0x0059A5F0` | 2 | require the exact operand about to be compared equals `0` |
| invocation/present gates | `0x0059F7F0` | 2 | require D3 selector value `2` |
| present gate | `0x0059063E` | 1 | require initialized, nonzero |
| present gate | `0x00590638` | 1 | require presentation enabled, value `0` |
| present gate | `0x00573FF0` | 4 | select fullscreen Flip vs windowed Blt gate |

Do not read optional `0x005BDB9C`, renderer scratch `0x0063E888`, any broader
matrix-copy tail, stack memory, or any unlisted global. At each hardware stop,
register reads are limited to `EIP`, `EAX`, `EFLAGS`, `DR0`, `DR1`, `DR2`,
`DR3`, `DR6`, and `DR7`.

### Execution controls

The future runner may attach a debugger only to the exact guarded owned game
PID and one atomic census of its tasks. Before any debug-register change, it
must retain each task's raw `DR0-DR3`, `DR6`, and `DR7`. `DR0-DR3` must equal
zero. For `DR6`, only defined status bits
`B0-B3/BD/BS/BT` (mask `0x0000E00F`) must be clear; reserved-one and all other
raw bits are retained, not interpreted. For `DR7`, only defined enable/control
bits (mask `0xFFFF2BFF`) must be clear. The runner preserves every bit outside
that mask.

It then arms only `DR0 = 0x0040FFC0` as a local execution breakpoint on every
initially enumerated task. The first exact hit selects the sole measured TID.
While all tasks remain stopped, the runner restores every nonselected task's
exact pre-run `DR0-DR3/DR6/DR7` values; only then may those tasks resume. A
new, missing, or changed task before or after selection rejects.

On the selected TID, `DR0` remains continuously armed at `0x0040FFC0`.
`DR1-DR3` rotate through the next expected sites. After each classified stop,
the masked `DR6` status must equal exactly the expected `Bn` for the occupied
slot. Any other `B0-B3`, `BD`, `BS`, or `BT` bit rejects before clearing. The
runner clears only `DR6 & 0x0000E00F` while preserving the remaining raw bits.

`DR7` changes only bits selected by `0xFFFF2BFF` and preserves every reserved
bit. Only local enables `L0-L3` may be set for occupied slots. Global enables
`G0-G3`, `LE`, `GE`, `RTM`, and `GD` remain zero. Every occupied slot has
`R/Wn=00` and `LENn=00`, specifying a one-byte execution breakpoint. Cleanup
restores the selected TID's exact pre-run raw values for all six registers.
These six registers are the sole writable debugger state. The runner may
stop/continue the exact tasks, but it must never change a general register,
process code/data byte, or DAT byte. It must never use a software breakpoint:
writing `0xCC` is a process-code write and is prohibited.

The state machine retains every arm/clear receipt. It starts each measured
invocation at `0x0040FFC0`, next stops at `0x0040FFCF`, and there reads
`uint16[0x0059A5F0] == 0` immediately before the compared instruction executes.
It then requires, in order, `0x00414585`, `0x0041458F`, `0x00405F6C`, exactly
one of `0x004248F1` or `0x004249C4`, and `0x0040FFE3`. All hits must use the
selected TID. Because `DR0` remains armed, another `0x0040FFC0` hit before the
current completion is an unexpected new invocation and rejects. A missed,
out-of-order, or duplicate hit, unexpected thread, process/task replacement,
deadline, or breakpoint-management ambiguity also rejects.

At `0x00405F6C`, signed `EAX` must be nonnegative. At the presentation return,
`EAX` must equal zero exactly. `0x004248F1` requires
`uint32[0x00573FF0] != 0`; `0x004249C4` requires it equals zero. Both require
renderer selector `2`, initialized byte nonzero, presentation-disable byte
zero, and normal branch word zero. Both presentation sites or another
presentation hit before `0x0040FFE3` reject.

## Exact three-invocation capture sequence

Each process records exactly three complete normal invocations, numbered
`1..3`, followed only to the `0x00414585` phase of invocation 4 for the final
completion-to-next-phase screenshot-equality check. There is no adaptive
extension, frame search, nearest
state, retry inside one process, or favorable invocation selection.

At each `0x0040FFE3` completion, stop all owned game tasks and require every
task to be in a retained debugger-stop state. Request a fixed `0.500 s` host
settle, then take exactly three native `640x480` compositor screenshots with
requested `1.000 s` gaps. Retain atomic command/start/complete/path/size/hash
receipts. All three PNG files and decoded RGB buffers must be byte-identical.

Resume only after removing or rotating the consumed breakpoint. At the next
`0x00414585` hit, before any instruction there executes, stop all owned tasks
again and take the same fixed-settle, fixed-spacing triplicate. It must be
internally identical and exactly PNG/RGB-equal to the immediately preceding
`0x0040FFE3` triplicate. This check is performed for completion 1 at
invocation-2 phase, completion 2 at invocation-3 phase, and completion 3 at
invocation-4 phase. Invocation 4 is not completed or admitted as a fourth
sample.

Thus each process retains three completed-frame triplicates and three next-
phase triplicates: 18 PNGs per process, 36 total. Frozen duplicates are
technical stability checks, not independent samples.

## Exact equality and outcome table

For invocations `1..3`, compare D1 ordinal `i` only with D2 ordinal `i`.
No cross-index pairing is permitted.

| Gate | Pass requirement |
|---|---|
| coherent upstream | selector bit, common 18 bytes, and coordinate 12 bytes exact across D1/D2 for each ordinal |
| coherent generated view | all three generated ranges exact across D1/D2 for each ordinal |
| matrix-copy self-check | `0x005B58E0/18 == 0x005BDBAC/18` at every generated snapshot |
| invocation/presentation | exact ordered hits, gates, selected TID, continuously armed `DR0` outer-entry guard, and one successful present per complete invocation |
| stopped stability | every completion and next-phase triplicate is PNG/RGB-identical internally |
| completion-to-next-phase screenshot equality | each next-phase triplicate exactly equals its preceding completion triplicate |
| cross-process display | D1/D2 corresponding completion triplicates are exact PNG/RGB matches |
| nonstatic discriminator | in each process, at least one of completion `1->2` or `2->3` changes decoded RGB |

The equality gate is empirical screenshot equality only. Static analysis does
not exclude an intervening presentation between the two PCs, including the
separate `0x0049CC40 -> ShowBackBuffer` caller, and equal pixels do not prove
surface identity. No buffer-continuity or compositor-latch claim follows.

If every gate passes, publish only
`completed-present-state-sequence-calibrated` for these two controls and exact
ordinals. This supports a future separately authorized localizer design using
the same state/pipeline gate. It does not prove general compositor synchrony.

Any state or cross-process image mismatch is
`state-sequence-not-reproducible`. Stable screenshots with no completed-frame
change are `static-sequence-ambiguous`. Wrong order, HRESULT, branch, task,
capture, identity, audit, or cleanup is `procedurally-rejected`. Every failure
publishes no reusable state tuple or frame selector and authorizes no later
arm.

## Evidence and cleanup contract

Each execution hit receives a monotonic sequence number, host monotonic and
wall-clock timestamps, PID/start/TID, instruction address, registers, active
DR state, exact read bytes/hashes, and prior/next
expected state. Each capture and each stop/resume operation has its own
receipt. The final packet retains `bugs-final.log`, complete pre/post audits,
stage/build/DAT/CD/R mappings, input receipts, debugger attach/detach and
hardware-breakpoint receipts, task-state census, screenshots, comparison
matrix, and disposition.

On every exit, clear only the exact debug registers changed by the runner,
continue any runner-stopped owned tasks, detach, close the game normally, and
use only the established guarded group/device cleanup if needed. Cleanup or
`R:` restoration uncertainty leaves evidence in `pending`; it must not move
to `accepted` or `rejected`. No successor may launch until the prior final
audit is clear.

## Authorization boundary and next action

The exact `-004` runtime authorization was consumed by the `D1-AH-004`
task-census rejection recorded below. This committed `-005` amendment does not
itself authorize another runtime. Fresh
explicit user authorization must name both D1 and D2 and cover exact-PID/TID
debugger attachment, the sole debugger-state write exception to
`DR0-DR3/DR6/DR7` for hardware execution breakpoints, bounded stop/continue
and all-owned-task stopping, the listed register/process-memory reads, and
compositor screenshots. It must explicitly prohibit software breakpoints,
general-register writes, process code/data writes, DAT writes, and every other
debugger write.

No DAT mutation, localizer, candidate, one-byte arm, or causal intervention is
part of R2o. Commit and test the `-005` exact-census amendment, obtain James
acceptance, and only then request fresh exact runtime authorization.

## Links

- [[EXP-20260820-003 - R2n PC state-equivalence read candidates]]
- [[EXP-20260820-002 - R2m offline cross-time correspondence diagnostic]]
- [[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]]
- [[PC camera view-transform chain]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Known Unknowns]]
- [[Reverse Engineering MOC]]
- [[Current State]]

## Offline executor implementation (2026-08-20)

The argument-free executor is implemented at `scripts/r2o-run-completed-present-calibration.py`, with its fail-closed backend in `reimplementation/ablpc/r2o_completed_present.py`. At this implementation checkpoint no EXP-004 process had launched, attached to, read, or written the game. The later first runtime attempt is recorded separately below.

The implementation enforces the frozen design rather than selecting state after observation:

- it reads only `EIP`, `EAX`, and `EFLAGS` through exact-field `PTRACE_PEEKUSER` operations and reads only the authorized process-memory ranges;
- it permits debugger-state writes only to `DR0`-`DR3`, `DR6`, and `DR7`, with pre-read, exact readback, reserved-bit preservation, and exact restoration readback;
- it keeps `DR0=0x0040FFC0` as the continuous outer-entry guard and rotates only local execution slots with `R/Wn=LENn=0`;
- it journals every ptrace, memory-read, resume, and compositor-capture action as atomic `attempted` -> `completed` -> `validated` records, with failures retained;
- it anchors each stopped triplicate to the all-task-stop time, rechecks task/process/window identity around every capture, and binds PNG-before/decode/PNG-after plus a classified relative path;
- it validates each classified control independently before D2 or aggregate publication, quarantines provisional controls on aggregate rejection, and leaves cleanup/publication ambiguity pending.

`tests/test_r2o_completed_present.py` contains the offline regressions. The targeted suite passed 30 tests, including a non-game 32-bit ELF fixture that independently exercised the host's i386-compat `PTRACE_PEEKUSER` field offsets, hardware execution trap classification, continue path, and exact debug-register restoration. That fixture is tooling evidence only and is not game runtime evidence.

No terrain, collision, material, visibility, camera, player-state, compositor-latch, or causal claim follows from this implementation.

### Second hard-truth implementation correction (2026-08-20)

James rejected commit `0d83c94` because the first executor packet still allowed aggregate ambiguity to become rejected, did not independently cross-bind every control claim, lacked the full guard before every resume, omitted wall-clock hit evidence, published inconsistent capture observations, lacked an accepted aggregate disposition/manifest, and overstated debugger writes on pre-attach rejection. The corrected implementation now:

- retains cleanup, namespace, demotion, or publication uncertainty in the pending aggregate namespace;
- independently checks exact launcher/input/audit/PGID/`R:` identities, all stop TID/slot/EIP/DR6/DR7 facts, ordered phase bytes, result bindings, resume order, and capture representations;
- performs and retains an exact process/window/focus/cache/executable/DAT/CD/`R:` guard before the initial resume, before every later resume, and before detach;
- records monotonic and wall-clock evidence for every execution hit;
- atomically rewrites the final validated capture observation and cross-binds command, observation, journal, decoded RGB, PNG, size, and specific window guard;
- publishes an aggregate only with an accepted disposition, complete manifest, pre-publication validation, atomic rename, and post-publication validation;
- derives debugger-write disposition from actual journal state as `not-attempted`, `attempted-unclear`, or `completed`.

James rejected that `eb28b77` packet because its reconstructed evidence fixture
still used an impossible debugger chronology, pre-title read chronology was not
bound, exceptional runs could retain a null debugger-write disposition,
rollback failure could leave a true accepted disposition, and D1 was not
revalidated after D2 or publication.

### Third hard-truth implementation correction (2026-08-20)

The current candidate correction reconstructs the exact nested journal state
machine: open and initial DR writes, initial resume, every ordered breakpoint,
all-task stop, phase read, exact slot-map rotation, full pre-resume guard,
resume, capture, final restore, and close. It requires completion at DR3,
validates every baseline and debug-write before/desired/readback transition,
and binds each capture anchor to its exact all-task-stop receipt. The Level01
read is now bounded by a retained completion timestamp between the Anthill
selection Return and title Return.

Debugger-write disposition is derived in `finally` for accepted, rejected, and
pending evidence. Aggregate publication starts as `published-unverified`; D1
and D2 are revalidated after D2, immediately before publication, and after the
atomic rename. The final `accepted: true` disposition is the last atomic write.
If rollback itself fails, the accepted namespace retains the primary
`accepted: false` / `published-unverified` disposition plus an ambiguity
receipt.

James rejected that candidate because the journal census was not yet bound to
the guarded game PID/start identity, open/select/close payloads and result
summaries were incompletely rebound, terminal disposition/manifest write
failure could remain terminal, and journal timestamps could run backward.

### Fourth hard-truth implementation correction (2026-08-20)

The current validator requires the guarded PID/start pair in the initial task
census and validates exact `ptrace-open`, measured-TID selection, and
`ptrace-close` lifecycle payloads. It binds `result.selected_tid`, the ordered
completion RGB list, and every prohibited-write null directly to reconstructed
journal/capture evidence. Journal records and execution stops must be
monotonic in both host monotonic and wall-clock time.

If final debugger-disposition or classified-manifest publication fails for an
otherwise accepted or rejected arm, the executor atomically demotes that
terminal directory to `pending` and writes
`r2o-finalization-ambiguity.json`; it cannot remain reusable terminal evidence.

James accepted the validator, result-binding, chronology, and ordinary
finalization corrections but rejected the remaining demotion-failure edge: a
failed terminal-to-pending rename could leave no pending ambiguity receipt.
The executor now creates the pending ambiguity namespace even when that rename
fails, records both errors and journal-derived debugger state, and deliberately
leaves terminal/pending coexistence so aggregate classification must remain
pending.

Before the first runtime attempt, the targeted suite passed 76 tests, including illegal pre-title ordering,
resume-before-stop reordering, wrong completion slot, all debugger-disposition
outcomes, D1 mutation during D2, post-publication mutation, and rollback-rename
failure, guarded-census/open/select/close/result forgeries, backward journal
time, and accepted/rejected disposition/manifest failure. These are offline
tooling tests under renewed James audit. No game
runtime or authorization-gated operation had occurred at that checkpoint.

## First authorized runtime outcome and `-002` amendment (2026-08-20)

The user authorized the exact frozen D1-then-D2 packet. D1 used stage
`D1-auto-hardware-retail-001` and terminated as retained rejection
`evidence/rejected/D1-AH-001`; aggregate
`evidence/comparison/rejected/completed-present-state-calibration-001` is also
consumed. D2 did not launch.

The retained game log proves the complete six-marker Direct3D path and retail
Anthill Level01 load. `Right`, selection Return, title Return, and the sole
pre-title read `uint32[0x00861C84] == 1` completed. About 27 ms after title
keyup, the immediate pre-attach guard rejected because the retained game
window was not focused. No debugger attached; no debug-register write, R2o
state read, stopped capture, DAT write, localizer, or candidate action
occurred. Cleanup and retail `R:` restoration were clear. James accepted this
as a truthful pre-attach rejection, not as evidence against the renderer,
level, R2n state candidates, or completed-present design.

Durable ignored evidence anchors:

- `work/copies/EXP-20260820-004/evidence/rejected/D1-AH-001/disposition.json`, SHA-256 `36eedaf82c522758b4d43131d5f82dbd66032390d89594570aec7cbd46a54edc`;
- `work/copies/EXP-20260820-004/evidence/rejected/D1-AH-001/bugs-final.log`, SHA-256 `74de79ee554dbc7f8fcd3128e4cd273c930de5a0a941e6e32ac165102a7f4d57`;
- `work/copies/EXP-20260820-004/evidence/comparison/rejected/completed-present-state-calibration-001/disposition.json`, SHA-256 `467bb07ba741a3f09cb565225563740efbae66038932759cb6ed046e990d5818`.

The now-consumed retry identities were `D1-auto-hardware-retail-002` /
`D1-AH-002`, `D2-auto-hardware-retail-002` / `D2-AH-002`, and aggregate
`completed-present-state-calibration-002`. The executor performed the
bounded receipt-backed post-title focus-readiness gate specified above before
creating a ptrace session. A focus failure sends no further game input,
performs no attachment/debug write/R2o read, and follows the existing guarded
cleanup and baseline-`R:` restoration path. After James rejected the first amendment for an
after-deadline acceptance edge and incomplete earlier-attempt validation, the
same absolute deadline now caps every window subprocess and is checked after
identity/window work, after every command, and before readiness publication.
The accepted-packet validator reconstructs every attempt's exact permitted
command prefix, PID/start/PGID/XID guard, return codes, common-deadline timing,
non-overlap, status transition, and exact file census. The targeted offline
validator derives focus only from the exact `getwindowfocus` stdout and rejects
an earlier successful attempt followed by another attempt. A subprocess
timeout or other command exception is a terminal pre-attach rejection, not a
retryable attempt, and retains both attempt and summary receipts. The targeted
offline suite passed 90 tests after that correction.

## Second authorized runtime outcome and `-003` amendment (2026-08-20)

The user authorized the exact frozen `-002` D1-then-D2 packet. D1 used stage
`D1-auto-hardware-retail-002` and terminated as retained rejection
`evidence/rejected/D1-AH-002`; aggregate
`evidence/comparison/rejected/completed-present-state-calibration-002` is also
consumed. D2 did not launch.

D1 again passed the complete hardware Direct3D and retail Anthill Level01
load/title/index gates. The fixed readiness interval made 26 attempts against
the same retained XID, PID, start tick, PGID, and `640x480` loading/game window.
Discovery and identity guards used the confirmed nested X display, but all
three focus commands used the unscoped host environment and returned
`BadWindow` before any focus query could complete. This is an executor display-
scope defect, not disappearance of the game window, renderer failure, or an
R2o state result. No ptrace session, debug-register write, R2o process-memory
read, stopped screenshot, DAT write, localizer, or candidate action occurred.
Cleanup and retail `R:` restoration were clear. James accepted the rejection
and this narrow interpretation.

Durable ignored evidence anchors:

- `work/copies/EXP-20260820-004/evidence/rejected/D1-AH-002/disposition.json`, SHA-256 `01cc7e24cc17ed044ef282433284c8c692aa92fb015df4d7165b6e4bf274ce35`;
- `work/copies/EXP-20260820-004/evidence/rejected/D1-AH-002/bugs-final.log`, SHA-256 `2e649a1a6bdb28333eb7b61f92621adcaf5af1a08eda8ac8847ff7420ffebeb7`;
- `work/copies/EXP-20260820-004/evidence/rejected/D1-AH-002/post-title-focus-readiness.json`, SHA-256 `3c46fd8b51f27907771e34870665e46bb29bdf2f2d3d1fed8424bcd08fdb0e7c`;
- `work/copies/EXP-20260820-004/evidence/comparison/rejected/completed-present-state-calibration-002/disposition.json`, SHA-256 `2505c0b7d9974f965d0fe8d6ea37c720804d6ac7aa58b8035f07873925c4c5a6`.

The now-consumed retry identities were `D1-auto-hardware-retail-003` /
`D1-AH-003`, `D2-auto-hardware-retail-003` / `D2-AH-003`, and aggregate
`completed-present-state-calibration-003`. Every readiness and final focus
query now uses the confirmed nested display and is rebound to the retained
runtime-discovery receipt. The accepted-packet validator independently checks
that display provenance on every attempt. Missing or changed provenance
retains a rejection summary and stops before attachment. The targeted offline
suite passed 93 tests at that historical boundary.

## Third authorized runtime outcome and `-004` amendment (2026-08-20)

The user authorized the exact frozen `-003` D1-then-D2 packet. D1 used stage
`D1-auto-hardware-retail-003` and terminated as retained rejection
`evidence/rejected/D1-AH-003`; aggregate
`evidence/comparison/rejected/completed-present-state-calibration-003` is also
consumed. D2 did not launch.

D1 passed the complete hardware Direct3D, retail Anthill Level01 load/title/
index, and nested-display focus gates. The inherited uppercase-aware identity
guard successfully hashed physical `PC/BUGS/CD/LEVEL01/LEVEL.DAT`. The R2o
full pre-attach guard then attempted the nonexistent case-sensitive Linux path
`PC/BUGS/cd/level01/level.dat` and rejected before creating a ptrace session.
This is a host-path casing defect, not a renderer, level, display, or R2o state
result. No debugger-register write, R2o process-memory read, stopped capture,
DAT write, localizer, or candidate action occurred. Cleanup and retail `R:`
restoration were clear. James accepted the rejection and this boundary.

Durable ignored evidence anchors:

- `work/copies/EXP-20260820-004/evidence/rejected/D1-AH-003/disposition.json`, SHA-256 `730d368c9469a81470a233688754e79550b6ba1b0ee13538cb90b0abfb10d9ae`;
- `work/copies/EXP-20260820-004/evidence/rejected/D1-AH-003/bugs-final.log`, SHA-256 `a994bec70758032fc51984108091e8386f705dde3f40defbc6c214d35a7b0d36`;
- `work/copies/EXP-20260820-004/evidence/rejected/D1-AH-003/post-title-focus-readiness.json`, SHA-256 `9ab4a0c16322c97c8fba63826b28a18df05517a46b70aa8df754bd59eb25b99d`;
- `work/copies/EXP-20260820-004/evidence/rejected/D1-AH-003/identity-immediately-before-r2o-attach.json`, SHA-256 `28f79a13d3fb606dfb99aa7d4c0c01f3ce7ba4c66591842d6a5e5b24bf326618`;
- `work/copies/EXP-20260820-004/evidence/comparison/rejected/completed-present-state-calibration-003/disposition.json`, SHA-256 `8c0f544f1033386c22827c83436708b5ecf7d78fc23e5e71b66820abb97458d5`.

The now-consumed retry identities were `D1-auto-hardware-retail-004` /
`D1-AH-004`, `D2-auto-hardware-retail-004` / `D2-AH-004`, and aggregate
`completed-present-state-calibration-004`. Shared constants pin exact
physical `PC/BUGS/CD/LEVEL01/LEVEL.DAT` and `PC/BUGS/CD/CD.TXT` paths for
pre-launch validation, every pre-resume rehash, evidence validation, and test
fixtures. Receipts bind exact relative paths, canonical paths, and hashes.
Missing, lowercase-only, symlinked, nonregular, or changed assets reject before
launch or attachment with zero debugger actions. The targeted offline suite
passed 97 tests at that historical boundary.

## Fourth authorized runtime outcome and `-005` amendment (2026-08-20)

The user authorized the exact frozen `-004` D1-then-D2 packet. D1 used stage
`D1-auto-hardware-retail-004` and terminated as retained rejection
`evidence/rejected/D1-AH-004`; aggregate
`evidence/comparison/rejected/completed-present-state-calibration-004` is also
consumed. D2 did not launch.

D1 passed the complete hardware Direct3D, retail Anthill Level01 load/title/
index, nested-display focus, exact physical asset, process, and pre-attach
guards. Ptrace opened an exact 16-task census and armed only local `DR0 =
0x0040FFC0` on all 16 tasks. The first exact hardware trap occurred on main
TID `1592467` at `EIP = 0x0040FFC0`, `SIGTRAP`, `si_code = 4`, with only
`DR6.B0` set. The immediate all-task-stop census then differed from the
initial census, so the executor rejected before measured-TID selection,
further breakpoint programming, any R2o process-memory read, or any stopped
capture. This evidence establishes only that the two census observations
differed; it does not identify the task-lifecycle cause or weaken the exact
no-churn protocol gate.

The packet contains 32 debugger-register actions: 16 initial `DR0` arms and
16 final restores. Every restore was attempted, read back, and validated;
cleanup left no debugger attachment or owned runtime residue, and baseline
`R:` was restored to retail. No DAT, localizer, candidate, process code/data,
general-register, or unauthorized debugger write occurred. James accepted
this as a truthful procedural rejection, not an R2o scientific sample.

Durable ignored evidence anchors:

- `work/copies/EXP-20260820-004/evidence/rejected/D1-AH-004/disposition.json`, SHA-256 `553bf96d083a06c55c89748587f77502377c904c712432d9eed8f049b8c3f0ff`;
- `work/copies/EXP-20260820-004/evidence/rejected/D1-AH-004/bugs-final.log`, SHA-256 `a238705e3894c53ced8b19a9bd6a74d842f9f4588eb33b91633ec8e23f657d44`;
- `work/copies/EXP-20260820-004/evidence/rejected/D1-AH-004/r2o-pretrace-guard.json`, SHA-256 `10b6b3fd2e38b41a3fbd13c70f83e8c9be7f27752615d88a3e37815493941ace`;
- `work/copies/EXP-20260820-004/evidence/rejected/D1-AH-004/debugger-cleanup.json`, SHA-256 `cc5bfe046ae3d71ca7bc74b92bdca76299efd808da901b931bdb1cccaf990431`;
- `work/copies/EXP-20260820-004/evidence/comparison/rejected/completed-present-state-calibration-004/disposition.json`, SHA-256 `df90a7e18b0b62158f2694b18cb058437837df9b56da0023705bd72c26f26938`.

Fresh frozen identities are `D1-auto-hardware-retail-005` / `D1-AH-005`,
`D2-auto-hardware-retail-005` / `D2-AH-005`, and aggregate
`completed-present-state-calibration-005`. The exact no-churn gate remains:
the runner must neither enroll, ignore, nor remove a task after the initial
atomic census. Every census check now durably journals attempted, completed,
and validated-or-failed state and atomically retains its phase, expected and
observed sorted `(TID,start_ticks)` pairs, additions, removals, reused-TID
start changes, attached/stopped sets, and timestamps before applying a
verdict. The validator independently recomputes every delta, binds each
stop-all receipt to its census file and hash, and permits no selection,
breakpoint rotation, R2o read, capture, or ordinary resume after a mismatch;
only exact cleanup actions may follow. Census enumeration or receipt failure
cannot become reusable rejected evidence and remains pending.

At that pre-run boundary the `-005` amendment was offline and unauthorized.
Its later authorized D1 repeated task-census drift, so R2o retries stopped and
[[EXP-20260820-005 - R2p task lifecycle diagnostic]] became the active pickup.
No terrain, collision, material, face-visibility, causality, no-effect, or
retail-behavior inference follows.

### Fifth hard-truth implementation correction (2026-08-20)

James rejected the first committed `-005` amendment because rejected evidence
authenticated census records but not the complete journal prefix, cleanup did
not bind exact restored debug-register values to baselines and validated write
receipts, and accepted evidence treated census actions as an unordered side
set. Two durable evidence links also used the wrong filename for the retained
pretrace guard.

The correction authenticates the complete journal protocol, hash chain,
sequence, timestamps, action identity, and every lifecycle before terminal
classification. For a census rejection it derives the restore set only from
tasks with a validated non-cleanup debug-register write, binds their first
pre-write values to any completed ptrace-open baseline, requires exactly one
validated final restore to each exact baseline, and cross-binds the cleanup
file to the validated ptrace-close receipt. A pre-write open-census failure
therefore truthfully requires an empty restore set.

For accepted evidence, census actions are part of the exact journal grammar:
one open census, one census between each stop-all attempt and completion, and
one before and after every compositor capture. Stop and capture receipts bind
one-to-one to the exact phase/path/hash/task set; duplicates, swaps, unused
receipts, and unjournaled retained receipts reject. The corrected retained
pretrace path is `r2o-pretrace-guard.json`.

### Sixth hard-truth implementation correction (2026-08-20)

James rejected the preceding validator because lifecycle-shaped arbitrary
actions could still be inserted before a failed census and repeated stop PCs
made a phase-name-only binding insufficient. The corrected rejected-packet
validator now parses the exact frozen R2o grammar from ptrace-open through the
failed census: exact action order and IDs, initial/rotated debug-register
purposes and values, resume order, breakpoint/read sequence, selection,
captures, the physically enclosing owner action, and then only the exact
cleanup tail. A fully formed but out-of-protocol read, capture, debug write,
owner action, selection, or resume cannot classify as reusable rejection.

Accepted stop and capture census bindings now use the actual adjacent journal
records and action IDs, not phase text. This distinguishes repeated
`0x0040FFC0` stop phases and rejects a path/hash swap even when both receipts
carry the same phase label.

### Seventh hard-truth implementation correction (2026-08-20)

James rejected the preceding parser because later census receipts could each
carry a different but internally consistent expected task set, and the failed-
prefix breakpoint checks did not yet bind the complete raw-stop/debug state.
The correction makes the successful open census and completed ptrace-open task
list one immutable sorted `(TID,start_ticks)` identity. Every later census must
repeat that exact expected list and attached-TID set; only the terminal failed
census may differ in `observed_tasks`.

The failed-prefix parser now applies the accepted packet's exact transition
semantics: every debug-write `before` must equal the prior validated state
apart from defined DR6 status bits; desired/readback values must equal the
frozen slot map; every stop binds deadline, completed raw stop, selected TID,
slot, EIP, signal, `si_code`, one supported recorded register layout with a
three-native-word payload, exact DR6 defined status,
raw DR6, and complete active debug-register state. Internally consistent task-
identity changes, wrong stop slot/DR6/active state, and forged intermediate
debug `before` values reject.

### Eighth hard-truth implementation correction (2026-08-20)

James rejected the preceding validator because it hard-coded the synthetic
`i386-compat` stop layout even though the retained `-004` stop records the
supported `x86_64` layout with a 24-byte three-word register payload. The
corrected parser accepts only a layout named in `REGISTER_LAYOUTS`, derives the
payload size as three native words, and requires that one recorded layout to
remain unchanged across every stop in the packet.

The corrected evidence validator also requires the exact sorted, positive,
unique completed ptrace-open `(TID,start_ticks)` list to equal the immutable
successful open census. A forged attachment entry that preserves a TID while
changing its start tick now rejects. This is an offline evidence-integrity
correction only; it changes no protocol, authorization, scientific result, or
claim ceiling. At that correction boundary `-005` runtime was unauthorized; it
was later authorized, consumed, and rejected as recorded in
[[EXP-20260820-005 - R2p task lifecycle diagnostic]].

### Ninth hard-truth implementation correction (2026-08-20)

James rejected the preceding validator because its breakpoint-stop check did
not independently authenticate the raw wait status and its ptrace-open
comparison normalized a reordered task receipt. The corrected parser requires
`ptrace_event = 0`, a raw status for which `WIFSTOPPED` is true, and
`WSTOPSIG(wait_status) = SIGTRAP`, in addition to the already bound recorded
signal, `si_code`, EIP, slot, and DR6 state. Ptrace-event stops and internally
inconsistent stopped-signal receipts therefore reject.

The completed ptrace-open task list is now compared in its recorded order to
the immutable sorted open census; the validator no longer sorts the receipt
before comparison. Reordering otherwise correct `(TID,start_ticks)` entries
therefore rejects. This correction changes no runtime protocol,
authorization, evidence interpretation, or claim ceiling, and `-005` remains
uncreated and unauthorized.
