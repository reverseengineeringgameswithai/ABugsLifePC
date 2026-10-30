---
type: session
date: 2026-08-21
agent: Codex
topic: P0A-AH-001 accepted preflight and pending pre-collection runtime
status: pending
tags:
  - session
  - reverse-engineering
  - level01
  - terrain
---

# 2026-08-21 0022 - Codex - P0A pending pre-collection runtime

## Outcome

James returned **ACCEPT** on exact pre-run commit `8437c0a4b5630ba59bcb7601a67066074e02da06`
/ tree `532419060f1b5d5e4c4e7ed65e78bc2f7bf3acd9`, including 207/207
analyzer/packet tests, native X, and 1852/1852 full tests. The immediate
pre-launch session audit was clean. The user-authorized exact argument-free
`scripts/r2p-run-passive-lifecycle.py` invocation then launched once, consuming
P0A-AH-001. No process-memory read/write, debugger, signal, screenshot, DAT,
localizer, candidate, or R2o action occurred.

Hardware and Level Select gates passed. Focused `Right` and `Return` receipts
completed, but the retained log loaded level07 assets rather than Level01 and
reached `ROUTINE : Start ClearLoadScreen.` The Level01 gate timed out before
`collection.json`, so the run contains zero passive task-lifecycle samples and
no scientific lifecycle result.

Guarded `Alt_L+F4` delivery completed on the retained focused loading window,
but the runtime survived 89 bounded clearance polls. The executor correctly
used no signal fallback, left the stage/evidence pending, and did not restore
`R:`. A fresh read-only audit reports seven live Gamescope/Wine processes and
private sink
`ablpc_mute_1834769`; after wrapper exit they appear unattributed. The earlier
clearance receipt and later audit are distinct censuses: clearance records PIDs
`1834769`, `1834786`, `1834812`, `1834935`, `1834937`, and `1835030`; the
post-wrapper audit records `1834786`, `1834812`, `1834935`, `1834939`,
`1834955`, `1834980`, and `1835030`. They were recorded and not terminated.
The retained audit's raw field contains its census, but `parsed` is null with
`JSONDecodeError: Extra data: line 142 column 1` because Make stderr followed
the JSON stdout. The seven-process statement is independently supported by the
fresh read-only audit, not by a parsed retained receipt.

Runtime identity records Xwayland `(1834812,30382270)`, but both Xlib socket
`SO_PEERCRED` receipts name `(1834786,30382246)`, identified by the audit as
Gamescope. The accepted validator expected both peers to equal Xwayland and
would have rejected this packet had it reached terminal validation. The native
fixture therefore did not reproduce real Gamescope socket provenance; any
successor must resolve and re-freeze that binding.

Pending disposition SHA-256 `ca2dfaa3...0d80` records the Level01 timeout,
normal-close failure, false baseline restoration, and null prohibited-action
fields. Final-log receipt-file SHA-256 is `86e7a028...ea32`; normal-close receipt is
`e3eeffa4...e418`; clearance receipt is `e3ec4aa2...5fb4`. Here
`86e7a028...ea32` hashes the `bugs-final-log.json` receipt file; the receipt's
embedded exact log-text SHA-256 is `4a141868...cb92`. No terminal evidence
identity exists.

## Boundary

P0A-AH-001 is consumed and pending. No close retry, signal cleanup, `R:`
restoration, publication, or second arm is authorized. The selected-level
contradiction and surviving loading process are procedural findings only. No
task-lifecycle, collision, terrain, material, visibility, causality, or retail
claim follows. The socket-provenance mismatch and unparsed retained audit are
additional procedural findings. Any cleanup/recovery decision and any
corrected successor need fresh explicit authorization and a new frozen packet.

## Links

- [[EXP-20260820-005 - R2p task lifecycle diagnostic]]
- [[Decision Log#DEC-188 - Preserve P0A-AH-001 as pending after pre-collection route and close failures|DEC-188]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Known Unknowns#KU-079 - The render-geometry command grammar (the LEVEL.DAT draw-command stream)|KU-079]]
