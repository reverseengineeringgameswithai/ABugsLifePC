---
type: session
date: 2026-08-19
agent: Codex
topic: R2c F0 identity stabilization
tags:
  - session
  - re/runtime
  - re/level-format
---

# 2026-08-19 1618 - Codex - R2c F0 identity stabilization

## Preserved rejection

`F0-AH-008` rejected immediately after process discovery. It had not entered
the renderer gate and produced no input, signal, process-memory read, capture,
DAT edit, or runtime/debugger write. Launch-group and residual-device cleanup
reached a clear audit, and baseline `R:` was restored to retail.

The packet remains under `evidence/pending/F0-AH-008`. The old discovery path
did not persist each candidate or the compared field values, so the later
generic identity-mismatch message cannot identify whether command, cwd, PID,
start ticks, or process group changed. The old final-log collector also treated
the expected pre-renderer absence of `bugs.log` as a cleanup failure. The result
is therefore an unclassified pre-action tooling rejection, not evidence about
the renderer, Anthill navigation, freeze, or game behavior.

## Frozen correction

Fresh stage `F0-auto-hardware-retail-009` and packet `F0-AH-009` are pinned.
Runtime discovery now retains every candidate and confirming observation with
exact PID, start ticks, process group, command, cwd, timestamp, and field diff.
Command/cwd startup mutation may settle only under the same immutable identity;
assignment requires two consecutive identical exact-final observations.
Replacement, disappearance, ambiguity, or persistent instability fails before
any input. Missing `bugs.log` is explicitly receipted as accounted only before
the renderer/log gate and remains a cleanup failure after that boundary.

James's first audit found two remaining binding gaps. The corrected executor
now retains the previously observed PID's raw current identity before filtering,
so PGID or executable-shape drift carries the actual value and field diff. It
also checks post-snapshot and post-receipt timestamps against the absolute
pre-Return deadline before assigning the game. A synthetic second confirmation
that advances beyond the deadline rejects without reaching the renderer or any
input. The active frozen-path error now names `F0-AH-009`.

Sixty-three focused lifecycle regressions pass, including same-process startup
mutation, immutable replacement with exact diff, persistent instability with
no later action, raw PGID drift, post-snapshot deadline crossing, and both
log-absence classifications. The accepted scheduler, pidfd, authorized-read,
title, structural-region, and derived-frame gates are unchanged. No localizer
DAT has been created.

## F0-AH-009 runtime result

After James accepted the pre-launch packet at commit `c06de2d`, the immediate
pre-launch audit was clean and the argument-free executor returned
`accepted-f0`. It used exact retail Level01 DAT `786b7a...8b53`, exact executed
build `1e1d5099...c41f`, all six Direct3D markers, Level01 index `1`, and only
the three authorized read ranges. PID `937066` stopped through pidfd at
`t0+3.300000000 s` with `0.832 us` error; all 17 tasks were stopped.

All three `640x480` captures are PNG `05f5691c...506ad1c` / decoded RGB
`2ea65643...23b9d26c`, with identical structural regions and view-block hashes.
Visual review confirms a non-faded Anthill Level01 gameplay frame. SIGCONT
resumed the exact process. Normal close required the retained group TERM/KILL
and residual-device cleanup path; the final and independent post-run audits are
clean and `R:` is retail. Disposition records no runtime/debugger/DAT write.

This is the passed derived-build control calibration, not a localizer or causal
result. James accepted the committed F0 result.

## Post-F0 localizer tooling packet

At that offline-freeze checkpoint, no localizer DAT had been created and no arm
had launched. The offline successor
adds an argument-free creator pinned to `primary[81]`, object `0x4860`, geometry
`0x188cc`, face 8, exact tuple `(300,312,264,324) -> (300,300,300,300)`, the
three physical byte changes, and derived SHA `9942e2...11bfd`. It atomically
publishes DAT plus full diff/reparse receipt only at fresh ignored
`localizer-face8-001/`.

A dedicated argument-free executor pins fresh C1/L/C2 stages and accepted
namespaces, reuses the accepted F0 runtime lifecycle, requires exact accepted
view/structural hashes, and requires controls to reproduce derived PNG/RGB
`05f569...ad1c` / `2ea656...d26c`. The argument-free comparator rejects the
retail R2b phase hash and arbitrary paths, validates arm provenance, and writes
only `evidence/comparison/face8-localizer-001`. Ninety-eight focused tests pass,
including post-publication DAT failures and negative provenance cases for the
renderer window/XID, input, level-index bytes, read-only view bytes, signal
identity and resumed state, cleanup disposition, and frame-region receipts.
This packet must be committed and James-accepted before its creator is run.

## Links

- [[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Decision Log#DEC-20260819-159 - Stabilize and receipt the R2c runtime identity]]
- [[2026-08-19 1530 - Codex - R2c auto-hardware F0 pivot]]

## Completed face-8 localizer block

After James accepted the offline tooling and exact three-byte creation receipt,
the frozen runner completed C1-AH-001, L-AH-001, and C2-AH-001 with clear
per-arm audits. The comparator retained 18,612 changed pixels in 353 components
and rejected both localization concentration gates. Visual review found
distributed actor/vegetation/scene-state differences rather than one surface
hole. James accepted the run as procedurally valid and the interpretation as
causally inconclusive. No one-byte candidate was created or launched. The next
runtime proposal requires a committed and James-accepted control-only protocol,
then fresh authorization for two independent exact-build/retail-DAT controls
over a grid spanning an established animation cycle. Only those controls may
define the nuisance mask. After that mask is committed and James-accepted, a
second fresh authorization is required before `C/L/L/C`.
