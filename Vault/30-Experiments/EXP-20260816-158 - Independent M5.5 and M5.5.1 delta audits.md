---
type: experiment
id: EXP-20260816-158
date: 2026-08-16
question: 'Do the M5.5 and M5.5.1 corrections restore every M5.4 claim to retained evidence, with the settle band consistent across every live artifact and no logic drift?'
status: accepted
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline audit of repository state and retained artifacts; no game launch, debugger, or target write
environment_version: Python 3.14.6
working_directory: /home/dev/ABLPC
configuration: two delta passes, at cdef7c7 (REJECT, one residual site) and f0ea760 (ACCEPT); read-only toward game media, originals, and the external repository; nothing committed or modified
artifacts:
  - scripts/grain-gate-standoffs.py
  - scripts/type1-reset.py
  - work/copies/EXP-20260816-156-evidence/control-bugs.log
addresses: []
file_offsets: []
result: accept-m5-5-1-closes-the-chain-with-one-non-gating-count-erratum
created: 2026-08-16T20:30:00
updated: 2026-08-16T20:30:00
tags:
  - re/experiment
  - re/audit
  - milestone/m5
---

# EXP-20260816-158 - Independent M5.5 and M5.5.1 delta audits

## Verdict

**ACCEPT** at `f0ea760`, after a `REJECT` at `cdef7c7`. This closes the
M5.1 → M5.2 → M5.3 → M5.4 → M5.5 → M5.5.1 chain: exit gate 4 stands for the
type-1 module at its Level03 boundary.

## First delta pass - REJECT at `cdef7c7`

The M5.5 corrections were genuine and scope-clean, but the done condition
"the band is consistent everywhere it appears" was falsified by one residual
site: `scripts/grain-gate-standoffs.py` still published the superseded
`121-126` in its docstring **and inside its emitted deterministic JSON**
(`rest_y_note`). An operator reading that report would have treated the
accepted `+129` settle as an anomaly, and the tool's own companion note had
been corrected to `121-129` in the same commit — leaving tool and
documentation in disagreement. This is the same defect class M5.5 existed to
fix, in the sibling of the very note that commit corrected on the
"live operational guidance" principle.

Confirmed in that pass:

- **No-loop window.** The note states exactly what the trace holds — one
  `NextLife=2` row at `604.5 ms`, then 0 to the final retained row at
  `3076.1 ms`, about 2.47 s — and is explicitly bounded to what is retained.
  No substituted number. The stop explanation is properly hedged and coheres
  with the EXP-20260816-148 focus finding and with both arms ending near
  3.05-3.08 s.
- **Control log.** `control-bugs.log` SHA-256
  `85b39abf7fa1c85f95dd341e347f45dbbfbfe9c45e1f015b35244bdd871932b7` matches
  the citation, is byte-identical to the live file the auditor had
  independently located before the commit existed, and carries 6/6 markers
  with zero soft-render hits.
- **The new test is a real pin.** It rebuilds the candidate through the
  guarded editor, asserts the retained hash and the exact placement, and
  requires the hard-coded runtime observation `31897` to fall inside the
  emitted band. It **fails under the old constant** and passes at the
  boundary; the observed values are constants from the receipt, independent of
  the band definition. Its honest limit: it guards against a band that
  excludes receipts, not against arbitrary over-widening — the enumerated
  "observed extremes" framing carries that half.
- **Scope.** The pre-registered section is byte-verbatim against `a58f962`;
  only frontmatter differs, and that changed in `b861376`. No
  `reimplementation/` file, prediction value, selector or refusal code, or M4
  authority was touched. The extra corrected site
  ([[PC grain gate threshold mod]]) was **in bounds** and disclosed.
- **Historical notes.** Leaving the superseded band in EXP-141/142/153/157,
  the pre-registration section, dated history, session notes, and
  `test_terrain_height.py`'s receipt-specific docstring is the right call;
  none is forward guidance.

## Second delta pass - ACCEPT at `f0ea760`

Both strings now mirror the wording shipped in `scripts/type1-reset.py`, and
the report's `evidence` list gains the receipts that establish the range.
`build_report` was executed independently: the emitted note reads 121-129 as
observed extremes, not a guarantee, and two runs are byte-equal, so the
determinism test still compares two live invocations. The commit's only code
file is the standoffs script, whose diff contains no change to standoff
selection or the gate constants. The coverage-map row is now "Reset
placement" with zero occurrences of the banned word.

Gates: focused 39 (25 type-1 plus 14 terrain/standoff), full 648, vault-lint
450/0/0, M4 statement valid, tracked audit 0, clean tree.

## Erratum, non-gating

The acceptance-search tally recorded as "18 occurrences" is **19** at the
committed HEAD. The count is self-referential: the sentences recording the fix
themselves contain the superseded string, so a tally taken before committing
reads one lower than the committed tree. The substantive property the done
condition gated on — that every occurrence is historical, receipt-specific, or
an explicit quotation — was independently verified for all 19. Corrected in
[[Current State]] and the roadmap rather than banked as written, because this
chain's whole lesson is that recorded numbers must reproduce.

## Note on the coverage map

The auditor's sanity check found **no Cross-Port Evidence Policy violation**:
the cited commit matches the registry, reads were blobs-only, the 18 rows are
an ABLPC-authored condensation rather than a reproduction, the inventory is
labelled inference about where to look, every PC-status anchor cites PC
evidence alone, and sequencing is deferred to the roadmap. Two follow-ups were
recommended and are now applied: the banned word is gone from the row title,
and [[XPORT-20260816-003 - Subsystem inventory seeding]] records the seeding
event with the reproducible `git ls-tree` invocation behind the 115-note
count.

## Limitations

Neither pass ran the game, attached a debugger, or wrote target memory; the
runtime story continues to rest on the M5.4 audit's verification of retained
artifacts. The external repository was not consulted in these passes, so the
115-note count was not independently corroborated there — which is precisely
why the seeding record above now carries the reproducing command.
