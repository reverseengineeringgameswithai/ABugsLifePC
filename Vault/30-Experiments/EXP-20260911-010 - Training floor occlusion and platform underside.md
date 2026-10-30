---
type: experiment
id: EXP-20260911-010
date: 2026-09-11
status: implemented-bounded
created: 2026-09-11
updated: 2026-10-29
binary_sha256: 149351bfe9b120424aa113df67678907cf89048612aa7ab1e34b1a5264b0e002
environment: Owned Wine Gamescope hardware Direct3D; original PC x86 in offline Unicorn
question: What makes geometry behind original Training floors, and behind a raised authored deck, show through at some camera angles?
result: Original Training ground scenes 57..72 carry object byte+18 depth offset 9, which 00449B22..00449B32 passes as eight times its value into the mesh depth term, so Flik and seeds show through; clearing those sixteen bytes removes the 783/6957 wrong seed samples offline and the effect in hardware captures. A large authored deck face shows through because projection truncates camera-Z/4 at 0045CFE8..0045D05F; subdividing that face fixes it.
tags: [experiment/training, re/rendering, modding/geometry]
---

# Training floor occlusion and platform underside

Two reports are investigated: the underside of a raised authored deck in an
edited Training level showing through, and Flik and seeds showing through
Training floors at certain camera angles.

## Changes tested

Tested Training DAT SHA256
`ea09e0475a6c5fd129e91607a3f4c7d1c2163e212c98c2f1660ebaece499ca79`; only
LEVEL07/LEVEL1.DAT differs among CD files from the preceding build, and the
executable is unchanged:

- Original ground scenes57..72 retain their complete meshes. Their 0x41 object
  byte+18 changes9→0, removing the native depth offset. In the tested DAT these
  fields are11042,11066,…,11402, step24.
- The authored deck scene269 gains a 4-by-4 underside in place of one large quad.
  All other slab faces retain their geometry/winding/shading (312→372 vertices,
  78→93 quads, still one moving object).

`training_occlusion.py` guards all16 objects/meshes and expected bytes before
editing; malformed/truncated/aliased or already-patched input is rejected.
`final-preservation.json` checks parsed records and complete file inventories.

## Platform evidence

`before.png` retains the raised underside defect from EXP009. The brass bottom
exists at local Y125 with outward winding; the visible timber bottoms at Y−6 are
behind it. Original projection truncates camera-Z/4 at0045CFE8–0045D05F and stores
scaled hardware depth at0045E9BF–0045E9D4, using1/4096 at004C00E8. The earlier
[[EXP-20260904-009 - Paused side-view depth interpolation]] independently records
the same large-face interpolation problem.

`underside-only/offline.py` restores hash-exact retail .text to captured memory
and calls004498F0→0045A7F0. Original/candidate return in45,924/58,509 instructions,
emitting132/192 vertices and198/288 indices. Pixel-center linear-depth comparison
places the opaque brass bottom in front of22,181 of22,194 formerly visible timber
pixels;13 edge samples remain. This excludes textures, alpha, GPU edge rules and
an atomic screenshot match. Only29 original XYZRHW entries match the retained live
buffer, so no complete live-batch identity is claimed.

Final hardware `under-final` uses a file-built start/camera and places seed9 on
the button in its private RAW copy. Native seed contact25 alone holds height1000;
Flik remains below on native contact10. Captures at
`under-final/pressure-1789156388062316569.png` and
`under-final/pressure-1789156395237940212.png` show a solid brass underside.
The camera/start hooks are test-only. No external live writes.

## Floor discriminator

**Confirmed:** the preceding control build also exhibits the reported behavior; original
retail ground objects already carry bias9. The platform change did not introduce
those bytes. Static00449B22–00449B32 reads object+18 and passes eight times its
value as the mesh renderer's depth term;00449B06–00449B1C also adjusts the local
draw threshold. `scene-bias-disassembly.txt` and `scene-driver.json` retain the
instruction/decompiler evidence. Zero is a visual correction to original data,
not a claim that these bytes were recently regressed.

`regression/occlusion-probe.py` replays all16 floors, Flik0044C440 and the
seed-only actor list through00448350 in offline captured memory with retail
.text. Six COM call sites return success while native flush/counter reset code
executes; no GPU is emulated. `occlusion-zero.py` changes only the sixteen object
bias bytes in that offline copy. All259 emitted ground vertices retain X/Y/RHW,
color and indices while Z decreases by exactly72/4096 (0.017578125).

The independent pixel-center reference interpolates native RHW then inverts it
to compare perspective depth. With a0.0001 margin,790 Flik samples and6,957 seed
samples lie behind the ground. The original biased floor incorrectly leaves
783/6,957 in front; zero bias leaves0/0, with no false-hidden samples in this
bounded comparison. This is an offline depth discriminator, not a full GPU or
every-angle proof. The captured RAM is read-only and non-atomic; screenshots and
later settled-camera captures must not be treated as simultaneous.

Hardware `clear-base` and `clear-zero` use the same file-fixed camera/start recipe
and settle at identical Flik(30306,11877,−458) and seed(31681,9691,−8958) positions.
Their screenshots `clear-base/pressure-1789155710900813845.png` and
`clear-zero/pressure-1789156108093975774.png` show the foreground floor covering
the lower legs and seed after the16-byte correction. Grass is outside those
comparison regions. Animation phase differs, so no pixel-identical frame claim.

## Superseded arms and limits

The initial all-six-face platform subdivision (480 vertices, temporary512 author
budget) is superseded by the underside-only implementation. A private floor-mesh
subdivision prototype is also rejected: it grows ground emission259→3,540
vertices yet leaves6,925 of the6,957 seed depth errors. Its source, candidate DATs
and diagnostic build metadata stay private; it is **not** adopted.

Original-game controls initially used a seed slot affected by tutorial setup and
an unmatched camera; they do not discriminate this defect. A later matched
original/edited angle shows similar Flik occlusion, but grass covers the seed, so it
does not settle the failing-angle report. These limits remain explicit in
the report. No PS1 evidence is used, and the user's broader OG comparison is not
promoted to a universal cross-version claim.

The earlier observer's requested1ms Left includes a30ms sampling sleep and
process overhead; it is not a measured1ms delivered hold. A later guarded XTest
tap has1.069448ms between acknowledgements and produces no observed movement.
Camera settling after longer input further limits screenshot/memory alignment.

`make check` passes161 selected cases, compatibility and tracked-file gates.
The initial direct pytest command omitted PYTHONPATH and failed collection; the
required make invocation supplies it and passes. Historical full-suite R2p/R2q
failures and five existing Vault size warnings remain outside this packet.
`reports/studio/EXP-20260911-010.json` owns hashes, runtime ownership, closures,
checks and evidence paths. Private game assets/dumps are excluded from Git.
