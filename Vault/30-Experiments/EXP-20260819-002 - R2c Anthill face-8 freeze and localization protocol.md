---
type: experiment
id: EXP-20260819-002
date: 2026-08-19
status: complete-inconclusive
question: Can a calibrated process freeze and an orthogonal guarded topology edit independently establish that Anthill Level01 face 8 contributes visible pixels?
binary_sha256: 1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f
pc_binary_sha256: 1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f
environment: Authorized build-scoped auto-hardware F0 under Wine/Gamescope/Xwayland; staged assets remain retail and no derived DAT has been written
inputs:
  - retail Anthill Level01 SHA-256 786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53
  - EXP-20260819-001 accepted A1/B/A2 evidence
evidence:
  - "[[EXP-20260819-001 - R2b Anthill static mesh causal runtime]]"
  - "[[EXP-20260818-008 - R2a Anthill static mesh causal candidate]]"
  - "[[EXP-20260818-007 - R1 static mesh consumer, round trip, and causal candidate]]"
result: James accepted the procedurally valid C1/L/C2 run and the fail-closed rejected comparator. R2c localization remains causally inconclusive; face-8 visibility and terrain identity are unconfirmed.
tags:
  - re/experiment
  - re/level-format
  - re/runtime-pending
updated: 2026-10-02
---

# EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol

> Outcome (2026-10-02 audit): run on 2026-08-19 on the auto-hardware build
> (DEC-20260819-155 superseded only the retail renderer clause); valid C1/L/C2
> run, rejected comparator, causally inconclusive. See **Successor packet** below.

## Result and boundary

This packet freezes the **next experiment**, not a causal runtime conclusion.
On 2026-08-19 the user explicitly authorized:

> I authorize EXP-20260819-002 R2c to run the retail-only F0 Direct3D
> calibration, applying SIGSTOP/SIGCONT only to the guarded owned bugs.exe PID
> at t0+3.300 seconds and taking the bounded read-only view snapshots specified
> in the protocol. If F0 passes, I also authorize creation of the guarded
> three-byte face-8 localizer work copy and the exact C1/L/C2 runs. No runtime
> memory or debugger writes are authorized.

The user later directed the work to use the demonstrated working route:

> correct. can you just get to anthill level01, which is just one right press
> then enter and enter again

and, after that exact auto-hardware navigation succeeded:

> okay, doing this, now do the work you need to do from before, do you remember?

This supersedes only the earlier **retail-only renderer-selection clause**.
The exact-PID `SIGSTOP`/`SIGCONT`, bounded read-only evidence, no-runtime-write,
and localizer-before-candidate boundaries remain unchanged. The active claim is
explicitly scoped to executed PC build
`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`.
A later controlled retail-executable intervention remains mandatory before any
retail behavior, visible-ground, or retail-R2 promotion.

The authorization covers exactly three read-only process-memory ranges: the
pre-title Level01 index at `(0x00861c84, 4)` and, only while stopped, the view
blocks `(0x005b58e0, 18)` and `(0x005bdb8c, 12)`. It covers no other process
memory. This explicit list resolves an audit ambiguity without expanding the
user's authorization.

F0-001 and F0-002 were rejected by the renderer gate. Later RC0 preparations
were rejected before RC0 input because of evidence-path, capture-target, or
content-drive preflight defects. None sent carousel/title input, `SIGSTOP`, or
`SIGCONT`; none read process memory or created a DAT. No F0 had run at that
historical boundary, and no derived DAT has been written.

RC0-F0-001 through RC0-F0-007 and their raw receipts remain unchanged as
historical fail-closed retail chooser/setup rejections. The branch is
**superseded by the user-directed auto-hardware R2c pivot**; it is not evidence
that retail launch is impossible or that either chooser label is a default.
`reimplementation/ablpc/r2c_rc0.py` remains historical tooling and is not an
active launch instruction.

## Active auto-hardware F0 amendment

The only next runtime command is the committed, argument-free executor:

```bash
.venv/bin/python scripts/r2c-f0-auto-hardware.py
```

It pins fresh stage
`/home/dev/ABLPC/work/copies/EXP-20260819-002/F0-auto-hardware-retail-009`
and pending evidence
`/home/dev/ABLPC/work/copies/EXP-20260819-002/evidence/pending/F0-AH-009`.
The staged `PC/BUGS/bugs.exe` must remain exact retail source hash
`97c95ba5...27b878`; the actual executed image is the canonical nonsymlink
cache `/home/dev/ABLPC/work/copies/auto-hardware/bugs.exe`, hash
`1e1d5099...a9c41f`. Receipts distinguish those identities before launch,
after process discovery, before title Return, and immediately before signal.

The executor also proves the accepted transform rather than trusting the cache:
file `0x000A6C6B` changes `ffd72b0534127f0099` to
`896c2410e9e2010000`; relocation entry file `0x000FA912` changes `6f38` to
`6f08`. Eleven bytes are covered, nine bytes differ, every other byte must be
identical, and applying the inverse must reconstruct the exact retail hash.
Every F0/C1/L/C2 arm must use this same executed hash, launcher arguments,
prefix, navigation, freeze, and capture procedure; only Level01 DAT may vary.

The navigation-only run at
`work/copies/manual-anthill-level01-20260819-001/` is feasibility evidence only.
It used the exact route `Right`, `Return`, `Return`, then was closed through an
accounted normal-close/group/device cleanup and a clear audit. It is not F0 and
must never be promoted or reused as an experiment arm.

After prelaunch acceptance, the first argument-free command attempt exited at
wrapper import with `ModuleNotFoundError: _bootstrap`. The immediately preceding
session audit was clean; no stage, game process, input, signal, process-memory
read, capture, or DAT write occurred. The wrapper now resolves the repository
root from `__file__` and directly adds `reimplementation/`, matching the
established RC0 wrapper. A subprocess regression proves the real entry point
imports successfully before rejecting an unexpected argument. This is a
prelaunch tooling rejection, not F0 and not a consumed runtime arm.

The subsequent `F0-AH-001` launch passed exact stage/cache/transform/`R:` and
complete six-marker Direct3D gates, then rejected before input because the
first main-window query returned zero matches. It sent no input or signal, read
no process memory, and wrote no DAT. The retained packet contains every cleanup
audit and a clean final state. James accepted this as a pre-input readiness
race: renderer completion can precede creation of the main `Bugs` window. Its
stage and evidence identities are consumed and must not be reused.

`F0-AH-002` then passed the same exact identity and renderer gates and retained
its final 3,580-byte `bugs.log` at SHA-256 `963676a9...f7740`. It rejected
before input after seeing two same-PID X11 windows. James accepted the packet
and cleanup, but found that the executor counted all same-PID Wine windows
before filtering main-window identity. The two historical IDs cannot be
classified further because that revision did not retain their properties.
`-002` is consumed; this is not a renderer failure.

`F0-AH-003` retained 485 window polls through the unchanged deadline. Every
poll contained same-PID XID `14680071`, title `Loading - A Bugs Life`, exact
`640x480`, plus only a 1x1 `Default IME` helper. Its log reached the complete
hardware gate and `ROUTINE : --- Start LevelSelect ---`; the run was not stalled.
It sent no input or signal and performed no memory read or DAT write. James
accepted the rejection/cleanup and identified the exact-title validator as the
defect. `-003` is consumed.

`F0-AH-004` passed retained-XID readiness and sent guarded Right then Return.
The index read `2.026975840 s` after selection Return was `0`, but the final log
still contained Level00 and LevelSelect with no Level01 load or
`Start ClearLoadScreen`. No title capture/Return, signal, stopped read, or DAT
write occurred. James accepted the rejection/cleanup as a navigation-readiness
failure, not a demonstrated index-timing race. `-004` is consumed.

`F0-AH-005` then passed the same build, renderer, retained-XID, LevelSelect,
and Level01/ClearLoadScreen gates and captured a genuine Anthill Level01 title.
Its full-frame PNG SHA-256 was
`9a6f8495c1df09a4c7a62bb9e6cd90c4254bf57cf094e1e73f0eb334ca1fd797`
and decoded-RGB SHA-256 was
`c528d5e47aa81f78186a9c88da52e2a95721efb916f9e0842ec0fcb1a4d15dac`.
Those differed from the independently reviewed A1/B and A2 title frames in
[[EXP-20260819-001 - R2b Anthill static mesh causal runtime]], so the executor
rejected before the level-index read, title Return, signal, stopped read, or DAT
write. James independently reviewed the retained image as the same Level One
title with ordinary nonidentity animation, accepted the fail-closed rejection
and cleanup, and prohibited adding its whole-frame hash to the allowlist.

Offline decoded-RGB comparison of all three reviewed title variants (the A1/B
reference, the A2 reference, and `F0-AH-005`) found two exact common identity
regions. First used by `-006`, these remain the only active automated visual
title gate for `-007`:

| Region | Bounds | Exact decoded-RGB SHA-256 |
|---|---|---|
| level title and welcome | `360x150+275+120` | `da63e76507dbfdcc6d49192c029bec1467be5554cdf3b2f3a900f4fee91eddb3` |
| objective text | `590x70+25+285` | `0ae2bd627d6baf3a0386112524ed8252517c291370a3179f94c3bd15d0c48efe` |

The gate bounds-checks decoded `640x480` RGB, requires both exact crop hashes
and the exact Level01/ClearLoadScreen log identities, and only then permits the
single authorized index read. The full PNG and decoded-RGB hashes remain
retained evidence, never selection criteria. A one-pixel change inside either
crop, wrong dimensions, an out-of-bounds crop, or either log mismatch rejects
before the index read, title Return, `SIGSTOP`, stopped reads, or DAT creation.
No screenshots or other game assets are committed to git; the three-reference
comparison provenance remains in the ignored experiment evidence trees.

`F0-AH-006` then passed the exact build/assets/Direct3D/navigation/title-region
gates, read level index `1`, set title-Return key-up
`t0=186924.270543049`, stopped the pidfd-bound process at `t0+3.300 s` within
microseconds, and found all 17 tasks in state `T`. All four authorized stopped
view snapshots are byte-identical. Its three stopped captures are also
byte-identical at PNG SHA-256
`05f5691cab126962715d94857fd5085f7013353b3982a7d6e9d350215506ad1c`
and decoded-RGB SHA-256
`2ea6564339c406cbcd92ca32faaf4e6c1b177119939aee569f0cfc1223b9d26c`.
They did not equal the retail R2b phase frame, so the run rejected, resumed,
cleaned, audited, and restored retail `R:` without any DAT, runtime-memory, or
debugger write. James accepted that rejection and cleanup. The difference is
18,613 pixels (6.05859%) with normalized RMSE `0.0223747`; visual review shows
the same camera/terrain and differences in animated entities. `-006` is
consumed and is not promoted retroactively.

### Offline camera-equivalence receipt

This durable receipt was generated from the retained files with
`read_png_rgb()` and exact row-major decoded-RGB crops. It uses no brightness
normalization, registration, optical flow, masking, or frame search.

| Input | Retained path | PNG SHA-256 | Decoded-RGB SHA-256 |
|---|---|---|---|
| retail A1 | `work/copies/EXP-20260819-009/evidence/accepted/A1-005/frame-14.png` | `4a5bfde15d2221e3fbe97334856d52cf13e25e99d8fab7c979dc8e921f62f88b` | `b8290da48f462b414857a26c89f0fe1f8486a6ffbaeeb106b04dbba829ab6451` |
| retail B | `work/copies/EXP-20260819-009/evidence/accepted/B-001/frame-14.png` | `4a5bfde15d2221e3fbe97334856d52cf13e25e99d8fab7c979dc8e921f62f88b` | `b8290da48f462b414857a26c89f0fe1f8486a6ffbaeeb106b04dbba829ab6451` |
| retail A2 | `work/copies/EXP-20260819-009/evidence/accepted/A2-001/frame-14.png` | `4a5bfde15d2221e3fbe97334856d52cf13e25e99d8fab7c979dc8e921f62f88b` | `b8290da48f462b414857a26c89f0fe1f8486a6ffbaeeb106b04dbba829ab6451` |
| derived F0 frozen 1 | `work/copies/EXP-20260819-002/evidence/rejected/F0-AH-006/frozen-1.png` | `05f5691cab126962715d94857fd5085f7013353b3982a7d6e9d350215506ad1c` | `2ea6564339c406cbcd92ca32faaf4e6c1b177119939aee569f0cfc1223b9d26c` |
| derived F0 frozen 2 | `work/copies/EXP-20260819-002/evidence/rejected/F0-AH-006/frozen-2.png` | `05f5691cab126962715d94857fd5085f7013353b3982a7d6e9d350215506ad1c` | `2ea6564339c406cbcd92ca32faaf4e6c1b177119939aee569f0cfc1223b9d26c` |
| derived F0 frozen 3 | `work/copies/EXP-20260819-002/evidence/rejected/F0-AH-006/frozen-3.png` | `05f5691cab126962715d94857fd5085f7013353b3982a7d6e9d350215506ad1c` | `2ea6564339c406cbcd92ca32faaf4e6c1b177119939aee569f0cfc1223b9d26c` |

All six inputs are exact `640x480` and yield the same four-region map:

| Production key | Bounds | Exact decoded-RGB SHA-256 |
|---|---|---|
| `upper-right-structure` | `160x100+480+0` | `41aa36449cae7e735d5476644f670d01eb931490484d22091da1647ad1852bf6` |
| `left-middle-structure` | `120x100+20+220` | `7a87a57c278e09861fada1511c7aac9dd10cfe607d109fb6b48696103998ab14` |
| `lower-left-structure` | `160x100+0+380` | `59e3593b7b487553a63483cf20134aef9be97dae6b73690e5f5ababa8e1541e0` |
| `lower-right-structure` | `160x100+480+380` | `8b859ecf3a245fff1b4f3aa064ffae3c8c9a4a2b19e791e39f09cd2e2f45760f` |

Receipt result: `all_six_region_maps_identical=true`. This is a fixed
camera/terrain equivalence gate, not full-frame phase identity and not face-8
visibility.

`F0-AH-007` reached title Return after the exact build/renderer/navigation/title
and index-`1` gates, establishing `t0=187477.192697015`. The packet has 80 total
main-window guard receipts; exactly 70 are post-`t0` freeze-interval iterations
(`011` through `080`), while the first 10 belong to navigation/title/input. The
last post-`t0` guard completed `64.291 ms` before the freeze deadline, but the
old in-memory aggregate focus receipt was lost on rejection. Final process
identity completed `4.346 ms` before the deadline. The subsequent full XID
guard consumed most of that budget before its geometry subprocess launched
with a `0.255 ms` timeout budget and timed out. No `SIGSTOP`, stopped read,
frozen capture, DAT creation, or
runtime/debugger write occurred; cleanup and retail `R:` restoration are clear.
James accepted this consumed scheduler rejection. It is not a second derived
whole-frame identity because no frozen frame exists.

`F0-AH-008` rejected during runtime-identity discovery, before the renderer
gate or any input. Discovery temporarily accepted a candidate, but the
immediate after-discovery guard reported only that the guarded identity had
changed. The old executor retained neither each discovery candidate nor a
field-level comparison, so the changed field cannot be recovered and must not
be inferred. It sent no input or signal, read no process memory, captured no
frame, and made no DAT/runtime/debugger write. Launch-group/device cleanup and
retail `R:` restoration were clear. Its evidence remains in `pending`, rather
than `accepted` or `rejected`, because the old cleanup path incorrectly treated
the pre-renderer absence of `bugs.log` as a cleanup failure. This is an
unclassified pre-action tooling rejection, not renderer, navigation, or game
behavior evidence.

Fresh `F0-AH-009` keeps every scheduler, structural-region, and derived-frame
gate unchanged. Before assigning the guarded game, it atomically persists
every launch-group `bugs.exe` candidate with exact PID, start ticks, process
group, command, cwd, timestamp, and field-level difference. Startup command or
cwd mutation may continue only while PID/start/process-group remain identical;
immutable replacement, disappearance after observation, multiple candidates,
or persistent instability rejects before any input. Assignment requires two
consecutive identical observations of the exact final command and cwd. After
the first observation, the raw current identity for that exact PID is retained
and compared before candidate filtering, so PGID or command-shape drift cannot
collapse into an unsupported disappearance claim. Both the post-snapshot
observation time and the completed receipt cycle are checked against the
absolute pre-Return deadline before assignment; crossing it forbids every later
action. A
missing `bugs.log` before entry into the renderer/log gate receives an explicit
phase/path/timestamp/absence receipt and does not itself make cleanup unclear;
missing it after that gate remains a cleanup failure. Periodic focus sampling
still stops at `deadline-0.060`, the final full guard remains bounded to
`deadline-0.003`, and the final 3 ms remain exclusively for pidfd signal
scheduling. `-009` requires exact dimensions, all four structural hashes,
triplicate stopped-frame identity, and exact reproduction of the derived
`-006` PNG/RGB pair above. Another whole-frame identity with passing structural
regions ends hash extension and requires a preregistered state predicate or
dynamic-pixel mask. At protocol freeze, localizer creation remained prohibited
until a fresh F0
passes and James accepts it.

## F0-AH-009 calibration result

The committed executor returned `accepted-f0` for
`work/copies/EXP-20260819-002/evidence/accepted/F0-AH-009/`. This is a passed
freeze calibration at executed build
`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`,
not a face-localization or retail-behavior result.

- staged retail exe, Level01 DAT, and `CD.TXT` matched their frozen hashes;
  the executed cache transform covered exactly 11 bytes, changed exactly nine,
  and inverted to retail hash `97c95ba5...27b878`;
- runtime identity stabilized at PID `937066`, start ticks `18910330`, process
  group `936814`, the exact cache command, and the exact `-009` stage cwd;
- all six Direct3D markers passed with no software terminal marker; exact
  Level01 load/ClearLoadScreen markers passed; the title identity regions
  passed; and the authorized index read at `0x00861c84` returned `1`;
- pidfd `SIGSTOP` targeted only PID `937066` at `t0 + 3.300000000 s`; absolute
  deadline error was `0.0000008320203050971031 s`, below the `0.001 s` gate,
  and all 17 task states were `T`;
- the two authorized stopped view blocks remained constant at SHA-256
  `1885ce2c...ada8a8` and `a97fc507...73516` through all three captures;
- all three exact `640x480` captures were byte-identical PNG
  `05f5691c...506ad1c`, decoded RGB `2ea65643...23b9d26c`, reproduced all four
  frozen structural-region hashes, and visually show non-faded Anthill Level01
  gameplay;
- pidfd `SIGCONT` resumed the guarded process. Normal close left residual
  Wine/audio state, so the retained lifecycle continued through group TERM,
  group KILL, and exact residual-device cleanup. The final retained audit and
  the independent post-run audit are clean; retail `R:` is restored;
- `runtime_memory_write`, `debugger_write`, and `DAT_write` are all `null`.

The result freezes this derived-build control reference. It does not establish
that face 8 is visible, terrain, or ground; it does not validate the localizer;
and it does not close retail R2. James accepted the committed F0 result. The F0
condition for localizer creation is satisfied, but the separately committed
creator/executor/comparator packet below must itself be accepted before the DAT
is written or C1 launches.

No runtime memory write or debugger write is requested. `SIGSTOP` and
`SIGCONT` are execution-control perturbations and must be named explicitly in
the authorization; they are not treated as passive observation.

This packet deliberately stops before the EXP-008 one-byte vertex candidate.
The localizer result must be documented, committed, and accepted by James
before a separate candidate-successor packet can be prepared or launched.

## Why R2b failed and why `t0 + 3.300 s` is frozen

R2b compared every pixel across a fade-in interval. The accepted retail frames
show the same camera while the image changes from globally dark at
`t0 + 0.500 s` to fully bright. At frame 14, captured at `t0 + 3.300 s`, A1 and
A2 are decoded-RGB and PNG identical. The B frame is also identical to both.

The frozen retail **phase reference** is therefore:

| Item | Value |
|---|---|
| dimensions | `640x480` |
| deadline from title-Return keyup completion | `3.300000000 s` |
| PNG SHA-256 | `4a5bfde15d2221e3fbe97334856d52cf13e25e99d8fab7c979dc8e921f62f88b` |
| decoded RGB SHA-256 | `b8290da48f462b414857a26c89f0fe1f8486a6ffbaeeb106b04dbba829ab6451` |

This is not a build-independent whole-frame identity. No later wait, favorable
frame search, brightness normalization, image
registration, optical flow, or candidate-derived synchronization is allowed.

## Exact independent face-8 localizer

The retail chain remains:

`primary[81] @ 0x1b58 -> object 0x4860 -> geometry 0x188cc`.

The geometry has tag `0x0060`, 83 vertices, and 10 quad faces. Face 8 starts at
`0x18d38` and contains vertex-byte-offset tuple
`(300,312,264,324)`, selecting vertices `(25,26,22,27)`. Its exact 16 bytes are:

`2c 01 38 01 08 01 44 01 3f c0 00 c0 00 ff 3f ff`.

The localizer degenerates only face 8 to `(300,300,300,300)`, making both
triangles zero-area without changing a count, size, pointer, vertex, field word,
or other face:

| Physical offset | Retail | Replacement |
|---|---:|---:|
| `0x18d3a` | `0x38` | `0x2c` |
| `0x18d3c` | `0x08` | `0x2c` |
| `0x18d3e` | `0x44` | `0x2c` |

The hypothetical derived SHA-256, computed in memory without writing a file,
is `9942e252028b198dd0c16c6e45a1584620244f7dd9d9aeabe9a53bc04bd11bfd`.

This topology mutation is orthogonal to the one-byte component edit. It makes
no claim about coordinate axes, world scale, colour, UV, material, or tag
semantics.

## Guarded implementation

`LevelDat.set_static_mesh_face_vertex_byte_offsets()` is the only permitted
creator. It requires and verifies:

- the section and record index;
- exact expected object and geometry offsets;
- face index and triangle/quad arity;
- the exact original tuple;
- integer, 12-byte-aligned replacement offsets within the vertex array;
- a reconstructive reparse preserving the object/geometry chain and producing
  the requested face tuple.

Synthetic triangle and quad tests cover byte locality, reconstructive reparse,
identity mismatch, tuple mismatch, arity mismatch, alignment, range, and face
index rejection. A raw byte patch is prohibited.

F0 passed and James accepted its committed result. The next creator is the
argument-free `scripts/r2c-create-face8-localizer.py`; it is frozen to retail
source
`work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL01/LEVEL.DAT` and initially
absent ignored output
`work/copies/EXP-20260819-002/localizer-face8-001/LEVEL.DAT`, with adjacent
`creation-receipt.json`. It accepts no path or edit arguments. It builds only
through this API, requires the exact source/derived hashes and three physical
changes above, reparses, preserves size, writes DAT plus receipt into a
temporary sibling directory, and atomically publishes the complete directory.
Any extra changed byte rejects the localizer. Do not execute it until this
post-F0 packet is committed and James-accepted.

## Renderer setup evidence and bounded amendment

Chooser screenshots prove only temporal stability. They do **not** identify
the selected renderer, even when a hash recurs before or after a directional
input. The `b340...` and `cb3f...` image-hash observations are retained only as
forensic facts and cannot select or interpret an arm.

| Setup | Frozen input | Log-classified result | Boundary |
|---|---|---|---|
| F0-001 | one Down, then Return | software: `SYSTEM MEMORY ONLY`, `320x200`, `INITSOFTRENDER` | rejected before carousel input, signal, memory read, or DAT write |
| F0-002 | one Down, then Return | software: `SYSTEM MEMORY ONLY`, `320x200`, `INITSOFTRENDER` | rejected before carousel input, signal, memory read, or DAT write |

The later fresh RC0 preparation attempts did not consume RC0 because no
renderer Return was sent:

| Setup | Rejection | Boundary |
|---|---|---|
| preexisting `RC0-F0` namespace | freshness guard found unexpected paths | no copy, audit, launch, or input |
| RC0-F0-001 | incorrect Anthill host-path matcher | no audit, launch, or input |
| RC0-F0-002 | mistook the owned `177x63` transient setup window for the renderer chooser | no directional/Return input, signal, read, or DAT write; clean final audit |
| RC0-F0-003 | per-arm stage was not mapped in the launcher's Wine prefix; user saw the CD prompt | `bugs.log` recorded `App run from .`, a drive-less `\cd\cd.txt` load, and the fatal missing-file/CD path; no directional/Return input, signal, read, or DAT write; clean final audit |
| RC0-F0-004 | passed the exact installed-layout path gate and reached the owned `640x480` `Bugs` chooser, but interactive ImageMagick root capture waited until the 60-second chooser timeout selected software | no directional/Return input, signal, read, or DAT write; not RC0; clean final audit |
| RC0-F0-005 | passed source/prefix/CD/PID/window gates, but the frozen `ffmpeg` backend captured the rootless Xwayland black root; receipt/guard failures then allowed chooser timeout | no directional/Return input, signal, read, or DAT write; not RC0; guarded normal-close/group/device cleanup; clean final audit |
| RC0-F0-006 | passed source/prefix/CD/PID/window gates, then captured two startup/fade transitions followed by the already-known stable chooser | no Return or directional input, signal, read, or DAT write; not RC0; guarded normal-close/group/device cleanup; clean final audit |

The exact RC0-F0-003 cause is prefix scope. The launcher used
`/home/dev/ABLPC/work/wine/baseline`, but the attempted setup repointed
`$HOME/.wine/dosdevices/r:`. The accepted R2b arms instead loaded
`R:\PC\BUGS\cd\cd.txt` through
`work/wine/baseline/dosdevices/r:`. The baseline link was restored to the
retail full-disc tree after the rejection.

The retained RC0-F0-004 `cd-gate.txt` is preserved as written, but its
`rejection_markers=absent` label is false: `bugs-final.log` contains
`No CD-ROM found` at lines 16 and 83 while successfully loading
`R:\PC\BUGS\cd\cd.txt` at lines 17 and 96. The retained
`cd-gate-interpretation.txt` corrects that receipt without rewriting it.
`No CD-ROM found` alone is nondiscriminating. The fail-closed discriminator is the
installed-layout identity: require both `LOADING : App run from R:\PC\BUGS.`
and `LOAD : Loading file R:\PC\BUGS\cd\cd.txt.`; reject the drive-less
`LOAD : Loading file \cd\cd.txt.` fallback, fatal missing-file/CD prompt, or
absence of either required identity.

RC0-F0-004 independently established the window lifecycle: the owned
`177x63` `A Bug's Life` window is transient setup UI and is replaced by the
same PID's owned `640x480` `Bugs` chooser. RC0-F0-005 then disproved the
`ffmpeg` X11-root backend: its live `chooser-1.png` is uniform black, with PNG
SHA-256 `724319c36b0ea551aa309b59afed2e46bb1255b254b235f4dcfc77d96f1c6931`
and decoded-RGB SHA-256
`0b150fd32588b1daca5569992ebe559c0102c837306b1af4c44d35128ec58366`.
Both `capture-fixture-002` images are byte-identical to that black frame. The
fixture proved only command completion against the rootless Xwayland black
root, not capture of game pixels. Preserve it as disproof; neither `ffmpeg`
X11-root nor either ImageMagick path may be used for R2c.

The established compositor backend is restored:

```bash
GAMESCOPE_WAYLAND_DISPLAY=gamescope-0 \
  gamescopectl screenshot /canonical/absolute/initially-nonexistent/frame.png
python3 scripts/wait-for.py file \
  --path /canonical/absolute/initially-nonexistent/frame.png \
  --stable-ms 200 --poll-ms 20 --timeout 10
```

`gamescopectl screenshot` returns before the file necessarily exists, so the
committed file-exists/size-stable wait is mandatory. Each pre-input image must
decode as non-uniform RGB at exactly `640x480`, reject both known black hashes,
and match one of the retained genuine chooser decoded-RGB identities:

- no-direction chooser: `5b203faf56d00aef3bd94b3c1136911cc37e31d486021c2b79598bb2513752c7`
  (retained PNG `b340afa0...6727bb`);
- post-Down chooser: `a073f9da15536243f36366a5cad3b87aae911c1a5cd80967150dae98852a6ff7`
  (retained PNG `cb3f4b2d...25eee`).

Those hashes establish only that a known chooser image is present. They never
identify its selected renderer. RC0 still requires three captures one second
apart to be both byte-identical and decoded-RGB-identical. A black, wrong-size,
unstable, or unknown image stops before Return.

The retained RC0-F0-004 `chooser-guard.txt` incorrectly calls transient window
`14680065` `owned_selector_window`; `window-transition.txt` and `session.env`
correctly identify `SELECTOR_WINDOW=14680071`. Preserve that discrepancy. A
fresh guard must resolve the current `SELECTOR_WINDOW`, require that exact
window to be named `Bugs`, be `640x480`, and belong to the recorded guarded
game PID before any capture or input.

RC0-F0-005's raw packet is classified under
`work/copies/EXP-20260819-002/evidence/rejected/RC0-F0-005-black-root-capture/`.
It preserves the malformed receipt command, the over-broad preliminary-marker
guard, the timeout-selected software log, every non-clean cleanup audit, the
exact group/device cleanup provenance, the final clear audit, and retail `R:`
restoration. It did not consume RC0.

RC0-F0-006 is retained under
`work/copies/EXP-20260819-002/evidence/rejected/RC0-F0-006/`. Its captures are
a startup sequence, not a new chooser identity: `chooser-1.png` is a two-color
white/black transition (decoded RGB
`9124b62c96bb246f339cb4252f575402b670bf2e0dbafe3082e77a68a13d6413`),
`chooser-2.png` is a darkened transition (`64a124c5...94359`), and
`chooser-3.png` is the already allowlisted stable no-direction chooser
(`5b203faf...752c7`, PNG `b340afa0...6727bb`). Neither transition hash is
allowlisted. The executor rejected before Return and retained an accounted
cleanup through a clean final audit.

No further ad hoc shell assembly is permitted. The committed
`scripts/r2c-rc0-executor.py` owns path freshness, retail hashes, prefix and CD
identity, PID/window ownership, asynchronous compositor capture, strict image
gates, the exact no-direction Return, complete renderer-log classification,
receipts, cleanup guards, and retail-link restoration. The next frozen command
is:

```bash
.venv/bin/python scripts/r2c-rc0-executor.py
```

The executor accepts no path arguments. It pins exact source
`/home/dev/ABLPC/work/copies/BUGS_PC-full-disc`, exact new stage
`RC0-F0-retail-007`, exact new pending packet `RC0-F0-007`, and exact prefix
`/home/dev/ABLPC/work/wine/baseline`; every deviation rejects before copy,
mapping, or launch. Baseline `R:` must resolve to retail before remapping.
`gamescopectl` itself has a `3.000 s` subprocess deadline, separate from the
asynchronous `10 s` file-settle wait.

One absolute deadline runs from launch to Return: `45.000 s`, safely below the
chooser's observed 60-second timeout. After the exact CD/window gate, the
executor waits a fixed `4.000 s` with no input while polling the same guarded
PID/window and rejecting terminal renderer evidence. Only then does it take
the three one-second-spaced captures. Every compositor command receipt is
written atomically immediately after that capture, and the dimensions,
PNG/decoded-RGB hashes, non-uniform flag, black-root flag, and chooser-presence
allowlist result are written before triplet acceptance. Deadline expiry,
unknown/transient pixels, instability, wrong dimensions, black pixels, or
terminal renderer evidence rejects before Return and invokes guarded cleanup.

The executor does not use fixture-only `scripts/send-keys.py`. After capture it
runs the direct PC-autonomous sequence: guarded `windowactivate --sync`,
`windowfocus --sync`, focused-window plus PID/window recheck, XTEST `keydown
Return`, requested host sleep `0.180 s`, and `keyup Return` in `finally`. The
receipt retains every command/result and measured timestamps. Staged executable,
Level01 DAT, and `CD.TXT` hashes are rechecked immediately before Return.
Every handoff or rejection disposition also records
`return_keydown_attempted`, `return_keydown_completed`,
`return_keyup_completed`, and `return_delivery_status` as one of
`not-attempted`, `failed-before-keydown`, `attempted-ambiguous`, or
`completed`. Any attempted or ambiguous Return consumes the pre-input boundary
and must never be described as an unconsumed setup.

The executor leaves only a complete hardware-classified process alive for
same-process F0. Immediately before handoff it again requires the exact live
PID/start/PGID/cmdline/cwd, current same-PID `640x480` `Bugs` window, stage
mapping at baseline `R:`, and all three hashes. Software, mixed/incomplete
evidence, capture-command timeout, or any guard failure is closed fail-closed
and cannot graduate; a cleanup failure leaves the packet in `pending`. The
complete handoff receipt is written before the final non-failing
`handoff=True` transition; a receipt failure cleans/restores and remains
pending.

The ignored raw packets are retained under
`work/copies/EXP-20260819-002/evidence/rejected/`. Each setup has an accounted
clear final post-close audit. These results reject another blind deterministic-
Down retry and freeze exactly two possible fresh renderer calibrations:

1. **RC0, no direction:** use a fresh retail-only process and work copy, an
   immediate clear pre-audit, exact executable and DAT hashes, exact owned
   PID/window guards, a fixed `4.000 s` no-input settle, and three byte-identical
   chooser captures spaced one second apart within the absolute `45.000 s`
   launch-to-Return deadline. Send no directional input. Send Return with the frozen
   XTEST keydown -> requested host sleep `0.180` -> keyup mechanism.
2. Classify RC0 only from the complete log. Hardware requires every existing
   six-marker Direct3D marker and no rejection marker. Software requires the
   complete software rejection markers. Chooser pixels are never part of the
   classification. The preliminary `Native software render mode is FALSE`,
   `RenderMode set to Direct3d render mode`, and `Screen mode 640x480x16
   selected` lines are insufficient: before Return, only terminal
   `OnlySystemMemory`, `D3DAPPCREATE : Mode set`, `INITSOFTRENDER`, or
   `Starting Direct3D` evidence proves that renderer creation already ran.
3. If RC0 proves hardware, do not restart. The same guarded process graduates
   directly into F0 and continues through carousel, title, level-index,
   `t0 + 3.300000000 s`, signal, read-only snapshot, capture, resume, and close
   gates below.
4. If RC0 proves software, send no carousel/title input, signal, process-memory
   read, or DAT write. Close it and require the cleanup and final clear audit
   below before RC1.
5. **RC1, sole fallback:** use a new fresh retail-only process and work copy
   with every RC0 guard. Send exactly one Down through the frozen mechanism,
   wait `1.000 s`, optionally retain a forensic screenshot, then send Return
   through that mechanism. Classify only from the complete log. Hardware
   graduates in-process into F0; software stops EXP-002. There is no third
   renderer attempt and no image-hash inference.

For a rejected RC process, first attempt bounded normal Alt+F4. If it fails,
retain the unclear audit, revalidate the exact recorded PGID, and terminate only
that owned launch group. Retain the next audit. A residual Wine device may be
terminated only after recording PID, `/proc/<pid>/stat` start tick, and process
name provenance showing it appeared after the clean pre-audit. Retain every
cleanup step and require a final clear audit before any next launch.

## Active auto-hardware launch and identity contract

F0, C1, L, and C2 each use a new, initially nonexistent absolute evidence
directory and a fresh staged game directory. Never source a prior
`session.env` and never reuse R2b artifacts.

The argument-free executor owns evidence namespace setup: it validates the
canonical existing `evidence/` root, safely creates canonical nonsymlink
`accepted/` and `rejected/` directories when absent, and then requires both
final arm destinations to be initially nonexistent. No out-of-band directory
creation is a launch prerequisite.

Every launch incorporates the already accepted renderer, carousel, title, and
level-index procedure from
[[EXP-20260818-008 - R2a Anthill static mesh causal candidate#Authorized R2b procedure]]
with these unchanged gates:

- before the immediate pre-launch audit, expose the exact arm full-disc stage
  through `/home/dev/ABLPC/work/wine/baseline/dosdevices/r:` and verify its
  resolved target, the baseline `user.reg` entry `"r:"="cdrom"`, and staged
  `PC/BUGS/CD/CD.TXT` SHA-256
  `6ceffd34caf1b53332d76b344864bed1fbcd71ef1415312db9ed995fcd91a74d`;
- pass that same baseline prefix and the mapped stage's `PC/BUGS` directory to
  `play-pristine.sh`; a mapping under `$HOME/.wine` is irrelevant and rejected;
- immediate clear `make session-audit` before launch;
- exact staged retail executable source hash **and** exact actual executed
  auto-hardware cache hash `1e1d5099...a9c41f`;
- the arm-specific exact Level01 DAT hash;
- `play-pristine.sh --auto-hardware`; no chooser input or chooser screenshot is
  expected, and the historical RC0/RC1 gates do not apply;
- require both `LOADING : App run from R:\PC\BUGS.` and
  `LOAD : Loading file R:\PC\BUGS\cd\cd.txt.` in the new log;
  `No CD-ROM found` alone is nondiscriminating, while the drive-less `LOAD : Loading file
  \cd\cd.txt.` fallback, fatal missing-file/CD prompt, or absence of either
  required identity rejects the setup;
- complete six-marker hardware-Direct3D log gate and no software rejection
  marker;
- within the unchanged absolute launch budget, poll the still-guarded game
  process and renderer log; first retain every same-PID window's ID, exact name,
  geometry, and `_NET_WM_PID`, then partition the observation;
- initial readiness requires exactly one same-PID `640x480` window titled
  `Loading - A Bugs Life`; the 1x1 `Default IME` is a retained non-main helper;
- persist that exact initial XID as the only later input/focus target; never
  rediscover or substitute another window;
- every later guard rechecks the retained XID, PID, geometry, process identity,
  and title. The only allowed titles are `Loading - A Bugs Life` and `Bugs`;
  every transition is retained. Unknown title, XID replacement/disappearance,
  geometry/owner drift, or more than one qualifying main window rejects before
  the next action;
- process-identity drift is receipted before rejection with expected/current
  identity, retained XID, `process-identity-drift` disposition, and an explicit
  skipped-window-observation reason; no window query or input follows it;
- atomically retain every poll's complete observation set, exact-candidate IDs,
  non-main IDs, malformed IDs, and disposition before applying its verdict;
- retain the complete hardware/main-window readiness receipt and use that
  exact retained XID for every later focus and input guard; inherited
  exact-`Bugs` window discovery is prohibited in the auto-hardware branch;
- after hardware/XID readiness, send no input until the live log contains exact
  `ROUTINE : --- Start LevelSelect ---`; retain its observation time and complete
  a fixed `1.000 s` no-input settle under retained-XID guards before Right;
- after guarded Right, fixed `1.000 s` settle, and guarded selection Return,
  poll only the log for both exact Level01 load and
  `ROUTINE : Start ClearLoadScreen.` within a fixed `10.000 s` navigation
  deadline also capped by the original absolute launch budget;
- missing markers classify navigation failure and prohibit title capture,
  title Return, memory read, and signal;
- only after both markers pass, capture and verify a reviewed Level One title,
  revalidate the complete process/retained-XID identity, and perform exactly one
  authorized `(0x00861c84, 4)` read. A value other than `1` is a
  state-consistency failure after log/title proof, not a timing assumption;
- marker observation and poll count are atomically receipted as
  `validation-pending` before any XID guard or settle; every guard uses the
  remaining navigation budget, the fixed settle starts only if its full second
  remains, and explicit post-guard/post-settle checks reject deadline overruns
  before Right, title capture, memory read, title Return, or signal;
- Training -> one Right -> Anthill -> Return;
- exact Level01 log identities `LOAD : Loading file
  R:\PC\BUGS\cd\level01\level.dat.` and `ROUTINE : Start ClearLoadScreen.`,
  plus a `640x480` title capture matching one independently reviewed
  PNG/decoded-RGB pair: `46680a32...7e913` / `301cc412...bdbf5` or
  `dd04f705...3cec` / `7b86f10e...2e330`;
- an immediate complete process/window/cache/stage identity guard, followed by
  the authorized read-only `(0x00861c84, 4)` level-index read and required
  value `1`, all before title Return;
- title Return keyup completion defines monotonic `t0`;
- no further key or pointer input and continuous owned-window focus;
- `End ClearLoadScreen`, `End InitMainGame`, and `NextLife` before accepting a
  stopped frame;
- normal close after resume and an immediate clear post-close
  `make session-audit` before any next launch, followed by restoration and
  verification of the baseline-prefix `R:` link to
  `work/copies/BUGS_PC-full-disc`.

Any wrong renderer, level, file hash, focus, log marker, title, index, timing,
window, dimensions, or audit rejects the arm. A rejected arm never enters the
accepted namespace.

## Exact PID and execution-control guard

Identify the one owned `bugs.exe` PID after title load and freeze these receipt
fields before title Return:

- PID and `/proc/<pid>/stat` start-time field;
- session leader and owned process-group ID;
- `/proc/<pid>/cwd` equal to the exact staged `PC/BUGS` directory;
- NUL-decoded `/proc/<pid>/cmdline` naming the canonical auto-hardware cache
  executable, never the staged retail source executable;
- `/proc/<pid>/exe` link;
- both the staged retail-source hash and actual executed-cache hash;
- proof that this is the only `bugs.exe` in the owned process group.

Immediately before signaling, compare every field again. Open a Linux `pidfd`
for that verified process and retain PID/start-time/pidfd provenance. At
monotonic deadline `t0 + 3.300000000 s`, record request timestamps, require
absolute deadline error no greater than `0.001 s`, and send `SIGSTOP` only via
that `pidfd`. Never fall back to a numeric-PID signal and never signal the
process group, session leader, Gamescope, Xwayland, or Wine server. Poll and
retain same-PID `640x480` window ownership and focus continuously from title
Return through the final pre-signal guard; any loss rejects without refocusing
or signaling. Every `xdotool`/`xprop` ownership or focus query in this interval
is capped by the remaining `t0 + 3.300000000 s` budget and a small per-call
limit. A hung query therefore rejects before `SIGSTOP` and enters normal
cleanup/restoration rather than stranding the process.

Poll `/proc/<pid>/status` and every `/proc/<pid>/task/*/status`; all tasks must
report stopped state `T`. Retain the raw states and timestamps. After evidence
capture, compare the identity guard again, send `SIGCONT` to that PID, and
confirm no task remains in `T` before normal close. Any PID reuse, identity
drift, unexpected task state, failure to resume, or signal sent to another
process rejects the arm.

## Exact authorized read-only receipt

Before title Return, and only after an immediate complete live-identity guard,
read exactly:

| Address | Length | Phase | Acceptance |
|---|---:|---|---|
| `0x00861c84` | 4 bytes | pre-title | little-endian level index equals `1` |

While each process is stopped, take read-only snapshots through
`/proc/<pid>/mem` of only the already bounded blocks:

| Address | Length | Phase | Static evidence boundary |
|---|---:|---|---|
| `0x005b58e0` | 18 bytes | stopped | nine signed fixed-point matrix words |
| `0x005bdb8c` | 12 bytes | stopped | three stored origin dwords |

No fourth range, widened read, runtime write, or debugger write is authorized.

Take one snapshot immediately after stopped-state confirmation and one after
each screenshot. Retain raw bytes, SHA-256, address, length, PID/start-time
guard, and timestamps. The four snapshots must be identical within an arm and
the two block hashes must match across C1/L/C2. These are camera-equivalence
gates only; they are not a face projection or occlusion proof. Do not read
`0x005bdbac` or expand either range without a new static bound and amended
protocol.

## Stage 1 - auto-hardware build-scoped F0 calibration

F0 uses retail Level01 assets but executes exact auto-hardware build
`1e1d5099...a9c41f`. It is not a C1/L/C2 arm or independent sample, but its
accepted derived RGB, PNG evidence, view hashes, and structural hashes anchor
the arm gates and comparator. There
is no chooser calibration: the executor requires the complete six-marker
Direct3D log, absence of software/mixed markers, and bounded exact main-window
readiness before navigation. Every launched packet retains `bugs-final.log`
inside its own evidence namespace before cleanup.

1. From the six-marker-qualified auto-hardware process, send exactly `Right`,
   `Return`, `Return` through guarded XTEST and run the common identity, level,
   and title gates.
2. Send title Return, retain `t0`, send no more input, and stop only the guarded
   game PID at `t0 + 3.300000000 s`. End periodic focus sampling at
   `deadline-0.060`, finish the complete final identity/window/focus guard by
   `deadline-0.003`, and reserve the final 3 ms only for signal scheduling.
3. Confirm `NextLife`, all-task state `T`, and the two stopped view snapshots;
   together with the pre-title level-index read, these are the exact three
   authorized memory ranges.
4. Capture three native `640x480` screenshots through the frozen asynchronous
   `gamescopectl screenshot` compositor backend and size-stable wait at
   one-second intervals while stopped, retaining request/complete timestamps,
   absolute paths, dimensions, and hashes.
5. Require all three stopped captures to have the four exact structural hashes
   in the offline camera-equivalence receipt and to be PNG/RGB-identical. The
   accepted `F0-AH-009` exact derived-build reference is:
   PNG `05f5691c...506ad1c` and RGB `2ea65643...23b9d26c`. The retail
   `4a5bfde1...f62f88b` / `b8290da...b6451` pair remains a retail R2b phase
   reference only.
6. Visually reject a faded, partial, menu, title, blank, or non-Anthill image.
7. Resume only the guarded PID, confirm it resumed, close normally, and retain
   every bounded normal-close/group/device cleanup step through the final clear
   audit. An immediately clear normal-close audit is sufficient but not
   required; unresolved cleanup remains a rejection.

If the compositor changes while the game is stopped, the derived reference does
not match, the stopped image is not fully bright Anthill gameplay, or any
lifecycle gate fails, F0 is rejected and C1 must not launch. Do not adjust the
deadline after seeing F0.

## Stage 2 - C1/L/C2 localizer

F0 and its result packet are James-accepted. After this post-F0 tooling packet
is committed and accepted, create the guarded localizer and run three fresh
launches in this exact order:

| Arm | Level01 DAT | Purpose |
|---|---|---|
| C1 | exact retail | first frozen control |
| L | exact guarded localizer | independent face-8 visibility test |
| C2 | exact retail | second frozen control |

The frozen fresh namespaces are:

| Arm | Stage | Pending evidence | Accepted evidence |
|---|---|---|---|
| C1 | `C1-auto-hardware-retail-001` | `evidence/pending/C1-AH-001` | `evidence/accepted/C1-AH-001` |
| L | `L-auto-hardware-face8-001` | `evidence/pending/L-AH-001` | `evidence/accepted/L-AH-001` |
| C2 | `C2-auto-hardware-retail-001` | `evidence/pending/C2-AH-001` | `evidence/accepted/C2-AH-001` |

Every path is under `work/copies/EXP-20260819-002/`, must initially be absent,
canonical, nonsymlink, and ignored. The sole executor is argument-free
`scripts/r2c-run-face8-localizer.py`. It validates the creator receipt before
C1, launches a fresh process/copy for each arm, and refuses the next arm unless
the preceding accepted packet independently passes its final clean audit and
all provenance gates.

Each arm repeats F0's exact stop, three-capture, view-snapshot, resume, close,
and audit procedure. Do not launch the next arm unless the preceding post-close
audit is clear. A stopped triplicate is one technical sample, not three
independent observations.

## Frozen comparison

The production comparator now hard-codes accepted derived F0 decoded-RGB
`2ea65643...23b9d26c`; retail R2b `b8290da...b6451` remains evidence-only and
is explicitly non-selecting. The wrapper accepts no paths or hash overrides.
It pins the exact accepted C1/L/C2 namespaces above, validates each arm's build,
DAT, transform/inverse, hardware, navigation, title/index, pidfd timing, stopped
tasks, exact three read ranges, view hashes, capture gate, resume, write
disposition, and final clean audit, then writes only to initially absent
`evidence/comparison/face8-localizer-001`.

After this packet is James-accepted, the exact sequence is:

```bash
PYTHONPATH=reimplementation python scripts/r2c-create-face8-localizer.py
PYTHONPATH=reimplementation python scripts/r2c-run-face8-localizer.py
PYTHONPATH=reimplementation python scripts/r2c-localizer-compare.py
```

The automated gate requires:

- exact `640x480` dimensions enforced by the comparator;
- PNG and decoded-RGB identity among the three stopped captures in every arm;
- exact full-frame decoded-RGB identity between C1 and C2;
- both controls equal to the future accepted derived-build F0 decoded-RGB hash
  after the required post-F0 comparator amendment;
- at least 25 and at most 25% changed pixels in L versus control;
- exactly one 8-connected component of at least 25 pixels;
- the largest component contains at least 75% of all changed pixels;
- its bounding-box area is at most 25% of the frame.

Retain `result.json`, `raw-xor.png`, `changed-mask.png`, and `overlay.png` plus
their hashes. Automated acceptance is necessary but insufficient. A human
visual audit and James must attribute the single localized component to one
surface hole. Actor-only animation, unrelated regions, diffuse or full-screen
change, fade/brightness change, zero difference, crash, or load rejection is
inconclusive and stops the track.

## Outcome table

| Observation | Permitted conclusion |
|---|---|
| exact controls, matching view blocks, automated mask pass, and a visually attributable surface hole | face 8 contributes visible pixels at this frozen state; call it ground only if the retained localization visibly lies on the floor surface |
| zero localizer difference | inconclusive; do not call face 8 offscreen or type `0x41` invisible |
| diffuse, multi-region, actor-only, fade-like, or unrelated change | reject interpretation; no visibility claim |
| controls or view blocks differ | reject run set before interpreting L |
| crash, wrong level/renderer/file, lifecycle failure, or failure to resume | reject affected arm and stop |

After a positive localizer result, close all processes, retain the final audit,
update the Vault, commit cleanly, and obtain James acceptance. Only then may a
new packet freeze the accepted control image, face-8 screen mask/bounds, and
view hashes for a separate one-byte A1/B/A2 candidate run. A zero one-byte
difference would bound only that edit; it would not reject type `0x41`.

## Prohibited interpretations and actions

- Do not reuse the R2b authorization or its work copies.
- Authorization for the exact localizer and C1/L/C2 is on record, but do not
  write it before the accepted F0 and committed/James-accepted exact-creator
  gates are both satisfied.
- Do not raw-patch the face bytes.
- Do not stop a process group or compositor process.
- Do not choose another freeze time or favorable frame after observing L.
- Do not count frozen duplicate captures as replication.
- Do not normalize away fade or an effect.
- Do not prepare or launch the one-byte successor before localizer acceptance.
- Do not call matrix/frustum membership proof of visibility; occlusion remains
  unmodelled.
- Do not promote a plausible region to ground without retained visual evidence.

## Links

- [[EXP-20260819-001 - R2b Anthill static mesh causal runtime]]
- [[EXP-20260818-008 - R2a Anthill static mesh causal candidate]]
- [[EXP-20260818-007 - R1 static mesh consumer, round trip, and causal candidate]]
- [[PC LEVEL DAT static mesh]]
- [[PC camera view-transform chain]]
- [[PC autonomous game control]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[2026-08-19 0245 - Codex - Anthill R2c offline freeze and localizer packet]]

## 2026-08-19 completed C1/L/C2 result

James accepted the run set as procedurally valid and accepted the comparator's
fail-closed rejection. The retained packets are
`evidence/accepted/C1-AH-001`, `L-AH-001`, and `C2-AH-001`; the frozen
comparison is `evidence/comparison/face8-localizer-001` under the ignored
EXP-002 work tree.

- C1 and C2 are full-frame identical: PNG
  `05f5691cab126962715d94857fd5085f7013353b3982a7d6e9d350215506ad1c`
  and decoded RGB
  `2ea6564339c406cbcd92ca32faaf4e6c1b177119939aee569f0cfc1223b9d26c`.
- L is internally triplicate-identical: PNG
  `4a5bfde15d2221e3fbe97334856d52cf13e25e99d8fab7c979dc8e921f62f88b`
  and decoded RGB
  `b8290da48f462b414857a26c89f0fe1f8486a6ffbaeeb106b04dbba829ab6451`.
  That same L image identity already occurred in unmodified retail R2b arms,
  so it is nondiscriminating evidence rather than a localizer signature.
- All arms retained the same two authorized stopped-view hashes and passed
  exact DAT, executable, renderer, Level01, input, PID-bound stop/resume, and
  lifecycle gates.
- The raw comparison has 18,612 changed pixels in 353 components. The largest
  component has 9,938 pixels at `x386..469, y0..395`, only 53.3957% of all
  changes. The preregistered exactly-one-large-component and 75%-concentration
  gates both fail. The overlay shows distributed actor/vegetation/scene-state
  differences, not one attributable surface hole.

**Result:** valid run; rejected comparator; R2c localization remains unresolved.
This does not prove face 8 is visible, that it is terrain/ground, that animation
caused the delta, or that the mutation has no effect. Retail R2 remains open.
The one-byte successor remains unauthorized.

**Superseded successor design:** the original Stage 1 required an empirically
established animation cycle. EXP-003 D1 later found no exact period, so that
requirement is retired. EXP-004 later rejected its phase-sensitive full-frame
gate; EXP-005 below is the active phase-agnostic finite stable-background
successor. Any later C/L/L/C block still requires a separately committed packet
and fresh authorization; zero, mask-only, or distributed residual remains
inconclusive.
## Successor packet

The accepted-but-inconclusive C1/L/C2 outcome requires an independently validated live-control exclusion gate before another localizer. EXP-003 rejected its exact-period model; EXP-004 rejected its phase-sensitive full-frame gate. [[EXP-20260819-005 - R2f Anthill phase-agnostic stable-background calibration]] ran two procedurally valid controls but aggregate-rejected on 233 D2 observations. [[EXP-20260819-006 - R2h Anthill D3 combined-mask holdout]] later accepted the frozen combined diagnostic mask on one finite grid without expansion. It cannot reinterpret this experiment's evidence; a new C/L/L/C packet remains separate and unauthorized.
