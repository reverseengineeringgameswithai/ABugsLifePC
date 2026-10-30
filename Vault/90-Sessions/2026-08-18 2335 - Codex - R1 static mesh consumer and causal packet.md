---
type: session
date: 2026-08-18
agent: Codex
status: complete
tags:
  - session
  - re/static
  - re/file-format
  - re/rendering
---

# R1 static mesh consumer and causal packet

## Goal

Continue [[New-level authoring roadmap (terrain, collision, materials)]] from
R0, reconcile its stale R1/R2 labels, and advance as far as possible without
implying authorization for the runtime causal write.

## Work

- Read the mandated [[START HERE]] orientation, current authorities, policy,
  relevant MOCs, R0 evidence, and Ghidra-export caveats.
- Independently traced retail `FUN_004498f0` to `FUN_0045a7f0` into the exact
  positive-count vertex/tag/face consumer using Ghidra only as a search surface
  and fresh raw `objdump` as instruction evidence.
- Added conservative static-mesh dataclasses and bounds-checked parsing to
  `reimplementation/ablpc/level_dat.py`, including reconstructive encoding and
  an expected-value-guarded component edit.
- Selected retail Level03 primary record 167 as an exact R2 candidate without
  writing or launching it. The planned `0xc50a: -891 to 1157` transform changes
  physical byte `0xc50b` only and predicts derived SHA-256 `492a53e8...adf80`.
- Reconciled the authoring roadmap to R0 discovery, R1 offline decode/tooling,
  then R2 causal runtime, preserving all runtime and semantic unknowns.

## Evidence and status

[[EXP-20260818-007 - R1 static mesh consumer, round trip, and causal candidate]]
is the bounded packet. [[PC LEVEL DAT static mesh]] is the format dossier.
`KU-079` remains open because visible-ground identity, world scale, colour/UV,
tag semantics, and Gate C remain unresolved.

No game, Wine, Gamescope, debugger, emulator, audio sink, runtime memory write,
or derived game file was launched or created in this session.

## Validation

- The 21-DAT retail corpus walk reconstructed all 2,543 type-`0x41` payloads
  byte-for-byte and validated 146,030 face references.
- `make check` passed after the implementation and Vault updates.
- No game process was launched and no runtime or file-write experiment was
  attempted.

## Next

Obtain fresh explicit user authorization for the exact EXP-007 R2 control and
candidate arms. Before launch, run `make session-audit`; require all six
hardware Direct3D markers; use only a retail-derived copy under `work/`; retain
the compare-before-write receipt and visual evidence; close the owned session;
and run the post-close audit.
