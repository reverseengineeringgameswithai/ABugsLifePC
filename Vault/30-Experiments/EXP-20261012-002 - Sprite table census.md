---
type: experiment
id: EXP-20261012-002
date: 2026-10-12
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Static only. Raw capstone decoding and the existing Ghidra export over retail bugs.exe, repeated byte-for-byte on a derived EXE c3d8b207…; no game launch or memory access
question: Which entries of the per-level sprite table 0x005BFD70 does each engine context fill, and can drop type 0x78 or its retirement sparkles reach a null entry, the 0x004536D1 crash class, in any level?
result: Type 0x78 cannot. It needs entries 0x7B (glyph) and 4 (retirement sparkles), and every level context with a nonzero engine index has both. Entry 51 (0x33), which the native pickup walker's default case needs, is absent in 8 of 19 engine contexts (engines 1, 2, 4, 6, 11, 14, 16 and 19), including Anthill
status: complete-bounded
created: 2026-10-12
updated: 2026-10-29
evidence: [EXP-20261001-006, EXP-20260910-008, EXP-20260817-188]
tags: [experiment/static, re/rendering]
---

# EXP-20261012-002 - Sprite table census

## Question

The drop renderer dereferences the per-level sprite table `0x005BFD70` entry
of each drop record's sprite, and a null entry faults at `0x004536D1`. That
was first observed in a derived build: the first pickup of an added drop
record reached the pickup walker's default case, which spawns type `0x40` on
entry `0x33`, and that level's table had no entry `0x33` (EXP-20261001-006).
This census asks which entries each engine context fills, and whether drop
type `0x78` (a spinning glyph) or its retirement sparkles can reach a null
entry in any level. The related open item is under
[[Known Unknowns#Moved bosses]] (donor pickups and sprite entry `0x33`).

## How the table is filled

These findings are static and use two methods: raw decoding of the
executable, and the export's decompiled switch.

1. **Dispatcher.** The level loader `0x004671D0` calls `0x00467C00`, which
   switches on the engine index. Cases 1–19 each call one initializer, and
   case 0 calls `0x004415E0`, which fills no list.
2. **Initializers.** Each one clears all 128 entries (`rep stosd`), then
   copies its own static list into entries 0 to N−1 (`rep movsd`, N = 50–64).
   None of the 19 lists contains a null entry.
   - A byte-pattern scan found only 17 of the 19. Engines 9 and 18 place an
     extra `mov edx, 0x5bfd70` inside the pattern; the dispatcher found them.
   - A 20th list (`0x00431670` → `0x004DA5C0`, 50 entries) has no caller.
3. **Shared setter.** Each initializer then calls `0x00456860` (via thunk
   `0x004011F4`). It fills entries 115–127, including **123 = `0x7B` →
   `0x004D7B58`**, but only when `[0x00861C84]` is nonzero.
   - `0x00861C84` is the engine level index. Live reads in earlier
     experiments: 1 for Anthill, 3 for Tunnels, 17 for Training
     ([[EXP-20260817-188 - Live game-memory read save restore validation]]).
   - Every gameplay level is 1–17. Index 0 means no level is loaded.
4. **Renderer.** The drop renderer `0x00453510` reads only
   `[sprite*4 + 0x005BFD70]` for the record's own sprite. The ground shadow
   (behaviour 2) is drawn elsewhere; the native resting leaf, type `0x2A`,
   uses it too.

## What drop type 0x78 draws

The type table is at `0x004D64C4`, 20 bytes per type. Field 0 is the sprite
entry. The self-checks match the crash record: type `0x78` → `0x7B`, and type
`0x40` → `0x33`.

| Use | Drop type | Sprite entry | Where it comes from |
|---|---|---|---|
| Spinning glyph | `0x78` | 123 (`0x7B`) | Shared setter, every nonzero engine index |
| Retirement action 7: five sparkles (case 7 of `0x0042A2E0`) | `0x13`, `0x14` | 4 | Every per-level list (all point to `0x004D7850`) |

## Per-level result

`reports/sprite-table/EXP-20261012-002.json` has the full table.

- **Entries 4 and 123:** present in all 19 engine contexts.
- **Entry 51 (`0x33`):** present in engines 3, 5, 7, 8, 9, 10, 12, 13, 15, 17
  and 18. It is **absent** in engines 1, 2, 4, 6, 11, 14, 16 and 19:
  - 1: Anthill;
  - 2: Council Chamber;
  - 4: City Entrance;
  - 6: Cliffside;
  - 11: Bird Nest;
  - 14: Bug Bar;
  - 16: the circus stage;
  - 19: not in the roster.

**Derived EXE.** The census was repeated on a derived EXE (`c3d8b207…`). It
is identical to retail in every byte checked: the dispatcher, the four
initializers sampled (including engines 9 and 18) and all 18 per-level copy
sites, all 19 lists, the setter and its gate, its 20 call sites, the type
rows and the descriptors. None of its 17 added sections references the
table.

## Confirmed, inferred, unknown

- **Confirmed (static, two forms).** Drop type `0x78` and its retirement
  sparkles cannot reach a null sprite entry in any level context with a
  nonzero engine index. They are outside the `0x004536D1` crash class.
- **Inferred.**
  - The mapping of engine to level name comes from
    [[PC level roster and numbering]].
  - Engines 18 and 19 exist in the switch, but no roster level uses them.
- **Unknown.**
  - Which native records reach the pickup walker's default case (action
    `0xC` → type `0x40` → entry `0x33`). In the 8 contexts without entry 51,
    such a pickup would crash. This matters for moving creatures between
    levels ([[PC native creature transplant]]): a moved creature's drops run
    against the target level's list.
  - The role of the uncalled list at `0x00431670`.

## Extension: what a moved creature can draw

This section was added later the same day, for [[PC native creature transplant]].

- **Pickup collectibility.** The pickup routine `0x004292C0` takes drops whose
  `+0x33` has value 2 set (`& 2`). The allocator `0x0042AA50` copies `+0x33`
  from the type table's byte `+0x10`, at `0x004D64C4 + type×20`.
  - All 29 types with that bit set have their own pickup case. The cases are
    2, 8, 9, `0xC`, `0xF`, `0x14`, `0x20`–`0x24`, `0x2E`, `0x33`, `0x3A` and
    `0x76`.
  - So no native drop reaches the default `0xC` path from table data.
  - The earlier statement in the Unknown section above stands corrected:
    that path is reached only when code makes a caseless drop collectible.
    The known case is the added drop record of EXP-20261001-006.
- **Drop types on sprites 50–52.** Ten types use sprites missing from engine
  1's list: `0x32`, `0x3A`, `0x3E`, `0x3F`, `0x40`, `0x49`, `0x4A`, `0x4D`,
  `0x70` and `0x79`. Where the type is a constant, they are spawned by:
  - retirement chains that start from sprite-50 drops: case `0x17` (type
    `0x32`) spawns `0x3A`; case `0x12` (type `0x4A`) spawns `0x4D`; case
    `0xC` (type `0x3E`, and the pickup default) spawns `0x40`;
  - home-level routines: `0x00439410` spawns `0x49`, `0x00438040` spawns
    `0x79`;
  - an uncalled routine at `0x00428EE0` (thunk `0x004019E2`) that Ghidra
    never made a function.
- **What creature scripts and generic routines spawn.** All of it stays on
  sprites below 50:
  - **The script interpreter** spawns only type 1 (sprite 1).
  - **Combat helpers.** `0x004288F0`, `0x00428990` and `0x00432A50` spawn
    `0x15`–`0x1C` (sprites 0, 5 and 6). Those retire through case 6 into
    type 1.
  - **Contact effect.** The contact routine's `0x00428CE0` spawns
    `0x5F`–`0x66` (sprite 3).
- **Inferred.** A moved creature cannot put a missing sprite on screen in
  any level through its script, contact or kill handling. The remaining
  routes need a home-level routine (these do not move) or a caseless drop
  made collectible.
- **Unknown.**
  - The spawners of `0x32`, `0x3E`, `0x3F`, `0x4A` and `0x70`. No call site
    has a constant type for them.
  - Whether a kill drop's type ever depends on the creature's type.

## Later findings (2026-10-18)

The extension's list of what a creature spawns omitted the per-type
handlers. [[EXP-20261018-004 - Creature type handlers and opcode-11 subroutines]]
adds:

- the long-legged spider's projectile kind `0x7A`, on sprite entry 118,
  which `0x00456860` sets in every engine with a nonzero index;
- the badbug/weevil dust drop `0x59` and the wasp ring's kind `0x1E`, both
  on sprite 1.

The inference that a moved creature draws no missing sprite still holds.

## Artifacts

- `reports/sprite-table/EXP-20261012-002.json`.
- Retail copy: `work/experiments/EXP-20261012-001/target/bugs.exe` (SHA-256 above).
