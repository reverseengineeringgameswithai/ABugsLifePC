---
type: session
date: 2026-10-07
agent: Codex
status: complete-bounded
updated: 2026-10-07
tags: [session, re/tooling]
---

# Evaluate local Kev against known PC facts

## Goal

Assess the user's local Kev installation using facts already established in
ABLPC. [[EXP-20261007-001 - Local Kev evidence classification probe]] owns
the protocol, exact provenance, results and limits.

## Work and findings

- Read the startup set, charter, operating manual and research MOC; entry
  tree was clean at `06c27c3d8ca6dd14cf3c6208bdf780b89c61f0f6`.
- Located `/home/dev/AI/kev`, read the installation record, API and packed
  loader, and queried the already-running loopback server. No Kev files changed.
- Froze 36 claims and labels from six cited PC notes before inference.
  Added `research/kev-evaluation/{claims.json,evaluate.py}` and the bounded
  metadata packet `reports/kev/EXP-20261007-001/`.
- Primary 35/36, reordered 36/36 twice, no evidence 36/36 insufficient.
  The only mismatch was conservative centipede evidence status; its answer
  changed with option order. No false supported answers in this selected set.
- Recommend an advisory review pilot. No new PC findings or pipeline
  integration. Updated Current State, Known Unknowns, Decision Log, research
  and experiment MOCs, Session Index and the evidence-tooling note.

## Boundaries and unresolved questions

Hand-selected excerpts and labels, no independent holdout; calibration,
unseen raw evidence and retrieval quality remain unmeasured. The next
discriminator is a separately labelled set from other experiments with stale
and competing evidence. No cross-port repository was consulted.

## Validation and environment

The runner completed all 24 requests (144 decisions), checked probability
domains and answer completeness, and preserved requests/responses. Retail
and production EXE hashes were independently rechecked. No game was launched
or written. Session audit is clean. The pre-existing Kev server and browser
remain running; this session started no service.

`make check` passed Python dependency checks and Vault lint (0 errors), then
stopped at the already-recorded M4 compatibility wording gate: it requires
the historical exact sentence about Active R2c. No full regression tests ran.
See `reports/kev/EXP-20261007-001/make-check.txt` and
[[Known Unknowns#Current regression-gate failure]]. The initial lint warning
about START HERE's older date was addressed by adding the new tooling pointer.
Final Vault lint, Python compilation and `git diff --check` pass. An independent
packet check verified the frozen hash, runner/spec hashes, all six unchanged
source hashes, all 24 request/response pairs and exclusion of annotation
labels/rationales from model inputs. Existing Git hooks are already configured
at `scripts/git-hooks`.

## Banking for future sessions

After reviewing the findings, the user asked to bank them for future sessions.
Checkpoint the runner, frozen labels, raw requests/responses and Vault handoff
together. START HERE and Current State point to EXP-20261007-001; its
recommendation and Known Unknowns preserve the advisory scope and next
independent evaluation. No game change or broader Kev integration is queued.
