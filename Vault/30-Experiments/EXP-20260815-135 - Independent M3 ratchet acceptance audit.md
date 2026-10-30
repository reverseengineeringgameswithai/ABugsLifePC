---
type: experiment
id: EXP-20260815-135
date: 2026-08-15
question: Does the approval-compliant EXP-134 correction close the sole defect from EXP-133 and independently satisfy all four M3 exit gates?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; offline tracked and ignored user-owned work-copy audit
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0; GCC 16.1.1
working_directory: /home/dev/ABLPC
configuration: exact clean worker HEAD 26c7109bca6adc2a011299d1a9500e7169d37681; no game launch, target mutation, debugger attach, or cross-port consultation
artifacts:
  - dynamic/wine/EXP-20260815-134-receipt.md
  - work/copies/EXP-20260815-134-approved-training-runtime
  - work/copies/james-m3-ratchet-audit.crHBQZ
addresses:
  - 0x00417720
  - 0x00442E70
  - 0x00432930
  - 0x0059D910
  - 0x0059D920
  - 0x0059D9B1
  - 0x0059D9B2
file_offsets:
  - 0x03E8
  - 0x422CB
  - 0x4A4
result: accepted-m3-four-gate-closure-after-authorization-correction
created: 2026-08-15
updated: 2026-08-15
tags:
  - re/experiment
  - re/audit
  - re/gameplay
  - milestone/m3
---

# EXP-20260815-135 - Independent M3 ratchet acceptance audit

## Verdict

**ACCEPT** at exact clean worker HEAD
`26c7109bca6adc2a011299d1a9500e7169d37681`.

EXP-134 supplies the smallest correction required by EXP-133: two fresh,
prior-authorized, breakpoint-free retail Training behavior receipts. Their
raw identities, write/readback boundaries, isolated outcomes, survival, and
cleanup survive independent offline review. Combined with EXP-133's retained
acceptance of gates two through four and the independently rechecked recipes,
all four written M3 exit gates are supported at their existing narrow limits.
M3 is Complete. No successor milestone activates automatically.

## Starting state and scope

The coordinator initially supplied an incorrect suffix for the worker commit,
then corrected it before substantive evidence review. Git independently
resolved the clean repository HEAD to the full hash above; its parent is the
EXP-133 rejection commit `ecad195dac748cf88f2179256d35fec93517385c`.

The audit re-read `AGENTS.md`, the START HERE chain, charter, operating manual,
M3 roadmap and MOCs, EXP-111 through EXP-117, EXP-129, EXP-131 through
EXP-134, their supersession notes, implementation boundaries, tracked receipt,
and ignored raw evidence. It used PC-native evidence only. No game, Wine,
Gamescope, debugger, observer, private sink, or target process was launched or
mutated by this audit.

## Authorization boundary

Before either EXP-134 launch, the worker presented the exact two fresh-process
mutations: current and preceding XYZ at `0x0059D910` and `0x0059D920`, grain
target `(167776,-34272,38112)`, letter target `(156800,-59296,48000)`, exactly
24 target bytes per process, read-only observation, excluded fields, and
abort-on-mismatch rules. The researcher then said that approvals were up to
the worker and `Assume yes for me`.

The durable experiment, session, decision, and receipt agree that the reply
followed the exact proposal and preceded both launches. This meets
[[Agent Operating Manual#Dynamic analysis]] at the same documented boundary
used for EXP-117. It does not retroactively authorize EXP-111 through EXP-114,
grant permission over originals, or widen the two exact writes.

## Raw identity and mutation audit

All hashes named by the tracked receipt reproduce from the retained raw files:

| Item | SHA-256 |
|---|---|
| retail executable in both arm trees | `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878` |
| grain DAT | `20d0f9b143a4fceeb058d5ce81680b3e6317995abc3d5ac4103fc85e79b5fd40` |
| duplicate-letter DAT | `e9c75bb24ae0d0f4f74d17ea63431195e49b7e5278c089588d9372b8eb8cae7a` |
| grain accepted trace | `bda3c390bce41cb5ee894217d500e37e18a8d80d2601d69131dc51b4004d3612` |
| letter accepted trace | `8ff28122ba8545f96e8a14323ccbb96d15d5fbf1793228504b77d0f6ad0787fd` |
| grain/letter write receipts | `1d334da9...c0f0e` / `a1d16934...91a65` |
| grain/letter logs | `f6a69287...d47d` / `6fdc4c95...694c` |

The retained helper source hashes to `7cc425b7...1fb`. An independent GCC
`-O2 -Wall -Wextra -std=c11 -no-pie` build reproduced the exercised helper
byte-for-byte at SHA-256 `a5a8fae9...910b6`. Source and disassembly contain one
two-local/two-remote-vector `process_vm_writev` call targeting only 12 bytes at
each of `0x0059D910` and `0x0059D920`; success requires return value 24 and is
followed by readback of current, preceding, and auxiliary triples.

Both retained write receipts report exactly 24 bytes and exact current plus
preceding readback. Auxiliary retained its pre-write value in the immediate
receipt, proving it was not directly written. In both later traces the engine
adopted the target into auxiliary, consistent with EXP-130; this ordinary
engine response is retained and is not mislabeled as part of the write.

## Independent trace reconstruction

Each accepted JSONL contains one clean identity row, one ready row, 791 sample
rows, and one summary with zero read failures. The summary exactly duplicates
the terminal sample.

| Arm | Fresh identity | Coupled transition | Isolation | Terminal |
|---|---|---|---|---|
| appended grain, PID 164249 | tag `0x003F003F`, entry 62 selector `0x14` y `-1301`, grain/mask/NextLife `0/0/0` | at 5.022054922 s, entry 62 y becomes `0x80000000` and grain `0 -> 1` | entries 0/1 remain exact; mask and NextLife stay 0 | 791st sample at 7.995816292 s retains target and accepted state |
| moved duplicate letter, PID 165750 | tag `0x003F0043`, entry 63 selector `0x10` y `-1853`, mask/grain/NextLife `0/0/0` | at 4.654635748 s, entry 63 y becomes `0x80000000` and mask `0 -> 1` | original entry 50 remains exact; grain and NextLife stay 0 | 791st sample at 7.992603017 s retains target and accepted state |

All record x/z/selector fields remain exact. Both rewards remain 5, internal
level remains 17, the table pointer and type/count tag remain stable, and each
current/preceding tuple has only its pre-write and authorized target values.
The later process-survival receipts are timestamped after their corresponding
terminal trace and show each exact PID still live in its owned process group.

Both 64,723-byte logs independently contain the required no-software,
Direct3D, 640x480x16, renderer-start, Training DAT load, end-init, and
`NextLife` markers; neither contains `INITSOFTRENDER`.

One failed initial grain calibration JSONL is retained. The narrative also
mentions a second read-only letter preflight that has no separate raw file.
No acceptance claim depends on those calibration attempts: each accepted
trace begins with its own clean, corrected, candidate-specific identity row.

## Recipe, inverse, and regression audit

Fresh outputs below ignored `work/copies/james-m3-ratchet-audit.crHBQZ`
match the accepted work-copy files byte-for-byte:

| Recipe | Rebuilt SHA-256 | Inverse disposition |
|---|---|---|
| Training 51-grain DAT | `20d0f9b143a4fceeb058d5ce81680b3e6317995abc3d5ac4103fc85e79b5fd40` | retail Training DAT exact |
| Training 51/50 executable | `8ececefbe1e5747322bd635830f4125500c087d3769094b79545bd7a7b6a4456` | retail executable exact |
| Training duplicate-letter DAT | `e9c75bb24ae0d0f4f74d17ea63431195e49b7e5278c089588d9372b8eb8cae7a` | 51-grain DAT exact |
| Training `FLIKFLIK` executable | `b572e6d19bc417969c159ba0df7521cbb01b675c260a4dc98d2e6b34475947f4` | M3.2 then retail exact |
| Level03 row-6 DAT | `4894b6159e5a36a37fb9a3f50243cdd816fa4e7f28e169bcadf45b48792d4c12` | source Level03 DAT exact |

Every current builder again reports its internal exact inverse. Those outputs
also match the files independently reversed in EXP-133, so the inverse claim
does not rest only on the worker packet. The five focused recipe suites pass
25/25 and the terrain parser suite passes 9/9.

The exact worker commit passes `make check`: Python dependency checks, Vault
388/0/0, all five M4 compatibility anchors, all 576 tests, and zero tracked-
file violations. Git diff checks pass.

## Four-gate ledger

| M3 exit gate | Independent disposition |
|---|---|
| Three behaviors with static/data plus PC runtime evidence | **Supported.** EXP-134 replaces the governance-defective runtime role of the old Training arms with fresh appended-grain and moved-duplicate-letter receipts. Their existing PC static/data paths remain exact. EXP-117/129/131 retain the independent Level03 reset family. |
| Two independently modifiable behaviors through safe data edits or reversible patches | **Supported.** Five exact outputs/inverses reproduce. The grain, letter, and Level03 DAT families are independently guarded, and two exact executable patch families remain available. |
| Baseline/mod scenarios cover load, play, failure handling, and restoration | **Supported at the documented boundary.** EXP-134 supplies fresh exact Direct3D load/play/survival receipts; the retained incomplete-drive and fail-closed CLI cases cover failure; all five recipes restore byte-exactly without touching originals. This does not claim deterministic route replay or transactional runtime rollback. |
| Data-driven versus executable-logic boundary is documented enough for prioritization | **Supported.** DAT records own bounded population, position, selector, and one Level03 row; executable logic owns pickup, reset selection, counters, masks, HUD/tally, and completion. Broader semantics remain explicit unknowns. |

## Limits and hygiene

The Training receipts are write-assisted position discriminators, not
controller-only reachability. They freshly confirm only appended grain entry
62 and duplicate selector-`0x10` entry 63; other historical selector,
counter/tally, and `FLIKFLIK` boundaries remain supported by their retained
technical evidence rather than being re-run by EXP-134.

Current process and sink audits are empty. Wine `Y:` resolves to
`work/copies/BUGS_PC-full-disc`. No game-bearing file, helper binary, trace,
log, screenshot, or work-copy output enters Git. M2 and M5 remain Deferred;
M4 and M6 remain Complete; the Python/C procedure and CAP-002 status are
unchanged.

## Result

`ACCEPT`: EXP-134 resolves KU-059 at its exact two-arm authorization boundary,
and all four written M3 gates independently pass. M3 is Complete only at the
documented Training and Level03 boundaries. Select any future work from a new
concrete goal and test it against the retained M2 or M5 entry gate; do not
invent an automatic successor.
