---
type: experiment
id: EXP-20261018-010
date: 2026-10-18
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Static disassembly (capstone, a skip-data sweep of all of .text) of retail bugs.exe and the hash-checked Battle Arena LEVEL1.DAT; no game launch
question: Does any code use Battle Arena's undispatched scene record primary.165, or the RAW 0x101/0x102 packets?
result: Neither has a consumer. Record 165 (flags 0x93, masked 0x83) falls outside the scene walker's dispatch range, and no instruction writes or tests flag bit 0x80 or indexes that record. The RAW loader compares tags only up to 0x7F, with no jump table, so 0x101 and 0x102 match no branch, and no other code compares or pushes either value. Both remain runtime-unconfirmed
status: complete-bounded
created: 2026-10-18
updated: 2026-10-18
evidence: [EXP-20260927-001, EXP-20261005-001, EXP-20261012-007]
tags: [experiment/static, re/level-data]
---

# EXP-20261018-010 - Two inert data items

Two of the small closures in section 7 of [[Next Tasks]].

## Battle Arena `primary.165`

[[EXP-20260927-001 - Complete original level Blender maps]] found one scene
record, out of 9,673, that no dispatch case draws. It is Battle Arena's
(engine 13) primary record 165, flags `0x93`, kept as a marker.

- **The record.** It is the last of 166 primary records, at DAT offset
  `0x10C0`. Its payload, at `0x2F18`, is used by no other record and does not
  parse as a sprite group, so its format is not read here.
- **The walker skips it.**
  - The scene walker `0x004498F0` masks the flags with `0xBFEF`, giving
    `0x83`.
  - It dispatches through a byte table only when `masked − 1 ≤ 0x6B`
    (`0x00449939`–`0x0044993F`).
  - `0x82` jumps to the default `0x0044B063`, so the record is never drawn.
- **No code singles it out.** In a skip-data sweep of all of `.text`:
  - **The only masked writes** to a `+0x0E` field are two
    `or byte ptr [esi + 0xe], 0x40` in the DAT loader's relocation pass
    (`0x0044BD34`, `0x0044BD6A`, inside `0x0044BB70`). They set bit `0x40` on
    records that carry a flag bit (`bl`, tested at `0x0044BD30` and
    `0x0044BD66`). That can only raise record 165's masked value to `0xC3`,
    still outside the range. Nothing clears bit `0x80`.
  - **No plain stores to scene records.** The 22 plain stores to `+0x0E`
    (all base registers) are not traced to scene records. They are matrix
    entries (`0x004637A0`, `0x004597B0`), a counter that cycles on
    type-`0x21` entries (`0x0044B81B`), a creature source byte
    (`0x0041BD10`) and similar.
  - **No test of the bit.** No instruction tests bit `0x80` after loading
    `+0x0E`.

  The Battle Arena routine `0x00439410` has no `0xA5` immediate.
- **Inferred.** The bit `0x80` makes the record inert. Without it the low
  bits (3) would select a yaw-facing sprite, which its payload does not
  match. It looks like an authoring leftover.

## The RAW `0x101`/`0x102` packets

EXP-20261005-001 inferred
("strong") that these packets are unused on PC. The loader `0x00465030` has
no case for them, and the character files come from the disc.

- **The full tag list** of `0x00465030`–`0x0046608F` is an if-chain on
  `edi`, with no jump table:
  - texture pages below `0x20`;
  - `0x20`, `0x21`, `0x22`, `0x23` (creatures), `0x24`, `0x25`, `0x26`,
    `0x28`;
  - the range `0x30`–`0x57`;
  - `0x58`–`0x5E`, `0x5F`, `0x7E` and `0x7F`.

  Nothing compares above `0x7F`.
- **Elsewhere.** The full sweep has no `cmp` with, or `push` of, `0x101` or
  `0x102` except `push 0x101` at `0x004B5C68`. That is in `0x004B5C22`,
  whose shape is the C runtime's unwind helper (inferred), and it has
  nothing to do with RAW data.
- **Data.** The early `COPYOFLE.RAW` has no such packets at all
  ([[EXP-20261012-007 - Unused disc content checked offline]]).

## Confirmed, inferred, unknown

- **Confirmed (static, whole image).**
  - Record 165 is skipped by the walker, with or without the loader's bit
    `0x40`, and no instruction clears or tests a flags bit `0x80`.
  - No loader branch handles `0x101`/`0x102`, and no code compares those
    tags.
- **Inferred.**
  - Record 165 is inert data.
  - The `0x101`/`0x102` packets are unused on PC. A computed access, such as
    scanning the decoded RAW for a type id, is not excluded by an
    immediate-value search.
- **Unknown.**
  - Record 165's payload format.
  - **Runtime.** A test image without the `0x101`/`0x102` pairs (and
    another with record 165 removed) would confirm both, as EXP-20261005-001
    proposed.
