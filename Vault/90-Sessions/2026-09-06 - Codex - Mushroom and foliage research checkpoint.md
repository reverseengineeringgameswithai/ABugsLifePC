---
type: session
date: 2026-09-06
agent: Codex
status: checkpoint
tags: [session, terrain/handoff]
---

# 2026-09-06 - Codex - Mushroom and foliage research checkpoint

The user requests committing all existing work and verifying a clean worktree before continuing foliage investigation. This checkpoint contains the PC-confirmed type5/source8 mushroom repair, its guarded writer/original-instruction probe/tests, live evidence summaries, and the initial foliage overlap/geometry diagnosis. Commit subject: `terrain: bank mushroom repair and foliage overlap evidence`. Parent: `e5db2ff6f197be6adc05d345e24d70a0a00766fc`.

## Validation

`make install-hooks` confirms the hooks are already installed. Before committing, ran `make check` with two workers, loadfile scheduling, repo-local scratch and `tests/test_r2q*.py` excluded under the terrain-session agreement. Result: **3990 passed, one failed in442.79s**. Failure: `tests/test_r2p_p0e_y_restore.py::test_action_journal_name_substitution_across_exchange_is_detected` at923 (`y:` resolves to `retail` rather than `stage`). This is the same failure recorded at the parent bank; its test and both imported R2p implementation files are unchanged. It is not repaired or reclassified as a terrain failure. Full `make check` is therefore not green; R2q was not collected.

JUnit: `work/experiments/EXP-20260906-007/bank-check.xml`. Python imports and M4 compatibility checks pass. Vault lint0 errors/8 existing maintenance warnings; tracked-file audit0 violations; staged/unstaged whitespace checks clean. Earlier focused plant40 and terrain72 passes remain valid. Claim sweeps remove the obsolete mushroom-type and spacing-first wording and correct an extra leading zero in the historical parent hash. Run-index audit retains the existing14 uncited directories/one missing cited directory; no new RUN citation is introduced.

## Preservation

Only source, tests, metadata reports and Vault notes are included. Originals, copied game assets, executables, raw RAM, private screenshots and Wine prefixes are excluded. The private geometry probe and captures remain under `work/`; hashes/provenance are banked. Protected stash remains `76db1c9ee1ffffce52cea6aee591c24ab6a1c39a`.

The session audit still matches the deliberate repaired-variety preview: game231286/start2242744, group231047, seven generic processes and sink `ablpc_mute_231047`, separately accounted by the prior handoff. This is not a clean runtime audit; the game is intentionally left open. No input, focus, capture, live-memory action, launch or close was performed for banking.

## Continuation gate

Verify the new commit and empty `git status --porcelain` before new research. Then continue [[EXP-20260906-006 - Perimeter barriers and original foliage reference]]: triangular cut-ins, not primarily gaps. The116 geometric crossing pairs are a candidate contributor, not exact screenshot attribution or proof of a GPU defect. Preserve the repaired collision and existing preview while discriminating geometry versus native drawing/depth behavior. See 2026-09-06 - Codex - Foliage overlap review and [[PC seed and mushroom collision state]].
