---
type: session
date: 2026-08-16
agent: James
status: audit-complete
tags: [session, re/audit, re/camera, testing]
---

# Camera audit and KU-065 follow-up

## Goals

1. Fresh-context adversarial audit of EXP-161 at subject commit `02946af`.
2. Reproduce and identify KU-065 without ever filtering live pytest output.

Mandatory startup material, the M5/operating-model roadmap sections, current
state, environment, operating manual, charter, cross-port policy, relevant
MOCs, KU-065, root instructions, EXP-161/XPORT-004, and prior James audit
precedents were read before substantive work.

## Camera audit result

[[EXP-20260816-162 - Independent camera reconnaissance audit]] returns
**REJECT**.

Surviving evidence: D3DApp-derived renderer scaffolding; the three known
`D3DVT_TLVERTEX` submissions; seven direct calls to terrain thunk
`0x00401659`; correct containing-function attribution; clean PS1/PC authority
separation; and an honest open manual-controls discrepancy.

Blocking defects:

- viewport endpoints `0x00423E93`/`0x00423F55` are operand bytes, while the
  viewport structure is built at `0x00423EDE`-`0x00423F43`;
- `0x00405FE0` performs the matrix/translation transform itself beginning at
  `0x0040605F`, so pointer arguments do not put the transform upstream;
- `0x0045A7F0` does not call that builder and an older PC static export already
  says it transforms and fills batches inline;
- tracing the matrix finds the under-claimed PC-only chain
  `0x0041ADF0 -> 0x0041B7D0 -> 0x00599C90 -> 0x00455710 ->
  0x005B58E0/0x005BDB8C -> 0x004636C0 -> 0x0063E888 -> 0x00405FE0`;
- after the two reset consumers and known City dispatcher are removed, four
  terrain-call functions are unmapped, not five.

The Camera row is frozen at Untouched only until one offline correction packet
propagates the view chain and a fresh delta audit accepts it. No runtime camera
differential comes first. The single bounded packet is EXP-164 as written in
EXP-162 and DEC-134.

XPORT-004 otherwise passes the policy audit. Source ID, exact commit, paths,
and evidence classes are present; PS1 confirms nothing about PC; the
researcher's word "confirm" did not alter that boundary; manual controls stay
an open candidate difference.

## KU-065 result

[[EXP-20260816-163 - KU-065 canonical-suite reproduction follow-up]] does
**not** reproduce the original `1 failed, 647 passed` signature:

- 13/13 canonical host suites: `648 passed` each;
- 100/100 complete manifest modules: `198 passed` each;
- 200/200 focused descriptor/mount selections: `17 passed` each;
- every pytest invocation wrote directly to its own raw log before any search.

One constrained-sandbox full run produced nine failures, including
`test_cli_receipt_cleanup_error_is_silent_and_closes_every_descriptor` with a
process-global descriptor count `15 -> 14`. Seven GDB cases were ptrace-
blocked and one input-movie case timed out in that same run, so this is an
Inferred candidate only, not identification of the lost single failure.
KU-065 remains open and the suite remains a qualified rather than unqualified
gate.

The 317 raw logs are retained locally under ignored
`work/copies/EXP-20260816-163-ku065-evidence/`; their SHA-256 manifest is
`e60f1ff3...63b1e`. This work started no game, Wine, Gamescope, debugger
target, or target write and touched no original or external PS1 checkout.

The final broad process audit found 32 pre-existing baseline-prefix
`winedevice.exe` helpers, PIDs `68248`-`344284`, parented by user systemd PID
`1927`. Their start times and sampled `work/copies/` working directories show
that they predate this work; no active game, Gamescope, `wineserver`, pytest,
or debugger target remained. Because the helpers were not recorded as owned
at launch, DEC-108 and the runtime lifecycle policy prohibit broad-name
termination. They remain recorded in Environment Status for an ownership-
aware cleanup before any future runtime launch. EXP-163's passing results
therefore include this residual helper background.

## Records updated

- EXP-162 and EXP-163;
- Current State, including replacement of the stale next-agent handoff;
- Project Roadmap coverage reconnaissance;
- Subsystem Coverage Map, Experiments MOC, and Reverse Engineering MOC;
- KU-065 in Known Unknowns;
- DEC-20260816-134;
- this session note.

## Final validation

- `make check` completed from a direct raw log with SHA-256
  `d0ea97fae2efe211b9809acc919557719685153fab1ae6dc0b41a7168fd69480`:
  Vault lint reported 465 notes, 0 errors, and 0 warnings; the M4 statement
  check found five valid hash anchors; the tracked-file audit reported zero
  violations; and this one observed suite run reported `648 passed in 17.94s`.
- That passing suite observation remains qualified by open KU-065; it is not
  recorded as an unqualified clean gate.
- `git diff --check` passed before the intentional commit.
- The closure process audit found no active game, Gamescope, `wineserver`,
  pytest, or debugger target. It did find the 32 unowned pre-existing
  `winedevice.exe` helpers recorded above; they were not terminated.

## Next

Run only EXP-164, the offline view-chain correction, then a fresh delta audit.
For KU-065, retain direct raw logs after the next independently authorized
Wine/Gamescope session; do not launch the game solely to create contention.
