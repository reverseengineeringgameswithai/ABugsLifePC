---
type: experiment
id: EXP-20260819-009
date: 2026-08-19
updated: 2026-08-20
status: complete
binary_sha256: 1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f
environment: PC auto-hardware derived-build control
question: Does fresh D4 produce zero differences outside the fixed EXP-008 mask?
result: Accepted finite D4 holdout; zero outside-mask observations
tags: [reverse-engineering, level01, terrain, runtime]
---

# EXP-20260819-009 - R2k Anthill D4 control-trained mask holdout

## Question

Does one fresh, unmodified Level01 control reproduce every D1-reference pixel
outside the fixed EXP-008 proposed mask over the exact 121-frame grid?

## Authorization boundary

The user authorized only one fresh D4 control and one read-only four-byte
Level01 index read at `0x00861C84`. The authorization excluded DAT writes,
runtime/debugger writes, `SIGSTOP`/`SIGCONT`, localizer creation, a candidate,
and every successor arm. That authorization is now consumed.

## Frozen identities

- command: `PYTHONPATH=reimplementation scripts/r2k-run-d4-combined-holdout.py`
- command accepts no arguments
- stage: `work/copies/EXP-20260819-009/D4-control-trained-mask-holdout-retail-001`
- provisional arm evidence: `D4-CTM-SB-AH-001`
- executed build: `1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`
- Level01 DAT: retail `786b7a...8b53`
- EXP-008 diagnostic: `83931a8a...9a5`
- proposed mask PNG: `b855df0a...c936`
- decoded mask: `9ff27caa...1ba`, exactly `93,445` pixels
- grid: the unchanged 121-frame start/cadence/end, crop, input, Level01/title/
  index, renderer-marker, process, and lifecycle gates

D4 must have a fresh PID/start identity distinct from D1, D2, D3, C1, L1, L2,
and C2. Revalidate diagnostic, mask, D1 reference, and every D4 PNG/decoded-RGB
identity before and after comparison.

## Acceptance and failure rules

Acceptance requires zero outside-mask observations and zero unique mismatch
pixels. There is no tolerance, phase adjustment, normalization, extension,
mask expansion, or D4-derived widening. Retain all 121 per-frame residuals,
their union, components, overlay, hashes, and result. Any mismatch rejects and
publishes no accepted reference. Analyzer/publication failure quarantines
provisional evidence; cleanup or retail-`R:` restoration uncertainty remains
pending.

## Claim ceiling

A pass establishes one finite-grid control holdout only for this exact
derived-build/view/grid. It does not establish exhaustive nuisance coverage,
terrain/ground identity, face-8 visibility, causality, no effect, collision, or
authorization for a later localizer.

## Result

D4 completed on fresh process `1267141/21477936/1266881`. Retail Level01 DAT,
the exact auto-hardware build, CD identity, six Direct3D markers, Level01 index
`1`, input chronology, all 121 timing/crop/frame gates, cleanup, and retail-`R:`
restoration passed. Exactly one read occurred: `(0x00861C84,4)`, bytes
`01000000`. No prohibited operation occurred.

All 121 frames produced zero observations and zero unique pixels outside the
fixed 93,445-pixel mask. All 123 holdout PNGs rehash; the union is the empty
mask PNG `136af9d0...fbe1`. Result JSON SHA-256 is
`bf2b46258ca92d654f993c9607f4bd5e453aac818dfb59e248e0ac01173569d8`;
arm disposition SHA-256 is
`cc4fdc2cbb91ebbcdc2f4c8999449b19268e9a76e0112249f27d73529c2e1ebe`.
James independently reproduced and accepted this finite-holdout result under
the claim ceiling above.

## Links

- [[EXP-20260819-008 - R2j Anthill control-trained successor mask]]
- [[EXP-20260819-007 - R2i Anthill replicated face-8 localizer]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Known Unknowns]]
- [[Decision Log#DEC-171 - Require a fresh D4 holdout for the control-trained mask]]

## 2026-08-20 successor boundary

D4 closure is preserved unchanged. Its accepted finite-mask result is a frozen input to [[EXP-20260820-001 - R2l fresh replicated face8 localizer]]. The successor uses fresh arms, stages, evidence, processes, and independently created work-copy DATs; it may not reuse or reinterpret EXP-007. No successor creation or runtime is authorized by EXP-009.
