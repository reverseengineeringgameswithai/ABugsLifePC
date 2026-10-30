# M2 plant resource static trace

## Provenance

- Executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Review source:
  `static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json` plus GNU
  `objdump -d -Mintel` and `objdump -s` against the exact derived work-copy
  executable.
- Runtime correlation:
  `RUN-WINE-20260812-000634` and `RUN-WINE-20260812-114514`.
- Experiment: `EXP-20260812-015`.

This report records addresses, control/data flow, and file metadata only. It
does not contain a game resource payload or decompiler pseudocode.

## Static call path

1. `0x004671D0` establishes a shared scene-resource arena cursor. Its initial
   base is `0x0063E998`; after earlier scene loads, the current cursor is saved
   in `0x005C5D58`. Call site `0x004679C2` invokes `0x00445020` with pointers
   to the current object index and arena cursor.
2. `0x00445020` calls `0x00416100` at `0x00445601` to produce a terminated
   list of plant IDs. It switches on each ID and submits an exact base path to
   `0x00444C40` through thunk `0x004018A7`.
3. `0x00444C40` appends `.anm` from `0x004DDC14`. Call site `0x00444CD8`
   invokes whole-file loader thunk `0x00401082` (`0x004AE240`) with the current
   arena cursor. It then calls `0x00444B70` at `0x00444D21`.
4. The same `0x00444C40` invocation passes the unchanged base path to
   `0x00448010` at `0x00444D69`. That function appends `.all` from
   `0x004DE028` and invokes the whole-file loader at `0x00448079`.
5. After the two immediate consumers populate shared tables, `0x00444C40`
   calls `0x00446970` at `0x00444E10`. This is a later convergence candidate,
   not a demonstrated complete ANM/ALL semantic boundary.

## Selected plant call sites

| Plant | Base-string VA | Resource ID | `0x00444C40` call site |
|---|---:|---:|---:|
| 04 | `0x004DDCE4` | `0x6B` | `0x0044575E` |
| 05 | `0x004DDCD0` | `0x6C` | `0x004457B5` |
| 06 | `0x004DDCBC` | `0x6D` | `0x0044580C` |
| 10 | `0x004DDC6C` | `0x71` | `0x00445968` |

The base strings are `plants\plant04`, `plants\plant05`,
`plants\plant06`, and `plants\plant10`. The extensions are appended by code;
there are not separate per-file full-path strings.

## Buffer and first-consumer boundaries

### `.ANM`

- If per-ID pointer table `0x005A9450` has no entry, `0x00444C40` supplies the
  current shared arena cursor to `0x004AE240`.
- The loader's returned byte count is rounded up to a 4-byte boundary and
  advances the cursor at `0x00444CDD–0x00444CF7`.
- The loaded pointer is stored in per-ID table `0x005B18E0`.
- `0x00444B70` is the first distinct consumer. It reads a signed count at
  file offset `+0x02`, relocates nonzero dword offsets beginning at `+0x08`
  in place, and performs a second bounded-by-file-fields walk from the first
  nonzero target.

| File | Bytes | `u16 +0x02` | Dword offsets from `+0x08` |
|---|---:|---:|---|
| `PLANT04.ANM` | 1,802 (`0x70A`) | 3 | `0x14`, `0x2AE`, `0x470` |
| `PLANT05.ANM` | 1,168 (`0x490`) | 4 | `0x18`, `0x16C`, `0x254`, `0x3A8` |
| `PLANT06.ANM` | 5,066 (`0x13CA`) | 3 | `0x14`, `0x6EE`, `0xC18` |
| `PLANT10.ANM` | 1,802 (`0x70A`) | 3 | `0x14`, `0x2AE`, `0x470` |

Every first-level offset is inside its exact file size. These observations are
enough to select `.ANM` for a later bounds-checked, multi-file inspection
packet, but not to name any field semantically.

### `.ALL`

- `0x00448010` supplies the current shared arena cursor to `0x004AE240` at
  `0x00448079`.
- The return byte count is not retained. The routine interprets the first
  dword as a doubled offset to another table, reads a count there, walks
  `0x4C`-byte entries, and advances the arena cursor using embedded dword
  lengths multiplied by two.
- Selected fields and data pointers are copied into the shared table rooted at
  `0x005A9660` with an observed `0x50`-byte stride.
- No destination capacity or file-size bound is passed to this parser path.
  `.ALL` therefore remains unsuitable for promoted tooling until independent
  bounds are established.

## Request origin and runtime correlation

`0x00416100` begins its output with literal plant ID 5, then derives additional
IDs from a 64-entry runtime table rooted at `0x0059B628` and a counted
16-byte-entry table reached through `0x005C595C`; it writes `-1` as a
terminator. The exact producer fields behind those two inputs remain unknown.

The unchanged hardware logs independently match the static pair order:

- Training: 05, 04, 10, 06;
- Level 01: 05, 07, 04, 10, 09, 03, 08, 02, 06.

For every listed plant, the `.anm` request immediately precedes `.all`, as the
single `0x00444C40` control path predicts. The logs prove requested paths and
order, not successful interpretation of every byte.

## Trace limits

- No M1 record, payload target, or file offset is yet connected to an ID
  consumed by `0x00416100`.
- Cache-table behavior exists, but the accepted retained controls begin after
  `0x004671D0` clears `0x005A9250` and `0x005A9450`, so both files are requested.
- The static routines do not receive an explicit arena capacity.
- ANM/ALL basename pairing and later convergence do not prove that either file
  is a complete model, animation, texture, or object resource.
