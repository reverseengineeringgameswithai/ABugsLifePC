---
type: experiment
id: EXP-20260815-114
date: 2026-08-15
question: Can the exact PC Training eight-letter demo own eight independent pickup bits, complete only on the first transition to all eight, and render centered FLIKFLIK in both the HUD and level-complete tally?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; Wine 11 Staging; Gamescope; native GDB; complete ignored user-owned PC content copy
environment_version: kernel 7.0.11-200.fc44.x86_64; Wine 11.0 Staging; Gamescope 3.16.25-1.fc44.x86_64; GDB 17.1; Python 3.14.6
working_directory: /home/dev/ABLPC
configuration: complete M3.3 candidate mapped as Wine Y drive with game at Y:/PC/BUGS; hardware Direct3D 640x480x16; exact M3.2 executable composition plus M3.4 recipe
artifacts:
  - dynamic/wine/EXP-20260815-114-receipt.md
  - static/exports/BIN-97c95ba5572dce63/M3-training-flikflik-static-trace.md
  - work/copies/M3-training-flikflik-full-disc/evidence/m34-accepted-nested-receipt.json
  - work/copies/M3-training-flikflik-full-disc/evidence/runtime/accepted-final-tally-16.png
addresses:
  - 0x00416890
  - 0x00416DF9
  - 0x00417720
  - 0x00417A59
  - 0x00417AB3
  - 0x00417B3B
  - 0x00417BC3
  - 0x00442E70
  - 0x004430BD
  - 0x004BBA00
  - 0x004BBB40
  - 0x0059D9B0
  - 0x0059D9B2
  - 0x0086396F
file_offsets:
  - 0x0161F9
  - 0x0424BD
  - 0x0BAE00
result: accepted-exact-eight-slot-flikflik-with-one-shot-completion
created: 2026-08-15
updated: 2026-08-15
tags:
  - re/experiment
  - re/dynamic
  - re/static
  - re/gameplay
  - re/hud
  - milestone/m3
---

# EXP-20260815-114 - Training FLIKFLIK HUD and completion

## Question

Can the accepted eight-letter Training DAT be paired with a reversible
executable recipe so all eight pickups own independent mask bits, the normal
completion/reward event occurs once, and the in-level HUD plus end tally
display centered `FLIKFLIK` with an `8/8` count?

## Exact boundary

The input executable is retail `bugs.exe`, 1,069,056 bytes at SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
The builder first reproduces the accepted M3.2 intermediate
`8ececefbe1e5747322bd635830f4125500c087d3769094b79545bd7a7b6a4456`,
then applies 29 exact spans. The final executable is the same size at SHA-256
`b572e6d19bc417969c159ba0df7521cbb01b675c260a4dc98d2e6b34475947f4`.
Both inverse stages reconstruct their inputs byte-for-byte.

The paired Training DAT is the accepted M3.3 output: 115,140 bytes at SHA-256
`e9c75bb24ae0d0f4f74d17ea63431195e49b7e5278c089588d9372b8eb8cae7a`.
Its original selectors remain at indices 50–53 and appended copies at 63–66.
No game-bearing output enters Git.

## Static implementation evidence

The authored packet is 576 bytes at VA `0x004BBA00` / file offset `0x0BAE00`,
SHA-256
`0d32f7fadf1dd7ccbfaba8689e9bb3a95278fcc7e6ab161084359e5eb27f8370`.
It occupies original `0xCC` linker padding and contains the two draw helpers,
four selector entry points, eight tally x positions, and a complete 256-byte
popcount table at `0x004BBB40`. New global reads are call/pop-relative.

The selector helpers distinguish record indices 50–53 from 63–66 and map
them to bits `1/2/4/8/16/32/64/128` in byte `0x0059D9B2`. Scratch byte
`0x0086396F` becomes one only for an incomplete-to-`0xFF` transition; the four
retained reward gates compare that byte with one. It is the final byte before
the original writable `.data` virtual end at `0x00863970`, outside raw data,
with no direct retail static reference. Existing absolute operands retain
their eight original HIGHLOW relocations.

The in-level renderer at `0x00416DF9` is replaced by an eight-slot helper with
x positions `64,88,112,136,160,184,208,232`. The tally renderer at
`0x004430BD` uses `66,90,112,132,160,184,206,226`, draws `FLIKFLIK`, reports
`/8`, and gates the existing emblem on eight. PE headers, all six section
tuples, and total file size remain unchanged. See the static trace for every
span and relocation.

## PC runtime acceptance

The exact final executable and M3.3 DAT booted the complete candidate through
Direct3D 640x480x16, loaded Training, and reached `---End InitMainGame---`
plus `NextLife`.

The all-eight pickup matrix established bits `1/2/4/8` for the originals and
`16/32/64/128` for the appended copies. On the exact final hash, a controlled
`0x7F -> 0xFF` pickup changed the reward byte to four and scratch to one. A
separate already-complete pickup retained mask `0xFF` and reward four while
scratch remained zero. Thus the accepted behavior is a transition, not an
equality retrigger.

Natural level-done state then entered the ordinary tally caller. The accepted
clear-phase frame visibly contains `51/50`, `8/8`, centered `FLIKFLIK`, and
the existing silver emblem at the left. The first candidate had placed the
emblem at x=32, visibly overlapping the first F; it was rejected. Moving only
the three exact emblem-x literals to x=0 produced the final accepted hash and
frame.

## Method correction

Execution breakpoints inside the hot HUD/tally loops at `0x00416890` and
`0x00443612` caused same-PC Wine WOW64 faults. A direct inferior call to the
draw routine also caused a GDB internal backtrace. No conclusion from those
arms is retained. The accepted final tally capture uses natural level-done
state plus external process scheduling, without an executable breakpoint.

## Implementation

- `reimplementation/ablpc/training_flikflik_mod.py` provides the exact
  composed recipe, exact-span checks, final hash pin, and inverse proof.
- `scripts/make-training-flikflik` writes only a fresh regular file under
  `work/copies/`, refuses linked/overwriting outputs, and preserves mode.
- `tests/test_training_flikflik_mod.py` pins code identity, redirects,
  transition gates, full popcount coverage, layout literals, exact inversion,
  byte preservation, and refusal cases.

## Result

**M3.4 is complete at the exact eight-slot `FLIKFLIK` boundary.** Eight
independent pickups, one-shot completion, centered in-level/tally rendering,
and `8/8` are accepted. This does not establish an arbitrary-word engine,
other glyph families, other slot counts or levels, new emblem artwork, or
save-format generalization. M3 remains Active and M2/M5 remain Deferred.

Independent [[EXP-20260815-115 - Independent M3.4 hard-truth audit]] accepts
this exact boundary after a fresh build/inverse, x86/PE/relocation/state audit,
runtime-identity linkage review, CLI refusal matrix, and full repository gate.

## Follow-up

Prefer the next concrete M3 edit from a different stream, such as a bounded
trigger/checkpoint or collision/traversal change. Revisit this HUD only when a
new goal requires a genuinely generic word/layout system.
