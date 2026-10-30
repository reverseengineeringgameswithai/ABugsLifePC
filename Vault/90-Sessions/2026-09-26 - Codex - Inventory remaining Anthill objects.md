---
type: session
date: 2026-09-26
agent: Codex
status: complete
tags: [session, research/anthill, implementation/blender]
---

# Inventory remaining Anthill objects

The user requested static investigation of the remaining original Anthill
objects. Entry commit `ccee6b8`, clean Git. Read the current
Vault handoff, relevant MOC, canonical operating manual, charter and Ghidra
export caveats. No subagents, game launch, Blender launch, native-code
emulation, external comparative research or original-file writes occurred.

[[EXP-20260926-001 - Static Anthill remaining object inventory]] accounts for
all 624 original scene records, 218 geometry blocks, RAW actors, pickups and
required scenery texture pages. [[PC Anthill remaining object inventory]] owns
the candidate table, exact source offsets, import limitations and useful first
batch. The private searchable gallery contains 192 inspected remaining/partial
geometry cards;126 are primary candidates, many of them landscape variants.

New research tools under `research/anthill-inventory/` reuse existing parsers,
preserve opaque source bytes and write decoded artwork only under `work/`.
The one additional format view follows independently derived static PC header
arithmetic for a negative-count mesh. It has synthetic regressions and is
not connected to the importer/compiler. Public report
`reports/anthill-inventory/EXP-20260926-001.json` contains metadata and evidence
bindings only. No game assets enter Git.

The review distinguishes disabled retained source bytes from objects a
derived build enables for drawing. It finds useful
stone, twig/branch, leaf, vine, platform and animated-flora candidates; their
appearance labels are inferences. General collision pairing and the cup-like
mesh's auxiliary behavior remain unknown. All needed scenery pages 0–4 are
available, including the later page 3 packet. Actor families and pickup
categories are already supported or preserved through their separate paths.

Provisional-output corrections are explicitly recorded in the experiment and
research README: the initial page scan, unscaled object selector offset and
a hand-entered test expectation. The accepted packet is only
`work/experiments/EXP-20260926-001/verified/`. Existing saved source/build hashes
match the previous importer report. Current State, Known Unknowns, Decision
Log, Roadmap, authoring/research MOCs and session/experiment indices are updated.
Obsidian settings and local UI state are preserved.

## Validation

The 18 inventory regressions pass, including odd/even negative layouts, every
truncation, malformed counts/indices, immutable source retention, both object
selector layouts and the pinned original/base census. The broader focused
`make check` passes **309 tests, 7,078 deselected in 7.93s**. Its Python,
compatibility, tracked-file and whitespace gates pass. Vault lint reports
1,115 notes, zero errors/warnings; briefing generation succeeds. The first
Vault gate identified missing experiment frontmatter, corrected before this
passing run. The final host audit reports no game processes, null sinks or
open sessions. Obsidian configuration bytes equal Git HEAD. Saved source/build
hashes were checked again.

The focused command deliberately excludes the existing native-relocation test
to keep all work in this task static:

```bash
PYTEST_ADDOPTS='-k "(anthill_inventory or asset_textures or level_dat or terrain_foliage or terrain_scenery or briefing or vault_lint) and not native_relocation" --basetemp=work/tmp/anthill-inventory-check -o tmp_path_retention_policy=failed' make check
```

Logs and their hashes are recorded in the public report.
The full historical recovery suite is not claimed passing; its unchanged
known failure remains [[Known Unknowns#Current regression-gate failure]].

## Handoff

Static investigation is complete. No object was imported. An import should
start with checked ordinary visual donors and account for allocation before
adding payloads; collision and native behavior need independent evidence. Git
checkpointing records this research, not gameplay acceptance.
