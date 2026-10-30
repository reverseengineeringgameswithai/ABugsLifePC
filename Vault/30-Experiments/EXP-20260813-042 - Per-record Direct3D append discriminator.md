---
type: experiment
id: EXP-20260813-042
date: 2026-08-13
question: Which individual calls append among M2.28's 124 exact records, and which outcomes differ outside both fresh controls?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; Wine 11.0 Staging; Gamescope; GNU GDB 17.1
environment_version: gdb-harness 1.4.0; watch/result schema 5
working_directory: /home/dev/ABLPC
configuration: Fresh Direct3D control/replacement/control; exact 168-call plan; retain only 124 candidate offsets as append booleans/counts
artifacts:
  - static/exports/BIN-97c95ba5572dce63/M2-per-record-append-preflight.md
  - dynamic/wine/EXP-20260813-042-comparison.txt
  - dynamic/wine/RUN-GDB-20260813-124153
  - dynamic/wine/RUN-GDB-20260813-124414
  - dynamic/wine/RUN-GDB-20260813-124610
addresses:
  - 0x00405838
  - 0x004059AB
  - 0x004069A1
  - 0x00407B00
  - 0x0044F951
  - 0x0045026C
  - 0x0044C8AB
file_offsets:
  - 0x0A6C
result: one-exact-replacement-local-append-outcome-at-0x0a6c
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/static
  - re/dynamic
  - re/resources
  - re/rendering
---

# EXP-20260813-042 - Per-record Direct3D append discriminator

## Question

Within only M2.28's 124 exact changed records, which individual calls append
in fresh control/replacement/control evidence, and which exact record outcomes
differ outside both controls?

## Authority and scope

The user's explicit instruction to proceed with M2.29 supplied fresh authority
for the bounded read-only metadata capture after a sound static design. No
target memory, register, code, or game file was written. No execution
breakpoint or quarantined address was armed. No source, vertex, or index
payload byte was read or retained. No semantic field, primitive, asset, or
identity name was assigned; no parser, other family, or PS1 source was used.

## Static preflight

Exact native disassembly proves:

- `0x00405FE0` writes its selected vertex count only at `0x004069A1`, adding
  four after six family-specific index increments;
- `0x00407450` writes its selected vertex count only at `0x00407B00`, adding
  three after three family-specific index increments;
- all earlier rejection edges reach `0x0040702F` or
  `0x00407469/0x00407E8C` without a selected counter change;
- the only reachable resets remain behind pre-reset marker stops
  `0x00405838/0x004059AB` established by `EXP-20260813-040`.

The complete address/edge map and fail-closed state machine are in
`static/exports/BIN-97c95ba5572dce63/M2-per-record-append-preflight.md`.

## Procedure

1. Reverified the exact executable and staged file hashes.
2. Extended the compatible read-only GDB harness to 1.4.0/spec schema 5.
   Purpose-specific `record_outcome` mode validates the complete exact
   168-call entry/offset/form plan but retains results only for M2.28's 124
   candidate offsets. It snapshots allowlisted roots/pointers/counters only.
3. Used the existing three safe conditioned data watches at the exact
   pre-call, pre-reset flush, and entry-post boundaries. Each completed call
   had to produce exactly no delta, form `0x3C` delta `(4,6)`, or form `0x34`
   delta `(3,3)`; candidate appends were restricted to root `0x004C4108`,
   page 16.
4. Ran fresh unchanged/replacement/unchanged arms. Each had to prove all four
   positive Direct3D markers, the exact selected load, `NextLife`, no
   `INITSOFTRENDER`, complete ordered capture, cleanup/detach, no target
   signal, and five resumed/untraced survival samples.
5. Selected an exact record only when both controls agreed and replacement
   had the opposite append boolean.

## Observed

Accepted runs are `RUN-GDB-20260813-124153` (control A),
`RUN-GDB-20260813-124414` (replacement), and
`RUN-GDB-20260813-124610` (control B). They retain respectively 62, 64, and
57 positive outcomes among the 124 candidates. Every arm completes two
rollovers and one captured cycle, has zero selected flushes, retains no
payload, and passes every runtime acceptance gate.

The controls disagree on 13 records. One exact outcome lies outside both:

- entry 7, file offset `0x0A6C`, form `0x3C`: control A does not append,
  replacement appends four vertices/six indices, and control B does not
  append (`0/1/0`).

No other candidate differs from both controls. The complete outcome-pattern
comparison is in `dynamic/wine/EXP-20260813-042-comparison.txt`; all 124 exact
rows remain in each accepted `result.json`.

## Contradiction and temporal scope

The three single-record outcomes isolated from M2.27 aggregates do not
reproduce: fresh outcomes at `0x0174`, `0x0858`, and `0x0AA4` are `1/1/1`,
`1/1/1`, and `0/0/0`, rather than M2.27's `1/0/1`, `1/0/1`, and `0/1/0`.
This does not invalidate either within-arm measurement or the native count
model. It independently confirms that post-call admission is per-frame and
that those older outcomes are not source-stable across fresh launches. The
contradiction is preserved rather than silently resolved.

Rejected `RUN-GDB-20260813-123859` attached before the natural title, reached
1,000 unmatched flush-marker stops, and failed closed at `max_stops` before a
candidate pre-call. Cleanup, detach, signal, and survival receipts passed; it
contributes no outcome evidence.

## Confirmed

- Exact offset `0x0A6C`, form `0x3C`, is the smallest replacement-local
  append-outcome set supported by these fresh matched arms.
- Every positive candidate outcome uses the proven first root/page, and no
  selected call flushes in any accepted arm.
- Schema 5 can retain per-record booleans/counts without retaining protected
  payload bytes.

## Unknown and limitations

- Which differing source byte or builder input makes `0x0A6C` pass only in
  the replacement arm.
- Whether its append is responsible for any pixel in M2.20's visible result.
- Record-field, primitive, material, asset, and identity meanings.
- Behavior outside this exact trajectory, file pair, executable, and three
  fresh arms.

## Result and follow-up

M2.29 is complete at one exact record outcome. M2.30 should remain offline:
within only record `0x0A6C`, map exact differing byte spans through
`0x0044F8E0`'s argument construction into `0x00405FE0`'s admission predicates.
Preserve multiple source alternatives unless native data flow distinguishes
them. Do not infer visible causality, create general `.ALL` tooling, inspect
another family, consult PS1, or begin another runtime without a new exact
question and fresh authority.
