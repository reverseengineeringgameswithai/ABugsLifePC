---
type: implementation
status: implemented-bounded
created: 2026-09-13
updated: 2026-10-29
evidence: [EXP-20260913-002]
tags: [implementation/modding, re/actor-ai]
---

# PC Dot flight path authoring

EXP-20260913-002 replaces Dot's route in the native LEVEL01/Anthill slot while
retaining Dot's PC model, wing animation, flight, proximity waits and endpoint
behavior. It owns static, native and hardware evidence. No PS1 source was
consulted. Dot does not grant invincibility or replace the cannon/exit
mechanics.

## Native route requirements

The route edit validates 2..99 control points and resamples them into the
existing 104-point absolute path1. It retains corners, uses a maximum nominal
800-unit segment length, and reserves native index98 for the destination with
five trailing copies. It does not grow DAT storage or move geometry offsets.
The RAW transformation requires original Anthill provenance and an untouched
slot25 before editing its XYZ only; other packets and all remaining actor bytes
survive.

PC retail SHA256 `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`:
actor initialization `0041BD10` selects type14/script7/path1 from RAW slot25;
script7 starts at `004C7E98`. `0041DC60` performs native flight and a 1200-unit
horizontal player-proximity wait. `004317D0` clamps the path cursor to count−6
and supplies **visibility-dependent catch-up**. Its phase gate is byte
`00599AB0`; the candidate placement must also fail the native visibility query
`00459620`. Catch-up is conditional, not a promise to appear at a skipped-to
location. The original endpoint also has turning inertia; 400 units is a
waypoint acceptance threshold, not a hard confinement radius.

Original DAT path1 starts at offset1128, with104 XYZ triples; the EXP002
compiler relocates that record to1192 without changing its allocation. PC
loader `0044BB70` installs its pointer at `005C5864`. Actor state is
`0059C30C`, with XYZ+4, flags+92, cursor+94, animation+64 and script pointer+112.
Private disassembly and native controls corroborate the decompiler, rather
than translating it into replacement source.

## Validation

Original x86 at PE bases400000 and1000000 runs both original and authored
routes (`research/dot-flight/native_probe.py`). In hardware, normal-start
movement demonstrates Dot's cursor2→6 and exact resident route loading. A
write-assisted hardware arm (Flik moved and given timed invincibility; Dot and
code never written) covers all99 cursor values0..98 with12 animation frames
and no NextLife transition; it is not a controller-only route. Wider views,
death/re-entry and arbitrary future paths remain open.
