---
type: implementation
status: implemented-bounded
created: 2026-09-15
updated: 2026-10-29
evidence: [EXP-20260915-007]
tags: [terrain/scenery, re/pc]
---

# PC wooden fence authoring

EXP-20260915-007 identifies the original Anthill wooden fence and extracts its
posts individually. This extends existing `terrain_anthill_props.read_sprites`,
`terrain_scenery.scene_pointer_fields`, `terrain_play_area.encode_group` and the
original-level texture reader. No external/PS1 source was consulted. The seven
original fence sprite batches hold 193 posts in all; scene118 supplies the first
32 ([[PC Anthill remaining object inventory]]).

## Confirmed PC evidence

Retail EXE SHA256 `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`; original LEVEL01 DAT SHA256 `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`.

- PC confirmed: primary scene118 at DAT7740, flags0x13; object31736 (24 bytes), geometry278848..280772. Thirty-two XYZ centers each own one opaque44-byte quad. In a hardware session of the original game the corresponding addresses are scene`0064C6F3`, object`006524AF`, geometry`0068E9F7`; all1924 geometry bytes match the file (`original-resident.json`). Screenshot `original-fences.png` records the supplied view and Flik pose.
- PC confirmed: `004498F0` dispatch3 calls `00453FF0`, using the negative camera yaw for the billboard matrix. Static disassembly, source locators and32 original-x86 primitive comparisons support independent post extraction. At `00405FE0`, all UV/color/XY arguments and translated centers match the original group after recentering at the post base (`native-art.json`). Quad+18 uses LOW five bits for texture page2; ordinary mesh preview tags put the page in bits8..12. Quad+16 varies between0 and−1 and stays opaque/preserved.
- Collision: EXP-20260915-007 authors post collision independently from the original visual; it makes no claim that the original billboard has matching collision of its own. Full native `0044BB70` DAT relocation preserves all24 compiled post resources (`production.json`).

## Limits

Original-game identification is live evidence; extraction and relocation checks
are offline native evidence. Broad gameplay, other renderers and distant
billboard rendering remain unverified; no distant proxy exists for dispatch3
posts in this work.
