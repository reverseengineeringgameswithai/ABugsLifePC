---
type: experiment
id: EXP-20260813-048
date: 2026-08-13
question: Does exact 0x0A6C admission vary and recur across three consecutive cycles in one unchanged process?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; Wine 11 WoW64; Gamescope 3.16.25; hardware Direct3D
environment_version: gdb-harness 1.6.0; watch/result schema 6 live-validated at fixed three-cycle bound
working_directory: /home/dev/ABLPC
configuration: Exact entry 7 offset 0x0A6C form 0x3C; one warmup plus three captured cycles in one unchanged process
artifacts:
  - dynamic/wine/EXP-20260813-048-consecutive-cycle-receipt.txt
  - dynamic/wine/RUN-GDB-20260813-150842
addresses:
  - 0x004065B0
  - 0x004069A1
  - 0x0044F951
  - 0x0044C8AB
file_offsets:
  - 0x0A6C
result: one-process-reject-pass-reject-recurrence
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/dynamic
  - re/rendering
  - implementation/tooling
---

# EXP-20260813-048 - Exact 0A6C consecutive-cycle live receipt

## Question

In one unchanged post-`NextLife` hardware Direct3D process, does the locked
schema-6 receipt for exact entry 7/file offset `0x0A6C` remain stable across
three consecutive captured cycles, or does its append/reject outcome vary and
recur?

## Scope and authority

The user's fresh instruction to continue to the next item authorized M2.33's
already staged live phase. The arm changed only exact `capture_cycles` from
one to three inside harness 1.6.0/schema 6, apart from required experiment/PID
provenance. It reused the existing data watches at `0x0059F7F0`,
`0x004C4118`, and `0x005B18E0`, the canonical 168-call plan, exact record,
root/page, renderer, redaction, signal, cleanup/detach, and survival gates.

No breakpoint, new watch, target write, source edit, other record/family,
semantic name, general `.ALL` tooling, or PS1 evidence entered the packet. No
raw GDB console transcript was retained in the curated run.

## Inputs and gates

The unchanged control used executable SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
and `CD/CHARS/FLICK.ALL` SHA-256
`a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`.
The complete new log is SHA-256
`4b31578df91c6662a95dced776f4611a77402117eda20e1789e7d4b0a4ed931c`.

It contains exactly one each of `Native software render mode is FALSE`,
`RenderMode set to Direct3d render mode`, `Screen mode 640x480x16 selected`,
and `Starting Direct3D renderer`; it contains no `INITSOFTRENDER`. It also
records exact `level07\level1.dat` and `chars\flick.all` loads,
`End ClearLoadScreen`, `End InitMainGame`, and `NextLife` before attachment.
The record plan remains 168 calls at SHA-256
`5eb280a7bd54b56a9654fed7984e9677a15618c5376be703a85718ea3bb2ffec`.

## Procedure

1. Re-read the complete START HERE chain, charter/manual, current registers,
   relevant MOCs, runtime-tooling contract, and M2.32/M2.33 evidence.
2. Reverified the executable and unchanged selected-file hashes, clean process
   baseline, launcher dry run, exact plan, and the focused 132-test fixture
   gate.
3. Launched the unchanged accepted control tree, selected the hardware
   renderer and Training, held the title Return long enough for DirectInput,
   and required a newly logged `NextLife` before attachment.
4. Derived the live spec from accepted `RUN-GDB-20260813-142433`. The diff is
   limited to experiment ID, fresh PID, and `capture_cycles: 1 -> 3`.
5. Ran exact `RUN-GDB-20260813-150842`, reconciled all three ordered receipts,
   removed the non-curated raw GDB console output, stopped only the scoped
   launch/prefix processes, unloaded its private sink, and restored Wine drive
   `R:` to the pristine derived disc tree.

Two earlier non-instrumented attempts were stopped at `Start ClearLoadScreen`
before the title Return was held. That line is the documented natural title,
not a fault. No debugger attached and neither attempt contributes evidence.

## Observed

The arm completes and is accepted at 816 stops: 672 pre-selector, 96 entry-
post, and 48 flush-marker stops. It observes four rollovers, exactly one
warmup plus three captured cycles. The prior 800-stop projection was
conservative but not exact because this arm observes 16 additional flush-
watch stops; it still finishes 184 stops below the unchanged ceiling.

The ordered receipts are:

| cycle | predicted / observed append | first reject | evaluated slots |
|---:|---:|---:|---:|
| 0 | `0 / 0` | `0x004065B0` | 7 |
| 1 | `1 / 1` | none | 12 |
| 2 | `0 / 0` | `0x004065B0` | 7 |

All predictions match independent count outcomes. The active-state digests
are distinct in all three cycles, including between the two slot-7 rejects.
The exact append sequence is therefore reject/pass/reject: one `A/B/A`
recurrence inside the same unchanged process, without a claim that the two
rejecting states are identical.

All three data watches are installed and deleted, no breakpoint is installed,
cleanup and detach verify, no target signal or controller error occurs, and
five post-detach samples find process state `R` with `TracerPid == 0`.

## Output exclusion

The result and every receipt declare `raw_inputs_retained: false` and
`payload_bytes_retained: 0`. All 816 stop rows have null watched values, empty
register maps, and empty memory-read arrays. The generated GDB console stream
was intentionally deleted rather than curated; `metadata.json` does not list
it as an artifact.

## Confirmed

- Exact `0x0A6C` admission can vary within one unchanged process; fresh-
  process state is not required for the observed boolean change.
- The bounded three-cycle sequence contains one reject/pass/reject recurrence.
- Harness 1.6.0/schema 6 is live-validated at its fixed three-cycle envelope,
  with evaluator/count agreement, payload-free receipts, and all safety gates.

## Limits

One three-cycle sequence does not establish a period, distribution, or a
sequence expected in another process. Equal slot-7 rejects do not imply equal
underlying state because their digests differ. The result does not attribute
admission to the source differences, prove a visible pixel consequence,
assign state or field semantics, or support a parser/editor/public mod.

## Result and follow-up

M2.33 is complete. The recurrence answers KU-045's within-process question
without resolving source or visible causality. The next packet should be an
offline M2 exit-gate reconciliation: decide whether the accumulated PC-native
level/resource/outcome path and asset-owned replacement instructions satisfy
the milestone gates, or name exactly one remaining blocker. Do not launch,
edit source, add tooling, or widen the record/family during that audit.

## Final validation

- Focused exact/evidence/harness suite: 132 passed.
- Full `make check`: dependency smoke test passed; Vault lint found 180 notes
  with 0 errors and 0 warnings; 203 tests passed; tracked-file audit found 0
  violations.
- `git diff --check` passed; the staged tracked-file audit and final clean
  worktree are commit/handoff gates.
