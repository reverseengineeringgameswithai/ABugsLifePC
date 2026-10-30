---
type: session
date: 2026-08-12
agent: Codex
status: completed
tags:
  - session
  - re/dynamic
  - re/resources
---

# Fixed trajectory plant route retirement

## Agent

Codex

## Goal

Execute roadmap packet M2.19 under the START HERE workflow, determine whether
the accepted plant-04-to-10 pair replacement has a stable rendered outcome
along one fixed Training trajectory, respect the Obsidian evidence policy, and
leave Wine and Git state clean.

## Files inspected

- The full required START HERE sequence, Project Charter, Agent Operating
  Manual, relevant MOCs, M2 roadmap contract, decisions, known unknowns,
  capability-gap register, Wine baseline, and preceding plant experiments.
- The retained PC content census, accepted Training logs, exact derived PC
  files under `work/copies/`, and `scripts/play-pristine.sh`.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments inspected

- [[EXP-20260812-015 - Plant pair caller and consumer trace]]
- [[EXP-20260812-016 - Plant request origin and separate DAT table]]
- [[EXP-20260812-018 - Same-layout PC ANM replacement]]
- [[EXP-20260812-019 - Same-size paired plant replacement]]
- [[EXP-20260812-032 - Fixed trajectory paired plant replacement]]

## Changes made

- Built fresh ignored control/replacement/control trees from the verified
  derived PC tree. The replacement changed only
  `CD/PLANTS/PLANT04.ANM/.ALL`, with exact plant 10 source bytes.
- Launched every accepted arm through
  `scripts/play-pristine.sh --research --windowed --mute`, steered only the
  exact isolated game window, and required the 640x480x16 Direct3D markers,
  no `INITSOFTRENDER`, all plant load lines, `End InitMainGame`, and `NextLife`.
- Sent the same receipt-bearing trajectory: three start samples, three seconds
  Up, two seconds Right, and three seconds Up, with fixed waits and three
  game-surface samples at each anchor.
- Captured only the isolated 640x480 Gamescope game surface. No desktop or
  whole-screen screenshot was taken. All PNGs/masks remain ignored under
  `work/copies/EXP-20260812-032/evidence/`.
- Compared same-index frames, temporal medians, all-pair phase proximity, and
  stable intersections across three replacement samples per anchor. Curated
  only text receipts, hashes, metrics, and accepted game logs.
- Rejected one bad-path preflight before renderer selection. Separately
  rejected one replacement and one unchanged attempt that both stalled at the
  same 954-line pre-resource loading boundary; neither contributes pair
  evidence.
- Restored Wine drive `R:` to
  `/home/dev/ABLPC/work/copies/BUGS_PC-full-disc`, stopped the exact scoped
  process trees, killed the scoped prefix server, and unloaded the private
  mute sink.
- Updated the roadmap, Current State, PC census note, KU-025/KU-032, decision
  log, capability gaps, implementation/research/experiment MOCs, and this
  session index. M2.20 now selects a one-path equal-size character-family
  discriminator from PC-only census evidence.

## Conclusions

- **Confirmed:** All three accepted arms are hardware Direct3D, reach
  `NextLife`, and emit byte-identical logs after only clock-line removal.
- **Confirmed:** The two fresh controls are byte-identical at 11 of 12
  same-index trajectory samples.
- **Confirmed:** No stable replacement-local rendered region is discriminated
  against either control. M2.19 closes as a bounded negative and retires the
  plant-04/10 direct visible route.
- **Unknown:** Later/off-camera plant behavior, complete `.ANM/.ALL` semantics,
  and the M1 placement-to-resource identity remain unresolved.
- **Decision:** M2.20 tests only
  `CHARS/FLICK.ALL <- CHARS3/FLICKD.ALL`. The companion `.ANM` files are
  byte-identical and the `.ALL` files are equal-size, making it a clean
  one-path PC-native discriminator without assigning identity from filenames.

## Contradictions and negative results

The replacement and unchanged arms each produced one pre-resource Training
loading stall before succeeding after a clean prefix restart. This matched
failure is not replacement evidence. M2.19's absence of a stable local region
does not prove that the plant files are unused or generally interchangeable.

## Tests run

- Metadata JSON validation: passed.
- `git diff --check`: passed.
- Final `make check`: Python smoke imports, Vault lint (137 notes, zero errors
  or warnings), 130 tests, and tracked-file audit (zero violations) passed.
- Final runtime audit: no scoped experiment process, Gamescope wrapper, or
  private sink remained; `R:` resolved to the pristine derived tree.

## Recommended next action

Execute [[Project Roadmap#M2.20 — Training character-family discriminator]].
Use fresh one-path staging, windowed muted hardware runs, the existing bounded
trajectory, and only isolated game-surface captures. Stop after the exact
discriminator and do not parse/edit unknown `.ALL` fields in advance.

## Git commit if applicable

Bounded commit message: `research: retire plant visible route`.
