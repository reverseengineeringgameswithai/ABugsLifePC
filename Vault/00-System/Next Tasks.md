---
type: plan
status: active
updated: 2026-10-29
tags: [system/plan, planning/backlog]
---

# Next Tasks

A prioritized snapshot of the open research tasks as of 2026-10-29. It keeps
the open items of the 2026-10-12 survey
([[2026-10-12 - Claude - Survey and prioritize next tasks]]) and adds what the
2026-10-18 session left open
([[2026-10-18 - Claude - Static research on creature rows and the script VM]]).
Items finished since are not repeated; [[Current State]] summarises them.

[[Project Roadmap]] still owns sequencing and [[Known Unknowns]] still owns the
questions. This note proposes an order; it authorizes nothing. Every runtime
arm still needs `make session-audit` and the lifecycle in
[[Agent Operating Manual]], and every live-memory write still needs fresh
permission. Items are pointers, not evidence: re-read the cited source before
acting. Re-survey or retire this note once its first priorities are done.

**Key.** Mode: offline (static, emulation, tests, notes) or **arm** (a runtime
launch, which needs the user's OK). Effort: S under an hour, M about a
session, L several sessions.

## 1. Cheap runtime arms with large payoffs

Each is one read-only launch unless stated.

1. **CAP-010 acceptance.** Arm, M.
   - One owned-session arm comparing `game-session`'s gate verdict, PID,
     window and close audit with the manual procedure.
   - Passing it lets later arms use the session tools as evidence, so it
     makes every item below cheaper.
   - Sources: [[Reverse Engineering Capability Gaps]],
     [[Session control plane]].
2. **FMV under Wine.** Arm, S.
   - One launch without `mpeg`, into the next unplayed level, decides whether
     Wine plays the MPEG-1 `.BUG` streams in-game.
   - Source: [[PC FMV playback]], [[Known Unknowns#Level FMV playback]].
3. **Flik's action states.** Arm, S–M.
   - No arm has watched `0x0059D998`/`0x0059D996` during play. A read-only
     Training arm (run, walk, turn, jump, second Shift, throw, pick up, idle)
     decides the state numbers.
   - The same arm should watch `0x0059D994` and `0x0059D940` through a second
     Shift: the hover length of movement state 4 is open.
   - Sources: [[PC Flik animation catalog]],
     [[EXP-20261012-005 - Flik movement state 4 ground pound]],
     [[Known Unknowns#Flik animations]].
4. **Seed draw height.** Arm, S.
   - Flagged seed records sit 400 stored units below the maps' markers
     (`0x0041C579`). Whether the visible seed is drawn there needs one
     observation.
   - Source: [[FUNC-97C95BA5572D-0041C420]].
5. **Creature types at runtime.** Arm, M.
   - 15 of the 41 types are named by the loader only, and two appearance
     hints contradict their file names (31 acorn, 37 weevil).
   - One live read-only spawn observation per type decides both.
   - Sources: [[EXP-20261012-006 - Creature types from the character loader]],
     [[Known Unknowns#Original level maps]].
6. **Runtime samples for statically answered questions.** Arm, S each.
   - KU-062: the auxiliary query value at the instant of reset selection.
   - KU-064: the type-indexed table for a level without the record (statically
     zero, [[EXP-20261018-011 - Type-indexed list table writers and readers]]).
   - KU-067: a trace of the telescope hide flags
     ([[EXP-20261018-012 - Telescope hide flags]]).
   - Battle Arena's record 165 and the RAW tags `0x101`/`0x102`, statically
     inert ([[EXP-20261018-010 - Two inert data items]]).
   - KU-074: whether the level-select carousel counter advances once per
     accepted press.

## 2. Offline research

Project policy puts recorded contradictions ahead of new mapping.

1. **Creature VM residue.** M. From
   [[Known Unknowns#Creature rows and the script VM]]:
   - what word `0x0059DD80` is (it vetoes the chase);
   - the meaning of `0x00599B20[type*5 + berry]` in the chase gate;
   - what sets mosquito flag `0x1000`, what subroutine 6's 21 part entries
     control, and whether the long-legged spider's kind-`0x7A` shot hurts
     Flik;
   - which of the fourteen sites that load script 13's entry `0x004C8424`
     runs on a kill;
   - the meaning and extent of the table at `0x004C881F` (48 entries
     examined; shipped types reach 41).
2. **Level routines and lists without a creature walker** (KU-063). M.
   Council Chamber, Riverbed Flight, Anthill Pt 2, Riverbed Canyon and Bug Bar
   hold type-1 lists that no creature walks; their consumers are level
   routines or unknown.
3. **Raw-scan pass over cited globals.** S–M. The `0x0059A5EE` census found a
   reference in code Ghidra never made into a function. One raw scan over the
   globals that other censuses cite would show how many relied only on Ghidra
   references ([[Known Unknowns#REA trial and the `0x0059A5EE` census]],
   [[Decision Log]] 2026-10-12).
4. **Camera modes** (KU-066). M. The manual controls are known (C selects
   camera mode 2, X mode 3, in `0x0041ADF0`); what the modes look like, the
   source roles, the second consumer and runtime frequency are open
   ([[PC camera view-transform chain]],
   [[EXP-20261018-006 - Controls configuration screen and action bits]]).
5. **Rows of the [[Subsystem Coverage Map]] with a top open question.** M–L
   each:
   - `LEVEL.RAW`: its record grammar and consumers;
   - `LEVEL.DAT`: most top-record types and payload fields (`KU-009`);
   - player physics: where gravity integrates, and movement state 5's writers;
   - audio: whether sound effects use a path separate from the music tracks;
   - menus: the pause and save screens;
   - level flow: the completion and transition path beyond `NextLife`.
6. **Flik animation residue.** M. Candidate names (the Z move, hanging from a
   seed, the tired idle, plant type 8, the Anthill Pt 2 bounce actors), the 24
   parts and their channels (needs the `.ALL` hierarchy), unreferenced slots 7
   and 12, Bug Bar's state-0 fallback and the harvester rider
   ([[Known Unknowns#Flik animations]]).
7. **Original level map residue.** M. The role of pickup selector `0x31`, the
   consumer of model normal tables and two Clover Forest type-27 tails, the
   far-offset seed model parts, page 18 missing from City Square's RAW for
   creature type 19, and the engine-16 stage's identity
   ([[Known Unknowns#Original level maps]]).
8. **Small residues.** S each. Joystick mode in the controls screen (KU-070);
   the four only-zeroed event-record fields (KU-071).
9. **Unused content leads.** S. The placeholder berry graphics and the
   graphic with PlayStation button images named on the TCRF page, which names
   no file; its development-text sub-page is unread
   ([[External Source Registry#SRC-TCRF]]).
10. **Kev holdout evaluation,** if the advisory pilot is wanted. M.
    Freeze different experiments and competing evidence before querying
    ([[EXP-20261007-001 - Local Kev evidence classification probe]],
    [[Known Unknowns#Local Kev evidence review]]).

## Tooling decisions

- **REA (github.com/morluto/rea).** Tried in [[EXP-20261012-001 - REA Ghidra analysis trial]]: optional, not adopted. It
  is pinned in `work/tools/rea-agents-6.4.0` and registered with no agent.

## Parked: do not start without the user

- R2q (dropped on 2026-09-27) and R2p (paused).
- M2 (deferred at its causal gate, `KU-023`).
- KU-081 and the remaining KU-079/080 geometry work (L).
- [[Flight Recorder]]'s later phases.

## Suggested order

1. **CAP-010 (1.1),** because it lowers the cost of every later arm.
2. **The other arms in section 1,** each with the user's approval; 1.2 and 1.3
   are the cheapest.
3. **Section 2,** contradictions first (the creature-type hints in 1.5 need a
   runtime observation, so they wait for an arm).
