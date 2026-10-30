---
type: experiment
id: EXP-20260814-113
date: 2026-08-14
question: Can the exact PC Training FLIK-letter records be moved, duplicated, and removed reversibly, and do four moved duplicates remain independently collectible under the unchanged executable?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; Wine 11 Staging; Gamescope; native GDB; complete ignored user-owned PC content copy
environment_version: kernel 7.0.11-200.fc44.x86_64; Wine 11.0 Staging; Gamescope 3.16.25-1.fc44.x86_64; GDB 17.1; Python 3.14.6
working_directory: /home/dev/ABLPC
configuration: complete candidate mapped as Wine Y drive with game at Y:/PC/BUGS; hardware Direct3D 640x480x16; exact Training LEVEL1.DAT recipe only
artifacts:
  - dynamic/wine/EXP-20260814-113-receipt.md
  - static/exports/BIN-97c95ba5572dce63/M3-training-letter-static-trace.md
  - work/copies/M3-training-duplicate-flik-full-disc/evidence/rebuilt-LEVEL1.DAT
  - work/copies/M3-training-duplicate-flik-full-disc/evidence/research/training-duplicate-flik/live-type-3f-initial.bin
addresses:
  - 0x00417720
  - 0x00417A59
  - 0x00417AB3
  - 0x00417B3B
  - 0x00417BC3
  - 0x00417C77
  - 0x00456A90
  - 0x0059D9B0
  - 0x0059D9B2
  - 0x005C595C
file_offsets:
  - 0x0004
  - 0x0328
  - 0x0338
  - 0x0348
  - 0x0358
  - 0x03F8
result: accepted-bounded-move-duplicate-remove-with-repeated-completion-boundary
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - re/dynamic
  - re/gameplay
  - re/file-format
  - milestone/m3
---

# EXP-20260814-113 - Training FLIK letter transformations

## Question

Can the four exact PC Training letter-selector records be moved, duplicated,
or removed without losing unknown bytes, and does an accepted demo containing
one moved duplicate of each selector load and collect correctly?

## Exact data boundary

The input is the accepted M3.1 Training DAT: 115,076 bytes, SHA-256
`20d0f9b143a4fceeb058d5ce81680b3e6317995abc3d5ac4103fc85e79b5fd40`.
Its first type-`0x3F` table has count 63 and exactly one record for each
selector `0x10`, `0x11`, `0x12`, and `0x13` at indices 50–53/file offsets
`0x328`–`0x358`.

The implementation treats these as the collective FLIK-letter set because
they converge on the four-bit completion mask in PC function `0x00417720`.
Exact selector-to-visible-glyph identity was not separately discriminated, so
individual claims remain selector-addressed.

The accepted recipe appends copied records at deliberately moved positions:

| Selector | New index | Authored position |
|---:|---:|---|
| `0x10` | 63 | `(4900,-50,1500)` |
| `0x11` | 64 | `(5100,-50,1000)` |
| `0x12` | 65 | `(5000,-50,500)` |
| `0x13` | 66 | `(4900,-50,0)` |

All non-coordinate bytes are copied exactly from the corresponding original.
The 64-byte table growth changes count 63 to 67 and relocates the same 556
known PC file-relative fields by `0x40`. The output is 115,140 bytes at
SHA-256 `e9c75bb24ae0d0f4f74d17ea63431195e49b7e5278c089588d9372b8eb8cae7a`,
reparses, preserves 51 grain selectors, contains two of each letter selector,
and inverses to the input byte-for-byte.

Synthetic fixtures independently cover positive and negative table growth:
move plus duplicate plus remove, removal of all four, unknown-tail-byte
preservation, pointer relocation, exact inverse, and invalid/ambiguous input
rejection.

## PC static path

`0x00456A90` initializes the moved non-`0x14` records through its alternate
terrain/correction route. `0x00417720` consumes a nearby record at
`0x00417A30`, then maps selectors `0x10`–`0x13` to mask bits 1, 2, 4, and 8 at
case addresses `0x00417A59`, `0x00417AB3`, `0x00417B3B`, and `0x00417BC3`.
Each case tests the resulting mask against `0x0F`.

The equality path increments byte `0x0059D9B0` while below nine. It does not
test whether the prior mask was already `0x0F`, predicting that duplicate
letters can retrigger the normal completion/reward path.

## Hardware runtime acceptance

The complete candidate tree boots the unchanged executable through Direct3D
640x480x16, loads the modified Training DAT and terrain, and reaches
`---End InitMainGame---` plus `NextLife`. A pre-perturbation live table has
count 67, retains the four originals, and contains terrain-initialized moved
copies at indices 63–66.

Four isolated pickup discriminators independently produce mask transitions
`0 -> 1`, `0 -> 2`, `0 -> 4`, and `0 -> 8`. In every case, the selected moved
copy alone changes its y dword to consumed sentinel `0x80000000`; the original
same-selector record remains intact.

## Repeated-completion boundary

The static prediction is confirmed. Starting with mask 15 and reward byte 1,
collecting duplicate selector `0x11` consumes only index 64, leaves original
index 51 intact, retains mask 15, and changes the reward byte `1 -> 2` before
reaching `0x00417C77`.

The accepted demo therefore supplies extra collectible instances but not
one-shot completion semantics. Suppressing the repeated event would be a
separate executable behavior change; it is not silently folded into this
data-only recipe.

## Method correction

Continuing under GDB from execution breakpoints at `0x00417A59` and
`0x00417C77` produced same-PC Wine page faults. Those continuation arms are
rejected. Accepted pickup evidence uses a single hardware breakpoint, records
state, and detaches without debugger continuation. The runtime survived those
bounded arms normally.

## Implementation

- `reimplementation/ablpc/training_letter_mod.py` provides the exact public
  duplicate-FLIK recipe and public hash-locked
  `transform_training_letter_records` move/duplicate/remove helper.
- `scripts/make-training-duplicate-flik` writes only a new file below
  `work/copies/` and refuses overwrite, links, source/output identity, or wrong
  input.
- `tests/test_training_letter_mod.py` uses only an independently created
  synthetic fixture.

No game byte, screenshot, runtime log, or debugger dump enters Git.
`originals/` remains untouched.

## Result

**M3.3 complete at the bounded moved-duplicate/repeated-completion boundary.**
The recipe demonstrates all three intended record operations—move, duplicate,
and remove—and the accepted output duplicates all four existing letter
selectors at new positions. M3 remains Active; M2/M5 remain Deferred and
completed M4/M6 authorities are unchanged.

## Follow-up

Choose a different concrete gameplay behavior such as a trigger/checkpoint or
collision/traversal edit. Revisit letter completion only if a distinct user
goal requires suppressing or redesigning the repeated reward.

## Later authorization correction

[[EXP-20260815-133 - Independent M3 closure authorization hard-truth audit]]
retains this experiment's exact recipe/static result but finds that its
historical runtime receipt does not prove prior authorization for the disclosed
state resets, position writes, and hardware breakpoints. It therefore cannot
independently satisfy M3 exit gate 1. [[EXP-20260815-134 - Approval-compliant Training runtime receipts]]
supplies a fresh, explicitly authorized, breakpoint-free selector-`0x10`
duplicate pickup with exact hashes, isolated original/duplicate state,
survival, and cleanup. It corrects only that milestone-governance defect; the
other selector and repeated-completion boundaries above remain technically
retained rather than freshly re-run.
