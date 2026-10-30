---
type: experiment
id: EXP-20260816-162
date: 2026-08-16
question: 'Does fresh-context adversarial review support EXP-20260816-161 at its claimed static boundary, including the viewport, D3DApp, TLVERTEX, upstream-transform, terrain-caller, coverage, and cross-port claims?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline static audit; GNU objdump; rabin2; existing PC static exports; no runtime, debugger, or target write
environment_version: Python 3.14.6
working_directory: /home/dev/ABLPC
configuration: fresh-context adversarial audit at clean subject commit 02946af277621f2b51cfe7936c06438c2211e2e2; read-only toward game media, originals, and the external PS1 source; no game, Wine, Gamescope, or debugger process
artifacts:
  - static/exports/BIN-97c95ba5572dce63/M2-exact-0a6c-builder-input-localization.md
  - static/exports/BIN-97c95ba5572dce63/M2-positive-target-selector2-input-provenance.md
  - Vault/20-Research/Cross-Port/XPORT-20260816-004 - Camera system shape.md
addresses:
  - "0x00405FE0"
  - "0x00406015"
  - "0x00406069"
  - "0x00414573"
  - "0x00414580"
  - "0x0041458A"
  - "0x0041ADF0"
  - "0x0041B7D0"
  - "0x0041B8C0"
  - "0x0041B920"
  - "0x00423E73"
  - "0x00423EDE"
  - "0x00423F43"
  - "0x00423F71"
  - "0x00455710"
  - "0x0045588D"
  - "0x004636C0"
  - "0x00463740"
file_offsets:
  - "0x0053E0"
  - "0x013973"
  - "0x01A1F0"
  - "0x01ABD0"
  - "0x023273"
  - "0x0232DE"
  - "0x023343"
  - "0x054B10"
  - "0x062AC0"
  - "0x062B40"
result: reject-false-upstream-transform-and-underclaimed-pc-view-chain-cross-port-boundary-survives
created: 2026-08-16T18:59:16-04:00
updated: 2026-08-16T18:59:16-04:00
tags:
  - re/experiment
  - re/audit
  - re/camera
  - research/coverage
---

# EXP-20260816-162 - Independent camera reconnaissance audit

## Verdict

**REJECT** at subject commit `02946af`. The packet is admirably willing to
record a partial result, and its D3DApp provenance, `D3DVT_TLVERTEX` core,
seven-call terrain census, cross-port separation, and manual-controls caution
survive. Its weakest Confirmed item does not: `0x00405FE0` performs the
fixed-point transform immediately after reading the four pointer arguments.
Following that transform also exposes a PC-native position/orientation
selection and view-matrix path that the packet did not follow. Consequently
"the transform is upstream" and "Camera stays Untouched because no PC anchor
was established" cannot both stand.

This is an offline audit only. No game process, Wine, Gamescope, debugger,
target write, original, or external PS1 checkout was touched.

## Checks that survived

- **Subject and binary identity.** `02946af` changes eight Vault Markdown
  files and no game, code, test, or fixture content. The exact work-copy
  executable rehashes to `97c95ba5...a27b878`.
- **D3DApp provenance.** The image contains the literal `D3DApp:` at
  `0x004CA974`, `d3dappi` member expressions, and
  `pDev->SetCurrentViewport(d3dappi.lpD3DViewport)` at `0x004CA91C`.
  Calling the renderer scaffolding D3DApp-derived is supported.
- **Known submissions are TL vertices.** The three known
  `DrawIndexedPrimitive` sites at `0x004047E9`, `0x00405816`, and
  `0x0040598B` each receive vertex type `3`; their exact diagnostic strings at
  `0x004C4B28`, `0x004C4EF8`, and `0x004C5190` spell
  `D3DVT_TLVERTEX`. Those paths consume already transformed vertices, so the
  relevant transform is game code. The narrower fact survives; the universal
  phrase "no Direct3D view matrix exists" does not follow from these three
  sites and must be removed or bounded to the known submissions.
- **Terrain-call count and addresses.** Thunk `0x00401659` resolves to
  `0x004AC460` and has exactly seven direct calls:
  `0x004329E9`, `0x004336D5`, `0x00433BA2`, `0x0043507E`,
  `0x00437AD9`, `0x0043E716`, and `0x0044085A`. The containing-function
  attribution in EXP-161 reproduces when calls are assigned from native
  function boundaries rather than a nearest-symbol guess.

## Defect 1 - viewport endpoints are operand addresses

The broad reading is sound: this is viewport/device setup, not an eye pose.
The cited range is not sound. `0x00423E93` is the first byte of the immediate
inside the `push 0x004CA9C0` instruction that starts at `0x00423E92`.
Likewise `0x00423F55` is the first byte of the immediate inside
`push 0x004CA980` at `0x00423F54`. Neither locator is an instruction address.

The bounded instruction sequence begins at `0x00423E73`, creates and adds the
viewport through calls at `0x00423E81` and `0x00423EB6`, builds the 44-byte
viewport structure at `0x00423EDE`-`0x00423F3F`, submits it at
`0x00423F43`, stores the viewport pointer at `0x00423F68`, and calls the next
setup helper at `0x00423F71`. The honest short locator for the structure
itself is therefore `0x00423EDE`-`0x00423F43`, not the two diagnostic-string
operands.

## Defect 2 - `0x00405FE0` performs the transform

The pointer reads at `0x00406015`, `0x00406028`, `0x00406035`, and
`0x00406046` do not prove an upstream transform. Beginning at
`0x0040605F`, the same function multiplies those signed input words by the
3x3 globals `0x0063E888`-`0x0063E8B0`, applies signed `/4096` reduction, and
adds `0x0063E8B8`/`BC`/`C0`; the first complete component is visible at
`0x00406069`-`0x004060A1`. It repeats the operation for the remaining
components and vertices. This is the transform, not merely a downstream
batch copy.

The repository already contained contradictory PC evidence that should have
stopped the claim. `M2-positive-target-selector2-input-provenance.md` says the
coordinates are transformed by `0x0063E888`-`0x0063E8C0` and that
`0x0045A7F0` fills batches inline; it does **not** call `0x00405FE0`.
Native call census agrees: thunk `0x00401D66 -> 0x00405FE0` has twelve calls,
including `0x0044F99D`, but none in `0x0045A7F0`.

## Defect 3 - a PC-native view chain was quietly earned

The failed upstream inference pointed directly to a stronger existing chain:

1. In the enclosing update sequence, `0x00414573` passes Flik's live-position
   block `0x0059D910` to `0x0043F9E0`, `0x00414580` calls thunk
   `0x0040119F -> 0x0041B7D0`, and `0x00414585` passes `0x00599C90` to
   thunk `0x00401848 -> 0x00455710` at `0x0041458A`.
2. `0x0041B7D0` calls `0x0041ADF0` on source block `0x0059DD90`.
   `0x0041ADF0` repeatedly reads Flik XYZ `0x0059D910`/`14`/`18`, derives
   heading and target offsets, and smooths source position fields at
   `[arg+0x00..0x14]` plus orientation fields. Calling this a gameplay-follow
   camera remains **Inferred**, but the Flik-relative position/orientation
   update is Confirmed by the instructions.
3. Depending on flag `0x0059A5EE & 1`, `0x0041B7D0` copies either position and
   angles from `0x0059DD90`/`0x0059DDA8` at `0x0041B8C0`-`0x0041B906`, or
   from `0x0059A5C0`/`0x0059A5E4` at `0x0041B920`-`0x0041B966`, into the
   common block `0x00599C90`-`0x00599CA0`. "Two camera sources and a
   selector" is still an interpretation; the two-source copy is Confirmed PC
   data flow.
4. `0x00455710` consumes that common position-plus-three-angle block. It calls
   angle-to-matrix thunk `0x004012BC -> 0x00463C80` at `0x00455799`, stores
   the input position into `0x005BDB8C`/`90`/`94` at
   `0x0045588D`-`0x004558A5`, and copies the resulting matrix into
   `0x005BDBAC` beginning at `0x00455910`.
5. Render code reads that origin and matrix extensively. In particular,
   `0x0044D4C1` passes matrix `0x005B58E0` through thunk
   `0x00401C4E -> 0x004636C0`, which copies all nine signed matrix words to
   the exact scratch globals consumed by `0x00405FE0`; translation-loader
   `0x00463740` supplies `0x0063E8B8`/`BC`/`C0` from object transform blocks.

This is enough for a deliberate PC-only view-transform anchor and a Bounded
camera investigation once the chain is corrected and indexed. It does not
prove player controls, semantic field names, or that every alternative path
is a camera. The row was under-claimed in the conservative direction.

## Terrain-candidate and count audit

The seven-call census is exact, but only **four**, not five, containing
functions are unmapped after subtracting the two known reset variants and the
known City dispatcher `0x00433900`: `0x004336A0`, `0x00434E10`,
`0x0043E6B0`, and `0x0043F9E0`. Exactly two of those four enclosing
functions read Flik's live position: `0x00434E10` at `0x00435912`/
`0x00435920`, and `0x0043F9E0` at `0x004409BB`-`0x004409DB`.

That does not mean either terrain query uses Flik's live point. The
`0x0043507E` call follows writes of a constant X and `EBP` Y into the global
position block; the `0x0044085A` call receives the function's `ESI` object.
The two functions are candidates only at their broad enclosing-function
boundary. EXP-161's Confirmed bullet lists all five non-reset functions and
labels City correctly, but XPORT-004 and the worker session compress this to
"five unmapped" and must be corrected.

## Cross-port policy audit

[[XPORT-20260816-004 - Camera system shape]] satisfies the policy boundary:
it names `SRC-PS1-ABL`, pins commit
`1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51`, lists exact external paths,
separates PS1 observations from PC evidence, and phrases all three PC items as
hypotheses. No PS1 statement is promoted into a Confirmed PC claim. The
researcher's request to use PS1 material to "confirm" did not change that
authority boundary.

The manual-controls discrepancy is also handled correctly. It remains an
open candidate difference because an unused or undiscovered PC control path
would match the observation; the audit found no basis to call it a port
difference. The only cross-port correction required is the PC-native
"five unmapped" count and updating hypothesis 3 from an untested search
strategy to the bounded PC view chain above. The PS1 side still confirms
nothing about PC.

## Limitations

No runtime frequency, visual camera effect, player control, field name, or
complete indirect-call claim was tested. The second call to `0x00455710` at
`0x0043D486` was not semantically classified. The audit establishes a
position/orientation selector feeding a render-consumed view transform; the
gameplay-follow, setpiece, and camera labels remain Inferred until an
independent PC discriminator supports them.

## One bounded corrective packet

**EXP-20260816-164 - PC view-chain correction and coverage
reclassification.** On the exact retail hash and subject commit, correct the
viewport locators to instruction boundaries; replace the absolute no-D3D-view
statement with the known-`TLVERTEX` boundary; remove the false upstream
transform and `0x0045A7F0` caller claims; document the PC-only chain
`0x0041ADF0 -> 0x0041B7D0 -> 0x00599C90 -> 0x00455710 ->
0x005B58E0/0x005BDB8C -> 0x004636C0 -> 0x0063E888 -> 0x00405FE0` with
Confirmed/Inferred labels; change five unmapped functions to four; and move
Camera from Untouched to Bounded only after every live Current State, roadmap,
coverage, MOC, XPORT, and session claim agrees.

Stop at documentation and static PC evidence: no game launch, debugger,
target write, implementation, new semantic function/field name, PS1 promotion,
manual-control conclusion, or M2/M5 expansion. Done means a repository-wide
search leaves the rejected locators/counts only as explicit historical
quotations, the row names one bounded PC view anchor and one honest open
question, Vault/M4/hygiene gates pass, and a fresh delta audit can reproduce
the chain from native instructions.
