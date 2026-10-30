---
type: session
date: 2026-08-19
updated: 2026-08-19
agent: Codex
status: complete
tags:
  - reverse-engineering
  - level01
  - terrain
  - offline
---

# 2026-08-19 2048 - Codex - R2i replicated localizer packet

## Work

Prepared [[EXP-20260819-007 - R2i Anthill replicated face-8 localizer]] as the offline successor to the accepted finite-grid nuisance-mask holdout. James required `C1/L1/L2/C2`, not `C1/L/C2`, so the packet independently builds two byte-identical guarded face-8 DATs from separate retail reads and requires exact decoded-RGB replication across both localizer processes.

The live-grid executor reuses the exact auto-hardware, Anthill Level01, timing, renderer, read-only index, lifecycle, and provenance gates. Controls must reproduce every eligible D1 pixel. L1/L2 now publish as one atomic pair after two separate retail reads and byte comparison. The localizer comparator requires one at-least-25-pixel static core, one dominant localized component, at least 75% dominance, and at most 5% total union coverage. L1, L2, and disagreement masks are retained separately for all timestamps; inside-mask counts are retained separately by arm and frame but remain nondiscriminating.

## Boundary

No production EXP-007 path, DAT, process, read, signal, or runtime evidence was created. The creator and runner remain blocked pending fresh authorization that explicitly covers two independent work-copy DAT publications and four read-only-index runtime arms. No runtime/debugger memory write, SIGSTOP/SIGCONT, one-byte candidate, or successor is included.

James's first audit rejected the initial implementation because pair publication, partial-failure classification, production-path test durability, separate comparison evidence, and lifecycle regression depth were incomplete. The first correction added reusable freshness guards, aggregate pending pair disposition, real retained-packet validation with the custom DAT/install receipt, install interruption and forgery tests, source/frame mutation tests, successful comparison publication, and pending/quarantine regressions.

James's second audit found false completed-write state on failed installation, accepted/pending pair ambiguity, corrupt accepted-pair misclassification, an overbroad localizer install-file allowance, and a missing accepted aggregate pair state. The second correction records install progress explicitly, requires an exact one-file accepted install receipt, blocks pair-state coexistence, demotes corrupt accepted pairs to pending, and publishes an accepted aggregate disposition only after successful pair publication.

James's third audit isolated the post-publication case where the filesystem itself refuses accepted-to-pending demotion. The final correction retains a separate pending ambiguity disposition while leaving the questionable accepted namespace visible, preventing both launch and inconclusive classification. The focused suite passed 33 tests; full `make check` passed 1,418 tests with zero Vault-lint errors and zero tracked-file-audit violations.

## Links

- [[EXP-20260819-007 - R2i Anthill replicated face-8 localizer]]
- [[EXP-20260819-006 - R2h Anthill D3 combined-mask holdout]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[PC LEVEL DAT static mesh]]
- [[Known Unknowns]]
