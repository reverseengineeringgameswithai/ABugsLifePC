---
type: experiment
id: EXP-20260820-001
title: R2l fresh replicated face8 localizer
date: 2026-08-20
environment: PC Wine/Gamescope auto-hardware derived build; authorized four-arm runtime packet
binary_sha256: 1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f
question: Does the independently derived face-8 topology mutation reproducibly change one localized rendered region outside the frozen nuisance mask?
status: completed
result: Procedurally valid C1/L1/L2/C2 run; scientifically inconclusive because L1 and L2 did not replicate outside the fixed mask
created: 2026-08-20
updated: 2026-08-20
tags:
  - experiment
  - pc
  - anthill
  - level01
  - static-mesh
  - causal
---

# EXP-20260820-001 - R2l fresh replicated face8 localizer

## Question

At the exact auto-hardware PC build and fixed Anthill Level01 title-view grid, does independently applying the exact face-8 topology mutation to two separately read retail DAT copies reproducibly change one localized rendered region outside the accepted finite nuisance mask?

This packet is an offline preregistration. It creates no production DAT, launches no game process, and consumes no runtime authorization.

## Why this is fresh

[[EXP-20260819-007 - R2i Anthill replicated face-8 localizer]] was procedurally valid but inconclusive. Its arms, stages, artifacts, process identities, and comparison outputs are provenance only and are prohibited from reuse. [[EXP-20260819-009 - R2k Anthill D4 control-trained mask holdout]] accepted a finite, control-trained mask against a fresh D4 holdout; it did not retroactively rescue EXP-007 or establish exhaustive nuisance coverage.

## Frozen sources

- Executed auto-hardware build SHA-256: `1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`.
- Retail executable transform source SHA-256: `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Retail Anthill Level01 DAT SHA-256: `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`.
- D1 reference PNG/RGB SHA-256: `05f5691cab126962715d94857fd5085f7013353b3982a7d6e9d350215506ad1c` / `2ea6564339c406cbcd92ca32faaf4e6c1b177119939aee569f0cfc1223b9d26c`.
- EXP-008 diagnostic SHA-256: `83931a8ae5158a3eb6478ddb664894fe96e705805dc13f889f5363a9d8cca9a5`, diagnostic provenance only.
- Accepted D4 result: `work/copies/EXP-20260819-009/evidence/holdout/accepted/control-trained-mask-d4-holdout-001/result.json`, SHA-256 `bf2b46258ca92d654f993c9607f4bd5e453aac818dfb59e248e0ac01173569d8`.
- Accepted D4 disposition: SHA-256 `cc4fdc2cbb91ebbcdc2f4c8999449b19268e9a76e0112249f27d73529c2e1ebe`; process instance `1267141/21477936/1266881`.
- Frozen nuisance mask PNG/decoded-byte SHA-256: `b855df0ac67554737ae990bcb5fdbb14a132eae32af6bddf292c07dba193c936` / `9ff27caa7842b9047c9eebf633f9d280dd820841b81eba5fd491845a66fb71ba`; population `93,445` pixels.
- EXP-007 aggregate: `work/copies/EXP-20260819-007/evidence/comparison/inconclusive/replicated-face8-localizer-001/result.json`, SHA-256 `723e03ed43d6133e65df25655954ba779767800b3b010f603a0b2d482e25a309`.

Every source is validated before creation/run and again during comparison. The mask may not be regenerated, widened, aligned, normalized, or selected from these arms.

## Guarded localizer pair

Only a future explicit authorization may let the argument-free creator publish the pair. It must perform two independent reads of the retail DAT and produce two byte-identical derived copies atomically.

- Geometry record: `0x188CC`.
- Face-8 record: `0x18D38`.
- Original tuple: `(300,312,264,324)`.
- Replacement tuple: `(300,300,300,300)`.
- Only physical byte changes: `0x18D3A 38->2C`, `0x18D3C 08->2C`, `0x18D3E 44->2C`.
- File size remains `332824` bytes.
- Each derived DAT SHA-256 must be `9942e252028b198dd0c16c6e45a1584620244f7dd9d9aeabe9a53bc04bd11bfd`.
- Bounds, arity, 12-byte alignment, index range, object/geometry/face identity, exact old tuple, reconstructive reparse, byte-local diff, source rehash, and pair independence are mandatory.
- A partial pair is quarantined. Game data remains under ignored `work/` paths and must never be committed.

## Frozen future sequence

The only runtime order is `C1 -> post-close audit -> L1 -> post-close audit -> L2 -> post-close audit -> C2 -> post-close audit`. Each arm also needs its own clean immediate pre-launch audit.

- All four arms use fresh stages, evidence namespaces, and process instances distinct from D1/D2/D3/D4 and every EXP-007 arm.
- C1 and C2 install retail Level01 DAT and have no localizer-install receipt.
- L1 and L2 install their corresponding newly derived DAT and each have exactly one complete install receipt.
- Every arm uses the identical pinned auto-hardware build, launcher, hardware six-marker gate, navigation, title/index gate, crops, and fixed 121-frame grid.
- The only permitted process-memory operation is one read-only four-byte Level01 index read at `0x00861C84` per arm.
- Runtime/debugger writes, SIGSTOP/SIGCONT, stopped view reads, the one-byte candidate, adaptive capture, and successor arms are prohibited.
- Any scientific failure with clear cleanup/restoration is quarantined as inconclusive. Cleanup, restoration, quarantine, or publication uncertainty remains pending.

## Comparator

For each of 121 timestamps and every pixel outside the frozen mask:

1. Require C1 and C2 to equal the frozen D1 decoded RGB everywhere. Any control mismatch is inconclusive.
2. Require L1 and L2 decoded RGB to equal one another everywhere. Any localizer disagreement is inconclusive.
3. Define replicated change only where `L1 == L2 != D1`.
4. Retain inside-mask differences as nondiscriminating evidence; they cannot support acceptance.
5. Rehash each PNG before decode and after decode in both comparison passes.

A positive automated localization requires all of:

- At least 25 pixels in the intersection across all 121 replicated masks.
- Exactly one union component with at least 25 pixels.
- The stricter constant-RGB static core is retained separately; if nonempty, the dominant component must contain it. The core does not replace the 25-pixel all-frame intersection gate.
- Dominant-component fraction at least `0.75`.
- Union coverage at most `0.05` of the frame.

Zero outside-mask change, fragmentation, control mismatch, L1/L2 disagreement, missing static core, threshold failure, crash, load rejection, or diffuse change is inconclusive. No result automatically authorizes a candidate.

## Evidence outputs

The comparator retains separate C1/C2 control mismatch, L1/L2 disagreement, replicated union, all-frame static core, inside-mask, connected-component, overlay, and source/output hash artifacts. Accepted comparison publication is atomic; partial or unclear publication remains pending.

## Claim ceiling

A positive result would support only:

> At auto-hardware PC build `1e1d...c41f`, the guarded Anthill Level01 face-8 tuple mutation reproducibly changes this localized rendered region in the frozen title-view grid.

It would not identify terrain, ground, collision, materials, world axes/scale, or authoritative retail-executable behavior. A later retail-executable intervention remains required for retail R2.

## Authorization boundary

Before production creation or launch, obtain a fresh explicit authorization for exactly the two work-copy DAT creations, C1/L1/L2/C2, and one read-only `(0x00861C84,4)` read per arm. No prior authorization carries forward.

## Implementation

- `reimplementation/ablpc/r2l_fresh_replicated_face8_localizer.py`
- `scripts/r2l-create-fresh-replicated-face8-localizers.py`
- `scripts/r2l-run-fresh-replicated-face8-localizer.py`
- `scripts/r2l-compare-fresh-replicated-face8-localizer.py`
- `tests/test_r2l_fresh_replicated_face8_localizer.py`

## Authorized execution result

The user authorized exactly the two work-copy creations, `C1 -> L1 -> L2 -> C2`, and one read-only four-byte Level01 index read at `0x00861C84` per arm. The authorization is consumed.

### Pair

- L1 and L2 were produced from separate retail reads and independently receipted.
- Both derived DATs are byte-identical at SHA-256 `9942e252028b198dd0c16c6e45a1584620244f7dd9d9aeabe9a53bc04bd11bfd`.
- Each preserves size `332824`, reparses to `(300,300,300,300)`, and differs only at `0x18D3A`, `0x18D3C`, and `0x18D3E` as preregistered.
- Creator receipt hashes used by the installs are `5806baaa3bdad604e0bd3aaad26f3048a8874f4331d15cecd1bb5a4b9f242928` for L1 and `295162d8cb181495ef944713a00596ce6c6ce05f1cc18345e3ea61d3da302432` for L2.
- Pair receipt: `work/copies/EXP-20260820-001/artifacts/accepted/fresh-replicated-face8-pair-001/pair-receipt.json`, SHA-256 `23087ee71d4e110a57f645f11a424b7fd4b9b2578a0cf85221f0fc72ed5ea333`.
- Final pair disposition: `work/copies/EXP-20260820-001/artifacts/accepted/fresh-replicated-face8-pair-001/pair-disposition.json`, SHA-256 `050a555a751022bc8f42162fa3c10b0d87b84aafee2635d15016460c0a6badcd`.

### Arms and lifecycle

| Arm | Process instance `pid/start/pgid` | Level01 DAT | Install receipt |
|---|---|---|---|
| C1 | `1317721/21991916/1317463` | retail `786b7a96...8b53` | absent, as required |
| L1 | `1319195/22003005/1318935` | localizer `9942e252...11bfd` | one completed authorized work-copy install |
| L2 | `1320718/22014279/1320462` | localizer `9942e252...11bfd` | one completed authorized work-copy install |
| C2 | `1322063/22025767/1321802` | retail `786b7a96...8b53` | absent, as required |

All four arms passed the exact auto-hardware build identity, complete six-marker Direct3D gate with no software marker, CD/path identity, Anthill Level01 navigation/title gate, one read-only `(0x00861C84,4)` receipt with value `1`, exact `640x480` geometry, 121 captures from `t0+3.3` through `t0+27.3` at `0.2` seconds, source/hash/chronology guards, cleanup, retail `R:` restoration, and clear pre/post lifecycle audits. No runtime/debugger memory write or signal occurred. Controls made no DAT write; L1/L2 performed only the authorized prelaunch work-copy installs.

The aggregate predates scientific quarantine, so the final lifecycle dispositions are anchored separately:

- C1: `work/copies/EXP-20260820-001/evidence/rejected/C1-FRFL-AH-001/disposition.json`, SHA-256 `9b2a27254dc16ed020c864f00644ea70439f714564f003b0da8284845cbd079c`.
- L1: `work/copies/EXP-20260820-001/evidence/rejected/L1-FRFL-AH-001/disposition.json`, SHA-256 `c11a69208ce80fae16e15b6e0881532eda3f60e4a317aa55844b402bded3fe72`.
- L2: `work/copies/EXP-20260820-001/evidence/rejected/L2-FRFL-AH-001/disposition.json`, SHA-256 `331e77c87d1b7de3aa4d40292401b31d488c28a8af341507ec2c68e28830d285`.
- C2: `work/copies/EXP-20260820-001/evidence/rejected/C2-FRFL-AH-001/disposition.json`, SHA-256 `6345f34e8a833a8cb3367ad7f30f5b54e923bafd1858ba5de2c8052d770c066a`.

### Comparator

Retained aggregate: `work/copies/EXP-20260820-001/evidence/comparison/inconclusive/fresh-replicated-face8-localizer-001/result.json`, SHA-256 `60c38e6719a0768db1e9569542d75ceb8a8b6a8ef51fc67e8cc69b7895cf97fd`.

- All 484 arm PNG/RGB bindings and all 1,093 comparison PNG outputs rehash.
- C1/C2 outside-mask mismatch observations: `0`.
- L1/L2 corresponding-frame RGB disagreement observations outside the unchanged mask: `20,634,078`.
- Outside-mask union: `211,650` pixels, or `0.68896484375` of the frame.
- All-frame intersection: `0`; stricter static core: `0`.
- Large components: `3`; dominant fraction: `0.5379163713678242`.
- Failed gates: localizer replication, 25-pixel intersection, one-large-component, 0.75 dominance, and 0.05 coverage cap.

The comparator therefore emitted `inconclusive-replicated-face8-localizer`, no claim scope, and no candidate authorization. All four otherwise valid arms were quarantined under `evidence/rejected/` because the aggregate scientific gate failed; this is not a lifecycle rejection.

## Interpretation and next boundary

This packet establishes neither face-8 visibility nor a no-effect result. It supports no terrain, ground, collision, material, world, causal, or retail-executable conclusion. The face mutation may have changed rendering, but the two independently created copies did not reproduce a corresponding outside-mask state, so causal attribution is forbidden.

No rerun or successor arm is authorized. The minimum next step is offline-only: use the quarantined L1/L2 frames to build a preregistered cross-time correspondence matrix outside the unchanged mask, with separate camera-safe crop/state diagnostics. Do not widen the mask or promote this run. A future runtime packet is scientifically viable only if the offline diagnostic finds a unique reproducible state/phase correspondence; otherwise new read-only camera/player-state anchors must be preregistered before requesting authorization.

James independently reproduced the pair, all arm gates, 484 bindings, 1,093 outputs, and comparator metrics, and returned `ACCEPTED` for this procedural/inconclusive interpretation.

## Offline successor

[[EXP-20260820-002 - R2m offline cross-time correspondence diagnostic]] is the separately frozen, non-runtime attempt to determine whether exactly one fixed lag explains the L1/L2 state mismatch. It may not alter this result, widen the mask, or promote R2l.

R2m completed with no unique fixed lag and therefore did not rescue R2l. Fixed wall-clock alignment is nonviable; only independently justified read-only state anchors may support a future design.

## Links

- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Current State]]
- [[Known Unknowns]]
- [[Reverse Engineering MOC]]
- [[EXP-20260819-007 - R2i Anthill replicated face-8 localizer]]
- [[EXP-20260819-009 - R2k Anthill D4 control-trained mask holdout]]
