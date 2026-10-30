---
type: experiment
id: EXP-20260904-007
date: 2026-09-04
status: bounded-diagnosis
question: What is the lower deck surface, and why might the block fail to hide Flik behind it?
environment: Existing Wine 11 Staging hardware game; guarded reads and compositor capture; offline original x86 slices
result: Block contact user-confirmed; lower-deck visibility defect reproduced; inherited depth offset identified; zero-offset candidate unlaunched
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
created: 2026-09-04
updated: 2026-09-04
tags: [re/experiment, re/rendering, re/collision]
---

# EXP-20260904-007 - Deck visibility and inherited depth offset

## Follow-up

[[EXP-20260904-008 - Block depth offset runtime comparison]] subsequently executes the candidate and
confirms the bounded visibility cause by removal/restoration. The observations
below describe the earlier diagnostic boundary; its user game40214/965017 was
closed for EXP-008 and replaced by the corrected handoff46701/1147812.

## User report and live observation

The user confirms landing on and colliding with EXP-006's block. They report
Flik's legs drawing over the block while standing on the lower surface beyond
it; their second image is explicitly **not** a top landing. This accepts the
reported block contacts, not every deck route or EXP-005's failed return path.

The broad surface is EXP-006's deliberately authored flat catch deck. It uses
one large textured quad and is distinct from the raised block. The black oval
under Flik looks like his native shadow; its renderer and apparent size have
not been independently traced. Do not call that oval a collision object.

The user game observed at this diagnostic boundary was PID/start40214/965017,
group39970, display`:2`,
accepted auto-hardware build SHA-256
`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`.
Guarded read-only observation and a game-surface capture reproduce the visibility
problem at XYZ`(171003,-102402,522024)`: Y is the lower deck, and Z is beyond the
block's maximum520000. Contact at`0x007F3D68` is source99/cell6973595, the second
new deck triangle. Camera translation is`(183270,-115207,495970)` and matrix bytes
`930e0000980600000010000068f90000930e`. The fresh640x480 capture is
`work/experiments/USER-20260904-deck-play-001/frame-1788566305052357975.png`,
SHA-256`93d5146dc23745cc224a0e5cd6f5f02f95e1ebb5f2a3556439e84d077d7050f7`.
Memory and image are sequential observations, not an atomic paused snapshot.

## PC-confirmed depth-field behavior

EXP-006 retained primary160's original object bytes, including byte`+0x12=8`.
Its object starts at LEVEL.DAT18672 (`0x48f0`); the byte is at18690 (`0x4902`).
The same value is present in the live object at`0x0064F1A7+0x12`, read through
the existing guarded direct operator. This is a render object field, not a
TERRAIN.ALL collision field.

Retail type`0x41` dispatch at`0x00449B22/00449B25` forms the renderer's third
argument from the caller input plus eight times this byte. The scene driver's
reviewed calls use zero for that input. `0x0045CFE8–0x0045D05F` truncates each
camera Z divided by4 and adds that argument. The tag`0x60` quad path writes
the resulting value times the depth scale to the Direct3D vertex's`+8` field
at`0x0045E9BF–0x0045E9D4`. The live scale at`0x004C00E8` is1/4096.

Two isolated original-instruction slices, with synthetic inputs and no stubs,
confirm the arithmetic: camera Z`[800,1200,1600,1000]` produces depth words
`[264,364,464,314]` for byte8, versus`[200,300,400,250]` for byte0. The inherited
field adds64 depth words, or0.015625 after the observed scale. These are bounded
instruction checks, not full renderer execution or a live corrected image.

The retained tag is not by itself evidence of accidental half transparency:
`0x0045E6C0–0x0045E6CE` permits alpha255 for mode bits`0x60`. Distance/fade
logic follows, so actual per-pixel opacity has not been established by that
constant alone.

## Inference, candidate, and limits

**Inferred:** inheriting this terrain depth offset is a plausible cause of the
new block failing to hide Flik and his shadow. The offset changes emitted depth
without relocating collision. Large faces and depth interpolation remain other
possible contributors. No causal visual fix is claimed.

Prepared a separate candidate at
`work/copies/EXP-20260904-007/LEVEL-depth-zero.DAT`: exactly byte18690 changes8→0.
SHA-256`b0e6a65a353e7a33c0e72399659a8f3ee6d08380fe45893232281d93c06805cb`.
At the EXP-007 boundary it was **not yet launched or installed**; EXP-008
subsequently tests it and supplies a corrected user handoff. The existing
mesh, collision file, original EXP-006 builder and report remain unchanged.
The discriminator is a fresh zero-offset runtime arm, checking visibility from
both sides at recorded deck height and rechecking top/departure contact. If the
artifact remains, compare subdivided render faces with the same collision.
Do not alter collision heights to conceal a rendering defect.

## Evidence and session accounting

`reports/terrain/EXP-20260904-007.json` retains user-image hashes, guarded live
receipts, exact candidate diff and instruction results. Companion
`EXP-20260904-007-depth-path.asm` and`EXP-20260904-007-depth-operator.txt` retain
raw retail instruction text and the isolated-slice operator. Images and assets
remain under ignored`work/` paths; no originals were changed.

The audit's seven processes and private sink`ablpc_mute_39970` all match the
existing handoff receipt. The fixture-only ledger calls them unattributed;
this does not make them abandoned. No launch, close, movement keys, live-memory
write, teleport, debugger, freeze or save-state action occurred. Capture only
focused the existing owned window. No full`make check` or independent audit was
run; original-slice checks and documentation gates are the new validation.
