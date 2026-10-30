---
type: experiment
id: EXP-20260816-145
date: 2026-08-16
question: Do EXP-20260816-144's runtime grain-gate visual-mapping claims (standoff agreement, engine-exact nearest-gate distances, screenshots, control recipe, boundary, and hygiene) survive an independent offline hard-truth audit?
status: rejected-then-accepted-after-correction
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline review of committed evidence with radare2 5.9.8, raw byte reads, repository Python 3.14; no game/Wine/Gamescope launch, no target write
configuration: fresh-context adversarial audit at clean worker HEAD 6dd9b124b0f84d76918beca1ccf98e3a2b62942f; read-only toward all game media and originals/; no launch, target write, commit, or staging
artifacts:
  - work/copies/EXP-20260816-144-gate-mapping/gate_probe.c
  - work/copies/EXP-20260816-144-gate-mapping/evidence/tunnels/
  - work/copies/EXP-20260816-144-gate-mapping/evidence/city/
  - scripts/grain-gate-standoffs.py
addresses:
  - "0x00416580"
  - "0x004A7600"
  - "0x004A7841"
  - "0x004A797A"
  - "0x004A7878"
  - "0x0059D910"
  - "0x0059D920"
  - "0x0059F020"
  - "0x00861C84"
  - "0x004DA9C8"
  - "0x007F1170"
result: reject-for-incorrect-city-nearest-distance-arithmetic-then-accept-after-worker-corrected-to-engine-sar-8-from-settled-current
created: 2026-08-16T12:18:00
updated: 2026-08-16T12:18:00
tags:
  - re/experiment
  - re/runtime
  - re/audit
  - re/gameplay
  - milestone/m3
---

# EXP-20260816-145 - Independent runtime gate mapping audit

## Verdict and authority

**Original verdict: REJECT. Final disposition: ACCEPT after the worker's
in-place correction** (see "Correction confirmed" below). For a single
specific, isolated, easily-fixable defect: the
City Entrance "nearest dist²" values for gate 0 (stated `4160`) and gate 1
(stated `9025`) in [[EXP-20260816-144 - Runtime grain-gate visual mapping]]
are **not** the engine `sar`-8 squared distances the packet claims. They
were computed with truncation-toward-zero, which diverges from the game's
arithmetic-shift helper `0x00416580` exactly for the two gates whose
coordinate difference is negative. The correct engine values are gate 0 =
`4289` (standoff→center) or `3482` (settled→center), and gate 1 = `9216`.
Gate 0's stated `4160` also silently contradicts the accepted
[[EXP-20260815-139 - Static grain-gate trigger geometry]], which computed
the identical gate-0 standoff-vs-center as `4289 < 6400 inside`.

This is not a rejection of the mapping science. Every load-bearing
conclusion — which visible gate is which mechanism, the inside/outside
verdicts, the unambiguous nearest-gate identity, `NextLife=0`
walkability, the screenshots, the control recipe, the write boundary, and
all hygiene — verified cleanly and is recorded below. The reject is
scoped so the worker recomputes two numbers with the engine predicate,
reconciles which reference position the City dist² column uses, and
resubmits.

This is an offline independent audit of committed PC-native evidence. No
game, Wine, Gamescope, debugger, or helper was attached to a live target;
no game state or target byte was changed; nothing was committed or staged.
Per task scope, the live runtime session was **not** reproduced
(concurrent nested Gamescope crashes; re-teleporting means more target
writes); the audit judges what is independently verifiable from the
committed artifacts.

## Procedure

- Re-read the startup authority chain ([[START HERE]]), the Current State
  "2026-08-16 runtime grain-gate visual mapping" section, the packet, the
  new [[PC autonomous game control]] recipe, EXP-136/138/139/141,
  [[PC grain gate threshold mod]], [[PC Flik teleport procedure]],
  [[Wine Linux Play Baseline]], and [[Known Unknowns#KU-060 - Modified grain-gate physical transition]].
- Rehashed `bugs.exe`; independently disassembled the cited chooser and
  proximity code; recomputed every stated distance in Python under both
  `sar` (`>>`) and truncation semantics; ran the standoff tool; visually
  inspected the retained PNGs; read `gate_probe.c`; and ran the hygiene
  and `make check` gates.

## Check 1 — Standoff agreement (PASS)

`.venv/bin/python scripts/grain-gate-standoffs.py --compact` reproduces the
twelve chosen standoffs. Each matches the EXP-144 tables and traces to an
EXP-141 candidate or a documented proven point:

- T0–T2, T4–T8: the computed candidates
  `(205067,33916,143005)`, `(489642,32092,-451306)`, `(843615,33812,302388)`,
  `(840401,33940,626583)`, `(1126934,31480,1308289)`,
  `(1471643,32820,1426369)`, `(1202034,31492,1970285)`,
  `(1646238,33792,2546125)` — exact table match.
- T3: proven `(501696,30092,494016)` (EXP-130/137), not the computed
  candidate — as the tool annotates and the note states.
- C0: proven `(-87622,917,-182181)` (EXP-137), not the computed candidate.
- C1: `(354031,2540,10716)`; C2: `(601433,1132,329374)` — exact table
  match.

No standoff coordinate fails to trace to EXP-141 or a documented proven
point.

## Check 2 — Nearest-gate arithmetic (DEFECT; the sole reject cause)

The engine predicate is helper `0x00416580` (thunk `0x00401A37`), raw-
verified in EXP-139: `dx = (a->x - b->x) >> 8` (`sar`, arithmetic),
`dz = (a->z - b->z) >> 8`, return `dx*dx + dz*dz < r*r`. Python `>>` on
negatives matches `sar`; `int(v/256)` truncates toward zero and differs
only for negative operands. `gate_probe.c`'s snapshot computes the Tunnels
distance correctly this way (`((int64_t)current - x) >> 8`), but computes
**no City distance at all** — it only dumps the `0x0059F020` state array —
so the City dist² numbers in the note are hand-derived.

**Tunnels (PASS).** All nine stated dist² match the engine `sar` value
exactly (from the standoffs): row0 `3872`, row1 `3969`, row2 `3872`, row3
`4993`, row4 `3754`, row5 `3969`, row6 `3844`, row7 `3969`, row8 `3872`.
Rows 1/3/5/7 have a negative difference; truncation would give
`3844/4805/3844/3844`, so the note used the correct `sar` handling here.
Row 3's `4993` also matches EXP-137/138. Standoffs sit ~16000 world units
out (inside the 25600 open radius, outside the 10240 message radius),
harmless at grain 0.

**City inside/outside verdicts and nearest-gate identity (PASS).** Gates
are hundreds of thousands of units apart; for each standoff the intended
gate is the unambiguous minimum (gate0 `3482` vs `3.7M`/`10.6M`; gate1
`9216` vs `3.3M`/`2.2M`; gate2 `11885` vs `10.9M`/`2.3M`). All three
inside/outside verdicts are correct under both `sar` and the stated
numbers: gate 0 inside 6400, gate 1 just-outside 8100, gate 2 just-outside
10000.

**City dist² values (DEFECT).**

| Gate | Note value | Engine `sar` (standoff→center) | Engine `sar` (settled→center) | Truncation (standoff) |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 4160 | **4289** | 3482 | 4160 |
| 1 | 9025 | **9216** | 9216 | 9025 |
| 2 | 10952 | **10952** | 11885 | 10952 |

- Gate 0's `4160 = 64² + 8²` comes only from standoff `(-87622,-182181)`
  with truncation (`floor(-16493/256) = -65` under `sar`, but `-64` under
  truncation). The engine value is `4289 = 65² + 8²`, exactly EXP-139's
  own accepted figure. Stating `4160` is an unflagged contradiction with
  accepted prior work, which the vault policy forbids resolving silently.
- Gate 1's `9025 = 95²` uses truncation (`floor(-24540/256) = -96`,
  `9216`, under `sar`). The engine value is `9216`.
- Gate 2's `10952 = 74² + 74²` is `sar`-correct because both differences
  are positive — but it is computed from the **standoff**, not the
  "Settled current" `(599675,·,332298)` shown in the adjacent column
  (which would give `11885`). So the City "Nearest dist²" column is also
  reference-position-inconsistent: it is standoff-based, while the table
  presents a settled-current column beside it and labels the method
  "engine sar-8 squared distance."

No verdict, nearest-gate identity, or correlation conclusion changes, but
two of three City distances are stated wrong under the packet's own cited
predicate. Fix: recompute gate 0 and gate 1 with `sar` (`4289`/`3482` and
`9216`), and state whether the City dist² is measured from the standoff or
the settled current, consistently for all three gates.

## Check 3 — Screenshots (PASS)

All 16 PNGs exist under `evidence/tunnels/` and `evidence/city/`, each
`640x480` RGBA — Direct3D hardware resolution, not the 320x200 software
surface a rejected renderer arm would show. Descriptions corroborated:

- Tunnels are diagonal wooden-pole barriers (verified on T0, T3, T6, T8).
- T3 shows a clear **"10"** on a leaf sign amid crossed poles (red mushroom
  bottom-right, grain HUD `00`). T6 shows a **"30"** on the right-hand gate
  leaf with the blue berry cluster at top-left. T0 shows the start-area
  pole gate with red mushroom.
- T8 shows the wooden-pole gate structure, but the **"30"** numeral and the
  patrolling grasshopper are not legible in this dark/occluded frame; the
  note's own row-8 wording ("patrolling grasshopper", "dark segment") is
  honest about the occlusion, so this is not overclaim, only a weaker
  frame.
- C0 is an unambiguous match: the giant red **"cola"** can with Flik in
  front and the red-pillar leaf gate on the left.
- C1 is heavily occluded (Flik's green pack visible through a gap between
  red pillars); C2 shows Flik facing the gate's wood-grain **back side**
  with the red pillar at the left edge — matching the note's "back side"
  clarification.
- `tunnels-start.png` shows the "Level Two: Tunnel Run / Locate the
  entrance to the Council Chambers" briefing, corroborating the three
  distinct numbering schemes (briefing "Level Two", carousel "tunnels",
  internal level 3).

The evidence is real, hardware-resolution, and not overclaimed.

## Check 4 — Control-recipe disassembly (PASS)

Rehash: `bugs.exe` is `97c95ba5...27b878` (matches).

- (a) The chooser is `SwitchDriverScreen` at `0x004A7600`. It loads
  `GetAsyncKeyState` at exactly `0x004A7841`
  (`mov esi, dword [sym.imp.USER32.dll_GetAsyncKeyState]`) and polls it
  via `call esi` after pushing the VK codes: `push 0x28` (VK_DOWN),
  `push 0x26` (VK_UP), `push 0xd` (VK_RETURN), `push 0x20` (VK_SPACE) —
  all present in the poll loop at `0x004A7939`–`0x004A7A19`.
- (b) The timeout compare is `cmp dword [0x7f1170], 0xea60` at
  `0x004A797A` (`0xea60 = 60000` ms); the counter is reset to 0 at
  `0x004A7878`.
- (c) The six hardware markers and the "320x200 lines are mode
  *enumeration*, not selection" nuance in the recipe agree with
  [[Wine Linux Play Baseline]] and [[START HERE]]. The XTEST-vs-XSendEvent
  reasoning is technically sound: `GetAsyncKeyState` reads the asynchronous
  physical key-state table, which synthetic `XSendEvent` (a posted window
  message) never updates, whereas XTEST injects at the input-device layer
  and does update it — hence `xdotool key --window` is ignored and
  `windowfocus --sync` + `xdotool key` works.

## Check 5 — Carousel order (PASS)

The recipe presents the carousel order (City Entrance = Right ×7)
explicitly as "researcher-provided", and states "Carousel position is not
the internal level number", listing the observed internal values
(Anthill=1, Council Chamber=2, Tunnels=3, City Entrance=4) with the
instruction to "Always confirm the loaded level by reading `0x00861C84`,
not by carousel position." These are correctly framed as
runtime-observed/researcher-provided, not static-derived.

## Check 6 — Overclaim / boundary (PASS)

- `gate_probe.c` `teleport` writes exactly current+preceding (24 bytes)
  via a two-`iovec` `process_vm_writev` to `CURRENT_XYZ` (`0x0059D910`)
  and `PRECEDING_XYZ` (`0x0059D920`), asserts `result == 24`, and reads
  back; it never writes auxiliary, grain, state, animation, life, or code.
  `snapshot` is read-only. `GRAIN` (`0x0059D9B1`) is only read. This
  matches [[PC Flik teleport procedure]].
- The packet stays **write-assisted** and explicitly disclaims controller
  reachability / natural access. M3 is kept **Complete** ("post-closure
  mapping, not a reopened milestone").
- KU-060 correctly keeps the physical modified-threshold receipts for the
  untested gates (City 1/2 and Tunnels rows other than 3) **open**, while
  recording that their confirmed approach standoffs now exist.

## Check 7 — Hygiene (PASS)

- `git status --porcelain` clean at HEAD
  `6dd9b124b0f84d76918beca1ccf98e3a2b62942f`.
- `git show --stat HEAD` touches only Vault notes (Current State,
  Experiments MOC, PC autonomous game control, PC grain gate requirements,
  the packet, Known Unknowns, the worker session note, Session Index) — no
  game bytes, no `work/copies`, no `.exe`/`.png`.
- `originals/` tracks only `.gitkeep`.
- `make check`: Vault lint 419 notes / 0 errors / 0 warnings, M4 statement
  valid (5 anchors), 610 tests passed, tracked-file audit 0 violations.
- The evidence PNGs and `gate_probe.c` are git-ignored (`git check-ignore`
  returns their paths).

## Accepted boundary (upon fix)

Everything except the Check-2 City distance arithmetic verified cleanly.
On correction of the gate 0/1 City dist² to their engine `sar` values
(`4289`/`3482` and `9216`) and a consistent statement of the City dist²
reference position, the acceptable boundary is: the twelve EXP-141
standoffs are runtime-walkable (`NextLife=0` at each post-teleport
snapshot); each visible gate is correlated to its mechanism by the
unambiguous nearest-gate index, the `0x0059F020` state array, and the
retained 640x480 screenshots; the [[PC autonomous game control]] recipe
(XTEST input, `GetAsyncKeyState`/`0x7f1170` chooser facts, carousel vs
internal-level distinction) is disassembly-accurate; the work stays
write-assisted with guarded 24-byte teleports only; M3 stays Complete; and
KU-060's physical modified-threshold receipts for the untested gates
remain open. No grain, executable, asset, or `originals/` mutation
occurred.

## Correction confirmed (2026-08-16, post-verdict)

The worker corrected the EXP-144 City Entrance table in place. It now
computes "nearest dist²" as the engine `sar`-8 squared distance (helper
`0x00416580`, arithmetic shift) from the **settled current** position to
each gate center, with a caption stating that reference and predicate, and
an "Independent audit and correction" section citing this note. The
corrected values — gate 0 `3482` (< 6400, inside), gate 1 `9216`
(>= 8100, just outside), gate 2 `11885` (>= 10000, just outside) — match
the values independently recomputed here, and all three now use one
consistent reference position (resolving the gate-2 standoff/settled
mismatch). No nearest-gate identity or inside/outside verdict changed.
This resolves the sole defect. **Verdict upgraded to ACCEPT.** The worker
still reconciles Current State and KU-060 and commits.

## Result

REJECT (original verdict) for the incorrect City nearest-distance
arithmetic (gates 0 and 1
computed with truncation instead of the engine `sar`, gate 0 also
contradicting EXP-139's accepted `4289`) and the reference-position
inconsistency of the City dist² column. All other claims — standoff
agreement, Tunnels distances, inside/outside verdicts, nearest-gate
identity, screenshots, control-recipe disassembly, carousel framing,
write boundary, milestone/KU-060 boundary, and hygiene — independently
verified. The worker reconciles Current State and Known Unknowns after
correcting the two numbers.
