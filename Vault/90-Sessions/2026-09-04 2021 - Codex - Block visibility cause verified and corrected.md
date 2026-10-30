---
type: session
date: 2026-09-04
agent: Codex
status: complete-user-game-open
---

# 2026-09-04 2021 - Codex - Block visibility cause verified and corrected

**Later same-session follow-up:** the user moves from this handoff and reports
residual side-view bleed. [[2026-09-04 2034 - Codex - Paused side-view visibility diagnosis]]
preserves that paused state and supersedes the spawn/next-step status below.
This session's offset removal/restoration is a bounded partial correction.

The user asked to resolve the block visibility cause before it affected future
level layouts. Reused EXP-007's one-byte candidate and existing direct runtime
operator, preserving earlier collision/mesh work and the R2q bank.

[[EXP-20260904-008 - Block depth offset runtime comparison]] supplies a causal
result: removing inherited type0x41 object byte+0x12=8 hides the demonstrated
lower-leg/shadow leak; restoring8 reproduces it. All16 stationary captures match
measured player position/contact and camera. The field also adjusts a distance
threshold; this does not recommend zeroing native objects globally.

The original-position zero-offset arm retains normal top landing and departure
to the lower deck. For the stationary comparison, a common box was moved with
its collision between the unchanged initial camera and player. Compared byte8,
split-face0, unsplit0 and restored8. Smaller faces also hide the leak but alter
textured pixels; the one-byte/six-face correction suffices for this bounded case.
General face-size/material/layout rules and EXP-005's return-fall remain open.

Added `scripts/terrain-deck-visual-probe.py`, a fixed experiment builder with
explicit offset and optional subdivision.197 focused tests pass in37.05s,
including9 new cases for invalid settings, exact byte change, unchanged physics,
known mesh span, coverage and winding. Full make check and independent review
were not run; no commit. Lightweight gates and claim sweep are retained.

Five scientific arms closed with clean audits. An additional attempt entered
Training17 because confirmation preceded carousel settling; it was excluded
before science and closed cleanly. Its successor checked the visible menu and
waited for selection settling. No live writes, debugger, freeze, save states,
teleport, PS1 comparison or unrelated mapping changes.

The prior user game40214/965017 is closed. **Leave open:**
`USER-20260904-deck-depth-play-001`, game46701/1147812, group46458, display`:2`,
sink`ablpc_mute_46458`/module536870916. The original box is ahead of Flik at the
initial deck position. It has only the verified object offset correction;
TERRAIN.ALL and visible geometry are the same as EXP-006. Loaded prefixes,
object bytes/pointer and all audit identities are in its handoff receipt.
Only menu input and no-input sampling occurred in this final user session.

Report330,451 bytes, SHA-256
`d7d898818422d210e5d0e189d722efc4fa433497ddfe573a407e7a8519a2663e`.
Interactive unchanged game captures:
`work/experiments/EXP-20260904-008/comparison.html`.
Images, binaries, assets and prefixes stay under work. EXP-006/007 JSON reports
and the original EXP-006 builder remain unchanged.

Updated Current State, Environment, roadmap, DEC-233, KU-079/080, mesh/authoring
notes, prior session closures, MOCs and Session Index. Next: preserve the new
offset/occlusion regression and resume the separate shared-floor boundary work.
