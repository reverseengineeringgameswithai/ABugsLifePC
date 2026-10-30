---
type: hypothesis
id: HYP-20260812-001
confidence: high
status: supported
supporting_evidence:
  - EXP-20260812-008
  - EXP-20260812-009
  - EXP-20260812-010
contradicting_evidence: []
created: 2026-08-12
updated: 2026-10-02
tags:
  - re/hypothesis
  - re/rendering
---

# HYP-20260812-001 - Shared payload targets identify reusable render content

## Hypothesis

For scene records in masked dispatch class `0x49`, records that share the same
positive payload target reuse the same render content while retaining separate
placement transforms.

## Confidence

High for positive targets in the tested masked dispatch-`0x49` Training path.

## Supporting evidence

- `EXP-20260812-008`: records 125 and 126 are distinct visible placements but
  both hold target offset `0x111E4`.
- `EXP-20260812-009`: both records select the same `0x49` path, which passes
  payload `+0x1C` to `0x0045A7F0`; its bounded target block supplies table and
  command data used to build renderer output.
- The Training primary population contains 19 multiply referenced targets, and
  990 same-dispatch records across 14 files validate against the positive block
  grammar.
- `EXP-20260812-010`: reciprocal guarded edits change only the independently
  identified record-124 and record-125 placement regions in phase-matched
  Direct3D captures. No pixel outside either difference union changes.

## Contradicting evidence

None yet. Shared input does not prove that animation, material state, or other
payload fields cannot alter the final visible identity.

## What would falsify it?

A cross-file or same-dispatch control in which records sharing a positive
target produce incompatible bounded target-consumer input, or a guarded
rebind that leaves the selected placement unchanged under an exactly matched
phase despite the new target reaching the same consumer.

## Next experiment

During M1.4, repeat a guarded shared/contrasting-target test in a non-Training
PC scene after its placements are independently identified.

2026-10-02 audit: M1.4 ran this as
[[EXP-20260812-013 - Level 01 target rebind no visible start effect]]. The
guarded Level 01 rebind (`0x3703C` → `0x3459C`, record 261) was accepted but
changed nothing at the start camera, and no Level 01 placement was assigned to
the nine matching records. That result neither supports nor contradicts the
hypothesis; a non-Training discriminator still needs a placement that is
visible after the edit. Later work found one Level 01 mesh shared by 22
placements, but under masked case 9, outside this hypothesis's bound
([[EXP-20260906-014 - Net-new scenery mushroom instances]]).

## Status

Supported. The claim remains bounded to positive targets and the tested PC
dispatch path. A target is not yet proven to be a complete object definition.
