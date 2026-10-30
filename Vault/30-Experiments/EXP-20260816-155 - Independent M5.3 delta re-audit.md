---
type: experiment
id: EXP-20260816-155
date: 2026-08-16
question: 'Do the M5.3 corrections restore every M5.1 claim to cited evidence, pin the corrected numbers genuinely, bound the slot claim without overclaiming in the other direction, and leave the module behaviourally unchanged?'
status: accepted
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline static audit; radare2 5.9.8; repository Python 3.14.6; pytest 9.1.1
environment_version: radare2 5.9.8
working_directory: /home/dev/ABLPC
configuration: delta re-audit at clean HEAD 66d1ad4 (parent 2ce8686, subject range 9044e24..66d1ad4); read-only toward game media and originals; no game launch, debugger, breakpoint, target write, commit, or staging
artifacts:
  - reimplementation/ablpc/type1_reset.py
  - tests/test_type1_reset.py
  - static/exports/BIN-97c95ba5572dce63/M5-type1-reset-selector-static-trace.md
addresses:
  - "0x004671D0"
  - "0x004671F2"
  - "0x004671F7"
  - "0x004671FC"
  - "0x00467207"
  - "0x00467971"
  - "0x00401D7A"
  - "0x0044BB70"
  - "0x004DA9C8"
file_offsets:
  - "0x0D95C8"
result: accept-m5-3-corrections-genuine-and-behaviour-preserving-next-packet-m5-4
created: 2026-08-16T17:40:00
updated: 2026-08-16T17:40:00
tags:
  - re/experiment
  - re/static
  - re/audit
  - milestone/m5
---

# EXP-20260816-155 - Independent M5.3 delta re-audit

## Verdict

**ACCEPT** at clean HEAD `66d1ad4`. Every M5.3 correction is genuine,
evidence-backed, and behaviour-preserving; the audit record represents the
M5.2 findings accurately without softening them; no wrong number survives as a
live claim; no retention statement overclaims in either direction.

Scope was the delta only. The M5.2 behavioural findings — the 264,232-trial
differential, the mod-4 argument, the four receipts, the census — stand and
were not re-derived.

## Delta checks

- **D1 numbers.** The corrected extremes appear verbatim in
  `EXP-20260816-153`, [[FUNC-97C95BA5572D-00432930]], and [[Current State]].
  A repository-wide search finds `39,619` and `284,005` surviving **only** as
  deliberate quotations of the rejected values in the audit record, the
  roadmap packets, the Experiments MOC, and the session notes. No live claim
  carries them.
- **D2 test pins are genuine, not retro-fitted.** The suite now asserts
  `(13,729, 17,993)`, `(37,231, 39,316)` and `303,653` as integer square
  roots, classifying near and far *within each gate pair*. These five values
  equal the ones the auditor derived from the binary's own `0x004DA9C8`
  records (file `0x0D95C8`) before this commit existed, so they pin an
  independent derivation rather than the code's output. The parity nuance is
  true: gate 1's near row is the odd one (row 3 at 13,799 versus row 2 at
  39,110); every other gate has the even row nearer.
- **D3 retention wording.** All six sites checked — the census bullet, the
  module's error message, the test docstring, the implementation note,
  `KU-064`, and the static trace. None asserts the slot *is* zeroed; each
  states only that the loader never writes it and the live value is
  unresolved.
- **D4 the `0x004671D0` label is grounded, and the finding strengthens.**
  Prior Vault evidence already established this function as the scene
  initializer that builds a `LEVEL.RAW` path and calls the record walk. The
  audit adds: the three prologue branches at `0x004671F2`, `0x004671F7` and
  `0x004671FC` all converge on `0x00467207`, so the clear is **unconditional
  on every entry**; and the same function calls `0x0044BB70` through thunk
  `0x00401D7A` at `0x00467971`. Statically, any load that walks records was
  preceded by the clear in the same invocation. `KU-064` is therefore
  conservative, and its phrasing remains safe.
- **D5 minor findings.** All three landed: the "distinct positions" wording
  with the repeated descriptors 558/517/484, consumer `0x00436D25`, and the
  implementation note's status.
- **D6 no behavioural drift.** `git diff 9044e24 66d1ad4 -- reimplementation/`
  is exactly the three-line error-message change in `engine_type1_record`,
  same exception type and trigger; `scripts/` and `compatibility.py` show zero
  diff. Both receipts re-ran identically: `(494438, 526143)` selects row 7 at
  distance 7,010 placing `(497248, 31176, 547264)` on descriptor 543;
  `(501696, 494016)` selects row 6 at distance 0 placing
  `(501696, 30092, 494016)` on descriptor 552.
- **D7 audit-record fidelity.** `EXP-20260816-154` reproduces the verdict, the
  checks with their exact numbers, both defects, all four minor findings, and
  the auditor's limitations without softening. The roadmap M5.2 result and the
  M5.3 packet match the corrective packet as specified.
- **D8 gates.** vault-lint 443/0/0, M4 statement valid with five anchors,
  focused 24, full suite 647, tracked audit 0 violations, clean tree.

## Attacks that failed to break the correction

Retro-fit attack on the new test pins; parity attack on the near/far
classification; overclaim attack on all six retention sites; and an attack on
the "level-load entry" label, which instead strengthened the finding.

## Noted imperfections, below the defect threshold

1. **Attribution compression.** The claim that both wrong numbers came from
   the demoted descriptor-anchor pass is **worker-attested, not independently
   established**. The auditor attempted reproduction: result-1 descriptor
   *base* anchors give a second-nearest minimum of `285,443` — close to
   `284,005` but not equal — while bounds-centre and min-corner variants do not
   match at all. The story is plausible, since the scratch pass used the
   `KU-061`-disputed Z bounds that cannot now be reconstructed, but summaries
   must carry the attribution. Corrected in this commit at the roadmap,
   [[Current State]], and the session note that had stated it flatly in the
   auditor's voice.
2. `KU-064` is conservative given D4; its runtime discriminator remains the
   right closure step, and its Known section now cites the convergent-prologue
   fact.
3. The M5.2 note about worker scratch files outside the repository was not
   transcribed; they are untracked environment trivia and need no action.

## Limitations

The M5.2 behavioural battery was not re-run, per the delta scope. The
root-cause story was tested against three anchor conventions only. Whether
`0x004671D0` runs on every level transition remains a runtime question, which
is exactly what `KU-064` holds open.

## Next packet

M5.4 in [[Project Roadmap]]: a predictive integration receipt, the only route
to M5's fourth exit gate at this module's boundary.
