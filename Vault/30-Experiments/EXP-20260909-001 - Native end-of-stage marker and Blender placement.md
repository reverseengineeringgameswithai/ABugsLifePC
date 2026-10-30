---
type: experiment
id: EXP-20260909-001
date: 2026-09-09
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: PC Wine hardware capture, offline Unicorn, Blender 5.2
question: Which original Anthill object is the right-facing leaf-on-a-stick sign, and does it carry its own collision?
result: DAT primary scene82 (record 7020, object 21232, geometry 211780; dispatch 0x19, 27 vertices, 23 primitives); native 004498F0 projection matches the live buffer and the renderer reads stored camera 005BDB9C; no dedicated sign collider or actor was found, nearby contact comes from terrain records 119/164; a relocated copy renders identically under 0044BB70 and loads byte-exact live
status: complete
created: 2026-09-09
updated: 2026-10-29
evidence: [EXP-20260909-001]
tags: [experiment/modding, re/scenery]
---

# EXP-20260909-001 - Native end-of-stage marker and Blender placement

This experiment identifies the original Anthill right-facing leaf-on-a-stick
sign (called the end-of-stage marker here), maps its geometry and renderer path,
and checks whether it has its own collision.

Private packet: `work/experiments/EXP-20260909-001/` (H). Public metadata:
`reports/end-marker/EXP-20260909-001.json`. No PS1 source was consulted. Original
files were not modified; all extracted geometry, dumps and images remain ignored
under work. No live memory writes occurred.

## Confirmed PC identity

Original-content copy `work/copies/original-anthill-play-20260909-01/` used the
supported auto-hardware executable
`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`.
The original DAT is `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`;
terrain is `62f3b73f21630eb19c04e585a92e1f3e32a76fdcb6ec36bae18f9c1ec3a2a868`.
Read-only capture matched pose/camera before/after at Flik world
(-193206,-180664,-161862). `memory.json` binds the source files and RAM hashes.
The original frame is `work/playtests/original-anthill-20260909-01/preview/frame-1788980337744561622.png`.

DAT primary scene82, record7020, object21232, geometry211780 is the requested
sign. It uses dispatch0x19,27 vertices,23 primitives, material tags160/8161/8162/
8163/8166. The682-byte geometry hash is
`027039db0c92ad8b2460e0a4a0524ef36e59ede3001c26fff4beec719cb2cafa`.
Object origin(-6241,-5564,-4778), Euler(0,3590,0), scales(5537,5537,5537), selector0.
The base anchor is at stem ground level; geometry extends816 stored units upward.

`project-sign.py` runs pristine PC renderer004498F0 and Euler00463C80 in captured
private Unicorn memory. `sign-projection.json` records47/47 projected XYZW entries
matching the live renderer buffer, within pixels320..400 by156..366. Its optional
Pillow overlay failed after the JSON was saved; no overlay is an acceptance gate.
`native-translated-render.json` independently runs original relocator0044BB70 on
the built DAT and repeats the source view with a translated camera. All projected
XYZW, colors, UV and indices match exactly; world vertices translate literally.

The first translated-camera attempt changed world camera005BDB8C and produced
no batches. The renderer query identifies its stored camera005BDB9C; adjusting
that by stored translation produces exact agreement. This is an offline fixture
correction, not a game patch or a claim based on decompiler text alone.

## Collision scope and contradictory probe results

`collision.json` inventories all source barrier segments; the nearest is3674
stored units from the stem. No dedicated sign actor was found within1200 units;
the one nearby actor was native type14 at a different location. The complete
source collision census at the anchor finds broad surrounding terrain records119
and164, with cells115088/115152 and194308/194396. These do not describe the tall
stem/leaf mesh. `collision-census-corrected.json` preserves coordinates and normal
words. Its first runtime descriptor scan mistakenly used+24 as minimum Z; the
corrected scan uses+28. Broad descriptor overlap alone does not prove contact.

Four native grounded traversals use004AB1A0. Three cross the requested axis;
one does not, while all show lateral displacement and surrounding-terrain
contacts119/164. They do not establish unrestricted passage through the sign.
No dedicated sign collider was mapped. The imported sign is therefore scenery
with **no authored collision**, retaining the source visual. Universal original
interaction/top-support behavior remains unknown; no guessed collider is added.

## Relocated copy check

A copy of the scene82 object and geometry placed at another position keeps native
shape, material/UV/opaque bytes, rotation, scale, selector and translated culling
origin. `edited-builds.json` verifies zero, one and two copies with literal
positions, exact native geometry and original relocation. In a live run,
`runtime/live-marker.json` verifies exact resident object/geometry bytes and
`runtime/verification-latest-load.json` verifies170 models. A first
resident-model check caught level0 with cleared model pointers and was rejected;
the corrected verifier selects the latest FLICK load sequence from the
multi-entry log. Selected `make check`:432 passed in44.48s.
