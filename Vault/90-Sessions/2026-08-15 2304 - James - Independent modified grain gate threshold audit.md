---
type: session
date: 2026-08-15
agent: James
status: accepted
tags: [session, re/audit, re/runtime, mod/gameplay]
---

# Independent modified grain gate threshold audit

## Goal

Treat EXP-137's worker claims as hypotheses and independently attack the exact
Tunnels row-3 and City gate-0 physical threshold boundaries without launching
a runtime or changing game state.

## Work completed

- Re-read the complete startup authority chain, grain-gate experiments,
  research/implementation notes, decisions, unknowns, MOCs, and worker session.
- Verified exact worker HEAD
  `b13b27e7c3ca64e1035793fbd56bc7baf49ed348`, the ignored packet boundary,
  the `4bbd20c1...b2c` evidence manifest, all 69 listed hashes, identities,
  logs, receipts, snapshots, and accepted/rejected frames.
- Rebuilt the final C helper byte-for-byte, reconstructed the earlier source
  to its exact recorded hash, attacked refusal behavior, and confirmed the
  helper never writes auxiliary or observed gate/animation/life state.
- Reproduced the exact `(1..9)`/`(1,2,3)` executable in memory, reversed every
  guarded span to retail, and checked the modified PC x86 consumers directly.
- Verified row 3's exact shifted squared distance 4,993 is below 10,000;
  checked fixed-position, fixed-PID, survival, state, animation, and visual
  isolation for both accepted thresholds.
- Confirmed the earlier outside-trigger City pair and later software-renderer
  candidate remain rejected and are not generalized by tracked wording.
- Corrected one non-behavioral receipt overstatement: `hashes.sha256` is the
  complete 69-file `evidence/` manifest; packet-root helper hashes are stated
  separately.

## Result

**ACCEPT.** [[EXP-20260815-138 - Independent modified grain-gate threshold audit]]
accepts only Tunnels row 3 (`3` closed / `4` open) and City gate 0 at the
fixed trigger (`0` closed / `1` open). Both remain write-assisted. All other
gates, linked-row presentation, controller reachability, numeral assets,
persistence, and other executables remain open under KU-060.

M3 remains Complete; M2/M5 remain Deferred and M4/M6 remain Complete. The
Python/C selection procedure and target-write approval boundary are unchanged.

## Validation

- raw evidence manifest: 69/69;
- final helper: byte-identical rebuild; earlier source: exact reconstruction;
- exact profile/inverse: reproduced; focused suite: 12 passed;
- complete `make check`: Vault 400/0/0, five M4 anchors, 588 tests, tracked 0;
- process/private-sink/Wine mapping, protected-content, diff, and Git hygiene:
  clear before the documentation commit.
