---
type: register
status: active
updated: 2026-10-29
tags:
  - research/provenance
  - research/cross-port
---

# External Source Registry

External sources are not part of the ABLPC repository. Paths are local discovery hints; durable claims cite the source ID, commit, repository-relative path, and locator.

## SRC-PS1-ABL

| Field | Value |
|---|---|
| Source ID | `SRC-PS1-ABL` |
| Platform | Sony PlayStation |
| Purpose | Comparative reverse-engineering evidence and experiment inspiration |
| Local path | `~/Downloads/ABL` (outside the repository) |
| Repository | Git repository, branch observed as `master` |
| Observed commit | `1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51` |
| Observed date | 2026-08-15 |
| ABLPC relationship | External and read-only; not vendored or linked |
| Trust boundary | PS1 facts do not establish PC facts |

The observed commit identifies the source snapshot only. A read-only
`git log -1` on 2026-10-02 still reports it as HEAD of `master`. On 2026-08-15 the
external working tree was heavily dirty; [[XPORT-20260814-001 - Training grain selector and count]]
and [[XPORT-20260815-002 - Level03 type-1 row respawn hypothesis]] therefore
read only committed blobs through `git show` and `git grep`.
No working-tree content was used or modified. Before citing another file,
record its repository-relative path and, when working-tree provenance matters,
its own SHA-256.

Comparison notes in `Vault/20-Research/Cross-Port/` (all cite `1186eb6…`):

- [[XPORT-20260814-001 - Training grain selector and count]]
- [[XPORT-20260815-002 - Level03 type-1 row respawn hypothesis]]
- [[XPORT-20260816-003 - Subsystem inventory seeding]]
- [[XPORT-20260816-004 - Camera system shape]]
- [[XPORT-20260817-005 - Berry contact array and type marker shape]]
- [[XPORT-20260818-006 - Berry equip byte candidate from replay-seeded static search]]
- [[XPORT-20260818-007 - PS1 Blender-to-native level authoring pipeline and format leads]]
- [[XPORT-20260819-008 - Bidirectional semantic bridge coordination]]
- [[XPORT-20260908-009 - Anthill enemy placement and model correspondences]]
- [[XPORT-20260909-010 - Training speech replacement]]

## SRC-TCRF

| Field | Value |
|---|---|
| Source ID | `SRC-TCRF` |
| Platform | Community wiki (tcrf.net, "The Cutting Room Floor"), page "A Bug's Life (Windows)", last edited 2026-07-14 (CC BY 3.0) |
| Purpose | Pointers to unused content, reported by the user |
| Access | On 2026-10-12, tcrf.net returned an AI-agent block page instead of article content. Agents do not work around it. The user pasted the Windows page's text the same day; only paraphrases are kept here |
| ABLPC relationship | External; nothing copied |
| Trust boundary | A lead only. It establishes no PC claim; PC evidence must decide, as for [[Cross-Port Evidence Policy]] sources |

Uses:

- **2026-10-12, PLANT12.** The user reported that it is listed as an unused
  plant. The PC evidence agreed independently (static request tables, a
  single reference and runtime logs): [[FUNC-97C95BA5572D-00416100]],
  [[EXP-20261012-006 - Creature types from the character loader]].

Claims on the Windows page, with their PC status on 2026-10-12:

| Page claim (paraphrased) | PC status |
|---|---|
| `TEST.ALL`/`TEST.ANM` is an unused model, seen only by renaming it over a used one. The page identifies it as a wrongly textured mermaid from Traveller's Tales' *Rascal* | **Unused: consistent.** No `chars\test` string in the executable, and no saved log loads it; the files are dated 1998-06-28. The mermaid identity is unchecked (needs a render). (Later: a render shows a mermaid silhouette textured only from character page 16, [[EXP-20261012-007 - Unused disc content checked offline]]. The *Rascal* origin is unverifiable here) |
| `PLANT12.ALL`/`.ANM` is an unused plant. Its petals resemble a gold-berry sprite, and it is perhaps an early exploding plant from Anthill Part Two | **Unused: confirmed** by the request tables, the single reference and runtime logs. Its appearance and the exploding-plant link are unchecked. (Later: its petals sample the gold-berry art on page 12, which is identical in all levels, and its bulb shares only plant 7's texels, [[EXP-20261012-007 - Unused disc content checked offline]]. The exploding-plant link is unproven) |
| `LEVEL04/COPYOFLE.RAW` is an earlier, different version of `LEVEL.RAW`, with older City Entrance textures and sprites | **Unused: consistent.** The project's RAW codec decodes it: 28 packets, 264,716 B against `LEVEL.RAW`'s 541,536 and 65 packets. It has 11 type-34 packets against 14, and no `0x101`/`0x102` packets. The executable never names it, and no saved log loads it. The older-texture contents are unchecked. (Later: all listed items located: cola on page 1, HUD plants on page 28, the dandelion seed and super jump on page 29. Pages 4 and 14 also differ entirely, [[EXP-20261012-007 - Unused disc content checked offline]]) |
| Placeholder berry graphics and a graphic with PlayStation button images | Unchecked; the page names no file |
| A development-text sub-page | Not read |

## SRC-WINE-SOURCE

| Field | Value |
|---|---|
| Source ID | `SRC-WINE-SOURCE` |
| Platform | Runtime environment source (Wine, the compatibility layer every hardware arm uses) |
| Purpose | Direct3D API constants and the defaults Wine gives a new device, for [[EXP-20261018-008 - Direct3D render states and the depth rule]] |
| Files read | `include/d3dtypes.h`; `dlls/wined3d/stateblock.c` (`init_default_render_states`); `dlls/ddraw/device.c` (partly) |
| Repository | `github.com/wine-mirror/wine`, branch `master`, read through `raw.githubusercontent.com` |
| Observed commit | Not pinned. Master on 2026-10-18; the installed Wine (11 staging, [[Environment Status]]) may differ |
| Observed date | 2026-10-18 (read by a fetch subagent, quoted lines only) |
| ABLPC relationship | External; nothing copied into the repository beyond quoted constant names and values |
| Trust boundary | API numbering and Wine's runtime defaults only. It says nothing about what the game does. A default it reports is the environment's behaviour, and a Windows Direct3D runtime may differ |

Verbatim lines relied on: `D3DRENDERSTATE_ZENABLE = 7`,
`D3DRENDERSTATE_ZWRITEENABLE = 14`, `D3DRENDERSTATE_ZFUNC = 23` and the
other state values listed in EXP-20261018-008, plus
`rs[WINED3D_RS_ZENABLE] = WINED3D_ZB_TRUE;`,
`rs[WINED3D_RS_ZWRITEENABLE] = TRUE;` and
`rs[WINED3D_RS_ZFUNC] = WINED3D_CMP_LESSEQUAL;`, which are unconditional in
`init_default_render_states`. The ddraw layer's depth-stencil update
(`d3d_device_update_depth_stencil`) was not read.

## SRC-DUCKSTATION-DBG

| Field | Value |
|---|---|
| Source ID | `SRC-DUCKSTATION-DBG` |
| Platform | Host tooling (PS1 emulator fork) |
| Purpose | Debugger/agent-tooling design patterns only; informed the runtime tooling uplift (`DEC-20260812-019`, [[Runtime Tooling]]) |
| Local path | `~/duckstation` (outside the repository) |
| Repository | Git repository, branch observed as `external-debugger-control` |
| Observed commit | `fe0cca16b` |
| Observed date | 2026-08-12 |
| ABLPC relationship | External and read-only; not vendored or linked. Only methodology (structured completion results, capabilities self-description, additive-only schemas, ownership-proof process handling) was reused |
| Trust boundary | Tooling methodology only. It establishes no PC or PS1 game semantics and is not a cross-port evidence source under [[Cross-Port Evidence Policy]] |

The reused patterns are engineering conventions, not game facts. This source
never establishes a PC behavioral claim; borrowing a schema or safety pattern
imports no semantics.

## Consultation log

Dated reads of an external source that are not already recorded in a
comparison note's own provenance.

### 2026-09-09 bounded Training speech comparison

SRC-PS1-ABL HEAD remains `1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51`.
[[XPORT-20260909-010 - Training speech replacement]] records the committed
paths and dated XA extension evidence consulted for the PC-native EXP005
question. External tree remains dirty and untouched; only committed blobs
were used. PC files and original instructions independently establish PCM
lesson replacement; no PS1 sectors, binaries or assets were copied.
