---
type: experiment
id: EXP-20260813-040
date: 2026-08-13
question: Which exact changed retained entries alter the selected Direct3D batch families in matched control/replacement/control arms?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; Wine 11.0 Staging; Gamescope; GNU GDB 17.1
environment_version: gdb-harness 1.3.0; watch/result schema 4
working_directory: /home/dev/ABLPC
configuration: Fresh Direct3D control/replacement/control; candidate indices 0-7 and 9-23; exact pre/flush/post data watches; digest-only bounded batch intervals
artifacts:
  - static/exports/BIN-97c95ba5572dce63/M2-direct3d-batch-provenance-preflight.md
  - dynamic/wine/EXP-20260813-040-comparison.txt
  - dynamic/wine/RUN-GDB-20260813-113620
  - dynamic/wine/RUN-GDB-20260813-113842
  - dynamic/wine/RUN-GDB-20260813-113954
addresses:
  - 0x004056A0
  - 0x00405838
  - 0x004058D0
  - 0x004059AB
  - 0x00405FE0
  - 0x00407450
  - 0x0044C89E
  - 0x0044C8AB
  - 0x0044F8E0
  - 0x0044F951
  - 0x0045026C
  - 0x004C4108
  - 0x004C410C
  - 0x004C4118
  - 0x0059F7F0
  - 0x005B18E0
result: replacement-count-difference-in-13-exact-candidates-family-a-page-16
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/dynamic
  - re/resources
  - re/rendering
---

# EXP-20260813-040 - Direct3D retained-entry batch provenance

> [!IMPORTANT] M2.28 count-label correction
> `EXP-20260813-041` proves that the retained pre-call set is broader than the
> `B4/B3` decomposition below. Those values count completed four-vertex/
> six-index and three-vertex/three-index append paths inferred from batch
> deltas, not all entries into `0x00405FE0/0x00407450`. The measured counts,
> 13-entry discriminator, roots, pages, and flush result remain unchanged.

## Question

During matched accepted Direct3D control/replacement/control arms, which exact
members of `{0-7, 9-23}` alter either selected Direct3D batch family reached
from the retained-entry `0x0044F8E0` call, including any data hidden by an
in-call flush/reset?

## Approval and renderer gate

The user's explicit M2.27 instruction supplied fresh authority for the bounded
read-only hardware data watches and execution control required by
[[Agent Operating Manual]]. The user also explicitly required confirmation
that the game was in hardware acceleration, not software, and asked that this
be durable. [[START HERE]] now requires every renderer-facing arm to
positively prove all four Direct3D markers and rejects an unproven arm or any
`INITSOFTRENDER` arm.

No point wrote target memory, registers, code, or files. The experiment used
no execution breakpoint, retained no batch payload bytes, armed none of
`0x0044C898/0x0044D794/0x0044D79A`, assigned no primitive/asset/field
semantics, opened no other resource family, and consulted no PS1 source.

## Static preflight

The complete PC-native layout and boundary proof is preserved in
`static/exports/BIN-97c95ba5572dce63/M2-direct3d-batch-provenance-preflight.md`.
Key points are:

- `0x00405FE0` appends four `0x20`-byte vertex records and six indices;
  `0x00407450` appends three and three.
- Both operate on 32 pages. Root `0x004F1730` is reached through
  `0x004C4108`; exact image-initialized root `0x00511510` is reached through
  `0x004C410C`.
- Pre-reset marker stops `0x00405838/0x004059AB` precede all counter zeroing
  in `0x004056A0/0x004058D0`. No other reset/flush callee is reachable from
  the two builders.
- Exact pre stops `0x0044F951/0x0045026C` precede the current entry's first
  selected builder. Exact post `0x0044C8AB` follows return while `ESI` still
  identifies the entry.
- The pre caller receipt uses return `[ESP+0x58] == 0x0044C89E`, preserved
  caller `ESI` at `[ESP+0x04]`, and preserved entry index at `[ESP+0x08]`.
  The original argument slot is invalid there because native
  `0x0044F905` overwrites it with a stream cursor.

## Procedure

1. Reverified exact executable SHA-256 and reused exact M2.20 staging:
   unchanged `FLICK.ALL` SHA-256
   `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`
   in both controls and replacement SHA-256
   `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.
2. Extended the read-only GDB harness to 1.3.0/watch schema 4. Three
   conditioned data watches capture exact pre, pre-reset flush, and post
   events. All pointer/root/page/count/order/address/digest bounds fail closed.
   SHA-256 results contain no payload bytes.
3. Required one warmup rollover and one complete ordered cycle. A candidate
   reaching post with no exact pre is recorded as a zero-builder interval;
   entry 8 is ignored because it is outside the M2.24 candidate set.
4. Ran fresh unchanged/replacement/unchanged arms, each from its exact staged
   tree. Every arm had to prove `Native software render mode is FALSE`,
   `RenderMode set to Direct3d render mode`, `Screen mode 640x480x16
   selected`, `Starting Direct3D renderer`, exact `flick.all` load,
   `NextLife`, no `INITSOFTRENDER`, cleanup/detach, no target signal, and five
   resumed/untraced survival samples.
5. Restored Wine drive `R:` to the pristine derived tree and removed every
   scoped game/Gamescope/null-sink runtime after capture.

## Expected discriminator

Replacement vertex/index counts outside both independent controls select a
smaller exact candidate set. An observed pre-reset flush contributes its
bounded segment before native zeroing. Counter decrease without a captured
flush, invalid root/pointer/page/order/caller, over-bound digest, target
signal, failed cleanup/detach, failed survival, missing hardware marker, or
software rendering rejects the arm.

## Observed

Accepted runs are `RUN-GDB-20260813-113620` (control A),
`RUN-GDB-20260813-113842` (replacement), and
`RUN-GDB-20260813-113954` (control B). Each independently reports:

- `capture_complete` after 417 conditioned data-watch stops;
- three installed/deleted watchpoints, verified cleanup, and detach;
- no target signal and five passing survival samples;
- two rollovers and one complete 23-candidate result;
- all required Direct3D hardware markers, exact load, and `NextLife`, with no
  `INITSOFTRENDER`.

Clock-normalized log prefixes through first `NextLife` are byte-identical,
SHA-256
`4939e81e81c6c7929725f87f2277d0320003ceaefb3a73414dcf4b35f06538f1`.

All selected additions occur only in root family `0x004C4108`, page 16. The
`0x004C410C` family remains zero. No selected entry invokes an in-call flush;
the 32 unmatched marker stops per arm occur outside a pending exact retained-
entry call and are audit metadata only.

Replacement counts lie outside both controls for exact set
`{1,2,4,5,6,7,9,10,14,15,18,19,20}`. The other candidates match both control
counts or are exact zero. Full counts and structural four-input/three-input
builder decompositions are in
`dynamic/wine/EXP-20260813-040-comparison.txt`.

## Independent checks

- Native disassembly accounts for every reachable builder flush/reset and
  proves each marker is before zeroing.
- The two controls independently agree exactly on counts for 19 of 23
  candidates. Their bounded count variance at entries 10, 14, 18, and 19 does
  not erase the result because each replacement count is outside both observed
  control values.
- The append equations independently decompose every measured `(V,I)` into
  integral counts of the two exact completed append paths.
- A synthetic controller regression exercises append, pre-reset flush, reset
  to zero, and a second append while retaining only hashes/metadata.

## Confirmed

- The exact selected Direct3D retained-entry path is active in the tested
  hardware trajectory and uses root family `0x004C4108`, page 16.
- No exact selected candidate flushes either family inside its measured call;
  post intervals therefore contain the complete additions.
- Exact candidates `{1,2,4,5,6,7,9,10,14,15,18,19,20}` have replacement
  vertex/index counts outside both controls. M2.27 reduces 23 candidates to
  this 13-entry set.
- Candidates 21–23 produce zero selected builder additions in all arms.

## Inferred

The 13-entry count set is the strongest current PC-native provenance set for
the M2.20 replacement-local visible result. Count changes show different
numbers of selected builder calls, but do not identify which record or source
byte is visibly causal.

## Contradictions and limitations

- Transformed vertex and batch-relative index hashes vary even between
  controls; they remain audit evidence but are not used to enlarge the exact
  count discriminator.
- Rejected calibration runs `RUN-GDB-20260813-112727` through `113555`
  (listed 2026-10-12 so the run index can match them: `RUN-GDB-20260813-112904`,
  `RUN-GDB-20260813-112939`, `RUN-GDB-20260813-113011`, `RUN-GDB-20260813-113037`,
  `RUN-GDB-20260813-113106`, `RUN-GDB-20260813-113231`, `RUN-GDB-20260813-113414`,
  `RUN-GDB-20260813-113443`, `RUN-GDB-20260813-113555`)
  corrected caller receipt, nullable inactive pages, exact second root,
  entry-8 no-pre behavior, unrelated callers, and conditioned stop limits.
  Every one failed or stopped boundedly, cleaned up, detached, observed no
  target signal, and passed survival. None contributes candidate evidence.
- The result does not prove `.ALL` layout, source-byte meaning, primitive or
  asset identity, pixel attribution, M1 placement identity, general
  replacement compatibility, or behavior outside the tested trajectory.

## Result and follow-up

M2.27 is complete with a smaller exact 13-entry set. M2.28 should remain
offline and PC-native first: within only those entries, use the already proven
`0x24/0x30` walk and native builder-call conditions to enumerate exact changed
record offsets/forms consistent with each measured builder-count delta. Do
not begin a general `.ALL` parser, assign semantics, inspect another family,
or consult PS1; any further live points need a new exact question and fresh
authority.
