---
type: experiment
id: EXP-20260815-115
date: 2026-08-15
question: Does exact clean commit 71a22a4 genuinely satisfy the bounded M3.4 FLIKFLIK claim under independent adversarial review?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; system Python and repository virtual environment; ignored user-owned PC work copy; read-only tracked audit
environment_version: Python 3.14.6; pytest 9.1.1
working_directory: /home/dev/ABLPC
configuration: exact clean Git commit 71a22a443def74d437d3f4d00a3a79aa052ca096; no tracked writes; generated material confined below ignored work
artifacts:
  - dynamic/wine/EXP-20260815-114-receipt.md
  - static/exports/BIN-97c95ba5572dce63/M3-training-flikflik-static-trace.md
addresses:
  - 0x00416DF9
  - 0x00417A65
  - 0x004430BD
  - 0x004BBA00
  - 0x004BBB40
  - 0x0086396F
result: accept-exact-m3-4-boundary
created: 2026-08-15
updated: 2026-08-15
tags:
  - re/experiment
  - re/audit
  - re/gameplay
  - milestone/m3
---

# EXP-20260815-115 - Independent M3.4 hard-truth audit

## Verdict

**ACCEPT** at exact clean commit
`71a22a443def74d437d3f4d00a3a79aa052ca096`.

The audit independently attacked the bounded claim in
[[EXP-20260815-114 - Training FLIKFLIK HUD and completion]]. It kept tracked
files read-only, generated only ignored material, and left tracked status
clean.

## Independent reproduction

- `make check` passed with 530 tests, Vault lint at 0 errors/0 warnings, all
  five M4 compatibility anchors valid, and tracked-content audit clean.
- Retail input independently rebuilt final executable SHA-256
  `b572e6d19bc417969c159ba0df7521cbb01b675c260a4dc98d2e6b34475947f4`
  byte-for-byte. Reverse reconstruction produced M3.2 SHA-256
  `8ececefbe1e5747322bd635830f4125500c087d3769094b79545bd7a7b6a4456`
  and then retail SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- The accepted DAT SHA-256 `e9c75bb2...cae7a` independently contains 67
  type-`0x3F` records with originals 50–53 and appended copies 63–66 mapped to
  selectors `0x10`–`0x13`.

## Adversarial static findings

The authored x86 preserves required stack, general-register, and flag
behavior. Its duplicate threshold is exactly record index 63. Scratch
`0x0086396F` clears for every pickup and becomes one only for an incomplete-
to-`0xFF` transition; all four reward gates consume it.

The 576-byte packet occupies verified original executable `0xCC` padding.
PE headers, sections, and directories remain identical. No cave relocation
overlap exists, all eight reused absolute operands retain HIGHLOW relocations,
and all four tally consumers uniquely target the complete 256-byte popcount
table.

Static redirects establish eight centered HUD/tally glyphs and `/8`. The
accepted capture SHA-256 `a37d6848...0e85` visibly establishes `51/50`,
`8/8`, `FLIKFLIK`, and unchanged emblem artwork.

## Runtime linkage audit

The all-eight matrix established bits `1/2/4/8/16/32/64/128` on the
immediately prior candidate. Exact binary comparison proves the final differs
only at three tally emblem-x literals. Separate exact-final runtime evidence
records `0x7F -> 0xFF`, reward `3 -> 4`, scratch one, followed by an
already-complete pickup with reward unchanged and scratch zero. This is a
sufficient identity bridge for the accepted one-shot state claim without
pretending the older matrix ran on different state code.

## Public boundary and hygiene

The CLI rejected wrong hash, overwrite, symlink, source/output identity,
outside-tree, and missing-parent cases without residue; a valid output
preserved mode. Final audit found no owned Wine, Gamescope, GDB, or private
null-sink runtime. The accepted claim remains exact eight-slot Training
`FLIKFLIK`, not a generic word/slot/glyph engine.

## Result

M3.4 is independently accepted at its documented boundary. M3 remains Active;
M2/M5 stay Deferred and completed M4/M6 authorities remain unchanged.
