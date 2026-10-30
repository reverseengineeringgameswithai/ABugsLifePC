---
type: moc
updated: 2026-10-29
tags: [moc/subsystems, research/cross-port]
---

# Subsystem Coverage Map

[[Subsystems MOC]] indexes what PC evidence we **have**. This note is the
other half: the list of subsystems the game plausibly contains, so the blank
areas are visible when choosing what to work on next.

It is **not** a plan and does not schedule anything — [[Project Roadmap]] owns
sequencing and gates. Use this to notice that a subsystem has no PC evidence
at all; use the roadmap to decide whether that is the right next packet.

## Provenance and trust

The subsystem inventory is seeded from the external PS1 project
`SRC-PS1-ABL` ([[External Source Registry]]) at commit
`1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51`, whose vault carries 115
`ObsidianVault/Canon/Systems/SYS_*.md` notes plus format and finding notes.
Only committed blobs were read; nothing was copied, linked, or vendored, and
the rows below are ABLPC-authored groupings, not reproductions.

Under [[Cross-Port Evidence Policy]], that inventory is **inference about
where to look, not evidence about the PC port**. A row existing here means
"the PS1 build has such a system, so the PC build probably does too" — a
search hint. Nothing here promotes a PC claim. The PC status column cites only
PC evidence, and rows with no PC anchor are genuinely unknown on PC, including
whether the PC port organises that area the same way at all.

## Status vocabulary

| Status | Meaning |
|---|---|
| Mapped | A bounded PC model exists with cited static and runtime evidence |
| Bounded | Real PC evidence at a documented boundary, with major parts open |
| Touched | Incidental PC observations only; no model |
| Untouched | No PC evidence beyond the subsystem plausibly existing |

## Coverage

| Subsystem | PC status | PC anchors | Top open question |
|---|---|---|---|
| Startup, capability and renderer selection | Mapped | `0x004B1670`, `0x0041F990`, `0x004A7600`; EXP-143/150/151/152 | None blocking; auto-hardware is accepted at its own build hash |
| Media root, CD gate and file loading | Mapped | `0x00403B90`, `0x004ADC30`, `0x004AE240`; [[PC Content Census]] | Does a block-device CD path change the selected branch? |
| `LEVEL*.DAT` structure | Mapped | M1 tooling; type-`0x3F` and type-1 tables; EXP-111/116/153 | Most top-record types and payload fields remain unnamed (`KU-009`) |
| `LEVEL.RAW` | Bounded | Referenced by the loader; type-`0x23` record seen in `EXP-20260813-056`. Since 2026-09: packet codec modelled on `0x0049A200` and compared on 169 decoded packets, with type-35 enemy placement ([[EXP-20260908-020 - Native enemy placement and scattered Blender population]]); every original level's type-35 creature table, its `0x102` packets and texture pages decoded ([[EXP-20260927-001 - Complete original level Blender maps]]); texture pages added by modified builds load and run in hardware. Reclassified from Touched on 2026-10-12 | What is its record grammar, and what consumes it? |
| Resource binding (`.ALL`, `.ANM`, actor models) | Bounded | M2 packets; `0x00448010`, `0x00444B70`; [[PC ANM inspector]] | **`KU-023`**: no proven edge from a placement record to a resource identity — M2's deferred causal gate |
| Scene rendering and Direct3D submission | Bounded | `0x0044D430`, `0x0045A7F0`, batch builders `0x00405FE0`/`0x00407450`; viewport structure setup `0x00423EDE`-`0x00423F43`; D3DApp-derived scaffolding and known `D3DVT_TLVERTEX` submissions (EXP-161, corrected by rejecting audit EXP-162); EXP-039..043; rules for added geometry in [[PC scene admission and DAT layout rules]]; sky, panorama origin and distant-pass depth in [[PC sky, panorama origin and distant pass depth]] | What decides per-frame append admission? Pixel causality is unproven; do not generalise three TL-vertex sites into absence of all D3D view state |
| Collision and terrain height | Mapped | `TERRAIN.ALL` parser; `0x004AC460`/`0x004ACA60`; EXP-131/141/142; requirements for added or moved collision in [[PC terrain collision rules for modified levels]] | `KU-061` descriptor Z-bounds derivation; `plantter.all` family out of scope (since 2026-09-06 PLANTTER record 8, the type-5 mushroom, is bounded in [[PC seed and mushroom collision state]]) |
| Reset placement | Mapped | `0x00432930`; EXP-153/154/155/156 | `KU-063` which levels use type 1 for reset; `KU-062` aux value at the selection instant |
| Triggers and gates | Bounded | Twelve confirmed Tunnels/City mechanisms; `0x00432B30`, `0x00433790`, `0x00416580`; EXP-136..149. EXP-170 implements the bounded resolver; the M5.8 audit EXP-171 accepted it at `dfd3af3` ([[PC grain gate opening resolver]]). EXP-167 narrows EXP-146 to direct/static references, so global family exclusivity is Inferred | Are there trigger families beyond the known grain gates, including indirect/cached grain consumers, and do they share `0x00416580`? |
| Collectibles, counters and HUD | Bounded | `0x00417720`, `0x00456A90`; M3 grain/letter/`FLIKFLIK` packets | Is there a general inventory/progression architecture, or only per-feature tables? |
| Player movement and physics | Bounded | Position globals `0x0059D910`; settle band 121-129; EXP-128/156. Since 2026-09: player controller `0x0043F9E0` on record `0x0059D910` (vertical velocity `0x0059D940`, movement state `0x0059D990`), jump bit `0x4000` (EXP-20260907-028, EXP-20260930-004); jumps counted in hardware (EXP-20260930-004); action state `0x0059D998` mapped statically ([[PC Flik animation catalog]]); outer loop, frame and player event sites in [[PC gameplay loop and player event sites]]. Reclassified from Touched on 2026-10-02 | Where does gravity integrate, and what are movement states 4 and 5 (see [[Known Unknowns]] and [[PC Flik animation catalog]])? |
| Input | Bounded | EXP-181, **accepted** at `EXP-20260817-184` after two rejections and corrections: bring-up `0x0042F350` creates a `GUID_SysKeyboard` device (`0x004C0230`) at `c_dfDIKeyboard` (`0x004AFE90`, non-exclusive foreground) plus enumerated joysticks promoted to `IID_IDirectInputDevice2A` (`0x004C0220`) at `c_dfDIJoystick` (`0x004AEE70`, exclusive foreground); per-frame read `0x0042EBC0` fills `0x00598A10`/`0x00598B60` and reduces them to action bits at `0x00598B10` via the runtime-written table `[0x004D8430,0x004D8490)`, which is also applied from the `0x18`-stride config array `0x004D9CF9` by blocks at `0x00430C3F` and `0x00431022`; `GetAsyncKeyState`'s thunk is dead and the chooser path is disjoint | What do the action bits in `0x00598B10` mean and what consumes them (`KU-070`)? The bindings are configurable — the screen behind the `0x004D9CF9` array is unidentified. Narrowed since: `0x4000` is jump (left Shift) and `0x8000` is throw (Ctrl); see `KU-070` in [[Known Unknowns]]. (2026-10-18: the screen is the controls screen `0x00430DF0`, whose items label every bit from "forward" to "kick": [[EXP-20261018-006 - Controls configuration screen and action bits]].) |
| Camera | Bounded | EXP-164/165: `0x0041ADF0` -> flag-selected copies in `0x0041B7D0` -> common `0x00599C90` -> `0x00455710` -> matrix `0x005B58E0`/origin `0x005BDB8C` -> renderer `0x0044D4C1`/`0x0044D4F0`; independently accepted at clean `0336d14` | Source roles, selector meaning, second consumer, runtime frequency, visual causality, and manual controls remain open under KU-066. 2026-09-15: within the telescope event only, bit 0 of `0x0059A5EE` selects the `0x0059A5C0` source (EXP-20260915-005, [[PC camera view-transform chain]], [[PC telescope camera paths]]) |
| Enemies, actors and AI | Bounded | EXP-172, **accepted** at `EXP-20260817-180` after seven rejections and corrections — see its Audit history: 64-slot pool `[0x0059B628,0x0059D728)` stride `0x84`, built by `0x0041C420` from the `0x1C`-byte `LOAD: Type 35, CreatListRam.` records at `0x00599EB0` (pool, both 64s and the string are prior art in `M2-plant-request-origin-static-trace.md` and `M2-second-deferral-hard-truth-audit.md`); type domain 6..41; update `0x0041EC40`; release `0x0041B9F0`; word-code interpreter `0x0041DC60`-`0x0041E845` with dispatch `0x0041E848`, 40 programs at `0x004C83F0`, and per-type handler call at `0x0041E7C7`. One spider damage/death observation in `EXP-20260815-129`. Boss rows, placements and level-bound fight routines: [[PC boss level routines and creature transplant limits]] | The interpreter region past `0x0041E1A8` — more than half the function, implementing the five modes — is unanalysed; so are the ten `+0x7C` handlers and the nine opcode-11 subroutines. And does a slot's `+0x70` actually walk a decoded program at runtime (`KU-068`)? (2026-10-18: yes for two slots, from saved hardware samples, [[EXP-20261018-002 - Creature script counter in saved runtime samples]]; every shipped row keeps the unbounded indexes in range, seeds never run a script and regular enemies run it only on screen, [[EXP-20261018-001 - Creature row index census]]. The five modes are read in [[EXP-20261018-003 - Creature VM movement modes]]; the per-type handlers and opcode-11 subroutines are read in [[EXP-20261018-004 - Creature type handlers and opcode-11 subroutines]]; event ids and level routines stay open.) |
| Event/scripting system | Bounded | EXP-185, **closed unaccepted** after six independent audits (`DEC-20260817-138`) — conclusions confirmed six times over, individual addresses and enumerations carry a demonstrated defect rate and must be re-derived before use: 16-slot table `[0x005982B0,0x00598670)` stride `0x3C`, each record an id word, three native callbacks at `+0x04` (create) / `+0x08` (unnamed) / `+0x0C` (destroy), a name at `+0x10` and an in-use flag at `+0x34`; register `0x0042DB10`, dispatch `0x0042D980`, destroy-all `0x0042DA70`; two static registration sites pass `"WINDOWS"` (`0x004D81A8`) and `"DIRECTX"` (`0x004D81E8`). **Not a VM and not a trigger stream** — a callback registry, disjoint from the creature scripts. Table geometry, layout, 7 of the 9 reachers and the `0x004ADEA0` reading (it writes `"bugs.log"`, reaching `KERNEL32.dll!DeleteFileA` through `0x004B13E0`; body gated on `0x008620AC`) are present in `ghidra-evidence.json` and were re-derived, not first found, here; new are the four dead entry points, two omitted reachers, the decoded records, the disjointness result, the negatives, and the §2.1 relocation result — all 26,713 type-3 relocations decoded, the 47 pointing into `[0x005982A0,0x005986F0)` all inside the seven functions. That is a negative on the **absolute** addressing form only, not a proof of isolation, and it was found by the second-round audit rather than by this census | What do the six callbacks do, and is any event registered outside the two static sites (`KU-071`)? (2026-10-18: answered. WINDOWS is the window and message pump, DIRECTX the renderer/input/sound lifecycle, and only these two register in 579 saved logs: [[EXP-20261018-005 - Event callbacks and registrations]].) |
| Audio: music, SFX, streaming | Bounded | DirectSound bring-up `0x004A3480` (object `0x007EDAE8`, ready flag `0x007ECA40`); track-name table `0x00596528`; builder `0x0042BB90`; `DSStream` parser `0x0042C130`; RIFF `mmio` cluster `0x004AD000`-`0x004ADB20`; EXP-159. EXP-185 closes that census's open caller question: `0x0042BA60` is the `"DIRECTX"` **event create callback**, the slot called at `0x0042DC2A` (a static path, not an observed call) | What is `0x0042B020`, the module's busiest entry point (34 call sites), and do sound effects use a path separate from the music tracks? (2026-10-12: `0x0042B020` is the projectile and effect allocator (EXP-20260909-008, [[PC projectile records, homing and kill accounting]]), so it is not an audio entry point; sound banks and per-level routing are in [[PC sound banks and per-level audio routing]]; whether SFX use a separate path stays open.) |
| FMV/video playback | Bounded | [[PC FMV playback]]: `mpeg` word disables FMV (`00403B90` → `004ED2A0`); player `004129A0` → DirectShow `AMMultiMediaStream` (`0049BBF0`/`0049BD20`); MPEG-1 `.BUG` files; level gates in `0042E5C0`/`0043DA40` | Does Wine's amstream/winegstreamer play the streams in-game without `mpeg`? |
| Menus, frontend, pause, results | Bounded | Level-select carousel recipe in [[PC autonomous game control]]. Level select `0x00443B40` inside CallOptions `0x00410310`, carousel index and exit store `0x004444C6`, medal display reads `0x00444231`/`67`/`98` (EXP-20261001-003); results-screen medal rule (EXP-20260930-001); save files, the `0x004D8428` record and medal bytes in [[PC save record and medal bytes]]; results loop and carousel internals in [[PC results screen and level select internals]]. Reclassified from Touched on 2026-10-02 | What is the menu/state structure beyond the level select and results (options, pause, save screens)? (2026-10-18: carousel position 0 opens Options_Scr `0x00441D20`, whose first row opens the controls screen `0x00430DF0`: [[EXP-20261018-006 - Controls configuration screen and action bits]]. Pause and save screens are still unmapped.) |
| Lives, continue and level transition | Bounded | `NextLife` `0x0059A5B0`; `Level done variable` log line. Deaths write level-done `0x0059A5B0` = 2 with countdown `0x0059D9B8` (EXP-20260930-006); local death return (EXP-20260909-002); carousel-to-engine index, the special slot and the load screen in [[PC level start, special slot and load screen]]. Reclassified from Touched on 2026-10-02 | What is the full level-completion and transition path beyond these hooks? |

## How to use this

1. Prefer a packet that opens an **Untouched** row or unblocks a **Bounded**
   one over a packet that deepens a **Mapped** row, unless a concrete goal
   needs that depth. Depth is not wrong — the mapped rows are what make the
   modding tools real — but momentum tends to pull work toward ground that
   already has tooling, and this table is here to make that visible.
2. Frame the bounded question from the "top open question" column, then follow
   the work-packet rules in [[Project Roadmap#Work-packet rules]].
3. If a PS1 note suggested the idea, record the comparison under
   [[Cross-Port Evidence Policy]] with source ID, commit, path, and the
   discriminating PC experiment. The PS1 side never closes a PC question.
4. Update the row's status and anchors when a packet lands, and keep this
   table short — it is an index, not a research note.

## Method note for opening an Untouched row

`EXP-20260816-159` was the first packet chosen from this table. Two things
made it cheap, and both generalise:

- **Start from an artifact that already exists.** The import table was
  exported back in `EXP-20260811-003`, so the audio census needed no runtime
  and no new tooling. Rows anchored in imports (audio, input, FMV, and the
  DirectDraw side of rendering) are therefore cheaper first packets than rows
  with no import surface (camera, enemies/AI, event scripting).
- **Resolve the thunks first, then look for pointer records.** This executable
  reaches imports through `jmp dword [IAT]` thunks and its own functions
  through the `0x00401xxx` `jmp` table, so a naive cross-reference search finds
  nothing at all. Thunks alone are still not enough: `EXP-20260816-159`'s own
  central initializer `0x0042BA60` has zero direct call sites and is dispatched
  from a `.data` record at `0x004D81E8`. Check call instructions, both thunk
  directions, **and** `.data` function-pointer tables before concluding that
  anything is unreferenced — and note that register-indirect dispatch can still
  hide callers beyond all three.

[[EXP-20260816-172 - PC creature actor pool and behaviour VM census]] opened a
row with **no** import surface. Its audit rounds produced the rules below.
The list has grown over the rounds, so it carries no count — an earlier
lead-in said "three further things" while the list reached six, and its
replacement said "four audit rounds" when there had been five. Both were caught
by the audits that the rules themselves came from:

- **A row with no imports may still have a log string.** The creature row is
  named by the game itself — `LOAD: Type 35, CreatListRam.` sits directly after
  the loader copy that fills its table. Searching the string table for the
  subsystem's *nouns* fails; searching it for the loader's *log lines* works.
- **An Untouched row is not the same as unexplored code, and the first search
  for prior art is usually too narrow.** **Nine** artifacts here referenced
  that pool base. The census's first two drafts cited three, the third named a
  file that does not contain the address at all and still omitted two that do —
  including `M2-plant-request-origin-static-trace.md`, which already had the
  `CreatListRam` string *and* runtime corroboration for it, and
  `M2-second-deferral-hard-truth-audit.md`, which published the pool extent
  arithmetic verbatim. Three audits were spent on this. Before claiming any
  result is new, grep **every** file in the export directory for the principal
  addresses and the distinguishing strings, and verify each hit rather than
  listing files from memory.
- **Establish a function's extent before making claims scoped to it — and do
  not assume the first `ret` is the end.** The census read `0x0041DC60` to
  `0x0041E1A8` and wrote completeness statements over the whole function; the
  unread part held five flag tests, program-counter writers and an outbound
  `call eax`. The next draft then took the only `ret`, at `0x0041E7D3`, as the
  end — but `0x0041E7D4`-`0x0041E845` is entered from inside the function and
  jumps back into it, and holds a further program-counter writer. Three drafts
  got this wrong three different ways before a fourth audit confirmed the
  extent with nothing beyond it.
- **An extent being correct is not the same as the range having been read.**
  The input census established both function extents correctly and verified
  them — and still wrote two unhedged negatives ("no other writer",
  "not read here") over ranges inside those extents that it had not actually
  read. One of them concealed a real finding. Where a negative covers a range,
  read the range.
- **A correction is a claim, and needs the same verification as the work it
  corrects.** Both defects in the input census's second rejection were
  introduced or left by the first correction pass, including a cited
  instruction address that does not exist.
- **Verify each edit landed before reporting it applied — and do not assert
  that everything landed.** Two correction passes on one packet declared their
  findings applied when they had not: one left a defect's flagship sentence
  half-edited (the replacement was anchored to the second half and left the
  broken first half untouched), and the next left a minor applied in one
  artifact of three. "All findings applied" is a claim like any other, it has
  been false here twice, and each time a later round had to catch it. Prefer
  recording per-item facts over asserting completeness — that is what
  `EXP-20260816-172`'s Audit history table now does.
- **Prefer enumerations to aggregate counts and derived percentages.** Repeated
  audits of one packet produced a string of counting defects — "three M2 exports"
  (eight, then nine), "thirteen sites" (unreproducible; twelve bits over 21
  instructions), "under 40%" (44.4%), "three record-index sites" (at least
  four). None was an analysis error; each was a summary written faster than it
  could be checked. Where a list can be printed, print the list.
- **Grep the generated `ghidra-evidence.json`, not just the authored exports.**
  It is 8 MB, machine-produced, effectively unread, and it already contained a
  decompilation of this subsystem's interpreter — the 26-way dispatch, the
  nine-way sub-switch, the indirect call through the record, and the extra
  program-counter advances. A novelty claim that skips it is not a novelty
  claim. Decompiler output is still evidence rather than a stated model
  ([[Agent Operating Manual]]), so it does not extinguish a packet's
  contribution — but it does bound it, and it should be checked first.
- **A decoded format should be validated, not just described.** The 40 shipped
  scripts were checked four independent ways — table contiguity, zero decode
  misalignment, every branch target on an instruction boundary, and an entry
  offset written by unrelated code landing on a boundary. Any one of them could
  have falsified the instruction-size model on its own.
