---
type: research
status: confirmed-bounded
created: 2026-10-29
updated: 2026-10-29
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
evidence: [EXP-20260909-008, EXP-20260909-009, EXP-20260914-016, EXP-20260930-005, EXP-20261001-006, EXP-20261005-001, EXP-20261005-002]
tags: [re/combat, re/weapons, re/static]
---

# PC projectile records, homing and kill accounting

The shared projectile and drop records, how a berry throw fills one, how homing
shots pick and follow a target, and what the berry-versus-enemy routine does
on a kill. Experiments cited as plain IDs are not in this vault. Unless marked,
the findings are PC static disassembly plus execution of the original
instructions at image bases `0x00400000` and `0x14000000`. Two cross-port notes
that compared these routines with the PS1 port, XPORT-20260909-011 and
XPORT-20261001-013, first gathered several of them; no PS1 address supports any
claim here.

## The shared pool

Two allocators, `0x0042AA50` and `0x0042B020`, share 64 records of 56 bytes
(0x38) at `0x00598CA8`, with cursor `0x00599B00`
([[EXP-20260908-013 - Seed auxiliary budget and distant carry]],
[[PC level authoring memory limits]]). Fields known so far:

| Offset | Field | First recorded |
|---|---|---|
| `+0x0C`, `+0x10`, `+0x14`, `+0x18` | velocity and gravity; for a homing shot `+0x10` is the target pointer and `+0x18` the heading | XPORT-20260909-011, EXP-20260914-016 |
| `+0x1C` | set to −1 by the allocator; a floor-flagged drop caches its floor here | XPORT-20261001-013 |
| `+0x20` | action, switched on by the pickup walker | XPORT-20261001-013 |
| `+0x22` | life | XPORT-20260909-011 |
| `+0x2C` | retirement action (0xB marks a gold projectile) | XPORT-20260909-011, XPORT-20261001-013 |
| `+0x2E` | when positive, the updater fades the tint over the last 16 frames | XPORT-20261001-013 |
| `+0x2F` | 6 also marks a gold projectile | XPORT-20261001-013 |
| `+0x33` | flags: bit 2 marks a record the pickup walker takes, bit 0x08 enables homing | XPORT-20261001-013, EXP-20260914-016 |
| `+0x34`..`+0x36` | RGB | XPORT-20260909-011 |

- **Throw.** `0x0043EB60` increments the player's owner count `+0x96`
  (`0x0059D9A6`) and dispatches a red-class shot through `0x0042B020`. The
  projectile class comes from the berry type `+0x97`, which is the selector
  `0x0059D9A7` ([[EXP-20260818-004 - PC confirmation of the berry-type selector 0x0059D9A7]]).
  See [[PC gameplay loop and player event sites]] for its single caller.
- **Retirement.** The pool updater `0x0042B1F0` retires a record through
  `0x0042A2E0` and decrements `0x0059D9A6`.
- **Landing drops.** The same updater lands floor-flagged drops with
  `0x004ABE00` at `y = floor - height*32`.
- **Overwriting.** The allocator can replace an unprotected live slot. A build
  that spawns several records per throw therefore needed a vacancy check and
  temporary protection of the occupied records (XPORT-20260909-011).
- **Selector census.** The first kind-3F tables of all 19 parsed original
  `LEVEL*/LEVEL*.DAT` files contain neither pickup selector 25 nor 26
  (`work/experiments/EXP-20260909-009/selector-census.json`).

## Aim and homing

First recorded in EXP-20260914-016:

| Locator | Role |
|---|---|
| `0x0043EBB8..0x0043EBE8`, `0x0043E870` | Non-green, non-purple primary throws make one initial aim calculation, with half-cone argument `0x0280`. It returns the heading and the vertical velocity, so red shots keep a native vertical auto-aim with target-dependent arcs. |
| `0x00428400` | Homing acquisition. It walks the active-actor list `0x0059D7E0` and takes the nearest eligible actor by squared X/Z distance. There is no rule that spreads a volley over several targets. [[EXP-20261012-004 - Homing target visibility bit]] shows that eligibility is the per-frame in-view bit 0x0001 with bits 0x80 and 0x20 clear. |
| `0x004284A6..0x004284CE` | The green successor allocation passes the chosen actor pointer as allocator argument 5 and a direction as argument 7. Disassembly shows template `0x10` as the eighth argument, which the decompiler hides through stack scheduling. |
| `0x0042B215..0x0042B338` | When `+0x33 & 0x08` is set, `+0x10` is a target pointer and `+0x18` a heading, instead of vertical velocity and gravity. Each projectile reads its own target. |
| `0x0042B278..0x0042B291` | A target with health `+0x6E == 0` or flags `+0x5C & 0x0880` shortens that projectile's life to 1. |
| `0x00429790`, `0x0042A2E0` | Native contact and retirement accept homing shots. |

- **Several targets at once.** Original updates of three homing records with
  explicit targets (two right, one left) moved two shots right and one left,
  each closer to its own target after twelve updates. A native contact fixture
  took two enemies' health from (10, 10) to (8, 9) and retired all three
  shots. All 18 cases passed at both bases. Stock acquisition from the same
  origin chose target 0 three times, so homing alone does not split a volley.
- **Speed differs.** Native homing moves at a sine-table velocity shifted by 3,
  while the red shot moves at three times a shift by 4, and homing changes the
  vertical motion. Turning a red-class shot into a homing one changes its
  speed and arc.
- **Pointer safety.** The update reads `+0x44` and `+0x74` of the target
  before its invalid-state test, so the native health and flag checks do not
  prove that a stored pointer is still safe.
- Not tested: actor destruction or reuse during flight, moving targets,
  obstacles, special enemies, long volleys and level transitions.

## Berry versus enemy `0x00429790`

First recorded in XPORT-20261001-013 and EXP-20261001-006, with damage values
from EXP-20261005-001 and EXP-20261005-002. [[FUNC-97C95BA5572D-0041B9F0]] holds
the kill and removal routine; [[FUNC-97C95BA5572D-0041EC40]] the actor
updater.

- **Walk.** `0x00429790` walks the active actors `0x0059D7E0` against the 64
  records at `0x00598CA8`.
- **Kill.** A killed actor gets `+0x6E` = 999 and `+0x5C` |= 0x880. The local
  `[esp+0x10]` holds the kill bits: 1 for any kill, and 2 when the projectile
  was gold (`+0x2C` = 0xB or `+0x2F` = 6).
- **Gold kill.** `0x00429DBE..0x00429DF5` pulses `0x00414860(0x00599AC8)`,
  sets `+0x62` = 0, lowers the enemies-left word `0x0059D99E`, calls
  `0x00415970(0x0059B5F8)` when it reaches zero, and spawns
  `0x0042AA50(x, y, z, 0x78, 0x19)`.
- **Every kill** then calls `0x0041B9F0(actor, 1)` at `0x00429E00`. An
  actor's `+0x62` of 0 makes the kill permanent; otherwise `0x0041EC40` counts
  it down and `0x0041BD10` resets the actor.
- **Damage per hit** (static, EXP-20261005-001): purple −3, gold −4, blue
  and green −2. Red is deflected when the target's flag 0x40 is set.
  Hardware hits on a 50-health creature came in −3 steps with the purple
  berry.
- **Immunity and flags** (static, EXP-20261005-002). Health 100 or more is
  immune (`cmp ax,0x64` at `0x00429C35`). Flag 0x80 makes a creature
  unhittable and 0x800 makes the contact routine ignore it (`0x0041CD7F`).
  Flag 0x04 is flying (it holds the target Y) and 0x40 deflects red.
- **Other writers of the count.** Boss level routines change `0x0059D99E`
  themselves: `0x004369B0`, `0x0043AD00` and `0x00438720`
  (XPORT-20261001-013).

## Pickup walker `0x004292C0`

The walker takes pool records with `+0x33` bit 2 and life `+0x22` > 0 and
switches on the action `+0x20`. Glyph type 0x78 has action 0x7B, which has no
case, so it takes the default at `0x0042951E`. The default retirement action
0xC spawns a type whose sprite is not loaded in every level
(XPORT-20261001-013); [[EXP-20261012-002 - Sprite table census]]
identifies it as type `0x40` on sprite entry `0x33`, absent in 8 of 19 engine
contexts. The walker also consumes the timed-protection pickups described in
[[PC gameplay loop and player event sites]].
