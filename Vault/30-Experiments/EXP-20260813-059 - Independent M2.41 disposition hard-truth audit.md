---
type: experiment
id: EXP-20260813-059
date: 2026-08-13
question: Does independent review support M2.41 and leave no exact finite PC-native M2 successor in the evidence already cited through EXP-20260813-058?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; independent adversarial offline PC-native evidence audit
environment_version: Git 2.54.0; GNU objdump 2.46-3.fc44; existing Ghidra structured evidence export
working_directory: /home/dev/ABLPC
configuration: Fresh-context M2.42 verification; exact cited M1/resource/index surfaces only; no runtime, mutation, parser/schema work, semantics, broad search, or cross-port evidence
artifacts:
  - static/exports/BIN-97c95ba5572dce63/M2-independent-disposition-hard-truth-audit.md
  - static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json
addresses:
  - 0x0041BBBA
  - 0x0041BBC4
  - 0x0041BC0C
  - 0x0041DFAF
  - 0x0041ED19
  - 0x0041EEE4
  - 0x004318E4
  - 0x004319CB
  - 0x004467E0
  - 0x00446870
  - 0x00448350
  - 0x00459620
  - 0x0044D4E6
  - 0x0044D4FA
  - 0x0044D57F
  - 0x0059C30C
  - 0x0059D6A4
  - 0x005B18E0
file_offsets: []
result: accept-m2-41-no-finite-cited-successor-m2-deferred-m4-1-active
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/resources
  - re/milestone-audit
  - re/static
---

# EXP-20260813-059 - Independent M2.41 disposition hard-truth audit

## Question

Does independent fresh-context review support M2.41's exact slot-25/slot-63
reader-time-zero, call-gate, order, and M1-intersection conclusions, and does
the evidence already cited through `EXP-20260813-058` retain any exact finite
PC-native M2 successor?

## Method

I began from a clean tree at commit
`b7f755404236cf4325b2fc68af4d6c54b4a41a8b`, reread the complete required
startup sequence and relevant MOCs, and independently reviewed
`EXP-20260813-049` through `EXP-20260813-058`, `KU-023`, the M1 record and
positive-target closures, the generic-reader reports, and the M2.41 worker
session/disposition.

I rehashed the exact read-only work-copy executable and used fresh native
disassembly to reproduce:

- fixed-pool slot arithmetic;
- the full direct call census for `0x00459620`, `0x004467E0`, and
  `0x00446870`;
- slot 25's actual later call gate and zero-return path;
- all five fixed slot-63 call gates and header `+0x04` reads;
- normal update versus M1 coordinator order;
- current/list-object reader ordering and mode-2 pointer-list compaction; and
- the alternate `0x0059A5F0 != 0` branch retained by M2.22.

I separately queried the existing structured export for M1 closure inputs and
exact state references. No game was launched or instrumented. No executable,
asset, runtime state, parser, schema, or tool was modified. No PS1 evidence,
semantic naming, other resource family, or broad whole-program/pool search
was introduced.

## M2.41 result

M2.41 survives falsification at its declared boundary:

- Exact arithmetic places `0x0059C30C` and `0x0059D6A4` at pool slots 25
  and 63.
- Slot 25's selected call is governed by the later clear-`0x4000` reload at
  `0x004318E4-0x004318F3`, counter-zero test at
  `0x004318F9-0x00431900`, positive route count, and fixed call
  `0x004319CB -> 0x00459620`. Conditional zero can reach that gate initially
  or after the next update clears `0x4000`; exact zero selects ID-zero header
  `0x005B18E0`, whose zero start word takes the reader's zero-return arm.
- Slot 63 has exactly five fixed calls. `0x00415EFF` and `0x0042E92C`
  require `I == 0x23` and exclude zero. `0x0041C854`, `0x004401F5`, and
  `0x0046810D` are state-gated without a first-dword test, so conditional
  zero is statically reachable and selects the ID-zero retained end index 24.
- The complete first-dword writer set remains the M2.40 constant clear,
  nonzero-gated `LEVEL.RAW` source copy, and conditional fixed-pool removal.
  The direct slot gates are earlier scene/update/counter/event state. Native
  order places every selected normal-update call before the current M1
  coordinator, and the selected M1 closures contain none of the relevant
  stores or fixed calls.

These are conditional static reachability conclusions, not observations that
a named shipped scene realizes every combined predicate.

## Stronger disposition result

I explicitly separated "no successor was ranked" from "no finite candidate
is retained." The latter now survives review.

The omitted candidates from the first two deferrals are fully disposed by
`EXP-20260813-056/058`. The remaining generic current/list-object reads do
not preserve a third candidate: their reads are dominated by positive
first-dword gates or precede possible removal, and mode-2 removal compacts the
zeroed pointer out of list `0x0059D7E0` before coordinator reader
`0x00448350`. The alternate update branch still calls the same M1 coordinator
after its branch-specific work and exposes no exact M1-derived ID-zero
selection. The 20-word signed-selector surface, direct ID-zero readers, and
positive-target selector-2 surface already have completed finite negatives.

Persistent/copied cross-frame state, indirect aliases, and unreviewed
families remain possible, but the cited evidence supplies no exact producer,
consumer, ID-zero value, or finite target set for them. They are limitations,
not already-retained successors. This audit does not claim whole-program
absence.

## Verdict

**ACCEPT.** M2.41 is supported, and no exact finite PC-native M2 successor
remains in the already cited evidence.

M2 is not complete because the causal dependency exit gate and `KU-023`
remain unresolved. The evidence-backed milestone disposition is to defer M2
without weakening its gates, keep M3 planned, and activate exact M4.1 at its
already demonstrated hash-guarded, asset-free whole-file replacement
boundary.

## Revisit condition

Revisit M2 only when cited PC-native evidence exposes one exact finite
M1-to-resource candidate, a concrete mod goal supplies a bounded
discriminator, or a contradiction invalidates a completed negative. A vague
persistent-state possibility or wider search is not a finite successor.
