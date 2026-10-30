---
type: session
date: 2026-08-13
agent: Codex
status: completed
tags:
  - session
  - re/resources
  - re/milestone-audit
---

# M2 dependency-gate disposition

## Agent

Codex

## Goal

Execute offline roadmap packet M2.37: decide whether M2's dependency gate can
close without weakening the milestone outcome, or retain exactly one finite
PC-native candidate and bounded first discriminator.

## Files inspected

- [[START HERE]], [[Agent Operating Manual]], [[Current State]],
  [[Environment Status]], [[Project Charter]], [[Project Roadmap]],
  [[Decision Log]], and [[Known Unknowns]]
- [[Reverse Engineering MOC]], [[Functions MOC]], [[Experiments MOC]], and
  [[File Formats MOC]]
- Existing exact function dossiers and the canonical-hash derived
  `bugs.exe` copy under `work/copies/`

## Experiments inspected

- [[EXP-20260813-049 - M2 exit-gate reconciliation]]
- [[EXP-20260813-050 - M1 positive-target selector-2 input provenance]]
- [[EXP-20260813-051 - Generic resource-index producer census]]
- The cited M1 and ID-zero resource evidence from `EXP-20260812-009/010`,
  `EXP-20260812-033/034`, and `EXP-20260813-039/040`

## Changes made

- Added [[EXP-20260813-052 - M2 dependency-gate disposition]].
- Added `DEC-20260813-047` to [[Decision Log]].
- Completed M2.37 with the gate retained and added offline M2.38 as the exact
  active packet.
- Updated [[Current State]], [[Known Unknowns]], the relevant function
  dossiers, and MOCs.
- Corrected the stale hardware-arena wording and outdated next action in
  [[FUNC-97C95BA5572D-0044D430]].

## Conclusions

- The existing M1 and ID-zero resource chains remain parallel. Rewording them
  into one dependency would remove the causal selection edge required by the
  current M2 outcome, so M2 cannot close.
- Exact `0x0044CA00` instructions bound one finite candidate: at most 20
  signed selector words at `0x0059D9C0 + i * 0x30`.
- Selector `-103` is the only exact value in that formula that addresses
  ID-zero header `0x005B18E0`; no M1 producer or observed value is proved.

## New hypotheses

One of the bounded source-record selector words may be populated from the M1
record/positive-target route and later consumed as signed `-103`. This is only
the M2.38 candidate, not a promoted dependency claim.

## Contradictions discovered

No evidence contradiction was found. One documentation-drift issue was fixed:
the `0x0044D430` dossier still called M2.23's shared arena hardware output
despite M2.26's exact selector-1 software-ownership correction.

## Tests run

- Verified the inspected derived `bugs.exe` SHA-256 against the canonical
  executable hash.
- Rechecked native instructions around `0x0044CA00-0x0044D205` and
  coordinator call `0x0044D7A4` with GNU `objdump` 2.44.
- Independently checked the signed arithmetic
  `0x005B1A7C + (-103 * 4) == 0x005B18E0`.
- Ran repository metadata/link, whitespace, diff, and Git hygiene checks at
  closeout.

## Unresolved questions

- `KU-023`: whether an M1 record or positive target produces one of the 20
  exact selector words and signed value `-103` at `0x0044CE0D`.
- Persistent/copied state and indirect routes remain unknown but are outside
  M2.38's selected finite candidate.

## Recommended next action

Execute only [[Project Roadmap#M2.38 — Signed source-record selector provenance]].
Classify native producers for the 20 exact selector words, intersect only
proven lineages with the established M1 route, and test for signed `-103`.

## Git commit if applicable

Bounded commit message: `research: disposition M2 dependency gate`.
