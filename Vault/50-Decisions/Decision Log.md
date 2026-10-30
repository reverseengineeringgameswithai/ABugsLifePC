---
type: register
status: active
updated: 2026-10-29
tags: [register/decisions]
---

# Decision Log

## 2026-10-18: saved samples count as runtime evidence when the code matches retail

The user asked for more static work. Two KU-068 answers came from samples
that earlier hardware arms had saved for other questions, under derived
executables
([[EXP-20261018-002 - Creature script counter in saved runtime samples]]).

- **Decision.** A saved sample from a derived build counts as runtime
  evidence for retail behaviour only after every code and data region the
  sampled path executes is compared byte for byte with retail. Any
  difference must be shown to lie off that path, as the six-byte seed-arm
  hook at `0x0041EDB4` was. The note states the comparison, and the claim
  stays bounded to the sampled slots.
- **Method rule from the same session.** A completeness claim, such as "no
  instruction writes X" or "every call of shape Y", needs a whole-image
  method:
  - a skip-data disassembly or raw byte scan of all of `.text`;
  - a search over every base register.

  A first linear capstone sweep stopped at `0x004269AB`. A register pattern
  that omitted `esi`/`edi`/`ebp` missed two writes. Both were caught and
  corrected before the claims were banked
  ([[EXP-20261018-007 - Frame wait rounding]],
  [[EXP-20261018-010 - Two inert data items]]).
- **External source.** Wine's headers and device defaults are registered as
  [[External Source Registry#SRC-WINE-SOURCE]]. They are environment facts
  only, quoted, from an unpinned master, and never game semantics.

## 2026-10-12: REA stays optional; a writer census needs a raw scan

The user asked whether REA (github.com/morluto/rea) would help, then approved
a trial. [[EXP-20261012-001 - REA Ghidra analysis trial]] ran its Ghidra path on the retail executable through the CLI
only.

- **Result.** It matched the existing export (10 of 10 references to
  `0x0059A5EE`, the same `0x00403A10` body) at 60–90 s a query.
- **Weaknesses.** Its caller lists do not follow thunks, and it shares
  Ghidra's blind spots.
- **Decision.** It is not registered as an MCP server or adopted as a core
  tool. The exact pin stays in `work/tools/rea-agents-6.4.0` for fresh
  re-analysis or a later interactive session.
- **Method rule.** The trial's raw scan found an 11th reference (`0x41a992`)
  in code Ghidra never made into a function. A census of a global's readers
  and writers now includes a raw scan of executable sections alongside Ghidra
  references.

## 2026-10-12: R2p and R2q tests become opt-in; the M4 gate quotes current wording

`make check` had failed since 2026-10-02 on three leftovers of the August R2
runtime-test track (R2c, R2p and R2q were its lettered attempts), not on any
current feature. The user said the R2q tests took about four hours per run and
did not want to return to them. They then approved making the R2 tests opt-in,
changing the gate wording and extending the hook. Claude Code's auto-mode
check had first blocked those edits as a test-gate bypass.

The user then said about 20 minutes for the other R2 tests is acceptable, so
the exclusion was narrowed to R2p and R2q:

- **Opt-in R2p and R2q.** `pytest.ini` ignores `tests/test_r2p*.py` and
  `tests/test_r2q*.py` by default. Nothing is deleted. Naming the files runs
  them, and their failures stand unchanged.
- **Measured on 2026-10-12, under host load.** R2c–R2p took 19 min 18 s.
  R2c–R2o passed, and six of those files account for about 17 min of it. All
  163 failures and errors were in R2p:
  - 125 because a restart renumbered the device of the pinned Wine preloader,
    though the file is byte-identical;
  - 13 on `/usr/bin/git` (`git-core` updated on 2026-10-11);
  - 13 on audio-server checks;
  - 7 on the frozen copy of `anm.py`;
  - 5 on other host-dependent checks.

  R2p therefore breaks on routine updates and restarts, whatever the
  project's work.
- **Why `pytest.ini`.** R2q froze `tests/conftest.py` (`f254e4f7`), and R2p's
  activation records pin the `Makefile`. `pytest.ini` is pinned by neither.
  CI calls pytest directly and follows the same setting.
- **Not chosen:**
  - **Speeding up R2q.** Its benchmark anchor hashes R2q's own test files, so
    any speed-up would fail as drift until R2q was re-anchored, which
    reopens the track.
  - **Re-pinning R2p's host identities.** That would rewrite frozen evidence.
- **M4 gate.** `compatibility.py` now requires the Wine baseline note's
  accurate "The historical R2c retail branch used fresh RC0…". The old
  "Active R2c uses…" sentence became false when R2c moved to the auto-hardware
  build on 2026-08-19. The file is listed in the release inventory, not
  hashed.
- **Pre-commit hook.** It now runs `check-m4-compatibility.py`, which takes
  under a second, and skips it where no checker exists, as in the hook's own
  test tree.

[[2026-10-12 - Claude - Survey and prioritize next tasks]],
[[Known Unknowns#Current regression-gate failure]], [[Next Tasks]].

## 2026-10-07: evaluate local Kev as an advisory evidence classifier

The user asked whether local Kev can help using established facts. Freeze
claims, source excerpts and labels before inference; include false claims,
unresolved questions, option permutations and an evidence-removal control.
Keep all requests local and retain the raw decisions. Do not revise the lone
ambiguous label after observing its score. The result supports a claim-review
pilot; it installs no automatic gate and promotes no PC claim. No training,
game experiment or production change is needed for this assessment.
[[EXP-20261007-001 - Local Kev evidence classification probe]].

## 2026-10-02: correct stale notes with dated pointers, not rewrites

The user asked for a deep dive to fix stale and incorrect vault notes.
Decisions:

- **Fix current-tense claims in place** (builds, sources, open previews,
  limits, counts, tool versions) after checking code, git, campaign keys or
  disassembly.
- **Keep dated records.** Experiments, dated sections and decisions get a short
  dated pointer to what superseded or corrected them, not a rewrite.
- **Record, do not resolve, contradictions** that need a new experiment, and
  raise no confidence or name during the audit itself.
- **Instruction files.** After the user delegated the follow-up decisions,
  `CLAUDE.md`/`AGENTS.md` were corrected to name the live-validated
  `game-memory` cycle, keeping both files identical and CAP-010 unchanged.
- **Names follow independent evidence.** `004129A0` became
  `candidate_fmv_playback` and `00467E60` `candidate_plant_constructor`;
  `00459620` stays unknown. Contradictions that a static rerun can settle
  are settled (flag 0x20); the rest stay recorded.

2026-10-02 - Claude - Vault staleness audit.

## 2026-10-01: Flik's animations are catalogued by action state, labels kept apart from data

The user asks to map all of Flik's animations and store them for later
reference. Decisions:

- Key the catalogue on the native action state `0x0059D998` and its table at
  `0x004C1CE8`, not on slot numbers alone: the game never picks a slot
  directly, and one state can blend two slots or a script subrange.
- Keep authored meanings in `config/animation/pc-flik-animations.json`, one
  row per state and slot with its own status and evidence. Generate
  `reports/animation/flik-animation-catalog.{json,md}` from the work copy with
  `scripts/flik-animation-catalog.py`, which re-derives the structure and
  rejects labels that contradict it. Commit metadata only, never pose data.
- Extend the read-only `.ANM` inspector to whole slot records rather than add
  a second parser.
- Name inferred gameplay meanings `candidate`, and record the movement-state-4
  "gliding" versus hover-dive-pound reading as a contradiction instead of
  choosing one.
- Leave visual previews to a later `.ALL` hierarchy packet; do not draw parts
  from guessed bones.

[[EXP-20261001-002 - Flik animation catalog]], [[PC Flik animation catalog]].

## 2026-09-27: map the other original levels with a separate complete importer

Keep the bounded Training importer and its tests unchanged; add
`original_levels.py` for every level and dispatch instead. Name creatures only
from earlier evidence and mark model-gallery names as "looks like" hints. Record
model tails as normal tables rather than drawing them, keep the one undispatched
row as a marker, and hide far-offset model parts instead of deleting them. Maps
stay private under `work/`; only metadata is published.
[[PC original level Blender maps]] and [[EXP-20260927-001 - Complete original level Blender maps]].

## 2026-09-26: reuse dormant scenery and preserve original collision assemblies

After a report of missing original rock, thornbush and offering-leaf
collision: reuse guarded dormant allocations and complete stored meshes; retain
unknown auxiliary bytes and native animation controls. Import spatially paired
models as one editor assembly with the original collision profile, using exactly
the same translation for both. Do not claim isolated contact samples establish
complete surface coverage. Preserve all memory/density limits.
[[PC Anthill scenery assemblies]] and EXP-20260926-002 own evidence.

## 2026-09-26: inventory geometry separately from import readiness

For the requested static Anthill review, count exact geometry and explicit
donor footprints, distinguish retained disabled records from enabled drawing
dispatch, and keep appearance labels as inferences. Decode the one negative
mesh only in a research view that retains its source and opaque auxiliary
extent/hash; do not extend production support by dropping unknown bytes.
Publish metadata and keep all decoded artwork under `work/`. New imports must
account for the current 1,648-byte DAT headroom (352 bytes after
EXP-20260926-002, entry above) and establish animation,
collision and functionality separately. [[PC Anthill remaining object inventory]]
and [[EXP-20260926-001 - Static Anthill remaining object inventory]] own evidence.

## 2026-09-26: keep active handoffs concise and preserve research history

The user's project review and cleanup request authorizes reviewing and
checkpointing the existing dirty work, reconciling stale notes and leaving Git
clean. Preserve dated evidence in verbatim archive bodies, retain the stable
handoff headings and legacy linked headings, and put current status in one
place. Archived commands, permissions and PID bindings are historical.
2026-09-26 - Codex - Project review and Vault cleanup owns validation.

A Git commit is a source/evidence checkpoint. Keep storage-cleanup EXEs local
and ignored. Preserve Obsidian configuration, templates, wikilinks and local UI
state.

The broad regression gate exposes an unchanged historical Y-only recovery test
failure. Preserve its source and assertion, record the isolated reproduction,
and report the passing 497-test focused gate separately. Do not hide the failure
with a skip or rewrite frozen recovery evidence during a documentation cleanup.
[[Known Unknowns#Current regression-gate failure]] owns the follow-up boundary.
(2026-10-02: the failure no longer reproduces; it passed on 2026-09-27 and in
an isolated 2026-10-02 rerun, with the test file unchanged.)

## Current decisions to carry forward

- R2q is not an active track: the user reported on 2026-09-27 that it was
  dropped for taking too long. The historical R2q decisions and their gate
  failures may be outdated, and R2q packets do not activate automatically.
  [[2026-09-27 - Claude - Map all original levels in Blender]].
- Preserve original PC authority, external read-only PS1 citations, and fresh
  authorization for every live-memory write. [[Agent Operating Manual]].
- Historical output deletion does not erase evidence: September 20 metadata
  receipts remain local; ordinary summed build sizes are not physical reclaim.
  2026-09-20 - Codex - Remove old generated game builds.

## Historical record

[[Decision Log history through 2026-09-26]] preserves the previous note. [[Session Index]] indexes the original session records. Historical permissions and process IDs do not carry forward.

## Historical heading links

These headings retain existing Obsidian links; their details are historical.

## DEC-170 - Do not adapt the nuisance mask from EXP-007 localizer arms

See [[Decision Log history through 2026-09-26#DEC-170 - Do not adapt the nuisance mask from EXP-007 localizer arms]].

## DEC-171 - Require a fresh D4 holdout for the control-trained mask

See [[Decision Log history through 2026-09-26#DEC-171 - Require a fresh D4 holdout for the control-trained mask]].

## DEC-180 - Preserve exact R2o task-census disagreement before verdict

See [[Decision Log history through 2026-09-26#DEC-180 - Preserve exact R2o task-census disagreement before verdict]].

## DEC-181 - End R2o retries and require passive task-lifecycle evidence

See [[Decision Log history through 2026-09-26#DEC-181 - End R2o retries and require passive task-lifecycle evidence]].

## DEC-187 - Bind P0A internal metadata errors to their producing phase

See [[Decision Log history through 2026-09-26#DEC-187 - Bind P0A internal metadata errors to their producing phase]].

## DEC-188 - Preserve P0A-AH-001 as pending after pre-collection route and close failures

See [[Decision Log history through 2026-09-26#DEC-188 - Preserve P0A-AH-001 as pending after pre-collection route and close failures]].

## DEC-189 - Retire the consumed P0A wrapper and correct offline runtime provenance

See [[Decision Log history through 2026-09-26#DEC-189 - Retire the consumed P0A wrapper and correct offline runtime provenance]].

## DEC-190 - Require exact integer domains and complete X peer credentials

See [[Decision Log history through 2026-09-26#DEC-190 - Require exact integer domains and complete X peer credentials]].

## DEC-191 - Share exact task partitions and reject numeric aliases

See [[Decision Log history through 2026-09-26#DEC-191 - Share exact task partitions and reject numeric aliases]].

## DEC-192 - Separate proved direct navigation from P0B passive collection

See [[Decision Log history through 2026-09-26#DEC-192 - Separate proved direct navigation from P0B passive collection]].

## DEC-193 - Preserve failed recovery and close only the residual environment

See [[Decision Log history through 2026-09-26#DEC-193 - Preserve failed recovery and close only the residual environment]].

## DEC-194 - Treat the post-title addition as reproduced but the audio role as inferential

See [[Decision Log history through 2026-09-26#DEC-194 - Treat the post-title addition as reproduced but the audio role as inferential]].

## DEC-195 - Freeze R2q as a two-control post-gameplay quiet-census barrier

See [[Decision Log history through 2026-09-26#DEC-195 - Freeze R2q as a two-control post-gameplay quiet-census barrier]].

## DEC-197 - Apply R2q semantics to successful prefixes and physical rename identity

See [[Decision Log history through 2026-09-26#DEC-197 - Apply R2q semantics to successful prefixes and physical rename identity]].

## DEC-198 - Use one conditional R2q dependency reducer and anchor publication stat time

See [[Decision Log history through 2026-09-26#DEC-198 - Use one conditional R2q dependency reducer and anchor publication stat time]].

## DEC-199 - Bind the executed process to the exact executable asset identity

See [[Decision Log history through 2026-09-26#DEC-199 - Bind the executed process to the exact executable asset identity]].

## DEC-200 - Make a self-bound completion file the final R2q acceptance boundary

See [[Decision Log history through 2026-09-26#DEC-200 - Make a self-bound completion file the final R2q acceptance boundary]].

## DEC-201 - Separate R2q envelope validity from durability and benchmark complete publication

See [[Decision Log history through 2026-09-26#DEC-201 - Separate R2q envelope validity from durability and benchmark complete publication]].

## DEC-202 - Bind R2q late outcomes and benchmark execution provenance

See [[Decision Log history through 2026-09-26#DEC-202 - Bind R2q late outcomes and benchmark execution provenance]].

## DEC-20260811-004 - Wine-first modding target

See [[Decision Log history through 2026-09-26#DEC-20260811-004 - Wine-first modding target]].

## DEC-20260812-006 - Natural-pause hardware watchpoints for Wine WoW64

See [[Decision Log history through 2026-09-26#DEC-20260812-006 - Natural-pause hardware watchpoints for Wine WoW64]].

## DEC-20260812-007 - Evidence-gated canonical roadmap

See [[Decision Log history through 2026-09-26#DEC-20260812-007 - Evidence-gated canonical roadmap]].

## DEC-20260812-009 - Hardware renderer evidence gate

See [[Decision Log history through 2026-09-26#DEC-20260812-009 - Hardware renderer evidence gate]].

## DEC-20260813-053 - Require an independent hard-truth ratchet for M2 disposition

See [[Decision Log history through 2026-09-26#DEC-20260813-053 - Require an independent hard-truth ratchet for M2 disposition]].

## DEC-20260813-054 - Accept the M2.41 disposition and defer M2 without closure

See [[Decision Log history through 2026-09-26#DEC-20260813-054 - Accept the M2.41 disposition and defer M2 without closure]].

## DEC-20260814-109 - Complete M3.2 at the 51-of-50 bonus boundary

See [[Decision Log history through 2026-09-26#DEC-20260814-109 - Complete M3.2 at the 51-of-50 bonus boundary]].

## DEC-20260814-110 - Complete M3.3 with explicit duplicate-letter retrigger behavior

See [[Decision Log history through 2026-09-26#DEC-20260814-110 - Complete M3.3 with explicit duplicate-letter retrigger behavior]].

## DEC-20260815-111 - Complete exact eight-slot FLIKFLIK behavior

See [[Decision Log history through 2026-09-26#DEC-20260815-111 - Complete exact eight-slot FLIKFLIK behavior]].

## DEC-20260815-114 - Keep the pinned launcher immutable and add companion input controls

See [[Decision Log history through 2026-09-26#DEC-20260815-114 - Keep the pinned launcher immutable and add companion input controls]].

## DEC-20260815-115 - Default companion routes to a shared PC log milestone

See [[Decision Log history through 2026-09-26#DEC-20260815-115 - Default companion routes to a shared PC log milestone]].

## DEC-20260815-120 - Bind the overlay to runtime-discriminated live position

See [[Decision Log history through 2026-09-26#DEC-20260815-120 - Bind the overlay to runtime-discriminated live position]].

## DEC-20260816-132 - Retain manual hardware selection until the paired candidate passes runtime

See [[Decision Log history through 2026-09-26#DEC-20260816-132 - Retain manual hardware selection until the paired candidate passes runtime]].

## DEC-20260817-140 - Gate memory writes on authorization, a compare-before-write guard, and a receipt

See [[Decision Log history through 2026-09-26#DEC-20260817-140 - Gate memory writes on authorization, a compare-before-write guard, and a receipt]].

## DEC-20260817-145 - Deterministic replay via libTAS + single-threaded PCem, not rr

See [[Decision Log history through 2026-09-26#DEC-20260817-145 - Deterministic replay via libTAS + single-threaded PCem, not rr]].

## DEC-20260817-146 - Guest memory read write watch is a hard prerequisite, tested before the determinism build

See [[Decision Log history through 2026-09-26]].

## DEC-20260817-147 - Build a GDBSTUB-enabled 86Box to prove Gate 2 memory access

See [[Decision Log history through 2026-09-26#DEC-20260817-147 - Build a GDBSTUB-enabled 86Box to prove Gate 2 memory access]].

## DEC-20260818-149 - Build the runtime flight recorder as emulator-side C instrumentation, not gdb watchpoints

See [[Decision Log history through 2026-09-26]].

## DEC-20260819-159 - Stabilize and receipt the R2c runtime identity

See [[Decision Log history through 2026-09-26#DEC-20260819-159 - Stabilize and receipt the R2c runtime identity]].

## DEC-203 - Cross-bind R2q owned deadline attempts to production failure semantics

See [[Decision Log history through 2026-09-26#DEC-203 - Cross-bind R2q owned deadline attempts to production failure semantics]].

## DEC-208 - Recover P0E residue only through a predecessor-durable additive envelope

See [[Decision Log history through 2026-09-26#DEC-208 - Recover P0E residue only through a predecessor-durable additive envelope]].

## DEC-211 - Freeze the James-accepted Y-only restoration source and activation

See [[Decision Log history through 2026-09-26#DEC-211 - Freeze the James-accepted Y-only restoration source and activation]].

## DEC-212 - Preserve failed Y-only v1 and freeze a distinct mapping recovery

See [[Decision Log history through 2026-09-26#DEC-212 - Preserve failed Y-only v1 and freeze a distinct mapping recovery]].

## DEC-213 - Preserve consumed YR2 and freeze provenance-free recovery2

See [[Decision Log history through 2026-09-26#DEC-213 - Preserve consumed YR2 and freeze provenance-free recovery2]].

## DEC-214 - Preserve consumed YR3 failed evidence and require a distinct recovery3

See [[Decision Log history through 2026-09-26#DEC-214 - Preserve consumed YR3 failed evidence and require a distinct recovery3]].

## DEC-215 - Freeze recovery3 source and activation before one Y-only action

See [[Decision Log history through 2026-09-26#DEC-215 - Freeze recovery3 source and activation before one Y-only action]].

## DEC-225 - Preserve R2q-029 through R2q-031 and bank accepted R2q-032 activation without finalizing it

See [[Decision Log history through 2026-09-26#DEC-225 - Preserve R2q-029 through R2q-031 and bank accepted R2q-032 activation without finalizing it]].
