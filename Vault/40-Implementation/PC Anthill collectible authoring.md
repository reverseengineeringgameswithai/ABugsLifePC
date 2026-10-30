---
type: implementation
status: implemented
created: 2026-09-08
updated: 2026-10-29
evidence: [EXP-20260908-021]
tags: [implementation/modding, re/collectibles]
---

# PC Anthill collectible authoring

Native pickup kinds in the Anthill (Level01) type3F table and the limit or
effect the original engine attaches to each (EXP-20260908-021):

| Kind | PC selector | Limit / native effect |
| --- | --- | --- |
| Grain | `14` |50; native counter/goal50 |
| F, L, I, K slots | `10`–`13` |one each; bits1,2,4,8, completed mask15 awards a life below9 |
| Yellow seed token | `29` |three; seed byte `0059D9A8` starts17 and reaches68 |
| Blue seed token | `2A` |three; `0059D9A9` starts0 and reaches51 |
| Green seed token | `2B` |three; `0059D9AA` starts0 and reaches51 |
| Blue / green / gold / purple berry power-up | `23` / `21` / `22` / `24` |32 total berries; weapon byte `0059D9A7` becomes1 /2 /3 /4 |

A collectible edit replaces all67 original Anthill records of these kinds; the
three source `30` telescope records are not part of that set and remain exact.
Capacity97 is the conservative authoring limit used (95 with native FLIK),
separate from scenery/enemies, not a newly established native allocation limit.
The native50-grain goal and token resource/progression bounds motivate the limits.
Additional letters beyond one each reject to avoid the native repeated-completion
life reward. These collectible berries are separate from solid scenery clusters.

The EXP-20260908-021 build uses the existing bounds-checked/inverse-proved type3F
relocator before terrain/scenery assembly. Original table SHA is pinned; unknown
rows and all unrelated streams survive. It adds a20-byte PIC
helper at `00456B60`, guarded by full retail initializer and padding hashes and
relocation exclusion. Hook `00456ACC` sends marker80 rows to the original grain
initialization path, which retains literal Y
([[FUNC-97C95BA5572D-00456A90]]). Unmarked rows keep retail height
presets. Native `00456BA0` replaces the marker with normal active flags. This
resolves arbitrary XYZ movement without indexing the original height table using
a world coordinate. It is a file-built change, never a live write.

EXP021’s original67-pickup build retains exact terrain, plant data, RAW enemies and every
DAT byte outside the first table. Native model170/six-chunk checks pass. Live
read-only inspection confirms all authored XYZ positions and normal active flags;
ordinary input collected two grains and advanced the counter. Offline original-PC
pickup logic verifies all kinds and full progression, with feedback/audio/HUD
callbacks stubbed. Individual sprite-letter glyph identity and every color/effect
have not each received a fresh live close-up in this experiment. Full traversal,
all collectibles' reachability, planting upgrades and death/reset routes remain
manual test coverage, not established by compilation. [[Known Unknowns]].
