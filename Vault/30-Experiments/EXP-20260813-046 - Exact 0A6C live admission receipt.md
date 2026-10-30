---
type: experiment
id: EXP-20260813-046
date: 2026-08-13
question: Does the exact 0x0A6C evaluator agree with native append counts and expose one stable control rejection outside the replacement?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; Wine 11 WoW64; Gamescope 3.16.25; hardware Direct3D
environment_version: gdb-harness 1.5.0; watch/result schema 6 live-validated
working_directory: /home/dev/ABLPC
configuration: Exact entry 7 offset 0x0A6C form 0x3C; fresh control/replacement/control
artifacts:
  - dynamic/wine/EXP-20260813-046-comparison.txt
  - dynamic/wine/RUN-GDB-20260813-142433
  - dynamic/wine/RUN-GDB-20260813-142708
  - dynamic/wine/RUN-GDB-20260813-142853
  - dynamic/wine/RUN-GDB-20260813-141810
  - dynamic/wine/RUN-GDB-20260813-142155
addresses:
  - 0x004065B0
  - 0x0044F951
  - 0x0044C8AB
file_offsets:
  - 0x0A6C
result: live-evaluator-agrees-fresh-outcome-temporally-variable
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/dynamic
  - re/rendering
  - implementation/tooling
---

# EXP-20260813-046 - Exact 0A6C live admission receipt

## Question

Does the purpose-specific schema-6 native-arithmetic evaluator reproduce exact
record `0x0A6C`'s observed append decision and, in fresh accepted control/
replacement/control arms, identify the same first rejection in both controls
while the replacement passes?

## Scope and authority

The user's explicit instruction to execute the next pending roadmap item
authorized M2.32's already specified live phase. The packet reused only the
existing safe data watches at pre selector `0x0059F7F0`, pre-reset marker
`0x004C4118`, and post header `0x005B18E0`. It added no execution point or
watch, retained no raw source/global/derived or batch values, wrote no target
state, and edited no game source file. It inspected no other record or family,
assigned no semantic name, created no general `.ALL` tooling, and used no PS1
source or runtime.

## Inputs and gates

All three arms used executable SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
Control A and B used `CD/CHARS/FLICK.ALL` SHA-256
`a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`;
the replacement used
`6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`,
equal to the staged `CD/CHARS3/FLICKD.ALL` source.

Every accepted log records the four required hardware-path markers, exact
`level07\level1.dat` and `chars\flick.all` loads, and `NextLife`; none records
`INITSOFTRENDER`. The complete 168-call plan remains locked at SHA-256
`5eb280a7bd54b56a9654fed7984e9677a15618c5376be703a85718ea3bb2ffec`.
Each arm requires entry 7/file offset `0x0A6C`/form `0x3C`, page 16, caller
mode 2, one warmup rollover, one captured cycle, exact count reconciliation,
cleanup/detach, no target signal, and five resumed/untraced survival samples.

## Procedure

1. Reverified all executable and selected-file hashes, launcher dry runs,
   schema-6 fixtures, the canonical plan, clean process state, `ptrace_scope`,
   and the pristine Wine-drive target.
2. Launched each staged arm separately under the hardware Direct3D path,
   selected Training, and required logged `NextLife` before attachment.
3. Attached the exact schema-6 receipt at the existing three data watches and
   captured one complete post-warmup 168-call cycle.
4. Preserved the purpose-specific prediction, native count outcome, first
   reject/evaluated count, active-state digest, and zero-payload declarations.
5. Closed each exact process group, private sink, and Wine server before the
   next arm; restored the Wine `R:` link to the pristine derived disc tree.

The accepted ordering was determined by two fail-closed timing calibrations.
`RUN-GDB-20260813-141810` attached at the natural title and exhausted 1,000
unmatched flush stops without a rollover. `RUN-GDB-20260813-142155` received
the title input only after attachment and exhausted 1,000 stops after one
rollover but before a captured cycle. Both cleaned up, detached, observed no
target signal, and passed survival; neither contributes admission evidence.

## Observed

Accepted runs are `RUN-GDB-20260813-142433` (control A),
`RUN-GDB-20260813-142708` (replacement), and
`RUN-GDB-20260813-142853` (control B). Every arm completes at exactly 400
stops, observes two rollovers, installs/deletes three data watches and no
breakpoints, verifies cleanup/detach, receives no target signal, and passes
all five survival samples. Every prediction matches the independently
observed count outcome. Raw input retention is false and retained payload
bytes are zero.

The exact fresh receipts are:

| arm | predicted / observed append | first reject | evaluated slots |
|---|---:|---:|---:|
| control A | `0 / 0` | `0x004065B0` | 7 |
| replacement | `0 / 0` | `0x004065B0` | 7 |
| control B | `1 / 1` | none | 12 |

Control B passes all 12 logical admission slots and reaches the native
four-vertex/six-index append. Control A and the replacement both reject at
slot 7. Their active-state digests differ, so the shared rejection does not
claim identical underlying state.

The full gate, digest, log-hash, and timing-rejection receipts are in
`dynamic/wine/EXP-20260813-046-comparison.txt`.

## Confirmed

- Harness 1.5.0/schema 6 exact mode is live-validated at this one locked
  record and envelope.
- The native arithmetic prediction agrees with the independently observed
  append count in all three accepted arms.
- The fresh append pattern is `0/0/1`, not M2.29's retained `0/1/0`.
- Exact `0x0A6C` admission is not source-stable across fresh launches: the
  unchanged controls disagree, and the replacement does not uniquely pass.

## Contradiction and limits

M2.29's `0/1/0` remains exact for its retained arms, but it does not reproduce
in these fresh arms. This packet preserves that temporal/process-state
contradiction rather than attributing it to the replacement bytes. There is
no evaluator/count mismatch: `prediction_matches_observation` is true in all
accepted arms.

The result does not identify which active-state input differed, prove that
slot 7 caused any visible pixel, assign meaning to its arithmetic, or promote
a parser/editor or public mod operation. The state digests are coherence
identities, not semantic or causal evidence.

## Result and follow-up

M2.32 is complete under its explicit ambiguity condition. The narrow next
question is temporal stability within one unchanged process, not another
fresh source attribution. M2.33 should remain offline first: review whether a
bounded consecutive-cycle schema can reuse the same exact watches, evaluator,
redaction, and plan while retaining only the existing receipt per cycle. Any
live repeated-cycle arm requires new explicit authority.
