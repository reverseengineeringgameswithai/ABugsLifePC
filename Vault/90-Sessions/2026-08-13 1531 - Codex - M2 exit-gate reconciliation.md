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

# M2 exit-gate reconciliation

## Agent

Codex

## Goal

Execute offline roadmap packet M2.34: reconcile every written M2 exit gate,
close the milestone only if all four are supported, and otherwise retain one
exact unsupported edge and the smallest PC-native discriminator.

## Files inspected

- [[START HERE]], [[Current State]], [[Environment Status]], [[Project Charter]],
  [[Project Roadmap]], [[Decision Log]], and [[Known Unknowns]]
- [[Evidence Standard]], [[Knowledge Hygiene]], [[Naming Conventions]],
  [[Research Method]], and the relevant MOCs/templates
- [[M1 Tool Support Matrix]], [[PC ANM inspector]], and
  [[PC ANM first-level]]
- Existing static and retained runtime evidence cited by
  `EXP-20260812-009/010/017/018/033/034` and
  `EXP-20260813-035/036/039/040/043`

## Experiments inspected

- [[EXP-20260812-009 - Training payload target structure and reuse census]]
- [[EXP-20260812-010 - Training target rebind visible substitution]]
- [[EXP-20260812-017 - Bounded PC ANM inspector]]
- [[EXP-20260812-018 - Same-layout PC ANM replacement]]
- [[EXP-20260812-033 - Character ALL replacement visible outcome]]
- [[EXP-20260812-034 - Character request and first consumer trace]]
- [[EXP-20260813-035 - Character retained-range first-use bridge]]
- [[EXP-20260813-036 - Shared-entry render-lineage discriminator]]
- [[EXP-20260813-039 - Direct3D renderer-path reconciliation]]
- [[EXP-20260813-040 - Direct3D retained-entry batch provenance]]
- [[EXP-20260813-043 - Exact 0A6C builder-input localization]]

## Changes made

- Added [[EXP-20260813-049 - M2 exit-gate reconciliation]] with a cited
  four-row gate matrix and exact asset-free replacement-instruction audit.
- Completed M2.34 without closing M2; added offline M2.35 as the canonical
  next packet.
- Updated [[Current State]], [[Known Unknowns]], [[Decision Log]], and the
  relevant MOCs.

## Conclusions

- Three M2 gates are supported: `.ANM` first-level multi-file/synthetic
  coverage, exact asset-free whole-file replacement instructions, and visible
  unknown preservation.
- M2's dependency-path gate remains unsupported because no PC-native edge
  makes an M1 record or positive target select the ID-zero `FLICK.ALL` path.
- M2.23's shared arena cannot fill that gap because M2.26 proves it belongs to
  selector-1 native software output, not the accepted Direct3D path.

## New hypotheses

The exact M1 positive-target Direct3D branch may carry a resource-selection
value indirectly through one of its builder arguments, but no existing
evidence demonstrates that edge.

## Contradictions discovered

No new evidence contradiction was found. The audit preserved two established
limits: `.ANM` tests do not validate `.ALL`, and shared renderer output does
not establish resource-selection identity.

## Tests run

- `git ls-files` protected-extension audit: no tracked `.ALL` or `.ANM` files.
- `git check-ignore` confirmation: `work/copies/` and the exact staged M2.20
  destination are ignored.
- `make check`: Python dependency smoke check passed; Vault lint reported 182
  notes, 0 errors, and 0 warnings; 203 tests passed; tracked-file audit
  reported 0 violations; Git whitespace checks passed.

## Unresolved questions

- `KU-023`: which, if any, exact M1 record/positive target selects the ID-zero
  character resource path?
- General `.ALL` layout, invalid-input behavior, semantics, and safe partial
  editing remain unknown and outside the supported format boundary.

## Recommended next action

Execute offline M2.35. Trace only selector-2 values from exact M1 positive-
target consumer `0x0045A7F0` into its Direct3D builder calls and test for a
data-flow edge from ID-zero header `0x005B18E0`, retained range
`[0x005A9660,0x005A9DE0)`, or the exact selected resource state.

## Git commit if applicable

Bounded commit message: `research: reconcile M2 exit gates`.
