---
type: experiment
id: EXP-20260816-161
date: 2026-08-16
question: 'Can a static pass locate PC camera state, given the row has no string anchor and no import surface?'
status: superseded
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline static analysis; radare2 5.9.8; rabin2; repository Python 3.14
environment_version: radare2 5.9.8
working_directory: /home/dev/ABLPC
configuration: read-only disassembly, string and import reads from the exact retail work copy; no runtime process, debugger, or target write
artifacts:
  - Vault/20-Research/Cross-Port/XPORT-20260816-004 - Camera system shape.md
addresses:
  - "0x00423A20"
  - "0x00423EDE"
  - "0x00423F43"
  - "0x00405FE0"
  - "0x00401659"
  - "0x004336A0"
  - "0x00434E10"
  - "0x0043E6B0"
  - "0x0043F9E0"
result: rejected-by-exp162-corrected-by-exp164-accepted-by-exp165
created: 2026-08-16T23:30:00
updated: 2026-08-16T23:30:00
tags:
  - re/experiment
  - re/static
  - re/camera
  - research/coverage
---

# EXP-20260816-161 - PC camera static reconnaissance

## Verdict

**Historical worker verdict, rejected by EXP-162 and superseded by
EXP-164.** The original packet said camera state was not located and kept the
row Untouched. Fresh native review found that the worker stopped before the
transform and did not follow its matrix to the already-present PC view chain.
The corrected authority is
[[EXP-20260816-164 - PC view-chain correction and coverage reclassification]],
accepted by
[[EXP-20260816-165 - Independent PC view-chain correction audit]].

This note now retains the search history and surviving findings while removing
its rejected claims from live authority. Git commit `02946af` remains the
exact audit subject if the original wording is needed.

## Why this was harder than audio

`EXP-20260816-159` opened the audio row in one static pass because audio had
labels to follow: `PLAYTRACK`, `SETMUSICVOL`, `DSStream`, and a 35-entry
filename table. The camera row has **no string anchor at all**. Searching the
image for camera, view, FOV, angle, zoom, pitch, yaw, and target terms returns
only DirectX viewport boilerplate and `D3DERR_*` constants — nothing
game-level. It also has no import surface: unlike audio (`DSOUND`) or input
(`DINPUT`), a follow camera calls no API that identifies it.

That was predictable from the coverage map's own method note, which ranks
import-anchored rows as the cheap ones. It is now confirmed by attempt.

## Surviving and corrected findings

- **The viewport path is projection, not camera, and sits in already-mapped
  code.** The viewport structure is built/submitted at
  `0x00423EDE`-`0x00423F43`, inside `0x00423A20`, an existing dossier.
  Per-frame viewport clears are at `0x00403E18`, `0x00403EE5`, and
  `0x00424B39`. None of this locates an eye position or orientation.
- **The renderer is built on Microsoft's D3DApp sample framework.** The image
  carries the literal `d3dappi` structure members — `hwnd`, `lpDD`, `lpD3D`,
  `lpFrontBuffer`, `lpBackBuffer`, `lpD3DViewport`, `lpGroundMat`,
  `lpSkyMat`, `lpTexture` and their material handles — plus source-level
  expressions such as `pDev->SetCurrentViewport(d3dappi.lpD3DViewport)`. The
  device and viewport scaffolding therefore follows a documented SDK pattern
  rather than being bespoke. This is new and applies to the rendering row, not
  just the camera.
- **The known TL-vertex paths use game-code transforms.** The three reviewed
  submissions use `D3DVT_TLVERTEX`, but that does not prove the program has no
  Direct3D view state anywhere. `0x00405FE0` itself performs a signed
  fixed-point transform beginning at `0x0040605F`; `0x0045A7F0` is not a
  caller of that builder and fills its own batches inline.
- **A PC-native view-transform chain exists.** `0x0041ADF0` updates a
  Flik-relative source, `0x0041B7D0` selects one of two source layouts into
  `0x00599C90`, and `0x00455710` converts the common position/angles into
  origin `0x005BDB8C` and matrix `0x005B58E0`. Renderer `0x0044D430` consumes
  both at `0x0044D4C1`/`0x0044D4F0`. Source roles remain Inferred.
- **The terrain height query has seven call sites**, through thunk
  `0x00401659`: `0x004329E9` and `0x00437AD9` are the two known reset
  consumers; the other five calls are in `0x004336A0`, `0x00433900`,
  `0x00434E10`, `0x0043E6B0`, and `0x0043F9E0`. Because `0x00433900` is the
  known City-gate dispatcher, only four enclosing functions are unmapped.
- **Two of the four unmapped enclosing functions read Flik's live position**:
  `0x00434E10` and `0x0043F9E0`. Their terrain-query arguments are not thereby
  Flik's point, and neither function is confirmed to be a camera.

## Not confirmed

The two terrain candidates' camera roles, the semantic roles of the two view
sources, PC manual controls, the second `0x0043D486 -> 0x00455710` call, and
complete indirect-call coverage. The corrected PC view chain did not come
from either terrain query.

## Cross-port note

[[XPORT-20260816-004 - Camera system shape]] records what the PS1 project's
camera notes suggest strictly as hypotheses. The terrain idea produced only
two broad enclosing-function candidates. Independently, PC instructions now
establish two source layouts, a flag-selected common block, and a
render-consumed 3x3 transform; PS1 still confirms none of those PC facts.

The researcher reports that the PC camera simply follows Flik with no player
camera controls, while the PS1 vault documents manual camera controls as a
system. That is a candidate port difference and is **not** recorded as one: an
undiscovered or unused PC control path would look identical from the outside.

## Coverage effect

The original Untouched disposition is rejected. EXP-164 supplies a bounded PC
view anchor and EXP-165 independently accepts it at clean subject `0336d14`;
Camera is Bounded.

## Suite anomaly observed during this packet

`make check` reported `1 failed, 647 passed` on four consecutive invocations
and `648 passed` on twelve runs afterwards. The failing test's name was lost:
the failing invocations piped pytest's output through `grep`/`sed`, discarding
the `FAILED` line, and it has not recurred. This packet changed **only Vault
markdown**, so it cannot have introduced the failure. Recorded as `KU-065`
with a reproduction procedure rather than quoting the passing run as a clean
gate.

## Next discriminating experiment

In a separately authorized future session, a read-only runtime/input
discriminator may test selector/source meanings and the manual-controls
unknown. No such semantics are implied by the accepted static correction.
