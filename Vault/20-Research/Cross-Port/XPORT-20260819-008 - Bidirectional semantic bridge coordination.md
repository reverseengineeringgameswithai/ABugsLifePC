---
type: cross-port
id: XPORT-20260819-008
date: 2026-08-19
source_id: SRC-PS1-ABL
source_commit: 1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51
pc_binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
status: planned-awaiting-pinned-abl-bridge-commit
updated: 2026-10-02
tags:
  - research/cross-port
  - re/static
  - re/tooling
---

# XPORT-20260819-008 - Bidirectional semantic bridge coordination

## Bounded question

How should ABLPC export a PC-native mathematical or structural observation so
the external PS1 project can rank MIPS candidates without allowing PC evidence
to confirm a PS1 claim?

This note coordinates the reverse, PC-to-PS1 direction of the existing
cross-port workflow. It does not create a correspondence, implement an ABLPC
exporter, or promote a claim on either port.

## Current state

The operator has requested a PS1-side inbound bridge. Its proposed boundary is:

```text
committed PC-native evidence
  -> versioned architecture-neutral lead packet
  -> read-only PS1 candidate ranking
  -> PS1-native static and behavioral discrimination
  -> PS1 claim, if independently supported
```

The ABL-side bridge work is presently outside an ABL commit. Under
[[Cross-Port Evidence Policy]], this note does **not** cite, inspect, hash, or
depend on that working-tree implementation. The `source_commit` above remains
the last pinned PS1 evidence revision used by the existing berry calibration,
not the identity of the new bridge. Activate and cite the consumer only after
the operator commits it and this note records that new commit and exact paths.

## Proposed outbound packet contract

An ABLPC-produced PC-to-PS1 lead should contain only bounded, reviewable data:

- schema and normal-form version;
- lead ID, `pc-to-ps1` direction, and `external_lead` status;
- exact ABLPC commit and `bugs.exe` SHA-256;
- one PC address/range and hashes of the committed PC evidence notes;
- normalized operations, operand widths, signedness, constants, table shapes,
  comparisons, effects, and control-flow features;
- a bounded PS1 question, explicit nonclaims, and required target-native
  verification.

A discovery packet must omit known PS1 addresses, names, and expected answers.
Raw Ghidra exports, decompiler bodies, binaries, runtime captures, and ABLPC
working-tree state do not enter the PS1 repository.

## Authority boundary

- A PC packet can select a PS1 candidate or experiment. It cannot confirm a
  PS1 function, address, field, format, behavior, or bug.
- A ranking result remains `ps1_candidate_only` and cannot satisfy an ABL
  Phase 4 gate or enter its Canon.
- The PS1 executable under a controlled PS1 environment remains authoritative
  for PS1 claims. ABLPC remains authoritative only for the PC claims its own
  evidence supports.
- When the ports disagree, preserve the divergence rather than weakening one
  side's evidence.

These are the reverse-direction application of [[Cross-Port Evidence Policy]],
not a new evidence hierarchy.

## Calibration relationship

[[XPORT-20260818-006 - Berry equip byte candidate from replay-seeded static search]]
already supplies a suitable positive calibration: PC function `0x0041C9B0`
contains a five-column byte accumulator indexed by `row*5+type`, guarded at
`200`, incremented by `2`, and tested at `100`; its PC selector was later
confirmed causally.

Using that known correspondence to test transport and scoring is circular. It
may validate the bridge machinery, but it is not another berry discovery or an
independent confirmation. The first efficacy claim requires a blind or held-out
packet whose expected PS1 locator is not supplied to the matcher.

## Activation gate

Before this note becomes active:

1. record the committed ABL revision containing the target-side consumer;
2. cite and hash its versioned schemas, tool, tests, and calibration packet;
3. implement or explicitly defer the ABLPC-native packet exporter;
4. validate one committed calibration packet from both repositories;
5. preregister one blind/held-out comparison and its target-native falsifier;
6. keep generated rankings out of ABLPC's PC claim surfaces.

Until those conditions are met, this is coordination documentation only.

2026-10-02 audit check: `SRC-PS1-ABL` still has no commit on any branch after
`1186eb6` (2026-08-12), and ABLPC has no packet exporter. Step 1 is unmet,
so this note is still inactive.

## Related

- [[Cross-Port Evidence Policy]]
- [[External Source Registry]]
- [[XPORT-20260817-005 - Berry contact array and type marker shape]]
- [[XPORT-20260818-006 - Berry equip byte candidate from replay-seeded static search]]
- [[Ghidra export structure and caveats]]
