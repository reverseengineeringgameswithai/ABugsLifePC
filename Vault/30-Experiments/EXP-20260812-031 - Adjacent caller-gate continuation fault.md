---
type: experiment
id: EXP-20260812-031
date: 2026-08-12
question: Is the reproduced caller-gate continuation fault confined to exact address 0x0044D79A?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora, Wine, GDB harness, windowed muted Gamescope
environment_version: wine-11.0-staging; gdb-17.1-6.fc44; gamescope-3.16.25-1.fc44
working_directory: /home/dev/ABLPC/work/copies/BUGS_PC-full-disc/PC/BUGS
configuration: Fresh unchanged Training run; Direct3D hardware 640x480x16; one adjacent hardware breakpoint; schema-2 required survival receipt
artifacts:
  - dynamic/wine/RUN-GDB-20260812-221224/metadata.json
  - dynamic/wine/RUN-GDB-20260812-221224/result.json
  - dynamic/wine/RUN-GDB-20260812-221224/stops.jsonl
  - dynamic/wine/RUN-GDB-20260812-221224/debugger-evidence.txt
  - dynamic/wine/RUN-GDB-20260812-221224/curation.txt
  - dynamic/wine/RUN-GDB-20260812-221224/bugs.log
  - static/exports/BIN-97c95ba5572dce63/M2-adjacent-caller-gate-continuation-fault.md
addresses:
  - 0x0040100A
  - 0x0044CA00
  - 0x0044D794
  - 0x0044D79A
  - 0x0044D79C
  - 0x0044D7A4
  - 0x005B1AA4
  - 0x005B56D0
  - 0x005BA80C
  - 0x005C5EDC
  - 0x006C342B
result: adjacent-address-also-signals-exact-follow-up-skipped-target-survives-nopass
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/dynamic
  - re/resources
  - implementation/tooling
---

# EXP-20260812-031 - Adjacent caller-gate continuation fault

## Question

Is the reproduced continuation fault specific to a hardware execution
breakpoint at `0x0044D79A`, or does adjacent same-path breakpoint
`0x0044D794` also terminate in a structured target signal?

## Inputs and authority

- Exact unchanged PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Exact unchanged Training `CD/LEVEL07/LEVEL1.DAT` SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`.
- Adjacent static instructions `0x0044D794: mov ecx,[0x005BA80C]` and
  `0x0044D79A: test al,0x10`.
- Independent exact-PC reproductions in
  [[EXP-20260812-029 - Fresh selected-entry chain debugger fault]] and the
  structured-signal controller from
  [[EXP-20260812-030 - Unexpected-signal-safe GDB control]].
- M2.18 contract in
  [[Project Roadmap#M2.18 — Adjacent caller-gate continuation discriminator]].

No executable byte, register, game memory, or game file was modified. No PS1
source or finding was consulted. Every screenshot targeted only the isolated
640×480 Gamescope game surface, never the desktop or whole screen, and remains
ignored under `work/copies/EXP-20260812-031/evidence/`. Raw GDB stdout/stderr
remain ignored beside those captures.

## Expected discriminator

- If adjacent `0x0044D794` survived normally, a separate fresh matched arm at
  exact `0x0044D79A` would test address specificity.
- If the adjacent arm produced `target_signal`, the packet would stop without
  re-arming the exact PC and retain a broader nearby-continuation bound.
- Either arm required strict Direct3D gates, terminal signal handling,
  cleanup/detach, a schema-2 survival receipt, and a game-only endpoint.
- No result could establish downstream callee/data behavior or game semantics.

## Procedure

1. Launch `scripts/play-pristine.sh --research --windowed --mute`. Target only
   its isolated game window and send Down and Return as separate events.
2. Reject the first preflight after its complete log proves
   `INITSOFTRENDER`; stop its exact process tree and private sink before a
   debugger attaches.
3. Relaunch fresh. Accept only `Screen mode 640x480x16 selected`,
   `Starting Direct3D renderer`, and no `INITSOFTRENDER`. Confirm the game-only
   selector frame, select unchanged Training, and wait at its natural title.
4. Verify PID ownership/executable hash and attach schema-2
   `RUN-GDB-20260812-221224` with only hardware execution breakpoint
   `0x0044D794`. Record fixed caller globals and plant slot, then advance the
   title once.
5. Treat any target signal as the arm endpoint. Reconcile result, raw
   transcript, appended log, five-sample survival receipt, and a later
   game-only frame.
6. Apply the contract's stop rule. Do not run the exact-address arm after the
   adjacent arm signals. Stop only the resolved run processes and unload its
   private audio sink.

## Observed

### Launch and presentation gates

The accepted log records hardware mode at line 76, Direct3D initialization at
line 127, plant10 `.ANM`/`.ALL` requests at lines 1470/1471,
`---End InitMainGame---` at line 1476, and `NextLife` at line 1478. It contains
no `INITSOFTRENDER`. Committed log SHA-256 is
`4b31578df91c6662a95dced776f4611a77402117eda20e1789e7d4b0a4ed931c`.

The Training selector and natural-title game-only captures were visually
checked before attachment. Their SHA-256 values are respectively
`449966b2f04a19678099c4c420a646857f785ab65a7c8d872e3408fb984a8461`
and `524654827cd39b09ac7bd55640580cfdb9c262efc45f0da54aaaae669da500b4`.
The game's sink input was routed to private sink `ablpc_mute_2560198` during
the arm.

### Adjacent stop and structured signal

`RUN-GDB-20260812-221224` spans
2026-08-12T22:12:25.076247-04:00 through
2026-08-12T22:12:36.735375-04:00. It records exactly one breakpoint stop at
`0x0044D794`, immediately followed by structured fatal `SIGSEGV` at PC
`0x44D794` under `stop-print-nopass`.

The one pre-instruction snapshot records:

| Observation | Exact value |
|---|---:|
| `RAX/AL` | `0x40` |
| `RCX` | `0x0` |
| `RIP` | `0x0044D794` |
| `[0x005C5EDC]` | `0x40` |
| `[0x005BA80C]` | `0x00000680` |
| `[0x005B56D0]` | `0x00000480` |
| `[0x005B1AA4]` | `0x006C342B` |

The result is correctly tool-negative: `stop_reason == target_signal`,
`completed == false`, and `accepted == false`. Its one breakpoint is deleted,
cleanup is verified, and detach succeeds. Raw stdout SHA-256
`92f4d3fd6122193b99e1f1985391901cc08755cb061ce63e617a6a5146b579e3`
independently records the breakpoint stop followed by `SIGSEGV` at the same
PC. Raw stderr is empty.

Static semantics say `0x0044D794` would load `[0x005BA80C]` into `ECX`; the
zero `RCX` is the state before that instruction. The signal means this arm
does not prove that the load, following test/store/branch, or call completed.

### Independent survival and exact-arm stop rule

After cleanup/detach, identity re-verification passes and five samples from
22:12:37.257805 through 22:12:38.058470 all record process state `R`,
`TracerPid == 0`, and pass. The later isolated game frame at
22:14:33.278179243, SHA-256
`70749edc62d202fea3c5db444eeb3fba0c968d6e31cbcfeb8c94fea95d0ca0a4`,
visibly shows live Training gameplay. The pending signal was suppressed by the
proven `nopass` detach policy, so this is target survival after a rejected
debugger arm—not normal continuation evidence for the instrumented boundary.

The log also appended `NextLife`, but the controller correctly gave the
target signal precedence. Per M2.18's explicit first-pass rule, no fresh
schema-2 exact-`0x0044D79A` arm was run after the adjacent failure.

## Confirmed

- A fresh unchanged hardware run with only adjacent breakpoint `0x0044D794`
  stops once and then receives `SIGSEGV` at that same instrumented PC.
- Schema-2 status rejects the arm, deletes its point, detaches, and independently
  proves the target resumed untraced; a later game-only frame shows live
  gameplay rather than Wine's fatal dialog.
- Independent prior fresh runs reproduce the corresponding same-PC failure at
  exact `0x0044D79A`. The tested failure is therefore not plausibly confined
  only to the exact `test al,0x10` address.
- The accepted launch was unchanged PC data under hardware Direct3D with a
  private mute sink. No whole-screen capture, PS1 evidence, or target mutation
  was used.

## Inferred

Hardware execution-breakpoint continuation in this nearby caller-gate region
is unsafe under the tested Wine/native-GDB setup. This is a tooling/environment
boundary inference from two adjacent instrumented PCs, not evidence that
normal uninstrumented game execution is faulty.

## Unknown and limitations

- Root cause remains unknown among Wine WoW64, native GDB, hardware execution-
  breakpoint continuation, this local instruction region, or another condition.
- The exact PC was not freshly re-tested under schema 2 because the packet
  required stopping after adjacent failure. Its independent fresh schema-1
  reproductions remain the exact-address anchor.
- Normal completion of the load/test/store/call path, callee entry, source
  selector, plant field meanings, and any M1-to-resource identity remain
  unproven.
- Post-detach samples and one visual endpoint prove bounded process/game
  survival, not future correctness of every subsystem.

## Contradictions and negative results

The first preflight selected software rendering and was rejected before
debugger attachment. In the accepted arm, `NextLife`, five live samples, and
live gameplay coexist with a terminal debugger signal because `nopass`
suppresses delivery during detach. There is no status contradiction: the arm
remains rejected as continuation evidence even though the target survives.

Scoped cleanup first terminated the game. The Gamescope wrapper and one Wine
device process did not exit after bounded TERM waits, so their already verified
exact PIDs were killed and private sink module `536870916` was explicitly
unloaded. Final audits found no scoped game, debugger, winedbg, wrapper, or sink.

## Result

M2.18 is complete under its adjacent-failure stop condition. `KU-031` widens
from an exact-PC question to a nearby caller-gate continuation limitation. No
caller/callee/data or resource semantic is promoted. To prevent milestone
drift, the roadmap now leaves this debugger region and returns to M2's visible
resource-family exit gate.

## Follow-up

Execute [[Project Roadmap#M2.19 — Direct visible plant-family outcome]]. Reuse
the already accepted unchanged versus plant-04-to-plant-10 paired replacement,
apply one bounded identical camera trajectory in fresh hardware runs, and seek
a stable replacement-local rendered difference. Do not extend the caller-gate
breakpoint chain or add debugger features in that packet.
