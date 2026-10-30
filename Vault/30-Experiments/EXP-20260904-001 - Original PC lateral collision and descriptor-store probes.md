---
type: experiment
id: EXP-20260904-001
date: 2026-09-04
question: Can original PC instructions distinguish a vertical-triangle crossing and bound render-side direct descriptor stores without launching the game?
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux; Python 3.14.6; Unicorn 2.1.4; synthetic offline address space
result: original-instruction-lateral-response-confirmed-and-direct-stores-bounded-in-finite-fixtures
status: completed-offline
tags:
  - re/collision
  - re/experiment
---

# EXP-20260904-001 - Original PC lateral collision and descriptor-store probes

## Scope and reproducibility

This is original-instruction execution with synthetic inputs, **not a game
runtime experiment**. No Wine, 86Box, DuckStation, game, live debugger, wrapper,
process-memory action, screenshot, mapping change, or original-file write ran.
The user requested a better route toward terrain/collision understanding.

`scripts/terrain-collision-probe.py` loads only `.text` from the hash-checked
retail work copy `work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe`. Other mapped
memory is zero-filled, then explicitly seeded with synthetic data. No
decompiler code is translated into a replacement implementation. Code hooks
enforce instruction bounds; the descriptor slice has the explicit omission
below. Executable bytes and RAM dumps are not published.

- Probe SHA-256: `7f6fa6e0f8b07680247ee2f55db3ba36bed6e6351402f4810ff7edcc74d27e91`.
- Tests SHA-256: `3461c08a0c153c759f7c53f05e18cb2e945e430a71ff03f2d0533e6b5b225e33`.
- `.text` SHA-256: `4ff4c59215b473c8701edcfea9d10ee610108efe09bdfc5078d4ebcb6b3e318a`.
- Local result: `work/copies/EXP-20260904-001/instruction-results-001.json`,
  34,011 bytes, SHA-256
  `6b30a6960c59478eea972373b581b309eeba33d91a1c1f114e52688ceee998ed`.
- Reproduce: `.venv/bin/python scripts/terrain-collision-probe.py`.
- Regression: `.venv/bin/python -m pytest -q tests/test_terrain_collision_probe.py tests/test_terrain_height.py tests/test_terrain_all.py`:
  **70 passed**, including all 47 new probe tests; none skipped on this host.

The JSON contains 27 descriptor cases and 12 movement cases. Its instruction
visit-count hashes are sorted PC-frequency histograms, not ordered traces.
Missing retail bytes cause instruction tests to skip explicitly on other
hosts; a present but wrong binary is rejected, not substituted.

## Confirmed: PC has a lateral-response branch

Fresh raw disassembly and Ghidra queries agree on this original-code chain:

- `004ab1a0` collects movement candidates and iterates response up to three
  times. `004ab83e` calls thunk `00401456 -> 004aa4d0` on the nongrounded
  branch; grounded handling also uses `004aae30` and `004a9ba0` (not tested).
- `004aa4d0` computes full XYZ signed plane distances before and after the
  requested movement. A negative endpoint and nonnegative start can invoke
  triangle inclusion at `004a9860` (crossing block `004aa600..004aa743`).
- `004a9860` selects a projection from the dominant normal component and
  calls `004a9420` for directed edge tests. X-dominant normals use YZ; vertical
  triangles are not inherently excluded by a height-only projection.
- A hit changes XYZ position and residual movement; a `0xc0` (192) adjustment
  participates in the approach fraction (`004aa7bb..004aa849`). This is a
  PC instruction finding, not a borrowed cross-port conclusion. Do not treat
  192 as a universal final wall standoff: the fixture's measured distance is88.
- Normal Y below `-0x2000` takes a different response from the wall-like branch.
  A wall-like response returns2 and changes lateral residual/velocity. Pointer
  equality with contact record `007f3ea8` changes the response gain.

### Synthetic intervention and controls

Two planes through the origin, normals `(16384,0,0)` and `(0,0,16384)`, are
tested separately. Edges are 100 encoded units = 3,200 position units. For +X,
edge1 is +Z and edge2 +Y; for +Z, edge1 is +Y and edge2 +X. This order follows
the executable's directed edge tests, not an assumed cross-product convention.
The first exploratory ordering was rejected; it is retained as the explicit
reversed-winding negative control in the final probe.

Candidate count is supplied as0 or1 at `007fc8d4`, candidate pointer at
`007f3f50`, descriptor index0 at `007f2680`, descriptor base `(0,0,0)` at
`007f4590`. Separate line-segment count `007fc8e8` is zero. The **full callee
path** through `004aa4d0`, `004a9860`, `004a9420`, and `004a95e0` executes
unmodified, including retail thunks; there are no movement stubs or skips.

For both X and Z, the crossing-axis start is1024, delta−2048, and the other
coordinates512. Ordinary contact pointer is `007f3d68`:

| Case (each axis) | Final crossing coordinate | Return | Lateral residual / velocity |
| --- | ---: | ---: | ---: |
| Inside triangle, crossing | 88 | 2 | 1128 / 2064 |
| Candidate removed | −1024 | 0 | −2048 / −2048 |
| Moving away, delta+2048 | 3072 | 0 | 2048 / 2048 |
| Outside triangle, Y=6400 | −1024 | 0 | −2048 / −2048 |
| Reverse edge winding only | −1024 | 0 | −2048 / −2048 |
| Crossing, special contact `007f3ea8` | 88 | 2 | 16 / 16 |

The other coordinates do not change. These are one-call outputs, not final
coordinator or frame positions. Ordinary response reverses lateral movement
in this fixture; special contact does not use that same gain. No general
wall-sliding, walking, slope-threshold, or retail-level behavior is claimed.

### Binding to an already-observed player writer

Raw instructions independently establish:

`00414573` pushes player position `0059d910`; `00414578` calls thunk
`0040103c -> 0043f9e0`, whose `0043f9e6` loads that argument into ESI.
`00440849..00440851` passes slot0, `ESI+0x82`, `ESI+0x2c`, and ESI to
`0040120d -> 004ab1a0`. Slot0 selects contact `007f3d68` at `004ab82c`.
The coordinator copies the resulting XYZ back at `004ab889/004ab88f/004ab896`.

Existing independent runtime evidence, not a new run:
[[EXP-20260818-001 - Watchpoint path and first forensic tuple for Flik position]]
caught `004ab889 -> 0059d910` with the game's CR3 and matching retail bytes.
[[EXP-20260818-002 - Flight-recorder Phase 0 write-trace]] reproduces that
writer. Its Phase-0 log was overwritten: use the preserved Phase-1 log for
qualitative rechecking, **not** the historical Phase-0 counts.
`work/86box/logs/ablrec-phase1.txt` SHA-256
`f7f6562d1950de69fd8f5edbbe68f31c8e16fabbba0e581f704ecb2e4d26a374`
contains the same writer (e.g. line103) and `00440802 -> 0059d920`.

Thus the helper is connected to the player movement path. Neither the old
writer traces nor these synthetic cases establish which retail triangles were
admitted or that the lateral-hit branch ran during those historical frames.

## Confirmed, bounded: direct descriptor stores target N..N+19

`0044ca00` is called from render driver `0044d430`. The call at `0044d7a4`
has a **global** `005c5edc & 0x10 == 0` guard, not a type-`0x41` dispatch.
Its object array is `0059d9c0`, twenty records with stride48. Direct descriptor
stores form `48*(N+i)` with `N=DWORD[007f3d30]`, `i=0..19`:

- Creation requires nonzero object type, nonzero referenced resource header,
  object flag mask `0x02` at `+0x2e`, a signed-nonnegative template lookup from
  `007f29e8+2*type`, and a destination tag different from `type+0x67`.
- Nine stores per created slot: tag `+0x2c`, payload pointer `+0x10`, bounds
  `+0x14/+0x1c`, spans `+0x24/+0x28`, and position `+0/+4/+8`.
  Store PCs are `0044caa9`, `0044cab9`, `0044cad1`, `0044caea`, `0044caf6`,
  `0044cb02`, `0044cb08`, `0044cb11`, `0044cb17`.
- Bounds are source bound minus source base plus object position. Equal tag
  skips the copy: **this slice does not refresh position on that path**.
- Flag-clear or missing-template clears a nonzero tag at `0044cb45`, not the
  entire descriptor. A matching current contact also clears `0059d992`.
- Original loop epilogue `0044d1f3..0044d205` increments slot and object
  pointer to exclusive `0059dd88`, proving twenty direct-store destinations
  under valid initialized, nonwrapping arithmetic.

The probe starts at `0044ca19`, executes the prefix, and explicitly redirects
at `0044cb5d` to the original loop epilogue `0044d1f3`. It excludes the initial
transform helper, all rendering code/callees, and the prologue/return. This is
**not execution or a side-effect proof of the complete render function**.

Nine branch fixtures each run at N=1,64,668 with template0 and synthetic type1.
Each checks all700 descriptors (33,600 bytes), records actual descriptor-store
events, and checks all twenty visited slots and the contact flag. Creation
has180 stores, clearing has20, skip cases have0. All bytes below N and beyond
N+19 remain unchanged in these fixtures. This supplements the raw address
arithmetic; finite tests alone are not a universal alias proof.

Important limits from James's independent audit:

- `004a9019..004a904a` copies the count to N, adds32 to total, and clears32
  reserved tags. But N counts kinds6/7/8 across700 descriptors; this is not
  established as the high-watermark of all loaded static/template records.
- Source template indices are checked nonnegative, **not `<N`**. The initializer
  also clears mapped template tags at `004a9050..004a906d`. Do not claim that
  initialization globally preserves the prefix or every source lies below N.
- Direct-store locality does not prove render/collision independence through
  omitted callees, aliased payloads, or real template identities.

## Consequence and next discriminator

KU-080 is narrowed from "possibly height-only" to **a player-connected lateral
response exists; real candidate admission and gameplay behavior remain open**.
KU-081's direct target arithmetic is answered; full static/dynamic independence
is not. KU-079 (which mesh visibly draws ground) is unchanged.

Next offline packet: trace `004ab1a0` candidate admission back to the bounds /
bucket initializer and exact retail LEVEL01 `TERRAIN.ALL` cells; census vertical
normals and mapped template identities; then feed selected cells through
original candidate collection plus response with positive/negative controls.
Keep all raw unknown fields. Only then design the smallest authorized live
movement discriminator or a collision writer. R2q screenshot calibration is
not a prerequisite for this static/original-instruction investigation.

James independently rehashed a second retail copy, checked raw disassembly,
reproduced the original 27 descriptor / 10 movement cases, and returned bounded
ACCEPT. The final report adds the two special-contact cases and provenance
clarifications; exact final review and repository-gate status are recorded in
[[2026-09-04 1809 - Codex - Direct collision instruction pivot]].
