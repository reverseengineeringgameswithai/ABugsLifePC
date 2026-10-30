---
type: implementation
status: active
created: 2026-08-17
updated: 2026-10-07
tags:
  - implementation/tooling
  - re/workflow
  - system/hygiene
---

# Agent evidence and query tooling

The offline half of the 2026-08-17 automation uplift: tools that make the
repository's existing evidence reachable, keep the mandated reading set inside
a working session, and stop defects that the audit loop was catching by hand.

[[Session control plane]] covers the live-session half.

## Optional local claim review

[[EXP-20261007-001 - Local Kev evidence classification probe]] evaluates the
existing `~/AI/kev` decision service using cited PC notes: 35/36 primary
labels matched, with one conservative, order-sensitive answer. The runner
`research/kev-evaluation/evaluate.py` freezes sources and labels, then saves
exact local requests and responses. It is an exploratory review aid; no
claim promotion or required gate is automated. Keep hash/count/offset checks
and literal claim sweeps deterministic. Unseen evidence and retrieval quality
need a separate evaluation before broader use.

## Context economy

The startup sequence in [[START HERE]] mandates seven documents. Measured on
2026-08-17 before any change: **1,091,966 bytes / ~272,994 estimated tokens**
(bytes/4). That exceeds a 200K-token context window outright, so no agent
could comply with the mandate as written, and the fresh-context audit loop
paid the cost once per round.

- `scripts/briefing.py brief` generates a bounded briefing from the
  authoritative notes: **4,615 estimated tokens, 1.7% of the mandated set**,
  with nothing truncated at the 6,000-token default. Sections: mission,
  hard runtime rules, current position, environment facts, open Known
  Unknowns, recent decisions, recent sessions, pointers.
  The hard runtime rules — the six Direct3D markers, `originals/`, `work/`,
  and the lifecycle requirement — are **non-elidable**: they are reproduced
  verbatim and are never truncated to meet the budget. Any section that cannot
  be parsed is emitted as `UNPARSED: <file> — read it directly` rather than
  guessed at. The briefing is generated and explicitly **not authoritative**;
  it is a map into the notes, not a replacement for them.
- `scripts/briefing.py measure` reports the mandated set's size, so the budget
  is a metric rather than an impression.
- `scripts/vault-lint.py --budget-only` emits the same measurement as JSON and
  warns per note (40K tokens) and per session (120K tokens).
- [[Current State]]'s dated packet chronology was moved verbatim into
  [[Current State Archive]] on 2026-08-17, which is what
  [[Agent Operating Manual]] already required ("chronology belongs in session
  notes"). Nothing was rewritten or dropped: 241 KB → 131 KB with the removed
  text preserved in the archive.

## Static-export querying

`static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json` is 7.7 MB on one
line. Reading it costs an entire context, so it went effectively unread, and
[[Current State]] records at least four audit rounds lost to work that the
file already contained.

`scripts/ghidra-query.py` gives it verbs: `index`, `function`, `callers`,
`callees`, `xrefs`, `grep`, `strings`, `stats`. A `function --addr` query
takes **0.07 s**; the sidecar index is **411 KB** and one record per line, so
it is greppable and small enough to read whole. Every output path is bounded
and flags its own truncation.

Its structural findings about the export are recorded separately in
[[Ghidra export structure and caveats]] — they change how the file must be
read and were not previously written down.

## Evidence pipeline

- `scripts/run-index.py` cross-references the 107 `dynamic/wine/RUN-*`
  directories against every Vault mention. First run found **14 orphaned runs**
  (evidence cited by no note — including nine consecutive
  `RUN-GDB-20260813-1129xx…1135xx` captures, about 1.2 MB) and **0 dangling
  citations** (every cited run id exists). The two are distinct integrity
  problems and are reported separately.
- `scripts/experiment-draft.py` generates a pre-filled experiment note from
  run receipts: frontmatter hashes, environment, working directory, addresses,
  and artifact tables come from `metadata.json`/`result.json` instead of being
  retyped. It **never asserts an interpretation or a result**, marks every
  unwritten section with `TODO:`, carries a provenance line, and its output
  passes `scripts/vault-lint.py`.

  This targets a measured failure mode, not a theoretical one: hand
  transcription produced a wrong-rounding coordinate table (rejected in
  EXP-20260816-145) and a duration typed from memory as "7 seconds" that the
  retained trace showed was 2.47 s (rejected in EXP-20260816-157).

## Claim propagation

The audit loop's dominant failure was never the model. The creature census was
rejected eight times and the event census six, and the postmortems record the
same defect repeatedly: "four round-1 fixes had landed **only at the first
occurrence** of the wording", then "the same partial-propagation failure a
third time" ([[Current State Archive]]).

`scripts/claim-sweep.py` makes that mechanical:

- `sweep --phrase` — every occurrence with path, line, and context.
- `pair --old --new` — the actual check: a tree carrying **both** wordings is
  tool-negative, which is exactly the mixed state those rounds shipped.
- `numbers --pattern` — groups locations by captured value, so a count
  corrected in one note and not another shows up as two groups.

Run `pair` after every correction, before handing a packet to an audit.

## Automated gates

The repository had **zero CI and zero git hooks**; `make check` ran only when
someone remembered. KU-065's first four failures were lost precisely because
pytest output was piped through `grep`, discarding the `FAILED` line.

- `.github/workflows/check.yml` runs the suite on push/PR, writes **raw
  unfiltered pytest output to a retained artifact**, and extracts the failure
  list from that file afterwards. A second job repeats the historically flaky
  node 50 times and reports a tally. Live-game work is explicitly out of CI
  scope; the suite is entirely synthetic.
- `scripts/git-hooks/pre-commit` (0.28 s) runs `git diff --check`,
  `audit-tracked-files.py` (the asset-leak guard), `vault-lint.py`, and a
  syntax check of staged Python. Install with `make install-hooks`.
- `pytest.ini` scopes collection to `tests/`. A leftover Wine prefix at
  `tmp/wine-smoke-2370022/dosdevices/z: -> /` made a bare `pytest` from the
  repository root follow that symlink out of the repository and never
  terminate. `make test` was already scoped; a bare `pytest` now is too.
- `tests/test_repo_hygiene.py` asserts `AGENTS.md` and `CLAUDE.md` stay
  byte-identical, that template and generator frontmatter agree, and that
  every executable Python script parses.

## Make targets

`briefing` `budget` `session-caps` `memory-caps` `keys-caps` `wait-caps`
`session-audit` `session-list` `ghidra-index` `ghidra-stats` `run-index`
`run-orphans` `install-hooks` `uninstall-hooks`.

## Boundary

These are repository-hygiene and query tools. They read the Vault, the static
exports, and existing run receipts; none of them launches the game, touches
`originals/`, or produces new evidence about the executable. A generated
briefing, draft, or index is a pointer to evidence, never evidence itself.

## Related

- [[Session control plane]] — the live-session half of the same uplift
- [[Ghidra export structure and caveats]] — how the export must be read
- [[Knowledge Hygiene]] — the conventions these tools enforce
- [[Reverse Engineering Capability Gaps]] — CAP-016 through CAP-018
