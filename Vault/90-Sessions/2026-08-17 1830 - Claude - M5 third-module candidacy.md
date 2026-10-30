---
type: session
date: 2026-08-17
agent: Claude
status: complete
tags:
  - session
  - milestone/M5
---

# M5 third-module candidacy

## Agent

Claude.

## Goal

Open M5's third-module work by executing step 1 of the milestone's own
procedure: rank candidate modules against the six entry-gate criteria and
record why the rejected ones fail, before deriving any contract.

## Files inspected

The startup sequence per [[START HERE]] (re-read this session, per
`DEC-20260814-055`); [[Project Roadmap]]'s M5 section in full;
`work/copies/BUGS_PC-full-disc/bugs.exe`, re-hashed to
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`; the
accepted creature and input censuses; `ghidra-evidence.json`.

## Experiments inspected

`EXP-20260816-172` (creature), `EXP-20260817-181`/`-184` (input),
`EXP-20260816-153` and `EXP-20260816-171` (the two admitted modules, for packet
shape).

## Changes made

New experiment note
[[EXP-20260817-186 - M5 third-module candidacy ranking]]; roadmap sections
**M5.9** (this packet, with result) and **M5.10** (the named next packet); M5
status line updated; `KU-072`; entries in [[Current State]],
[[Experiments MOC]] and this index.

No code, parser, test or module changed — this packet selects, it does not
implement. No game asset, `originals/` path or PS1 source touched.

## Conclusions

The obvious candidate failed and a better one was found by testing rather than
assuming.

The **creature behaviour VM** looked strongest — the census that mapped it was
accepted with zero defects — but it makes 16 direct calls to 15 distinct engine
thunks plus one indirect call, and three targets are unidentified anywhere in
the vault. That is a failure of entry criterion 1, not a gap to be papered
over.

The **input action-bit resolver** has a genuinely call-free core:
`0x0042ED41`-`0x0042EEBB` contains zero calls, so (state buffer, axis values,
binding tables) → action-bit word has no engine dependency. It also clears the
other five criteria from already-recorded evidence.

## New hypotheses

That the `±11200` axis comparison is a deadzone or clamp. The instructions give
the comparison and the magnitude; the interpretation is marked Inferred.

## Contradictions discovered

None.

## Tests run

No repository test suite is affected — no code changed. Method checks: every
outbound call in both candidate ranges enumerated directly from the binary and
each thunk resolved to its target; each of the 15 creature-VM targets grepped
across all authored notes and exports; the input function's call-free tail
confirmed against an aligned disassembly, the first attempt having started
mid-instruction; and the `8`-stride binding table checked against the input
census **before** any novelty claim — it is already documented there, at line
430.

## Unresolved questions

`KU-072` (three unidentified creature-VM callees); `KU-069` (the `0x18`-stride
configuration record's layout); whether the axis limit is a deadzone or a
clamp.

## Recommended next action

**M5.10**, as named in the roadmap: derive the resolver's contract from
`0x0042ED41`-`0x0042EEBB` directly rather than from any summary, implement with
exact wrapping and shift semantics, refuse on undefined inputs, and
differential-test against the CAP-002 receipts.

## Git commit if applicable

One intentional commit; tree clean.
