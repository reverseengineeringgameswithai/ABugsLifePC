---
type: research
status: accepted-bounded
updated: 2026-10-29
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
tags: [re/camera, re/rendering, re/static]
---

## 2026-10-12: every scripted view, not only telescopes

[[EXP-20261012-003 - Scripted camera flag census]] censuses the flags word `0x0059A5EE` (11 code references).

- **Writers.** Three setters write it:
  - `0x0041A620`, the telescope and path tour;
  - `0x0041A9D0`, a point-and-heading view, called from ten level and boss
    routines, Thumper's `0x00431CB0` and the Canyon Showdown Hopper's
    `0x0043AE00` among them;
  - `0x0041A910`, an eye-and-target view with no static caller.
- **Bit 0.** `0x0041B7D0`'s fade states set and clear it. It selects the
  `0x0059A5C0` source for all of these views.
- **HUD.** While bit 0 is set, the gameplay render skips the HUD call
  `0x0044D47D` (`0x0044D472`).
- **Bit 1.** It holds `0x0059D9A0` bit 4 for the view.

Manual controls remain unresolved.

## 2026-09-15: telescope source semantics confirmed within this event

EXP-20260915-005 combines retail00417720/0041A620/0041B7D0 evidence, original-x86 replay at two bases, and hardware jump/tour/return. During a telescope tour, selector0059A5EE bit0 chooses the0059A5C0 source driven by DAT paths11..13; return restores Flik-follow0059DD90. This confirms that bounded event, not every user of either source. The earlier structural evidence below remains valid; manual controls, other scripted events and synchronous whole-frame state remain unresolved.

# PC camera view-transform chain

## Boundary

This note records the independently accepted PC-native structural evidence
that moves the Camera row from Untouched to Bounded under
[[EXP-20260816-164 - PC view-chain correction and coverage reclassification]]
and [[EXP-20260816-165 - Independent PC view-chain correction audit]].
The exact instruction trace is
`static/exports/BIN-97c95ba5572dce63/SUBSYS-camera-view-chain-static-trace.md`.

The hashed Windows PC executable is authoritative. PS1 observations in
[[XPORT-20260816-004 - Camera system shape]] remain comparison hypotheses and
establish none of the claims below.

## Confirmed PC evidence

### Ordered common-block path

At `0x00414580`, thunk `0x0040119F` calls `0x0041B7D0`; at
`0x00414585` the same enclosing sequence pushes common block `0x00599C90`,
then `0x0041458A` calls thunk `0x00401848 -> 0x00455710`.

Inside `0x0041B7D0`, bit 0 of `0x0059A5EE` selects one of two copies into
that common block:

- `0x0041B8C0`-`0x0041B906` copies position and three 12-bit-style words
  from `0x0059DD90`/`0x0059DDA8`;
- `0x0041B920`-`0x0041B966` copies the same layout from
  `0x0059A5C0`/`0x0059A5E4`.

These are two source blocks, a bit selector, and one common destination. The structural claim predates the telescope identification below.

### Flik-relative source update

Before either copy, `0x0041B7D0` calls `0x0041ADF0` on `0x0059DD90`.
`0x0041ADF0` repeatedly reads live Flik coordinates
`0x0059D910`/`14`/`18`, derives target position/orientation values, and
smooths source position `[+0x00..+0x08]` toward `[+0x0C..+0x14]` at
`0x0041B486`-`0x0041B4B6`. It updates wrap-normalised angle-like words at
`[+0x18]`/`[+0x1A]` at `0x0041B4DD`-`0x0041B5C0`.

The alternate branch calls `0x0041ACC0` on `0x0059A5C0`; that function
smooths the same position/target shape and updates its own 12-bit fields at
`[+0x24]`/`[+0x26]` (`0x0041ACC0`-`0x0041ADA5`).

### View-transform consumer and renderer join

`0x00455710` reads common-block position and three words. At
`0x00455799` it calls `0x00463C80` with output `0x005B58E0`; the callee writes
nine signed fixed-point matrix words at offsets `+0x00..+0x10`. At
`0x0045588D`-`0x004558A5` it stores the input position to
`0x005BDB8C`/`90`/`94`, and at `0x00455910` it copies the matrix-adjacent
block to `0x005BDBAC`.

Renderer `0x0044D430` consumes both forms independently:

- `0x0044D4C1` passes `0x005B58E0` through
  `0x00401C4E -> 0x004636C0`, which sign-extends all nine matrix words into
  scratch `0x0063E888`-`0x0063E8B0`;
- `0x0044D4F0` passes origin `0x005BDB8C` and matrix copy `0x005BDBAC` to
  `0x004A3990`.

Batch builder `0x00405FE0` reads the scratch matrix and translations and
performs its own signed fixed-point transform beginning at `0x0040605F`; the
first complete component is `0x00406069`-`0x004060A1`. This corrects the
rejected claim that the pointer arguments place the transform upstream.

## Inferred interpretations

- `0x0059DD90` is likely the ordinary Flik-follow source because its updater
  repeatedly reads live Flik position and the researcher observes a follow
  camera.
- `0x0059A5C0` is confirmed for telescope tours by EXP-20260915-005;
  its other scripted/setpiece uses remain unclassified.
- The chain is a camera/view path rather than merely a generic orientation
  path because it creates the renderer's shared origin and 3x3 view matrix.

These broader interpretations are deliberately not function or field names.
Only the telescope event now has confirmed gameplay semantics; player controls,
other events and global update frequency remain unestablished.

## Unknown

- Whether the PC build has player-facing manual camera controls.
- Uses of selector bit `0x0059A5EE & 1` and both sources beyond the confirmed
  telescope tour/return event.
- The higher-level role of the second `0x00455710` call at `0x0043D486`.
- Whether Direct3D view state exists outside the three known
  `D3DVT_TLVERTEX` submissions.
- Whether all scratch-matrix writers and indirect consumers have been found.

These questions are tracked by
[[Known Unknowns#KU-066 - PC camera-source semantics and manual controls]].

## R2n bounded equality-candidate disposition

[[EXP-20260820-003 - R2n PC state-equivalence read candidates]] reuses this
accepted chain without changing its semantics. It binds upstream comparison
to PC `0x00414585` and generated-view comparison to PC `0x0041458F`; arbitrary
asynchronous polling is unsupported because renderer code mutates several
globals.

The exact candidates are selector bit `0x0059A5EE & 1`, common input
`0x00599C90/18`, live Flik coordinates `0x0059D910/12`, generated matrix
`0x005B58E0/18`, origin `0x005BDB8C/12`, and copied matrix
`0x005BDBAC/18`. Derived origin `0x005BDB9C/12` is optional/redundant. The
copy stops at 18 bytes despite the physical 32-byte `rep movsd`, and the
`0x0063E888` scratch family is excluded because render jobs repeatedly
clobber it. These are bounded equality candidates, not complete camera/player
state, runtime authorization, or visibility evidence.

## R2o completed-present boundary

[[EXP-20260820-004 - R2o completed-present state calibration protocol]]
extends the R2n static order without changing the state candidates. In one
normal `0x0040FFC0` invocation, `0x00414585` and `0x0041458F` precede the
renderer call at `0x0044DBEE`, D3 branch `0x00405B09`, EndScene return
`0x00405F6C`, ShowBack call `0x00405F8B`, and outer completion
`0x0040FFE3`.

The outer completion is not independently a presentation receipt. A bounded
runtime protocol must first observe exact `EAX == 0` at fullscreen Flip return
`0x004248F1` with `uint32[0x00573FF0] != 0`, or at windowed Blt return
`0x004249C4` with that dword equal to zero. Both alternatives also require D3
selector `2`, initialized byte `0x0059063E != 0`, presentation-disable byte
`0x00590638 == 0`, normal branch word `0x0059A5F0 == 0`, and one TID/enclosing
invocation. Static evidence proves CPU order and a successful DirectDraw
method return only; Gamescope compositor-exposure timing remains a runtime
calibration question.

## Corrected adjacent boundaries

- Viewport structure construction/submission is
  `0x00423EDE`-`0x00423F43`; it is projection/device setup, not an eye pose.
- The three reviewed submissions at `0x004047E9`, `0x00405816`, and
  `0x0040598B` use `D3DVT_TLVERTEX`; that fact is not a universal proof that
  the executable never sets Direct3D view state elsewhere.
- Thunk `0x00401659 -> 0x004AC460` has seven direct callers. Removing two
  known reset consumers and known City dispatcher `0x00433900` leaves four
  unmapped enclosing functions, exactly two of which also read Flik position.

## Coverage disposition

The PC has a reproducible position/orientation selector feeding a
render-consumed 3x3 transform. EXP-165 independently accepts that as a real,
bounded camera/view anchor, so Camera is Bounded. Mapped would overclaim:
semantic source roles, controls, runtime frequency, and visual causality
remain open.

## Independent acceptance

James independently re-derived the chain from native instructions and
returned **ACCEPT** in EXP-165 at exact clean subject commit
`0336d14dd0ce36b7f77d90d50e7ab693030b7f52`. The accepted boundary includes
the direct matrix join, renderer-side origin/matrix use, selector ordering,
local transform, and adjacent locator/count corrections; it does not promote
the Inferred or Unknown items above.
