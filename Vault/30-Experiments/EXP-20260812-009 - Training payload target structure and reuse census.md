---
type: experiment
id: EXP-20260812-009
date: 2026-08-12
question: What bounded positive-count structures and PC consumers correspond to the Training payload targets, and how widely are they reused?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora static analysis and local corpus inspection
environment_version: Python 3.14.6; GNU objdump 2.45.1; Ghidra export from 12.1.2
working_directory: /home/dev/ABLPC
configuration: Exact-hash PC executable and user-owned LEVEL DAT work copies; no PS1 source consulted
artifacts:
  - reports/level-dat/EXP-20260812-009-training-primary-payload-targets.json
  - reports/level-dat/EXP-20260812-009-dispatch-49-corpus.json
addresses:
  - 0x0044BD03
  - 0x0044BD4A
  - 0x004498F0
  - 0x00449933
  - 0x00449E1A
  - 0x0045A7F0
file_offsets:
  - 0x111E4
  - 0x1319C
result: positive-target-layout-and-reuse-population-bounded
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/static
  - re/file-format
---

# EXP-20260812-009 - Training payload target structure and reuse census

## Question

What bounded positive-count structures and PC consumers correspond to the
Training payload targets, and how widely are they reused?

## Inputs

- PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Training `CD/LEVEL07/LEVEL1.DAT` SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`
- Prior runtime evidence: [[EXP-20260812-008 - Training record watchpoints and individual roles]]
- Reviewable static export:
  `static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json`
- Exact executable disassembly produced read-only with GNU `objdump` from
  `work/copies/BUGS_PC-disc/bugs.exe`

## Procedure

1. Follow the `0x0044BB70` fixup path for scene records whose flag byte has
   bit `0x08` set.
2. Trace Training flags `0x0059` through the masked dispatch in `0x004498F0`
   and identify the consumer of payload `+0x1C`.
3. Reproduce the positive-count byte walk performed by `0x0045A7F0`, including
   entry-table and command-item bounds.
4. Enumerate all Training primary record-to-target references and deduplicate
   the target blocks.
5. Validate the same positive-count layout for every corpus scene record whose
   flags satisfy `(flags & 0xBFEF) == 0x49`.
6. Add only read-only inspection and a hash-/old-offset-guarded target-rebind
   operation. Test it with synthetic data and stage two Training candidates;
   do not claim original-executable acceptance without a runtime run.

## Expected

If the shared offsets are reusable rendering inputs, the fixup should relocate
the same payload field, the record dispatch should pass it to a rendering
consumer, and repeated target offsets should parse as internally bounded blocks.
Malformed or distinct layouts should fail visibly rather than be normalized.

## Observed

### PC static path

- `0x0044BD03` tests scene flag bit `0x08`. The selected path relocates the
  payload dword at `+0x1C` against the pointer stored in `0x005BA240`
  (`0x0044BD4A` through `0x0044BD57`).
- `0x00449933` masks scene flags with `0xBFEF`. Training value `0x0059`
  therefore selects dispatch value `0x49`.
- In that path, `0x00449E1A` loads payload `+0x1C` and `0x00449E20` calls thunk
  `0x00401604`, which jumps directly to `0x0045A7F0`.
- For a nonnegative first dword, `0x0045A7F0` treats the following area as
  `count × 12` bytes, then walks 4-byte command headers until a `0xFFFF` word.
  An even command mode advances 16 bytes per item; an odd mode advances 12.
  Command items address the 12-byte table through 16-bit relative offsets and
  feed transformed renderer output. The negative-count branch is different and
  remains unsupported.

### Training target blocks

The complete primary census contains 262 references to 109 unique target
blocks. Nineteen targets are shared by multiple records; the most reused target
has 33 primary references. All 109 blocks pass bounds and table-reference
validation, and each aligned end equals the next block's start from `0x38DC`
through `0x19E00`.

| Target | Primary references | Count × 12 area | Command groups | Terminator / aligned end |
|---:|---|---|---|---|
| `0x111E4` | 85, 119, 125, 126, 127, 130, 204, 213, 222, 233, 244 | 102 entries, `0x111E8–0x116AF` | `0x0060`:30×16, `0x8062`:15×16, `0x8064`:10×16, `0x8066`:5×16 | `0x11A80` / `0x11A84` |
| `0x1319C` | 93, 113, 120–124, 128, 168–169, 248–254 | 67 entries, `0x131A0–0x134C3` | `0x0060`:28×16, `0x8062`:16×16, `0x8064`:8×16 | `0x13810` / `0x13814` |

The exact population and every group boundary are in the Training JSON report.

### Same-dispatch corpus validation

The hash-scoped corpus report scanned all 21 `LEVEL*.DAT` files previously
accepted by the prefix parser. Fourteen files contain dispatch-`0x49` records:
990 matching records resolved to 201 per-file unique positive-count target
blocks with zero errors. This does not claim that other dispatches or the
negative-count branch share the same layout.

### Prepared target-rebind candidates

- Record 124: expected `0x1319C`, candidate target `0x111E4`; staged output
  SHA-256 `b8012a95f7ec0254805bdd3cf32df2b16f2ad0926308fe8678cc2360027f720e`.
- Record 125: expected `0x111E4`, candidate target `0x1319C`; staged output
  SHA-256 `b8ea00be86de53a9b659a20f8b0023369e687c9309b61dd61fe8496393d90ed9`.

Each synthetic/local staging check changed only its selected four-byte field
(only the low two bytes differ for these particular values). These candidates
have not yet been run in the original executable.

## Confirmed

- The exact relocation and consumer path for the tested `0x49` dispatch class.
- The positive-count block grammar and exact boundaries above.
- The Training reference population and same-dispatch corpus validation counts.
- Records sharing a target supply the same target address to `0x0045A7F0`.

## Inferred

- Positive target blocks are reusable render-content blocks. The consumer
  transforms table entries and emits renderer data, but whether the block alone
  is a complete object definition remains unknown.
- The 12-byte entries contain per-vertex rendering data and command items
  describe triangle/quad-like primitives. Exact field and mode semantics remain
  unconfirmed, so the implementation retains structural names.

## Unknown and limitations

- Runtime effect of rebinding record 124 or 125 between the two target blocks.
- Exact meanings of the 12-byte fields, command mode bits, and item suffixes.
- Negative-count target layout, other scene-dispatch consumer paths, and
  cross-file generality of the grammar outside masked dispatch `0x49`.
- Whether all records sharing a target depict the same recognizable content
  after placement transforms, animation, and camera visibility are controlled.

## Contradictions

No Training contradiction was found. The executable contains a separate
negative-count branch; treating it as the positive layout would contradict the
static consumer, so the parser rejects it explicitly.

## Result

Completed. Roadmap packet M1.1 is closed with static, file-structural,
cross-file, and prior runtime support. M1.2 remains active because reusable
render content is strongly supported but the guarded target-rebind candidates
still require matched original-executable runs.

## Artifacts

- `reports/level-dat/EXP-20260812-009-training-primary-payload-targets.json`
  (SHA-256 `5f445e1a5d6786c5c555f2d233ab17abffc4ca133fbffba910bbed18ecfe50d1`)
- `reports/level-dat/EXP-20260812-009-dispatch-49-corpus.json`
  (SHA-256 `bd5b50bfedd985ae1e2cfb15651043dbcfec3aba80d95eccb60655c90fee2b0c`)
- `mods/training-primary-record-124-target-111e4.json`
- `mods/training-primary-record-125-target-1319c.json`

## Follow-up

Run the two prepared manifests and an unchanged control through the matched
Direct3D Training capture procedure. Test whether only the selected placement
adopts the contrasting target's visible render content.
