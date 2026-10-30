---
type: implementation
status: implemented
created: 2026-09-08
updated: 2026-10-29
evidence: [EXP-20260908-019]
tags: [implementation/modding, terrain/authoring]
---

# PC Anthill berry and flower authoring

## Confirmed PC evidence and implementation

EXP-20260908-019 maps original Level01 scene65/66 to the berry leaf mesh and 21 sprite
groups, and scene90/91 to tall/short flowers. `004498F0` dispatch0x0A enters
`00454B70`; the importer retains the entire native quad stream, including unknown
bytes. Flower object byte25 low bits14 select animated matrix slot3; native
`00455710` phase replay and 25 distinct live matrix samples confirm sway.
Original DAT SHA256:
`786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`.
Authoritative retail PC exe SHA256:
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.

`terrain_anthill_props.py` bounds-checks sprite counts/extents and preserves
opaque records. Existing native scene relocation/footer rules are reused.
Berry collision retains source180 contour segments24..47 and adds one authored
closing back edge for freestanding placement. Original collector
`004AB60F..004AB73A` uses X/Z without a height bound; it supplies no landing top.
Eight paired native approach checks block, retreat and settle; two paired drops
match the no-barrier control and reach real ground. This is bounded native-code
evidence, not an exhaustive live collision guarantee for future placements.

No flower collision was identified or authored. Full original-flower contact
coverage, every camera angle and arbitrary rotated/scaled donors remain unknown.
No PS1 comparative source was used.
