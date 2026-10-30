---
type: reference
status: active
created: 2026-08-16
updated: 2026-10-29
evidence:
  - EXP-20260812-013
  - EXP-20260815-136
  - EXP-20260816-144
  - EXP-20260820-005
  - EXP-20260911-020
  - EXP-20260914-010
  - EXP-20260927-001
addresses:
  - "0x004671D0"
  - "0x0043DB83"
  - "0x00443F54"
  - "0x00443FB3"
  - "0x004444D6"
  - "0x0041475F"
  - "0x00414766"
  - "0x0041476E"
  - "0x00599AF8"
  - "0x004C6A30"
  - "0x00861C84"
tags:
  - re/gameplay
  - re/static
  - reference
---

# PC level roster and numbering

The PC game uses **two distinct level numbering schemes** that do not match.
Reading "level 4" without qualification is ambiguous; always say which
scheme.

1. **Internal engine index** — the value stored at `0x00861C84`, which the
   level dispatcher `0x00418780` switches on and which names the data
   directory `LEVELxx/`. This is what the executable, gate code, and asset
   files key on. It is **not** the play order.
2. **Flik's Journey progression** — the "fliks journey" level-select
   carousel order (= number of `Right` presses from the start), which also
   matches the in-game briefing numbering (e.g. Tunnels, internal index 3,
   is briefed as "Level Two" = progression 2).

## Cliffside progression confirmation

EXP-20260914-010 additionally loads progression 4 live: carousel “cliffside”, original title “Level Four: Dandelion Flight”, engine selector `00861C84`=6 and LEVEL06 assets. User-facing LEVEL04 must not be mistaken for folder LEVEL04/City Entrance.

## Level data files (static rule)

[[EXP-20260927-001 - Complete original level Blender maps]] confirms the file
choice in loader `004671D0`: engines 1..10 load `LEVELnn/LEVEL.DAT`, `LEVEL.RAW`
and `TERRAIN.ALL`; engines 11..17 subtract 10, add `0x140` to `005C5E88` and load
`LEVEL(n−10)/LEVEL1.DAT`, `LEVEL1.RAW` and `TERR1.ALL`. This matches the runtime
logs for engines 1, 3, 6 and 17. Other files such as `LEVEL01/LEVEL2.DAT` or
`LEVEL04/LEVEL4.DAT` need variant bits 2/3, which no gameplay path sets.
Engine 16 therefore uses `LEVEL06/LEVEL1.*`; its map looks like a circus tent,
which is appearance only. All 17 are mapped in [[PC original level Blender maps]]
and [[PC original Training Blender mapping]].

## Flik's Journey chronology

The full progression→internal-index mapping is **statically derived** from
the level-select table at `0x004C6A30`, indexed by the carousel position
counter `0x00599AF8` and written to `0x00861C84` at `0x00414766` (see
Static derivation below). Position 0 is the carousel's starting "training"
slot; positions 1–15 are the Right-press progression. The original four live-loaded levels (Anthill, Tunnels, Council Chamber,
City Entrance) match the table exactly; EXP-20260914-010 adds Cliffside as above.

The **level names** and their play order are researcher-provided; the
**internal indices** are statically derived from the table below. The two
were initially cross-validated at those four live-loaded levels; Cliffside
now has the additional carousel/title/engine confirmation above.

| Progression (Right ×N) | Level name | Internal index (`0x00861C84`) | Confirmed direct/static grain-gate family |
| ---: | --- | ---: | --- |
| 1 | Anthill | 1 | none found |
| 2 | Tunnels | **3** | **confirmed — 9 (rows 0–8)** |
| 3 | Council Chamber | 2 | none found |
| 4 | Cliffside | 6 | none found |
| 5 | Riverbed Canyon | 10 | none found |
| 6 | Bird Nest | 11 | none found |
| 7 | City Entrance | **4** | **confirmed — 3 (indices 0–2)** |
| 8 | City Square | 5 | none found |
| 9 | Bug Bar | 14 | none found |
| 10 | Clover Forest | 7 | none found |
| 11 | The Tree | 12 | none found |
| 12 | Battle Arena | 13 | none found |
| 13 | Anthill Pt 2 | 9 | none found |
| 14 | Riverbed Flight | 8 | none found |
| 15 | Canyon Showdown | 15 | none found |

Carousel position 0 ("training") maps to internal index **17**. The internal
indices used by the carousel are therefore `{17} ∪ {1..15}`; internal index
**16** is the only dispatcher slot not reachable from the carousel. It is
**outside the carousel but reached by a special initialization path**; it is
not an established free slot. This accounts for the 17 dispatcher entries.
EXP-20260911-020 confirms
the distinction with fresh disassembly and64 original-x86 cases at two PE bases.

Internal index equals the data-folder number only for engines 1..10
(internal 3 → `LEVEL03`, internal 4 → `LEVEL04`). Engines 11..17 use
`LEVEL(n−10)/LEVEL1.*`; the training slot (internal 17) therefore loads
`LEVEL07/LEVEL1.*`, as its runtime log records. See Level data files above.

The final column follows from the direct/static internal-index evidence
([[EXP-20260816-146 - Grain-gate level exclusivity static proof]]): the only
directly referenced gate families are at internal indices 3 and 4, i.e.
progression **2 (Tunnels)** and **7 (City Entrance)**. No gate is confirmed in
another level, but indirect/aliased/cached families are not excluded.

## Static derivation

`0x004C6A30` holds a 16-entry dword table (positions 0–15) terminated by
`0xFFFFFFFF` at `0x004C6A70`:

```
pos:      0   1  2  3  4   5   6  7  8   9  10  11  12  13  14  15
value:   17   1  3  2  6  10  11  4  5  14   7  12  13   9   8  15
```

Level-select code loads the carousel position from `word [0x00599AF8]`,
reads `dword [pos*4 + 0x004C6A30]`, and stores it to the internal level
global `0x00861C84` (`0x0041475F`–`0x0041476E`; the table base `0x004C6A30`
is also referenced at `0x0041013C`, `0x0041480A`, `0x0043DD84`). Reading the
table as internal→progression instead fails at City Entrance (it would place
it at progression 6, contradicting the observed position 7), so the
direction is unambiguous. The four live-loaded levels (Anthill 1, Tunnels 3,
Council Chamber 2, City Entrance 4) match the table, cross-validating it.

### Selector-loop held-state caveat

The PC path that enters Level Select writes zero to the 16-bit carousel global
at `0x0043DB83`. Inside candidate selector routine `0x00443B40`, instruction
`0x00443F54` tests the live input byte at `0x00861C98` for Right bit `0x20`.
The admitted path increments its local position at `0x00443FB3`; confirmation
eventually stores the selected position to `0x00599AF8` at `0x004444D6`.
There is no previous-state edge test in that increment condition, although the
animation/position conditions still constrain when another increment can
occur. Ghidra decompiler evidence and a fresh bounded disassembly of the retail
binary independently show the same instructions.

This corrects the automation assumption that one 180 ms held Right necessarily
means one carousel step. P0A-AH-001 retained such a hold and then loaded
internal level07, which is progression position 10 in the table above. That
outcome is consistent with repeated held-state polling but does not prove the
number or cadence of accepted increments. It also does not make a shorter tap
safe: EXP-156 observed approximately 12 ms XTEST taps being dropped. A future
passive route therefore needs a separately authorized observable carousel
check or a proved edge-delivery mechanism; assumed timing alone is not an
acceptance gate. See [[EXP-20260820-005 - R2p task lifecycle diagnostic]].

## Known grain-gate routing is an internal-index fact

[[EXP-20260816-146 - Grain-gate level exclusivity static proof]] confirms that
all 22 direct/static references to grain byte `0x0059D9B1` contain gate paths
only in **internal index 3 (Tunnels)** and **internal index 4 (City Entrance)**
— Flik's-Journey progression **2** and **7**. The dispatcher and known gate
structures independently bind those two families. Static reference
enumeration cannot exclude address-computed, aliased, or cached consumers, so
global exclusivity remains Inferred.

## Dispatcher-slot accounting (resolved)

The dispatcher `0x00418780` has 17 internal level entries (indices 1–17).
The carousel table above accounts for 16 of them: internal 17 = the
"training" slot (carousel position 0) and internal 1–15 = the fifteen
progression levels. The one remaining slot, **internal index 16**, is not
reachable from the carousel, but initializer `00410100` selects it when global
`004F0680` is nonzero (`0041015B`). The outer loop `0043DA40` sets that flag
following level-done value6. Its exact special-stage name is not determined
here. This supersedes the earlier uncertainty about whether index16 was unused.
It fully reconciles the earlier "15 progression levels
vs 17 dispatcher entries" question.

## Related

- [[PC autonomous game control]] (carousel navigation recipe)
- [[EXP-20260816-144 - Runtime grain-gate visual mapping]]
- [[EXP-20260816-146 - Grain-gate level exclusivity static proof]]
- [[PC grain gate requirements]]
