---
type: experiment
id: EXP-20260813-053
date: 2026-08-13
question: Does the established M1 record or positive-target route produce one of the 20 exact source-record selector words, and can it be signed -103 at 0x0044CE0D?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline PC-native static analysis
environment_version: GNU objdump 2.44; existing Ghidra baseline export
working_directory: /home/dev/ABLPC
configuration: Exact 20-word native producer census and M1-route intersection; no runtime, mutation, parser/schema, semantics, other family, indirect sweep, or cross-port evidence
artifacts:
  - static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json
  - static/exports/BIN-97c95ba5572dce63/M2-signed-selector-producer-provenance.md
addresses:
  - 0x0042DDB0
  - 0x0042DF58
  - 0x00465030
  - 0x0046510F
  - 0x00467D70
  - 0x00467D7F
  - 0x00467E60
  - 0x00467EE9
  - 0x00468BF0
  - 0x00468C9A
  - 0x0041EC40
  - 0x0041EDF8
  - 0x0044D430
  - 0x0044D4FA
  - 0x0044D7A4
  - 0x0044CA00
  - 0x0044CE0D
  - 0x004DE9F0
  - 0x0059D9C0
  - 0x0059DD50
  - 0x005B18E0
  - 0x005B1A7C
result: all-native-selector-producers-classified-m1-minus103-negative
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/static
  - re/resources
  - re/level-data
---

# EXP-20260813-053 - Signed source-record selector provenance

## Question

Does the established M1 record or positive-target route produce any word in
exact set `0x0059D9C0 + i * 0x30`, `0 <= i < 20`, and can that word be signed
`-103` when `0x0044CE0D` selects header `0x005B18E0`?

## Inputs and procedure

- Verified the exact executable SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Enumerated structured references only across the exact 20-record storage
  range and classified native writes to selector offset `+0x00`.
- Checked the PE `.data` raw/virtual boundary to classify the array's initial
  zero-filled image state.
- Resolved the sole nonzero writer, its two direct thunk call sites, its fixed
  source-record pool, slot cursor, index expressions, and image lookup table.
- Extracted all 20 in-range selector/second-word pairs and independently
  checked the table grouping through `0x00416100`.
- Over-approximated both byte-derived lookup formulas against the canonical PE
  image and checked the native immediate follow-on table read for hypothetical
  selector `-103`.
- Intersected the producer call sites and source storage with the established
  normal-update order, M1 root/record walk, dispatcher, and positive-target
  consumer.

No game was launched or instrumented. No executable, asset, parser, schema,
runtime tool, source, or target was modified. No semantics were assigned, no
other index/resource family or whole-program indirect search was opened, and
no PS1 source was consulted.

## Result

Five native functions can write the selector position:

- `0x0042DDB0` conditionally clears individual active records at
  `0x0042DF58`;
- `0x00465030` clears the complete 20-record array at `0x0046510F`;
- `0x00467D70` clears the complete array at `0x00467D7F` before rebuilding
  selected fixed-pool records;
- `0x00468BF0` clears an individual record at `0x00468C9A` when its native
  stream terminates; and
- `0x00467E60` is the sole nonzero writer, storing at `0x00467EE9`.

The array also begins in the PE `.data` zero-fill tail: initialized data ends
at VA `0x004ED400`, below selector base `0x0059D9C0`. The first four native
outcomes are exact zero. `0x00467E60` copies its selector from
one of 20 four-byte image entries at `0x004DE9F0-0x004DEA3F`. Their selector
words are:

```text
5, 3, 8, 2, 7, 7, 6, 7, 4, 10,
9, 1, 6, 6, 6, 6, 14, 13, 11, 11
```

All are positive; none is `0xFF99`. An independent over-approximation of all
255 nonzero branch-byte values and all 4096 zero-branch byte/high-nibble pairs
also finds no canonical-image lookup that yields `0xFF99`. Structured xrefs
record no direct write to the table or wider lookup envelope. Corrupt pointers
or arbitrary indirect mutation remain outside this packet and are not
promoted into producers.

Both nonzero-writer calls receive a member of the same fixed 64-record pool
`[0x0059B628,0x0059D728)` with stride `0x84`. The normal-update call is
`0x0041EDF8` inside `0x0041EC40`, reached from early update `0x004144C0`.
Native order calls that update at `0x0040FFD9`, returns, and only then calls
M1 coordinator `0x0044D430` at `0x0040FFDE`. The coordinator loads M1's
`LEVEL*.DAT`-derived root `0x005BA7E0` at `0x0044D4FA`, walks its 20-byte
records, and calls selector consumer `0x0044CA00` at `0x0044D7A4`.

Neither the selected-record dispatcher nor the exact positive-target consumer
contains a selector writer or destination reference. No current-invocation M1
record, relocated payload, or positive target therefore produces a selector.
Persistent fixed-pool state remains a bounded unknown, but no copy edge from
M1 is proved and the sole native nonzero writer still has no `-103` table
value.

## Independent checks

- Structured range references produced the five-function writer set and the
  three selector-reader/neighbor-writer functions.
- Native disassembly independently confirms every zero store, the only
  nonzero store, both direct calls, exact strides/bounds, and M1 call order.
- Canonical PE byte extraction independently confirms the 20 selector values
  and absence of `0xFF99` in both over-approximated lookup envelopes.
- `0x00467F13-0x00467F20` supplies an additional consistency check: a forced
  selector `-103` would read dword `0x0000000F` from `0x004DE818` as a pointer
  and then attempt to dereference it.
- `EXP-20260812-009/010` independently anchor the M1 selected-record and
  positive-target route; `EXP-20260813-051/052` independently establish the
  normal pre-coordinator order and exact signed-selector candidate.

## Confirmed

- All native selector writers in the declared exact-word surface are
  classified.
- The PE loader supplies the array's initial all-zero state.
- Four writer paths can only clear to zero.
- The sole nonzero writer uses an image table whose 20 native entries are
  positive values `1..14` excluding 12; no entry is signed `-103`.
- The established current-invocation M1 record/positive-target route does not
  produce the writer argument, its table index, or a selector destination.
- M2.38's signed-selector candidate is negative and retired.

## Inferred

The selector array is maintained from the separate fixed-pool update and is
only consumed by the post-record coordinator call. This is the simplest
reading of the exact storage and call order, but it is not promoted into a
whole-lifetime semantic or independence claim.

## Unknown and limitations

- Persistent/copied state across frames could connect wider-lifetime object
  behavior; no exact M1-to-fixed-pool selector edge is evidenced.
- Arbitrary indirect aliases, corrupt source pointers, and malformed table
  indices were outside the authorized whole-program scope.
- The selector, source-record, and associated stream meanings remain unknown.
- `KU-023` remains unresolved because no PC-native M1-to-ID-zero selection
  edge is proved.

## Contradictions and negative results

The M2.37 candidate was addressable but not producible on the reviewed native
lineage. Treating the post-record call as evidence that M1 populated the
selector array would contradict the producer storage and native call order.
No prior accepted evidence was contradicted.

## Result and follow-up

M2.38 is complete with the precise negative required by its done condition.
The candidate is retired, the causal M2 gate remains unsatisfied, and no new
index/resource-family search is opened implicitly. Any successor packet
requires a separate recorded scope decision rather than continuation from
this negative.
