---
type: session
date: 2026-09-05
agent: Codex
status: recorded
evidence:
  - EXP-20260905-003
---

# Shared floor return and stitched patch

## User-directed terrain-only validation, 2026-09-05

The user clarified that these terrain tests must not rerun R2q. The once-started
full `make check` trial was cancelled with SIGINT after 360.849 seconds wall time;
pytest reported 885 passed and the one known pre-existing R2q historical SHA
mismatch in 359.80 seconds before interruption. All test processes exited.
There is no completed full-repository verdict and no serial/full-suite retry.
The exact terrain gate passed 72/72 in 27.66 seconds; the 27 added regressions
passed in 6.44 seconds. This session uses those terrain-only gates, not a claim
that the repository suite passed. See `reports/terrain/EXP-20260905-003-validation.json`
and [[EXP-20260905-003 - Shared floor return discriminator and stitched patch]].


Continued from 68ce28a048e07a817b47154ac3bd7ddbcfede621, subject
`terrain: bank diagonal and movement validation`, initially clean worktree.
Required startup notes, terrain MOCs, authoring roadmap and cited EXP-005/006
sources read; `make briefing` used only for orientation. Run/index checked before
assigning EXP-20260905-003. Historical run-index diagnostics remain 14 uncited
runs and one dangling RUN-WINE-20260819-003708 citation, not repaired here.

## Work and outcome

[[EXP-20260905-003 - Shared floor return discriminator and stitched patch]]
records the 68-cell boundary census, complete nearby render-stream/duplicate
census, original-instruction return failure and four-way controls. A full incident
six-cell star, with paired LEVEL.DAT vertex heights and unknown-byte preservation,
passes all 16 isolated modeled directions. Three complete-scene routes are
prop-confounded identically in retail and stitched (13/16 each). Rigid remains
an unchanged failure fixture.

Three fresh runtime arms verified resident assets. Retail passed one out/back
cycle; rigid reproduced the fall on return; stitched passed two cycles and a
normal jump/landing. A separate source100 extension stalled by a visible rock,
then returned safely. Do not count that extension as a seam pass. No live writes,
teleport, debugger, STOP/CONT or save-state operation; no PS1 consultation.

## Environment and preservation

The original files remain untouched, including existing 0644 ISO modes; the user
approved treating them as read-only without chmod. All assets and experimental
copies remain under work/. The protected stash is
76db1c9ee1ffffce52cea6aee591c24ab6a1c39a and was not applied or modified.
The previous diagonal/movement archive and manifest remain separate protected
checkpoint evidence.

Initial sandbox audits were visibility-limited: the first unrestricted post-close
audit found older USER-20260904-deck-depth-play-001 game46701/group46458 plus its
mute sink. The user explicitly authorized closing it. Exact-identity cleanup was
followed by a clean unrestricted audit. Retail used a correctly peer-bound separate
compositor while that old game existed; rigid/stitched pre/post audits were clean.
Final runtime cleanup leaves no live game, helper or mute sink.

## Validation and banking

New focused regressions: 27 passed in 6.44s. Exact legacy terrain gate before
runtime: 72 passed in 27.50s. Final gate, full-suite measured two-worker trial,
protected-path/claim/tracked-file/diff audits and any failures are authoritative
in `reports/terrain/EXP-20260905-003-validation.json`. Full-suite scratch stays
under work/tmp; the known R2q historical protocol SHA mismatch remains pre-existing
and out of scope. No private game data or captures are staged for Git.

Decision DEC-241: retain the rigid failing control and admit only a bounded
connected-floor repair; general mesh authoring, prop-aware seam routes and broader
pose/velocity coverage remain open. The banked box/diagonal experiments are not
redone or generalized.

Updated Current State, Environment Status, Known Unknowns, Decision Log, Project
Roadmap, terrain authoring roadmap, relevant MOCs, EXP-005/006 follow-ups and
Session Index. See [[Experiments MOC]] and [[Implementation MOC]].
