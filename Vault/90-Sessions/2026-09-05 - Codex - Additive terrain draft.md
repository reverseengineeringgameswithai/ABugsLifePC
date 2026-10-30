---
type: session
date: 2026-09-05
agent: Codex
status: completed
tags: [session, terrain/authoring]
---

# 2026-09-05 - Codex - Additive terrain draft

Continued the user's request to preserve original Level01 terrain/collision while adding the working play area. Experiment: [[EXP-20260905-009 - Additive terrain preservation and access ramp]]. Evidence: `reports/terrain/EXP-20260905-009-progress.json`.

Added a bounded additive writer, fresh-copy builder, offline native proof driver, and synthetic/private-fixture regressions. First focused run: 37 passed, 2 failed in 0.36 seconds. Failures concerned the new tests expecting TypeError rather than the writer's ValueError for mutable inputs. Approval was pending at this historical snapshot; the user approved the exception and landing corrections in [[2026-09-06 - Codex - Additive terrain validation]], which now carries the current results. The redundant overridden hash remains a nonfunctional cleanup item.

The passing private-fixture checks preserve all original source-99 cells and all other original collision payloads, original mesh-160 vertex/command bytes, and all other supported static references. This is in-memory writer evidence only. No assets staged, no native probe or runtime comparison yet. The old render batch's depth bias deliberately changes from 8 to 0 in the combined-mesh candidate.

No R2q or complete make check, no Git or stash operations, no original-file writes, and no live-game actions. Existing OG session left untouched. The next steps recorded at this snapshot were approved draft corrections, affected tests, terrain-only gate, isolated build and native comparison; see the 2026-09-06 continuation for their results and remaining gates.
