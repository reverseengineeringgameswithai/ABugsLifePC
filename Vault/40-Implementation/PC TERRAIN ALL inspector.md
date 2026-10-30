---
type: implementation
status: supported-read-only
created: 2026-08-15
updated: 2026-10-02
tags: [implementation, re/file-format, milestone/m3]
---

# PC TERRAIN ALL inspector

See [[PC barrier translation prototype]] for the new size-preserving edit API
and EXP-004's live changed/restored-file proof. The inspector and height model
remain read-only. [[PC floor translation prototype]] now adds a bounded rigid
floor edit and a fixed visual companion; general mesh writing remains open.
(Later, 2026-09-07: PC Blender level authoring's compiler,
`level_scene_build.py`, writes authored scene meshes and rebuilds collision
floor groups for its pinned profile; this inspector stays read-only.)

`reimplementation/ablpc/terrain_barriers.py` adds the bounded kind`0x101`
read-only parser, preserving unknown words and raw bytes. The companion
`scripts/terrain-barrier-probe.py` reuses the earlier loader to compare original
candidate collection and exercise movement after original landing establishes
grounded contact. See [[PC TERRAIN ALL barrier strips]] and
[[EXP-20260904-003 - Barrier grammar and landing-seeded grounded movement]].
The read-only parser remains separate from the bounded edit APIs.

The complementary offline instruction tool is
`scripts/terrain-retail-probe.py` (run with `.venv/bin/python`). It loads
hash-pinned Level01/Level03 and PLANTTER through original retail instructions,
constructs original bounds/buckets, and records real candidate admission and
controlled movement response. It is not a collision reimplementation or writer.
See [[EXP-20260904-002 - Retail collision admission and separate XZ barriers]]
for its initializer slice, nongrounded-input scope,22 movement controls and
source hashes. The original height-model API below is unchanged.

`reimplementation/ablpc/terrain_all.py` is a read-only, lossless parser for the
bounded PC `TERRAIN.ALL` source-descriptor layout in
[[PC TERRAIN ALL collision descriptor source]]. It does not edit or serialize
game assets.

Inspect only records whose source/result word is 1:

```bash
python -m reimplementation.ablpc.terrain_all \
  work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL03/TERRAIN.ALL \
  --result-word 1
```

Add `--json` for structured output. The TSV/JSON reports source record and
payload offsets, shifted runtime base coordinates, the conservatively named
source fields, and X/Z bounds only when the bounded collision-group grammar
parses.

The parser rejects impossible directory/count/payload relationships, malformed
groups, missing negative terminators, and negative spans when world bounds are
requested. It preserves the complete source bytes, raw records, raw payloads,
cell words, terminator trailer, and unknown suffix. Never point it at or write
under `originals/`; use a read-only work copy.

Validation authority: [[EXP-20260815-131 - Level03 collision geometry and M3.5 disposition]].
