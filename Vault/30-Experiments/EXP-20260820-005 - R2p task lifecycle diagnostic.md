---
type: experiment
id: EXP-20260820-005
title: R2p task lifecycle diagnostic
date: 2026-08-20
environment: Offline analysis of retained R2o and P0B evidence after accepted operator cleanup; no live session or runtime authority
binary_sha256: 1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f
question: What exact task-lifecycle fact explains the repeated first-breakpoint R2o census change, and what passive measurement can discriminate it without weakening no-churn coherence?
status: paused
created: 2026-08-20
updated: 2026-10-02
result: diagnostic-valid-task-addition-identity-unresolved
evidence:
  - EXP-20260820-004
  - work/copies/EXP-20260820-005/evidence/offline/task-lifecycle-002/analysis.json
  - work/copies/EXP-20260820-005/evidence/pending/P0A-AH-001
  - reimplementation/ablpc/r2p_passive.py
  - scripts/r2p-run-passive-lifecycle.py
  - work/copies/EXP-20260820-005/evidence/offline/task-attribution-001/analysis.json
  - work/copies/EXP-20260820-005/evidence/offline/task-attribution-002/analysis.json
  - work/copies/EXP-20260820-005/evidence/offline/task-attribution-003/analysis.json
  - reimplementation/ablpc/r2p_p0c_attribution.py
  - scripts/r2p-analyze-p0c-task-attribution.py
  - work/copies/EXP-20260820-005/evidence/offline/quiet-census-design-001/design.json
  - work/copies/EXP-20260820-005/evidence/offline/quiet-census-design-002/design.json
  - work/copies/EXP-20260820-005/evidence/offline/quiet-census-design-004/design.json
  - reimplementation/ablpc/r2q_quiet_census_design.py
  - scripts/r2q-freeze-quiet-census-design.py
tags:
  - re/runtime
  - re/static
  - level01
  - terrain
  - diagnostic
---

# EXP-20260820-005 - R2p task lifecycle diagnostic

> Paused 2026-10-02: no further R2p arm is planned. The user dropped the R2q
> successor track on 2026-09-27 as too slow. The stage, pending evidence and
> the baseline prefix's `R:` mapping stay retained; restoring `R:` needs the
> parsed clean zero-process audit below, and any later baseline arm re-links
> `R:` in its own preflight.

## Question

What exact task-lifecycle fact explains why two independent R2o D1 controls
reached the first `0x0040FFC0` hardware trap and then failed the immutable task
census? This packet first authenticates the consumed evidence offline, then
freezes a future passive P0 discriminator. It does not retry R2o.

## Accepted runtime boundary inherited from EXP-004

The authorized `-005` D1 passed hardware Direct3D, Anthill Level01, focus,
process, asset, and exact initial 16-task attachment gates. At the first exact
`0x0040FFC0` trap, the immediate stop-all census gained TID `1648646`, start
ticks `28065259`, with no removal or reused-TID change. It rejected before TID
selection, R2o memory reads, stopped captures, or later scientific action. All
32 permitted debug-register actions completed and restored the 16 attached
tasks; cleanup and retail `R:` restoration were clear. D2 was never created.
James accepted this procedural rejection. Under the frozen rule, R2o retries
now stop.

Durable anchors:

- `-004` D1 disposition `553bf96d083a06c55c89748587f77502377c904c712432d9eed8f049b8c3f0ff`;
- `-004` pretrace guard `10b6b3fd2e38b41a3fbd13c70f83e8c9be7f27752615d88a3e37815493941ace`;
- `-004` cleanup `cc5bfe046ae3d71ca7bc74b92bdca76299efd808da901b931bdb1cccaf990431`;
- `-004` classified manifest `335fb4982548291b6f7a6c3579f3c137e1c7a9f47dc58fe7fc4236e773defa53`;
- `-005` D1 disposition `3f1fb007138dda38b33990f9b8344ff8a71d518a5d8ef495b64d1eb49af24639`;
- `-005` initial census `d91cad25e7c1fc23a44afff7edd718aa707fee76b1d82dd2d38a643eb7e43e7a`;
- `-005` changed census `909cc5f1d97fac909da2f7914a1517492c93e002050ec994e4d3b9121e62ecf0`;
- `-005` cleanup `31e1ba0cf3dc8ae09e013960d7c88eaf65bce212703adb4e50d7eb6eb7b726ca`;
- `-005` classified manifest `801a8e1d3982ba93faa25ae229681b6b81f38f44424cc24efa141ea26c136177`;
- rejected aggregate `df90a7e18b0b62158f2694b18cb058437837df9b56da0023705bd72c26f26938`.

## Offline analyzer result

The argument-free command is:

```bash
scripts/r2p-analyze-task-lifecycle.py
```

It authenticates every file in both classified manifests, rejects any missing,
extra, changed, escaping, or symbolic-link entry, and then applies the accepted
R2o census/action grammar to the full packet. Only after that closure does it
check the exact first trap, permitted debug-register lifecycle, cleanup,
static PE sources, and the `-005` task delta. Result:

- outcome `diagnostic-valid-task-addition-identity-unresolved`;
- analysis SHA-256 `8d35c6b68a21d881ad98981db6842b8d050a17d7900c29fec4ea319378f70e43`;
- analyzer module SHA-256 `89d77ff400dd31c3892d89f4f0e0b02055112ddb84bd25982e871492cfa69dc9`;
- argument-free wrapper SHA-256 `b011bfcc788b081e46bed6e3cde8dffa2b8f3d20f0adfea96b65daa8b7856aa9`;
- initial-census completion `280652411738878` monotonic ns;
- changed-census start `280652592461321` monotonic ns;
- bounded observation gap `180722443` ns;
- one addition `(1648646,28065259)`, no removal, no reused TID.

The run did not record host `_SC_CLK_TCK`; converting `start_ticks` into
monotonic time is prohibited. Existing evidence does not identify task name,
creator TID, role, module, lifetime, or whether debugger activity caused it.

The earlier analysis SHA-256
`b407bcf2c6f7408350a53ebeb831ca811a47553eae340688596025dc440a22d5`
is preserved unchanged at
`work/copies/EXP-20260820-005/evidence/offline/obsolete/task-lifecycle-001-b407bcf2/analysis.json`.
It is obsolete because it did not authenticate full manifest closure or reuse
the accepted R2o grammar. It must not be cited as the active result. The
corrected output is written to a fresh path by temp-file write, file and
directory `fsync`, byte re-read, atomic rename, and final byte re-read.

## PC-static boundary

`static/exports/BIN-97c95ba5572dce63/R2P-task-lifecycle-static-thread-creation.md`
records the one direct PC
`CreateThread` call through IAT `0x008645F8`: call `0x0042CF04`, physical
offset `0x0002C304`, start thunk `0x00401889`, target `0x00440F50`. The call
and thunk bytes are identical in retail and auto-hardware builds. This does
not bind the added Linux task to that PC path. The empty-import Ghidra export
cannot resolve the imported call, and a Wine-created task remains possible.

## Frozen P0A passive collector

The argument-free runtime wrapper was implemented at
`scripts/r2p-run-passive-lifecycle.py`. At the historical offline boundary in
this section it was unrun, explicitly authorized, and blocked until corrected
James acceptance; the consumed pending runtime is recorded below. Frozen
source identities at that offline boundary were:

- collector/validator SHA-256 `7d2305338c5b571963917e11f13000364e94b36ba368fd428d9d1dc542a399e6`;
- lifecycle analyzer SHA-256 `c7441293a2b2504abf2bae7c934d0dc2eb83cce63af6abde20671cf5f3b9fe78`;
- wrapper SHA-256 `5ea5fcab93c36fb317a386156a5f1d176b326a613b443ceada1bb32370599f6f`;
- launcher SHA-256 `0965241132af6e15e9b19db9e8dc0b821ec85ff1f14f292e86037618c75f6051`;
- focused test SHA-256s: passive `3be19489eec06d4f00f13e2563755afc50e986f7fc3c19fbe602f6a2e8d2c2c3`,
  packet integrity `3c84f37a3ed0f6d85e7e39e47e002d4cf188483ca40f16114cf28374524e37d1`,
  native X11 `9be0e42892399b7e5dc2682cdc2bee16504ae9a29f86e224da34a1791eb849d5`,
  lifecycle `987e5cadb9cc9e9e807a17329662ffb9d1663356ef9ea790363ad043df1acb90`,
  and native fixture `fc7799031ecce767c279eb73a7833dc607b7a7877b43ef0aa51ab28840665284`;
- 207 focused analyzer/packet tests plus the separate native X fixture passed
  (208 total); at that historical boundary no production stage, pending,
  published-unverified, accepted, or rejected evidence identity existed.

The executor is independent from the R2o/F0 control runners. It has no
level-index or other process-memory read, ptrace/debug-register path, signal
cleanup, screenshot, DAT editor, localizer, candidate, or R2o action. Two
persistent X11/XTEST connections split the sampler and title-input workers.
They bind one retained XID and never refocus or replace it. A failed normal
`Alt+F4` close remains pending with `R:` unrestored if the process is live;
no `SIGTERM`/`SIGKILL` fallback is permitted.

The first executor audit correction requires an exact owned process-group and
session census plus a parsed zero-process/zero-sink/zero-session audit before
restoring `R:`, then a second parsed clean audit after restoration. Discovery
failure, unreadable live process identity, residual Wine task, or either audit
failure retains the stage mapping and pending evidence. The validator requires
the exact acquisition receipt inventory and exact source/timing/prohibited-
action maps. It recomputes enumeration stability and sole-window identity from
raw lists, cross-binds all first-seen task metadata to the guarded executable,
and limits title-Return keydown to requested `+0.010 s` on the retained input
connection. Executor-authored summary booleans are not verdict evidence.

Current P0A identities after the consumed P0A-AH-001 attempt:

- stage `work/copies/EXP-20260820-005/P0A-auto-hardware-retail-001` is
  **present** and intentionally retained;
- pending evidence `work/copies/EXP-20260820-005/evidence/pending/P0A-AH-001`
  is **present**;
- nonterminal publication staging
  `work/copies/EXP-20260820-005/evidence/published-unverified/P0A-AH-001` is
  absent;
- terminal evidence `evidence/accepted/P0A-AH-001` or
  `evidence/rejected/P0A-AH-001` is absent.

P0A is a fresh auto-hardware process with retail executable/assets and the
same guarded `Right`, `Return`, `Return` navigation mechanism. It must retain
the exact retail/derived hashes, full-disc `R:`, six hardware markers,
Level01 load and ClearLoadScreen log identities, exact PID/start/PGID/cwd,
current `640x480` `Bugs` window, focus, input receipts, normal close, and
pre/post `make session-audit` receipts.

No debugger attachment, hardware/software breakpoint, signal, process-memory
read, screenshot, DAT write, localizer, candidate, or R2o state read is
permitted. The collector starts before title Return:

1. At `t_collect`, retain sample 0 and host `_SC_CLK_TCK`.
2. Schedule title-Return keydown at exactly `t_collect + 0.100 s`, use the
   frozen requested `0.180 s` host sleep, and keyup in `finally`.
3. Sample `/proc/<pid>/task` on the exact 521-point fixed grid
   `t_collect + n * 0.020 s`, `n = 0..520`, ending at `+10.400 s`.
4. Before every sample, require the same PID/start/PGID/cmdline/cwd/executable,
   stage assets, `R:` target, window, and focus without refocusing.
5. Require both task enumerations to contain the guarded process leader. A
   structurally stable sample must contain exactly
   `(pid,process.start_ticks)` for that leader, and no sampled task may predate
   the process start. A missing parsed leader is admissible only with that
   sample's exact leader identity-read error and therefore becomes unresolved
   enumeration drift.
6. Retain requested, started, and completed monotonic ns, sorted
   `(TID,start_ticks)`, and for
   every newly observed TID immediately retain `comm`, full `status`, task
   `exe` target plus device/inode/hash identity. Record metadata disappearance
   rather than filling it from a later sample.
7. Each sample must start no later than requested `+0.002 s`, complete no
   later than requested `+0.010 s`, and complete before the next request. The
   request grid and sequence are exact; a missing, duplicate, backward,
   overlapping, late, or extra sample rejects. Missing added-task metadata,
   task-enumeration error, identity drift, renderer/level/window/focus drift,
   or unclear cleanup rejects or remains inconclusive as defined below.

Each sample brackets task reads with two `/proc/<pid>/task` enumerations. A
difference is retained as `task-enumeration-drift-unresolved`; it is never
described as an atomic census. Stable samples record every sorted
`(TID,start_ticks)` and immediately bind every first-seen identity to `comm`,
full `status`, task `exe` target/device/inode/hash. Full source/asset hashes
are pre/post gates, while each timed sample uses persistent descriptors and
direct identity fingerprints rather than subprocesses or repeated full-file
hashing.

P0A records `/proc` observations only. Creator-TID attribution requires a
separate later authorization for a filtered kernel lifecycle source such as
`sched_process_fork`/`sched_process_exit`, with kernel/BTF/tool hashes and
lost-event counts. Polling alone cannot prove creator identity.

## Fail-closed outcomes

| Observation | Result |
|---|---|
| Exact new task with complete metadata | `diagnostic-valid-task-added` |
| Existing task disappears | `diagnostic-valid-task-removed` |
| Identity first appears after sample 0 and later disappears without reappearing or participating in reuse | `diagnostic-valid-short-lived` |
| Same TID, changed start ticks, including across an observed absence | `diagnostic-valid-reused-tid` |
| Same `(TID,start_ticks)` appears on both sides of an absence | `task-identity-reappearance-unresolved` with exact absence intervals |
| More than one of the exact lifecycle classes occurs | `diagnostic-valid-mixed-lifecycle` with the ordered class list |
| Initial task loses first-seen metadata before read | `task-identity-unresolved` with that identity only in `initial_identities` |
| Added task loses first-seen metadata before read | `task-identity-unresolved` with that identity only in `added_identities` |
| Polling gap or later lost kernel event | inconclusive |
| Process/asset/renderer/level/window/focus drift | rejected |
| Cleanup or `R:` restoration uncertain | pending |
| No observed change | `finite-no-change-observed`, never proof of stability |

Any result must be documented, committed, and James-accepted before another
arm. A second independent passive process is required before claiming a
reproducible lifecycle class. P1 attach-only is considered only if passive
evidence does not explain the lifecycle; P2 DR0 diagnostics are considered
only after P1. Each stage requires a separate frozen packet and fresh explicit
authorization.

The executor and validator must be James-accepted before requesting P0A
runtime authorization. This implementation commit authorizes nothing.

## Decision boundary

R2o may be redesigned only after at least two independent fresh processes
reproduce one lifecycle class and establish a deterministic way to complete
it before measurement, followed by a fixed no-churn interval longer than the
full R2o acquisition. Dynamic enrollment, ignoring, detaching, or normalizing
new tasks remains forbidden. Terminate this route if creation is intermittent,
recurs during measurement, cannot be attributed without perturbative
instrumentation, or would require weakening no-churn.

No terrain, collision, material, face-visibility, causality, no-effect,
compositor-latch, or retail-behavior claim follows.

## 2026-08-20 P0A evidence-integrity hardening

The unrun P0A executor now treats launch through restoration as one authenticated
prefix. Both scientific and procedurally rejected publication require exact
`game-session` `1.0.0` audit receipts with monotonic times and `R:` targets,
an independent pre-navigation runtime PID/start/PGID/cmdline/cwd/host-image
receipt, full retained log-gate text, exact raw window and X-connection binding,
the fixed one-second carousel settle, input chronology, owned-runtime clearance,
and an exact stage-to-retail `R:` restoration receipt. An incomplete prefix
remains pending rather than becoming rejected evidence.

Procedural rejection also has a dedicated collection grammar: it authenticates
the exact retained zero-to-521 sample prefix, task metadata, window/assets,
clock, request grid, process image and title-input state machine; permits only
enumerated acquisition/title/timing runtime failures; and requires the derived
failure text to equal `disposition.error`. Malformed evidence cannot be made
publishable merely by adding an error string. Audit receipts require
`parse_error: null` as well as a valid parsed payload.

The rejected grammar applies the same `+10 ms` title-start and `180 ms` hold
contract to a successful title receipt and makes success mutually exclusive
with a worker error. Metadata errors are sample-local: identity-read errors must
match that sample's enumeration gap, and a newly seen `(tid,start_ticks)` must
have exactly one first-seen outcome at that sequence, either one bound metadata
record or one failure, never both or neither.

Each retained sample also reconstructs the collector's exact
enumeration-to-identity-read partition: parsed task TIDs and identity-error TIDs
must be duplicate-free, disjoint, and their union must equal
`enumeration_before`. An unexplained missing TID or a parsed TID absent from that
enumeration is malformed evidence, not task-enumeration drift.

The real X11/XTEST boundary is covered by an isolated non-game Gamescope/Xwayland
fixture. It opens two actual persistent connections, observes raw window
properties and focus, performs the direct guard/enumeration, and delivers an
XTEST press/release. This fixture is tooling evidence only and is not game
runtime evidence. At that historical hardening boundary P0A was unrun and
unauthorized; the later explicit authorization and still-blocking James gate
are recorded below.

## 2026-08-20 first James rejection and correction

James independently audited exact commit
`52d9a0f6db4d98ffa9676d956d406254cb82c281` (tree
`8b271be807f596ac7122636dd4ff53731cf18c26`) and returned **REJECT** before
runtime. The nine reproduced defects were: terminal publication before final
validation; missing timing bounds on rejected sample prefixes; an overbroad
nested title-error allowlist; no post-metadata task-identity read; descriptor-
only asset guards; synthetic rather than kernel-backed X-connection identities;
generic/under-specified lifecycle outcomes; stale source/test pins; and a
double-read final log receipt.

The correction keeps publication under a fixed `published-unverified` identity
until post-move validation, manifest closure, and file/directory `fsync` all
complete; only the final rename creates `accepted` or `rejected`. A reproduced
`KeyboardInterrupt` after the first rename leaves only the nonterminal identity.
Every rejected-prefix sample now preserves the same exact request grid and
structural grammar as a full collection. An observed `+2 ms` start, `+10 ms`
completion, overlap, or monotonic-order miss is admitted only as the exact
derived procedural-rejection reason; an earlier miss and a later partial
acquisition failure are both retained rather than masking either one.
Title failures use one exact typed layer and only enumerated window/XTEST
classes. First-seen metadata is bracketed by exact equal pre/post
`(TID,start_ticks)` reads. Each asset guard binds the live path's regular-file
identity and exact path/hash to the retained open descriptor. The two X11
connections retain distinct `XConnectionNumber` socket descriptor receipts and
bind their display to one exact owned Xwayland PID/start/PGID/cmdline identity.
All stable, single-class, and mixed lifecycle results have exact outcome
strings. The final log is read once and its retained bytes are hashed.

The adversarial focused suite at that boundary was 150/150, including the real isolated
Gamescope/Xwayland fixture. The user explicitly authorized the bounded P0A
runtime after the original offline packet, but the frozen ordering gate still
blocked launch at that boundary. James later rejected this candidate as
recorded below. No game launched, no production identity was created, and no
process-memory read/write, ptrace, signal, screenshot, DAT/localizer/candidate,
R2o, terrain, collision, material, visibility, or causal action occurred during
the correction.

## 2026-08-20 second James rejection and correction

James re-audited exact commit
`b24890bfe0e265fb1e00ebbf18cf9eb0bb2b23fa` (tree
`8ce1cfc3ae9e09a90cabe948e5db7d9bc69be1f8`) and returned **REJECT** before
runtime. The prior nine defects were closed and both his focused 150/150 suite
and full 1794/1794 repository gate passed. Five remaining counterexamples still
blocked launch: an authentic timing miss could not pass the rejected validator;
manifest creation left a post-semantic-validation mutation window; unresolved
metadata duplicated one identity and mislabeled baseline failures as additions;
a 64-character non-hex executable digest passed a partial rejection; and socket
shape/display text did not prove either X connection's peer was the recorded
Xwayland process.

The second correction separates exact collection structure from the timing
verdict. Scientific packets still require the full timing contract; rejected
packets can authenticate the exact derived timing failure, including a timing
miss earlier than a later partial-acquisition error. Publication now writes the
post-validation receipt and manifest, semantically revalidates those exact
current bytes, reauthenticates the manifest, fsyncs the complete packet, and
after terminal rename fsyncs both the removed nonterminal directory entry and
the created terminal entry. Unresolved identities are deterministically
deduplicated under neutral `task-identity-unresolved`, with separate
`initial_identities` and `added_identities` lists. Every admitted executable
SHA-256 is lowercase hexadecimal. Both actual Xlib sockets retain Linux
`SO_PEERCRED` PID/UID/GID plus `/proc/<peer>/stat` start ticks, and both
PID/start pairs must equal the frozen owned Xwayland identity.

The focused suite at that boundary was 158/158, including full-grid and partial timing
rejections, mutation-during-manifest, both-parent fsync, neutral unresolved
categories, non-hex rejection, and the real isolated Gamescope/Xwayland
`SO_PEERCRED` fixture. The authorized live arm remains unconsumed pending James
acceptance of the next immutable commit. No game or production identity was
created and no process-memory read/write occurred.

## 2026-08-20 third James rejection and correction

James audited exact commit
`c05f1677fb4a5ebd1ac4f968621b5da0056d1833` (tree
`d60d88bba65eb3c57f90ff5d310fce27b4a34e40`) and returned **REJECT** before
runtime. He confirmed all five preceding corrections, matching source pins,
158/158 focused tests, absent production identities, and clean git/session
state. One root lifecycle-partition defect remained. Adjacent deltas followed
by set intersection mislabeled a baseline identity that disappeared for one
sample and returned as short-lived, missed changed start ticks when the same
TID returned after a gap, and made the two analyzers disagree about the
first-seen category for missing metadata on that later identity.

The third correction derives a compact ordered history for every TID and
`start_ticks` identity across all 521 samples. Reuse comparison carries the
last observed start ticks across absence. Metadata categories use the identity's
global first-seen sequence in both analyzers. `short-lived` requires first
observation after sample 0, later disappearance, no reappearance, and no role
as either endpoint of a reuse transition. The same identity appearing on both
sides of any absence now fails closed as
`task-identity-reappearance-unresolved`, retaining the exact absent and
reappearance sequence boundaries. Six paired regressions exercise all three
histories through both analyzers; the focused suite is 164/164.

The authorized live arm remains unconsumed and blocked on James acceptance of
the next immutable commit. No game or production identity was created and no
process-memory read/write occurred.

## 2026-08-20 fourth James rejection and correction

James audited exact commit
`96e2fdf58fb263720250cc922057abf4b39a0215` (tree
`60ab6a3d62761a73630116e16cc986d83dd20b41`) and returned **REJECT** before
runtime. He confirmed the complete-history correction, 164/164 focused tests,
1808/1808 full tests, exact source pins, absent production identities, and
clean repository/session state. The remaining root defect was an impossible
fixture and missing process-leader anchor: both analyzers admitted a guarded
process `(pid=10,start_ticks=20)` while accepting leader task `(10,1)`, only
unrelated workers, an empty task set, or a reused leader identity.

The fourth correction anchors every task census to the frozen process
identity. Both enumerations must contain the guarded PID; every stable sample
must parse the exact leader `(pid,process.start_ticks)`; and every task's start
ticks must be at least the process start. Only an exact sample-local identity
read error for the enumerated leader can omit its parsed identity, and that
sample is unresolved enumeration drift. The lifecycle fixtures now keep a
permanent `(10,20)` leader and place addition, removal, reuse, short-life,
metadata, gap, and reappearance cases on worker TIDs. Paired direct,
scientific, and rejected-prefix regressions cover wrong leader ticks, an absent
leader, an empty census, a worker predating the process, and impossible leader
reuse. The focused suite is 184/184 and the full repository gate is 1829/1829.

The authorized live arm remains unconsumed and blocked on James acceptance of
the next immutable commit. No game or production identity was created and no
process-memory read/write occurred.

## 2026-08-20 fifth James rejection and correction

James audited exact commit
`b8e8d447d356c40168af98d70bd768edf8920c00` (tree
`5c48cbb48ea7d0e60518d7600ede854ca1c06d6f`) and returned **REJECT** before
runtime. He confirmed the leader anchor, all prior corrections, matching pins,
184/184 focused analyzer/packet tests plus the native X fixture, absent
production identities, and clean repository/session state. One narrow
exception-path defect remained: direct analysis accepted missing, extra,
non-string, empty, or untyped leader identity-error receipts as authority to
omit the mandatory leader. The packet-prefix path rejected field/type
forgeries but still accepted an empty string in both scientific and rejected
terminal validation.

The fifth correction routes every metadata-error receipt through one shared
validator before leader omission or any early enumeration-drift return. Each
phase has one exact field set, positive integer identity fields, a nonempty
single-line typed error string bounded to 4096 characters, a closed exception
type set, and a closed message-prefix set for internal `P0AError` values.
Direct, scientific, and rejected regressions cover missing/extra fields,
non-string, empty, untyped, disallowed, and multiline errors. The positive
sample-local `FileNotFoundError: fixture` case still returns unresolved
enumeration drift. The focused analyzer/packet suite is 201/201 and the native
X fixture passes separately (202 total); the full repository gate is
1846/1846.

The authorized live arm remains unconsumed and blocked on James acceptance of
the next immutable commit. No game or production identity was created and no
process-memory read/write occurred.

## 2026-08-20 sixth James rejection and correction

James audited exact commit
`a68076f3197f7c16318dc9c102e7350f4ad0e3e0` (tree
`10bdcad9b1ff60470b33b182908e4a6852520cfa`) and returned **REJECT** before
runtime. He confirmed every preceding malformed-record case was closed,
201/201 analyzer/packet tests plus the native X fixture, matching pins, absent
production identities, and clean state. One exact-provenance defect remained:
the shared validator used a union of internal `P0AError` messages for both
phases. An `identity` receipt could therefore claim `task identity changed
during first-seen metadata capture`, although that message can only arise after
the initial identity read succeeds in `new-identity-metadata`. Direct,
scientific, and rejected validation all admitted the forged phase/message pair.

The sixth correction uses exact phase-specific internal-error sets. `identity`
admits only the five fixed `/proc/stat` parser messages. The metadata phase
admits those same post-read parser messages plus the one exact identity-change
message. Direct, scientific, and rejected regressions reject the metadata-only
message in `identity` and accept it in `new-identity-metadata`. The focused
analyzer/packet suite is 207/207 and the native X fixture passes separately
(208 total); the full repository gate is 1852/1852.

The authorized live arm remains unconsumed and blocked on James acceptance of
the next immutable commit. No game or production identity was created and no
process-memory read/write occurred.

## 2026-08-21 P0A-AH-001 pending pre-collection runtime

James returned **ACCEPT** on exact pre-run commit
`8437c0a4b5630ba59bcb7601a67066074e02da06` (tree
`532419060f1b5d5e4c4e7ed65e78bc2f7bf3acd9`) after independently passing
207/207 analyzer/packet tests, the native X fixture, and 1852/1852 full tests.
The clean pre-launch audit had zero processes, sinks, or open sessions. The
single exact authorized invocation of `scripts/r2p-run-passive-lifecycle.py`
then launched one fresh auto-hardware process. This consumed P0A-AH-001.

The hardware and Level Select gates passed, and both frozen input receipts
record successful focused key delivery: `Right`, one-second settle, then
`Return`. The retained final log nevertheless loads
`R:\PC\BUGS\cd\level07\level1.dat` and
`R:\PC\BUGS\cd\level07\terr1.all`, then reaches `ROUTINE : Start
ClearLoadScreen.` The preregistered Level01 gate timed out before collection,
so `collection.json` does not exist and **zero P0A task-lifecycle samples are
evidence**. This falsifies the frozen assumption that one requested 180 ms
`Right` hold is equivalent to one accepted carousel step. It does not establish
the exact number or timing of accepted steps.

The guarded normal-close receipt records successful `Alt_L+F4` keydown/keyup
on the retained focused `640x480` loading window, but the process survived all
89 bounded clearance polls. The executor correctly prohibited signal cleanup,
retained stage and evidence as pending, did not restore `R:`, and created no
published-unverified, accepted, or rejected identity. The post-close audit is
not parsed evidence: its raw field contains the process/sink census, but
`parsed` is null with `JSONDecodeError: Extra data: line 142 column 1` because
Make's error line was concatenated after the JSON. A fresh read-only
post-wrapper audit independently recorded seven Gamescope/Wine processes plus
private sink `ablpc_mute_1834769` as live and unattributed at that boundary.
They were recorded and not terminated. Any successor must retain session-audit
stdout separately from Make's stderr before claiming a parsed audit receipt.

The live run also falsified the frozen real-X provenance premise. Runtime
identity records Xwayland `(PID 1834812,start_ticks 30382270)`, while both the
sampler and input Xlib socket `SO_PEERCRED` receipts identify peer
`(PID 1834786,start_ticks 30382246)`, which the live audit identifies as
Gamescope. The terminal validator requires both peers to equal the frozen
Xwayland identity, so the packet would have failed this gate even if collection
and cleanup had completed. The isolated native X fixture did not reproduce
real Gamescope socket provenance; any successor must resolve and re-freeze
this binding before authorization.

The pending disposition (SHA-256
`ca2dfaa324f00f8be88289729ad46ad30036ddf40bdd43fa4f18abfc3eb70d80`)
records `P0AError: level01: log gate timed out`, cleanup error `normal close:
P0AError: normal close failed; signal cleanup is prohibited`, baseline
`R:` restoration false, and null process-memory read/write, debugger, signal,
screenshot, DAT, localizer, candidate, and R2o fields. Supporting exact hashes
are runtime identity `c0ad5df6...1eb0c4`, carousel input
`c7fd7f18...4c27cd`, selection input `9dbcb3fb...db19`, normal-close receipt
`e3eeffa4...4e418`, clearance receipt `e3ec4aa2...15fb4`, post-close audit
receipt `e2f801e3...b0226`. `86e7a028...6ea32` is the SHA-256 of the
`bugs-final-log.json` receipt file; its embedded exact retained log-text hash is
`4a141868...cb92`.

No second launch, normal-close retry, signal, process-memory access, `R:`
restoration, or evidence publication is authorized. P0A-AH-001 supplies no
task-lifecycle, collision, terrain, material, visibility, causality, or retail
behavior conclusion. Any cleanup/recovery decision and any corrected passive
successor require fresh explicit authorization and a new frozen packet.

## 2026-08-21 offline postmortem hardening

No game launch, input, close attempt, signal, process-memory access, or `R:`
change occurred in this offline correction. The consumed argument-free wrapper
now refuses with `P0A-AH-001 is consumed; no deterministic successor level
route is frozen`, so it cannot be mistaken for a reusable authorization arm.
No P0B identity, stage, protocol, or authorization was created.

Two packet defects exposed by the consumed runtime are corrected offline:

- session-audit receipts retain stdout and stderr separately, authenticate each
  independently, and parse only stdout. A nonzero Make result still fails, but
  Make's stderr can no longer corrupt an otherwise parseable JSON census;
- both retained X sockets are now bound to their actual common peer. The peer
  record is the positive-PID/start/PGID `gamescope-wl` identity read from
  `/proc/<peer>/stat` and `/proc/<peer>/cmdline`, with the exact owned Gamescope
  command. The display remains independently bound to the sole exact
  `Starting Xwayland on :N` launch-stderr marker. The native fixture confirmed
  that Gamescope is the socket peer and also showed that its `/proc` `cwd` and
  `exe` links are not readable from the fixture process; the successor schema
  therefore does not invent those unavailable fields.

The failed level route was investigated but not patched speculatively. On the
PC path that enters Level Select, instruction `0x0043DB83` writes zero to
`word [0x00599AF8]`. In the chooser at `0x00443B40`, `0x00443F54` tests the
live Right bit `0x20`; the accepted path increments the local position at
`0x00443FB3`, and `0x004444D6` writes the resulting position back to
`0x00599AF8`. The increment condition contains no previous-state edge test.
These instructions were independently checked in a fresh bounded `objdump`
disassembly of retail SHA-256 `97c95ba5...b878`, not only in the Ghidra export.
The retained 180 ms Right receipt followed by internal level07—progression
position 10 in the static table—is consistent with repeated held-state polls,
but it does not prove their count or cadence. Earlier EXP-156 evidence also
shows that approximately 12 ms XTEST taps can be dropped. Therefore neither
the old persistent-X hold nor an unverified shorter tap is a deterministic
successor route. The separately established direct focused `xdotool`
edge-delivery mechanism was overlooked here and is operationally reconfirmed
below; it does not require a carousel screenshot or process-memory read to
support the exact Level01 log-gated route.

The user reported that save states do not currently work. That is an
operational constraint, not independently acquired runtime evidence, and no
save-state mechanism is used or proposed by this correction.

Offline identities for this correction are collector/validator SHA-256
`1e5f4c719c243b00d0abd0231588bbf11b1205a6c669280c75b2ec55307292ca`,
lifecycle analyzer `c7441293a2b2504abf2bae7c934d0dc2eb83cce63af6abde20671cf5f3b9fe78`,
wrapper `5ea5fcab93c36fb317a386156a5f1d176b326a613b443ceada1bb32370599f6f`,
and launcher `0965241132af6e15e9b19db9e8dc0b821ec85ff1f14f292e86037618c75f6051`.
The focused lifecycle/analyzer/packet/native-X suite passes 215/215 and the
full repository gate passes 1859/1859 with zero tracked-file violations. This
hardening authorized no runtime action. At that checkpoint a successor still
needed its overlooked established route restored to the design, plus a new
frozen identity, fresh explicit user authorization, and a new James verdict.
The route correction is recorded below.

## 2026-08-21 first postmortem audit rejection and exact-domain correction

James **REJECTED** exact commit
`932627d62c1a7d649d650c0c8e5c1d0d8e316c36` (tree
`4742aa21fcf2afa2b0b62455e6495daea1894567`). Although 214/214 non-native
focused tests, native X, and the 1859-test full collection passed, adversarial
packets showed three blocking defects:

- Python integer checks admitted JSON booleans in launch, process, X-peer,
  connection, and audit numeric fields, and audit timestamps admitted negative
  values;
- the two X receipts agreed only on PID/start, so different UID/GID values
  could describe one purported peer;
- a peer could predate the launcher or collide with the game/launcher
  identity, while the fixture used the same launcher and game PID.

The correction centralizes strict JSON-integer predicates, applies positive or
nonnegative domains to every authoritative identity and chronology field, and
gives the fixture distinct launcher/game/peer identities. Both X receipts must
now agree on one exact `(peer_pid,peer_uid,peer_gid,peer_start_ticks)` tuple.
The independently read peer must be the exact owned Gamescope command and
PGID, start no earlier than the launcher, and differ from both launcher and
game. The same strictness covers task metadata identity brackets, sample
enumerations, audit inner counts, raw/path asset identities, navigation
sequence, window observations, and successful title timing. Exact sample
timing is validated before direct enumeration drift can return unresolved.

Paired direct, executor, scientific, and rejected-prefix regressions pass
269/269; the native X fixture passes separately (270 focused total) and asserts
complete peer UID/GID consistency. The full repository gate passes 1914/1914
with zero tracked-file violations. Current offline identities are
collector/validator SHA-256
`71f9099aa2040e8cb141523f9114d38f9b972622b37dc935f513213995d528bd`,
lifecycle analyzer `c7441293...9fe78`, wrapper `5ea5fcab...99f6f`, and launcher
`09652411...f6051`. At that checkpoint the correction awaited James audit and
granted no runtime authority.

## 2026-08-21 second postmortem audit rejection and shared-partition correction

James **REJECTED** exact commit
`740cb0757df5c5c26345bc15e894060ca3767a00` (tree
`56818bd1a9610af6a332f1a5125499cbe09c03cf`). He confirmed the earlier boolean,
complete-peer, chronology/collision, and current-census fixes, but reproduced
four adjacent blockers:

- float aliases passed equality-only collection count, title/navigation hold,
  plan contract, settle duration, and owned launch-PID checks, while boolean
  `owned.polls` was ignored;
- direct enumeration drift returned unresolved before exact sequence/request
  grid, sorted-unique enumeration, or sorted-unique task validation;
- direct metadata errors could be phantom, contradict parsed identities, occur
  after first observation, or duplicate, and malformed success metadata was
  mislabeled unresolved without a bound failure receipt;
- a missing runtime `process.pid` raised raw `KeyError` before evidence-schema
  validation.

The correction applies strict positive/nonnegative integer checks to every
named equality-only field and validates the exact owned-clear field set plus
positive polls. Direct and packet validation now call one shared task-partition
gate. It requires sorted unique before/after enumerations and task identities,
exact sequence/request grid, complete enumeration-to-identity/error partition,
the guarded leader anchor, and unique metadata failures only at global first
observation. Malformed or contradictory success metadata raises
`EvidenceError`; only a missing record paired with one exact first-seen failure
becomes unresolved. Missing runtime PID is converted to an evidence error.

All reproduced scientific and rejected float aliases, the seven direct drift/
metadata counterexample families, and missing runtime PID have paired
regressions. The non-native focused suite passes 297/297, native X passes
separately (298 focused total), and the full repository gate passes 1942/1942
with zero tracked-file violations. Current collector/validator SHA-256 is
`415fe20a699a3491735c9cbbb8f169da65ee067ef842811125964dc098085e4e`;
the other three production hashes are unchanged. This remained offline and
awaited James re-audit at that checkpoint. No runtime, `R:`, pending evidence,
or authorization state changed. The later ACCEPT verdict is recorded below.

A read-only `make session-audit` at `2026-08-21T05:35:13-04:00` recorded three
unattributed helpers—Gamescope `1834786/30382246`, gamescopereaper `1834935`,
and winedevice `1834980`—plus private sink `ablpc_mute_1834769`, with no open
managed session. An independent existence check found launcher shell `1834769`
and those helpers present, but prior Xwayland `1834812` and game `1835030`
absent. This updates the current census without erasing the historical
seven-process post-wrapper census and without attributing a cause. Pending
evidence/stage, `R:`→stage, sink, and absent terminal evidence identities are
unchanged. No runtime input, close, signal, memory access, restore, or launch
occurred.

## 2026-08-21 postmortem acceptance and operational Level01 correction

James returned **ACCEPT** on exact postmortem commit
`1b61da32c93b1238c108c0a95cb02628f3284949` (tree
`925ce807af1cd4db706a2d6f733ba935b73d30ba`). His independent audit passed
297/297 non-native focused tests, native X (298 focused total), the 1942/1942
full gate, and 50/50 reproduced prior/adjacent counterexamples. This accepts
the offline validator hardening only. P0A-AH-001 remains consumed/pending with
zero samples.

The premise that a successor still needed to discover a deterministic
Level01 route was then corrected. With explicit user direction, the recorded
P0A residual process group and winedevice were recovered; TERM did not clear
them, so KILL was sent only to those exact verified targets. Their sink
disappeared and the next prelaunch session audit was clear. Pending P0A
evidence/stage bytes and `R:` were unchanged.

A fresh operational PC launch used auto-hardware image `1e1d5099...c41f`, the
exact LevelSelect marker plus one-second settle, and the already-established
direct focused `xdotool` delivery: Right held 180 ms, one-second gap, Return
held 180 ms, then final Return held 180 ms. The new log loaded
`Y:\PC\BUGS\cd\level01\level.dat` and reached Start/End ClearLoadScreen,
End InitMainGame, and NextLife. A transient compositor capture
`77f6eeff...84f598` visually shows live Anthill gameplay. The game remains
open for the user and is not P0B evidence. No process-memory access, save
state, debugger, DAT mutation, or `R:` change occurred.

This does not resolve carousel-counter semantics. It does resolve the
procedural route blocker: P0A's Level07 failure followed its substitution of
the new persistent-X held-state delivery for a proved direct input path. A
fresh P0B may retain no process-memory access by using the exact direct route
before its persistent collection connections are opened. It still requires
new identities, a frozen/tested packet, James acceptance, and fresh explicit
runtime authorization. No lifecycle, terrain, collision, material,
visibility, or causal conclusion follows from the operational launch.

## 2026-08-21 P0B offline successor implementation

P0B is now implemented under protocol
`ablpc-r2p-p0b-passive-lifecycle-v1` with fresh `P0B-AH-001` namespaces and a
separate `Y:` stage. The production entry point is deliberately inert: it
raises `P0B-AH-001 is offline-only and not runtime-authorized` until fresh
explicit authorization and a pre-runtime James acceptance are both recorded.
The currently open operational PC process is excluded by the required exact-
clear prelaunch audit and is not P0B evidence.

The executor preserves the accepted 521 requests, 20 ms cadence, sample-5
title Return, task/error partitions, Gamescope credential binding, publication
manifest, fsync, and ambiguity semantics from P0A. Before navigation it
authenticates the complete pinned P0A stage/pending trees; after cleanup it
requires identical manifests. P0B paths must be absent, canonical, and outside
both exclusion roots. `R:` is never remapped.

The only precollection navigation actions are direct focused `xdotool` Right
and select Return, each held at least 180 ms and separated by exact guarded
one-second settles. A wrong level load rejects before persistent sockets open.
After exact Level01 plus Start ClearLoadScreen, two distinct persistent X
connections open and the grid begins. The independent worker sends the sole
title Return at sample 5; ordered unique gameplay markers are authenticated
only after the final sample against the exact pre-title log prefix. Once
`collection.json` exists, xdotool close fallback is prohibited.

Exact scientific packets require the gameplay gate. Exact collection-failure
procedural rejections omit it; precollection or gameplay-gate failures remain
pending and produce no lifecycle result. Every cleanup failure remains pending
without signal fallback, `Y:` restoration, or terminal publication. The
first immutable candidate passed 308/308 focused tests and 2250/2250 full
tests, then James **REJECTED** its exact commit `2277b75` / tree `cf2f88c`.
The retained executor could clone a stale `bugs.log`; wrong-level detection was
`Y:`-specific; xdotool was not display-bound; strict JSON still admitted focus,
settle, gameplay, and nullable-window aliases; publication receipts/manifest
were not exact; direct collection structures were permissive; and the
save-state/ptrace/P0A-`R:` boundary was inconsistent.

The successor correction removes and authenticates the staged log before
launch, binds one newly created regular file identity through exact UTF-8
append prefixes, recognizes level loads across drives and slash spellings,
scopes all xdotool receipts to `runtime.x_display`, shares exact structural
validation before every lifecycle outcome, authenticates ordered publication
phases and canonical manifest closure, uses one prohibited-action schema, and
binds the preserved `R:` symlink in plan, both receipts, current filesystem,
and lifecycle chronology. Its focused analyzer/packet/native-X suite passes
351/351, including every reproduced attack and real staged-log removal. The
full repository gate passes 2293/2293 in 663.10 seconds with zero tracked-file
violations. Corrected collector/validator SHA-256 is `91cd0ec4...786b`;
lifecycle analyzer remains `c7441293...9fe78`, wrapper `e4ae7fbf...e3ff`, and
launcher `09652411...f6051`. The next audit below then rejected that exact
candidate. This was still offline-only: it created no runtime authorization
and supplied no lifecycle, terrain,
collision, material, visibility, or causality evidence.

## 2026-08-21 P0B second immutable rejection and correction

James **REJECTED** exact commit
`8b8d19df0dd8d1db76ef26302753add2938039b0`, tree
`e8b58c9f26dea6473648b71017ad0ff5b05f3ede`. He passed the 351/351
focused suite, confirmed absent production P0B namespaces and the fail-closed
wrapper, and reproduced nine blockers:

1. the pre-Right guard recognized only backslash level paths;
2. direct P0A exclusion validation did not bind entry count and exact entries;
3. a later coherent Level02 load could supply the gameplay append;
4. duplicate XIDs and a second focused X window were accepted;
5. retained audit parses admitted float/bool/int aliases through Python
   equality;
6. `r_mapping.is_symlink` admitted integer/float aliases for `true`;
7. publication result receipts admitted numeric aliases;
8. an exact-key list connection receipt leaked raw `AttributeError`; and
9. a lexical `..` terminal-root alias bypassed complete publication receipts.

The successor shares one any-drive/either-slash level-load parser across the
executor and packet chain and requires exactly one total post-LevelSelect
Level01 load. It validates exact P0A entry schemas/count/order, unique window
XIDs with one retained focus, retained audit types, an exact boolean `R:`
mapping, canonical publication bytes derived from the validated result, object
connection receipts, and canonical absolute packet roots. Paired direct,
scientific, and procedural-rejection regressions pass in a 396/396 focused
suite. Collector/validator SHA-256 is
`b50a81d847eb225b25b75f4f5baf6260ecb17b456e6005132be6a219489eb4e5`.
No runtime/session action, memory access, save-state action, P0A mutation, or
authorization consumption occurred. At that checkpoint P0B was offline-only pending a new
exact-commit James acceptance and fresh explicit runtime authorization.

## 2026-08-21 P0B third immutable rejection and correction

The 396-test successor passed `make check` at 2338/2338 in 666.31 seconds with
zero tracked-file violations and was frozen as commit
`e0fa61a4e634a47e811bbe0a94b161a0aefca06a`, tree
`02550b15d3ed588f87b790f585057d130fc2233e`. James independently passed the
same 396-test focused suite and broad schema sweeps, but **REJECTED** it for two
blockers:

1. list/dict JSON values in a retained P0A entry `type` reached dictionary
   membership before string validation and leaked raw `TypeError`; and
2. executor and packet validation ignored a fresh wrong-level load before the
   sole LevelSelect marker because they parsed only the post-marker suffix.

The successor requires a string entry kind before membership and emits the
controlled evidence error in direct, scientific, and rejected paths. It also
requires zero parsed level loads anywhere in the fresh LevelSelect prefix
before the first key and exactly one later Level01 load through final gameplay.
The paired focused suite passes 405/405. Collector/validator SHA-256 is
`347fd5062aff61c7302ced489621fa6b3caec7460b170150f6568969f413e014`.
No runtime/session action, memory access, signal, save-state action, P0A
mutation, or authorization consumption occurred.

## 2026-08-21 P0B immutable offline acceptance

The correction passed 405/405 focused tests and `make check` at 2347/2347 in
663.90 seconds with zero tracked-file violations. It was frozen as exact commit
`3c90a6f1e2291f21e756be7c7f339bd2bdbd33e9`, tree
`5fb8ea633f4401e471d29aaced69bb148afe37d5`. James independently passed the
focused suite, replayed the prior and adjacent schema/route/lifecycle/
publication boundaries, confirmed exact P0A 2339/17-entry exclusions and
preserved `R:`, absent P0B namespaces, wrapper exit 2, and clean git, and
returned **ACCEPT**.

This accepted only the immutable offline P0B pre-runtime design. At that
checkpoint the wrapper remained fail-closed and no runtime authorization had
been consumed or created. The later authorization recorded below remains
limited to the
frozen direct Right/Return route, sole sample-5 title Return, exact 521-point
passive `/proc` grid, normal close only, and authenticated classification. No
memory access, ptrace, signal, screenshot, save state, DAT/localizer/candidate,
P0A mutation, or terrain/collision conclusion is permitted. A finite grid
cannot prove absence outside its observation interval.

## 2026-08-21 P0B one-shot authorization and blocked activation

Immediately after the accepted design's fresh-authorization requirement was
restated, the user replied `okay continue on`. This authorizes one exact
`P0B-AH-001` wrapper process invocation only. The first process invocation
consumes the identity regardless of pre-plan failure or exit, and no retry is
allowed. If pending or terminal evidence exists, the activated source bytes
remain pinned because packet validation authenticates them and namespace
exclusivity prevents replay. Only an exit before any P0B namespace exists
permits retiring the entrypoint; authorization is still consumed.

The preflight audit remained dirty with the deliberately preserved operational
group `1978654`, game identity `1978909/33236220`, Xwayland `:2`, and sink
`ablpc_mute_1978654`. The authoritative activate, focus, then unscoped-XTEST
`Alt_L+F4` normal close did not clear it. No signal was used, no P0B namespace
was created, and the one-shot arm remains unconsumed.

The accepted activation replaces the offline raise with exactly one
`P0BExecutor(frozen_config()).run()` call. Both former offline-wrapper tests
are launch-proof fixtures before any broad gate: one proves exactly one
constructor and one `run()` call on the frozen config; the other monkeypatches
a controlled wrapper error and proves production namespaces unchanged.
Collector/validator SHA-256 is
`9e2093bbfa27dd3b4e68ece79ebde296e7977fc14ed9c5d08cf49b4111ea2a5e`.
Focused tests pass 405/405 and the safe full gate passes 2347/2347 in 667.45
seconds with zero tracked-file violations. James independently **ACCEPTED**
exact activation commit `c3ad480f7988870eba3582f8d8d887aae9a50942`, tree
`59acd5d5ace9328a28cf99c1bf3e71fc418370a5`, after the exact 405/405 focused
suite and launch-isolation/source-pin review. An immediately preceding exact-
clear session audit and the frozen immediate prechecks are the sole remaining
gates before the single real invocation.

## 2026-08-21 P0B-AH-001 consumed pending runtime

The user explicitly authorized process killing with `can't you alsojust use
pkill or something`. The exact prior operational group `1978654` first received
TERM. Its launcher/game/Gamescope/Xwayland/wineserver and sink cleared; only
guarded survivors `gamescopereaper 1978824/33236126` and `winedevice
1978862/33236135` required KILL. The next `make session-audit` was exactly
clear. All five P0B namespaces were absent, the P0A stage/pending trees were
exactly 2339/17 entries with their pinned hashes, `R:` still mapped P0A, `Y:`
mapped retail, the accepted P0B source hash matched, and git was clean.

The exact wrapper was then invoked once and is consumed. It passed hardware,
route, Level01, window, asset, title-input, schedule, and gameplay gates. The
collection contains 521/521 samples; maximum start lateness is 70,151 ns and
maximum completion latency 2,194,275 ns, inside the frozen 2 ms/10 ms limits.
There are zero acquisition, metadata, enumeration, or title-input errors.
Direct analysis returns only `diagnostic-valid-task-added`: exact task
`2086681/34785536` is absent at sequences 0–26, first appears at 27, and remains
through 520. There are no removals, reused TIDs, short-lived identities, or
mixed class. `collection.json` SHA-256 is
`d8ff0e76d62cb9ce133dc48845aa00ef0ac92a7083b48d9c187d312c8d44bc2f`.

The focused normal-close chord was delivered successfully, but the game
survived 89 polls. The wrapper exited 2 with cleanup error `normal close failed;
signal cleanup is prohibited`, used no signal, did not restore `Y:`, and
retained a 26-file pending tree at SHA-256 `323c958d...451661`. New launch group
`2086248`, game `2086503/34784704`, and sink `ablpc_mute_2086248` remained live;
`Y:` remained the P0B stage and `R:` remained P0A. The standard scientific and
rejected validators correctly refuse the missing restore/publication inventory.

James independently authenticated the cross-bound runtime, log, navigation,
collection, and cleanup receipts and returned **ACCEPT** for the provisional
finite-grid task-addition conclusion plus **ACCEPT** for fail-closed pending.
At that P0B checkpoint, this proved only that one task was added and persisted
through the remaining finite samples. It had not established its function/
creator, later persistence, cross-run replication, debugger relation, terrain,
collision, material, visibility, or causality. P0C below later resolves only
the bounded replication/debugger-necessity point; the original packet must
remain pending forever and P0B must never rerun.

## 2026-08-21 separate authorized-signal recovery candidate

James accepted only an additive recovery design. New protocol
`ablpc-r2p-p0b-authorized-signal-recovery-v1` and separate recovery-pending/
recovered namespaces pin the original 26-file manifest and collection/
disposition hashes without changing them. The tool records the user's signal
authority and operator-only invocation/exit provenance, requires clean git,
authenticates all four original source pins plus its own source hashes, and
revalidates the exact current group and three helper PID/start identities.

Recovery permits TERM to exact group `2086248/34784562`, then KILL only to
identity-rechecked survivors. Exact helpers `2086420/34784596`,
`2086429/34784600`, and `2086454/34784605` receive their own TERM and guarded
survivor KILL. Only module `536870916` may be unloaded, and only if it still
names `ablpc_mute_2086248`. Every check, signal completion/failure, and poll is
atomically retained. A clear process/sink audit is required before atomically
replacing and fsyncing `Y:` from the exact P0B stage to retail; another clear
audit, unchanged original pending tree, exact P0A 2339/17 trees and `R:`, and
exact stage/auto-hardware asset hashes follow. Canonical result receipts and a
closed manifest publish separately as
`recovered-out-of-band-after-authorized-signal`; the original run is explicitly
not relabelled normal-clean and no future runtime is authorized.

James rejected first implementation `575756d` / `004bf35d`. He independently
reproduced float/bool aliases throughout receipts, forged commands,
contradictory member/check and present/absent histories, nonconsecutive polls,
noncanonical manifests, incomplete invariant identities, silently dropped
`/proc` enumeration errors, stale individual-signal guards, pre-validation
publication receipts, and pre-namespace/final-rename failure gaps. He also
identified unbound operator Git strings. No runtime was inspected or changed.

The successor removes the unbound Git fields and freezes exact commands for all
12 identities. Its group census parses every `/proc/<pid>/stat` first and
retains/rejects every unresolved row; every individual TERM/KILL rereads and
retains the exact PID/start/group/command guard. Poll receipts carry exact
start/deadline/budget/interval, consecutive attempts, monotonic absence, and
terminal state. Complete immutable-tree entries and current original/P0A/R:/Y:
and asset identities are authenticated. The first process invocation creates
an exclusive attempt before preflight; a distinct stable failure namespace
survives any later error. Success publishes core -> prevalidated pending ->
fresh unverified -> postvalidated/canonical-manifest -> fresh recovered.

James rejected exact successor `d4de863` / `208e6fd` for three further
counterexamples. `original-pending-before.json` used plain equality and accepted
nested integer-to-float/bool aliases; event validation allowed another poll
after a prior poll exactly at its deadline; and both `lexists`/ordinary-rename
publication moves could overwrite a competing empty directory created in the
race window. No runtime was inspected or changed.

The next correction uses `_exact_json_equal` for the complete pending receipt,
rejects any poll after a prior observation at or beyond its exact deadline, and
uses Linux `renameat2(..., RENAME_NOREPLACE)` for both directory moves with a
fail-closed unavailable/error path. Race-injection tests prove that both
competing destinations remain intact. Recovery module SHA-256 is now
`d1b3e4af...3c38a`; wrapper SHA-256 remains `2b26e74d...fa2e1`. Recovery tests
pass 48/48, all non-native P0B tests pass 482/482, and native X passes
separately. Full `make check` passes 2395/2395 in 672.58 seconds with zero
tracked-file violations. At that checkpoint the corrected tool had not run;
clean exact commit and James pre-execution ACCEPT remained required.

## 2026-08-21 recovery failure and accepted operator cleanup

James accepted recovery commit `fae9b2f4c4e840f64f41d92dfc8efb21d7edaa45`
/ tree `a6e9148d84d56effb32b532327c35a1e4b79f33e`; its sole invocation is now
consumed. The authorized group TERM began shutdown, but the next exact identity
guard encountered still-present processes whose command line had cleared. The
recovery failed closed before `Y:` restoration or recovered publication. Its
retained pending and failure trees are 6 entries / `444b221e...f309e` and 1
entry / `8e2fb90e...f5d1`.

Between the authenticated pre-recovery and post-TERM states, 160 bytes of
shutdown text were appended to the original P0B `launch.stderr`. Chronology,
content, and retained-FD provenance make attribution to recovery shutdown
consistent, but it remains an inference. The suffix SHA-256 is
`aa26aff2...da66`. The former 26-file `323c958d...451661` identity is therefore
the exact historical pre-recovery state, while the preserved current packet is 26 files /
`1092fcb9...25f2` and the log is 11,423 bytes / `fb2ba241...eaf5`. No byte was
repaired or removed.
The remaining exact processes were Gamescope `2086265/34784563` and
gamescopereaper `2086416/34784596` in group `2086248`, plus winedevice
`2086454/34784605`; the sink and open-session lists were empty.

The separately authorized operator-only protocol
`ablpc-p0b-operator-cleanup-after-consumed-recovery-failure-v2` was frozen at
commit `4de8b085f856a54fec315a078dc4f07dc8161852`, tree
`666cd92f5cdb933ebe68efb04a308387d7d6d528`, after 30/30 operator, 266/266
focused, and 2425/2425 full tests. James accepted that exact preflight. The sole
invocation then sent individual SIGTERM and, after its bounded poll, fresh-
identity-guarded SIGKILL to only the same three PIDs. It did not signal a group,
perform a broad kill, or act on a sink. Its 65-event terminal record has no
signal failure.

Both retained post-signal and post-restore audits are exactly clear. `Y:` is
restored atomically and parent-fsynced to retail `BUGS_PC-full-disc`; `R:` still
targets the exact P0A stage. The operator added zero later bytes to
`launch.stderr`. James independently authenticated the 15-entry terminal tree,
SHA-256 `24df2fb7da89effca3e72a9b52e4bcb1ea15184bcd0401841b6954ce3a23d65b`,
and returned **ACCEPT**.

This closes only the recorded residual environment. The original P0B packet
remains `pending-cleanup-failed`, the recovery remains `failed-consumed`, and
the original run is not relabelled normal-clean or recovered. At this cleanup
checkpoint, its provisional task-addition observation was unchanged: task
`2086681/34785536` was present only in the bounded sequences 27–520, and
cross-run reproduction/debugger necessity had not yet been tested. P0C below
resolves only that limited lifecycle-class question. The task's name, creator,
function, later persistence, and any terrain/collision/material/render role
remain unknown. No future runtime is authorized.

## 2026-08-21 P0C offline attribution and census boundary

P0C performs no runtime or live `/proc` access. Argument-free command
`scripts/r2p-analyze-p0c-task-attribution.py` authenticates the append-
preserving 26-entry P0B pending tree at SHA-256 `1092fcb9...25f2`, the exact
collection SHA-256 `d8ff0e76...44bc2f`, the accepted R2o D1-AH-005 packet,
and the retail/auto-hardware PE plus static exports. It applies the production
P0B analyzer and accepted R2o grammar before comparing title-relative time.

The exact confirmed topology is:

- P0B sequences 0–26 contain 16 tasks; sequences 27–520 contain 17;
- the sole addition is `2086681/34785536`, with no removal, reuse, later
  transition, unstable enumeration, acquisition error, metadata error, or
  title-input error;
- first-seen metadata is `comm=bugs.exe`, sleeping, `Tgid=2086503`,
  `Pid=2086681`, `PPid=2086416`, `Threads=17`, `TracerPid=0`, zero blocked
  signals, and the guarded Wine-preloader identity;
- sequence 26 starts `239.282435 ms` after title keyup and still has 16 tasks;
  sequence 27 starts `259.282684 ms` after keyup and has 17. These are
  observation bounds, not exact creation time;
- the identity remains observed through sequence 520, an exact first-to-last
  sample-start span of `9.859999646 s`; later lifetime remains unknown;
- R2o D1-AH-005 independently has 16 tasks at open-and-arm and 17 at the first
  trap. Its initial census completes `88.530394 ms` after title keyup and its
  changed census completes `269.576809 ms` after keyup. R2o did not record
  `_SC_CLK_TCK`, so its `start_ticks` is not converted.

Thus a one-task 16→17 post-title lifecycle class occurred in two fresh
processes, including debugger-free P0B. Debugger activity is not necessary for
the class. This does **not** prove that R2o TID `1648646` and P0B TID `2086681`
are the same logical worker or that debugging did not affect the R2o instance.

PC static evidence narrows the best role candidate. `FUN_0042BB90` emits
PLAYTRACK, initializes the DirectSound stream buffer through `FUN_0042C9C0`,
sets the stream-active flag, and synchronously dispatches `WM_COMMAND 0x9C46`.
That handler calls `0x00401276 -> 0x0042CE80`, whose sole direct
`CreateThread` call is `0x0042CF04` with start thunk
`0x00401889 -> 0x00440F50`; the worker waits on two stream-notification events.
P0B's authenticated append contains one Level1a PLAYTRACK followed by
SETMUSICVOL. “PC Level1a DirectSound stream worker” is therefore the strongest
candidate, but remains an inference. No receipt binds the Linux TID to
`0x00440F50`; the untimestamped log, generic `comm`, PPid, sleep state, Tgid,
and executable identity cannot supply that link.

The first offline implementation passed 28/28 focused and 2453/2453 full tests
but James rejected exact `f362fae` / `de8f1af`. Its inherited check-then-
replace publisher could destroy a racing destination and did not durably
record a newly created output directory; central 16/17, no-debugger, and log-
chronology meanings were not all semantically checked; decoder/thunk/builder
spans and the executed-source/objdump ledger were incomplete; the output made
one unsupported BPF/tracefs assertion; and the session wording overstated
sample-start bounds. The rejected `task-attribution-001` output remains
unchanged at SHA-256 `ecd92bfd...9c7`.

The correction publishes only to fresh
`work/copies/EXP-20260820-005/evidence/offline/task-attribution-002/analysis.json`,
SHA-256 `6156b96847936f778577a7ef5fae8a223a0e9c424514b5f324759007ad841f88`.
It uses canonical ancestor checks, durable fresh-directory creation, and
`renameat2(RENAME_NOREPLACE)`; retains competitors; requires exact 16/17
segment sets and plan/disposition no-debugger semantics; cross-binds exact
Level01/title/grid/gameplay chronology and marker receipts; pins the complete
WM_COMMAND decoder/arm, buffer-init thunk, event builder, executed scientific
sources, and objdump; and labels creator tracing not assessed offline.
Analyzer/wrapper SHA-256 values are `089a9e81...5157` and
`68410c5c...8563`; the correction suite passed 44/44 and the full gate passed
2469/2469 in 647.40 seconds with zero tracked-file violations. James rejected
exact `923ffb2` / `4db811a` because the advertised complete executed-source
ledger omitted `r2c_f0.py`, the intermediary through which retained R2o bound
`sha256_file` and other names.

That rejected `task-attribution-002` output remains unchanged. The successor
publishes only to fresh
`work/copies/EXP-20260820-005/evidence/offline/task-attribution-003/analysis.json`,
SHA-256 `62af5c091c9f97499c346146c50d2ceaf0fb7e3d05ddd0056338da099a96d6ff`.
It pins `r2c_f0.py` (`3d171ba9...a8f`) and active dependency
`r2c_localizer.py` (`fbd55193...906`) in addition to the prior sources. It
also pins `ablpc/__init__.py`, `anm.py`, and `level_dat.py`, which the wrapper's
package import executes. An independent AST regression requires the complete
wrapper-rooted local import closure to equal its anchored module set.
Analyzer/wrapper SHA-256 values are `a3f35182...813b` and
`68410c5c...8563`; 45/45 focused tests and 2470/2470 full tests pass, the
latter in 647.23 seconds with zero tracked-file violations. The final exact-
tree gate passes 2470/2470 in 648.20 seconds with zero tracked-file violations.
James independently regenerated `-003` byte-for-byte, matched its 11-entry
source ledger to the actual loaded local-module census, replayed the prior
publisher/semantic/static counterexamples, and **ACCEPTED** exact commit
`f2629944b9163ae39e608320e60e7fed76fabb09`, tree
`9c7c1294e60f3c0ed6bb47f9f8575362d9ac1d45`. This acceptance closes only the
offline P0C packet; the scientific and authorization ceilings below remain.

The evidence falsifies the old early 16-task census as stable and does not
establish a universal or immutable 17-task census. It justifies an offline R2q
redesign: authenticate the Level1a PLAYTRACK/gameplay transition,
prospectively require a fixed repeated-census quiet interval, freeze the
result only as **pre-attach stable**, recheck immediately before attach, and
continue fail-closed census checks through acquisition and cleanup. The exact
quiet interval and full acquisition budget still require a frozen audit.
Dynamic enrollment after attachment remains forbidden. No R2q runtime, memory,
debugger, signal, or terrain/collision/material/visibility action is authorized.

## 2026-08-22 R2q offline quiet-census design

The authenticated P0B collection cannot measure post-gameplay quiet: its last
sample completed at monotonic timestamp `347865223262239`, while the first
authenticated gameplay observation is `347865275165589`, a positive gap of
`51,903,350 ns`. R2q therefore derives no threshold from P0B and fixes its
future barrier prospectively.

For each of D1 and D2, the frozen design requires 3,002 complete census
summaries with request sequence 0 through 3,001 at 20 ms request spacing. The
first-to-last request span is `(3,002 - 1) * 20 ms = 60.020 s`; authenticated
coverage from the first sample start through final sample completion must be
at least 60.020 seconds, while each start may be at most 2 ms after its request.
The baseline is each run's first post-gameplay census. No fixed
17-task count, TID list, or task role is accepted. The actual first
`PTRACE_SEIZE` syscall is recorded separately from attempted-action and
receipt-fsync timestamps and must occur within 20 ms after pre-attach
completion.

The accepted acquisition interval is independently capped at 60.000 seconds
from the durable attempted-action timestamp through debug-register restoration,
signal-zero detach verification, and the post-detach census. Timing validation
can return only `timing-boundaries-satisfied`; scientific acceptance remains
undetermined until every topology, environment, log, mapping, journal, action,
capture, cleanup, and publication rule validates. Scientific timeout requires
cleanup but cannot become an accepted packet.

The future two-control design uses fresh D1/D2 `-008` namespaces, stages and
restores `Y:`, and preserves P0A's exact `R:` target. Each control requires one
pre-title gate PNG plus three complete stopped invocations, each with two
triplicate batches: 19 PNGs per control and 38 total. Each invocation has the
current R2o four phases, eleven post-seize memory-read ranges, exact debug-
register/exception behavior, stable 640x480 PNG decoding, triplicate PNG/RGB
identity, and ordinal D1/D2 equality. There is no adaptive nearest-phase rule.

James rejected the first immutable output,
`quiet-census-design-001/design.json` SHA-256
`529a798fa752e30b113c8bc158c2f2f79faf59d4f83e01b9fde89da276838217`,
because the design lacked a strict terminal validator, separated timing from
scientific acceptance incorrectly, omitted the actual first syscall/full
inventory, left receipt and capture grammars open, incompletely cross-bound
P0B and R2o, did not guarantee same-byte source parsing, and omitted the
current R2o wrapper closure.

The first correction, `quiet-census-design-002/design.json`, is SHA-256
`7de8d565732f76fa10e84b96429d2274199826b0870d8f801034162595aef3ad`.
Analyzer/wrapper/test SHA-256 values at publication are respectively
`1a814cc3271f1b0b3f6c8282cff2fb375183656e64b689120f2be40d4525d9a9`,
`cf02db6beecf4fd8c4a52e7036bb7d1762f2ade1c209aa7bf74486a59316ccb5`,
and `5079f97222ea1c9c868b9eec74c88ecc98e32a4618baefd77f8e36281839bf68`.
Its focused suite passes 69/69. The candidate-tree repository gate passes
2539/2539 in 651.29 seconds with zero tracked-file violations. James
independently passed the focused suite and authenticated output, then
**REJECTED** exact commit `a8840d51dbf7f8ae52b19c0a97d84ceb85fa9711`,
tree `b0cdfb3fc91954384babc3055ac12d8b1f675d8f`. Direct
`build_frozen_design` accepted forged title key/failure/hold/timestamps,
unbound P0C collection/title summaries, contradictory or phantom task
metadata, and a forged pre-title hash. The claimed closed receipt grammar
listed fields but did not freeze executable nested action/capture semantics.
The note also overstated coverage as beginning no later than request zero;
the accepted validator instead allows up to 2 ms start lateness and requires
at least 60.020 seconds from first sample start through final completion.

Immutable `quiet-census-design-003/design.json`, SHA-256
`c41256e585242db7b42432982b23a50593e6c64f1546f2220348777fd943931d`,
closed the retained P0B/P0C semantic defects. James nevertheless **REJECTED**
exact `caeddfd45d5d9c6524908cd258070ff40265171d` /
`ac853d4960bfeaa987e9832747f6dd427a83e99d`: the census schema accepted empty,
late, leaderless, and overlapping-reuse constructions; manifests never read
or dispatched their receipt bytes; the journal permitted launch after failed
preflight; captures lacked stopped anchors, cross-entry chronology, guards,
and actual PNG-byte authentication; and the D1/D2 comparison could reuse one
control while omitting four required R2o result families.

Fresh `quiet-census-design-004/design.json` is SHA-256
`0f0f7cfe5ee70cd3459606d157e81888b4eb00320a962d0f899916d8a9c05f9b`.
Analyzer/wrapper/test SHA-256 values at publication are respectively
`0674fdfda57f15b1c08ed15673ad97a9f8b59875355780988c2f125d646f2856`,
`cf02db6beecf4fd8c4a52e7036bb7d1762f2ade1c209aa7bf74486a59316ccb5`,
and `923a6bf2b5ca7e167be73fb6ec845fe8eeba6e40a2b6a6cf5c278f38702cbf36`.
It preserves `-003` as an immutable rejected anchor and closes James's five
runtime-schema findings with executable validators:

- each census is nonempty, includes the exact guarded leader/process start,
  uses disjoint addition/removal/reuse partitions, and is bound into the exact
  3,002-point timing grid plus separate pre-attach observation;
- each manifest authenticates canonical receipt bytes and dispatches every
  kind to a closed semantic validator, including 18 pre-action/post-resume and
  18 post-action census receipts;
- the journal enforces prerequisite failure/skipped-action transitions, exact
  completed/validated action identity, and aggregate-derived manifest hashes;
- each capture derives its target from the stopped anchor, enforces command,
  settle, decode, and cross-capture chronology, authenticates actual PNG
  chunks/CRC/IDAT decode, and derives 640x480 RGB/nonuniform facts;
- the ordinal D1/D2 comparison requires distinct process/stage/evidence
  identities and equality of selector bit, common range, Flik coordinates,
  generated matrix/origin/copy, and completion PNG/RGB.

A complete synthetic control packet exercises the byte-to-manifest-to-journal
chain and all census/timing/capture/R2o cross-bindings. The focused correction
suite passes 121/121. The candidate-tree repository gate passes 2591/2591 in
673.17 seconds with zero tracked-file violations. At that freeze boundary,
exact commit identity and James's certifying verdict were still pending. The
wrapper remains an offline publisher
only: no runtime entry point, execution authority, or terrain/collision
conclusion follows.

James then **REJECTED** exact `0606bcf8d94e6d1d26eaa8e95f2993ba8e319914` /
`ca7800e516b324c6954bf45bc02f0b090b666b85`. Immutable `-004` accepted a 1 ns
three-key envelope and ordered its alleged pre-title evidence after title
Return; left census process/window/mapping/log hashes and stage/seize/detach
identities unbound; allowed post-seize and post-detach chronology inversions;
described rather than executed the task/debugger/memory/detach and terminal
namespace/publication grammars; lacked D1-before-D2 execution; allowed shared
process groups; and admitted direct numeric aliases or raw range exceptions.

Fresh `quiet-census-design-005/design.json` is SHA-256
`a5472f0124c1e2d9b2bd13d6071aa4fbf86de386cf9158fe84559cefa0031c5e`.
Analyzer/wrapper/test SHA-256 values at publication are
`01e5af9e6b5a4232e1c071f4d4a9272ddada94c6745a79542377b1176588db6f`,
`cf02db6beecf4fd8c4a52e7036bb7d1762f2ade1c209aa7bf74486a59316ccb5`,
and `9bd72b48f7feaa089e278ec20cb053c8f9ddab79ad1aab3ce6fe62decf12f81e`.
It makes every rejected boundary executable. Its debugger lifecycle follows
the current source: seize all baseline tasks, interrupt all, require exact
`PTRACE_EVENT_STOP`, preserve allowed baseline DR6/DR7 bits, arm DR0 on every
task, continue every task, accept the selected task's natural hardware stop,
then interrupt only nonselected tasks and restore/read back exact originals
before signal-zero detach. The focused suite passes 150/150. The full gate,
run on the candidate tree, passes 2620/2620 in 772.75 seconds with zero
tracked-file violations. James's subsequent exact rejection is recorded below.
No runtime occurred and no runtime authority or terrain/collision conclusion
followed.

James **REJECTED** exact `814ada4054be6fa345bff39cc83d37eea6887381` /
`b79e88587a5bbc99337eeab3d45e540bbbc58eaf`. His ten-blocker packet showed
that `-005` did not actually parse the Level01 load set, had an impossible D2
namespace gate, underauthenticated publication/mapping/audit/close receipts,
asserted rather than derived debug-register state, omitted EndScene's second
continue/wait, permitted rejected cleanup uncertainty, discarded successful
failure prefixes, admitted nested numeric aliases, left D1/D2 P0A identities
independent, and accepted a weak title task guard.

`quiet-census-design-006/design.json` SHA-256 `a068f686...1b33` was frozen but
superseded before James audit: final self-review found that D1's accepted-root
tree hash was only asserted equal across controls. Fresh
`quiet-census-design-007/design.json` is SHA-256
`f7cf2346245a4eb43eae1453e5cdd02257b462d79a58f8f691a3796ceba62d12`.
Analyzer/wrapper/test SHA-256 values are respectively
`f489d3b256b89cbb8e1a3cd97668f1e2e3256c6b6f88cadea42cac9c60d5e828`,
`cf02db6beecf4fd8c4a52e7036bb7d1762f2ade1c209aa7bf74486a59316ccb5`,
and `6a334143d36908809f8c0683a62c0e8c926937609d0f5e3d7a3c4a47709c77ae`.
It closes the packet without broadening science or authority:

- the fresh canonical log is reset with file/parent durability, rebound by
  device/inode to the append, and contains exactly one staged `LEVEL01` load
  plus exactly one ordered occurrence of every gameplay marker;
- D1 requires all future paths absent, while D2 authenticates the immutable D1
  accepted root and keeps D2/comparison future paths absent; both controls
  reuse one exclusive no-replace attempt identity and identical P0A/R/P0B
  invariants;
- mapping stage/restore receipts carry compare-before, operation result,
  readback identity, and durability; session audits authenticate raw empty
  process/sink/session inventories; normal close authenticates the exact
  process and wait result;
- terminal and comparison publication reread the exact canonical destination
  bytes, preserve rename device/inode identity, fsync both parents, and publish
  the same acyclic manifest/receipt-map envelope later aggregated; the D1
  accepted root is an authenticated canonical one-entry tree manifest bound to
  those exact bytes, file identity, and parent identity before D2 observes it;
- only the selected task is armed. Every register reprogram has exact
  before/desired/readback chronology, active PCs are derived, EndScene has two
  complete resume/stop receipts, and cleanup requires attach plus the exact
  R2o-derived final state;
- failure manifests authenticate and dispatch every successful normal receipt
  prefix before one terminal failure receipt. Active cleanup, audit, mapping,
  publication, or classification uncertainty is pending, never rejected;
- the title task guard uses stable before/after census-grade identities around
  the capture, including the process leader and start-time ordering; all count,
  index, ordinal, journal-root, and title-only numeric domains are exact.

The adversarial focused suite passes 163/163. The exact-tree full gate passes
2633/2633 with zero tracked-file violations. At that `-007` freeze boundary,
exact commit and James audit remained pending; the resulting rejection is
recorded below. The artifact is still an offline design
publisher only: no game, `/proc`, ptrace, memory read/write, signal, input,
screenshot, mapping mutation, or terrain/collision experiment occurred.

James **REJECTED** immutable `-007` at exact commit
`ecf809f70af0a94c9d62ba21ce2a18e3ac8b43ab`, tree
`71b294f5a2b89c9262d217bb846c4e1309e92c10`. He independently authenticated
the artifact and source ledger and passed 163/163 focused tests, then produced
accepted counterexamples for restore-before-close and late one-shot creation;
an attach-prefix terminal with unrelated cleanup; copied D1 tree/control
rereads; malformed later command-line bytes; and raw `TypeError` from a
pending action-9 two-control packet.

Fresh immutable `quiet-census-design-008/design.json` is SHA-256
`9140145545fcd03dad674a3a8face8c645679d0e1f86d3a91cc3c60334dae155`.
Analyzer/wrapper/test hashes are `a67ee14f...7e3d`, `cf02db6b...ccb5`, and
`bf351af8...d623`. The correction enforces one-shot → preflight and a closed
cross-action receipt partial order; stage/log → process identity; normal close
→ first clean audit → mapping restore → second clean audit → invariant; and
validation → publication. Failed receipts name the exact next kind/ordinal.
Nonaccepted state is reduced through the authenticated process, attach,
original and last register state; full cleanup validation is mandatory after
attach, while uncertain attach or partial R2o acquisition stays pending.
D2 authenticates recomputed canonical D1 tree bytes, and the aggregate requires
distinct post-D2 rereads for both published controls with exact bytes, stat
identities, and chronology. Terminal/comparison publication additionally
binds source-parent identity and destination reread stat/timestamps. Process
identity decodes the entire strict UTF-8 command line and accepts only the
frozen NUL-separated argument inventory. Nonaccepted two-control inputs reject
with `DesignError`. The focused suite passes 175/175; the first full repository
gate passes 2645/2645 in 916.68 seconds with zero tracked-file violations.
Exact commit, final exact-tree gate, and James re-audit remain pending. No
runtime evidence or terrain/collision conclusion was created.

James **REJECTED** exact `-008` commit
`18591f3424f01eaaa69e0b5430889678df1c09d6`, tree
`ff65061f6cf3e67ea3c774852f39f3c4a9ffe7bf`. Independent verification matched
all frozen hashes, passed 175/175 focused tests, and kept Git clean. The exact
counterexamples were coherent rejected terminals with Right after the first
Return or a stage-mapping source hash unrelated to the authenticated asset
manifest; successful debugger-cleanup or game-close prefixes targeting an
unrelated process before their phase later failed; action-9 failure after a
forged successful timing/control-validation prefix; and arbitrary or
cross-filesystem source-parent device/inode identities in terminal and
comparison publication.

Fresh immutable `quiet-census-design-009/design.json` is SHA-256
`c8c451fae413e2adb93f867723ff865185d700f697089a073029c9d4d13047a1`.
Analyzer/wrapper/test hashes are `1dc00b7f...e09e`, `cf02db6b...ccb5`, and
`a9e99944...7bb`. A shared prefix semantic reducer now validates every
relationship whose receipts are present, including title route,
mapping/asset, complete timing sources, and action-9 outcome/hash. Successful
cleanup and game-close prefix receipts remain identity-bound even when their
phase later fails; phase completion separately controls positive-cleanup
classification. Each publication authenticates a canonical-directory stat
for the exact temporary parent, binds its inode and fsync chronology, and
requires the temporary/source parent/destination parent/destination/reread
(plus terminal tree root/entry) to share one filesystem device. Seventeen new
regressions cover the complete rejection packet; the focused suite passes
192/192 in 444.74 seconds. The first full repository gate passes 2662/2662 in
1102.04 seconds with zero tracked-file violations. Exact commit, final gate,
and James re-audit remain pending. No runtime evidence or terrain/collision
conclusion was created.

James **REJECTED** exact `-009` commit
`f81502bd2cbe4915be21d313d1ea1c411c4cd11e`, tree
`e56942bc2f6fc2b5a0235c5bc469eb05c5c5f9bb`, after independently matching
the frozen hashes, passing 192/192 focused tests in 448.16 seconds, and
leaving Git clean. His coherent rejected packets substituted the title-capture
PID or gameplay-log inode. The complete finding was broader: every
dependency-applicable aggregate relation had to share one conditional reducer,
and `source_parent_stat` time had to be anchored inside terminal publication
and after both comparison post-D2 rereads.

Fresh immutable `quiet-census-design-010/design.json` is SHA-256
`d07d3d5e9e71095080eaf854e1c1822720fb1791ea6b8ae3899dde7b85effd5c`.
Analyzer/wrapper/test hashes are `113fe442...6d13d`, `cf02db6b...ccb5`, and
`e4d7d0b4...baad0`. The correction reduces all authenticated
dependency-applicable accepted/rejected/pending relations through one helper.
Its coherent matrices cover census/guard/process/title/log/asset/mapping,
attach/R2o/continued/stopped-capture/completion, cleanup, invariant, timing,
validation, and publication links. Terminal chronology is validation complete
< outer start <= stat start <= stat complete <= temporary fsync <= rename <=
both parent fsyncs < reread <= outer complete. Comparison chronology places
the ordered D1/D2 post-D2 rereads strictly before source-parent stat. Focused
tests pass 226/226 in 727.47 seconds; the first full gate passes 2696/2696 in
1369.49 seconds with zero tracked-file violations. Exact commit/final gate and
James verdict remain pending. No runtime evidence or terrain/collision
conclusion was created.

James then **REJECTED** exact `-010` commit
`889f105aadb0eb55dfb4677750b186540235163c`, tree
`a93c929f275f58e4a8b55a047e057d6135c62e8f`. His independent audit matched
the 72,752-byte artifact and all published hashes, passed 226/226 focused
tests in 726.14 seconds, retained Vault lint at 608/0/8, and left Git clean.
The nominal fixture itself was contradictory: the executed
`PC/BUGS/bugs.exe` record used device/inode/size/mtime `401/402/403/404`, while
the exact same-path/SHA asset entry used `412/422/3/432`. All terminal states
accepted the composition because no direct or conditional-prefix validator
cross-bound those identities.

Fresh immutable `quiet-census-design-011/design.json` is 73,008 canonical
bytes with SHA-256
`6a8fd3df00406e0ed045b4bd16e94d3255cefdcf025a9d9862cf7e8fbcdc1022`.
Analyzer/wrapper/test hashes are `e8895a9b...1bfd`, `cf02db6b...ccb5`, and
`472cbabd...32f`. The nominal process record now derives its stat tuple from
the exact executable asset entry. A single binding validator requires exact
process path/SHA/device/inode/size/mtime equality with that entry in both the
accepted-control validator and shared conditional prefix reducer. Four
coherent regressions cover the direct, accepted-terminal, rejected-terminal,
and pending-terminal paths: they mutate the process inode, recompute all
dependent process-guard and envelope hashes, and reject specifically on the
process/asset binding. Focused tests pass 229/229 in 740.93 seconds; the first
full repository gate passes 2699/2699 in 1397.31 seconds with zero tracked-file
violations. Exact commit/final gate and James re-audit remain pending. No
runtime evidence or terrain/collision conclusion was created.

James then **ACCEPTED** exact commit
`409cbfbe2b56c271909228d55ea340759b5c6435`, tree
`de4fa877e4aadae12b64e190ba313dca6e9a8d37`, as the
documentation-inclusive R2q `-011` offline design basis. He verified its parent
was rejected `ed2e655`, its diff was exactly three `73,752` → `72,752`
historical `-010` corrections, old wording was absent, and corrected wording
occurred exactly three times. Preserved `-010` measured 72,752 bytes /
`d07d3d5e...effd5c`; `-011` remained 73,008 bytes /
`6a8fd3df...c1022`. Analyzer, tests, wrapper, artifact, namespaces, and
implementation bytes were unchanged. Vault lint remained 608/0/8 and Git was
clean. This ACCEPT certifies only the immutable offline prerequisite; it grants
no runtime authorization and produces no terrain/collision conclusion.

## 2026-08-25 R2q runtime-edge status

The accepted `-011` prerequisite was followed by four James-rejected runtime
edges: `-012` (`ac7e0b1` / `2acfa24`, `7fccf459...b8198`), `-013`
(`c54ed0f` / `cbd2e1b`, `bd0ec48c...b2b28`), `-015` (`6b2c867` /
`bb27926`, `fe8a7712...a6f5`), and `-016` (`5217ca0` / `c0420ca`,
`432a4ede...8933`). Intermediate `-014` (`6ec83b3c...20ff`) was superseded
without a certifying verdict. The exact blocker and gate chronology is retained
in [[2026-08-22 1553 - Codex - R2q offline quiet-census design]].

Candidate `-017` adds a final self-identity-bound completion rename after
receipt durability, full-packet validation, and pre-final tree reconstruction;
post-rename reconstruction remains inside the runtime deadline, and exact
competitor or late-owned valid envelopes are authenticated only as pending.
Frozen `-017` is 102,029 canonical bytes / `c6fe10e2...2fa7`; 261/261 design
and 59/59 runtime tests pass. The full gate passes 2,790/2,790 in 1,843.51
seconds with zero tracked-file violations; exact commit and James verdict
remain pending. The user's unconsumed authority covers only one passive
521-point P0A `/proc` collection without process-memory access, not the broader
R2q ptrace/memory scope. No runtime or scientific result was produced.

## 2026-08-25 R2q `-017` rejection and `-018` correction

James **REJECTED** exact `-017` commit
`2267cc5101c1f82222d72154f94b9899185b417f` / tree
`8166cc4a12e6f7fd02aa280350a7525284d27c08`. The exact 102,029-byte artifact
`c6fe10e2...2fa7` and prior gates authenticated, but the retained quiet-packet
benchmark did not execute either complete accepted-publication path, the
five-second deadline was impossible for nominal complete comparison evidence,
a valid envelope appearing before attempt construction had no accountable
owned attempt, and final-root-fsync failure was promoted to durable/late based
only on readability.

`-018` corrects the evidence boundary without running it. Failure protocols v3
separate `*_complete_envelope_valid` from `*_commit_durability_confirmed`.
Every owned completion attempt records final directory fsync, completion
reread, tree reconstruction, tree verification, and deadline facts. A valid
pre-attempt/losing-rename envelope is non-owned ambiguity; an owned fsync,
reread, or tree uncertainty is durability-uncertain; only a fully verified
envelope that then crosses the final deadline is owned-late and durable. The
stable identity tuple excludes atime but retains device, inode, mode, size,
mtime, and ctime.

Anchored `terminal-publication-benchmark-004/result.json` is 3,233 bytes /
`4cb6ed3491f98aaaea35249c880dffc231b9af0a89462a4708d0a28ecd0d7b2c`.
Across three complete control plus three complete comparison publications,
worst control was 23.167699052 seconds and worst comparison 79.340400010
seconds, leaving 100.659599990 seconds below the prospectively fixed
180-second deadline. It times production construction/validation,
serialization, fsync, exact rereads, tree reconstruction, and final no-replace
completion. Rebuilt deterministic seeds reproduce `67471eb9...f001` and
`42f8d398...e58` after design-source changes.

Frozen `quiet-census-design-018/design.json` is 103,156 bytes /
`435df6253370efcce1308dae2f0e038be0b45665dbd9456415d51bd70130d382`.
Focused gates pass 262/262 design in 1,386.74 seconds and 68/68 runtime tests.
The full gate passes 2,800/2,800 in 2,003.33 seconds with zero tracked-file
violations; exact commit and James re-audit remain pending. The user's retained
authority is still only the passive 521-point P0A `/proc` collection without
process-memory access; it does not authorize this R2q wrapper. No runtime or
terrain/collision result was produced.

## 2026-08-25 R2q `-018` rejection and `-019` provenance correction

James **REJECTED** exact `-018` commit
`7e6a3b0f1a5c801399c19396aecff71646ac5e02` / tree
`2c99beff21048e5a5f42df4ee619e7bf83ee74a7`. He authenticated artifact
`435df625...d382`, benchmark `4cb6ed34...d7b2c`, all reported hashes,
`validate_published_design`, 68/68 runtime tests, Git objects, and cleanliness.
Three evidence defects remained: `ambiguous-owned-late-envelope` derived from
stage flags without retaining the actual deadline exception; the declared
30-second failure-recording budget did not span completed-action, ordinary, or
comparison failure accounting; and benchmark `-004` lacked an exact ledger of
the production design/runtime bytes executed during timing.

`-019` stores an exact `publication-deadline-exceeded` receipt with deadline,
observed time, and `final-acceptance-boundary-reread` checkpoint. Runtime
requires equality with the chained `PublicationDeadlineError`; validators bind
it to the completion deadline, require `observed > deadline`, and cross-bind
rename and outer-failure chronology for control and comparison. The old broad
30-second claim is removed: only failed/skipped durable journal transitions
retain one absolute 30-second deadline, while end-to-end failure accounting is
explicitly unbounded.

The benchmark source was first committed clean as `3fe4833` / tree `5953ebf`.
Benchmark `terminal-publication-benchmark-005/result.json` then recorded that
identity and exact five-file byte/hash ledger before and after all trials. It is
4,563 bytes / `645376228b51dd1cfeac50e77b369f6ca1a153f0a972303dc4e6e9a5bf5c28fa`;
the final tracked data anchor is 1,363 bytes / `e6b542a2...e4de`; source-ledger
hash is `01abbe48...341f`. Worst complete control/comparison paths were
22.983197250/78.945117065 seconds, leaving 101.054882935 seconds under 180.

Frozen `quiet-census-design-019/design.json` is 104,745 bytes /
`f3d985a51d60adee3a63545d7209c7e214e58a7788f2dffe24b7fd959f5aeadf`.
Focused gates pass 263/263 design in 1,545.22 seconds and 68/68 runtime tests.
The first full gate passes 2,801/2,801 in 2,205.27 seconds with zero tracked-
file violations; exact final commit and James re-audit remain pending. No live
operation or terrain/collision result was produced; passive P0A authority does
not authorize R2q.

## 2026-08-25 R2q `-019` rejection and `-020` outer-failure correction

James **REJECTED** exact `-019` commit `8e1b98958382886f4df9f39dc5046a9259ac0279`
/ tree `c3334e33f8550c478a10a5a17b7747138e92fa1f`. He authenticated the artifact,
benchmark, anchor, source ledger, Git integrity/cleanliness, all three prior
corrections, and runtime tests. He then reproduced two new certifying defects:
owned final-deadline attempts accepted an unrelated outer `DesignError` and
impossible comparison phase, while non-string `stage` could escape as raw
`TypeError`.

`-020` failure protocols v5 cross-bind final-deadline attempts to outer
`R2qRuntimeError` and the exact production boundary message. Comparison must
use `commit-marker`; control observation must precede failure-accounting start,
and comparison observation must follow comparison start. Both must precede
outer completion. `stage` is type-checked as an exact string before closed-set
lookup. Direct and full control/comparison regressions cover forged exception,
message, phase, code, chronology, and list/dict/integer/Boolean/null stages.

Immutable source commit `9e4ccf724f61ec0c4c22a341654c1d8f40de3a99` / tree
`f2502d873aa60bcf2d848cf169292835a4f36aab` binds source ledger
`0f184368...bcf27`. Benchmark `-006` is 4,563 bytes / `72373103...e95b`;
its tracked 1,363-byte anchor is `53c3f811...b7c3`. Worst complete
control/comparison paths are 23.035894094/78.864340257 seconds, leaving
101.135659743 seconds below 180.

Frozen `quiet-census-design-020/design.json` is 105,429 bytes /
`462b882d24922fa86520b9811f18f2ade9ca5dc154827a4f8d8667283966061a`.
`validate_published_design` and the complete 331/331 R2q gate pass, the latter
in 1,799.86 seconds. The first full repository gate passes 2,801/2,801 in
2,458.12 seconds and the documentation-complete exact-tree gate passes
2,801/2,801 in 2,457.27 seconds, both with zero tracked-file violations.

James **ACCEPTED** exact commit
`4635a5320ba48f87ee26923b3f31ce697d74e791` / tree
`fa5d63dacef3b98799927d016669c338b90aa5c0`. His independent audit confirmed
Git integrity and cleanliness; the source, ledger, artifact, benchmark, and
anchor identities; both validators; the real deadline exception chain; closed
rejection of forged outer semantics and malformed stage values; 68/68 runtime
tests; and both coherent strengthened terminal arms. This certifies the
immutable offline R2q design/runtime edge as publication-grade. No live
operation or terrain/collision result was produced; passive P0A authority does
not authorize R2q.

## Links

- [[EXP-20260820-004 - R2o completed-present state calibration protocol]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Known Unknowns#KU-079 - The render-geometry command grammar (the LEVEL.DAT draw-command stream)|KU-079]]
- [[Decision Log#DEC-188 - Preserve P0A-AH-001 as pending after pre-collection route and close failures|DEC-188]]
- [[Decision Log#DEC-189 - Retire the consumed P0A wrapper and correct offline runtime provenance|DEC-189]]
- [[Decision Log#DEC-190 - Require exact integer domains and complete X peer credentials|DEC-190]]
- [[Decision Log#DEC-191 - Share exact task partitions and reject numeric aliases|DEC-191]]
- [[Decision Log#DEC-192 - Separate proved direct navigation from P0B passive collection|DEC-192]]
- [[Decision Log#DEC-193 - Preserve failed recovery and close only the residual environment|DEC-193]]
- [[Decision Log#DEC-199 - Bind the executed process to the exact executable asset identity|DEC-199]]
- [[Decision Log#DEC-200 - Make a self-bound completion file the final R2q acceptance boundary|DEC-200]]
- [[Decision Log#DEC-201 - Separate R2q envelope validity from durability and benchmark complete publication|DEC-201]]
- [[Decision Log#DEC-202 - Bind R2q late outcomes and benchmark execution provenance|DEC-202]]
- [[Decision Log#DEC-203 - Cross-bind R2q owned deadline attempts to production failure semantics|DEC-203]]
- [[Current State]]

## 2026-08-26 P0D consumed marker and corrected P0E candidate

James rejected the initial P0D pre-freeze packet for six blockers: its attempt
marker followed fallible import/configuration work; it trusted invocation-time
source hashes and omitted executed local imports; a terminal directory could
remain after a final fsync failure; stage and restore used unlink/symlink gaps;
the final owned-runtime census preceded audit 02 and could become stale; and
the actual Wine host image was not frozen separately. He otherwise accepted
the direct Level01 route, exact 521-point grammar, passive-only scope,
historical exclusions, and normal-close-only boundary.

A legacy wrapper test then used `runpy(..., "__main__")` against the production
path. It created `evidence/P0D-AH-001.attempted` and stopped because the
activation anchor was absent. The marker is a 30-byte mode-0600 regular file,
device 54, inode 9281337, created 2026-08-26 11:52:53.125290792 -0400, with
SHA-256 `89883723f4cc51269caae0d46a13cba57a14ae58056c4826d60eaa18edc23f19`
and exact bytes `ablpc-p0d-attempt-consumed-v1\n`. It is intentionally retained
and P0D is not reusable. No launcher, game, input, mapping mutation, `/proc`
lifecycle sample, memory operation, or signal occurred; `make session-audit`
remained exactly clear.

Fresh P0E protocol `ablpc-r2p-p0e-passive-lifecycle-v1` corrects all six
findings. The bootstrap performs the exclusive open before any project import
or preflight, and failure at every subsequent write/fsync/stat/import/source/
config/path/mkdir/reread boundary leaves the arm consumed. The activation
freezer binds exact committed Git blobs and SHA-256 values for
`ablpc/__init__.py`, `anm.py`, `level_dat.py`, `r2p_p0e.py`,
`r2p_passive_core.py`, `auto_hardware_mod.py`, `make-auto-hardware`,
`play-pristine.sh`, and the P0E wrapper. The wrapper also requires the tracked
anchor's exact committed HEAD bytes before importing P0E.

The Wine host is independently frozen as
`/usr/lib64/wine-wow64/wine/x86_64-unix/wine-preloader`, SHA-256
`3adeb326d09b0a1fb0027c8eb8710978d4ac9593eaf29fb497168b239331734f`,
size 18072, device 38, inode 3825178, mode 0755, mtime
1768608000000000000 ns. Stage and restore each authenticate a same-parent
temporary symlink, reauthenticate both old and prepared identities, atomically
replace `Y:`, fsync its parent, and perform two stable rereads. Immediately
before restore, P0E repeats both its owned group/session census and a complete
`game-session` audit; either errors closed. Publication never creates
accepted/rejected and can end only in `published-unverified`, where James must
perform post-run classification.

P0E also authenticates the consumed P0D marker, P0A stage/pending/`R:`, and all
five P0B trees before/after. Focused tests pass 519/519, including every
James-requested failure boundary. The exact source tree passed 3320 tests and
committed as `01902e0c7bff99bc17f10e9c21c2b4082112a14e` / tree
`aa80c5a2eb1ed49433cbb7b481f72f7d6ef5299b`. The generated canonical activation
anchor has SHA-256
`8ea16668f6da72d888ff35ce9cf9f59239716b86488b709cfc893af19ebddcbe`.
P0E is unconsumed and all P0E production paths are absent. Final gate/commit
and James acceptance of that exact final revision remain required. No
lifecycle or terrain/collision result follows.

## 2026-08-26 first P0E exact-tree rejection and correction

James **REJECTED** exact `b77775397bead19e6e31a9a3d97d71662b73ff14` /
tree `85799bef2374b762a52f9c5122e7758b973cad35`. His independent 519/519
focused run and source/host checks confirmed the six original P0D blockers
were materially closed. He nevertheless reproduced a byte-identical P0D
marker replacement that validated under its new coherent inode and packet
validation at both an arbitrary copied root and exact zero-receipt
published-unverified.

The corrected candidate freezes P0D's documented device 54, inode 9281337,
and mtime 1787759573125290792 ns in the plan and pre/post validation. It admits
only the four exact production packet roots, only publisher-reachable receipt
prefixes in pending/published-unverified, complete publication evidence in a
terminal, and only the matching validator class for accepted/rejected. Direct
regressions cover James's three bypasses, each physical-field mutation, every
reachable prefix, and wrong-class terminals. Focused tests pass 542/542;
James's independent 106-case matrix also passes and he returned
`ACCEPTABLE-FOR-FREEZE`. The source-phase full gate passes 3343 tests in
2481.11 seconds with 0 tracked-file violations. Corrected source
`c7bdd6c8b15c3697cc5ffeeea0a51e79d66ca60a` / tree
`e0a5fea3d0412bed8d674e4fd916705e328dd76c` is bound by activation anchor
SHA-256 `7342d729cd91214bc820d19fa70e93a4b18cc312c1acd6548cda49167ad08c5d`.
No live operation had occurred and P0E was still unconsumed; the final full gate,
commit, and James exact-tree ACCEPT remain prerequisites.

## 2026-08-26 sole P0E run - collection accepted, cleanup pending

The final full gate passed 3343/3343 in 2472.58 seconds with 0 tracked-file
violations. James **ACCEPTED** clean exact `b1896e1` / `a696e48`, and the fresh
pre-launch audit was exactly clear. The one allowed argument-free invocation
consumed P0E marker `b3638ebd...f5235`, validated the PC auto-hardware
Anthill/Level01 route, and completed collection `9ed7d8e...456b0`.

All 521 samples meet the 20 ms schedule and metadata/window/process guards.
One identity `(310752,9973602)` is absent sequences 0–26, first captured at 27,
and present continuously through 520. No removal, reuse, short-lived identity,
enumeration instability, metadata error, or acquisition/title failure occurs.
James independently **ACCEPTED the collection level only**. The addition is in
the game TGID and reproduces the earlier 16→17 topology, but role/creator and
any DirectSound interpretation remain inference; no terrain/collision claim
follows.

Alt+F4 delivery authenticated but did not terminate the game. The 89-poll
clearance receipt retained nine identities; audit 02 retained seven
unattributed processes plus sink `ablpc_mute_310283` and was nonclear. The
protocol omitted audit-02b/audit-03/immediate-clear/Y-restore, left `Y:` staged,
and retained the packet in pending with no publication root. Disposition
`215a99bb...79e7` records all prohibited actions null and cleanup failure.
P0E is consumed and cannot retry. Agent cleanup or mapping restoration needs
fresh explicit authority plus a separate frozen/James-accepted recovery.

## 2026-08-26 P0E-R1 additive recovery source freeze

The user explicitly authorized recovery of the consumed P0E residue. The
separate `ablpc-r2p-p0e-authorized-residual-recovery-v1` protocol preserves the
33-name original pending packet and accepts only descriptor-bound append to
`launch.stdout`/`launch.stderr`. Its wrapper consumes a fresh one-shot marker
before project import and closes Git/environment/interpreter/source authority.
It can act only on the 12 frozen original process identities after exact
reauthentication, can unload only module `536870916` when the exact sink is
present, and can restore `Y:` only after repeated exact-clear gates. It has no
process-memory, ptrace, debugger, screenshot, save-state, or game-input path.

James rejected the first source candidate because a corrupt stage snapshot
could precede signals, a failed envelope could validate forged retained
receipts, and physical publication-parent/root binding was incomplete. The
correction made the coherent packet snapshot a pre-action gate, semantically
validated every retained failure prefix, and bound all renames through
authenticated directory descriptors. James then found one durability gap: if
pending→published succeeded but its pending-parent fsync failed, reclassification
could move published→failed without repairing the first rename's source parent.

The exact corrected candidate authenticates retained `publication.json`,
records its hash and three publication bits plus both predecessor-parent
identities, fsync-repairs the exact pending parent before any failure move, and
validates repair chronology. A one-shot injected failure now repairs and
validates; a persistent repair failure leaves explicit uncertainty in
published-unverified and cannot create a complete failed terminal. Exact
hashes are `a1a854cf...bb024` (module), `c14ed69a...f951` (wrapper),
`fafc5acc...30b0` (freezer), and `c58068ed...299f` (tests). Focused tests pass
101/101; combined P0E/passive/lifecycle tests pass 809/809. James independently
passed 101/101 and returned `ACCEPTABLE-FOR-SOURCE-FREEZE`. The source-phase
full repository gate then passed 3,444/3,444 in 2,500.62 seconds with 0
tracked-file violations.

At the source-freeze checkpoint no recovery marker or packet root existed and
no live action had occurred. A read-only audit at 18:59 found only PIDs
310463/310509, no null sink, no open
session, and `clean:false`; direct census agrees. Original P0E tree
`53aa3b5a...a396c` normalizes to frozen `edcd8269...031` after excluding the
allowed `launch.stderr` append (11,347→11,706 bytes). Stage/`Y:` remained exact
`b9b26839...df44a`; `R:` remained P0A. The activation/docs commit, exact James
ACCEPT, and fresh accounted audit were then required before the sole wrapper
invocation; their later disposition is recorded below. This recovery cannot
classify P0E and provides no terrain/collision result or R2q authority.

Source is committed immutably as
`dc2481be6479333878774dd9194cb02d9f7912f9` / tree
`ba664464977ef600076b666a204f940017a1fc88`. The dedicated exclusive freezer
produced a 2,501-byte canonical activation anchor, SHA-256
`df1def843f3d0c51f2de61c5d6f544390101de660e74e69be4405b145a103556`,
which binds the 12-file executed local closure to that earlier source commit.
The anchor was not live authority; it then required a committed clean tree and
exact James acceptance, which were later satisfied as recorded below.

## 2026-08-26 sole P0E-R1 run - residuals removed, recovery failed

The documentation-inclusive activation tree passed `make check` with
3,444/3,444 tests in 2,481.05 seconds and 0 tracked-file violations, then
committed as `3aa9127db4312338a090ae1e096326b020b8e7f0` / tree
`1be8a4a5baef013a3f4686e1d5c20b0476c50419`. James independently validated
clean Git, the tracked activation/source closure, 101/101 focused tests, absent
marker/namespaces, and all action/durability bounds. He **ACCEPTED** exactly one
argument-free `/usr/bin/python3.14 -I scripts/r2p-recover-p0e-pending.py`
invocation after a fresh accounted audit. That audit contained only exact
frozen residuals 310463/310509, with no sink or open session.

The sole invocation consumed marker SHA-256 `2e8a0f3a...51d94`. Events 0–31
record an exact initial census, authenticated TERM to each residual, 23 TERM
polls spanning the full five-second budget with both still exact, fresh exact
pre-KILL identities, and authenticated KILL to each. Both then disappeared
between the first two post-KILL census reads. Because those rows differed,
`require_census_stable` raised `residual census was unstable` before a poll or
`pending-after-kill.json` could be recorded. No sink action or mapping action
occurred.

The exact failed envelope validates in production. Its 10-entry tree is
`0be8f7be1f2da2a417774ed702db2c803b94fd0a525d9855cd3c679216543f89`;
the 32-event prefix is `cad13b38...58056`; failure, failure-publication, and
failure-manifest hashes are `4f64f610...18d46f`, `d16e2e95...d8376e`, and
`82fb238e...f23316`. Pending→failed publication renamed once and fsynced both
parents. The failure snapshot records all 12 frozen identities and sink absent.
A post-action session audit is independently exactly clean.

James returned **ACCEPT-AS-FAILED-EVIDENCE**: the signals support removal of
the two residuals, but the missing two-consecutive-poll gate means this is not
a successful recovery. Original P0E remains current/normalized trees
`53aa3b5a...a396c` / `edcd8269...031`; `Y:` remains P0E stage
`b9b26839...df44a`; `R:` remains P0A. P0E-R1 is consumed with no retry. A new
explicitly authorized and frozen successor is required to restore `Y:`. No
P0E classification, R2q, task-role, terrain, or collision result follows.

## 2026-08-27 Y-only restoration successor checkpoint

The user supplied fresh authority for exactly one atomic restoration of staged
`Y:` to retail. A dedicated successor is now implemented and banked as WIP,
not activated or run. It preserves original P0E/P0E-R1 evidence and `R:`, has
no process control/input/memory/sink path, and can publish success or failure
only as unverified evidence for James.

Exact hashes are `49c90537...53f3` (module), `9c9dbb28...a80` (wrapper),
`640aefb1...42bc` (freezer), and `92ae90bb...3a3` (tests). The focused suite
passes 96/96; combined P0E/P0E-R1/Y-restoration tests pass 357/357. James's
round-26 verdict found a missing cleanup-repair completion lower bound and
uncontrolled repair-error text. The current successor corrects both with
coherent regressions. Round 27 confirmed those fixes and 357/357 combined
tests, then rejected missing/ancient mapping-repair provenance on a coherent
`mapping-fsync-once` packet. No activation anchor or attempt marker exists, no
mutating live action occurred, and no lifecycle, task-role, terrain, or
collision result follows. One preliminary James fixture unexpectedly called
the production read-only session audit and made no mutation. Full handoff is in
[[2026-08-27 0816 - Codex - P0E Y restoration hard-truth checkpoint]].

## 2026-08-27 Y-only restoration source and activation freeze

James rounds 28-34 successively rejected inverse mapping-provenance invention,
unfinished journal and prefix chronology gaps, contradictory parent-durability
state, inverse cleanup-provenance invention, event-absent cleanup ambiguity,
and reversed joint repair ordering. The corrected successor now cross-binds
mapping and cleanup provenance to retained durable events in both directions,
conservatively repairs unfinished events, covers the full retained prefix,
binds nested/top-level durability state, and orders mapping repair no later
than cleanup repair. Coherent fixtures cover mapping-fsync-once omission/zero,
unfinished journals, inverse provenance, durability contradictions, cleanup
omission/invention, and joint reordering.

James round 34 accepted exact module `541fbe59...3d57`, unchanged wrapper
`9c9dbb28...ea80`, unchanged freezer `640aefb1...42bc`, and tests
`bad67fe1...e6111`. The source passes 98/98 focused, 359/359 combined,
741/741 broad P0E, and 3,542/3,542 full-repository tests. Source commit
`1964eec` / tree `f0afa1a` is bound by activation anchor
`95e632dc...d8307`.

This remains a pre-action freeze. The attempt marker is absent, the wrapper
has not run, and `Y:` remains the exact P0E stage. No lifecycle, task-role,
terrain, collision, or R2q result follows. See
[[2026-08-27 1457 - Codex - P0E Y restoration source and activation freeze]].

## 2026-08-28 recovery3 source and activation freeze

Consumed YR3 is preserved exactly: marker `7191e193...e43`, placeholder
`0c0a027d...f152`, failed tree `69daa4a7...0589`, empty events, idle reducer,
unchanged mappings, and absent action/scratch names. Distinct YR4 corrects the
multiline PipeWire parser and cross-boot chronology, physically reauthenticates
all non-Y predecessor state across the stage/retail transition, and exact-binds
the duplicate YR1/YR2 histories. James rounds 39/40 accepted the corrected
source and fresh authority.

The restoration/broad/full gates pass 202/845/3,646. Source `9a815a3` /
`27b23a` is bound by 119,469-byte activation `111fbc78...6fcb` over 25 exact
files plus the full predecessor closure. This is pre-action provenance only:
the YR4 marker and namespaces are absent, the wrapper has not run, `Y:` remains
staged, and `R:` remains P0A. Final commit, James clean-tree acceptance, and a
fresh clear audit remain mandatory. No lifecycle classification, R2q result,
terrain, or collision conclusion follows. See
[[2026-08-28 1704 - Codex - P0E Y restoration recovery3 activation freeze]].

## 2026-08-28 recovery3 successful Y restoration

After activation commit `29ed6d9` / `4494ec8`, James round-42 exact one-action
acceptance, and a fresh exactly clear audit, the sole YR4 wrapper exited 0.
Marker `b109d6ca...c5e00` and 28-entry packet tree `9a4979ca...e46c6` validate
one entered-and-returned stage-to-retail exchange, Y-parent/retirement
durability, retained stage quarantine, unchanged P0A `R:`, and preserved
predecessor evidence. The immediate post-action audit is exactly clear.

James round 43 accepts this only as published-unverified mapping success with
zero runtime/input/signal/sink/process-memory actions. It does not classify the
persistent task or provide R2q, terrain, collision, render, material,
visibility, causality, or future-action evidence. R2q runtime remains subject
to separate fresh authority. See
[[2026-08-28 1704 - Codex - P0E Y restoration recovery3 activation freeze]].

## 2026-08-30 R2q round-91 through `-022` activation

The banked round-91 source was restored without dropping stash object
`76db1c9ee1ffffce52cea6aee591c24ab6a1c39a`. It authenticates full-frame
pre/post SHA-256, byte count, mtime/ctime, and timing around one-shot file fsync
and rejects James's corruption→fsync→restore-without-fsync reproduction.
James accepted round 91; the source was frozen at `eececd7`. Fresh
benchmark-007 preparation and continuity correction were frozen at `40bee21`
and `ec46c9a`; result `69c64794...27d07` accepted and produced immutable
design-021 `5891e93f...13fac`.

The first full post-activation gate reported 3,764 passed, 9 failed, and 13
setup errors. Every defect was a stale test/environment assumption exposed by
the new activation state: current retail-Y inode, fresh namespace serial,
renamed link-receipt contract, mandatory predecessor closure, and journaled
mapping projection. Because the corrected test and runtime module are timed
source, `-021` was preserved rather than overwritten.

James round 96 accepted successor source `3998111` / `0c61a85`. It binds all
bytes of `-021` as the prior design, separately authenticates the failed `-020`
operator/physical closure, and advances every prospective runtime identity to
`-022`. Benchmark-008 is 4,562 bytes / `eb930b77...9cfd9`; its final anchor is
1,363 bytes / `1049049c...b7a1`, source ledger `6f0c6ac2...37a9`, and worst
control/comparison totals 25.740025121/80.520710670 seconds. Activated
design-022 is 8,061,582 bytes / `b79f63b0...e6b72` and validates as runtime
unauthorized. The repaired 11-node tranche, 157 runtime/freezer tests, and
3,786-test full gate all pass; the full gate took 3,276.94 seconds and found
zero tracked-file violations.

No game, restoration wrapper, R2q wrapper, live R2q `/proc` census, ptrace,
process-memory, input, signal, screenshot, save-state, or stage-mapping action
occurred. This adds no terrain/collision result and grants no runtime authority.

## 2026-08-31 R2q `-023` preservation and `-024` activation

Source `fbba31f` / tree `480abf0`, benchmark-009 4,563 bytes /
`95478c34...9a38b`, and immutable design-023 12,035,411 bytes /
`be7cf41f...08cd3c` are preserved. The first activation suite exposed only
offline source/fixture problems: incomplete restored-path authority in
terminal and emergency projections, stale D2 continuity authority, a wrong
phase-receipt access, incoherent mapping-mutation identity, and a genuine
maximum-shape continuity frame above the old 256 MiB raw fallback ceiling.

Fresh `-024` fixes those cases, advances prospective identities, and uses
one-shot frame protocol v6 with a 320 MiB raw ceiling while retaining the
128 MiB stored-data reservation. James accepted exact staged diff
`86b737d4...e8976`; source is committed at `022f739` / `9d78651`.
Benchmark-010 is 4,563 bytes / `592ac4a7...d3e7`, final anchor 1,363 bytes /
`10264047...fb7`, and worst comparison 79.652494057 seconds. Immutable
design-024 is 17,336,651 bytes / `321eb8c6...2288` and validates as
runtime-unauthorized. Runtime tests pass 160/160; full `make check` passes
3,843/3,843 in 4,000.96 seconds with zero tracked-file violations.

No game, runtime/restoration wrapper, `/proc` census, ptrace, process-memory,
input, signal, screenshot, save-state, or mapping action occurred. The
experiment still has no accepted quiet-census, task-role, terrain, collision,
render, material, visibility, causality, or no-effect result. See
[[2026-08-31 0648 - Codex - R2q 024 hard-truth activation freeze]].

## 2026-08-31 R2q-024 failure/recovery and `-025` activation

The sole authorized `-024` D1 arm failed during `stage-and-launch`. Exact
failure receipt `b188a953...c5fe` records `R2q process maps read binding
mismatch`; later title/gameplay, quiet-census, debugger, acquisition, and
comparison phases did not produce an accepted result. The arm is consumed and
cannot retry. After identity-guarded cleanup, a separately frozen and
authorized mapping-only recovery ran exactly once. James accepts its 28-entry
tree `afacab0a...90bfa`, result `14e29a9e...28a9`, and mapping receipt
`ed20963a...033` as one parent-fsynced stable-reread D1-stage-to-retail Y
exchange, zero rollback, P0A R unchanged, and zero runtime/input/signal/sink/
process-memory action. The active/retired Y inodes are `9733762`/`9731469`;
R remains inode `9054047`. This is environment recovery, not science.

The larger v3 predecessor closure then invalidated `-024`'s 320 MiB raw and
128 MiB data bounds. Maximum valid failure-material accounts measure
379,306,355 raw / 153,758,493 compressed bytes; maximum valid continuity
accounts measure 428,420,338 / 166,728,453 bytes. Fresh `-025` advances all
prospective namespaces and uses `ablpc-r2q-one-shot-authority-v7` with 448 MiB
raw, 192 MiB data, and a 201,330,816-byte frame. James independently accepted
source diff `c0114ada...fd3c`; source commit/tree are `d23ece3` / `8492bcb`.

Three clean-source benchmark-011 trials pass. The result is 4,568 bytes /
`9ec2ec6a...d79`; final 1,364-byte anchor is `9997ac75...588`; worst
control/comparison totals are 37.446760533/128.966455183 seconds, leaving
51.033544817 seconds under 180 seconds. The argument-free offline freezer
published immutable design-025, 25,557,671 canonical bytes /
`d25acc8c...34a9`, outcome
`offline-r2q-design-frozen-runtime-unauthorized`. Its canonical 24,558,434-byte
predecessor closure is `c71147ff...884e`; its 5,966-byte activation manifest is
`6bfe5747...2451`. Direct published validation passes.

The first full gate found one failure and 13 setup errors after 3,864 passes,
all from two historical recovery tests that treated earlier retail-Y inode
values as exhaustive. The bounded correction recognizes current inode
`9733762` only under the full accepted recovery closure. Diff
`b4910678...7d4a`, 48 affected tests, and James's independent 87-test tranche
pass. A second unchanged full run was environmentally invalidated at 90% by
`Errno 122` because completed prior pytest scratch remained in `/tmp`: 3,658
passed, 178 failed, and 42 errors. After deleting only completed scratch, the
third unchanged run passes 3,878/3,878 in 6,571.36 seconds with zero tracked-
file violations.

No `-025` runtime occurred. EXP-005 still has no accepted quiet census,
persistent-task role, render grammar, terrain/ground source, collision linkage,
material, visibility, causality, no-effect, or retail-executable result.
KU-079, KU-080, and KU-081 remain open. See
[[2026-08-31 1849 - Codex - R2q 025 activation freeze]].

## 2026-09-01 R2q-025 failed run and mapping recovery

The sole R2q-025 D1 arm consumed its authority and failed in
`stage-and-launch`: bounded game-process maps did not converge. Terminal
packet `d1a33753...fa04` is 118,724,996 bytes and remains pending. It records
no accepted quiet census, debugger capture, stopped memory, screenshot batch,
D2 comparison, or scientific result. Exact identity-guarded cleanup removed
only matching survivors and ended with a clear audit; it does not authorize a
retry.

The distinct Y-only recovery source is `3ac52dc` / `675d5b1`, bound by
activation `5ff648a2...2e90` and authority `e9e1710a...922`. Its wrapper ran
exactly once. James returned `ACCEPT EVIDENCE` for 28-entry packet tree
`0b0aa411...f4d2b`, mapping receipt `f37158da...c383`, and result
`243f8966...22a4`: one exchange, zero rollback, parent fsync, stable reread,
retail Y inode `9773754`, retired D1 inode `9770116`, unchanged P0A R inode
`9054047`, and zero runtime/input/signal/sink/process-memory action.

Benchmark-011 source remains exact at `c556df93...5155`. Clean checkpoint
`c851110` received James `ACCEPT`; the strict success validator passes without
projection, and full `make check` passes 3,905/3,905 in 6,213.97 seconds with
zero tracked-file violations. The final session audit is clear.

This is failed pre-science evidence plus environment recovery, not a terrain/
collision result. KU-079, KU-080, and KU-081 remain open. A fresh successor
must bind this complete closure and solve process-map convergence offline
before any new runtime authority. See
[[2026-09-01 0317 - Codex - R2q 025 failed-run mapping recovery]].

## 2026-09-01 R2q-026 convergence correction and activation freeze

The exact R2q-025 convergence failure completed all eight attempts in only
417,319,810 ns because each cohort waited 50 ms. Fresh protocol v2 keeps eight
triplicate full-byte cohorts but waits 625 ms per cohort and accepts a
nonconvergence result only when the five-second deadline has actually elapsed.
The exact failed-025 trace is a negative fixture and cannot claim current
nonconvergence.

The successor binds all failed-025 and mapping-recovery-025 artifacts in a
36,241,115-byte v4 predecessor closure /
`f3e777b25d3366e2e02eac467d891b2a8490d9777fb3427cd49d2f2f6c928d2e`.
Finalized maximum-shape capacity tests require protocol v8's 640 MiB raw and
256 MiB stored bounds; the derived one-shot frame is 268,439,680 bytes.

James accepted source `812b6d0` / `37353bf`. Three clean-source benchmark-012
trials produced 4,563-byte result `afc246e8...75ae3`; worst control/comparison
totals are 23.367732980/80.813913839 seconds, leaving 99.186086161 seconds
below 180 seconds. Final anchor-012 is 1,364 bytes / `408812eb...3638`.
Immutable design-026 is 37,673,716 bytes / `a7eb768b...2d7b`, with activation
manifest `a1f56b67...be8d`, and validates as runtime-unauthorized.

Finalized design/runtime suites pass 350/350 and 160/160. A first full gate
found one historical consumed-R2q-025 test recapturing the predecessor through
active `-026`; James accepted the test-only exact-activation correction, which
does not weaken the production validator. The complete rerun passes
3,908/3,908 in 4,632.89 seconds with zero tracked-file violations.

No live action occurred. This freeze supplies no quiet-census, persistent-task,
render, terrain, collision, material, visibility, causality, no-effect, or
retail-executable result. KU-079, KU-080, and KU-081 remain open. See
[[2026-09-01 1524 - Codex - R2q 026 convergence and activation freeze]].

## 2026-09-01 R2q-026 failed run and mapping recovery

The sole R2q-026 D1 arm consumed its authority and failed before Level01
navigation. The corrected convergence protocol did reach its intended window;
the new failure was `game executable provenance is not exact`. Exact
reproduction showed that `/proc/<pid>/maps` reported device `00:24`
(`0/36`) inside the process mount namespace while host `stat()` reported minor
`38` for the same exact preloader path/inode/SHA-256. The current validator
incorrectly treated those namespace-relative device numbers as directly
comparable. The terminal packet is 170,486,748 bytes /
`741fbd362c9c2f5d15c842e2b5deb34bedc6cf73d271e8f14b7df59429c2b14e`.
The title, quiet census, ptrace acquisition, stopped ranges, 38 PNGs, D2, and
comparison did not occur.

Exact identity cleanup used the seven frozen PID/start-tick pairs, with KILL
only for surviving `1801271`, `1801424`, and `1801463`; the sink module was
already absent and the audit became exactly clear. James accepted cleanup,
failed evidence, and root cause.

The separate mapping-only successor is source-frozen at `9cf28fa` / `746e9d4`,
activation `16bbcfcc...de1d`, and authority `d1150b39...4cfe`. Its sole
invocation published 28-entry tree `264ecdac...780c`, mapping receipt
`be0a3633...80c4`, and result `d81c6f2b...c142`: one exchange, zero rollback,
parent fsync, stable reread, retail Y inode `9998033`, retired D1 inode
`9997058`, unchanged P0A R inode `9054047`, and zero runtime/input/signal/
sink/process-memory actions. James accepted the evidence as mapping recovery
only. Focused post-action coverage passes 143/143 and complete `make check`
passes 3,937/3,937 in 4,792.33 seconds.

No terrain/collision result follows. KU-079, KU-080, and KU-081 remain open.
Any successor must be fresh and must correct the cross-mount-namespace device
comparison offline before seeking new runtime authority. See
[[2026-09-01 1718 - Codex - R2q 026 failed-run mapping recovery]].

## 2026-09-04 R2q-028 pre-lock disposition and R2q-032 activation bank

The authorized R2q-028 entrypoint was invoked once but stopped before one-shot
consumption: remount-only device fields made its immutable predecessor closure
differ while every other compared field remained exact. Receipt
`quiet-census-design-028/prelock-invocation-rejection.json` is
`322cb1b1...5cb`; James accepted the pre-lock failure disposition. It contains
zero launches, mapping actions, process-memory actions, and runtime paths.

The offline correction chain is retained rather than rewritten:

- design-029 `6cd3d734...3da0` plus finalization rejection
  `694d0f7f...7f20` records literal-device historical-test failures;
- R2q-030 has no design because its only freezer call rejected historical
  design-029 byte drift; activation rejection is `440a7e9b...2403`;
- design-031 `7d826b13...c554` plus finalization rejection
  `f4481e28...aa2` records one stale active mapping test and two Python 3.14
  teardown errors caused by a global `os.fstat` mock.

R2q-032 delegates real file descriptors to the real `os.fstat`, advances the
active mapping namespace to `retail-032` / `D2-AH-032`, preserves exact
historical dispatch, and rejects appearance of unused R2q-031 paths. James
accepted source `45ae9539d200786064309ffb9a249e526de0897d` / tree
`2292c1a419212fe7f14c3b846e939c690ee830d5`. The sole benchmark-018 is
5,023 bytes / `c93ea507...7bb9` and leaves 96.774281435 seconds below the
180-second ceiling. Anchor-018 is `d6951e11...ab70`. The sole design freezer
published 204,641,846-byte design-032 `0604d37d...b2b8`, whose 6,332-byte
activation manifest is `d3dc03ae...f402`; James accepted activation at
`b6abcb2` / `e65362d`.

Runtime/freezer 163/163, predecessor/one-shot/continuity 124/124, post-anchor
17/17, and exact capacity 1/1 pass. The full repository gate is unresolved:
its attempt reached 79%, showed one failure marker, and was interrupted before
pytest produced a summary or traceback. This is neither a pass nor a
reproducible rejection. Scratch is absent and the session audit is clear.

No game, restoration/R2q wrapper, live census, ptrace, process-memory, input,
signal, screenshot, save-state, or mapping action occurred after the R2q-028
pre-lock stop. The experiment remains pending and has no terrain/collision or
persistent-task result. See
[[2026-09-04 1711 - Codex - R2q 032 activation bank and incomplete final gate]].
