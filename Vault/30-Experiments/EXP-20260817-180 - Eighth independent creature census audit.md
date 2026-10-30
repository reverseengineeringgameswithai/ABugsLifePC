---
type: experiment
id: EXP-20260817-180
date: 2026-08-17
question: 'Does the creature actor pool and behaviour VM census survive an eighth independent re-derivation and stand at its documented boundary?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline audit; GNU objdump 2.46; radare2 5.9.8; no runtime, debugger, or target write
environment_version: objdump 2.46-3.fc44
working_directory: /home/dev/ABLPC
configuration: fresh-context audit at clean HEAD 2cb6b07; read-only toward game media and originals; git history inspected; nothing committed or modified by the auditor
artifacts:
  - static/exports/BIN-97c95ba5572dce63/SUBSYS-creature-actor-static-census.md
addresses:
  - "0x0041E2E9"
  - "0x0041E2E4"
  - "0x0041E801"
file_offsets: []
result: accept-zero-defects-creature-row-bounded-and-event-row-touched
created: 2026-08-17T06:30:00
updated: 2026-08-17T06:30:00
tags:
  - re/experiment
  - re/audit
  - re/actors
  - research/coverage
---

# EXP-20260817-180 - Eighth independent creature census audit

## Verdict

**ACCEPT** at `2cb6b07`. **Zero defects.**

Every number in the packet was re-derived from the retail bytes without
trusting the text, and all of them reproduce: 463 instructions; 69 branch
instructions with zero off-boundary **and zero out-of-script** targets; the
digit-identical histogram; both switch tables entry by entry; the 21 `+0x5C`
instructions, after independently accounting for the four rebased `[esi-0xe]`
sites in `0x0041EC40`; the four `+0x70` writers; the ten `+0x40` stores; the
ten condition-slot reuses from `0x0041E369`; the four `[esp+0x4c]` reads; the
trailing-byte histogram; and the extent `0x0041DC60`-`0x0041E845` with nothing
beyond it.

The §0/§0.0 prior-art accounting is judged honest **in both directions**: the
nine-artifact membership list is exactly the set of files in the directory
containing the pool base, the two byte case tables really are the only two of
the five addresses absent from every artifact, and every quoted draft
attribution matches `git show` verbatim. All seven rows of the Audit-history
fact table check out against the notes they cite, and every correction
`EXP-20260817-179` required landed.

## One new fact about the binary

The auditor found an **eighth writer of the mode slot**, at `0x0041E2E9`:

```text
41e2e4: 68 10 d9 59 00          push 0x59d910
41e2e9: c7 44 24 50 01 00 00 00 mov  DWORD PTR [esp+0x50],0x1
41e2f1: e8 cd 2d fe ff          call 0x4010c3
```

`[esp+0x50]` there is the same storage as `[esp+0x4c]` elsewhere in the
function, because the `push` at `0x0041E2E4` has displaced `esp` by 4. No
search on the displacement finds it. `ghidra-evidence.json` corroborates
independently: it models the slot as `param_3` and emits
`param_3 = (int *)0x1;` immediately before
`thunk_FUN_0041a550(&DAT_0059d910)`.

It falsifies nothing. The site writes `1`, so §5.1's reading of the mode-`> 2`
gate survives; it lies in the region the packet declares unanalysed; and it is
outside §0.1's declared full-extent sweep inventory, which covers `+0x5C`,
`+0x70`, the `call eax` and record fields. The clause that could be read as
covering it is the only clause in that sentence **not** marked "over the full
extent" — the marked one, the four reads, is exactly right. The auditor
recorded it as a MINOR rather than a failed claim, and it is now in §5.3 with
the `esp`-delta caution generalised for future sweeps.

## Minor findings, all applied

The eighth mode-slot writer above. `EXP-20260817-179`'s "seven writes" is
corrected to eight in an appended Corrections section. Current State's
round-six paragraph carried both a stale "3,046 everywhere" clause and its
replacement; the stale one is removed. §0.1 mixed a half-open byte count with
an inclusive extent in one sentence; both conventions are now stated
explicitly. Current State described the coverage-map rule edit loosely; it now
says the rule drops the false count and describes the two failed correction
passes qualitatively. Audit-history row 6's final cell answered a different
question than its column header; it now answers directly.

## What survived

Everything, for the eighth time. Beyond the verdict's list: the pool extent
and stride from both loop terminations; `0x700`/`0x1C`/64; `380 = 181 + 199`
and `199 = 2 + 197`; §3.1's nineteen rows, ten distinct thunks and 9/5/5/17
partition; §3.2's eleven types; §3.3 over 48 entries; all twelve flag bit rows
with register provenance; reachability with **zero** stored little-endian
pointers to any of the five functions or their thunks; all table extents; the
external entry point; `0x004C7970` at zero references; five `EVENT` strings;
the four `KU-069` indexes; the Ghidra character counts (18,101 / 18,205) and
the four PC-advance lines; and all 22 cited file offsets. All quoted
disassembly blocks match objdump byte for byte.

## Scope answers

- **Bounded is correct for Enemies/actors/AI.** The packet has PC-native
  static evidence — the pool, both switch tables, the VM, 40 validated
  programs, the handler-call edge — and states its boundary explicitly: the
  region past `0x0041E1A8` unanalysed, no runtime, the level gate unresolved.
  Mapped requires runtime evidence and is correctly withheld behind `KU-068`.
- **Touched is correct for Event/scripting.** Five log strings and one push
  site, no code read.
- **The §0/§0.0 novelty and prior-art accounting is honest.** The surviving
  novelty claim — the two byte case tables plus the authored, validated model —
  is exactly right.
- **All seven Audit-history rows are accurate**, each checked against the note
  it cites. The lead-in's disclaimer of a global claim is genuine: no such
  assertion remains.
- **Every correction `EXP-20260817-179` required landed.** The strings the
  earlier rounds rejected survive only as quoted records of those defects.

## Limitations of this audit

What the region past `0x0041E1A8` computes, the ten per-type `+0x7C` handlers,
the nine opcode-11 subroutines and the five modes were not analysed — only that
the packet claims nothing about them, and no sentence was found that does.
Caller completeness rests on rel32 call scans plus whole-image absolute-value
scans; computed dispatch is excluded by construction. `+0x5C` accesses outside
the five named functions were enumerated only for the two forms the export
names. The underlying correctness of the cited M2 exports and of
`EXP-20260815-128`/`129`, `EXP-20260816-153`/`155`/`165` and `KU-064` was not
re-verified — only that the quoted text and addresses are present and match.
`0x0059D99E`'s eleven other writers, the `0x004C2100` table and the
`0x004ABE00` ground-snap callee were not re-derived. No level file was parsed
and nothing was run.

## Hygiene

`make vault-lint` 502 notes / 0 errors / 0 warnings; `make audit-tracked` 0
violations; `make test` **686 passed** of denominator **686**, single
invocation, 17.34s. The figure carries the open `KU-065` qualification, which
the packet correctly applies rather than treating the green suite as
unconditional.

## Disposition

The packet is **accepted** at its documented boundary:

- **Enemies, actors and AI** stands at **Bounded**;
- **Event/scripting** stands at **Touched**;
- `KU-068` keeps every runtime claim closed and `KU-069` records four unbounded
  table indexes;
- no milestone status changes, and M5 stays where `EXP-20260816-171` left it.

Eight fresh contexts re-derived the analysis and **no derived number in it ever
changed**. The seven rejections were: three on substance (scope, an unread
function tail, prior-art attribution), and four on the prose describing the
packet and its own audit history. The lasting method rules from that sequence
are in [[Subsystem Coverage Map]].
