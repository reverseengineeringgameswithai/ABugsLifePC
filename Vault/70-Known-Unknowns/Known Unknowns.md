---
type: register
status: active
updated: 2026-10-29
tags: [register/unknowns]
---

# Known Unknowns

This is the active issue summary. The linked historical register retains every
older question, correction and failed arm. No unmentioned question is declared
resolved by this compaction, and these items are not an automatic work queue.

## Creature rows and the script VM

[[EXP-20261018-001 - Creature row index census]] answers KU-069 for shipped
data: no retail row drives an unbounded creature index out of range.
[[EXP-20261018-002 - Creature script counter in saved runtime samples]]
answers KU-068 for two slots from saved samples. Open:

- **The five modes.** (2026-10-18: answered statically by
  [[EXP-20261018-003 - Creature VM movement modes]], with the taxi bug's
  samples matching speed, arrival, landing and leash.) Open from it:
  - what word `0x0059DD80` is (it vetoes the chase);
  - what makes `+0x20` negative for mode 3 (2026-10-18: opcode-11
    subroutines 1, 2 and 3 do,
    [[EXP-20261018-004 - Creature type handlers and opcode-11 subroutines]]);
  - the meaning of `0x00599B20[type*5 + berry]` in the chase gate;
  - what the ten per-type handlers do (2026-10-18: read in EXP-20261018-004).
- **Creature event ids.** (2026-10-18: named. Each event's first word is a
  bank sample id, and the creature events play `WASPBUZZ`, `ERUPTION`,
  `THROW01`, `SPIDER01`, `BOULDER`, `SEEDROLL`, `CANNPLNT` and `DANDLION`,
  per EXP-20261018-004.) Still open: what sets mosquito flag `0x1000`, what
  subroutine 6's 21 part entries control, and whether the long-legged
  spider's kind-`0x7A` shot hurts Flik.
- **Script 13's writer for a kill.** Fourteen sites load script 13's entry
  `0x004C8424`; which one ran when the moved taxi bug died is not traced.
- **`0x004C881F`.** The table's meaning and extent; only 48 entries are
  examined, and shipped types reach 41.
- **Lists without a creature walker.** Council Chamber, Riverbed Flight,
  Anthill Pt 2, Riverbed Canyon and Bug Bar hold lists that no creature
  walks; their consumers are level routines or unknown (KU-063).
- **Off-screen enemies.** Rows with `+0x11 = 100` run their script only
  while on screen (static gate `0x0041EE89`). (2026-10-18: confirmed live
  in City Square. 15 off-screen sample pairs were frozen, and a fly ran on
  screen and froze after a turn, [[EXP-20261018-013 - Options screens and the creature gate live]]. Rows with another `+0x11`
  were not exercised.)

## REA trial and the `0x0059A5EE` census

[[EXP-20261012-001 - REA Ghidra analysis trial]] found that REA's Ghidra path
matches the existing export on bugs.exe. A raw scan found an 11th reference to
`0x0059A5EE`, a 16-bit store at `0x41a992`, in code Ghidra never made into a
function. Open:

- **The `0x41a992` routine.** (2026-10-12: its entry is `0x0041A910`, through
  thunk `0x00401023`, an eye-and-target camera setter. Neither address has a
  direct call or a stored pointer, so it is probably unused ([[EXP-20261012-003 - Scripted camera flag census]]).)
- **Other globals.** How many other censuses rely only on Ghidra references
  and miss code of this kind. One raw-scan pass over the cited globals would
  tell.
- **REA over MCP.** Per-query cost in a persistent session (one import) is
  unmeasured. The CLI took 60–90 s per command under load.

## Local Kev evidence review

[[EXP-20261007-001 - Local Kev evidence classification probe]] matches 35/36
primary labels on curated evidence excerpts, with no false supported answer;
one conservative status decision changes with option order. Open: accuracy
and false-confirmation rate on an independently labelled holdout, conflicting
or stale notes, imperfect retrieval, raw x86 and long contexts. No probability
threshold is calibrated for ABLPC. Next discriminator: freeze different
experiments and competing evidence before querying, keeping review advisory.

## Moved bosses

EXP-20261005-001 and
EXP-20261005-002 move
every native boss and six tough regulars into Moonlit as test images. Open:

- **Homing lock-on.** (2026-10-12: resolved statically by [[EXP-20261012-004 - Homing target visibility bit]]. Bit 0x0001 is
  set each frame by `0x00456640` for actors inside the camera's view, so
  homing picks the nearest on-screen live actor.) Static `0x00428400` needs
  flags bit 0x0001, which no
  donor row has; at runtime every boss had it once awake. Airborne bosses took
  purple hits and a frame shows a berry climbing to a flying Hopper. No writer
  of the bit was found. Sample the purple projectile's +0x10 target and +0x33
  bit 0x08 with one enemy near.
- **Boss routines.** Each fight is its home level's routine (EXP-002 lists
  them) bound to fixed slots; none runs in Moonlit. Porting one needs its
  slots, projectiles, voices (home bank), camera and win write retargeted.
  Three boss routines change `0059D99E` themselves (`004369B0`, `0043AD00`,
  `00438720`; EXP-20261001-006). See
  [[PC boss level routines and creature transplant limits]].
- **Immune donors.** Hopper (Riverbed Flight) and the Cliffside and Canyon
  Showdown birds have health 101; they keep the enemies-left count above 0.
- **0x101/0x102 packets.** Inferred unused on PC (no RAW case, loader reads
  the disc files); a build without them would decide it. (2026-10-18: the
  loader's whole tag list stops at `0x7F`, and no code compares either value:
  [[EXP-20261018-010 - Two inert data items]].)
- **Donor pickups and sprite entry 0x33 (2026-10-12).** A level's sprite
  table (`005BFD70`, filled per level) can lack effects used by other code
  paths. Entry 0x33, which the pickup walker's default retirement action 0xC
  needs, is absent in engines 1, 2, 4, 6, 11, 14, 16 and 19
  ([[EXP-20261012-002 - Sprite table census]]). Moonlit
  runs on engine 1's sprite list. A donor drop that reaches the pickup
  walker's default case would crash there, as the first pickup of an added
  record did (the default case's action 0xC spawns type 0x40 through
  `00428AA0`; EXP-20261001-006). All 14 test images ran without a fault,
  but which native drops reach that case is unknown. (Later on 2026-10-12, the
  extension in [[EXP-20261012-002 - Sprite table census]]: no table-collectible drop reaches that case. A creature's
  script, contact and kill drops all use sprites below 50. The spawners of
  five sprite-50/52 types remain unknown.)
- **Moved path walkers (2026-10-18).** A moved row whose script runs op 4
  or op 10 walks the target level's list of the same slot, and faults at
  `0x0041DDDE` if that slot is empty
  ([[EXP-20261018-001 - Creature row index census]]). The moved taxi bug
  walked Moonlit's list 1, Dot's route, which is why it "ran far east":
  all 55 saved samples match
  ([[EXP-20261018-002 - Creature script counter in saved runtime samples]]).
  The Canyon Showdown Hopper's list walk is only entered by engine 15.

## Flik animations

[[EXP-20261001-002 - Flik animation catalog]] maps every slot and action state
statically ([[PC Flik animation catalog]]). Open:

- **Runtime confirmation.** No arm has watched `0x0059D998`/`0x0059D996` during
  play. A read-only Training arm (run, walk, turn, jump, second Shift, throw,
  pick up, idle) decides the state numbers.
- **Movement state 4.** (2026-10-12: statically a hover, dive and ground pound
  with an 8-shot ring on landing, [[EXP-20261012-005 - Flik movement state 4 ground pound]]. Hover length and ring damage are
  open.) "Gliding" in EXP-20260930-004 versus a hover-then-dive
  ground pound here (`0x0044033C`, `0x00440390`–`0x00440419`); the same arm
  should watch `0x0059D994` and `0x0059D940` through a second Shift press.
- **Candidate names.** The Z move (state 1), hanging from a seed (`0x10`), the
  tired idle (`0x1F`), plant type 8, the Anthill Pt 2 bounce actors (slots 2
  and 3) and which seeds reach seed-state 3.
- **Parts and channels.** Which body part each of the 24 (FLICKP: 29) parts
  is, the axis order of the angles, the units of the linear words, and whether
  the extra words are a 4.12 scale (Flik's part 8 fits; other models do not).
  Needs the `.ALL` hierarchy.
- **Unreferenced slots 7 and 12.** Present, never referenced; their content
  needs a preview or a write-authorized forced-state arm.
- **Bug Bar.** Idle-family and turn states become state 0 at full speed
  there (`0x00403137`); the visible result is unverified.
- **Harvester rider.** Whether Flik's model is drawn while riding FLIKHARV, and
  what its part-mode change (`0x00446870`) shows.

## Engine questions from derived test builds

These came up while testing derived builds; each names its experiment. The
established facts around them are in [[PC gameplay loop and player event sites]],
[[PC results screen and level select internals]],
[[PC save record and medal bytes]] and
[[PC level start, special slot and load screen]]. Open:

- **Results frame cap (resolved 2026-10-18).** EXP-20260930-001's 60 fps cap
  cites `0x00441D3B`, which is in Options_Scr. The cap is still 60: the results
  screen runs inside CallOptions, which writes it at `0x0041032D`
  ([[EXP-20261018-007 - Frame wait rounding]]).
- **Depth rule.** Tpage 51 drawing above the other results sprites is confirmed
  by captures (EXP-20260930-001). That this follows D3D's default LESSEQUAL
  (`00420C80` sets no Z state) was inferred, not traced. (2026-10-18: traced. No
  `SetRenderState` call in the image sets a Z state, and Wine's device default
  is Z on, writes on, LESSEQUAL:
  [[EXP-20261018-008 - Direct3D render states and the depth rule]].)
- **Frame rate.** An unpaused-frame counter ran at 30.5–30.9 rather than 30
  frames per wall second (EXP-20260930-002). The `00405AD0` wait's rounding was
  inferred, not traced. (2026-10-18: traced. The wait passes at 32 ms because
  1000/33 = 30, capping play at 31.25 fps,
  [[EXP-20261018-007 - Frame wait rounding]].)
- **Movement-state writers.** Flik's movement state `0059D990` enters 1 through
  controller `0043F9E0`; every other absolute writer sets 5 or 0
  (EXP-20260930-004). Open: the roles of the state-5 writers `0041C6C0`,
  `00434E10`, `00436B40` and `00439E90`; gamepad jumps (the same input bit
  0x4000) and the controller's special-mode jump (state 1 on a fresh Shift edge)
  in hardware.
- **Throws.** The player controller calls `0043EB60` from the single site
  `00440555` (throw animation frame 10) (EXP-20260930-005). Controller throws
  and blue berries in hardware (the same counted call) are untested.
- **Damage and deaths.** `0041C7A5`, in the hit handler, is the single health
  decrement; hits during invulnerability never reach it (EXP-20260930-006).
  Open: damage from real enemy contact, seeds and plants (only a native mode-0
  call was exercised in hardware); whether any death skips the death countdown
  `0059D9B8`, which would hide level-done 2.
- **Results draw budget.** `00409150` drops draws past its buffer. About 40
  glyph draws per results frame lost none in hardware (EXP-20260930-006); the
  limit itself was not measured.
- **Save record size.** The game reads each slot file's 540-byte record with one
  `fread`. Whether the unmodified game loads an 804-byte slot file has not been
  run (EXP-20261001-001).
- **Load-screen fade.** All load-screen draws seen in hardware were fade-scaled
  (`0040A090`, `00404AE0`; `00404410` references the fade), so aiming the level
  start's load-screen fade (`0042E68A`) at black covers the picture, the loading
  sprite and the sky (EXP-20261001-004). A draw on that screen without the fade
  would still show.
- **Four-bit page palettes.** Is page 0's palette one 16-entry row per 64×64
  block (`(v/64)*4+u/64`)? It was inferred from flat lower-row tiles
  (EXP-20260928-001), not from a traced renderer routine. (2026-10-18: answered
  yes. The converter's 4-bit branch `0x004630D2`–`0x00463126` computes exactly
  that row, and decoding Anthill's page 0 with it reproduces the live index
  buffer of EXP-20260905-005 byte for byte:
  [[EXP-20261018-009 - Four-bit page palette rows]].)
- **Plant orientation.** Whether plant models are ever rotated per seed;
  EXP-20260928-001 assumed unrotated templates.
- **Height-model agreement.** On authored geometry the project's model
  sentinel-height criterion fails at (-8100, 31300), where model plane −156096
  disagrees with movement contact near the visual floor (EXP-20260916-014).
  Whether native `004AC460`/`004ACA60` agree with the model there is
  unconfirmed. Next discriminator: replay those original-PC height entries and
  inspect the accepted cell corners and plane at exactly the same X/Z.

## Level FMV playback

[[PC FMV playback]] shows that every project launch passes `mpeg`, which the game
treats as "Mpeg play OFF", so no cutscene can play. Level intros additionally
play only for the next unplayed level. Open: whether Wine plays the MPEG-1
`.BUG` streams through `amstream` once `mpeg` is removed; one runtime launch
decides it.

## Original level maps

[[EXP-20260927-001 - Complete original level Blender maps]] leaves these open:
identities of 32 of 40 creature types (14 carry appearance-only hints)
(2026-10-12: all 41 types now have loader file names, 26 also confirmed by
runtime logs, [[EXP-20261012-006 - Creature types from the character loader]]. Still open: the two hint-versus-file contradictions
(31, 37) and runtime for 15 types); the
role of pickup selector 0x31 (persistent, shares the telescope fall-through);
Battle Arena's undispatched `primary.165` (flags `0x93`; 2026-10-18: the walker skips it and no code singles it out, [[EXP-20261018-010 - Two inert data items]]); the consumer of model
normal tables and two Clover Forest type-27 tails that do not fit that reading;
the far-offset seed model parts; page 18 missing from City Square's RAW for
creature type 19; and the engine-16 stage's identity (circus-tent appearance).
Pickup heights come from offline `00456A90`, not a live comparison.
Seed heights (added 2026-10-02): 130 retail seed rows set flag `0x20` at
`+0x12`, which the note had said no row sets. For those rows `0041C420` adds
`0x3200` to the floor query (`0x0041C579`), while `map-original-levels.py`
records the plain floor for every creature. Whether the maps' seeds sit
`0x3200` runtime units off is unchecked ([[FUNC-97C95BA5572D-0041C420]]).
(2026-10-12: checked statically. Each flagged seed record's runtime Y is the
floor plus `0x3200` (`0x0041C579`). Positive Y is down, so the record is 400
stored units below the maps' markers. Whether the visible seed is drawn there
is still open.)
Next discriminator: one live read-only spawn observation per creature type.

## Remaining Anthill object imports

[[PC Anthill scenery assemblies]] records original collision profiles for
Anthill's rock, thorny vines and offering surround. In EXP-20260926-002, twenty
solid additions pass 53 original-code samples, seven profile placements
reproduce original traces, and all 20 payloads are active in hardware. Broader
approach/route, camera and damage/interaction behavior remain open. The first
revision's passing samples missed a real coverage defect; retain that
discrepancy in EXP002.

The negative-count mesh at DAT `0x2F700` retains its 656-byte opaque span and
original near renderer; its auxiliary semantics and interactive role remain
unknown. No launcher/damage role or distant counterpart is invented.
The remaining inventory includes landscape fragments and secondary
geometries, not automatically usable prop families. [[PC Anthill remaining object inventory]]
retains the pre-import census. The original small and round stones have no
paired collision shell at the EXP-20261005-003 audit's thresholds; four small
unpaired sources (159–162) lie among stones. Additional ground or props must
pass the same unchanged allocation limits: the 2,000,000-byte combined load and
a collision density of 300.

## Current regression-gate failure

**Resolved 2026-10-12.** `make check` passed in full on 2026-10-12: 5,639 tests in 52 min 27 s under host load (load average
17–26 on 16 cores). R2c–R2o took 16.4 min of that. All gates exited 0. The changes ([[Decision Log]] 2026-10-12):

- R2p and R2q tests are opt-in through `pytest.ini`. Run them by naming the
  files; their failures below stand unchanged.
- The M4 gate quotes the note's accurate "The historical R2c retail branch
  used fresh RC0…".
- The pre-commit hook runs that gate.

The history below is kept.


October 2's non-R2q suite (7,229 passed) fails all seven tests in
`tests/test_r2p_p0c_attribution.py` with `source anchor mismatch:
reimplementation/ablpc/anm.py`. That file last changed in `b73fb31` (the Flik
animation catalogue, 2026-10-01), and the frozen R2p attribution anchors pin
its older copy. Re-anchoring is left for the user, as with R2q.

September 26 independently reproduces
`tests/test_r2p_p0e_y_restore.py::test_action_journal_name_substitution_across_exchange_is_detected`.
The expected journal-substitution exception occurs, but the synthetic `y:` link
resolves to the temporary retail directory instead of the expected stage at
line 923. The test, recovery implementation and checked dependencies are byte
identical to entry commit `0c6e328`. This was an open failure in the unchanged
historical recovery path; no live mapping or game state was used or modified.
It no longer reproduces: the test passed in the 2026-09-27 full run and in an
isolated 2026-10-02 rerun (1 passed in 0.12 s), and the 2026-10-02 non-R2q
suite reported no failure outside the seven above. The test file is unchanged
since `32d8a83` (2026-08-27), before `0c6e328`, so the September 26 failure was
at most environment-dependent. The September 26 record stands.

September 27's full `make check` also fails a cluster in
`tests/test_r2q_quiet_census_design.py` with `DesignError: R2q terminal benchmark
executed-source drifted`. The newest anchor
`reimplementation/ablpc/r2q_terminal_publication_benchmark_anchor_018.json`
(commit `45ae953`) pins that test file at SHA-256 prefix `9a2efa1c`; HEAD and the
working tree hold `69b8c6b6`, last changed by `1d82c8a` (2026-09-16). All seven
pinned sources are byte-identical to HEAD, so this predates EXP-20260927-001.
Re-anchoring or restoring the file is an R2q decision, not done here. The user
reports (2026-09-27) that R2q was recently dropped for taking too long, so this
gate and the R2q packets may be outdated rather than an active queue.

`tests/test_repo_hygiene.py::test_agents_and_claude_instructions_are_identical`
failed from `0376cad` (2026-09-11) until 2026-10-01, when CLAUDE.md was resynced
from AGENTS.md (the user accepted that recommendation); it passes now.

That full run took 3 h 24 min and ended with 203 failed and 371 errors. R2q tests
each left about 1.5 GB in pytest's temporary directory, 49 GB in total on the
RAM-backed `/tmp` tmpfs, until `Errno 122 Disk quota exceeded` broke later tests.
All 485 non-R2q failures were in files that passed separately with free space
(2,300 passed, the AGENTS/CLAUDE check failed). Clear `/tmp/pytest-of-$USER`
after such a run, or exclude R2q, before trusting a full `make check`.
`reports/project-review/2026-09-26/recovery-regression.json` records the isolated
failure and hashes. If it recurs, diagnose the fixture/rollback boundary
separately; do not rewrite frozen recovery evidence or infer new runtime
permission from this review.
The session note owns the full-gate and focused-check terminal results.

Since the 2026-10-02 vault audit, `make check` also stops at
`m4-compatibility`, before its tests. That gate (`compatibility.py`) requires
the exact sentence "Active R2c uses fresh RC0 with no directional input before
Return." in the Wine Linux Play Baseline renderer selection. `d1d5e08d`
reworded it as "The historical R2c retail branch used fresh RC0…". The same
cause fails 11 tests in `tests/test_compatibility.py` and
`tests/test_release.py::test_installed_entry_points_preserve_complete_inventory`;
all 12 reproduce on a clean `71c1b213` checkout. The 2026-10-03 non-R2q suite
had 7,268 passed and 19 failed: these 12 plus the seven `test_r2p_p0c_attribution`
anchors. Restoring the wording or retiring the R2c-era gate is left to the
user, as with R2q (found in EXP-20261003-001).

## Runtime, rendering and remaining gameplay scope

- CAP-010's session-control acceptance against the real game is still open.
  Host audit success is only a process census. [[PC autonomous game control]].
- Exact compressed storage reclaim remains unmeasured. The September 20
  filesystem-wide availability change is not an isolated physical measurement.
  2026-09-20 - Codex - Remove old generated game builds.

## Legacy numbered register

The following statuses are extracted from the pre-review register, **not newly
revalidated**. Their full qualifications and later chronological updates remain
in [[Known Unknowns history through 2026-09-26]]. Current issues above take
precedence over historical runtime or work-queue wording.

- **KU-001 (open (no status recorded in the note)):** Root bugs.exe is the installer-designated candidate; its disc-copy hash, architecture, imported libraries, and Ghidra baseline are known. (2026-10-02 audit: its identity as the game executable is confirmed by its unchanged run to play under Wine, [[EXP-20260811-004 - Wine launch and CD sentinel gate]]; image base `0x00400000` and entry `0x004B1670` are recorded in [[BIN-97c95ba5572dce63 - bugs.exe]]. Version resource, compiler provenance and Win98 behavior remain open.)
- **KU-002 (open (no status recorded in the note)):** Required Win98 hardware, graphics adapter, sound adapter, driver versions, DirectX version, and resolution remain unknown.
- **KU-003 (open (no status recorded in the note)):** Wine 11 staging reaches playable Direct3D training rendering under EXP-20260812-005, and Gamescope provides the aspect-preserving host presentation in EXP-20 …
- **KU-004 (open (no status recorded in the note)):** Whether a modern Windows debugging VM is necessary is unknown.
- **KU-005 (open (no status recorded in the note)):** Whether PCem cross-validation will be necessary is unknown.
- **KU-006 (open (no status recorded in the note)):** The remaining Fedora utilities are not installed until sudo authorization is provided.
- **KU-007 (open (no status recorded in the note)):** The degree of code, data-format, and behavioral similarity between the PS1 and PC ports is unknown; each proposed correspondence requires a bounded comparison a …
- **KU-008 (resolved):** Matched individual mutations produce three disjoint visible plant-element differences, and native watchpoints route all three records through 0x0044D5B8.
- **KU-009 (open (no status recorded in the note)):** Semantics of LEVEL.DAT record types, many payload fields, negative signed record +0x0C, negative-count target blocks, dispatches other than the bounded 0x …
- **KU-010 (open (no status recorded in the note)):** Direct absolute work-tree paths fault downstream at 0x004A84A4 for both modified and unmodified files; the specific legacy path or loader assumption is unknow …
- **KU-011 (resolved):** A compositor portal capture produced a discriminating cropped control/mod pair in EXP-20260812-006; ordinary X11 capture remains unsuitable for these DirectDr …
- **KU-012 (open (no status recorded in the note)):** The exact period-correct texture filtering, display scaling, monitor behavior, and WineD3D-versus-Windows rendering differences remain unknown.
- **KU-013 (narrowed by static audit; runtime open):** EXP-20260816-143 - Automatic Direct3D startup static audit proves the exact retail executable has no native renderer-selection or chooser-bypass argument.
- **KU-014 (open (no status recorded in the note)):** EXP-20260812-010 resolves the guarded-rebind discriminator: reciprocal 0x111E4/0x1319C edits change only the selected placement's phase-matched visible co …
- **KU-015 (open (no status recorded in the note)):** A late 25-second gameplay watch window did not reread record 124, but the full lifetime and revisit conditions for primary scene records remain unknown.
- **KU-016 (open (no status recorded in the note)):** 0x0045A7F0 has a distinct negative-count target branch, and other masked scene dispatch values use different payload consumers.
- **KU-017 (resolved within dispatch 0x49):** The first three record dwords are upstream candidate-center components, not the render-placement tuple; relocated +0x10 supplies the payload used for placemen …
- **KU-018 (open (no status recorded in the note)):** EXP-20260812-013 accepts a Level 01 record-261 center edit and guarded 0x3703C -> 0x3459C rebind, but both retain exact control frames at the starting camer …
- **KU-019 (partially resolved):** EXP-20260812-014 records the exact derived PC content-family census, five duplicate-hash groups, and the explicit paths requested in unchanged Training and Le …
- **KU-020 (partially resolved):** EXP-20260812-015 confirms that selected .ANM/.ALL basenames share coordinator 0x00444C40 but use distinct load call sites and immediate consumers.
- **KU-021 (resolved at the traced boundary):** 0x00416100 emits plant ID 5 literally. Exact Training DAT type-0x3F selector bytes at 0x394, 0x3A4, and 0x3B4 produce IDs 4, 10, and 6 through pointer …
- **KU-022 (partially resolved):** EXP-20260812-017 bounds the .ANM first-level count/offset walk, first nonzero referenced header/list, and -2 comparison.
- **KU-023 (narrowed):** A direct dependency from an M1 20-byte placement record or positive target to a specific plant/resource identity remains unknown.
- **KU-024 (resolved at the tested boundary):** Replacing plant 04 .ANM with exact plant 10 .ANM bytes while retaining plant 04 .ALL is accepted under Direct3D Training and reaches NextLife.
- **KU-025 (resolved at the tested boundary):** Plant 04 and 10 .ALL files are both 0xE08 bytes.
- **KU-026 (partially resolved/corrected):** EXP-20260812-020 proves that changing only the second Training 0x2B selector at 0x3A4 to 0x00 removes both plant 10 request lines, otherwise preserves t …
- **KU-027 (partially bounded):** EXP-20260812-021 binds the exact Training plant 10 destination to ANM slot 0x005B1AA4 and two entries at 0x005AAB00, 0x005AABA0).
- **KU-028 (root cause identified; fix needs one root action):** rr record cannot capture the Wine 11 run while Wine's in-kernel synchronization driver ntsync is present: Wine issues ioctl(0x80044e88) on anon_inode …
- **KU-029 (partially resolved):** Freezing the single game PID with SIGSTOP, capturing a frame via gamescopectl screenshot, and resuming works cleanly; a re-verification frame was visually c …
- **KU-030 (narrowed):** apitrace --api egl (not GLX — WineD3D drives GL through EGL on this Wayland/XWayland host) captures a valid, apitrace dump-parseable GL stream with real dra …
- **KU-031 (narrowed to nearby caller-gate continuation fault):** Exploratory RUN-GDB-20260812-204252 first recorded SIGSEGV at hardware- breakpoint PC 0x0044D79A even though its structured result later reported cleanup …
- **KU-032 (resolved at the M2.20 visible boundary):** Retained unchanged Training logs explicitly request CD/CHARS/FLICK.ANM/.ALL.
- **KU-033 (resolved at the M2.21 request/first-consumer boundary):** EXP-20260812-034 binds accepted Training chars\flick.all to 0x004671D0 -> 0x00445020 -> 0x00444C40 -> 0x00448010 -> 0x004AE240.
- **KU-034 (resolved at the M2.22 direct-bridge window):** EXP-20260813-035 classifies the first proven unindexed post-initialization ID-zero read in one normal 0x0040FFC0 branch.
- **KU-035 (resolved at the M2.23 conditional-output boundary):** EXP-20260813-036 traces the retained-entry and M1 positive-target inputs through exact PC address formation.
- **KU-036 (resolved at the M2.24 record-span boundary):** EXP-20260813-037 maps the exact 24 retained ID-zero intervals to 0x0004,0x2AE8).
- **KU-037 (resolved negatively at the M2.25 conditional-arena boundary):** EXP-20260813-038 records one complete ordered cycle for exact candidates {0-7, 9-23} in each of fresh accepted Direct3D control/replacement/control arms.
- **KU-038 (resolved at the M2.26 renderer-path boundary):** EXP-20260813-039 maps selector 1 to native software render and selector 2 to Direct3d render.
- **KU-039 (resolved at the M2.27 Direct3D count boundary):** EXP-20260813-040 statically accounts for both selected batch families and every reachable in-call flush/reset, then records fresh accepted hardware-rendered c …
- **KU-040 (resolved at the M2.28 form/count boundary):** EXP-20260813-041 reanalyzes both complete retained cycles in all three M2.27 arms and maps the exact pre-call record pointers/forms without a new runtime.
- **KU-041 (resolved at the fresh per-record outcome boundary):** EXP-20260813-042 maps exact append writes 0x004069A1/0x00407B00 and all earlier no-append edges, then accepts fresh metadata-only Direct3D control/replaceme …
- **KU-042 (resolved at the exact builder-input boundary):** EXP-20260813-043 finds exactly 12 differences in record-relative spans +0x00..+0x02, +0x24..+0x26, +0x28..+0x2A, and +0x2C..+0x2E.
- **KU-043 (resolved at the M2.31 admission-slice/design boundary):** EXP-20260813-044 reduces the physical non-source input union for exact record 0x0A6C to 23 locations, with at most 22 read in one native path because two th …
- **KU-044 (resolved at live evaluator agreement; stable attribution rejected):** EXP-20260813-046 live-validates the exact schema-6 evaluator in three accepted post-NextLife hardware arms.
- **KU-045 (resolved at bounded within-process recurrence):** EXP-20260813-047 fixes the M2.33 discriminator at three captured cycles after one warmup and fixture-proves its complete-cycle, ceiling, redaction, and output …
- **KU-046 (resolved at the deterministic planned-path/type boundary):** EXP-20260814-060 proves that schema 2 can copy the exact user-owned CD/CHARS3/FLICKD.ALL source over exact CD/CHARS/FLICK.ALL destination with both input …
- **KU-047 (resolved at exact authored-sequence composition boundary):** EXP-20260814-064 adds compose LEFT RIGHT --source-root ROOT for exactly two existing schema-1/schema-2 manifests.
- **KU-048 (accepted at the exact current-Linux removal boundary):** The ordinary sparse overlay contains recorded destination files plus fixed .ablpc/receipt.json, and the accepted receipt records schema, manifest name, exact …
- **KU-049 (rejected incomplete executable-authority alignment):** EXP-20260814-078 - Versioned exact M4 compatibility statement publishes one canonical asset-free v0.1 statement whose five hash entries are demonstrated evidenc …
- **KU-050 (bounded M4.25 report accepted; general dry-run remains unsupported):** EXP-20260814-084 - Deterministic single-manifest dry-run report adds one write-free report for an existing single manifest.
- **KU-051 (resolved at the strict current-receipt/component/closure boundary):** The ordinary receipt records schema, manifest name, destination path, input/output hashes, contiguous applied edit details, and replacement-source path/hash whe …
- **KU-052 (resolved: manifest-driven clean-derived-copy lifecycle):** Separate accepted evidence covers staged/sparse installation and validation, manual runtime launch of modified derived copies, and authenticated sparse- overlay …
- **KU-053 (resolved at the accepted installed lifecycle boundary):** A clean tracked source can build the asset-free ablpc-toolkit-v1.0.0 twice as byte-identical 378,880-byte canonical tar archives at SHA-256 1527281c60d1dd13a …
- **KU-054 (resolved at retained/displayed 51/50 boundary):** EXP-20260814-111 proves the 51-record table and isolated new pickup.
- **KU-055 (resolved for the data-only duplicate-letter boundary):** EXP-20260814-113 proves selectors 0x10–0x13 are the four-member Training FLIK mask set, that moved copies initialize, and that each duplicate can be consu …
- **KU-056 (resolved at the exact eight-slot FLIKFLIK boundary):** EXP-20260815-114 assigns original Training letter records 50–53 mask bits 1/2/4/8 and appended records 63–66 bits 16/32/64/128.
- **KU-057 (open — natural Level03 row-6 nearest-region selection):** EXP-20260815-116 confirms that exact PC Level03 row 6 is a type-1 signed XYZ record at file offset 0x4A4 and that 0x00432930 conditionally scans this tabl … (2026-10-02 audit: the history's own later entry resolves KU-057 as an M3.5 blocker, [[EXP-20260815-131 - Level03 collision geometry and M3.5 disposition]]; a controller-only row-6 contact, checkpoint semantics and other rows/levels stay unresolved and non-blocking.)
- **KU-058 (resolved at the live-coordinate display boundary):** EXP-20260815-128 - Live Flik position globals uses a controlled visible Training jump, ordinary ground movement, and independent static PC instructions to confi …
- **KU-059 (resolved by EXP-135):** EXP-20260815-133 - Independent M3 closure authorization hard-truth audit confirms that the cited EXP-111 through EXP-114 durable records disclose Training targe …
- **KU-060 (effectively resolved. EXP-138 accepted Tunnels row 3 and City gate 0; EXP-20260816-148 - Modified grain-gate thresholds …):** Modified grain-gate physical transition
- **KU-061 (open):** Runtime descriptor Z-bounds derivation (2026-10-12: settled offline. The original loader, emulated on the retail Level03 terrain, stores descriptor 570 `+0x1C` = 101632, the loader-literal value, not EXP-131's 98112. A live read would add a third form. [[EXP-20260816-141 - Engine-faithful terrain height and gate standoffs]].)
- **KU-062 (open):** Auxiliary query value at the instant of reset selection
- **KU-063 (open (one negative added by runtime capture 2026-08-18)):** Which levels use type 1 for reset placement (2026-10-18: creature scripts walk type-1 lists in Anthill (Dot), City Entrance (taxi bugs, lists 1–6), Clover Forest (mosquito), The Tree (acorns) and Canyon Showdown (Hopper). Council Chamber, Riverbed Flight, Anthill Pt 2 and Riverbed Canyon hold one that no creature walks; Tunnels' is the reset table. [[EXP-20261018-001 - Creature row index census]]. Bug Bar's level routine `0x00439E90` reads the table by index, the likely user of its lists 0–5, [[EXP-20261018-011 - Type-indexed list table writers and readers]].) (2026-10-12: a second negative. Level01's type-1 record at `0x005C5864` is Dot's 104-point flight path, not reset rows: [[FUNC-97C95BA5572D-004317D0]], EXP-20260913-002.)
- **KU-064 (answered statically 2026-10-18; runtime sample open):** Type-indexed pointer table state for a level with no such record (2026-10-18: zero. The only writer is the DAT walk, called only inside `0x004671D0` after its unconditional clear; the duplicate clear is uncalled, and every other absolute reference is a read. [[EXP-20261018-011 - Type-indexed list table writers and readers]].)
- **KU-065 (resolved for the identified node on 2026-08-17; the identity of the four original camera-packet failures remains o …):** Intermittent single-test failure in the canonical suite
- **KU-066 (open):** PC camera-source semantics and manual controls (2026-10-12: the selector bit's semantics now cover every scripted view, [[EXP-20261012-003 - Scripted camera flag census]]. Manual controls stay open. 2026-10-18: the manual controls are C ("camera", bit 0x400), which selects camera mode 2, and X ("lock camera", bit 0x800), which selects mode 3, in `0x0041ADF0`. What the modes look like is unread. [[EXP-20261018-006 - Controls configuration screen and action bits]].)
- **KU-067 (answered statically 2026-10-18; runtime trace open):** Meaning and consumers of the City gate-0 byte write (2026-10-18: `0x00599C69` is the second of four telescope hide flags at `0x00599C68`–`0x00599C6B`. Its only reader, the pickup walker `0x00417720`, parks the nth telescope out of sight when flag n is set; a level-start routine clears all four. [[EXP-20261018-012 - Telescope hide flags]].) (2026-10-12: a second writer. Level01's per-level update `0x004317D0` sets `0x00599C69` as second-telescope suppression when the berry type is 3, so the byte looks like per-level scratch rather than a City-only flag. That is static evidence plus a flag-level replay, not a live test: [[FUNC-97C95BA5572D-004317D0]].)
- **KU-068 (answered at two sampled slots, 2026-10-18; modes read statically, per-type handlers and opcode-11 subroutines read 2026-10-18):** Runtime behaviour of the creature script program counter (2026-10-18: answered for two slots from saved hardware samples. Dot's `+0x70` holds only decoded starts of script 7 and follows the decoded first activation; the moved taxi bug's sits in script 23 and, once dead, script 13, and its op-4 targets equal its list rows. [[EXP-20261018-002 - Creature script counter in saved runtime samples]]. The five modes were then read statically, [[EXP-20261018-003 - Creature VM movement modes]]; the per-type handlers and opcode-11 subroutines in [[EXP-20261018-004 - Creature type handlers and opcode-11 subroutines]]; event ids stay open under [[#Creature rows and the script VM]].)
- **KU-069 (answered for shipped data, 2026-10-18; the code stays unbounded):** Unbounded table indexes in the creature subsystem (2026-10-18: answered for shipped data. In all 534 retail rows type is 1–41 and script 0–39; every script that walks a list selects list 1–6, present in its level's DAT; `+0x0F` reaches 246 but selects a list only with flag bit 3, set only on seed rows, which never run a script. The reads stay unbounded in the code. [[EXP-20261018-001 - Creature row index census]].)
- **KU-070 (answered 2026-10-18, static and runtime; joystick mode open):** Meaning of the input action bits and the identity of the configuration screen (2026-10-18: the screen is the controls screen `0x00430DF0`, "define keys"/"define buttons", opened from Options_Scr `0x00441D20`, carousel position 0. Its items label every bit: forward 0x10, back 0x40, left 0x80, right 0x20, fire/get/drop 0x8000, jump/change 0x4000, seed color 0x1000, camera 0x400, lock camera 0x800, walk 0x200, kick 0x8200. Return 0x8 is the one key it cannot rebind. A read-only hardware arm then opened Options_Scr and "define keys" and read the live key table and item bytes, matching exactly: [[EXP-20261018-013 - Options screens and the creature gate live]]. The animation catalog's "turn in place" for 0x400 and the label "camera" were then shown to describe the same key: it selects camera mode 2 and makes Left/Right turn Flik in place. [[EXP-20261018-006 - Controls configuration screen and action bits]].) (narrowed: the controller's jump bit 0x4000 maps to left Shift, EXP-20260907-028/EXP-20260930-004; default bindings give 0x8200 to Z and joystick button 3, 0x0200 to Space and 0x8000 to Ctrl, and poll `00464E10` stores the word `00598B10` to `00861C98`, EXP-20261001-003, static. The configuration screen remains unknown.)
- **KU-071 (answered 2026-10-18; four only-zeroed fields stay unknown):** Event callback semantics and whether any event is registered outside the two static sites (2026-10-18: WINDOWS creates the window and pumps messages each frame; DIRECTX wraps the renderer, input and sound, with a no-op per-frame slot. Both registrations run in every saved log past the renderer chooser, and no other event name appears in 579 logs. [[EXP-20261018-005 - Event callbacks and registrations]].)
- **KU-072 (open):** Three unidentified creature-VM engine callees (2026-10-12: two are now identified. `0x0041A550` is the tracked speech query that must return 0 before an event voice plays ([[EXP-20260910-009 - Flik action pools and preview tail diagnosis]]), and `0x00464D40` computes the heading toward a target, masked to 4095 (EXP-20260914-016). Only `0x00403A10` remains unidentified. Later the same day [[FUNC-97C95BA5572D-00403A10]] identified
it statically. It shows a timed frame on atlas sprite `0x7D`: frame 8 on a
pickup, frame 7 on a creature event. A per-frame updater animates `0x7D` and
`0x7C` like a mouth and eyes, and KU-072 is closed at that boundary.)
- **KU-073 (RESOLVED for the selector (2026-08-18) — 0x0059D9A7 is the equipped berry-type selector, confirmed causally on the P …):** Which variable selects the thrown berry type on PC
- **KU-074 (open):** Live semantics of the level-select carousel position counter (narrowed 2026-10-01, static: the select's exit `004444C6` stores carousel index − 3 to `00599AF8`, EXP-20261001-003; whether it advances once per accepted press and is stable between presses is still unmeasured.)
- **KU-075 (open):** Exact log wording of a rejected software-renderer arm
- **KU-076 (resolved at the environmental boundary — the crash is classic-Wine-9.0-specific; the same executable and assets load …):** Cause of the CONVPSXTPAGE8 corrupt-pointer crash under classic Wine
- **KU-077 (partly resolved by source/binary evidence; residual tests open):** Guest-virtual memory access via the 86Box GDB stub (Gate 2)
- **KU-078 (open (engineering debt, not a research unknown)):** The 86Box Win95 install is a driven session, not a reproducible script
- **KU-079 (narrowed, R1 complete; fresh derived-build visible-ground example confirmed (EXP-20260904-005) — the linchpin for …):** The render-geometry command grammar (the LEVEL.DAT draw-command stream)
- **KU-080 (narrowed, 2026-09-04 — original PC instructions admit real Level01 triangles and separate X/Z barrier segments and produ …):** Does PC terrain collision block laterally, or is it height-only?
- **KU-081 (narrowed, 2026-09-04: direct-store destinations proven N..N+19, real Level01/Level03 templates and reserved ranges resol …):** Render-side mutation of the collision descriptor table (FUN_0044ca00) (2026-10-02 audit: read-only live censuses have since seen plant descriptors it registers: descriptor 193 in [[EXP-20260906-007 - Plant-state collision regression]]'s control game and descriptor 233 in [[EXP-20260909-004 - Restore native plant collision]].)
- **KU-082 (open (defect in a working copy, surfaced 2026-08-18 by the R0 mesh decode — EXP-20260818-006 - R0 the static mesh format …):** A project mod artifact has unrelocated object pointers (LEVEL07/LEVEL1.DAT) (2026-10-12: closed. The copy is EXP-20260814-111's rejected first staging. Only that DAT differs from retail among 720 files, and its log stops at a missing `level00\level.raw`, so the game never loaded it. The accepted output is a different file (`20d0f9b1…`). A `QUARANTINED.md` marker sits in the copy, which is not deleted.)

## Historical record

[[Known Unknowns history through 2026-09-26]] preserves the previous note. [[Session Index]] indexes the original session records. Historical permissions and process IDs do not carry forward.

## Historical heading links

These headings retain existing Obsidian links; their details are historical.

## 2026-08-22 KU-079 update - R2q quiet-census design frozen offline

See [[Known Unknowns history through 2026-09-26#2026-08-22 KU-079 update - R2q quiet-census design frozen offline]].

## 2026-08-25 KU-079 update - R2q runtime edge remains audit-pending

See [[Known Unknowns history through 2026-09-26#2026-08-25 KU-079 update - R2q runtime edge remains audit-pending]].

## KU-051 (resolved at the strict current-receipt/component/closure boundary)

See [[Known Unknowns history through 2026-09-26#M4 toolkit unknowns]].

## KU-052 (clean-derived-copy lifecycle is not jointly demonstrated)

See [[Known Unknowns history through 2026-09-26#M4 toolkit unknowns]].

## KU-057

See [[Known Unknowns history through 2026-09-26#Gameplay unknowns after EXP-20260815-114]].

## KU-060 - Modified grain-gate physical transition

See [[Known Unknowns history through 2026-09-26#KU-060 - Modified grain-gate physical transition]].

## KU-061 - Runtime descriptor Z-bounds derivation

See [[Known Unknowns history through 2026-09-26#KU-061 - Runtime descriptor Z-bounds derivation]].

## KU-065 - Intermittent single-test failure in the canonical suite

See [[Known Unknowns history through 2026-09-26#KU-065 - Intermittent single-test failure in the canonical suite]].

## KU-066 - PC camera-source semantics and manual controls

See [[Known Unknowns history through 2026-09-26#KU-066 - PC camera-source semantics and manual controls]].

## KU-067 - Meaning and consumers of the City gate-0 byte write

See [[Known Unknowns history through 2026-09-26#KU-067 - Meaning and consumers of the City gate-0 byte write]].

## KU-074 - Live semantics of the level-select carousel position counter

See [[Known Unknowns history through 2026-09-26#KU-074 - Live semantics of the level-select carousel position counter]].

## KU-079 - The render-geometry command grammar (the LEVEL.DAT draw-command stream)

See [[Known Unknowns history through 2026-09-26#KU-079 - The render-geometry command grammar (the LEVEL.DAT draw-command stream)]].

## KU-080 - Does PC terrain collision block laterally, or is it height-only?

See [[Known Unknowns history through 2026-09-26#KU-080 - Does PC terrain collision block laterally, or is it height-only?]].

## KU-081 - Render-side mutation of the collision descriptor table (FUN_0044ca00)

See [[Known Unknowns history through 2026-09-26#KU-081 - Render-side mutation of the collision descriptor table (FUN_0044ca00)]].
