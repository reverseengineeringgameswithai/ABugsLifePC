---
type: implementation
status: bounded
platform: Windows PC under Wine
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
evidence:
  - EXP-20260815-128
  - EXP-20260815-130
created: 2026-08-15
updated: 2026-08-17
tags:
  - implementation/runtime
  - re/safety
  - milestone/m3
---

# PC Flik teleport procedure

## Scope

This is the durable procedure for user-authorized runtime teleport diagnostics
against the exact retail PC executable. It is not a pristine/no-write method,
does not establish controller reachability, and must not be used to label an
event natural gameplay.

## Position layout

All components are signed little-endian 32-bit integers:

| Triple | Addresses | Role |
| --- | --- | --- |
| current XYZ | `0x0059D910/14/18` | current live Flik position |
| preceding XYZ | `0x0059D920/24/28` | preceding distinct position |
| auxiliary XYZ | `0x0059D960/64/68` | auxiliary/reset coordinate; not live airborne position |

The layout is confirmed in [[STRUCT-PC-FLIK-POSITION-GLOBALS]]. Level03's Y
increases downward in the observed fall traces. Coordinates are level-specific.

## Mandatory preflight

Before a write:

1. Require explicit authorization for the position mutation and its purpose.
2. Use a copy below `work/`; never run against or write `originals/`.
3. Resolve exactly one owned `bugs.exe` and record PID, process group, PID
   start ticks, CWD, executable SHA-256, internal level, renderer, internal X
   display/window, and focus.
4. Require SHA-256
   `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
   and the intended `work/copies/` CWD.
5. Start a read-only observer before the write. At minimum retain current,
   preceding, auxiliary, flags `0x0059D9A0`, `NextLife` `0x0059A5B0`, internal
   level `0x00861C84`, and current collision index/result.
6. Read and retain all three position triples immediately before mutation.

## Accepted write boundary

Only a destination already proven walkable is accepted for routine teleport:

- write current and preceding XYZ together in one 24-byte
  `process_vm_writev` call — meaning **one call carrying two 12-byte
  vectors**, not a 24-byte contiguous range. The two triples are not adjacent:
  current ends at `0x0059D918`+4 while preceding begins at `0x0059D920`,
  leaving an unidentified dword at `0x0059D91C` between them. A contiguous
  24-byte write from `0x0059D910` would overwrite that unknown dword and place
  the second triple four bytes early. Corrected on 2026-08-17 while
  implementing [[Session control plane]], where a fixture reproduced the
  misalignment; `DEC-20260817-140`. Read the dword back and confirm it is
  unchanged;
- do not write auxiliary as part of the routine relocation;
- read back current, preceding, and auxiliary immediately;
- observe at least several engine updates and verify stable current position,
  `NextLife=0`, and a nonfatal auxiliary value before handing control back.

A full 24-byte return and exact readback prove completion of that syscall;
they do not make the write atomic relative to the game's engine threads or
identify an engine frame.

EXP-130 accepted the exact Level03 target `(501696,30092,494016)`. The engine
copied this stable target into auxiliary about 10 ms after the 24-byte write.
That adoption is expected evidence for this exact walkable target, but it also
means the teleport can move the reset anchor.

## Prohibited shortcut

Do not set current and preceding equal at an unverified, below-floor, pit,
out-of-bounds, or otherwise unsupported coordinate. Do not write all three
triples to such a point. EXP-130 showed both forms can make the engine adopt
the bad point as auxiliary and repeat `NextLife=2` until Game Over.

Omitting auxiliary is not by itself a safety guarantee. A paused/current-only
or guarded recovery technique remains unvalidated and must be a separate
experiment before use. If an auxiliary point becomes unsafe, terminate the
owned process group promptly instead of spending lives trying speculative
repairs in a running death loop.

## Evidence wording

- Say **write-assisted teleport** and list every written address/value/byte
  count.
- A later engine response may be ordinary code execution, but the setup is
  still mutated and cannot be called natural, pristine-state, or controller-
  only.
- Teleporting beyond a closed grain gate does not prove normal access. The
  first observed Level03 gate requires 10 grain in ordinary gameplay;
  EXP-136 independently joins that result to Tunnels resident row 3. Any
  separately authorized grain edit at `0x0059D9B1` must be disclosed
  independently.
- Preserve contradictions. A zero material-1 result at a forced coordinate
  does not contradict a prior natural trace unless the same collision path
  and state are reproduced.

## Supported implementation

`scripts/game-memory.py teleport` implements this procedure: it requires an
authorization reference and `--destination-evidence`, samples all three
triples plus flags/`NextLife`/level/collision before the write, writes current
and preceding as two vectors in one call, reads all three back, settles, and
reports a nonzero `NextLife` as tool-negative. It writes a receipt under
`dynamic/wine/RUN-POKE-<stamp>/`. It is fixture-validated and **not
live-validated**; see [[Session control plane]] and CAP-010.

## Reference helper

The earlier exercised source lives under ignored work storage:

`work/copies/EXP-20260815-130-row6-teleport/teleport_flik_keep_anchor.c`

Its EXP-130 SHA-256 is
`7cc425b774135cd3a4d631b35589e8e6abf0fcd7d3b00436bb008471a26eb1fb`.
It performs the accepted 24-byte current+preceding write and prints before and
readback receipts. It is an experiment helper, not a supported release tool.

## Cleanup

Close the exact owned process group, wait a bounded interval, terminate only
the exact retained reaper PID if required, unload the private audio sink, and
audit game/Wine/Gamescope processes and sink names. Confirm Wine `Y:` again
points to the intended work copy. Update the experiment, session, current
state, known unknown, decision log, and relevant MOCs before committing.
