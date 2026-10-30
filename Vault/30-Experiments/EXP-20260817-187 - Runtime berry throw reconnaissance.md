---
type: experiment
id: EXP-20260817-187
date: 2026-08-17
question: 'Where does the PC port keep the thrown-berry projectile state, and which variable selects the berry type?'
status: partial
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; Wine under gamescope (640x480, nested X display :2); live Training session PID 57939, launched by the researcher, not by this agent
environment_version: objdump 2.46-3.fc44; xdotool 3.x; process_vm_readv/process_vm_writev
working_directory: /home/dev/ABLPC
configuration: read-only live memory reads plus synthetic keystrokes; later bounded target writes with explicit researcher approval; no debugger, no breakpoints, no watchpoints
artifacts: []
addresses:
  - "0x00598B10"
  - "0x00861C98"
  - "0x00861C8C"
  - "0x00598C00"
  - "0x00599A00"
  - "0x0059D910"
  - "0x0042EBC0"
  - "0x00464E10"
file_offsets: []
result: throw-bit-and-projectile-pool-confirmed-berry-type-selector-not-found
created: 2026-08-17T20:30:00
updated: 2026-10-02
tags:
  - re/experiment
  - re/runtime
  - re/input
  - research/coverage
---

# EXP-20260817-187 - Runtime berry throw reconnaissance

> Resolved 2026-08-18 by [[EXP-20260818-004 - PC confirmation of the berry-type selector 0x0059D9A7]]:
> the equipped berry-type selector is `0x0059D9A7` (KU-073).

## Date

2026-08-17.

## Question

Berries are the projectiles Flik throws at enemies; the retail game exposes red,
blue, green (homing), purple (mega-homing) and gold. Static analysis alone had
not located any of it. Where is the thrown-berry state on PC, and which variable
selects the type?

This packet answers the first half and **fails** the second. It is recorded
partial rather than completed.

## Binary SHA-256

`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.

## Environment

Fedora Linux 44. Wine under gamescope at 640x480, with the game on gamescope's
nested X display `:2`, window id `14680071`. Live Training session, PID `57939`,
running from `work/copies/BUGS_PC-full-disc/PC/BUGS`.

**The session was launched by the researcher, not by this agent.** Per
[[Agent Operating Manual#Runtime instance lifecycle]] it was adopted rather than
replaced, and no competing instance was started.

## Environment version

`objdump 2.46-3.fc44`; `xdotool`; Linux `process_vm_readv` / `process_vm_writev`.

## Working directory

`/home/dev/ABLPC`.

## Configuration

Two phases, both authorised explicitly by the researcher in-session:

1. **Read-only.** Live reads via `process_vm_readv` and synthetic keystrokes via
   `xdotool` into the game window. No ptrace attach, no breakpoints, no
   watchpoints, no writes.
2. **Bounded writes.** `process_vm_writev` into the projectile pool and into
   candidate bytes, on explicit instruction ("try adjusting the memory address
   and throw"). No code, register or execution changes. No `originals/` path,
   no game asset, no PS1 source modified.

Tooling was hand-rolled under the session scratchpad. `scripts/game-memory.py`
and `scripts/game-session.py` appeared in the working tree during this session
and are the sanctioned tools for this job; they were not used here because they
were not present when the work began.

## Procedure

1. Adopt the running session; audit the process table first.
2. Sample the action-bit words while the researcher pressed keys, to bind the
   static input model to observed values.
3. Verify synthetic keystroke injection reaches the game.
4. Differentiate memory activity across idle / walking / throwing.
5. Characterise the region that responds only to throwing.
6. Attempt to isolate the berry-type selector by held-value writes.

## Observed

### Confirmed

- **The throw action bit is `0x8000`.** Sampling `0x00598B10` (the raw action
  word produced by the binding walk in `0x0042EBC0`), `0x00861C98` (latched
  current) and `0x00861C8C` (previous frame) while Ctrl was pressed yields
  `0x8000` in all three, 248/248/247 samples. `0x0040` (back) and `0x0020`
  (right) appeared from movement. This binds the **static** model of
  `EXP-20260817-181`/`-184` — which derived `DIK_LCONTROL` scancode `0x1D` →
  mask `0x8000` from the default binding table — to observed runtime values, and
  they agree exactly.
- **`0x00464E10`-`0x00464E2F` is the input latch.** It copies `0x00861C98` to
  `0x00861C8C`, then reads `0x00598B10` into `0x00861C98` — the current/previous
  pair that the edge-detection idiom at `0x00413AAC` onwards consumes.
- **A projectile pool responds only to throwing.** Over
  `[0x00598F00, 0x00599A00)`, sampled across ten frames per condition: **idle 0
  dwords active, walking (Up x3) 0 dwords active, throwing (Ctrl x3) 38 dwords
  active.** Repeated with consistent results.
- **The pool has stride `0x38`.** Record starts observed at `0x00599640`,
  `0x00599678`, `0x005996B0`, `0x00599838` — successive differences `0x38`. Its
  extent is consistent with 64 records over `[0x00598C00, 0x00599A00)`:
  `0x00599680 - 0x00598C00 = 0xA80 = 48 * 0x38` exactly, so the observed records
  are slot-aligned to that base.
- **Record shape.** `+0x00`/`+0x04`/`+0x08` a position triple that advances
  smoothly then settles; `+0x0C`/`+0x10`/`+0x14` small signed values consistent
  with velocity; `+0x1C` is `-1` in 58 of 64 slots.
- **The pool is not the creature actor pool.** `[0x0059B628, 0x0059D728)` held 9
  occupied slots throughout and gained none across throws.
- **The pool has no absolute static references.** The only match for `0x599000`
  in the whole disassembly is a misaligned byte pattern inside a data table, and
  a scan of live memory found no global holding a slot-aligned pointer into the
  pool. It is addressed by a base computed inline — which is why static analysis
  had not reached it.
- **`+0x2C` is not the visible berry colour.** All 49 occurrences of its value
  `0x00710000` were rewritten to `0x00000071` and held continuously for 45s. The
  researcher observed **no visual change**. Negative result.
- **The engine owns these fields per frame.** Of 49 one-shot writes, 28 were
  reverted within 2s; a continuous rewrite (~4ms period) does hold.
- **`0x0059D918`, `0x0059D928`, `0x0059D968` are Flik position, not berry
  state.** They are the current, retained-preceding and auxiliary **Z**
  coordinates recorded in [[STRUCT-PC-FLIK-POSITION-GLOBALS]]. They changed on a
  jump because Flik moved. This was found only after they had been poked.

### Inferred

- That the stride-`0x38` pool is the **berry** projectile pool. The throw
  exclusivity is strong evidence that it carries thrown objects, but the pool
  demonstrably holds **more than one object class** (see below), so "berry pool"
  is a reading, not a demonstrated fact.

### Unknown

- **Which variable selects the berry type.** Not found. `KU-073`.
- The pool's exact base and slot count. `0x00598C00` with 64 slots fits the
  observed alignment but the bound was not proven.
- The throw handler and spawn code.
- What `+0x18`, `+0x28`, `+0x30` mean.

## What did not work, and why

Recorded because the failures are the useful part of this packet.

| Attempt | Why it failed |
|---|---|
| Diff memory across a throw, subtracting per-frame noise | A flying projectile **is** noise-like, so the filter removed exactly the target |
| Look for stably-zero dwords becoming non-zero (allocation signature) | A pooled slot is **reused, not zeroed**, so allocation never shows as zero→non-zero |
| Compare the **modal** record identity before/after a poke | ~57 stale berries dominate the mode; two fresh records can never shift it |
| One-shot write, then throw | The engine rewrites the field within ~200ms, so the value was gone before the throw read it |
| Per-throw identity fingerprint | The fields chosen include an age counter, and the pool holds several object classes, so every condition produced "new" identities — 25/25 false positives |

The common thread: **every oracle failed because there is no read-only signal
that distinguishes berry type.** Without the researcher's eyes on the screen or
a watchpoint, candidate testing has no ground truth.

## Outstanding state

The `+0x2C` tint test left **21 sites** written with `0x00000071` in place of
`0x00710000`; the engine reverted the other 28. Those slots have most likely
been recycled since, but the session was not returned to a pristine state. A
relaunch clears it. No `originals/` path, asset, or repository file was
modified.

## Interpretation

The runtime pass did what static analysis could not: it located a projectile
pool that carries no absolute references anywhere in the image, and it bound the
static input model to observed values. Both halves of the throw path's *entry*
are now solid.

The type selector is a different problem. It is one small value among ~3.6MB of
writable data, and the search needs an oracle this packet did not have.

## Follow-up

Two options, both recorded in `KU-073`:

1. **One hardware write-watchpoint** on a pool record, which would report the
   spawning instruction on the first throw and yield the type dispatch by
   reading code. Requires explicit approval under
   [[Agent Operating Manual#Dynamic analysis]].
2. **A labelled A/B** with the researcher naming the held berry colour before
   each sample, giving the diff a ground truth.

Cross-port structure for the same question is recorded separately in
[[XPORT-20260817-005 - Berry contact array and type marker shape]].
