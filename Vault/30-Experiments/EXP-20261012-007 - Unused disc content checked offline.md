---
type: experiment
id: EXP-20261012-007
date: 2026-10-12
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Offline. The project's RAW codec and ALL model reader (original_levels) over the hash-checked retail disc copy, plus a new numpy/Pillow preview renderer (research/unused-content/render-model.py); no game launch
question: Do The Cutting Room Floor's claims about TEST, PLANT12 and COPYOFLE.RAW on the Windows version hold up against the PC files?
result: Yes, as far as PC files can show. COPYOFLE.RAW holds every early graphic the page lists, plus fully different pages 4 and 14. TEST is a mermaid figure textured only from character page 16. PLANT12's petals sample the gold-berry art on page 12, which is identical in every level, and its bulb shares plant 7's texels. The Rascal origin and the exploding-plant lineage remain unverified
status: complete-bounded
created: 2026-10-12
updated: 2026-10-12
evidence: [EXP-20261012-006]
tags: [experiment/static, re/assets]
---

# EXP-20261012-007 - Unused disc content checked offline

## Question

The user pasted The Cutting Room Floor's "A Bug's Life (Windows)" page
([[External Source Registry#SRC-TCRF]]) and asked for its claims to be checked
offline. [[EXP-20261012-006 - Creature types from the character loader]]
had already shown that TEST and PLANT12 are never requested.

## Method

- **Level files.** Texture pages were decoded with
  `original_levels.texture_image` from `LEVEL04/COPYOFLE.RAW` and
  `LEVEL04/LEVEL.RAW`, then diffed page by page.
- **Models.** `TEST.ALL`, `PLANT07`, `PLANT11` and `PLANT12` were parsed with
  `original_levels.creature_model`.
- **Previews.** `research/unused-content/render-model.py` renders the stored
  pose, without animation:
  - faces use vertex colours, or texture-page texels at `(tag >> 8) & 31`,
    `u = word & 255`, `v = word >> 8`;
  - texels are modulated by vertex colour.
- **Plant requests.** Each level's plant list was recomputed with the
  `0x00416100` rule ([[FUNC-97C95BA5572D-00416100]]).

## Images

The pictures are derived from game assets, so they are not committed. They are
in `work/experiments/EXP-20261012-007/`:

- `copyofle/compare-page-NN.png`: early on the left, shipped on the right.
- `test-shape.png` and `test-textured-training.png`.
- `plant12-textured.png`, `plant11-textured.png` and `plant07-textured.png`.
- `plant12-uv-vs-berries.png`.

## Findings

### COPYOFLE.RAW

It is an earlier City Entrance RAW:

- 28 packets, against `LEVEL.RAW`'s 65;
- no page 3;
- no `0x101`/`0x102` model packets.

Ten of its fifteen shared pages differ, and the page's items are all there:

- **Cola can (page 1):** early brown can with a Traveller's Tales logo on the
  label; shipped red can with a nutrition panel and barcode.
- **HUD plant sprite sheet (page 28):** grey up-arrow plants (shipped: blue
  cones), grey spheres in leaves (shipped: green spheres; read as the early
  bubble shield, inferred), and different berry colours and red crosses.
- **Dandelion seed and super-jump power-up (page 29):** a soft grey seed
  (shipped: dark spiky puff) and a white-and-blue top (shipped: stacked blue
  cone). A grey block stands where the shipped page has a red X.
- **Page 30:** a different plant row, a different "PAUSE/DEMO" typeface, and
  a green-veined dark ball (shipped: red-veined green ball).

Beyond the page:

- **Page 4** is entirely different. It holds outdoor textures (clover, soil,
  clouds, bark) where the shipped level has cardboard-box art.
- **Page 14** is an abstract pattern where the shipped level has a box
  backdrop.

### TEST

- **Model.** 327 faces in 37 parts. Its silhouette is a humanoid upper body
  with arms, tapering into a long tail with a forked fin: a mermaid.
- **Texturing.** Every face samples page 16, the character page `FLICK.ALL`
  also uses. Its own texture is not on the disc. Any level would therefore
  paint it with that level's character art; the render with Training's page
  16 looks like that.
- **Not checkable here.** The page's statement that it comes from Traveller's
  Tales' *Rascal* (Atlantis Present) would need Rascal's files.

### PLANT12

- **Shape.** A red-orange striped bulb in a ring of spiky golden petals, with
  a stem and leaves. One part is stored far from the origin.
- **Petals.** 75 of the 79 faces sample the gold-berry cluster art at the
  bottom-left of page 12. Page 12 is byte-identical in all 17 levels. So the
  "petals resembling a gold berry" are the gold berry's own texture.
- **Bulb.** The bulb samples page 11 texels (UV 129–189). Only one shipped
  plant shares them: plant 7 (24 faces), a red-orange bulb with leaves on top.
- **Plant requests.** Plant 11 is requested only by Anthill Pt 2 (and by
  engine 16, which requests almost every plant). PLANT11 is a spiky brown pod
  with a purple top and does not resemble PLANT12.
- **Not established.**
  - Which plant explodes in Anthill Pt 2.
  - Whether PLANT12 is an earlier form of it.

  The shared bulb texels with plant 7 are a lead only.

## Confirmed, inferred, unknown

- **Confirmed (static, PC files).**
  - COPYOFLE.RAW's pages contain the early graphics described.
  - TEST is textured only from page 16 and has a mermaid silhouette.
  - PLANT12's petals use the gold-berry art, on a page shared by every
    level.
  - PLANT12's bulb uses plant 7's texels.
- **Inferred.**
  - The early bubble shield reading of page 28's grey spheres.
  - That COPYOFLE.RAW predates City Entrance's final texture set.
- **Unknown.**
  - TEST's *Rascal* origin.
  - Which plant explodes in Anthill Pt 2.
  - The placeholder berry graphics and the PlayStation button graphic: the
    page names no file.
  - The development-text sub-page.

## Artifacts

- `reports/unused-content/EXP-20261012-007.json`: page differences, model
  facts, and the per-level plant request table.
- `research/unused-content/render-model.py`.
