---
type: experiment
id: EXP-20260815-133
date: 2026-08-15
question: Does the M3 closure at exact clean HEAD 20527a8 survive independent recipe, receipt, refusal, authorization-provenance, and four-gate review?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; exact ignored user-owned PC work copies; offline tracked and runtime-receipt audit
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: exact clean HEAD 20527a87cb0ffc3d5c164ed9c8016e293e64bfe2; worker closure 9ae0e3d26ae331e41da3bd09400f93c8db7a83d5; no game launch, target write, asset edit, debugger attach, or cross-port consultation
artifacts:
  - work/copies/james-m3-closure-audit.knsr12
  - work/copies/EXP-20260815-117-approved-row6-reset
  - dynamic/wine/RUN-KU057-20260815-184629
addresses:
  - 0x00417720
  - 0x00442E70
  - 0x00432930
  - 0x0059D9A0
file_offsets:
  - 0x03E8
  - 0x422CB
  - 0x4A4
result: reject-m3-training-runtime-authorization-provenance
created: 2026-08-15
updated: 2026-08-15
tags:
  - re/experiment
  - re/audit
  - re/gameplay
  - milestone/m3
---

# EXP-20260815-133 - Independent M3 closure authorization hard-truth audit

## Verdict

**REJECT** at exact clean HEAD
`20527a87cb0ffc3d5c164ed9c8016e293e64bfe2`.

The exact recipes, byte identities, inverse transformations, PC static/data
boundaries, accepted Level03 evidence, load/failure/restoration coverage, and
data-versus-executable split survive independent review. The first exit gate
does not: the cited Training behavior receipts disclose target-memory/state
changes and hardware breakpoints, but the cited durable experiment, receipt,
and session records do not establish prior explicit user authorization.

[[Agent Operating Manual#Dynamic analysis]] has required explicit approval for
memory, register, code, execution, or breakpoint changes since the Vault's
bootstrap commit `d3d2738fdd91c97ad22ca9ed38bd712920834e7e`. The project has
already applied that rule in
[[EXP-20260815-116 - Level03 type-1 row discriminator]], where otherwise
useful target-write evidence was retained as diagnostic only until the fresh,
explicitly authorized EXP-117 rerun. The independent audit cannot silently
apply a weaker rule to the Training arms. M3 returns to **Active** only for the
authorization-provenance corrective packet below. No successor begins.

## Method and independence

The audit started from `AGENTS.md`, the full START HERE sequence, charter,
roadmap, decision and unknown registers, relevant MOCs, implementation notes,
static traces, experiments, runtime receipts, and ignored raw artifacts. It
used only PC-native evidence. The bounded PS1 comparisons already recorded by
the worker were not consulted as authority or re-opened.

No game, Wine, Gamescope, debugger, sampler, input worker, or audio sink was
launched. No target state or game asset was changed. Generated rebuild outputs
and refusal probes stayed below ignored
`work/copies/james-m3-closure-audit.knsr12`. Initial and final targeted process
and private-sink audits were clear.

## Exact recipe and inverse reproduction

All five public builders reproduced the existing accepted work-copy files
byte-for-byte:

| Recipe | Output SHA-256 | Independent inverse |
|---|---|---|
| Training 51-grain DAT | `20d0f9b143a4fceeb058d5ce81680b3e6317995abc3d5ac4103fc85e79b5fd40` | retail Training DAT `494d2818...5a22` exact |
| Training 51/50 executable | `8ececefbe1e5747322bd635830f4125500c087d3769094b79545bd7a7b6a4456` | retail executable `97c95ba5...b878` exact |
| Training duplicate-letter DAT | `e9c75bb24ae0d0f4f74d17ea63431195e49b7e5278c089588d9372b8eb8cae7a` | 51-grain DAT `20d0f9b1...fd40` exact |
| Training `FLIKFLIK` executable | `b572e6d19bc417969c159ba0df7521cbb01b675c260a4dc98d2e6b34475947f4` | M3.2 then retail exact |
| Level03 row-6 DAT | `4894b6159e5a36a37fb9a3f50243cdd816fa4e7f28e169bcadf45b48792d4c12` | source Level03 DAT `bda28dc7...0f2b` exact |

The independent reverse walk restored the two inserted/grown DAT tables by
undoing the exact 556 pointer-field relocations, table counts, and inserted
records. It separately reversed the three M3.2 executable bytes, all 29 M3.4
spans to the M3.2 intermediate and then retail, and the Level03 byte at
`0x4A4`. Each result matched its source byte-for-byte and by SHA-256.

The five focused recipe suites pass 25/25. The Level03 `TERRAIN.ALL` parser
suite passes 9/9 and independently reproduces the nine result-1 descriptors
570-578, including descriptor 572 bounds
`X 471712..529888`, `Z 508672..537728`. The complete repository gate passes
576 tests; the pre-documentation Vault check was 384/0/0, all five M4 anchors
were valid, and the tracked-file audit reported zero violations.

## Refusal and failure attacks

- Wrong-source hash: all five public recipes rejected with no output, 5/5.
- Existing output: all five rejected without changing the existing file, 5/5.
- Same source/output argument: all five rejected before mutation, 5/5.
- Outside-tree output: the four CLIs that declare an enforced work boundary
  rejected, 4/4. The older 51-grain CLI documents rather than enforces its
  `work/` output rule, so no outside-work game-bearing output was created.
- Dangling output link: the duplicate-letter, `FLIKFLIK`, and Level03 CLIs
  rejected. The 51-grain and 51/50 CLIs resolve the argument to a fresh target
  and succeed when that target remains in the audit directory. This narrows
  EXP-132's broad “link cases fail closed” wording; it is not the closure
  blocker because the written independent-edit gate remains supported by the
  guarded duplicate-letter and Level03 data families.

The retained incomplete-drive-shape failure from EXP-111 remains a genuine
load/staging discriminator. Rejected Wine/GDB fault arms remain excluded from
behavioral acceptance.

## Runtime receipt audit

The retained PC artifacts agree with the written technical observations:

- EXP-112 transition, HUD, and tally receipt hashes match the ignored files.
- EXP-113's four duplicate-selector receipts match bits `1/2/4/8`; its
  accepted repeated-completion-only receipt matches `3cc319d9...9ee6`.
- EXP-114's exact-final transition/no-retrigger receipts and accepted tally
  capture match their recorded hashes.
- EXP-117's complete `SHA256SUMS` set passes. Its control/candidate traces
  retain exact reset X/Z `(501696,494016)` and `(505792,494016)` after the
  explicitly approved prerequisite writes.
- EXP-129's metadata records the separately authorized grain byte `1 -> 10`;
  the retained selected-event trace contains two ordinary descriptor/value
  `572/1`, flags-`0x14`, `NextLife=2` pit events and the repeated row-7-like
  endpoint.

The current M3 work copies also retain exact final executable/DAT hashes and
positive Direct3D 640x480x16, level-load, `End InitMainGame`, and `NextLife`
markers. Some receipt-pinned historical game-log snapshots have since been
overwritten by ordinary ignored work-copy churn; this does not contradict the
retained hashed state receipts and screenshots, but those missing historical
log bytes cannot be independently rehashed now.

## Exact closure defect

The Training runtime families use target changes beyond ordinary controller
input:

- EXP-111 restores live records, resets the grain counter, places the player,
  and zeroes velocity before the isolated new-grain pickup.
- EXP-112 arms pickup/tally state and uses breakpoints to discriminate
  `49 -> 50 -> 51`, the HUD cache, and the patched completion path.
- EXP-113 resets mask/reward state, places the player at duplicate records,
  and installs hardware breakpoints for the selector discriminators.
- EXP-114 arms exact mask/reward/tally state for the final transition and
  visible tally receipts.

Those experiment notes, their runtime receipts, and their session notes
disclose the procedures, but none records prior explicit approval for the
target-memory/state changes and breakpoints. This audit does not assert that
approval never occurred outside the durable repository. It finds that the
cited evidence cannot prove it, and conversation memory is not an acceptable
substitute for the Vault handoff.

The Level03 family is different: EXP-117 records the exact proposed writes and
the user's explicit prior reply, while EXP-129 records the exact separately
authorized grain-byte write and distinguishes it from the ordinary pit
events. Only that one of EXP-132's three behavior families therefore has
independently auditable authorization provenance.

## Four-gate ledger

| M3 exit gate | Independent disposition |
|---|---|
| Three gameplay behaviors with static/data plus PC runtime evidence | **Open.** The technical Training receipts exist, but their cited durable records do not prove the prior authorization required for the target changes and breakpoints. EXP-116 establishes that such evidence is diagnostic until corrected. Only Level03 has auditable approval provenance. |
| Two independently modifiable behaviors through safe data edits or reversible patches | **Supported.** All five hashes and inverses reproduce; at minimum the guarded duplicate-letter and Level03 data families are independent. The two dangling-link normalizations narrow refusal wording but do not erase those two safe families. |
| Baseline/mod scenarios cover load, play, failure handling, and restoration | **Supported at the stated work-copy/byte boundary.** Current exact candidates retain load gates; explicitly authorized Level03 control/candidate and ordinary pit play exist; staging and refusal failures are retained; all five byte inverses are exact. No deterministic route or transactional runtime rollback is inferred. |
| Data-driven versus executable-logic boundary is documented enough for prioritization | **Supported.** DAT population/position/selector and one Level03 row remain separate from executable terrain, selection, counter, mask, HUD, tally, and completion logic. The old Level03 static-trace phrase “current player globals” is explicitly superseded by EXP-128 and the current function/structure dossiers, which correctly call `0x0059D960` auxiliary/reset-coordinate state. |

Three supported rows cannot close a four-gate milestone.

## Smallest corrective packet

Create one approval-compliant Training runtime packet; do not change any
recipe, parser, static conclusion, milestone wording, Python/C procedure, or
Level03 result:

1. Before launch, present and obtain explicit approval for the exact bounded
   Training memory/state changes and any hardware breakpoint or execution-
   control use.
2. In fresh exact Direct3D processes, reproduce one isolated appended-grain
   pickup under the retail executable and one moved duplicate-letter mask
   pickup under the retail executable. Record exact executable/DAT hashes,
   before/after values, target survival, and complete cleanup.
3. Use no continuation from the known faulting breakpoint sites. Retain any
   contradiction rather than substituting static inference.
4. Re-run the focused/full/Vault/M4/tracked/process/sink gates and request a
   fresh independent closure audit.

If a durable artifact that proves the exact prior authorization already
exists, citing and validating that artifact may replace the corresponding
rerun. An inferred or reconstructed approval statement may not.

## Result

`REJECT`: reopen only M3's exit-gate reconciliation for the two missing
authorization-provenance Training runtime families. All exact recipes,
inverses, static/data results, explicitly authorized Level03 evidence,
failure/restoration evidence, completed M4/M6 results, deferred M2/M5 state,
and the Python/C procedure remain unchanged.

## Later corrective worker

[[EXP-20260815-134 - Approval-compliant Training runtime receipts]] executes
the requested smallest corrective packet with two fresh, explicitly
authorized, breakpoint-free Training arms. This does not rewrite or self-
overrule the `REJECT` above. The later
[[EXP-20260815-135 - Independent M3 ratchet acceptance audit]] validates that
correction and returns a new `ACCEPT` disposition without rewriting this
historical rejection.
