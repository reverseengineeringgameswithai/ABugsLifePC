---
type: experiment
id: EXP-20260814-111
date: 2026-08-14
question: Can one new selector-0x14 record be added to the exact PC Training DAT, survive all required relocations and hardware initialization, and be collected independently of its neighbors?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; Wine 11 Staging; Gamescope; native GDB; complete ignored user-owned PC content copy
environment_version: kernel 7.0.11-200.fc44.x86_64; Wine 11.0 Staging; Gamescope 3.16.25-1.fc44.x86_64; GDB 17.1; Python 3.14.6
working_directory: /home/dev/ABLPC
configuration: complete candidate mapped as Wine Y drive with game at Y:/PC/BUGS; hardware Direct3D 640x480x16; exact Training LEVEL1.DAT recipe only
artifacts:
  - dynamic/wine/EXP-20260814-111-receipt.md
  - static/exports/BIN-97c95ba5572dce63/M3-training-grain-static-trace.md
  - work/copies/M3-training-51-grains-full-disc/evidence/rebuilt-LEVEL1.DAT
  - work/copies/M3-training-51-grains-full-disc/evidence/research/training-51-grains/live-type-3f.bin
addresses:
  - 0x00417720
  - 0x00439E90
  - 0x0044BB70
  - 0x00456A90
  - 0x0059D9B1
  - 0x005C595C
file_offsets:
  - 0x0004
  - 0x03E8
result: accepted-bounded-51-record-collectible
created: 2026-08-14
updated: 2026-08-14
tags:
  - re/experiment
  - re/dynamic
  - re/gameplay
  - re/file-format
  - milestone/m3
---

# EXP-20260814-111 - Training 51st grain collectible vertical slice

## Question

Can one new grain be added somewhere collectible in PC Training, raising its
type-`0x3F` grain-selector census from 50 to 51 without modifying the original
executable or any source material?

## Inputs and bounded comparison

- `bugs.exe` SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- exact source `CD/LEVEL07/LEVEL1.DAT`: 115,060 bytes, SHA-256
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`
- source first top record: file offset `0x4`, type `0x3F`, count 62,
  16-byte entries, range `[0x4,0x3E8)`
- source selector histogram:
  `0x10:1, 0x11:1, 0x12:1, 0x13:1, 0x14:50, 0x23:2, 0x2B:2, 0x2C:4`

The external PS1 source at commit
`1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51` was consulted only to seed the
bounded selector/count hypothesis. [[XPORT-20260814-001 - Training grain selector and count]]
records that comparison. PC static and runtime evidence
below independently establish the PC conclusion.

## Static evidence and recipe

`0x0044BB70` fixes the type-`0x3F` record into pointer slot `0x005C595C`.
`0x00456A90` treats selector `0x14` distinctly while initializing terrain
height. `0x00417720` consumes nearby selector-`0x14` records, writes y sentinel
`0x80000000`, and increments `0x0059D9B1`. Exact address detail is retained in
`M3-training-grain-static-trace.md` and the two new function dossiers.

The recipe appends entry 62 at original file offset `0x3E8`:

| Field | Value |
|---|---:|
| x | `4950` |
| y | `-1301` |
| z | `1127` |
| selector byte | `0x14` |

The point lies between original selector-`0x14` entries 0 and 1. Insertion
changes the first record count `62 -> 63`, moves the remainder of the file by
16 bytes, and increases exactly 556 known file-relative pointer fields by
`0x10`. All other bytes remain recoverable: applying the inverse pointer
changes, restoring count 62, and removing the new entry reconstructs the
source byte-for-byte.

The output is 115,076 bytes at SHA-256
`20d0f9b143a4fceeb058d5ce81680b3e6317995abc3d5ac4103fc85e79b5fd40`.
It reparses with top count 63, primary count 262, secondary count 16, its final
dword unchanged, and exactly 51 selector-`0x14` entries.

## Staging regression and correction

The first launch used a standalone tree containing the game directory but not
the complete `PC/BUGS` drive shape. The user correctly identified corrupt black
level-select panels. Its log reports absolute
`\pc\bugs\cd\level00\level.raw` missing even though the file existed below the
standalone directory, discriminating a launch/staging regression rather than a
DAT-content regression.

(2026-10-12: the rejected standalone tree is `work/copies/M3-training-51-grains`.
Its `LEVEL1.DAT`, `8ab9acd4…`, is an earlier unrelocated insertion, not this
note's output `20d0f9b1…`; it is now quarantined, and KU-082 is closed.)

The corrected candidate is a complete work copy with only
`CD/LEVEL07/LEVEL1.DAT` intentionally changed, mapped as `Y:` so the game runs
at `Y:\PC\BUGS`. The same 394,492-byte level-select RAW now loads, and the
level-select capture is visually normal. This complete-tree/drive-shape
requirement is part of the user-facing recipe.

## Hardware runtime acceptance

The corrected run positively records:

- `Native software render mode is FALSE`;
- `RenderMode set to Direct3d render mode`;
- `Screen mode 640x480x16 selected`;
- `Starting Direct3D renderer`;
- no `INITSOFTRENDER`;
- Training `level1.raw`, modified `level1.dat`, and `terr1.all` loads;
- `---End InitMainGame---` and `NextLife`.

Both the Training title and gameplay captures are visually normal. Exact
artifact hashes and log excerpts are in
`dynamic/wine/EXP-20260814-111-receipt.md`.

## Live table and isolated pickup

At the title, the live type-`0x3F` table contains count 63 and exactly 51
selector-`0x14` entries. New entry 62 is present at the authored coordinates
and has initialized runtime height `-1048`, bracketed by neighboring values
`-1051` and `-1043`.

For the pickup discriminator, the two neighboring original records and new
record were restored, the counter was reset to zero, and the player was placed
inside the new record's pickup radius while remaining outside the two
neighbors. After three seconds:

- `0x0059D9B1` changed `0 -> 1`;
- the new entry y dword became `0x80000000`;
- original entry 0 remained `-1303`;
- original entry 1 remained `-1300`.

This is an isolated PC runtime proof that the added record itself is
collectible and increments the grain counter.

## Counter boundary and contradiction retained

The requested level now contains 51 collectible grain records, and the added
one has been individually collected. A displayed/current total of 51 is not
claimed. Function `0x00439E90` clamps counter `0x0059D9B1` to literal 50 at
`0x0043A0EB–0x0043A0F3`; `0x00417720` also has an exact-50 event test. The
all-51 sequential case was not run. That is a separate bounded gameplay/code
question, recorded as `KU-054`.

### Later correction

`EXP-20260814-112` resolves this experiment's open boundary and corrects one
inference. The cap inside `0x00439E90` exists statically, but was not reached
after a controlled Training `49 -> 50` transition and is not required for a
retained/displayed 51. The Training-specific clamp attribution is therefore
withdrawn; the function's broader identity remains unknown. The later
experiment proves the live HUD already supports 51 and bounds the separate
end-of-level tally patch.

## Implementation

- `reimplementation/ablpc/training_grain_mod.py` implements the exact-hash,
  exact-layout recipe and verifies the selector and relocation census, output
  identity, reparse, and byte-exact inverse.
- `scripts/make-training-51-grains` exposes a no-game-bytes CLI.
- `tests/test_training_grain_mod.py` uses an asset-free synthetic DAT to cover
  relocation, unknown-byte preservation, inverse reconstruction, and rejection
  of wrong/nonretail input.

No asset, screenshot, log containing game output, or DAT entered Git.
`originals/` remained untouched.

## Result

**Accepted at the bounded record-total/individual-pickup boundary.** M3 becomes
Active with M3.1 complete. M2 remains Deferred because this collectible-table
goal was established directly through PC gameplay consumers and does not
resolve M2's separate scene-placement-to-resource dependency gate.

## Follow-up

Completed by [[EXP-20260814-112 - Training 51 counter and tally boundary]].
Choose another concrete gameplay behavior rather than widening the emblem art
or goal presentation without a separate mod request.

## Later authorization correction

[[EXP-20260815-133 - Independent M3 closure authorization hard-truth audit]]
retains this experiment's technical recipe/static result but finds that its
historical runtime receipt does not prove prior authorization for the disclosed
target-state changes and breakpoint work. It therefore cannot independently
satisfy M3 exit gate 1. [[EXP-20260815-134 - Approval-compliant Training runtime receipts]]
supplies a fresh, explicitly authorized, breakpoint-free isolated entry-62
pickup with exact hashes, before/after state, survival, and cleanup. The new
receipt replaces only the milestone-governance role of the historical runtime
arm; it does not alter this experiment's bounded technical claim.
