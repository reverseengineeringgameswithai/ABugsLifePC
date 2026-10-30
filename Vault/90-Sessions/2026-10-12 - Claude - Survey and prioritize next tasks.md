---
type: session
date: 2026-10-12
agent: Claude
status: complete-bounded
updated: 2026-10-29
tags: [session, planning/backlog]
---

# Survey and prioritize next tasks

## Goal

The user asked for a deep dive into the project to find the next tasks, a
prioritized list, and a note recording it. [[Next Tasks]] holds the list. This
note records the method, the evidence checked and the sweep's findings.

## Method

- Read the startup set: START HERE, Current State, Project Roadmap,
  Environment Status, Decision Log, Known Unknowns, the Project Charter and the
  Agent Operating Manual. Then read the latest session notes and the git log
  since 2026-09-25.
- Ran three read-only sweeps in parallel, then spot-checked each sweep's key
  claims against the cited files:
  - feature and maintenance notes in `40-Implementation`, plus the research
    notes they cite;
  - code, tests, gates and tooling debt;
  - the research backlog: the coverage map, hypotheses, experiment statuses,
    open KU items and recorded contradictions.
- Ran the fast `make check` gates, plus `make session-audit`, `briefing`,
  `budget`, `run-orphans`, `ghidra-stats` and `criu-check`. Also ran the
  non-R2q pytest suite.

No game, Wine, Blender or service was launched, and nothing under `work/` or
`originals/` changed. The entry tree was clean at `8c13fc94`.

## Findings

### Gates

- `m4-compatibility` fails (exit 2). It expects the sentence "Active R2c uses
  fresh RC0 with no directional input before Return." (`compatibility.py:906-910`),
  which `d1d5e08d` reworded in [[Wine Linux Play Baseline]].
- The note is not hash-pinned, so a text-only fix on either side clears all
  12 tests.
- The pre-commit hook lacks this check.

### Briefing

`make briefing` exits non-zero. The Current State handoff (lines 11–443,
about 26 KB) is never cut and alone exceeds the 6,000-token budget, so every
open unknown is dropped.

### Register items answered by later work

- **KU-072:** two of its three callees are identified.
- **KU-067:** the telescope suppression write.
- **KU-063:** Level01's type-1 table is Dot's path.
- **Coverage map, Audio row:** `0x0042B020` is the projectile allocator, per
  EXP-20260909-008 ("allocator `0042B020`").

Each was checked against its cited note, not yet against the binary.

### Contradictions still open

- homing flag 0x0001;
- movement state 4;
- the seed `0x3200` floor offset;
- KU-061's z_min, 101632 versus 98112.

All four, plus the `0x0059A5EE` census, were settled statically later in this
session (see "Later the same session").

### Tooling

- **Evidence hygiene:**
  - `make run-orphans` exits 1: 14 run folders are uncited, and
    `RUN-WINE-20260819-003708` is cited but missing.
  - KU-082's artifact still exists, unexamined.
- **Ghidra and hooks:**
  - `ghidra-stats` warns that the imports table is empty and one function
    name is duplicated.
  - Hooks are installed via `core.hooksPath`.
- **Disk:**
  - `tmp/wine-smoke-2370022` holds 1.6 GB.
  - `make criu-check` is blocked, as expected (CAP-011).

## Changes made

- New [[Next Tasks]], linked from [[Project Roadmap]], [[Current State]] and
  [[START HERE]].
- Session index entry.
- At the user's request, the stale-note cleanup (section 2 of
  [[Next Tasks]]). Each correction is a dated parenthetical, per the
  2026-10-02 decision to correct with dated pointers rather than rewrites:
  - **KU-063, KU-067 and KU-072:** later answers added, each checked in its
    source; KU-072 now has one unidentified callee, not three.
  - **Coverage map:** the `LEVEL.RAW` row moves from Touched to Bounded
    (EXP-20260908-020, EXP-20260927-001). The Audio row records that
    `0x0042B020` is the projectile and effect allocator.
  - **Current State handoff:** the entries from 2026-09-28 to 2026-10-02 (19
    KB) moved verbatim to [[Current State Archive]]; **Pending** stays. `make
    briefing` now exits 0 and lists open questions again.
  - **Dangling run citation:** EXP-20260818-008 now records that
    `RUN-WINE-20260819-003708` was never stored.
  - **Not done:** the 14 uncited run folders and KU-082's artifact. Those
    need evidence work, not note edits.
- No new research claim; register statuses keep their wording, with dated
  additions.

## Tests run

- **Fast gates:**
  - `make python-doctor`: pass.
  - `make vault-lint`: 1,168 notes, 0 errors.
  - `make m4-compatibility`: fail, as recorded.
  - `make audit-tracked`: 0 violations.
- **Other make targets:**
  - `make session-audit`: clean.
  - `make budget`: 40,198 of 120,000 tokens.
- **Non-R2q suite:** `pytest -q --ignore-glob='tests/*r2q*' tests` on HEAD
  `8c13fc94`. It was still running at commit time (15% after about 10
  minutes by the process's elapsed time, on pace for the 65 minutes of the
  2026-10-03 run), with early failures in line with the recorded
  compatibility cluster. (Corrected the same day: the first wording said 35
  minutes, misread from the clock.) It was stopped when the R2 decision
  changed the default set; the two runs below replace it.
- **R2c–R2p alone:** 19 min 18 s. 2,011 passed and 150 failed with 13
  errors, all in R2p, from host-identity drift and the `anm.py` anchor (see
  "Later the same session").
- **Final `make check`,** with R2p and R2q opt-in: **5,639 passed, exit 0**,
  52 min 27 s, starting 18:18 under load. R2c–R2o took 16.4 min. The gates
  passed:
  python-doctor, vault-lint, m4-compatibility, audit-tracked and
  `git diff --check`.
- **During the run.** Vault edits continued while it ran. On the final tree,
  Vault lint, the briefing, the M4 gate and the vault, briefing, hygiene,
  compatibility and hook tests (186 passed) were rerun.
- **All three `make check` failures belong to the old R2 track.** R2 was the
  August runtime-test phase of the render-geometry work. Its lettered
  attempts include R2c (EXP-20260819-002), R2p (EXP-20260820-005) and R2q.
  The m4 wording gate cites R2c, the attribution anchors are R2p's, and the
  census cluster is R2q's. No current feature fails.
- **Vault and briefing tests:** `tests/test_vault_lint.py`,
  `test_briefing.py` and `test_repo_hygiene.py` (103 passed) after the
  edits.

## Later the same session

The user then made the three choices and asked for more.

- **R2 tests.**
  - R2q took about four hours per run, and the user did not want to return to
    it. Speeding it up would fail its own anchor, which hashes its test files.
  - The user approved making the R2 tests opt-in, changing the gate wording
    and extending the hook. Claude Code's auto-mode check had first blocked
    the edit as a test-gate bypass.
  - The user then accepted about 20 minutes for the rest, so only R2p and
    R2q are opt-in (`pytest.ini`).
  - R2c–R2p alone took 19 min 18 s under host load. All 163 failures were
    R2p's: 125 Wine-preloader device renumbering after a restart, 13 `git`,
    13 `pactl`, 7 the `anm.py` anchor and 5 others.
  - [[Decision Log]] 2026-10-12.
- **Stale notes.** Section 2 was done at the user's request (listed above).
- **REA.** The user asked whether github.com/morluto/rea would help, then
  approved a trial. [[EXP-20261012-001 - REA Ghidra analysis trial]] keeps it
  optional, not adopted.
- **Static research from [[Next Tasks]]:**
  - Per-level sprite tables:
    [[EXP-20261012-002 - Sprite table census]].
  - Scripted-camera flag:
    [[EXP-20261012-003 - Scripted camera flag census]].
  - Homing visibility bit:
    [[EXP-20261012-004 - Homing target visibility bit]].
  - Flik's ground pound:
    [[EXP-20261012-005 - Flik movement state 4 ground pound]].
  - Seed offset: [[FUNC-97C95BA5572D-0041C420]].
  - KU-061: EXP-20260816-141.
- **More offline work, at the user's request.**
  - **KU-072 closed:** [[FUNC-97C95BA5572D-00403A10]]. It shows a timed
    frame on atlas sprite `0x7D`; the updater `0x004037F0` animates `0x7C`
    and `0x7D` like eyes and a mouth (inferred).
  - **The drop analysis for creatures moved between levels**, added to
    [[EXP-20261012-002 - Sprite table census]].
    Table-collectible drops all have pickup cases, and a moved creature's
    scripts, contact and kill paths spawn only sprites below 50.
  - **Evidence clean-up.**
    - The 14 uncited runs are now cited where they belong:
      - EXP-20260813-040's range of 9 GDB calibration runs, listed one by one;
      - EXP-20260811-004's 3 setup probes;
      - 2 intermediate runs of EXP-20260812-006.
    - `make run-orphans` shows 0 uncited runs and the 1 dangling citation
      that cannot be fixed.
    - KU-082 is closed. The copy is EXP-20260814-111's rejected first
      staging; only its DAT differs from retail, and its log stops before
      Training loads. A `QUARANTINED.md` marker sits in the copy, which is
      not deleted.
  - **A self-correction.** I first tested collectible bit `0x04`. The
    routine tests `& 2`, and the recorded result uses `& 2`.
- **Creature identities, at the user's request.** [[EXP-20261012-006 - Creature types from the character loader]].
  - The loader `0x00445020` names all 41 types.
  - The census across 17 engines and 574 saved logs confirms 26 types at
    runtime.
  - The user's side question about TEST and PLANT12 is answered in the same
    note: TEST is unreferenced by the executable, while PLANT12 is a real
    plant whose level use is unknown.
- **TCRF claims checked offline**, at the user's request: [[EXP-20261012-007 - Unused disc content checked offline]].
  - `COPYOFLE.RAW`'s early graphics are all located.
  - TEST renders as a mermaid textured from character page 16.
  - PLANT12's petals use the gold-berry texture, and its bulb uses plant 7's
    texels.
  - New: the renderer `research/unused-content/render-model.py`. Its images
    are not committed.
- **Method lesson.** One method alone missed something twice. Ghidra and REA
  missed the `0x41a992` writer, and the byte-pattern scan missed engines 9
  and 18's sprite initializers. A census now pairs at least two methods.

## Unresolved questions

- **Static questions.** The `0x4000` actor-flag writer, the ring's damage,
  the hover length, and which native drops reach the walker default (a risk
  for creatures moved between levels).
- **Still needing evidence work.** The 14 uncited run folders and KU-082.

## Recommended next action

[[Next Tasks]] sections 4.2–4.4 and 6 remained; they need a runtime launch
and launch approval.
