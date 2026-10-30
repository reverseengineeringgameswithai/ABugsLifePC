---
type: experiment
id: EXP-20260818-007
date: 2026-08-18
question: Can R1 close the retail type-0x41 static-mesh code-to-data link, provide a lossless bounds-checked parser, and select one exact causal candidate without claiming the unrun runtime result?
status: completed-offline
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; static retail bugs.exe disassembly plus offline retail LEVEL DAT corpus; no game execution or runtime write
working_directory: /home/dev/ABLPC
addresses:
  - "0x004498f0"
  - "0x00449b2c"
  - "0x00449b32"
  - "0x0045a7f0"
  - "0x0045a81e"
  - "0x0045a89b"
  - "0x0045a8c3"
  - "0x0045c79c"
  - "0x0045c822"
file_offsets:
  - "LEVEL03/LEVEL.DAT:0x23a0"
  - "LEVEL03/LEVEL.DAT:0x3cd4"
  - "LEVEL03/LEVEL.DAT:0xc504"
  - "LEVEL03/LEVEL.DAT:0xc50a"
  - "LEVEL03/LEVEL.DAT:0xdb44"
result: R1 offline boundary completed; exact type-0x41 consumer linked, parser round-trips all 2543 retail payloads, and one guarded Level03 component edit is specified. Visible-ground identity and causal movement remain unconfirmed until R2.
tags:
  - re/experiment
  - re/static
  - re/file-format
  - re/rendering
---

# R1 static mesh consumer, round trip, and causal candidate

## Scope

This executes only the offline R1 gate in
[[New-level authoring roadmap (terrain, collision, materials)]]. It performs no
game launch, debugger operation, runtime write, or user-visible experiment.
R2 remains separately authorization-gated.

## Confirmed: code-to-data consumer

Retail raw disassembly corroborates the R0 data grammar independently:

1. `FUN_004498f0` cases `1/0x41` replace the instance pointer with instance
   `+0x10`, then load object `+0x14` at `0x00449b2c` and call
   `FUN_0045a7f0` through thunk `0x00401604` at `0x00449b32`.
2. `0x0045a81e` establishes payload `+4` as the vertex base.
3. `0x0045a89b`-`0x0045a89e` computes
   `vertex_base + vertex_count * 12`, landing on the tag.
4. `0x0045a8c3`-`0x0045a8d7` reads the tag and branches on bit 0. The
   candidate's even tag reaches the quad arm at `0x0045c79c`.
5. `0x0045c79c`-`0x0045c7b2` skips tag/count, extracts structural tag
   fields, and retains `face_count`.
6. `0x0045c822`-`0x0045c89e` reads four face words and adds them directly to
   the vertex base. This is instruction-level evidence that the face values are
   vertex **byte offsets**, not plain indices.

This closes EXP-006's partial consumer trace. It does not by itself identify a
mesh as visible ground.

## Confirmed: parser and reconstructive round trip

`reimplementation/ablpc/level_dat.py` now parses only the evidenced masked
dispatch `0x41` chain. It bounds-checks every object, geometry, vertex, header,
and face read; rejects negative/impossible counts; rejects face offsets that are
not aligned to 12 or lie outside the vertex array; and retains every unknown
field under an offset-based name.

Corpus validation over
`work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL*/*.DAT`:

```text
files parsed: 21
type-0x41 payloads reached: 2543
payloads encoded byte-exact: 2543
face vertex references checked: 146030
failures: 0
```

The denominator is every type-`0x41` record reached, not only successful
parses. The broken `work/copies/M3-training-51-grains/` artifact in `KU-082`
was not used.

Synthetic regression fixtures cover both tag-bit-0 face arities, nonzero
unknown vertex fields, unknown face words, impossible counts, misaligned face
references, wrong dispatch, expected-value mismatch, and exact edit locality.

## Confirmed structural tag fields; semantics unknown

The retail instructions establish:

- `tag & 1`: face arity branch, triangle when set and quad when clear.
- `tag & 0x1f`: internal branch selector.
- `tag & 0x60`: bits incorporated into downstream render flags.
- `(tag >> 8) & 0x1f`: index used against `DAT_005836a4`.

No semantic promotion is made. These are not named material, culling, texture,
or blend fields. The three bytes at vertex `+8..+0a` and the per-face second
word group also remain offset-named despite colour/UV plausibility.

## Exact R2 candidate

Source is retail `CD/LEVEL03/LEVEL.DAT`, 274,812 bytes, SHA-256
`bda28dc7287ebc3648998425b3c09f19d6470a85c9fcd439cca5ad8e391c0f2b`.

| Link | Exact value |
| --- | --- |
| primary scene record | index 167, file `0x23a0`, flags `0x0051` |
| object | file `0x3cd4`, XYZ `(28854,-196,39931)`, Euler `(0,0,0)` |
| geometry | file `0xc504`, 474 vertices, tag `0x0060`, 205 quads |
| vertex 0 | file `0xc508`, `(476,-891,-3470)` |
| face 0 | file `0xdb44`, vertex byte offsets `(0,12,24,36)` |

Candidate guard and transform:

```text
file component offset: 0xc50a
expected signed int16: -891
replacement signed int16: 1157
before vertex bytes: dc 01 85 fc 72 f2 00 00 08 14 18 00
after vertex bytes:  dc 01 85 04 72 f2 00 00 08 14 18 00
changed physical byte: 0xc50b only
predicted derived SHA-256: 492a53e8f32a2416a400ac4127c01938d3438bf3bc5fe8b5b5a34639581adf80
```

Prediction: because the object Euler triple is zero, vertex 0 of face 0 moves
`+2048` along the transform's second input axis while the other three face
vertices remain unchanged. Competing outcomes are no visible change, a
different primitive/corner moving, load rejection, or a non-geometric effect;
any one rejects or narrows the candidate rather than being normalized away.

## Explicit non-results

- The candidate was not written to a launched game copy.
- No control/candidate frame or runtime receipt exists yet.
- The type-`0x41` mesh is not promoted to confirmed visible ground.
- Screen direction, world scale, colour, UV, material, and tag semantics remain
  unknown.
- Type-`0x01` variants, collision linkage `KU-081`, and static-mesh insertion
  remain outside this packet.

## R2 acceptance gate

R2 requires fresh explicit user authorization, a retail-derived copy under
`work/`, compare-before-write using the exact guard above, unchanged-executable
control/candidate arms, the complete six-marker Direct3D gate, durable visual
evidence of the predicted corner outcome, pre/post `make session-audit`, and a
receipt recording derived hash and byte-local diff.

## Links

- [[PC LEVEL DAT static mesh]]
- [[EXP-20260818-006 - R0 the static mesh format and where visible ground lives]]
- [[Known Unknowns#KU-079 - The render-geometry command grammar (the LEVEL.DAT draw-command stream)]]
