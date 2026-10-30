---
type: experiment
id: EXP-20260816-171
date: 2026-08-16
question: Does the exact M5.7 grain-gate resolver correction reject duplicate JSON keys at every admitted object level without changing any accepted native-model, receipt, threshold, or evidence boundary?
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; Python 3.14 repository virtual environment; offline fresh-context audit only
configuration: exact clean commits efad1c255dcfda31e225c7fdf62608bc59f63e5a and dfd3af31c845939aa972babfd0f44a60e54b6487; no game, Wine, Gamescope, debugger, target write, originals access, or cross-port access
working_directory: /home/dev/ABLPC
artifacts:
  - scripts/grain-gate-resolver.py
  - tests/test_grain_gate_resolver.py
  - work/copies/EXP-20260816-170-m57-resolver/evidence/m58-reaudit-dfd3af3/pytest-resolver-python-m.log
  - work/copies/EXP-20260816-170-m57-resolver/evidence/m58-reaudit-dfd3af3/pytest-focused-64.log
  - work/copies/EXP-20260816-170-m57-resolver/evidence/m58-reaudit-dfd3af3/make-check.log
  - work/copies/EXP-20260816-170-m57-resolver/evidence/m58-reaudit-dfd3af3/sha256.txt
  - work/copies/EXP-20260816-170-m57-resolver/evidence/m58-acceptance-propagation/root-make-check.log
  - work/copies/EXP-20260816-170-m57-resolver/evidence/m58-acceptance-propagation/root-vault-lint.log
  - work/copies/EXP-20260816-170-m57-resolver/evidence/m58-acceptance-propagation/root-tracked-audit.log
  - work/copies/EXP-20260816-170-m57-resolver/evidence/m58-acceptance-propagation/root-diff-check.log
  - work/copies/EXP-20260816-170-m57-resolver/evidence/m58-acceptance-propagation/root-processes.log
addresses:
  - "0x00416580"
  - "0x00432EEA-0x00433043"
  - "0x00432F6A"
  - "0x00432F85"
  - "0x00432F9D"
  - "0x00433790"
  - "0x004337EF"
  - "0x00433807"
  - "0x00599C69"
result: accepted-after-one-strict-json-correction
status: complete
created: 2026-08-16T23:58:00
updated: 2026-08-16T23:58:00
tags: [re/experiment, re/audit, re/static, re/gameplay, reimplementation, milestone/m5]
---

# EXP-20260816-171 - Independent M5.8 grain-gate resolver audits

## Verdict

**ACCEPT** for exact clean correction commit
`dfd3af31c845939aa972babfd0f44a60e54b6487`, tree
`8b7d4234e3a517ed63032bd2d9c9ab8770801714`, over rejected worker
`efad1c255dcfda31e225c7fdf62608bc59f63e5a`.

The first fresh-context audit of `efad1c2` returned **REJECT** for one defect:
default `json.loads` accepted conflicting duplicate member names
last-value-wins despite the strict-JSON contract. It independently retained
the exact retail hash, native disassembly, 50,000 arithmetic plus 10,000
randomized family oracle comparisons, all receipts, focused 60/60, qualified
canonical 682/682, claim limits, lifecycle, and hygiene. The only authorized
correction was all-level duplicate-key rejection plus direct regressions and
honest propagation.

A wholly new James context then returned **ACCEPT** for `dfd3af3`. This is the
independent M5.8 verdict; neither the worker nor the correction accepted
itself.

## Exact correction delta

The audited commit contains 13 tracked files. Code changes are confined to:

- `scripts/grain-gate-resolver.py`: `object_pairs_hook` constructs each JSON
  object while rejecting any repeated decoded member name; and
- `tests/test_grain_gate_resolver.py`: top-level request, nested City gate,
  nested Tunnels record, and valid named-path regressions.

The evaluator, static trace, threshold builder, standoff/coordinate tooling,
and their tests are blob-identical to `efad1c2`. Therefore no correction-delta
claim extends native arithmetic, refusal order, coupling, direct writes,
downstream metadata, receipts, or scope.

## Independent adversarial results

James independently obtained:

- resolver `38 passed` and combined resolver/threshold/coordinate `64 passed`;
  raw-log SHA-256 values
  `6bbfc84227d13919deb67463151df17da3a3c5449de436c828642ca49041145d`
  and `521692fcde22fdcaa9832c66d4ceda49534d79b31b664a27b6f4ed5b92cadc15`;
- literal and JSON-escape decoded-equivalent duplicate keys at the top request,
  nested gate, and nested record all return 2 with empty stdout and exact
  deterministic stderr through stdin; the escaped nested-gate case also
  rejects identically through a named path;
- top/gate/record stderr SHA-256 values
  `0503b432fd04cacc5f01de8bf260c6e00d0bd13ae4fd974e9d69dc3046582bb0`,
  `46c4c43641238006bb84049b68f89d10c027dc2fd2d778256013ef43514f6570`,
  and `b33b73950d637f9d8bc5fe19b8844eb2e543d501d3ce737b1c6d25b5d388bd48`;
  all corresponding stdout files are empty SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- valid stdin and named-path output are byte-identical at SHA-256
  `0e76042f0a5de17a5f38205bdb1bab0701ede5280002012822613bf8e2feb8eb`;
  malformed JSON, bool type, and grain/requirement/index range refusals retain
  exit 2, empty stdout, and their expected messages; and
- direct-log canonical validation reports Vault 482/0/0, five valid M4 hash
  anchors, `686 passed`, and tracked audit 0. Raw-log SHA-256
  `b1e9a4737585160dd7037b79bcc9511b198904f4c2b2302a1456403348bc713f`.

The canonical denominator is explicitly qualified by open KU-065. It neither
erases the retained input-movie timing recurrence nor closes that unknown.
The complete copied audit-evidence manifest is
`work/copies/EXP-20260816-170-m57-resolver/evidence/m58-reaudit-dfd3af3/sha256.txt`,
SHA-256 `44bf4cc6b6cca88e551ba04bdcafe812c7e47be1d3842846c65c8b763f09fc89`.

After acceptance propagation, Root retained a distinct direct-log canonical
gate: Vault 484/0/0, five valid M4 anchors, `686 passed in 18.64s`, and tracked
audit 0. Raw-log SHA-256
`7027c574c9bb6619ea29dc74bc0f62cacbff87333211ec846cde8e71b903df37`.
This is also KU-065-qualified and makes no stronger suite claim.
Final post-propagation Vault lint remains 484/0/0 (SHA-256
`138a1b22d7efc40cf138384c134330cd4d73334ac9a22daf04de48490a7ed278`),
tracked audit is 0 (SHA-256
`341e3736a49a7e7722f7f5f57b7db2b03da46772492f3ecf3c2341ab8d5e30e4`),
and Git diff-check plus exact target-process logs are empty SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## Lifecycle, boundaries, and disposition

The permitted executable work copy independently rehashed to exact retail
SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
Final HEAD/tree, working/index/range diffs, and Git status were clean. No game,
Wine server/client, Gamescope, debugger, pytest, rr target, or ABLPC private
sink was active. The same 32 pre-existing unowned `winedevice.exe` helpers
remain untouched.

M5.7 and M5.8 are complete at the twelve-confirmed-mechanism boundary. The
resolver remains an optional offline model: it does not execute downstream
updates, replace the game routine, name `0x00599C69`, claim global grain-family
exclusivity, or supply the missing row-1 exact-boundary/row-4 independent
runtime observations. Any later integration claim needs a separate admitted
packet and evidence.

Related: [[EXP-20260816-170 - M5.7 grain-gate opening resolver]],
[[PC grain gate opening resolver]], [[Known Unknowns#KU-065 - Intermittent single-test failure in the canonical suite]],
[[Known Unknowns#KU-067 - Meaning and consumers of the City gate-0 byte write]],
and [[Project Roadmap#M5.8 — Independent M5.7 grain-gate resolver hard-truth audit]].
