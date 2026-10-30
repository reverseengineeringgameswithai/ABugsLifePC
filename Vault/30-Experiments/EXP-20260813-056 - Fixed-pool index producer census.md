---
type: experiment
id: EXP-20260813-056
date: 2026-08-13
question: Can fixed-pool slots 2 or 3 hold zero at the exact generic header-index reads, and does any such value derive from the established M1 record or payload route?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline PC-native static analysis
environment_version: GNU objdump 2.46-3.fc44; existing Ghidra structured evidence export
working_directory: /home/dev/ABLPC
configuration: Exact-hash work-copy executable; direct and bounded fixed-pool producer census restricted to first dwords 0x0059B730/0x0059B7B4; no runtime, mutation, parser/schema work, semantic renaming, other pool/index/resource family, or cross-port evidence
artifacts:
  - static/exports/BIN-97c95ba5572dce63/M2-fixed-pool-index-producer-census.md
  - static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json
addresses:
  - 0x00414597
  - 0x004145BB
  - 0x0041BBBA
  - 0x0041BD24
  - 0x0041C430
  - 0x0041CE5F
  - 0x0041ECF7
  - 0x0041EEE4
  - 0x004372A2
  - 0x00437337
  - 0x0046574D
  - 0x00599EB0
  - 0x0059B730
  - 0x0059B7B4
file_offsets: []
result: reader-time-zero-statically-reachable-but-level-raw-state-derived-and-m1-negative
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/resources
  - re/static
  - re/provenance
---

# EXP-20260813-056 - Fixed-pool index producer census

> [!warning] Follow-up superseded
> `EXP-20260813-057` preserves this packet's complete slot-2/slot-3 result but
> rejects its M2 deferral. Exact fixed-pool slots 25 and 63 remained excluded
> or misclassified and now define M2.41.

## Question

What native direct or bounded fixed-pool writers can produce first dwords
`0x0059B730/0x0059B7B4`, can either word equal zero at the exact
`0x00436B40` reads, and does either lineage derive from the established M1
20-byte record, relocated payload, or positive-target route?

## Method

I independently rehashed the exact work-copy executable, enumerated all
structured references over pool `[0x0059B628,0x0059D728)`, disassembled the
target readers and every direct or bounded record-first-dword writer, resolved
all callers of the two shared writer helpers, and followed the selected source
fields back through scene initialization. I then checked the exact per-frame
ordering and the reader's `+0x5C`/`+0x44` gates.

The bounded active-record closure included the generic update helpers and all
callbacks installed by `0x0041C420`. Exact-address passes through
`0x00428BB0`, `0x0041DC20`, and `0x00414F80` were also classified rather
than treating an address reference as a write.

No game process was launched or changed. No source, executable, asset,
runtime state, parser, schema, or tool was modified. No PS1 evidence was
consulted.

## Observed

### Exact writer set

Three native store classes can reach both target first dwords:

1. `0x0041C430` clears the complete `0x2100`-byte pool to zero.
2. `0x0041BD24` stores the zero-extended byte at retained source `+0x0C`.
   Its in-pool calls are `0x0041C559`, `0x0041ED3A`, and `0x0043213E`;
   `0x00436257` targets out-of-pool record `0x0059C9C0`.
3. `0x0041BBBA` conditionally zeros an active record when mode bit 2 is set
   and record `+0x62 == 0`. Of its direct callers, only the mode-2 call at
   `0x0041EEE4` can reach that store.

The structured export contains no other direct record-first-dword write. The
bounded generic update, installed callback, exact-address helper, and resource
batch closures contain no additional store to record `+0x00`.

### Source lineage

Slots 2 and 3 correspond to source records `0x00599EE8` and `0x00599F04`.
`0x0046574D-0x0046576A` copies the entire source table from parsed
`LEVEL.RAW` packet type `0x23`. `0x0041C458` skips source records whose
`+0x0C` byte is zero; only its nonzero branch stores the retained source
pointer and calls `0x0041BD10`. Consequently, the copier cannot write zero to
a valid initialized record. Its record `+0x62` input comes from source
`+0x11` at `0x0041BD60-0x0041BD65`.

### Reader-time zero

Initial clear zero cannot pass the reader: `0x0041EC40` clears `0x4000` from
every record and restores it only after a positive first-dword gate. The late
removal store can pass. `0x0041ECF7` sets `0x4000` before active-list
processing; mode-2 removal later writes zero at `0x0041BBBA` without clearing
record `+0x5C` or `+0x44`. `0x0041CE5F` supplies a concrete native
record-`+0x6C = -20` state, and `0x0041EE7D-0x0041EE87` advances it to zero
and branches to the mode-2 call.

Main-update order is exact: `0x00414597` reaches `0x0041EC40`, and only later
does `0x004145BB` dispatch through `0x00418780`; case 9 reaches the selected
reads. Native control/data flow therefore permits zero at either reader when
the cited source/state predicates hold. This packet did not observe those
predicate values in a particular unchanged scene.

## Confirmed

- The complete direct and bounded fixed-pool first-dword writer set at the
  declared surface is `0x0041C430`, `0x0041BD24`, and `0x0041BBBA`.
- Initial zero and copier zero do not reach the indexed reads for a valid
  record; conditional removal zero can.
- The value and zero predicate lineages are constant initialization, separate
  `LEVEL.RAW` type-`0x23` source fields, and fixed-pool runtime state.
- None derives from an M1 20-byte record, relocated payload, or positive
  target at the declared boundary.

## Inferred

This makes the removal path a real native ID-zero selection possibility for
the generic reader, not evidence that slots 2 or 3 select ID zero in a named
unchanged scene. Source-field and pool-state meanings remain unidentified.

## Contradictions and limitations

- `EXP-20260813-055` correctly rejected the claim that the exact surface was
  already exhausted. The completed census now closes that omission, but its
  conclusion is more precise than either "the words cannot be zero" or "the
  initial clear selects ID zero."
- Static reachability does not establish the concrete source bytes or state
  sequence for every shipped scene. That limitation does not preserve an M1
  candidate: every proven value/predicate source is outside the M1 route.
- No meaning is assigned to source `+0x0C`, source `+0x11`, record `+0x62`,
  or record `+0x6C`.

## Result

M2.40 is complete with a bounded causal negative. Reader-time zero is
statically reachable through conditional removal, but the path is derived
from separate `LEVEL.RAW` plus fixed-pool state. No exact M1-derived ID-zero
selection edge is present at this surface.

## Follow-up

Retire the fixed-pool candidate without widening to another persistent object,
pool, index, or resource family. Keep `KU-023` and the M2 causal gate open;
defer M2 until a separately cited PC-native candidate or concrete mod goal
supplies a finite discriminator. Resume the already evidence-backed M4.1
exact whole-file replacement manifest packet as the sole active work packet.

This priority conclusion is superseded by `EXP-20260813-057`; the result above
remains valid only for the declared slot-2/slot-3 surface.
