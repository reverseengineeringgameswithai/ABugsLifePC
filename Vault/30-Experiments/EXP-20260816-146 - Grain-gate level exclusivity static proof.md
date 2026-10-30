---
type: experiment
id: EXP-20260816-146
date: 2026-08-16
question: Are Tunnels (internal level 3) and City Entrance (internal level 4) the only levels with grain gates, confirmed by offline static analysis?
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline static analysis; radare2 5.9.8; no runtime process
configuration: read-only disassembly and reference analysis of the exact retail work copy; no executable, asset, or originals mutation
working_directory: /home/dev/ABLPC
artifacts: []
addresses:
  - "0x00416580"
  - "0x00418780"
  - "0x00432810"
  - "0x00432B30"
  - "0x00432F0C"
  - "0x00433606"
  - "0x00433790"
  - "0x00433900"
  - "0x004337D6"
  - "0x004DA9C8"
  - "0x004DAA80"
  - "0x0059D9B1"
  - "0x0059F020"
result: direct-grain-byte-census-binds-known-gates-to-internal-levels-3-and-4-global-exclusivity-inferred
status: corrected-scope
created: 2026-08-16T12:45:00
updated: 2026-08-16T20:45:00-04:00
tags:
  - re/experiment
  - re/static
  - re/gameplay
  - milestone/m3
---

# EXP-20260816-146 - Grain-gate level exclusivity static proof

> [!correction] Authority narrowed by EXP-167
> The 22 **direct/static** references to `0x0059D9B1`, their classification,
> dispatcher routing, and known gate-structure bindings are Confirmed. Static
> address-reference enumeration does not exclude address-computed, aliased, or
> cached consumers, so global family exclusivity is Inferred, not Confirmed.
> [[EXP-20260816-167 - Independent M5.6 hard-truth audit]] records the
> correction.

## Question

Are the visible Tunnels (internal level 3) and City Entrance (internal
level 4) the only levels with grain gates? Confirm offline against the exact
retail executable, without running the game.

## Method and decisive argument

A grain **gate** is the positional barrier that reads Flik's grain count,
compares it to a per-gate requirement, and — gated by a proximity test —
opens a barrier. Every confirmed gate reads grain-count byte `0x0059D9B1`.
Enumerating direct/static code references is an exhaustive census of that
addressing form, not of address-computed, aliased, or cached consumers.

radare2 reference analysis (`aar; axt @ 0x0059d9b1`) on the hash-verified
retail exe finds **22** code references. Each was disassembled in context
and classified:

| # refs | Kind | Addresses |
| ---: | --- | --- |
| **2** | **positional gate: grain vs requirement** | `0x00432F0C` (Tunnels), `0x004337D6` (City) |
| 4 | grain pickup increment (`inc`/store) | `0x00417D7B/8D`, `0x00418C40/52` |
| 2 | Training completion check (`cmp ==0x32`/50) | `0x00417DC2`, `0x00418C8A` |
| 4 | clamp / reset writes | `0x0043A0EB/F3`, `0x00442EC2/ED0` |
| 3 | level-specific non-gate grain events | `0x00436208/308` (counter-change), `0x0043A911` (`cmp <0x28`/40) |
| 7 | HUD counter read / digit render | `0x00416BB7`, `0x00416C2C`, `0x0042E93C`, `0x0044341D`, `0x00443457`, `0x004434C5`, `0x0044358B` |

Only the two positional-gate comparisons feed a barrier-open decision:

- `0x00432F0C` is inside the Tunnels update `0x00432B30`; it compares the
  grain byte to each nine-row record's requirement `+0x08`.
- `0x004337D6` is inside the shared City gate routine `0x00433790`; it
  compares the grain byte to the retail inline `10 * (index + 1)`.

Both are the exact comparisons already accepted in EXP-136/139. The other
20 references are pickup, completion (Training's 50-grain event), HUD
display, clamp, or level-scripted grain events — none reads a per-gate
requirement, calls the proximity predicate, or changes a gate barrier.

## Level dispatcher binds the two known direct gate paths

The per-level update dispatcher `0x00418780` is a 17-entry jump table on the
internal level `0x00861C84`. Resolving every thunk to its real routine:

| Level | Routine | Level | Routine |
| ---: | --- | ---: | --- |
| 1 | `0x004317D0` | 10 | `0x00437B70` |
| 2 | `0x00431CB0` | 11 | `0x00438040` |
| **3** | **`0x00432B30` (Tunnels gate)** | 12 | `0x00438A80` |
| **4** | **`0x00433900` -> `0x00433790` (City gate)** | 13 | `0x00439410` |
| 5 | `0x00434170` | 14 | `0x00439E90` |
| 6 | `0x00434620` | 15 | `0x0043AE00` |
| 7 | `0x00434E10` | 16 | `0x0043BD10` |
| 8 | `0x004362D0` | 17 | `0x0043C340` |
| 9 | `0x00436B40` | | |

Only level 3 routes to `0x00432B30` and only level 4 routes to
`0x00433900` (which calls `0x00433790`). Two other level routines read the
grain byte but neither is a gate: level 8 (`0x004362D0`) compares grain to
a **previously stored** value (`0x0059F404`) to detect a count change for
the on-screen counter, and level 14 (`0x00439E90`) clamps grain to a max
(`0x0043A0EB`) and triggers a grain-`<40` scripted event (`0x0043A911`).
Neither uses a per-gate requirement, the proximity predicate, or a barrier.

## Gate-specific structures are L3/L4 only

Independent confirmation from the byte-referenced gate data structures:

- Tunnels gate table `0x004DA9C8` is referenced only at `0x0043281E`
  (initializer copy `0x00432810`), `0x00432EF4`, `0x00432F6D`,
  `0x00432F9F`, `0x00433027` — all inside the Tunnels routine/initializer.
- Its initializer template `0x004DAA80` is referenced only at `0x00432819`
  (the same initializer).
- City gate-state array `0x0059F020` is referenced only at `0x00433606`
  (a City initializer that writes `-1` to the state slots — matching the
  live `(-1,-1,-1)` observed in EXP-137/144) and inside `0x00433790`
  (`0x0043379B`, `0x004337F2`, `0x0043383E`, `0x0043384E`).
- The City requirement lookup gap `0x004338B0` has **zero** references in
  retail (it is `INT3` padding; retail uses the inline formula, and the
  three-dword lookup exists only in the EXP-136 modified profile).

No other level's routine references any gate table, gate-state array, or
gate requirement.

## Result

**Confirmed:** all 22 direct/static code references to `0x0059D9B1` are
accounted for. Only `0x00432F0C` in internal level 3 (Tunnels) and
`0x004337D6` in internal level 4 (City Entrance) are positional
grain-vs-requirement barrier comparisons. The level dispatcher and known
gate-specific structures independently bind those two confirmed families to
levels 3 and 4.

**Inferred:** those are the only grain-gate families in the retail executable.
The direct-reference census does not exclude an address-computed, aliased, or
cached grain consumer, so global absence elsewhere is not Confirmed.

## Limitations

- Scoped to executable SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`; not a
  claim about another PC release or port.
- "Grain gate" means the positional grain-count barrier. Other grain
  mechanics (pickups in every level, Training's 50-grain completion, the
  level-8 counter and level-14 grain event) exist and are not gates.
- "Level 3/4" here means the **internal engine index** (`0x00861C84` /
  `LEVELxx`), not the Flik's Journey play order: internal index 3 = Tunnels =
  progression 2, and internal index 4 = City Entrance = progression **7**.
  The complete internal↔progression mapping is statically derived from the
  level-select table in [[PC level roster and numbering]]. Under it the two
  non-gate grain readers here are internal 8 (Riverbed Flight, progression
  14) and internal 14 (Bug Bar, progression 9); neither is a gate, so the
  result is unaffected.

## Follow-up

- Independent audit optional; the enumeration is mechanically reproducible
  from the two radare2 queries above.
