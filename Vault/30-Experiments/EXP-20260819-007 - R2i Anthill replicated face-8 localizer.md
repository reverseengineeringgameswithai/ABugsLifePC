---
type: experiment
id: EXP-20260819-007
status: completed
date: 2026-08-19
updated: 2026-08-19
result: Authorized C1/L1/L2/C2 completed procedurally; causal result inconclusive because fresh control nuisance escaped the frozen mask and the localizer effect did not replicate.
question: Does the exact guarded face-8 tuple mutation reproducibly change one localized rendered region outside the accepted nuisance mask in two independent localizer processes?
environment: PC auto-hardware derived-build route; four fresh runtime arms completed and closed cleanly
binary_sha256: 1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f
evidence:
  - reimplementation/ablpc/r2i_replicated_face8_localizer.py
  - scripts/r2i-create-replicated-face8-localizers.py
  - scripts/r2i-compare-replicated-face8-localizer.py
  - scripts/r2i-run-replicated-face8-localizer.py
  - tests/test_r2i_replicated_face8_localizer.py
  - work/copies/EXP-20260819-007/evidence/comparison/inconclusive/replicated-face8-localizer-001/result.json
tags:
  - reverse-engineering
  - pc
  - level01
  - terrain
  - runtime-planned
---

# EXP-20260819-007 - R2i Anthill replicated face-8 localizer

## Question

At the exact auto-hardware PC build and fixed live-grid view, does independently applying the exact face-8 topology mutation twice produce the same localized rendered change outside the nuisance mask accepted by [[EXP-20260819-006 - R2h Anthill D3 combined-mask holdout]]?

This is a derived-build localization experiment. It is not a ground, terrain, collision, material, world-coordinate, retail-executable, or one-byte-candidate experiment.

## Authorization boundary

- No EXP-007 localizer DAT, stage, evidence packet, or comparison result exists while this note is `planned`.
- The argument-free creator and runner perform prelaunch work-copy DAT writes. They must not run without fresh explicit user authorization covering both independently created DATs.
- The only planned process-memory access is one read-only four-byte Level01 index read at `0x00861C84` in each of the four arms before title Return.
- No runtime/debugger memory write, SIGSTOP/SIGCONT, stopped-view read, one-byte candidate, or later arm is authorized or reachable.
- The accepted EXP-006 authorization is consumed and does not authorize this packet.

## Frozen source identities

| Item | Exact identity |
|---|---|
| Executed auto-hardware PC build | SHA-256 `1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f` |
| Retail Level01 DAT | SHA-256 `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53` |
| EXP-005 diagnostic | SHA-256 `1640615be9df20d640dab77a740ce2221d822dba3c94354616ac3e42f857a283` |
| Accepted nuisance mask PNG | SHA-256 `ed8f43e54597a6d0f5d25bdd9c381319b1ed62bdededd4a0d28c4a67ff838c50` |
| Decoded nuisance-mask bytes | SHA-256 `2a07565016efd050129e7d53b9f71942b2503cec8fffc7cbc592e0d619373cb6`; 92,480 pixels |
| Frozen D1 reference PNG | SHA-256 `05f5691cab126962715d94857fd5085f7013353b3982a7d6e9d350215506ad1c` |
| Frozen D1 reference RGB | SHA-256 `2ea6564339c406cbcd92ca32faaf4e6c1b177119939aee569f0cfc1223b9d26c` |
| Accepted EXP-006 result JSON | SHA-256 `3fe541dfd9973ce1238f603e3fafb28834749db7530f2e27db6efb09e2bc0c19` |

The preflight validates every identity above before localizer creation and again before and after comparison. EXP-005 remains aggregate-rejected. The mask may not be regenerated, widened, selected, registered, normalized, or adapted from any EXP-007 arm.

## Exact localizer mutation

Both L1 and L2 start from separate fresh reads of the exact retail DAT and use only `LevelDat.set_static_mesh_face_vertex_byte_offsets` with these guards:

| Field | Frozen value |
|---|---|
| Section / record | primary / 81 |
| Object / geometry | `0x4860` / `0x188CC` |
| Face | 8 at record `0x18D38` |
| Original tuple | `(300,312,264,324)` |
| Replacement tuple | `(300,300,300,300)` |
| Physical changes | `0x18D3A: 0x38->0x2C`; `0x18D3C: 0x08->0x2C`; `0x18D3E: 0x44->0x2C` |
| Derived DAT | SHA-256 `9942e252028b198dd0c16c6e45a1584620244f7dd9d9aeabe9a53bc04bd11bfd` |

L1 and L2 are first built under one provisional pair directory. Each requires its own receipt, separate fresh retail read, reconstructive reparse, exact three-byte full-file diff, and preserved size. The pair is byte-compared, receives one aggregate receipt, and only then publishes through one atomic pair-directory rename. Any partial creation or validation failure remains under `artifacts/pending` with an aggregate disposition; no arm may launch. The two arm receipts differ by arm and final publication path even though their DAT bytes match. No one-byte vertex candidate is created.

The argument-free full runner is the authoritative end-to-end command. If the separately exposed argument-free creator is used first under the same authorization, the runner consumes and revalidates that exact accepted pair; it never silently recreates or replaces an accepted pair. Accepted and pending pair namespaces may not coexist. A corrupt accepted pair is demoted to pending with an aggregate disposition before any arm can launch. If that filesystem rename fails, the accepted namespace remains visibly questionable and a separate pending ambiguity disposition is retained, still blocking launch and clean classification. Successful publication has an explicit accepted aggregate pair disposition; reused, ambiguous, corrupt, or pending namespaces reject before launch.

Localizer DAT installation records `attempted`, temporary verification, replacement, final verification, and completion separately. A failed copy or verification cannot carry the completed `DAT_write` receipt. An accepted localizer arm requires exactly one `stage-dat-install-receipt.json` equal to the frozen completed write; controls prohibit every `stage-dat-install*` file and extra localizer install files reject.

## Fixed arms and acquisition

Run order is exactly `C1 -> L1 -> L2 -> C2`.

| Arm | DAT | Role |
|---|---|---|
| C1 | retail `786b...8b53` | leading control |
| L1 | independently created `9942...1bfd` | first face-8 localizer |
| L2 | independently created `9942...1bfd` | replication localizer |
| C2 | retail `786b...8b53` | trailing control |

Every arm uses a fresh stage, evidence namespace, PID/start tuple, complete six-marker Direct3D gate, chronological Right/Return/Return navigation, one authorized read-only level-index read, exact Level01/title gates, and the fixed live 121-frame grid `t0+3.300+0.200*i`, `i=0..120`. Every arm must close with a clear audit and retail `R:` restoration before the next arm starts. A cleanup or quarantine uncertainty stays pending.

Controls require the exact established camera-control crop hashes on every frame. Localizers record those crops but do not require control-derived crop equality because face 8 has not been proven crop-insensitive; intended localizer pixels must not be censored by the acquisition gate.

## Frozen comparator

1. Rebind every arm's 121 PNG and decoded-RGB hashes before analysis and after comparison.
2. Require both controls to equal the frozen D1 RGB reference at every eligible pixel and timestamp outside the accepted mask. One mismatch makes the set inconclusive before localizer promotion.
3. Require L1 and L2 to be decoded-RGB identical at every corresponding eligible pixel and timestamp outside the mask. Equal masks alone are insufficient.
4. Build separate L1 and L2 per-frame outside-mask difference masks against D1 and a separate L1/L2 disagreement mask for every timestamp, plus combined union, both-arm/all-time intersection, static-core, component, bounds, and overlay evidence. Retain all 363 per-frame masks and all output hashes.
5. Define the static core as pixels whose localizer RGB is constant across every timestamp and both localizer processes and differs from D1.
6. Require a nonempty static core that is one 8-connected component of at least 25 pixels.
7. Require exactly one union component of at least 25 pixels. Its dominant component must contain the static core and account for at least 75% of all union pixels.
8. Require the union to cover at most 5% of 640x480. This successor guard is informed by the prior distributed 6.0586% failure; it is not a terrain-size fact.
9. Record control and localizer inside-mask mismatch counts and binary observation masks separately by arm and frame. They are nondiscriminating and cannot support acceptance.

No frame hunting, phase rotation, image registration, normalization, mask adaptation, favorable component selection, or threshold change is permitted after an arm starts.

## Outcomes

| Observation | Disposition |
|---|---|
| All lifecycle, provenance, control, replication, static-core, component, dominance, and coverage gates pass | `accepted-replicated-face8-localizer` |
| Zero effect, mask-contained effect, control mismatch, L1/L2 disagreement, distributed/global effect, component failure, timing failure, or scientific gate failure | `inconclusive-replicated-face8-localizer`; no no-effect claim |
| Cleanup, quarantine, or publication state is uncertain | pending |

## Accepted-claim ceiling

A pass supports only: at auto-hardware PC build `1e1d...c41f`, the exact guarded Level01 face-8 tuple mutation reproducibly changes one localized rendered region outside the frozen nuisance mask in this view and finite grid.

It does not establish that the region is ground or terrain, establish collision/material/world-coordinate semantics, establish authoritative retail-executable behavior, reject type `0x41`, or authorize the one-byte candidate. The complete packet must be documented, committed, and James-accepted before any separately preregistered successor is considered.

## Offline implementation receipt

- Module: `reimplementation/ablpc/r2i_replicated_face8_localizer.py`.
- Argument-free creator, comparator, and full runner: `scripts/r2i-*.py`.
- Regression suite: `tests/test_r2i_replicated_face8_localizer.py` plus the shared live-grid suites. It covers atomic pair creation and partial failure, a real retained-packet transformation through the shared localizer validator, install interruption/forgery, source and frame rebinding, separate comparison publication, scientific quarantine, cleanup uncertainty, and quarantine failure.
- Correction result after the third hard-truth audit: focused R2i suite `33 passed`; full `make check` `1,418 passed`; Vault lint `0 errors`; tracked-file audit `0 violations`.
- At the accepted pre-runtime commit, all production EXP-007 artifact, stage, evidence, and comparison paths were absent.
- No DAT, game process, runtime read, signal, localizer arm, or candidate was created while preparing this packet.

## Authorized runtime result

The user then authorized exactly two independent work-copy DAT creations, `C1 -> L1 -> L2 -> C2`, and one read-only four-byte Level01 index read at `0x00861C84` per arm. Runtime/debugger writes, `SIGSTOP`/`SIGCONT`, the one-byte candidate, and successor arms remained prohibited. The authorization is consumed.

The accepted static pair remains under `work/copies/EXP-20260819-007/artifacts/accepted/replicated-face8-pair-001/`. Both independent retail reads produced byte-identical DAT SHA-256 `9942e252028b198dd0c16c6e45a1584620244f7dd9d9aeabe9a53bc04bd11bfd`. Pair receipt SHA-256 is `e4d8ea7d8d176fdecc41ed40ae34848fa7244c2cc68207cf688fc817beaa87bf`; pair disposition SHA-256 is `fce6bcab78dcc1d0ae6e831b83e4c186031da7306cf57fe0d8e1cccf2a95485e`.

All four fresh arms passed the build, DAT, Direct3D, Anthill Level01 index `1`, 121-capture, input/read, and lifecycle gates before aggregate comparison. Their distinct process identities were:

| Arm | PID | Start ticks | Process group |
|---|---:|---:|---:|
| C1 | `1175620` | `20833305` | `1175362` |
| L1 | `1176921` | `20844491` | `1176665` |
| L2 | `1178274` | `20855740` | `1178019` |
| C2 | `1179473` | `20867084` | `1179202` |

The aggregate result at `work/copies/EXP-20260819-007/evidence/comparison/inconclusive/replicated-face8-localizer-001/result.json` has SHA-256 `723e03ed43d6133e65df25655954ba779767800b3b010f603a0b2d482e25a309` and is `inconclusive-replicated-face8-localizer`:

| Gate | Retained result |
|---|---|
| Control outside-mask mismatches | `251`; C1 `0`; C2 frame 25 `2`, frame 35 `228`, frame 105 `19`, frame 108 `2` |
| L1/L2 outside-mask disagreement | `228`, all at frame 35 |
| Outside-mask union | `228` pixels, fraction `0.0007421875` |
| Intersection / static core | `0` / `0` pixels |
| Rejection reasons | `control-outside-mask-mismatch`; `localizer-rgb-disagreement`; `static-core-gate-failed` |

L1 had zero outside-mask differences. L2's only outside-mask difference was frame 35. Its exact 228-pixel positions and RGB values were independently reproduced by C2 frame 35; the L2 mask, L1/L2 disagreement mask, and aggregate union share PNG SHA-256 `29e5b5e4ab259cb67200657598ce6c853155c40100350563ed2db6608bf4eb1b`. This is control-reproduced nuisance, not replicated face-8 localization evidence. It also proves the accepted EXP-006 mask only passed its single D3 holdout and is not exhaustive across fresh controls.

The four runtime arms were quarantined under `evidence/rejected/` only because the aggregate scientific gate failed. Every arm retained its original accepted lifecycle disposition, null cleanup error, retail `R:` restoration, and prohibited-operation boundary. The final and independent session audits were clean. James accepted the procedural run and this inconclusive interpretation.

No face-8 visibility, terrain, causality, or no-effect conclusion follows. R2 remains open and the one-byte candidate remains unauthorized. A future mask revision may use only an offline, control-only diagnostic; it cannot retroactively rescue this experiment and must pass a fresh independently authorized control holdout before any separately authorized localizer successor.

## Links

- [[EXP-20260819-006 - R2h Anthill D3 combined-mask holdout]]
- [[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[PC LEVEL DAT static mesh]]
- [[Known Unknowns]]
