---
type: experiment
id: EXP-20260815-132
date: 2026-08-15
question: Do the accepted PC-native M3.1 through M3.5 results satisfy all four written M3 exit gates at their documented boundaries?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; offline repository and ignored user-owned work-copy audit
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: existing accepted M3 evidence; exact local recipe rebuild; focused asset-free regressions; no game launch, target write, asset edit, or cross-port consultation
artifacts:
  - Vault/00-System/Project Roadmap.md
  - Vault/40-Implementation/Training 51-grain vertical slice.md
  - Vault/40-Implementation/Training FLIK letter transformations.md
  - Vault/40-Implementation/Training FLIKFLIK HUD and completion.md
  - Vault/40-Implementation/Level03 type-1 row discriminator.md
addresses:
  - 0x00417720
  - 0x00442E70
  - 0x00456A90
  - 0x00432930
  - 0x004ACF90
file_offsets:
  - 0x03E8
  - 0x422CB
  - 0x4A4
result: all-four-exit-gates-supported-m3-complete
created: 2026-08-15
updated: 2026-08-15
tags:
  - re/experiment
  - re/milestone-audit
  - re/gameplay
  - milestone/m3
---

# EXP-20260815-132 - M3 exit-gate reconciliation

## Question

Do the accumulated accepted PC-native M3 results satisfy all four written
milestone exit gates, and if so, at what exact boundary can M3 close without
promoting unresolved semantics or broader compatibility?

## Scope and procedure

This packet reviewed only existing evidence for retail executable SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`:

- Training grain insertion, pickup, counter, HUD, tally, and completion in
  `EXP-20260814-111/112`;
- Training letter move/duplicate/remove, pickup-mask behavior, and the exact
  eight-slot one-shot `FLIKFLIK` design in `EXP-20260814-113` and
  `EXP-20260815-114/115`;
- Level03 type-1 row-6 reset-coordinate causality, the natural first-pit
  result-1 path, and the explicit M3.5 geometry disposition in
  `EXP-20260815-117/129/131`.

No game, Wine, Gamescope, debugger, sampler, or audio sink was launched. No
target memory, executable, DAT, `originals/` entry, or persistent work copy was
changed. No PS1 evidence was consulted. Generated audit outputs were created
only in a fresh ignored `work/copies/m3-exit-audit-*` directory and moved to
the desktop trash after their hashes were recorded.

## Exact recipe reproduction

The current public builders were run from the exact retail-derived work copy.
All five results reproduced their accepted hashes and independently reported
exact inverse reconstruction:

| Recipe | Reproduced output SHA-256 | Inverse result |
|---|---|---|
| Training 51-grain DAT | `20d0f9b143a4fceeb058d5ce81680b3e6317995abc3d5ac4103fc85e79b5fd40` | source exact |
| Training 51/50 executable | `8ececefbe1e5747322bd635830f4125500c087d3769094b79545bd7a7b6a4456` | retail exact |
| Training duplicate-letter DAT | `e9c75bb24ae0d0f4f74d17ea63431195e49b7e5278c089588d9372b8eb8cae7a` | 51-grain DAT exact |
| Training `FLIKFLIK` executable | `b572e6d19bc417969c159ba0df7521cbb01b675c260a4dc98d2e6b34475947f4` | M3.2 then retail exact |
| Level03 row-6 candidate DAT | `4894b6159e5a36a37fb9a3f50243cdd816fa4e7f28e169bcadf45b48792d4c12` | source exact |

The combined asset-free suites for those five recipe families pass 25/25.
A first bare system-`pytest` invocation failed collection because it omitted
the repository's configured `PYTHONPATH`; the canonical Makefile-equivalent
invocation with `.venv/bin/python` and `PYTHONPATH=reimplementation` passes.
This is a command-environment correction, not a product or test failure.

The final repository gate passes 576 tests. Vault lint reports 382 notes with
0 errors and 0 warnings; the five M4 compatibility anchors remain valid; the
tracked-file audit reports 0 violations; and both Git diff checks pass.

## Four-gate matrix

| M3 exit gate | Status | Exact evidence and limit |
|---|---|---|
| At least three selected gameplay behaviors have bounded dossiers combining PC runtime and static/data evidence | **Satisfied with three distinct behavior families** | **Collectible/count/completion:** `EXP-111/112` join exact type-`0x3F` records and `0x00417720`/`0x00442E70` to isolated pickup, `49 -> 50 -> 51`, HUD, and `51/50`. **Letter mask/reward/HUD:** `EXP-113/114/115` join selectors, `0x00417720`, exact authored x86, eight runtime bit transitions, one-shot completion, and visible `FLIKFLIK`/`8/8`. **Level03 reset selection:** `EXP-117/129/131` join row-6 file offset `0x4A4`, `0x00432930`, `0x004ACF90`, natural descriptor-572/result-1 events, and repeated row-7 resets. The split Level03 evidence does not establish checkpoint semantics or natural row-6 selection. |
| At least two behaviors can be modified independently through safe data edits or a documented reversible patch mechanism | **Satisfied with four exact recipe families** | Training grain insertion and Level03 row-6 X are independent edits in different level files, each source-hash/layout guarded, reparsed, output-hash pinned, and exactly invertible. Training letter transformation supplies a third guarded data family; the 51/50 and `FLIKFLIK` executable recipes supply documented exact reversible patch mechanisms. None is promoted into a generic gameplay editor. |
| Baseline and mod regression scenarios cover load, play, failure handling, and restoration | **Satisfied at the recorded work-copy and exact-byte boundary** | **Load:** accepted complete-tree Direct3D loads exist for M3.1, M3.3, M3.4, and Level03 control/candidate. **Play:** isolated grain/letter pickups, counter/tally transitions, one-shot completion, and natural pit/reset behavior are recorded. **Failure handling:** the incomplete-drive staging failure is retained in `EXP-111`; wrong hash/layout/old value, overlap, overwrite, link, same-path, and outside-work cases fail closed in the dedicated suites and `EXP-115` audit; rejected debugger-fault arms are not acceptance evidence. **Restoration:** all five reproduced builders prove byte-exact inverse reconstruction and write fresh outputs while leaving their sources and `originals/` unchanged. This is not deterministic whole-route replay, transactional runtime rollback, or a generic installer claim. |
| The boundary between data-driven behavior and executable logic is documented well enough to prioritize future work | **Satisfied at the exact Training and Level03 boundaries** | Data edits can add/move/remove collectible records and alter one authored Level03 row. Existing executable logic supplies terrain initialization, pickup selection, nearest-row reset selection, legacy masks/counters, and the original exact-50 event. Retaining 51 in the tally and extending four letter bits/UI to eight require the documented executable patches. `EXP-131` keeps result-word vocabulary, controller reachability, and row semantics unknown rather than hiding them behind names. Future generic word systems, cross-level reset semantics, persistence, or selective replacement each need a new entry-gated packet. |

## Confirmed

- Three distinct gameplay behavior families meet the written static/data plus
  PC-runtime evidence threshold.
- More than two independent exact edits or reversible patch mechanisms are
  demonstrated without distributing game bytes.
- The recorded scenario set covers complete-tree load, controlled play,
  fail-closed tooling/staging behavior, and exact-byte restoration.
- The documented split between authored DAT state and executable-controlled
  counter, mask, HUD, completion, and reset logic is sufficient to choose
  future bounded work without semantic renaming.

## Explicit non-claims

M3 closure does not establish:

- a generic collectible, word, HUD, checkpoint, trigger, collision, or level
  editor;
- natural controller-only row-6 selection, user-facing checkpoint semantics,
  complete collision-result vocabulary, or cross-level generalization;
- deterministic gameplay replay or engine-frame input capture (`CAP-002`
  remains partial);
- save-format persistence, arbitrary new glyphs/art, or an independently
  reimplemented gameplay module;
- completion of deferred M2 or entry of deferred M5.

## Result

All four written M3 exit gates are supported at their exact demonstrated
boundaries. M3 is **Complete**. This closes the milestone evidence ledger, not
the broader study of gameplay.

No successor milestone activates automatically. M2 retains its causal gate;
M5 retains its module entry gate. Further work should begin from a new concrete
modding or replacement goal, or from PC evidence that contradicts one of this
ledger's bounded conclusions.
