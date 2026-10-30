---
type: session
created: 2026-08-20
updated: 2026-08-20
agent: Codex
status: complete
---

# 2026-08-20 0808 - Codex - R2n static state anchors

## Scope

Continued the terrain-authoring R2 agenda after R2m closed fixed wall-clock
alignment. This session was offline/static only.

## Work

- Rechecked the accepted PC view chain against retail Ghidra search results
  and native disassembly.
- Proved that the auto-hardware patch preserves the cited addresses, bytes,
  section layout, and data locators.
- Bounded six exact equality candidates at upstream PC `0x00414585` and
  generated-view PC `0x0041458F`.
- Limited `0x005BDBAC` to 18 bytes despite its physical 32-byte copy and kept
  `0x005BDB9C/12` optional/redundant.
- Excluded repeatedly clobbered `0x0063E888` transform scratch.
- Corrected the stale claim that `0x00405FE0` receives already transformed
  inputs; it performs the signed fixed-point transform locally.

## Boundary

No game, Wine, Gamescope, debugger, process-memory access, signal, input, DAT
creation/write, localizer, or candidate action occurred. The packet authorizes
no runtime. A successor requires a separately committed read-only protocol,
James acceptance, and fresh explicit user authorization.

## Links

- [[EXP-20260820-003 - R2n PC state-equivalence read candidates]]
- [[EXP-20260820-002 - R2m offline cross-time correspondence diagnostic]]
- [[PC camera view-transform chain]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
