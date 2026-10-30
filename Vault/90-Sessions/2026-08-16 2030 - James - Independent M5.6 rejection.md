---
type: session
date: 2026-08-16
agent: James
status: rejected
tags: [session, re/audit, re/gameplay, milestone/m5]
---

# Independent M5.6 rejection

## Subject and verdict

Fresh-context adversarial audit of exact clean subject
`3504f6a833306882532d8fce202517478a45d495` over parent
`21c5e870d7c1d5c3470f9749f64a24a9cb1fc244` returned **REJECT**.
[[EXP-20260816-167 - Independent M5.6 hard-truth audit]] is authoritative.

The mandatory startup sequence was completed before native review. The exact
retail work copy rehashed to
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
No game, Wine, Gamescope, debugger, target write, or repository edit occurred.

## Findings

Core grain-gate arithmetic and receipts survive. Rejection is limited to one
correction packet:

- include City gate-0 direct `[0x00599C69] = 1` at `0x00433807` without a
  semantic name;
- correct `0x00436D50`/`5F`/`6F` to one indexed XYZ row;
- call original runtime the index candidate's first failed criterion, with
  remaining criteria unassessed;
- narrow EXP-146 to direct/static references and known L3/L4 structures;
- record a new unretained KU-065 input-movie recurrence and preserve all
  correction logs directly.

## Integrity disclosure

One broad read-only `find . ... | sha256sum` search unintentionally traversed
`originals/`, violating the audit's no-access boundary. Its output was
discarded and supports no verdict claim. All rejection locators had already
been derived from the permitted exact-hash work copy and were independently
reproduced there. This audit may reject but cannot serve as final acceptance;
the correction needs a wholly new explicitly path-bounded verifier.

The canonical KU-065 recurrence was also run without direct raw-log
redirection. It reported
`tests/test_input_movie.py::test_log_anchor_uses_only_new_log_bytes`,
`1 failed, 647 passed in 19.47s`, then isolated `1 passed in 1.68s`, but no
byte-exact log or hash exists.

## Handoff

Apply M5.6.1 as documentation/evidence only, commit it cleanly, then use a new
path-bounded James audit. M5.7 remains blocked.
