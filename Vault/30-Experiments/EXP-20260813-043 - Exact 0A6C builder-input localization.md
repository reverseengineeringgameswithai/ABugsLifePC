---
type: experiment
id: EXP-20260813-043
date: 2026-08-13
question: Which exact differing bytes in record 0x0A6C reach the four-input builder's admission predicates or append inputs?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline native disassembly and exact file comparison
working_directory: /home/dev/ABLPC
configuration: Exact span [0x0A6C,0x0A9C); unchanged/replacement M2.20 files; no runtime
artifacts:
  - static/exports/BIN-97c95ba5572dce63/M2-exact-0a6c-builder-input-localization.md
addresses:
  - 0x00405FE0
  - 0x004069A1
  - 0x0044F8E0
  - 0x0044F99D
file_offsets:
  - 0x0A6C
  - 0x0A90
  - 0x0A94
  - 0x0A98
result: twelve-changed-bytes-reach-four-post-admission-inputs-but-no-differing-admission-input
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/static
  - re/resources
  - re/rendering
---

# EXP-20260813-043 - Exact 0A6C builder-input localization

## Question

Which exact differing byte spans inside only record `[0x0A6C,0x0A9C)` feed
arguments or admission predicates on the native
`0x0044F8E0 -> 0x00405FE0` path, and what is the smallest supported
source-level set?

## Scope

This was offline and PC-native. I compared only the unchanged and replacement
M2.20 work-copy records, then followed native caller and builder
instructions. No game launch, debugger, file edit, source or batch payload
retention, general parser/editor, semantic naming, other record/family, or
PS1 evidence was used.

## Procedure

1. Reverified the authoritative executable and both exact source-file hashes.
2. Enumerated the differing positions only within the 48-byte record.
3. Mapped the fourteen arguments built at call site `0x0044F99D`, including
   partial-register high-half propagation.
4. Traced every direct changed-byte path through `0x00405FE0`, distinguishing
   reads before the append/no-append boundary from reads after the successful
   vertex-count write at `0x004069A1`.
5. Independently checked the caller's table index and sign/zero-derived mode
   for both source files without retaining their raw payload values.

The complete address and offset map is in
`static/exports/BIN-97c95ba5572dce63/M2-exact-0a6c-builder-input-localization.md`.

## Observed

The record has exactly 12 differences in four three-byte spans:

- record `+0x00..+0x02`;
- record `+0x24..+0x26`;
- record `+0x28..+0x2A`;
- record `+0x2C..+0x2E`.

The unchanged bytes at `+0x03`, `+0x27`, `+0x2B`, and `+0x2F` separate the
spans. Caller arguments 3, 6, 12, and 9 respectively carry the four direct
dwords. Partial-register construction also copies changed `+0x2A` or
`+0x2E` into high halves of four other arguments, but the builder reads only
the unchanged low words of those arguments; those duplicate paths are
discarded.

The first direct changed-byte argument read occurs at `0x004069B3`, after
the successful count write at `0x004069A1`. Each three-byte group is then
extracted and ultimately packed into a separate dword at `+0x10` of one of
the four appended vertex records (`0x00406C11`, `0x00406D5B`,
`0x00406EBE`, and `0x00406FFF`). No meaning is assigned to those dwords.

Admission instead consumes unchanged source spans through pointer arguments
1, 4, 7, and 10, an index derived only from unchanged record `+0x2F`, and
per-frame native state. Although changed `+0x2E` is the low byte of the
caller's sign/zero word, that word is positive and nonzero in both files, so
the caller writes the same mode in both.

## Confirmed

- The smallest changed-byte-to-append-input set is all 12 exact positions in
  the four spans above.
- The smallest changed-byte set that can distinguish an admission predicate
  between these files is empty.
- All four changed groups are live as separate conditional append inputs;
  they are not indistinguishable alternatives at this boundary.

## Contradiction and limits

M2.29's exact fresh receipt remains `0/1/0`, but none of this record's source
differences can explain that append decision through native admission data
flow. The receipt is therefore arm-local evidence of admission state, not a
source-stable causal attribution. The changed bytes affect only values built
after admission has already succeeded.

This result does not prove visible causality, format semantics, safe editing,
or why per-frame admission differed. It does not identify any asset,
primitive, material, field, or pixel meaning.

## Result and follow-up

M2.30 is complete. The exact next packet should remain offline and
backward-slice the `0x00405FE0` no-append branches to the smallest non-source,
per-frame input set that could distinguish M2.29's three arms. A future live
predicate receipt, if static design requires it, needs a new exact question
and fresh explicit authority and must remain metadata-only and fail closed.
