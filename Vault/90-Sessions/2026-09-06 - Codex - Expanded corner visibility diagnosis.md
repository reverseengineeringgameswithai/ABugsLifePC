---
type: session
date: 2026-09-06
agent: Codex
status: diagnosed-fix-not-installed
tags: [session, terrain/handoff, re/rendering]
---

# 2026-09-06 - Codex - Expanded corner visibility diagnosis

Started clean at `90c8a44`. User reports terrain disappearing at one corner while collision remains. [[EXP-20260906-011 - Expanded corner visibility regression]] reproduces visible/hidden/visible with guarded normal Up4.020s / Down1.541s and read-only state/camera/scene captures. All keys released; no writes or asset/source/test changes.

Original-PC replay rejects hidden views at `0x0044D677`. Expansion's foliage mesh appender used a geometric-only bound10087 instead of the established camera-aware14183. Radius-only emulated comparison admits142/142 observed cameras; control rejects121. Resident gate equals retail instructions and entire loaded mesh/collision/retained plant data still match. No live branch/GPU trace, all-camera proof or installed fix is claimed. Public report/notes are banked; private helpers/captures/receipts stay ignored.

Same game350624/start2935292, leader/group350348/start2935133, display`:2`, window14680071, sink `ablpc_mute_350348` remains OPEN. Stage `work/copies/EXP-20260906-010/expanded-game-02`; prefix/controller `work/experiments/EXP-20260906-010/expanded-preview-02`. All14 owned identities match prior binding; generic audit7 processes/one sink is accounted, not clean. Last pose `(239669,-102400,720628)`, flags257, velocity0, terrain visible; later user play can change pose. No input worker remains, no input after return capture. No launch/close, debugger, stop, teleport/save state, PS1 source or originals action.

Validation: native replay passes finite radius-only discriminator in0.182s. Terrain-selected `make check` passes780 tests in38.06s with two workers, repo-local scratch and R2q excluded. Vault lint708 notes/0 errors/8 existing maintenance warnings; imports, M4 compatibility, tracked-file and whitespace gates pass. Corrected bound claim sweep is new_only (old0/new1); hooks already installed. These existing tests do not cover the newly diagnosed native camera failure. No full-suite or unrelated R2p work. Protected stash `76db1c9ee1ffffce52cea6aee591c24ab6a1c39a` remains intact.

Next, if requested: fix foliage growth bound, add synthetic/captured-camera regression gates, prepare separate file-loaded candidate. Do not treat proposed14183 as a live repair already applied or silently overwrite the running preview's files.
