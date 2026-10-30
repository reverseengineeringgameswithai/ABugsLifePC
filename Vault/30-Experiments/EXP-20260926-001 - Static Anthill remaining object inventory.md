---
type: experiment
id: EXP-20260926-001
date: 2026-09-26
status: complete
question: Which original Anthill objects outside the existing donor library can be characterized statically for import?
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Linux; Python file parsers; static Ghidra queries and Capstone disassembly
working_directory: /home/dev/ABLPC
artifacts: [reports/anthill-inventory/EXP-20260926-001.json]
result: Complete static inventory and private gallery; new imports and behavior acceptance remain separate
tags: [experiment/static, research/anthill, implementation/blender]
---

# EXP-20260926-001 - Static Anthill remaining object inventory

## Question and boundary

Which original PC Anthill objects are outside the existing Blender donor
library, and what can be established about importing them through static
analysis? Completion here means a bounded inventory and readiness review, not
new object support or native behavior acceptance. User explicitly requested
static investigation. Entry commit `ccee6b8`; no external comparative sources.

## Inputs and method

Copied source files under `work/studio/fliks-adventure/levels/anthill/`:

| Input | SHA-256 |
|---|---|
| `inputs/original.dat` | `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53` |
| `base-game/PC/BUGS/CD/LEVEL01/LEVEL.RAW` | `c07452bafcf3799b55574d1622a37189358f5debcbd1127e167fd0fe0181700e` |
| `inputs/original.terrain` | `62f3b73f21630eb19c04e585a92e1f3e32a76fdcb6ec36bae18f9c1ec3a2a868` |
| `inputs/original.exe` | `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878` |

1. Parse the DAT prefix independently and validate all scene/object pointers.
   Group by exact geometry offset, then compare complete geometry hashes.
2. Map explicit tree/mound/grass/clover/mushroom/prop/fence importer donors;
   distinguish whole geometry from selected upper-tree faces. Bind the prior
   exact Blender export to the unchanged saved `.blend` and semantic export hash.
3. Decode ordinary meshes and sprite batches with existing bounded readers;
   inspect original PC dispatch and negative-count header instructions through
   Ghidra queries and fresh Capstone disassembly from known function starts.
4. Independently derive a temporary inspection view for the one negative-count
   mesh, preserving the source and recording the opaque auxiliary extent/hash.
5. Decode all RAW packets, required scenery pages, actor slots and DAT pickups.
   Compare original geometry against the base and a derived build's scene
   pointers, retaining disabled/enabled dispatch distinctions.
6. Draw and inspect every remaining/partial geometry using Python/NumPy/Pillow.
   No original executable code is executed; these are local orthographic
   diagrams, not game screenshots. Separate appearance inference from metadata.

Reproduce with `research/anthill-inventory/README.md`. Accepted private packet:
`work/experiments/EXP-20260926-001/verified/`; public metadata:
`reports/anthill-inventory/EXP-20260926-001.json`. Each report geometry records
source records, offset, byte extent/hash, topology/page counts and donor coverage.
Native evidence: `004498F0`, `0045A7F0`, `0045A82E..0045A8B4`, and sprite
consumers `00453FF0`/`00454B70`. Queried decompiler text and machine disassembly
remain in the private experiment root; no pseudocode was copied into project code.

## Result

**Confirmed:** 624 records, 218 distinct geometry blocks; 26 whole donor
footprints and two partial ones. Outside coverage: 126 primary and 64
secondary-only blocks. All192 remaining/partial blocks have inspected gallery
cards. Every required scenery page 0–4 exists. The actors and pickup categories
already have authoring/preservation paths. The full classification, practical
candidate table and exact offsets are [[PC Anthill remaining object inventory]].

**Confirmed:** source geometry retained in disabled scene rows must not be
mistaken for an imported object. A derived build's DAT retains 217 original
blocks at pointers; none outside the mapped coverage has a recognized drawing
dispatch. Its 1,648-byte authoring headroom is a separate constraint on adding
new objects. No compiler budget, scene flags or resource allocation were changed.

**Confirmed static format:** geometry `0x2F700` uses count−109 and the dispatch 4
mesh path. Commands begin at `0x2FEB0`, after ordinary vertex bytes and a
656-byte opaque span. The stored view has 102 faces. **Inferred appearance:** a
hollow green plant cup. **Unknown:** functional identity, auxiliary behavior
and corresponding native collision. Static surface decoding alone is not
functionality-preserving import support.

## Corrections and limits

The initial packet scan only found early pages; the full 69-packet traversal
locates page 3 at `0x46CD9`. `census-01` is superseded. A provisional generic
selector formula misread unscaled objects' last Euler byte. Checking
`004498F0` established +19 for unscaled objects and +25 for scaled objects;
`verified/` replaces selector labels in `census-02`, `census-03` and `final/`.
Topology, mesh bytes and preview surfaces were unaffected. Synthetic tests
now distinguish selector bytes from rotation/scale bytes in both layouts.

The first negative-mesh fixture assertion had an incorrect hand-entered
expected auxiliary length. The instruction arithmetic and parser agree on 656;
the expectation was corrected. No malformed-input acceptance was relaxed.
The final tests cover odd/even counts, every truncation, impossible counts,
offsets, mutable sources and bad face references. No significant contradictory
PC evidence remains hidden by the correction; provisional artifacts remain
private and explicitly superseded.

Remaining unknowns: native animation acceptance for new selector profiles,
general visual/collision pairing, negative-format auxiliary semantics,
semantic/damage behavior, exact secondary pairing and allocation strategy.
Appearance names are hypotheses from drawings. All original/source/build bytes
are preserved; no launch, memory action, game build or Blender session occurred.

## Validation and handoff

18 inventory tests pass, including pinned source/RAW/base comparisons. The
session note records the larger focused `make check`, Vault/Git checks and
read-only host audit. [[Known Unknowns]] records the remaining gates.
[[2026-09-26 - Codex - Inventory remaining Anthill objects]] owns closure.
