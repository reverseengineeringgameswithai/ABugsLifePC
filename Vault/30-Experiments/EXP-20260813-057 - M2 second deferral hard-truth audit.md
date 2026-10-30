---
type: experiment
id: EXP-20260813-057
date: 2026-08-13
question: Does the post-M2.40 evidence support deferring M2, or were exact finite fixed-pool candidates still retained or left structurally unclassified?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; adversarial offline evidence audit
environment_version: Git 2.54.0; GNU objdump 2.46-3.fc44
working_directory: /home/dev/ABLPC
configuration: Read-only premise audit of EXP-20260813-056 follow-up and DEC-20260813-051; exact local work-copy hash, native arithmetic/disassembly, and existing PC evidence only; no runtime, mutation, parser/schema change, other resource family, broad indirect search, semantics, or cross-port evidence
artifacts:
  - static/exports/BIN-97c95ba5572dce63/M2-second-deferral-hard-truth-audit.md
  - static/exports/BIN-97c95ba5572dce63/M2-generic-resource-index-producer-census.md
  - static/exports/BIN-97c95ba5572dce63/M2-fixed-pool-index-producer-census.md
addresses:
  - 0x004145BB
  - 0x00418791
  - 0x00431804
  - 0x00431983
  - 0x004319CB
  - 0x004467E6
  - 0x00446825
  - 0x00446876
  - 0x004468B5
  - 0x00459628
  - 0x0045962B
  - 0x0059B628
  - 0x0059C30C
  - 0x0059D6A4
  - 0x0059D728
  - 0x005B18E0
file_offsets: []
result: m2-second-deferral-premature-residual-fixed-pool-slots-25-and-63
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/resources
  - re/milestone-audit
  - re/static
---

# EXP-20260813-057 - M2 second deferral hard-truth audit

## Question

Does the evidence after M2.40 support returning M2 to `Deferred`, or did that
disposition again confuse an unranked/excluded surface with the absence of a
finite PC-native candidate?

## Method

I attempted to falsify each premise of the post-M2.40 disposition. I reread
`EXP-20260813-049` through `EXP-20260813-056`, the two fixed-pool reports, the
eight-reader census, `DEC-20260813-049` through `DEC-20260813-051`, and the
current roadmap. I independently rehashed the exact executable, recalculated
every retained fixed-pool address, and checked the residual readers and direct
call sites in native disassembly.

No game was launched or instrumented. No executable, asset, runtime state,
parser, schema, or tool was changed. No other resource family, broad indirect
search, semantic name, or PS1 evidence was introduced.

## Observed

### Premises that survive

- M2's causal gate and `KU-023` remain unresolved; M2 cannot be complete.
- M2.40 is complete at its declared slot-2/slot-3 boundary. Its conditional
  zero is separate `LEVEL.RAW` plus fixed-pool state, not M1-derived.
- M4.1 remains technically evidence-backed at its exact hash/path boundary.

### Premise that fails

The claim that no finite successor remained is unsupported.

First, the prior hard-truth report explicitly retained `0x0059D6A4` as
fixed-pool slot 63 and called it lower-ranked. M2.40's stop rule expressly
excluded that address, so M2.40 did not dispose its exact reader paths.

Second, that report described `0x0059C30C` only as a separate object. Exact
arithmetic supplies the omitted pool classification:

```text
0x0059B628 + 25 * 0x84 = 0x0059C30C
0x0059B628 + 63 * 0x84 = 0x0059D6A4
```

Both are therefore first dwords in the already bounded 64-record pool, not a
new arbitrary-object family.

### Exact residual readers

Dispatcher case 1 reaches `0x004317D0` through `0x00418791`. That function
passes fixed slot 25 at `0x00431983` to `0x00459620`; the read at
`0x00459628-0x0045962B` uses the first dword directly in
`0x005B18E0 + I * 4`. Its earlier flag test at `0x00431804` reads slot 25
`+0x5C`. M2.40 proves late zero does not clear that field, so the gate does
not by itself exclude reader-time zero. Other predicates remain unresolved.

Functions `0x004467E0` and `0x00446870` likewise use fixed slot 63's first
dword directly in the same header formula. Five direct calls pass
`0x0059D6A4`. Two have explicit `I == 0x23` gates; three are guarded by other
state. Their coexistence with late zero and their exact M1 intersection were
not classified by M2.40.

These observations prove a finite next question, not that either slot is zero
at a named unchanged-scene read or that either is M1-derived.

## Confirmed

- `0x0059C30C` and `0x0059D6A4` are exact fixed-pool slots 25 and 63.
- Both first dwords feed already-censused generic `0x005B18E0 + I * 4`
  readers through exact fixed-pointer call sites.
- M2.40 explicitly excluded those paths and cannot retire them by implication.
- The post-M2.40 M2 deferral and exclusive M4.1 activation are premature.

## Inferred

The residual slot-25 and slot-63 paths are the best next M2 packet because
they are the smallest exact candidates already retained by the same reader
and fixed-pool evidence. This ranking does not assert reader-time values,
source meanings, execution in a particular scene, or M1 provenance.

## Contradictions and limitations

- “Separate object” can correctly mean a distinct record, but treating
  `0x0059C30C` as outside the bounded pool is contradicted by exact stride
  arithmetic. This packet records the missing slot-25 classification.
- `EXP-20260813-056` remains valid for slots 2/3. Its wider follow-up claim is
  superseded; the packet did not authorize or classify slots 25/63 readers.
- The common writer/source structure strongly suggests another M1 negative,
  but evidence discipline forbids promoting a shared structure into an exact
  reader/caller result before the residual gates and order are classified.

## Result

Hard-truth verdict: **fail for M2 deferral and exclusive M4.1 activation; pass
for M2.40's declared result, the causal-gate retention, and M4.1 technical
viability**.

Restore M2 to `Active` on exact offline packet M2.41. Return M4/M4.1 to
`Planned` without discarding their technical boundary.

## Follow-up

Execute M2.41 offline only. Reuse the M2.40 first-dword writer set, but
classify the exact consumer gates, call order, reader-time zero reachability,
and M1 intersection only for fixed slot 25 at `0x0059C30C` through
`0x004319CB -> 0x00459620` and fixed slot 63 at `0x0059D6A4` through the five
calls to `0x004467E0/0x00446870`. Stop with an exact causal edge or bounded
negative. Do not add other pool/list objects, readers, resource families,
runtime, mutation, parser/schema work, semantic names, or PS1 evidence.
