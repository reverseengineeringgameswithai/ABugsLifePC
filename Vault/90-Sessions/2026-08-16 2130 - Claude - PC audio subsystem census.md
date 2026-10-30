---
type: session
date: 2026-08-16
agent: Claude
status: worker-complete
tags: [session, re/audio, research/coverage]
---

# PC audio subsystem census

## Goal

Run the first packet chosen from [[Subsystem Coverage Map]] rather than from
milestone momentum: open the audio row, which had no PC evidence at all.

## What was done

Offline static census of the exact retail work copy — import table, strings,
disassembly, and direct byte decoding. Evidence in
`static/exports/BIN-97c95ba5572dce63/SUBSYS-audio-static-census.md`; boundary
and unknowns in [[EXP-20260816-159 - PC audio subsystem static census]].

Anchors established: DirectSound bring-up `0x004A3480`, the `0x00596528`
music track table and its builder `0x0042BB90`, the assembled path buffer
`0x00596960`, the `DSStream` window class at `0x0042C29F`, and the
`0x004AD000`-`0x004ADB20` RIFF `mmio` cluster. Two function dossiers added.

The census nearly failed at the first step: neither DirectSound import has a
direct `call dword [IAT]` site, and no audio function has a direct caller,
because everything routes through `jmp` thunks. Resolving those in both
directions is now recorded as a method note in the coverage map, since it will
bite every future subsystem pass the same way.

## Corrections to my own earlier work

The map's first draft folded input into "player movement and physics",
following the PS1 taxonomy. That is wrong for the PC port — `DINPUT.dll` is a
distinct import surface, and `0x0042BA60` brings audio and input up as
siblings. Input is now its own row with anchor `0x0042F350`.

## Boundary

No runtime, debugger, breakpoint, or target write; `originals/` untouched. No
milestone status changed; this advances coverage, not a gate.

## Next

Identify `0x0042B020` (34 call sites), the module's busiest entry point.
