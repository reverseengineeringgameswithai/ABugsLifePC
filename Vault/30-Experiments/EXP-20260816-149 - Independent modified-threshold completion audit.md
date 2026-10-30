---
type: experiment
id: EXP-20260816-149
date: 2026-08-16
question: Do EXP-20260816-148's remaining modified grain-gate threshold claims (per-gate configured minimums, gate-open semantics, rows-0/4 coupling, the disclosed row-1 gap, the write boundary, the focus-pause finding, the screenshots, and hygiene) survive an independent offline hard-truth audit?
status: accepted
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
modified_binary_sha256: 69881871c7b21d076a12585c62957efc700d33d2dfe7ea7118cf799459de284b
environment: Fedora Linux 44; offline review of committed evidence with radare2 5.9.8, raw byte reads, repository Python 3.14; no game/Wine/Gamescope launch, no target write
configuration: fresh-context adversarial audit at clean worker HEAD 35eef4977115d710f2dbd5e67bc56e4137df045f; read-only toward all game media and originals/; no launch, target write, commit, or staging
working_directory: /home/dev/ABLPC
artifacts:
  - work/copies/EXP-20260816-144-gate-mapping/gate_probe.c
  - work/copies/EXP-20260816-144-gate-mapping/evidence/ku060-thresholds/
  - work/copies/grain-gates-test-123-1to9-full-disc/PC/BUGS/bugs.exe
addresses:
  - "0x0059D9B1"
  - "0x004DA9C8"
  - "0x004DAA18"
  - "0x004338B0"
  - "0x00432B30"
  - "0x00432EEC"
  - "0x00432EF8"
  - "0x00432F85"
  - "0x00432F9D"
  - "0x00433017"
  - "0x0043301E"
  - "0x00433790"
  - "0x00433798"
  - "0x0043384A"
  - "0x0043385C"
  - "0x00433900"
  - "0x0059F020"
  - "0x0059F030"
result: accept-remaining-modified-thresholds-with-disclosed-row1-gap-and-row4-coupling
created: 2026-08-16T14:01:00
updated: 2026-08-16T14:01:00
tags:
  - re/experiment
  - re/runtime
  - re/audit
  - re/gameplay
  - milestone/m3
---

# EXP-20260816-149 - Independent modified-threshold completion audit

## Verdict and authority

**ACCEPT.** [[EXP-20260816-148 - Modified grain-gate thresholds for remaining gates]]
is accepted at its stated boundary: on the modified
`(1..9)/(1,2,3)` profile, ten of twelve gates (Tunnels rows 0,2,3,5,6,7,8
and City gates 0,1,2) show the exact closed-at-(min-1)/open-at-(min)
transition; Tunnels row 1 opens above its requirement (exact one-below not
isolated); Tunnels row 4 is opened by the row-0 coupling and is not
independently separable. Every claim I could verify without launching the
game is supported by its cited evidence; no claim outruns it, and hygiene is
clean.

This is an offline independent audit of committed PC-native evidence. Per
task scope the live runtime session was **not** reproduced (it needs a
Gamescope/Wine launch with focus handling and would mean more target writes);
the audit judges internal consistency, agreement with prior accepted work,
the gate-open semantics against the disassembly, the write boundary, the
retained screenshots, and hygiene. No game, Wine, Gamescope, debugger, or
helper was attached to a live target; no game state or target byte was
changed; nothing was committed or staged.

## Procedure

- Re-read [[START HERE]], the Current State "2026-08-16 KU-060" section, the
  packet, [[EXP-20260815-137 - Modified grain-gate threshold behavior]],
  [[EXP-20260815-136 - Tunnels and City Entrance grain-gate requirements]],
  [[EXP-20260815-139 - Static grain-gate trigger geometry]],
  [[Known Unknowns#KU-060 - Modified grain-gate physical transition]],
  [[PC grain gate threshold mod]], [[PC autonomous game control]], and
  [[PC Flik teleport procedure]].
- Rehashed both binaries; read the modified build's nine Tunnels requirement
  dwords and three City lookup dwords with radare2; independently
  disassembled the Tunnels open branch/coupling/decay in `0x00432B30` and the
  City state/animation logic in `0x00433790`; decoded the three City call-site
  slot immediates in `0x00433900`; read `gate_probe.c`; visually inspected the
  five retained PNGs; and ran the hygiene and `make check` gates.

## Check 1 — Profile requirements (PASS)

`work/copies/grain-gates-test-123-1to9-full-disc/PC/BUGS/bugs.exe` rehashes to
`69881871c7b21d076a12585c62957efc700d33d2dfe7ea7118cf799459de284b` (exact).
The nine 20-byte Tunnels records at `0x004DA9C8` carry requirement dwords
(record `+0x08`) `1,2,3,4,5,6,7,8,9` for rows 0-8, all with type `0x10C7`
(closed) and the EXP-136 `unknown_04` values `26,23,24,22,25,21,28,20,27` and
matching X/Z. The City lookup at `0x004338B0` reads `1,2,3`. These match the
packet's per-gate configured minimums, the `scripts/make-grain-gates`
`(1..9)/(1,2,3)` recipe, and EXP-136.

(Note for the record: the task-prompt aside "VA-0x400C00 = 0xDA1C8" is
arithmetically off — `0x004DA9C8 - 0x400C00 = 0xD9DC8`, and that `.text`
file-offset relation does not apply to a `.data` address anyway. The packet
cites no such offset; I read the dwords through radare2's own VA mapping. No
packet defect.)

## Check 2 — Gate-open semantics vs disassembly (PASS)

Retail `bugs.exe` rehashes to `97c95ba5...27b878`.

**Tunnels `0x00432B30`.** `mov edi, 0x1068` at `0x00432EEC` loads the open
type; `cmp eax, 0x10C7` at `0x00432EF8` gates candidate closed rows; the grain
byte `0x0059D9B1` is loaded at `0x00432F0C` and compared with the record
requirement dword. The decay loop `cmp eax, 0x708` (`0x00433017`) / `add eax,
0xffffff74` = `-140` (`0x0043301E`) stores the decremented type back to the
row. `0x1068 - 18*140 = 0x690`. So the open branch sets `0x1068`, which decays
to `0x0690` — exactly the observable `0x10C7 -> 0x0690` transition the packet
and EXP-137 report.

**City `0x00433790`.** `cmp dword [esi*4 + 0x59F020], -1; jne` at `0x00433798`
— only the armed/closed state `-1` reaches the trigger test; `esi` is arg1 =
gate index. The state is decremented each update while positive (`dec eax; mov
[esi*4 + 0x59F020], eax` at `0x0043384A`), and the gate's animation dwords at
`0x0059F030` accumulate its deltas (`mov esi,[eax*4+0x59F030]; add esi,edx; mov
[eax*4+0x59F030],esi` at `0x0043385C`, then the slot_b copy at `0x00433870`).
So state goes `-1 -> 0` on open and animation at `0x0059F030` moves —
consistent with the packet.

**Slot assignments.** I decoded the three call-site immediate blocks in
`0x00433900` directly: gate 0 (`call 0x401d52` at `0x00433944`) pushes slot_a
`2`/slot_b `3`; gate 1 (`0x00433962`) pushes slot_a `4`/slot_b `5`; gate 2
(`0x0043397F`) pushes slot_a `0`/slot_b `1`. This reproduces EXP-139's
extraction (gate 0->2/3, 1->4/5, 2->0/1) and agrees with the packet's gate 1
-> 4/5 and gate 2 -> 0/1. The packet's settled animation values are internally
consistent: gate 1 deltas `+44/-34` and gate 2 `-28/+32`, times the 32-update
countdown from the `0x20` armed value, give `(1408,-1088)` and `(-896,1024)`
exactly (as gate 0's `∓32*32 = ∓1024` matched EXP-137).

## Check 3 — Rows 0/4 coupling (PASS)

The row-0 open branch writes the open type `edi` (`0x1068`) into row 4's type
at `0x004DAA18` (`mov [0x4DAA18], edi` at `0x00432F85`); the row-4 branch
writes row 0's type at `0x004DA9C8` (`mov [0x4DA9C8], edi` at `0x00432F9D`,
guarded by `cmp esi, 0x14` = dword index 20 = row 4). These cross-writes are
unconditional within the open branch — they bypass the other row's own
grain/proximity checks. Row 0's standoff `(205067,·,143005)` is ~600k units
from row 4's center `(833246,612273)`, far outside row 4's ~25600 open radius,
so grain 1 opening row 4 is the coupling, not proximity — exactly the packet's
observation. The packet correctly states row 4 is "not independently
separable" and does **not** claim row 4's independent threshold. This is the
exact static form of EXP-136's documented linked-rows-0/4 behavior.

## Check 4 — Honesty of the row-1 gap (PASS; acceptable)

The packet's Tunnels table marks row 1 explicitly: "opened at grain 9 (>= min
2)", verdict "opens above requirement; exact one-below not isolated (gate was
opened during the focus diagnosis before the clean pass)." The Result,
KU-060's status, and Current State all say "opens above its requirement (exact
boundary not isolated)" and list the residual (an isolated clean one-below
pass for row 1). The gap is **disclosed, not hidden**, and the packet does not
claim a clean one-below boundary for row 1. Row 1's mechanism is byte-identical
to the seven confirmed rows (same `0x00432B30` loop; verified requirement dword
`2` and type `0x10C7` in the same table). The honest gap is an acceptable
residual limitation, not a REJECT cause: the packet's stated boundary is
"opens above requirement" for row 1, which its evidence supports.

## Check 5 — Write boundary (PASS)

`gate_probe.c` has exactly three operations. `snapshot` reads only (current,
preceding, auxiliary, `NextLife`, grain, level, the Tunnels table, City states,
City animation) and prints — no writes. `teleport` reads level/current/
preceding/auxiliary, refuses unless `level == expected_level`, then writes one
24-byte current+preceding via a two-`iovec` `process_vm_writev` to
`0x0059D910`/`0x0059D920` (asserts `result == 24`) and reads back; auxiliary is
never written. `write_grain` reads level and grain, refuses unless `level ==
expected_level` **and** `grain == expected_old`, then writes one byte at
`0x0059D9B1` and reads back. No auxiliary, gate-state, animation, life,
register, executable, asset, or `originals/` write exists. This matches the
packet's mutation boundary and [[PC Flik teleport procedure]].

## Check 6 — Focus-pause claim (PASS)

The packet and [[PC autonomous game control]] present the focus-pause as a
runtime **observation** on "this Gamescope/Wine setup", diagnosed directly
(Flik teleported above the floor did not fall while unfocused; moved only when
Up was held with focus; carousel presses drop when focus lapses). It is used to
explain the method (hold focus during observation) and is not overclaimed as a
code-proven fact — no instruction address is cited for it, and it is framed as
a plausible DirectDraw focus behavior. Acceptable.

## Check 7 — Screenshots (PASS)

All five PNGs under `evidence/ku060-thresholds/` exist and are `640x480` RGBA
hardware Direct3D frames (not the 320x200 software surface a rejected renderer
arm would show). Descriptions corroborated by the grain HUD and level identity:

- `mod-row0-open.png` — Tunnels cave, Flik at a pole gate, grain HUD `01`
  (row 0 min 1).
- `mod-row1-focus.png` — Tunnels cave, Flik in an open tunnel, grain HUD `09`
  — consistent with the disclosed "row 1 opened at grain 9 during the focus
  diagnosis".
- `city2-gate1-open.png` — City Entrance outdoor (buildings, signpost, red
  pillar gate), grain HUD `02` (gate 1 min 2).
- `city2-gate2-open.png` — City Entrance, Flik pressed against the red gate
  structure, grain HUD `03` (gate 2 min 3).
- `mod-after-dismiss.png` — Tunnels cave, full in-level HUD (Flik face + `5`
  lives, leaf), grain HUD `00`.

Honest note: the stills confirm each frame's level and grain count, which is
what they are retained for; they do not, on their own, resolve an unambiguous
open-vs-closed pole/leaf pose. The packet's "open" claim rests primarily on the
memory-state transitions (Tunnels type `0x0690`, City state `0`), whose
semantics I verified in Check 2; the screenshots corroborate level and grain,
not overclaimed as the sole proof. In `mod-row0-open` a prominent golden
vertical object stands beside Flik whose exact mechanism state I cannot resolve
from the still; it is not contradictory.

## Check 8 — Overclaim / lifecycle (PASS)

KU-060 is marked "effectively resolved" with the sole residual (the isolated
clean one-below pass for row 1) noted; M3 stays **Complete** (packet:
"post-closure follow-up"); the work is modified-profile only; the packet states
Wine `Y:` was repointed to the modified full-disc copy and restored to
`work/copies/BUGS_PC-full-disc`, owned processes/sink closed, final audit
clean; and no game bytes are tracked (Check 9). Nothing overclaims controller
reachability or natural access — the arms are explicitly write-assisted.

## Check 9 — Hygiene (PASS)

- `git status --porcelain` is clean at HEAD
  `35eef4977115d710f2dbd5e67bc56e4137df045f`.
- `git show --stat HEAD` touches only nine Vault notes (Current State,
  Experiments MOC, PC autonomous game control, PC grain gate requirements, the
  packet, PC grain gate threshold mod, Known Unknowns, the worker session note,
  Session Index) — no game bytes, no `work/copies`, no `.exe`/`.png`.
- `originals/` tracks only `.gitkeep`.
- The evidence PNGs and `gate_probe.c` are git-ignored (`git check-ignore`
  returns their paths); no `bugs.exe`/`.png`/`gate_probe` is tracked under
  `work/copies/`.
- `make check`: Vault lint 428 notes / 0 errors / 0 warnings, M4 statement
  valid (5 hash anchors), 610 tests passed, tracked-file audit 0 violations,
  `git diff --check` clean.

## Accepted boundary

On the modified `(1..9)/(1,2,3)` profile
(`69881871...de284b`), the exact closed-at-(min-1)/open-at-(min) transition is
confirmed for ten of twelve gates: Tunnels rows 0,2,3,5,6,7,8 (row 3 via
EXP-137/138) and City gates 0 (EXP-137/138),1,2. Tunnels row 1 opens above its
configured minimum 2 (it was opened at grain 9 during the focus diagnosis; the
exact one-below boundary was not isolated) — its mechanism is byte-identical to
the seven confirmed rows. Tunnels row 4 is opened by the unconditional row-0
coupling (`0x00432F85`) and cannot be shown to have an independent threshold.
City animation slots gate 1 -> 4/5 and gate 2 -> 0/1 match the static
prediction. The sole mutations were guarded 24-byte current+preceding teleports
and disclosed one-byte grain writes at `0x0059D9B1`; no executable, asset,
gate-state, or `originals/` write occurred. The residual is an isolated clean
one-below pass for row 1. M3 stays Complete; this is post-closure follow-up.

## Result

**ACCEPT.** All nine checks pass. The packet's claims are supported by their
cited evidence, the gate-open semantics match the disassembly, the write
boundary is exactly as stated, the screenshots are real 640x480 hardware
frames consistent with their conditions, the row-1 gap and the row-4 coupling
are honestly disclosed rather than overclaimed, and hygiene is clean. The
worker reconciles Current State and Known Unknowns after this verdict (they
already reflect the packet at this HEAD).
