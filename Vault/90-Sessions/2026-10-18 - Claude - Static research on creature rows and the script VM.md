---
type: session
date: 2026-10-18
agent: Claude
status: complete-bounded
updated: 2026-10-29
tags: [session, re/creatures]
---

# Static research on creature rows and the script VM

## Agent

Claude (Opus 5.5), in Claude Code.

## Goal

The user asked to continue the earlier work with more static research,
keeping git and the Obsidian vault clean. From section 7 of [[Next Tasks]]
this session took the creature items: KU-069 (unbounded indexes) and
KU-068 (the program counter at runtime), then the interpreter's unread mode
tail, the type handlers and event sounds, and finally KU-071's event
callbacks.

## Files inspected

- Startup set: START HERE, Current State, Environment Status, Next Tasks,
  Known Unknowns (active and the history entries for KU-062–071), the
  Agent Operating Manual, the Project Charter and `make briefing`.
- [[EXP-20260816-172 - PC creature actor pool and behaviour VM census]] and
  its export `SUBSYS-creature-actor-static-census.md`;
  [[EXP-20261012-006 - Creature types from the character loader]];
  [[EXP-20261012-004 - Homing target visibility bit]]; the function notes
  for `0x0041EC40` and `0x0041DC60`; [[PC Dot flight path authoring]].
- Retail `bugs.exe` (`97c95ba5…`), disassembled with capstone. Regions:
  - `0x0041B9F0`–`0x0041EF00`;
  - `0x0044BB70`;
  - `0x004317D0`;
  - the callees `0x00414F80` and `0x00459620`.
- The hash-checked retail CD copy `work/copies/BUGS_PC-full-disc`.
- The saved packets of EXP-20260913-002 (Dot) and EXP-20261005-002 (the
  tough-regulars arm), and the derived EXEs they ran.

## Experiments inspected

- EXP-20260913-002: its
  `dot-*.json` samples hold slot 25's `+0x70`.
- EXP-20261005-002:
  its jsonl samples hold the moved taxi bug's whole slot.

## Changes made

- **New experiments:**
  - [[EXP-20261018-001 - Creature row index census]];
  - [[EXP-20261018-002 - Creature script counter in saved runtime samples]];
  - [[EXP-20261018-003 - Creature VM movement modes]];
  - [[EXP-20261018-004 - Creature type handlers and opcode-11 subroutines]];
  - [[EXP-20261018-005 - Event callbacks and registrations]] (KU-071);
  - [[EXP-20261018-006 - Controls configuration screen and action bits]] (KU-070), with new function notes
    [[FUNC-97C95BA5572D-00430DF0]] and [[FUNC-97C95BA5572D-00441D20]];
  - [[EXP-20261018-007 - Frame wait rounding]];
  - [[EXP-20261018-008 - Direct3D render states and the depth rule]], with a new registry entry
    [[External Source Registry#SRC-WINE-SOURCE]] for Wine's headers and
    defaults (read by a fetch subagent, quoted lines only);
  - [[EXP-20261018-009 - Four-bit page palette rows]];
  - [[EXP-20261018-010 - Two inert data items]];
  - [[EXP-20261018-011 - Type-indexed list table writers and readers]];
  - [[EXP-20261018-012 - Telescope hide flags]] (KU-067).
- **New research scripts:**
  - `research/creature-rows/creature-row-census.py`;
  - `research/creature-rows/script-counter-samples.py`;
  - `research/creature-rows/creature-events.py`.

  They write `reports/creatures/EXP-20261018-001.json`, `-002.json` and
  `-004.json` (numbers, addresses and file names only).
- **Dated pointers:** Known Unknowns (a new section "Creature rows and the
  script VM", KU-063, KU-068, KU-069, Moved bosses); the function notes
  `0x0041EC40` and `0x0041DC60`; EXP-20261005-002; the Experiments MOC,
  Subsystems MOC and Subsystem Coverage Map; Next Tasks; Current State.
- **Correction:** EXP-20261012-006 said 525 rows; its report and this
  census count 534. The claim sweep for "525 rows" now reports new wording
  only.
- **Archive:** two old handoff entries (2026-10-03 and the Thumper image)
  moved verbatim to [[Current State Archive]], so `make briefing` keeps its
  recent sessions within budget.

## Conclusions

- **KU-069, for shipped data.** In 534 rows, type is 1–41 and script 0–39.
  The 19 rows that run a list-walking script select lists 1–6, all present
  in their DATs. The code stays unbounded.
- **The VM's single call site** (`0x0041EE9F`) is gated:
  - bit `0x20` (all 130 seeds) never runs a script;
  - otherwise a row runs it on a frame where it is on screen, where
    `+0x11` is not 100, or where it is type 15.
- **KU-068, for two slots** from saved hardware samples:
  - every `+0x70` value is a decoded instruction start;
  - Dot's first activation matches the decode step for step;
  - the moved taxi bug's op-4 targets equal its list rows in all 55 samples.
- **Creature consumers of type-1 lists** are known per level (KU-063).
- **The five modes** are read: steering, arrival (`+0x14 << 4`), landing,
  a chase near home (`+0x16 << 4`) and a leash, which op 4 moves to the
  previous waypoint. The taxi bug's samples match the speed cap, arrival
  radius, grounding and leash.
- **The ten type handlers and nine opcode-11 subroutines** are read. They
  cover event frames, buried dust, the spider's aimed shot, the mosquito
  dash, emerge and burrow, the wasp ring, and level hooks. The sprite
  census's "no missing sprite" conclusion survives the additions.
- **Creature event sounds are named.** An event's first word is a bank
  sample id (positive: one-shot; negative: a keyed channel). With
  EXP-20260910-004's bank census this names the creature events:
  - emerge plays `ERUPTION.WAV`;
  - the spider's shot plays `THROW01.WAV`;
  - the flyers buzz `WASPBUZZ.WAV`;
  - the badbug's footstep plays `SPIDER01.WAV`.
- **KU-071, answered.** The event table is the platform layer's registry:
  - WINDOWS creates the window and its `+0x08` is the message pump;
  - DIRECTX wraps renderer, input and sound teardown, with a no-op `+0x08`.

  The chooser runs between the two registrations. In 579 saved logs only
  these two events ever register.
- **KU-070, answered statically.** The `0x004D9CF9` array is the controls
  screen's item table. The screen is reached from level select position 0 →
  Options_Scr → first row. The developers' labels give each input bit its
  meaning; Return alone cannot be rebound.
- **Timer rate.** The frame wait passes once `1000 / (ms + 1) ≤ 30`, which
  holds at 32 ms. Gameplay is therefore capped at 31.25 fps, matching the
  measured 30.5–30.9. Under Direct3D the frame-begin routine clears
  half-rate mode each frame.
- **Depth rule.** No `SetRenderState` call sets ZENABLE, ZWRITEENABLE or
  ZFUNC. The game's 24 calls set 15 other states, so the device default
  applies; under Wine that is LESSEQUAL with writes on.
- **Palette rows.** The 4-bit page converter gives each 64×64 block its own
  16-colour palette row. Decoding Anthill page 0 that way matches the live
  buffer an earlier hardware arm read, byte for byte.
- **Two inert data items.** Battle Arena's `primary.165` is skipped by the
  scene walker and singled out by no code. The RAW loader's tags stop at
  `0x7F`, so the `0x101`/`0x102` packets are never read.
- **KU-064, answered statically.** The list table is written only by the
  DAT walk inside the level load, after its clear, so a level without a
  type-1 record sees zero. The note lists all of the table's readers.
- **KU-067, answered statically.** `0x00599C69` is telescope hide flag 2
  of four. The pickup walker parks a telescope out of sight when its flag
  is set, and City's gate 0 hides the second telescope.
- **Two more resolutions the same day.**
  - The camera key: C selects camera mode 2 and turns Flik in place.
  - The results screen's 60 cap is real but set by CallOptions
    (`0x0041032D`).
- **Moved path walkers** follow the same-numbered list in their new level.

## New hypotheses

None recorded as a hypothesis note. The census suggests `+0x11 = 100` acts as
"think only on screen", which no runtime test has shown.

## Runtime follow-up (later the same day)

After the static work the user asked what was next, then said they were
not available for manual reviews: "whatever you need to do here". The
agent chose a bundled read-only arm needing no review and no memory writes.

- [[EXP-20261018-013 - Options screens and the creature gate live]] ran two arms on reflink copies of a derived build, pre-registered,
  each 6/6 and audited clean before and after.
- **Arm A.** Options → "define keys" matched the static mapping in live
  memory and on screen.
- **Arm B.** In City Square, off-screen regular enemies stayed frozen in
  all 15 pairs, and a fly ran on screen and froze after a turn.
- **Not run.** KU-062 and KU-067 need gameplay (a pit death, opening City's
  gate). KU-064 has nothing to discriminate within one process, since the
  frontend's DAT has no lists.

## Decisions

[[Decision Log]] 2026-10-18 adds three items:

- saved samples from derived builds count as runtime evidence only after a
  byte comparison of the executed path;
- completeness claims need whole-image scans over every base register;
- Wine's source is registered as `SRC-WINE-SOURCE`, environment facts only.

## Contradictions discovered

- EXP-20260930-001's results-screen 60 fps cap cites `0x00441D3B`, which is
  in Options_Scr. Resolved the same day: the cap is 60, written by
  CallOptions at `0x0041032D` before it dispatches to the results routine.

- The Flik animation catalog's "turn in place" for C (`0x400`) against the
  controls screen's label "camera". Resolved the same day: the camera code
  selects mode 2 on that bit, and Flik's controller turns him in place
  while it is held.

- EXP-20261012-006's row count (525 against 534), corrected with a dated
  pointer.
- EXP-20261005-002's audit line "reachable script code uses no op4, op10 or
  op11" holds for the boss scripts but not for the taxi bug's script 23.
  That is a scope note, recorded there.

## Tests run

- **A tooling slip, caught and repaired.** The first whole-image linear
  disassembly stopped at `0x004269AB`, the first invalid byte, so greps over
  it saw only a quarter of `.text`.
  - EXP-20261018-008's `SetRenderState` census was re-run as a raw byte scan
    over all of `.text`: 27 sites, identical.
  - EXP-20261018-007's writer lists were re-run on a skip-data sweep. One
    list grew from 3 to 12 writers with the same conclusion, and that run
    found the results-screen contradiction above.
  - Other results used targeted disassembly, the reference scanner over the
    whole image, or the Ghidra export, not that file.

- Both research scripts ran to completion on the retail inputs (hash checks
  passed).
- `make briefing` exit 0, nothing truncated.
- `claim-sweep pair --old "525 rows" --new "534 rows"`: new wording only.
- The pre-commit gates (diff check, tracked-file audit, vault-lint,
  m4-compatibility, compileall) passed at every commit.
- `pytest` on `tests/test_original_level*.py`: 42 passed, after the two
  decoder docstring edits.
- `make check`: exit 0, 5,641 tests passed in 55 min 47 s. It was started
  on the first commit's tree (`ef8600b0`); later commits changed notes,
  research scripts and two decoder docstrings only.
- `make session-audit` at the static close: `clean: true`. For the later
  arms it was clean before each launch, after each close and at the end.

## Unresolved questions

See [[Known Unknowns#Creature rows and the script VM]]:

- the word `0x0059DD80` that vetoes a chase;
- the meaning of the event entry's later fields;
- which script-13 writer ran when the taxi bug died;
- the `0x004C881F` table;
- the consumers of lists that no creature walks.

## Recommended next action

Remaining section 7 items in [[Next Tasks]]:

- KU-062, which needs a runtime sample;
- all of the small closures are done.

A runtime look at the options and controls screens would give KU-070 a
second form. The next creature-side read is a boss level routine, such as
Thumper's `0x00431CB0`.

## Git commit if applicable

Committed on `main` with this note.
