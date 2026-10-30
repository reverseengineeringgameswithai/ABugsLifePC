---
type: experiment
id: EXP-20261012-006
date: 2026-10-12
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Static decode of retail bugs.exe (existing Ghidra export and raw strings), the retail type-35 census of all 17 engines through original_levels, and LOAD lines in 574 saved bugs.log files from earlier sessions; no new game launch
question: Which character is each of the 41 creature types placed in retail levels?
result: The character loader 0x00445020 names a file for every type, 1 to 41 (chars\gypsy … chars4\badcent). The saved runtime logs agree exactly where a level ran with retail creatures, which confirms 26 types two ways; 15 are static only. Two appearance hints contradict their file names (31 acorn, 37 weevil)
status: complete-bounded
created: 2026-10-12
updated: 2026-10-29
evidence: [EXP-20260927-001, EXP-20261005-001, EXP-20261005-002]
tags: [experiment/static, re/creatures]
---

# EXP-20261012-006 - Creature types from the character loader

## Question

[[EXP-20260927-001 - Complete original level Blender maps]] left 32 of 40
creature types unidentified. This is section 7 of [[Next Tasks]], at the
user's request. Identities are needed before moving a creature or a boss
routine to another level ([[PC native creature transplant]]).

## Method

1. **Static.**
   - The character loader `0x00445020` switches on each pool slot's type and
     passes a file stem to `0x00444C40`. Type 11 goes to `0x00444EF0`
     (`bits\seed`).
   - Every `case` was resolved to its string in the binary. The decompiler's
     `s_…` labels were checked against the bytes at their addresses.
2. **Census.** `original_levels.read_inputs` and `creature_rows` were run over
   the hash-checked retail RAW of all 17 engines: 41 types in 534 rows (corrected 2026-10-18; see [[#Correction (2026-10-18)]]).
3. **Runtime.**
   - Every saved `bugs.log` under `dynamic/`, `work/experiments/` and
     `work/copies/` was read (574 files). Each `LOAD : Loading file
     …\charsN\X.anm` line was attributed to the most recent `Loading packet
     data level…, level N` line.
   - For each engine, the loaded set was compared with the files the census
     predicts. Flik's own models were excluded.

## Runtime agreement

| Engine | Predicted = observed? | Note |
|---|---|---|
| 3 Tunnels | 6 = 6 | badbug, grub, ggrassh, flikharv, badworm, badcent |
| 4 City Entrance | 6 = 6 | fran, slim, fly, heim, hspider, taxibug |
| 6 Cliffside | 3 = 3 | bbird, dragfly, weevil |
| 15 Canyon Showdown | 3 = 3 | ggrassh, hopper, bbird |
| 16 | 1 = 1 | badbug |
| 1 Anthill | all 7 present, plus 11 extra | The saved logs include derived builds; the extras are exactly the boss and tough-regular types those builds moved in (EXP-20261005-001/002) |
| 17 Training | 2 present, plus `mos`, `wasp` | The extras are mosquitoes and bees added in derived builds |
| 7 Clover Forest | not comparable | The saved engine-7 logs come from a derived build with custom content |

`bits\seed.all` appears in 496 logs.

## The 41 types

The column "Runtime" says how a type was confirmed at runtime.

- **E:** an exact per-level match in the table above.
- **T:** loaded when moved into engine 1.
- **A:** in engine 1's retail set.
- **S:** seed.
- **Tr:** Training.
- **—:** static only.

The reading is inferred from the developers' file stem and, where present, the
appearance hint. The full table with counts and scripts is
`reports/creatures/EXP-20261012-006.json`.

| Type | File | Placed in | Runtime | Reading |
|---:|---|---|---|---|
| 1 | `chars\gypsy` | City Square | — | Gypsy (moth) |
| 2 | `chars\manny` | City Square | — | Manny (mantis) |
| 3 | `chars\fran` | City Entrance | E | Francis |
| 4 | `chars\rosie` | City Square, The Tree ×3 | — | Rosie |
| 5 | `chars\slim` | City Entrance | E | Slim (stick insect) |
| 6 | `chars\fly` | City Entrance, City Square, Riverbed Canyon (22) | E, T | fly |
| 7 | `chars\heim` | City Entrance, Clover Forest | E | Heimlich |
| 8 | `chars\dim` | City Square | — | Dim |
| 9 | `chars\badbug` | 8 levels (65) | E | the common enemy (earlier label: spider) |
| 10 | `chars\mos` | 6 levels (33) | A, Tr | mosquito |
| 11 | `bits\seed` | 16 levels (130) | S | seed |
| 12 | `chars\grub` | Tunnels (11) | E | grub |
| 13 | `chars\wasp` | 6 levels (43) | A, Tr | wasp (earlier label: bee) |
| 14 | `chars2\dot` | Anthill, The Tree | A | Dot |
| 15 | `chars2\ggrassh` | Tunnels, Anthill Pt 2, Canyon Showdown (42) | E, T | green grasshopper |
| 16 | `chars2\thumper` | Council Chamber | T | Thumper |
| 17 | `chars2\hspider` | City Entrance, City Square, Riverbed Canyon (25) | E, T | long-legged spider |
| 18 | `chars2\taxibug` | City Entrance (6) | E, T | taxi bug |
| 19 | `chars2\roach` | City Square (6) | T | roach |
| 20 | `chars2\tuckroll` | City Square | — | Tuck and Roll together |
| 21 | `chars2\attaflik` | Riverbed Flight | — | Atta with Flik |
| 22 | `chars2\hopper` | Riverbed Flight, Anthill Pt 2, Canyon Showdown | E, T | Hopper |
| 23 | `chars2\tuck` | Anthill Pt 2 | — | Tuck |
| 24 | `chars2\roll` | Anthill Pt 2 | — | Roll |
| 25 | `chars2\gypsy` | Clover Forest | — | Gypsy, second model |
| 26 | `chars2\manny2` | Clover Forest | — | Manny, second model |
| 27 | `chars2\franslim` | Clover Forest | — | Francis and Slim together |
| 28 | `chars3\atta` | Anthill Pt 2 | — | Atta |
| 29 | `chars3\molt` | Battle Arena | T | Molt |
| 30 | `chars3\bbird` | Cliffside, Bird Nest, Canyon Showdown | E, T | bird |
| 31 | `chars3\acorn` | The Tree (7) | — | acorn (hint said flytrap plant) |
| 32 | `chars3\bluescot` | The Tree (5) | — | blue scout |
| 33 | `chars3\fdim` | The Tree | — | a Dim variant |
| 34 | `chars3\dragfly` | Cliffside, Riverbed Flight, Bird Nest (34) | E | dragonfly |
| 35 | `chars3\flikharv` | 6 levels, one each | E, A | Flik's harvester |
| 36 | `chars3\thud` | Bug Bar | T | Thud |
| 37 | `chars3\weevil` | Cliffside, Riverbed Flight, Riverbed Canyon, Bird Nest (35) | E | weevil (hint said dandelion seed) |
| 38 | `chars3\soil` | Training | Tr | Mr. Soil |
| 39 | `chars3\protect` | Anthill, Clover Forest, Riverbed Canyon (8) | A | "protect" (earlier label: pill bug) |
| 40 | `chars4\badworm` | 5 levels (15) | E, A | "bad worm" (earlier label: caterpillar) |
| 41 | `chars4\badcent` | Tunnels, Riverbed Canyon (9) | E, T | centipede |

## Confirmed, inferred, unknown

- **Confirmed.**
  - **Static.** Every type 1–41 has one loader file stem.
  - **Static and runtime.** For 26 types, the game loaded exactly the
    predicted files.
- **Inferred.** The readings in the last column are inferred from the file
  stems and, where present, the appearance hints. Character names (Gypsy,
  Manny, Heimlich and so on) follow the stems, not PS1 or film sources.
- **Contradictions recorded, not resolved.** In
  [[EXP-20260927-001 - Complete original level Blender maps]], two
  appearance-only hints disagree with the stems:
  - 31 "flytrap plant" against `chars3\acorn`;
  - 37 "dandelion seed" against `chars3\weevil`.

  The hints were viewing aids, so the stems are the better evidence. A
  render of the two models, or a look in game, decides it.
- **Naming corrections for project notes.**
  - Type 13 loads `wasp`; several notes call it "bee".
  - Type 9 loads `badbug`, labelled "spider".
  - Type 39 loads `protect`, labelled "pill bug".
  - Type 40 loads `badworm`, labelled "caterpillar".

  The earlier labels described appearance and stay valid as descriptions.
- **Unknown.** The 15 static-only types need a run in their levels: City
  Square, Council Chamber, Riverbed Flight, Anthill Pt 2, Bird Nest, The Tree,
  Battle Arena and Bug Bar.

## Side note: TEST and PLANT12 on the disc

The user asked about two model pairs.

- **TEST.** `CHARS/TEST.ALL` (22,804 B) and `TEST.ANM` (9,896 B) are dated
  1998-06-28, three months before `FLICK.ANM`, and duplicate no other model.
  The executable has no `chars\test` string, and no saved log loads it.
  - **Inferred:** a leftover test model that the PC game never loads. The
    Cutting Room Floor's Windows page (pasted by the user) agrees. It
    identifies the model as a wrongly textured mermaid from Traveller's
    Tales' *Rascal*, which is unchecked here ([[External Source Registry#SRC-TCRF]]).
- **PLANT12.** `PLANTS2/PLANT12.ALL` (4,620 B) and `.ANM` (4,418 B) are named
  by the plant loader in `0x00445020` (`plants2\plant12`, case `0xC`,
  resource slot `0x73`), so it is a real plant.
  - **Unused on PC (follow-up the same day).** The user found it listed as
    unused on The Cutting Room Floor. The PC evidence agrees independently in
    three ways:
    - **Request tables.** A level's plant list comes only from `0x00416100`:
      the constant 5, the seed table at `0x004DE9F0`, and five token lists.
      Together they can produce 1–11, 13 and 14, never 12.
    - **One reference.** `plants2\plant12` is referenced once, by the
      loader's case `0xC`.
    - **Runtime.** The saved logs load every other plant, 1–11, 13 and 14,
      hundreds of times, and plant 12 never.

    See [[FUNC-97C95BA5572D-00416100]]. The Cutting Room Floor page itself
    could not be read: the site serves automated agents a block page.

## Artifacts

- `reports/creatures/EXP-20261012-006.json`: per-type file, placements,
  levels, scripts, prior labels and runtime basis, plus the per-engine
  comparison.

## Later data point (2026-10-18)

On the 31/37 hint contradiction above: type 31's handler (`chars3\acorn`)
holds `DANDLION.WAV` on a keyed channel at a low pitch, and type 37
(`chars3\weevil`) shares the badbug's `SPIDER01.WAV` footstep
([[EXP-20261018-004 - Creature type handlers and opcode-11 subroutines]]).
Sound names are a third, weak form. They do not settle the identities; the
model render or an in-game look still decides.

## Correction (2026-10-18)

The method first gave 525. The report's placements sum to
534, which [[EXP-20261018-001 - Creature row index census]] counts
independently. 525 is 534 minus Training's 9 rows.
