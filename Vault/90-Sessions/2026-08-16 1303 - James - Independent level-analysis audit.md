---
type: session
date: 2026-08-16
agent: James
status: worker-complete
tags: [session, re/static, re/audit, re/gameplay]
---

# Independent level-analysis audit

> [!correction] EXP-167 later rejects this audit's promotion of the verified
> direct/static reference census into global gate-family exclusivity. The
> roster, 22-reference classification, dispatcher, and known structure
> bindings survive; indirect/aliased/cached absence does not.

## Goal

Adversarially audit two committed static-analysis packets at HEAD
`5a265f1` — [[EXP-20260816-146 - Grain-gate level exclusivity static proof]]
and [[PC level roster and numbering]] — and return ACCEPT or REJECT from a
fresh offline context. No game launch.

## Verdict

**Original REJECT, upgraded to ACCEPT after correction** —
[[EXP-20260816-147 - Independent level-analysis audit]]. One specific,
isolated, easily-fixable defect: [[PC level roster and numbering]] cited the
carousel position-counter as `word [0x00059AF8]` (frontmatter + two body
lines), but the consumer at `0x00414766` reads `word [0x00599AF8]` (raw
bytes `0f bf 05 f8 9a 59 00`). `0x00059AF8` is below the image base and
unmapped, so it was unreproducible — a dropped-hex-digit transcription
error. The worker replaced all three occurrences with `0x00599AF8`, fixed
the propagated copy in
[[2026-08-16 1237 - Claude - grain gate level exclusivity]], and added the
recommended researcher-provided-names clarification. Re-verified against the
binary and vault-lint (0 errors); defect resolved, verdict upgraded to
**ACCEPT**.

## What verified cleanly

- Rehashed `bugs.exe` → `97c95ba5…27b878` (matches).
- Grain byte `0x0059D9B1`: exactly 22 code refs, classification fair; only
  `0x00432F0C` (Tunnels) and `0x004337D6` (City) are positional
  grain-vs-requirement gates. Level-8 `0x00436308` compares grain to stored
  `0x0059F404` (counter-change); level-14 `0x0043A911` is a `cmp <0x28`
  event — neither a gate.
- Dispatcher `0x00418780`: 17-entry jump table; all 17 thunk targets match
  the note; only L3→`0x00432B30`, only L4→`0x00433900`→`0x00433790`.
- Gate structures bind L3/L4 only: Tunnels table `0x004DA9C8` (5 refs) /
  template `0x004DAA80` (1 ref); City state `0x0059F020` (init `0x00433606`
  writes `-1`, plus 4 in-routine refs); City lookup `0x004338B0` = zero refs
  / all `0xCC`.
- Roster table `0x004C6A30` = `[17,1,3,2,6,10,11,4,5,14,7,12,13,9,8,15]` +
  `0xFFFFFFFF`; mapping arithmetic exact; City Entrance pos 7 → internal 4;
  direction unambiguous; carousel = `{17}∪{1..15}`, internal 16 the sole
  non-carousel slot.
- Overclaim caveats (training→17 unverified; internal 16 identity not
  claimed) present and honest; recommended a small clarification that level
  names are researcher-provided while only indices are static.
- Hygiene: git clean at `5a265f1`; `originals/` only `.gitkeep`;
  `make check` = Vault 424/0/0, M4 valid, 610 passed, tracked-file audit 0.

## Durable changes

- New: [[EXP-20260816-147 - Independent level-analysis audit]] (this
  audit), this session note, Session Index and Experiments MOC entries.
- Did **not** edit Current State or Known Unknowns — the worker reconciles
  after the verdict.

## Next

- Worker corrects `0x00059AF8` → `0x00599AF8` (3 occurrences + propagated
  session-note copy) and resubmits; a single-edit re-check suffices.
