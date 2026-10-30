---
type: experiment
id: EXP-20260905-005
environment: "Fedora Linux 44; Wine 11; hardware Direct3D under Gamescope; original PC assets and guarded read-only captures"
result: "Both: original steep wall faces use different page-0 atlas regions (U64..191,V192..255) from the floor and different vertex colour triples; the live-extracted page-0 regions differ before vertex colour, so a flat darkening factor does not reproduce them"
date: 2026-09-05
status: accepted-bounded
question: Does the original near-spawn wall appearance come from texture selection, vertex colour, or both?
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
created: 2026-09-05
updated: 2026-10-29
evidence:
  - EXP-20260905-004
tags: [re/terrain, re/rendering]
---

# Original wall texture regions and colour inputs

## Status and scope

This note answers whether the original near-spawn wall appearance comes from
texture selection, vertex colour, or both, using a static census of the
original Level01 DAT, the PC quad path, and a live read-only extraction of
texture page 0 from an original Level01 run.

Run-index orientation retained the existing 14 uncited runs and one dangling
citation; EXP-005 was unused in the checked experiment/session index.

## Evidence

- Read-only census: `scripts/terrain-wall-material-probe.py` and
  `reports/terrain/EXP-20260905-005.json`.
- Original PC Level01 DAT SHA:
  `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`.
- Original PC executable SHA:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- EXP-004 DAT SHA:
  `54d1ae4d96a4d926b806584cc669e791c3f6565688ec4aa491a987b0c2f56aab`.
- Private screenshot and exploratory census:
  `work/experiments/EXP-20260905-005/`.
- [[PC LEVEL DAT static mesh]], [[FUNC-97C95BA5572D-0045A7F0]].

The original PC quad path reads face bytes into output UV slots at
`0x0045D38C/0x0045D3A7 -> 0x0045D3A4/0x0045D3B9`. At `0x0045D474` it loads
vertex+8. `0x0045D462/0x0045D49D/0x0045D4A7` participate in its channel/global
multiplier path. Fresh disassembly of the hash-verified PC executable and the
Ghidra export agree on distinct coordinate and three-channel inputs. This
does not assign all tag bits or imply a fixed final pixel brightness ratio.

## Confirmed file comparison

There are 400 selected faces with centroids within stored X/Z +/-4200 of
`(6160,15400)`, using zero-rotation primary static meshes. Using the absolute
first-triangle normal-Y fraction: 231 exceed 0.85, 101 are below 0.4, and 68
are between. These are geometric census categories, not visibility or
collision classifications.

All 101 steep samples use page index 0. Of those, 93 use UV region
`U=64..127,V=192..255`; eight use `U=128..191,V=192..255`. EXP-004's entire
49-quad primary160 mesh instead uses the `U=0..63,V=192..255` region, including
its 24 vertical-wall quads. Subdivision distributes that region over the faces.
The 64-pixel bins are an analytical grouping, not newly decoded tile metadata.

An exact pair with **the same tag `0x0060` and page index 0**:

| Source | Face offset | UV corners in file order | Vertex channel triples |
| --- | --- | --- | --- |
| Original primary160, group0, face2 | 114280 | (63,192), (0,192), (0,255), (63,255) | (96,96,100), (96,96,100), (112,108,108), (100,100,104) |
| Original primary128, group0, face13 | 221788 | (127,255), (127,192), (64,192), (64,255) | (108,76,56), (120,88,64), (92,64,44), (104,76,56) |

The latter steep face has substantially less green/blue relative to red,
not merely a uniform reduction of the floor channels. Its UV orientation also
differs. EXP-004 used `(96,96,100)` uniformly. Therefore copying a flat darkening
factor alone does not reproduce this original face's authored inputs.

## Boundaries and next discriminator

At the end of the static phase, the reference screenshot was not localized
to an exact PC face and the page pixels were not extracted. The runtime
section below now supplies the page pixels and a confirmed wall view;
the exact pixel-to-face join remains open.
Do not claim every OG wall uses one material, or that the original image has
been explained completely. No PS1 evidence was consulted.

Next: identify the wall in an original PC view, then retain separate baseline,
wall-region-only, donor-colour-only and combined file-loaded arms. Preserve
collision, coordinates and unknown fields. Respect the native UV orientation
and keep the top's colour vertices separate if required. Compare by normal
launch/input/read-only capture, with no inherited write/debugger authority.

No pytest, R2q or full-suite run was performed for this read-only investigation.

## Original runtime and native texture page extraction

The preceding EXP-004 launch-only session was closed first. It had no
`active.json`, so its normal close guard failed; the operator's exact-identity
cleanup completed and the post-close audit was clean. This is not a
normal-close success claim.

A fresh full-disc copy at `work/copies/EXP-20260905-005/original-game` uses
untouched original assets and an isolated cloned prefix. The first preflight
looked for the drive type in `system.reg`; it is correctly present in
`user.reg`. No registry repair or launch preceded that correction. The clean
pre-launch audit, exact CD sentinel, R: target, asset hashes, six hardware log
markers and both R: log identities were checked. The executed image is the
established auto-hardware derivative `1e1d5099...c41f`, not the unmodified
retail executable. Right/Return/Return reached Anthill gameplay normally.

The auto-hardware menu's same-PID 640x480 `bugs.exe` window was titled
`Loading - A Bugs Life`, not the older procedure's exact `Bugs` selector title.
The old exact-title condition did not pass. No chooser existed; the actual
owned window, mapped code, compositor peer, log identities and visible
Training/Anthill/title/gameplay frames were checked instead. This difference
must remain visible in the procedural record.

Read-only full loaded collision sources99/100 and mesh streams128/160/213/280
matched the original files. Three short Down holds turned Flik and the
following camera back toward the wall. The camera continues rotating after
input release; the last turn allowed five seconds. The user confirmed the wall
was visible; a closer approach followed. Up holds of .35, .5 and .45
seconds produced the close reference. Ten native 640x480 captures were retained.

**Texture-page pixels have now been extracted.** Native PC `0x0040F340`
allocates the indexed-mode buffer using the page dimensions. In this live arm,
page0 dimensions at `0x00573408` were 256x256, mode at `0x00573118` was1,
and the pointer at `0x00582EB0` was `0x09423EC0`. Its 65,536 index bytes and
768-byte palette at `0x005844F4` were read twice unchanged under the pinned
PID/start/group. Native `0x00466260` and `0x00462C30` provide supporting
palette/index consumer evidence; their legacy debug-string names are PC
executable evidence, not an external PS1 consultation.

- Indexed page SHA: `da6ed96650d2a3464f6d8af8d37f6088222d744ae95b322bff0031d9e14caf85`.
- Palette SHA: `0e848743ea7fcae70325a8a71b9691a65f048d4634781212860627120d57e1dc`.
- Floor region RGB SHA: `faf7f4c439a9dfcd961a13f2c723bdaf0ececbc298f8545ded5c5a5c369d2ac5`.
- First wall region RGB SHA: `967cfca143e62753b1505b10924e981982d91516cab63571007462da82bb4e16`.
- Second wall region RGB SHA: `4ecc9990bd2c5e36de7677d7da7ec0ec330293ae2fdeaf28000faa9989edc728`.

The three decoded 64x64 regions differ before vertex colours are applied.
Their low-nibble index hashes also differ; this does not prove independent
source artwork or rule out palette-remapped/edited/rotated variants. Combined
with the same-tag face comparison, this supports separate texture-region and
vertex-colour contributions, not a flat uniform shade.

Public runtime metadata: `reports/terrain/EXP-20260905-005-original-runtime.json`.
Private pixels, palette, screenshots and receipts:
`work/experiments/EXP-20260905-005/original/`.
Final close-up: `frame-1788650817506429264.png`, SHA
`22efec899aec7793cae393e6d89de9346908d4d3282ccd679972f82fb1979064`.
No process memory writes, teleport, ptrace, stops, registers, save states or
debugger control occurred. No authored material candidate or pytest/R2q gate
was run in this arm. The original session was later closed with a clean
post-close audit.

## Combined-arm edit check

A later combined-arm edit to the EXP-004 test box (wall U bytes increased by64
to select `U64..127,V192..255`, plus vertex colours interpolated from the
primary128/group0/face13 donor at221788) kept every face's XYZ corners, unknown
vertex fields, tag and the entire TERRAIN.ALL unchanged, and its1730-byte prefix
fits inside the known2234-byte allocation. Live comparison matched the entire
render prefix, source99's618-byte collision prefix and unchanged scene/object
fields to the files; live prefix hash
`f1fb09c2c10bc8bf330d56c3a6414460de9cd4cc7928063b63bbeff550c328c6`. Public
packet: `reports/terrain/EXP-20260905-005-material.json`. Only the combined arm
was launched, so this is not a bracketed four-arm causal result; independent
live four-arm attribution and universal material rules remain unclaimed.
