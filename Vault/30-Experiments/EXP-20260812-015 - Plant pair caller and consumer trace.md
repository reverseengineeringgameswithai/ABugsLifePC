---
type: experiment
id: EXP-20260812-015
date: 2026-08-12
question: Which PC callers request the plant ANM/ALL pairs shared by Training and Level 01, and where do their buffers first diverge downstream?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora static analysis and retained Wine logs
environment_version: GNU objdump 2.44; Ghidra baseline export; Wine logs from wine-11.0-staging
working_directory: /home/dev/ABLPC
configuration: Static call/data-flow trace correlated with accepted hardware Training and Level 01 explicit load order
artifacts:
  - static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json
  - static/exports/BIN-97c95ba5572dce63/M2-plant-resource-static-trace.md
  - dynamic/wine/RUN-WINE-20260812-000634/bugs.log
  - dynamic/wine/RUN-WINE-20260812-114514/bugs.log
addresses:
  - 0x00416100
  - 0x00444B70
  - 0x00444C40
  - 0x00445020
  - 0x00448010
  - 0x004AE240
file_offsets:
  - 0x02
  - 0x08
result: paired-requests-share-caller-immediate-consumers-distinct
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/static
  - re/resources
  - re/file-access
---

# EXP-20260812-015 - Plant pair caller and consumer trace

## Question

Which PC callers request the basename-matched plant `.ANM`/`.ALL` pairs shared
by Training and Level 01, and where do their buffers first diverge downstream?

## Inputs and procedure

- Exact executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Queried function callers, callees, data references, and decompilation from
  the existing Ghidra evidence export.
- Independently checked extension strings, base strings, call instructions,
  arguments, cursor arithmetic, and parser instructions with GNU `objdump`
  against the exact derived work-copy executable.
- Correlated the predicted pair order with unchanged accepted hardware logs
  `RUN-WINE-20260812-000634` and `RUN-WINE-20260812-114514`.
- Read only the first-level header words/offsets of the four selected `.ANM`
  files to determine whether a future bounded multi-file inspector is viable.

No runtime was launched or modified. No PS1 source was consulted.

## Static result

`0x00445020` calls `0x00416100` to collect plant IDs, maps each ID to a built-in
base path, and calls `0x00444C40`. For the four pairs shared by both scenes:

| Plant | Base string | Internal ID | Pair-loader call site |
|---|---:|---:|---:|
| 04 | `0x004DDCE4` | `0x6B` | `0x0044575E` |
| 05 | `0x004DDCD0` | `0x6C` | `0x004457B5` |
| 06 | `0x004DDCBC` | `0x6D` | `0x0044580C` |
| 10 | `0x004DDC6C` | `0x71` | `0x00445968` |

Within the one pair-loader invocation:

- `0x00444C40` appends `.anm` from `0x004DDC14`, loads it through
  `0x004AE240` at `0x00444CD8`, advances the shared arena cursor by the
  4-byte-aligned returned size, and passes the buffer to `0x00444B70` at
  `0x00444D21` for in-place offset relocation.
- It then calls `0x00448010` at `0x00444D69`. That helper appends `.all` from
  `0x004DE028`, loads through `0x004AE240` at `0x00448079`, and immediately
  walks file-derived tables into the shared array rooted at `0x005A9660`.

Thus the two extensions share base-path selection and arena ownership but
have distinct immediate consumers. Their paths later converge in shared
resource/object tables; complete pair semantics are not established.

## Buffer boundary

`0x004671D0` begins the scene arena at `0x0063E998`, carries a cursor through
earlier loads, stores the current cursor in `0x005C5D58`, and calls
`0x00445020` at `0x004679C2`. No explicit capacity accompanies the cursor.

- `.ANM`: the whole-file byte size controls aligned cursor advancement. The
  first consumer reads a signed count at `+0x02` and relocates nonzero dword
  offsets beginning at `+0x08`.
- `.ALL`: `0x00448010` ignores the whole-file loader return and advances the
  cursor from embedded lengths. No file-size argument bounds its table walk.

This difference is retained as a tooling constraint, not normalized away.

## Runtime correlation

The static sequence predicts `.anm` immediately followed by `.all` for each
selected ID. The accepted hardware logs show exactly that order:

- Training: plant 05, 04, 10, 06;
- Level 01: plant 05, 07, 04, 10, 09, 03, 08, 02, 06.

`0x00416100` always emits ID 5 first and derives later IDs from two runtime
tables, consistent with both logs. The exact field producing each later ID is
not yet identified.

## Candidate-format decision

The four shared `.ANM` files have exact sizes 1,802, 1,168, 5,066, and 1,802
bytes. Their `+0x02` counts are 3, 4, 3, and 3, and every corresponding
first-level offset at `+0x08` is inside the exact file. Combined with the
loader-return size boundary and `0x00444B70` relocation loop, `.ANM` has enough
PC-native evidence to enter a later bounds-checked multi-file inspection
packet.

Exact first-level offsets are:

- plant 04: `0x14`, `0x2AE`, `0x470` within `0x70A` bytes;
- plant 05: `0x18`, `0x16C`, `0x254`, `0x3A8` within `0x490` bytes;
- plant 06: `0x14`, `0x6EE`, `0xC18` within `0x13CA` bytes;
- plant 10: `0x14`, `0x2AE`, `0x470` within `0x70A` bytes.

`.ALL` does not yet qualify for promoted parsing because its first consumer
does not use the loader byte count to bound embedded offset/length walks.

## Confirmed

- The four selected basename pairs all use the same PC pair-loader path.
- `.ANM` and `.ALL` requests have separate whole-file-loader call sites and
  distinct immediate consumers.
- Both file types occupy the same caller-managed scene arena; `.ANM` advances
  it by aligned file size, while `.ALL` advances it from embedded lengths.
- Retained Training and Level 01 request order independently agrees with the
  static base-path and extension construction.

## Inferred

- The two files are related resources because they share one selected base
  path, resource ID, and coordinating routine. Their complete relationship is
  not known.
- `0x00446970` is a later convergence consumer candidate, not yet a complete
  semantic bridge.

## Unknown and limitations

- The exact producers of plant IDs after literal ID 5.
- Any direct dependency from an M1 scene record/positive target to a plant ID
  or file path.
- Arena capacity, malformed-file behavior, and semantic field names.
- Whether ANM or ALL alone represents a complete visible asset.

## Contradictions and negative results

- The filename pairs do share a coordinating caller, but they do **not** share
  the same immediate parser or size boundary.
- `.ALL` has a readily visible parser path, but the absence of a consumed file
  size makes it the weaker first tooling target.
- No dynamic debugger run was needed; retained hardware logs supplied an
  independent request-order check without changing execution.

## Result and follow-up

M2.2 is complete. M2.3 should trace one selected ID from the two inputs read by
`0x00416100` back to its exact PC data producer and determine whether that
producer intersects the M1 `LEVEL*.DAT` record/payload path. `.ANM` remains the
selected later format-inspection candidate; parser authoring waits for the
dependency bridge packet.
