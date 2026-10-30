---
type: experiment
id: EXP-20260816-166
date: 2026-08-16
question: 'Does any distinct second module satisfy all six M5 entry criteria on existing PC evidence, or should M5 deliberately rest with the type-1 resolver alone?'
status: independently-accepted-after-correction
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; GNU objdump 2.46-3.fc44; repository Python 3.14.6; offline PC evidence audit only
environment_version: Python 3.14.6
working_directory: /home/dev/ABLPC
configuration: exact clean subject 21c5e870d7c1d5c3470f9749f64a24a9cb1fc244; exact retail work-copy executable; existing static/runtime evidence only; no game, Wine, Gamescope, debugger, target write, implementation, or external-source access
artifacts:
  - Vault/20-Research/PC grain gate requirements.md
  - Vault/40-Implementation/PC grain gate threshold mod.md
  - static/exports/BIN-97c95ba5572dce63/M3-level03-type1-row-static-trace.md
  - static/exports/BIN-97c95ba5572dce63/M5-type1-reset-selector-static-trace.md
addresses:
  - "0x00416580"
  - "0x00432B30"
  - "0x00432F0C"
  - "0x00432F85"
  - "0x00432F9D"
  - "0x00433790"
  - "0x004337D6"
  - "0x004369B0"
  - "0x00436D25"
file_offsets:
  - "0x00015980"
  - "0x00031F30"
  - "0x0003230C"
  - "0x00032385"
  - "0x0003239D"
  - "0x00032B90"
  - "0x00032BD6"
  - "0x00035DB0"
  - "0x00036125"
  - "0x000D95C8"
result: grain-gate-resolver-admitted-after-m561-acceptance
created: 2026-08-16T20:04:00-04:00
updated: 2026-08-16T21:15:00-04:00
tags:
  - re/experiment
  - re/audit
  - re/gameplay
  - milestone/m5
---

# EXP-20260816-166 - M5 second-module entry-gate audit

> [!correction] M5.6.1 correction after independent rejection
> [[EXP-20260816-167 - Independent M5.6 hard-truth audit]] rejects exact
> subject `3504f6a` for an omitted City gate-0 direct write, one misread
> type-1 row expression, an unsupported claim that only one criterion was
> missing from the rejected candidate, and over-promotion of EXP-146's direct
> reference census into global exclusivity. The live corrected worker boundary
> is recorded here and in
> [[EXP-20260816-168 - M5.6.1 claim and contract correction]]. Final
> path-bounded [[EXP-20260816-169 - Independent M5.6.1 delta audits]] accepts
> exact clean correction `dd034c9` after one residual table-scope repair.

## Verdict

**Final accepted result: admit exactly one second module, a bounded grain-gate
opening resolver.**
Existing PC evidence satisfies all six M5 entry criteria for the exact
Tunnels/City Entrance trigger-decision boundary. This packet performs no
implementation; M5.7 owns that separate active packet after EXP-169 acceptance.

Do not admit the index-ordered type-1 consumer candidate. Its PC-static path is
real at `0x004369B0` and `0x00436D25`, but no retained original runtime
observation establishes an index advance or output transition. That is the
decisive **first failed** entry criterion; the complete state contract, known
edges, and distinct modding outcome remain unassessed rather than silently
credited.

This result does not reopen M2/M3/M4/M6, extend the accepted type-1 module,
promote type 1 to checkpoint/respawn semantics, or create a general trigger
engine. No PS1 or other external evidence was used.

## Procedure and identity

The exact retail work-copy executable rehashed to
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
The candidate instructions were independently re-read with GNU
`objdump -d -Mintel`; the audit then reconciled those instructions against
EXP-136/139/144/145/146/148/149, existing implementation notes, ignored
runtime-receipt references, and asset-free tests.

No runtime was launched. The audit was read-only toward all game material and
did not access `originals/` or the external PS1 working tree.

## Candidate ranking

| Rank | Candidate | Result | Decisive reason |
| ---: | --- | --- | --- |
| 1 | Grain-gate opening resolver (`0x00432B30`, `0x00433790`, `0x00416580`) | **Admit** | All six criteria pass at a pure Tunnels/City trigger-decision boundary. |
| 2 | Index-ordered type-1 consumers (`0x004369B0`, `0x00436D25`) | **Reject for now** | Missing cited original runtime observation of the index/source/output transition. |

The coverage-map screen found no stronger distinct candidate. The accepted
terrain-height model is already a direct dependency inside the first admitted
type-1 resolver's closed boundary, so counting it again would not be a second
module. The Training collectible/HUD packets have extensive evidence and
exact builders, but their notes explicitly close the current authored goals;
no new replacement outcome is stated. Resource-binding/render-admission work
remains excluded by DEC-133 and `KU-023`. The remaining Touched/Untouched rows
lack either a bounded contract or retained original behavior at their current
top open question.

## Admitted contract: grain-gate opening resolver

The future module is a pure, offline state-transition evaluator, not an
executable patcher and not a whole-level update reimplementation.

### Inputs

- family/internal level: Tunnels level 3 or City Entrance level 4;
- signed 32-bit Flik X/Z and unsigned grain byte;
- explicit current gate state plus the exact requirement/center/radius data;
- for Tunnels, the nine 20-byte resident records while preserving unknown
  `+0x04` and the original row order;
- for City, the gate index, current state, call-site center/radius,
  animation-slot indices/deltas, and either the retail formula or an explicit
  guarded `0..50` requirement.

### Outputs

- whether the original gate-opening branch is eligible;
- the ordered direct-write plan for the opening branch: Tunnels type `0x1068`
  plus row-0/4 coupling; City state `0x20` plus, for index 0 only, address-
  named byte write `[0x00599C69] = 1`; and the downstream Tunnels decay or
  City state-decrement/animation slot-delta rule needed to explain the
  accepted terminal receipt;
- an explicit non-opening reason: already non-closed, insufficient grain, or
  outside the engine-exact proximity predicate.

The contract excludes callee side effects and their semantics, message/audio
dispatch, renderer behavior, controller reachability, per-frame animation
rendering, unrelated portions of the two level-update functions, save
persistence, and trigger families other than the twelve confirmed mechanisms.
The meaning of byte `0x00599C69` is Unknown; the address-named write is included
only because it is a direct instruction in the index-0 opening branch.

## Six-criterion entry matrix

| Gate criterion | Existing PC evidence | Result |
| --- | --- | --- |
| Bounded input/output or transition contract | Tunnels gate loop `0x00432EEA`-`0x00433043`; City helper `0x00433790`; exact inputs/outputs above. EXP-146 confirms 22 direct/static grain-byte references, the two known positional comparisons, dispatcher routes, and structure bindings; it does not exclude indirect/cached families. This module is bounded to the twelve accepted mechanisms and needs no global-exclusivity claim. | **Pass** |
| PC locators and original runtime observations | Grain compare `0x00432F0C`/`0x004337D6`; proximity `0x00416580`; coupling `0x00432F85`/`0x00432F9D`; runtime EXP-137/138/148/149 and visible mapping EXP-144/145. | **Pass** |
| Asset-free fixtures | `tests/test_grain_gate_mod.py` builds synthetic executable-shaped bytearrays; `tests/test_coordinate_overlay.py` uses fake memory and pins centers, requirements, states, and signed-shift distance results. The combined focused run is 26 tests and needs no game bytes. | **Pass** |
| Known error and edge behavior | Only closed Tunnels type `0x10C7` and City state `-1` may trigger; arithmetic is signed 32-bit `sub`/`sar 8`/wrapping `imul`+`add` followed by signed comparison; supported authored requirements stay in the accepted `0..50` domain; rows 0/4 couple unconditionally on either opening arm; row 1's exact one-below runtime receipt is absent and disclosed. | **Pass** |
| Differential test where practical | Ten of twelve mechanisms have accepted closed-at-`min-1`/open-at-`min` PC runtime transitions. Row 1 has the narrower accepted “opens above minimum” receipt and the same native loop; row 4 is intentionally non-separable because opening row 0 opens it. City slot/delta predictions match terminal values exactly. | **Pass** |
| Written modding outcome | The existing exact threshold builder changes requirements but still needs a game launch to predict whether a state/position/count tuple opens a mechanism. An offline resolver gives mod authors deterministic preflight for threshold and placement edits and explains row coupling before runtime. | **Pass** |

## Confirmed native boundary

### Tunnels

Inside `0x00432B30`, only rows whose type is `0x10C7` reach the opening test
(`0x00432EF1`-`0x00432EFD`). `0x00432F0C` zero-extends grain byte
`0x0059D9B1`; the signed comparison at `0x00432F12` branches to the
insufficient path when grain is below the record requirement. The position
differences wrap at 32 bits, use arithmetic `sar 8`, and their wrapped signed
squared sum must be less than `0x2710` at `0x00432F49`.

A qualifying row receives type `0x1068` at `0x00432F6A`. Row 0 also writes
that type into row 4 at `0x00432F85`, while row 4 writes it into row 0 at
`0x00432F9D`. Later updates subtract 140 while type exceeds `0x708`, producing
the accepted terminal `0x0690` state. The future resolver may report the
opening event and state plan without claiming to replace all of
`0x00432B30`.

### City Entrance

`0x00433790` tests state `-1`, calls `0x00416580` with the live Flik block and
call-site center/radius, then compares the grain byte at `0x004337D6` with
the requirement. A qualifying event writes state `0x20` at `0x004337EF`;
after `test esi,esi` at `0x00433803`, index 0 additionally writes byte value 1
to `0x00599C69` at `0x00433807` (file `0x00032C07`). The byte's meaning is
Unknown. Positive state then decrements and applies the call-site animation
deltas to the two specified slots. EXP-139's gate-to-slot predictions
reproduce the accepted terminal runtime values for gates 0-2.

These are Confirmed instruction/state facts. Visible barrier identity is
confirmed only through the bounded EXP-144/145 mapping; no general trigger
architecture is inferred.

## Rejected candidate: index-ordered type-1 consumers

The candidate is not imaginary. `0x004369B0` reads slot `0x005C5864` and
initializes `0x0059C184`/`88`/`8C` from the first 12-byte row shifted left
five. Inside the later update, `0x00436D25` reads the same slot, uses index
`0x0059F4C4`, and loads one indexed XYZ row: X from
`[base + 12*i + 4]` at `0x00436D50`, Y from `[base + 12*i + 8]` at
`0x00436D5F`, and Z from `[base + 12*(i+1)] = [base + 12*i + 12]` at
`0x00436D6F`. It writes the shifted tuple to
`0x0059C1A8`/`AC`/`B0` and calls the same proximity helper before later index
state advances. Those PC-static facts do not establish the original runtime
transition or its higher-level purpose.

**Decisive first failed criterion:** cited original runtime observation. The
complete contract, edge behavior, and distinct modding outcome are not
established and are not scored as passes. The smallest discriminator is one
separately authorized, read-only internal-level-9 observation retaining the
type-1 record/count, index `0x0059F4C4`, the one selected row, current triple
`0x0059C184`/`88`/`8C`, candidate triple `0x0059C1A8`/`AC`/`B0`, and before/
after index state across one natural index advance. No target write or semantic
name is required. A receipt would trigger a new six-criterion audit; it would
not admit the candidate automatically.

## Adjacent knowledge correction

KU-063 still said a type-1-less level leaves the previous level's pointer in
slot `0x005C5864`. That is contradicted by the already-accepted clear at
`0x00467207`-`0x00467215` in level-load entry `0x004671D0`, recorded by
EXP-154/155 and KU-064. The live register is corrected: a load through
`0x004671D0` clears the slot before the record walk; only a transition that
skips that entry could retain stale state, and whether such a route exists is
Unknown.

## Validation

- Focused candidate fixtures ran through the repository virtual environment:
  `26 passed in 0.30s`; raw log SHA-256
  `a0594220bed2eb93f2f65c443c70d2e98d53ad47c080d1e23414a9810ecb9caa`,
  preserved at
  `work/copies/EXP-20260816-168-m56-correction/evidence/worker-focused-26.log`.
- An initial bare host `pytest` invocation collected no tests because the
  repository package was not on that interpreter's import path; it is an
  invocation error, not a test failure, and the virtual-environment command
  above is the retained result.
- Canonical `make check` completed with Vault lint `472 notes, 0 errors,
  0 warnings`, five M4 compatibility anchors, `648 passed in 18.18s`, and
  tracked-file audit `0 violation(s)`. Raw log SHA-256:
  `4059dbfcc8532dd34c4905babebe3bb02d03f8c9ab6e235f8258c544361b8eb2`,
  preserved at
  `work/copies/EXP-20260816-168-m56-correction/evidence/worker-make-check-648.log`.
  This is one exact passing observation, not an unqualified clean-suite claim;
  KU-065 remains open because its lost one-test failure still has not been
  identified.
- Closure found no active game, Gamescope, Wine server, Wine client, debugger,
  pytest, or `rr` process and no private audio sink. The same 32 unowned
  pre-existing `winedevice.exe` helpers recorded by EXP-163 remain, PIDs
  `68248`-`344284`, all parented by user systemd PID `1927`; they were not
  terminated by name. Exact process-name table SHA-256:
  `a2a8aa299bc8fb43573a0ec6228fe1c2532ff5fd9797f394cf1304cd81bd30e8`,
  preserved at
  `work/copies/EXP-20260816-168-m56-correction/evidence/worker-process-names.log`.
- No implementation, game-bearing file, runtime process, or target state was
  created or changed.

## Resulting work packet

EXP-169 independently accepts the corrected grain-gate resolver as M5's second
module at exact commit `dd034c9`. M5.7 may now implement only this pure
twelve-mechanism boundary; the entry audit licenses no broader trigger family.
