---
type: experiment
id: EXP-20260819-008
date: 2026-08-19
updated: 2026-08-19
status: complete
binary_sha256: not-applicable-offline
environment: offline retained-evidence analysis
question: Can C1 and C2 alone produce a bounded successor nuisance-mask proposal?
result: Proposed 93445-pixel control-trained mask; fresh D4 holdout required
tags: [reverse-engineering, level01, terrain, offline]
---

# EXP-20260819-008 - R2j Anthill control-trained successor mask

## Question

Can control-only pixels that invalidated the EXP-006 nuisance mask in
[[EXP-20260819-007 - R2i Anthill replicated face-8 localizer]] be incorporated
into a bounded successor proposal without using either localizer arm or
retroactively changing EXP-007's result?

## Authorization and scope

This packet is offline only. It launched no game process and performed no DAT,
runtime-memory, debugger, or signal operation. Inputs are the validated C1/C2
control packets plus immutable EXP-005/006/007 provenance. L1/L2 frames, masks,
and comparator outputs are not selection inputs.

## Frozen transform

```text
raw_new = union((control_frame != D1_reference) AND NOT old_mask)
successor = old_mask OR chebyshev_dilate(raw_new, radius=3)
```

The old mask is not dilated again. Publication is atomic into a fresh
`proposed/` namespace. The result remains proposed until a separately
authorized D4 holdout passes.

## Result

James independently reproduced and accepted the offline artifact:

- diagnostic JSON SHA-256: `83931a8ae5158a3eb6478ddb664894fe96e705805dc13f889f5363a9d8cca9a5`
- C1 observations: `0`
- C2 observations: `251` in frames `25`, `35`, `105`, and `108`
- raw unique control pixels: `249`
- dilated raw set: `1,645` pixels, including `680` already in the old mask
- successor additions: `965` pixels
- successor population: `93,445 / 307,200` (`0.30418294270833335`)
- eligible unmasked population: `213,755`
- decoded binary-mask SHA-256: `9ff27caa7842b9047c9eebf633f9d280dd820841b81eba5fd491845a66fb71ba`
- mask PNG SHA-256: `b855df0ac67554737ae990bcb5fdbb14a132eae32af6bddf292c07dba193c936`
- overlay PNG SHA-256: `8bd02d57dbdbb514dc603f3566491d1a5f131a844fef12d3ecd07a07259a2bb6`

All 248 retained output PNG hashes reproduced. The artifact is ignored under
`work/copies/EXP-20260819-008/`; no game data or generated evidence is tracked.
The focused suite passed `16/16`.

## Interpretation ceiling

This is a proposed nuisance mask, not an accepted reference. It does not rescue
EXP-007, prove exhaustive nuisance coverage, localize face 8, identify terrain
or ground, establish causality/no effect, or advance collision behavior. The
next gate is [[EXP-20260819-009 - R2k Anthill D4 control-trained mask holdout]].

## Links

- [[EXP-20260819-006 - R2h Anthill D3 combined-mask holdout]]
- [[EXP-20260819-007 - R2i Anthill replicated face-8 localizer]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Known Unknowns]]
- [[Decision Log#DEC-171 - Require a fresh D4 holdout for the control-trained mask]]
