---
type: session
date: 2026-08-16
agent: Codex
status: completed
tags: [session, re/static, re/startup, re/direct3d, documentation]
---

# Automatic Direct3D startup documentation

## Goal

Convert the earlier read-only audit into durable startup-reachable Vault
memory without implementing or launching the candidate.

## Work completed

- Re-read the required startup authority and relevant renderer/runtime notes.
- Rehashed the exact retail work copy to `97c95ba5...27b878`.
- Re-read the two command-line parsers, machine probe, WinMain dispatch, and
  chooser control flow from the Ghidra export and native disassembly.
- Re-read the exact code bytes at file `0xA6C6B`, relocation bytes at
  `0xFA912`, PE checksum/security directories, and the paired replacement
  decode.
- Preserved the retained software-versus-hardware log contradiction.
- Recorded [[EXP-20260816-143 - Automatic Direct3D startup static audit]],
  [[PC automatic Direct3D startup candidate]], and
  [[FUNC-97C95BA5572D-004A7600]].
- Added a prominent [[START HERE]] routing note, reconciled KU-013, Current
  State, the Wine baseline, relevant MOCs, function dossiers, and the decision
  boundary.
- Preserved the James ratchet: whole-chooser bypass rejected; paired
  code-plus-relocation candidate accepted only for static plausibility.
- The final read-only James documentation audit returned **ACCEPTED** after
  independently checking the retail hash, both source/replacement spans,
  instruction and jump boundaries, stack slot, cleanup, relocation and PE
  claims, parser census, startup flow, Obsidian links, and limitation wording.
- `make check` passes: Vault 416 notes / 0 errors / 0 warnings, M4 v0.2 five-
  anchor compatibility valid, 610 tests passed, tracked-file audit 0, and
  `git diff --check` clean.

## Result

Agents now learn at startup that there is no native renderer parameter and
that the paired transform is not implemented or runtime-proven. The manual
hardware choice and full six-marker log gate remain authoritative.

No executable, original, work-copy game file, launcher, runtime artifact, or
code was modified. No runtime process was launched.

The final lifecycle audit found no `bugs.exe`, Gamescope, project launcher,
coordinate-overlay, input-movie, Wine-server, or ABLPC private-sink instance;
only the audit command itself matched its search text.

## Next step

Only on a later explicit implementation request: build a hash/byte-guarded,
create-only derived-copy builder, prove exact inverse, execute the complete
fresh runtime discriminator, and require a new James ratchet before changing
the default launcher.
