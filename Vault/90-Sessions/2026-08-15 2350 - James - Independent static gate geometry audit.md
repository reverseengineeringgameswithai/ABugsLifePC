---
type: session
date: 2026-08-15
agent: James
status: accepted
tags: [session, re/audit, re/static, re/gameplay]
---

# Independent static gate geometry audit

## Goal

Treat EXP-139's static grain-gate geometry packet as hypotheses and
independently attack every claim from a fresh context: rehash, raw-byte
re-verification, independent disassembly, arithmetic recomputation, overlay
diff safety review, gates, and overclaim review — with no runtime process
and no target write.

## Work completed

- Re-read the startup authority chain, the 2026-08-15 grain-gate sections of
  Current State, EXP-136/137/138/139, the research/mod notes, KU-060, and the
  three function dossiers.
- Rehashed the retail work copy to the exact
  `97c95ba5...a27b878` and confirmed the `.text` `VA - 0x400C00` relation
  from the PE section table.
- Re-read every cited file-offset byte string raw (`0x32D2F`, `0x32BEF`,
  `0x15980`, `0x322EC`, `0x322F8`, `0x32349`, `0x32385`, `0x3239D`,
  `0x323EB`, `0x32417`, `0x3241E`) and independently disassembled
  `0x00433900`, `0x00433790`, `0x00416580`, and the `0x00432B30` loop.
- Attacked the argument order and X/Z assignment specifically: traced exact
  stack offsets for the local-struct stores, ran a deliberate swap test that
  contradicts the accepted EXP-137 receipts (377-shifted dx; 4,933 vs the
  receipt's exact 4,993), and confirmed a binary-wide census finds exactly
  the three claimed call sites and no other caller of `0x00433790`.
- Recomputed all cross-check arithmetic including sar-vs-Python-shift
  equivalence on negatives: 4993 / 4289 / 7177 against the receipt
  coordinates, animation `-128/+128 -> -1024/+1024` from slots 2/3 deltas
  `-32/+32`, and the `0x1068 - 18*140 = 0x690` decay.
- Diffed the existing accepted-profile build against retail: exactly 46
  changed bytes in the pinned mod ranges, zero overlap with any
  geometry-bearing range.
- Audited the overlay 1.3.0 diff: no write/attach path, two-hash boundary
  fails closed, short reads raise, constants match evidence, unknown-hash /
  wrong-level / tie / negative-shift adversarial cases handled, default
  readout unchanged without `--gates`.
- Ran the gates: overlay suite 14 passed; `make check` (Vault 403/0/0, five
  M4 anchors, 596 tests, tracked-file audit 0); `git diff --check` clean;
  hygiene confirmed (nothing staged, no game-bearing bytes tracked,
  `originals/` untouched, no EXP-139 runtime artifacts anywhere).
- Reviewed all touched Vault notes for overclaim: gates 1/2 stay
  single-evidence-form static, KU-060 stays open, M3 stays Complete, static
  centers are nowhere presented as walkable or teleport targets.

## Result

**ACCEPT.** [[EXP-20260815-140 - Independent static gate geometry and overlay audit]]
records the full procedure. Two minor non-defect wording observations are
noted there (grain-compare cited at its load address; the INT3 pad is longer
than the 12 bytes used). Current State and Known Unknowns reconciliation is
left to the worker per the audit protocol.

## Validation

- executable rehash: exact retail; profile build rehash: exact accepted hash;
- byte pins: all eleven cited offsets re-read identical; call census: 3/3;
- arithmetic: all recomputed values match the packet and receipts;
- overlay suite: 14 passed; complete `make check`: Vault 403/0/0, five M4
  anchors, 596 tests, tracked-file audit 0; `git diff --check`: clean;
- vault lint re-run after writing this audit's notes: 0 errors.
