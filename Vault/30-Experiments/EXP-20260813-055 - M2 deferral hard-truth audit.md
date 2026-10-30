---
type: experiment
id: EXP-20260813-055
date: 2026-08-13
question: Does the evidence support deferring M2 and making M4.1 the sole active packet, or did the disposition overlook a finite PC-native M2 candidate?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; adversarial offline evidence audit
environment_version: Git 2.54.0; GNU objdump 2.45.1
working_directory: /home/dev/ABLPC
configuration: Read-only premise audit of EXP-20260813-054; existing PC static/runtime/implementation evidence plus exact local work-copy hash recheck; no runtime, mutation, parser/schema change, new resource family, whole-program indirect search, or cross-port evidence
artifacts:
  - static/exports/BIN-97c95ba5572dce63/M2-deferral-hard-truth-audit.md
  - static/exports/BIN-97c95ba5572dce63/M2-generic-resource-index-producer-census.md
  - static/exports/BIN-97c95ba5572dce63/M2-signed-selector-producer-provenance.md
addresses:
  - 0x0041C420
  - 0x0041C430
  - 0x00436B40
  - 0x004372A2
  - 0x004372B7
  - 0x00437337
  - 0x0043734C
  - 0x0059B628
  - 0x0059B730
  - 0x0059B7B4
  - 0x0059D728
  - 0x005B18E0
file_offsets: []
result: m2-deferral-premature-fixed-pool-index-candidate-restores-active-m2
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/resources
  - re/milestone-audit
  - implementation/modding
---

# EXP-20260813-055 - M2 deferral hard-truth audit

## Question

Does the evidence support deferring M2 and making M4.1 the sole active packet,
or did `EXP-20260813-054` overlook a finite PC-native M2 candidate?

## Method

The audit attempted to falsify each premise of the disposition rather than
restate it. It reread `EXP-20260813-049` through `EXP-20260813-054`, followed
their cited PC static artifacts back to native instructions, compared the
roadmap before and after M2.39, checked the existing implementation boundary,
recalculated the fixed-pool addresses, and independently rehashed the exact
executable plus the two user-owned M4.1 files in the ignored work copy. It also
checked tracked paths for protected game-data extensions.

No game was launched or instrumented. No memory, register, executable, asset,
parser, manifest, schema, or runtime tool was changed. No PS1 source was
consulted.

## Observed

### Premises that survive

- M2's first exit gate and `KU-023` remain unresolved. The separate M1 and
  ID-zero rendered chains still lack an exact causal selection edge.
- M2.38's signed-selector negative remains supported at its declared boundary.
- M4.1 remains technically viable: both exact local work-copy files are
  13,548 bytes and match the hashes recorded by `EXP-20260812-033/049`.
  The audit found no protected game-data extension among Git-tracked paths.

### Premise that fails

`EXP-20260813-054` accurately stated that no successor had been *ranked*, but
then treated that scheduling fact as if the evidence contained no finite
candidate. `EXP-20260813-051` had already preserved two exact unresolved
inputs in generic header reader `0x00436B40`:

- `0x0059B730` at `0x004372A2-0x004372B7`; and
- `0x0059B7B4` at `0x00437337-0x0043734C`.

Each first dword is used as `I` in `0x005B18E0 + I * 4`, where exact zero
selects the ID-zero header. The two addresses are exactly the first dwords of
slots 2 and 3 in the already bounded 64-record pool
`[0x0059B628,0x0059D728)` with stride `0x84`. Native disassembly at
`0x0041C424-0x0041C430` independently confirms a full `0x2100`-byte zeroing
of that pool, and `0x0041C58A-0x0041C597` confirms 64 destination records with
stride `0x84`.

Initial zero does not prove zero at either reader, and neither address has a
proved M1 producer. That is why the surface is a next experiment, not a
conclusion. But it is exact, finite, PC-native, in the already reviewed
resource-index family, and directly discriminates ID zero. The M2.39 audit did
not classify its writers/producers. Deferral was therefore premature.

## Confirmed

- The prior conclusion does not survive intact: M2 must not be complete, but
  it should return to `Active` for one exact offline producer census.
- The active surface is restricted to fixed-pool first dwords
  `0x0059B730/0x0059B7B4`; it does not authorize an arbitrary persistent-state
  sweep, another resource family, or a whole-program indirect search.
- M4.1's evidence and safety boundary survive, but its priority conclusion
  does not. M4.1 returns to `Planned` rather than being discarded.

## Inferred

The two words are the best next M2 candidate because they are the smallest
unresolved surface already cited by the generic-reader census, occupy one
finite fixed pool, and can select the exact ID-zero header without signed or
alias arithmetic. This ranking is a roadmap inference; it does not assert
their values or provenance.

## Unknown and limitations

- Whether either word is zero at the exact native read.
- Every native direct or bounded dynamic writer that can reach slots 2 and 3.
- Whether a reader-time value is derived from an M1 20-byte record, relocated
  payload, positive target, or copied cross-frame state.
- Whether completing that census yields the causal edge or another precise
  negative.
- General `.ALL` layout, identity, and compatibility remain unknown.

## Result

Hard-truth verdict: **fail for M2 deferral and exclusive M4.1 activation; pass
for M2 gate retention, the M2.38 finite negative, and M4.1 technical
viability**. Restore M2 and exact offline packet M2.40 to `Active`; return M4
and M4.1 to `Planned`.

## Follow-up

Execute M2.40 offline. Enumerate and classify every native direct or bounded
fixed-pool writer that can produce the first dwords at
`0x0059B730/0x0059B7B4`; establish caller order and source lineage; test exact
zero reachability at `0x004372A2/0x00437337`; and test whether either value is
derived from the established M1 record/payload route. Stop with either an
exact causal edge or a precise finite negative. Do not widen the surface or
perform runtime/mutation work without a separate authorization packet.
