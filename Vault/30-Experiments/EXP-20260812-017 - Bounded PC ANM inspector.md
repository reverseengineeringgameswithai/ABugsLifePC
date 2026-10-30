---
type: experiment
id: EXP-20260812-017
date: 2026-08-12
question: What exact first-level PC ANM layout does 0x00444B70 consume, and can an independent inspector reproduce it safely across multiple files?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora static analysis and offline work-copy corpus validation
environment_version: GNU objdump 2.44; Ghidra baseline export; Python 3.14.6; pytest 9.1.1
working_directory: /home/dev/ABLPC
configuration: Read-only parser against exact PC plant ANM files with synthetic invalid fixtures
artifacts:
  - static/exports/BIN-97c95ba5572dce63/M2-anm-first-level-static-trace.md
  - reports/resources/pc-plant-anm-first-level.md
  - reimplementation/ablpc/anm.py
  - tests/test_anm.py
addresses:
  - 0x00444B70
  - 0x00444C40
  - 0x00444CD8
  - 0x00444D21
file_offsets:
  - 0x00
  - 0x02
  - 0x04
  - 0x06
  - 0x08
  - 0x0C
result: bounded-read-only-anm-inspector-validates-eleven-files
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/static
  - re/resources
  - re/file-format
  - implementation/parser
---

# EXP-20260812-017 - Bounded PC ANM inspector

## Question

What exact first-level PC `.ANM` layout does `0x00444B70` consume, and can an
independent inspector reproduce it safely across multiple files?

## Inputs and procedure

- Exact executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Disassembled the complete `0x00444B70` body and its caller around
  `0x00444CD8–0x00444D21` with GNU objdump; checked the existing Ghidra export
  without treating pseudocode as source.
- Compared the four M2-selected PC files `PLANT04.ANM`, `PLANT05.ANM`,
  `PLANT06.ANM`, and `PLANT10.ANM`, then scanned all 11 exact files under the
  user-owned derived `CD/PLANTS` work copy.
- Implemented an independent parser under `reimplementation/ablpc/`, synthetic
  tests under `tests/`, exact-address evidence under `static/exports/`, and a
  metadata-only corpus report under `reports/resources/`.
- Ran `inspect-anm`, `scan-anm`, the focused synthetic tests, and `make check`.

No runtime was launched or modified. No PS1 source or findings were consulted.

## Expected discriminator

- If the inferred header/offset walk is correct, all four selected files should
  pass exact-size checks and report the offsets previously read manually.
- Contradictory counts, zero entries, nested bounds, or selected-record behavior
  must remain visible rather than normalized.
- Synthetic truncation, impossible counts, and out-of-range offsets must fail
  closed without reading past the supplied byte string.

## Static result

`0x00444B70` reads a signed count at `+0x02`, relocates nonzero dwords beginning
at `+0x08`, and retains the first nonzero pointer. With its nonzero caller flag,
it reads an unsigned nested count at first-record `+0x08`, treats signed words
from `+0x0C` as a list, and distinguishes `-2`.

The whole-file loader size controls caller arena advancement but is not passed
to this consumer. The independent parser therefore adds exact byte bounds that
the original routine cannot enforce at this boundary.

The caller also overwrites in-memory header words `+0x00` and `+0x04` before
the consumer. All checked PC files contain zero there on disk, so those runtime
values are not promoted to file constants.

## Selected-file result

| File | SHA-256 prefix | Size | Count | Offsets | First nested count |
|---|---|---:|---:|---|---:|
| `PLANT04.ANM` | `32dce9588272` | `0x70A` | 3 | `0x14, 0x2AE, 0x470` | 2 |
| `PLANT05.ANM` | `d474fe3c374c` | `0x490` | 4 | `0x18, 0x16C, 0x254, 0x3A8` | 1 |
| `PLANT06.ANM` | `d90a35b047c4` | `0x13CA` | 3 | `0x14, 0x6EE, 0xC18` | 6 |
| `PLANT10.ANM` | `12d2550ea89b` | `0x70A` | 3 | `0x14, 0x2AE, 0x470` | 2 |

All four pass and exactly reproduce the M2.2 first-level observations.

## Corpus result

`scan-anm` accepts all 11 PC plant `.ANM` files with zero failures. All have
zero on disk at header words `+0x00`, `+0x04`, and `+0x06`; counts are 3 or 4;
all offsets are nonzero, even, strictly increasing, and in range; and every
first offset equals its offset-table end. First nested counts range from 1 to
7. `PLANT03.ANM` alone has a `-2` in the inspected list, at index 6.

These last properties are corpus observations, not required parser rules.

## Parser and tests

`AnmFile` preserves the exact source bytes and exposes no writer. It rejects:

- truncated 8-byte headers;
- negative or table-impossible first-level counts;
- nonzero offsets outside the exact file;
- a truncated 12-byte first referenced record header;
- an item count whose signed-word list exceeds exact file size.

Sixteen ANM tests also cover zero offsets, exact byte preservation,
metadata-only JSON, case-insensitive extension scanning, and per-file failure
reporting. The complete suite passes 38 tests. The tracked-file audit reports
zero protected artifacts.

## Confirmed

- The offset/count widths, locations, relocation behavior, first-reference
  selection, nested list bounds, and `-2` comparison listed above are exact PC
  consumer behavior.
- The independent inspector reproduces that bounded layout for the four
  selected files and all 11 local plant `.ANM` files.
- Inspector output contains metadata only and the implementation preserves the
  complete unknown byte string unchanged.

## Inferred

- `0x00444B70` is a first-level `.ANM` relocator/setup routine, based on its
  exact `.anm` caller path and in-place offset conversion.
- Matching first-level layouts for plants 04 and 10 make them a useful
  same-layout replacement discriminator; no semantic interchangeability is
  claimed.

## Unknown and limitations

- Complete `.ANM` structure and every semantic field.
- Referenced-record layouts after the first nonzero entry.
- Whether `.ANM` alone controls visible geometry, animation, or another
  behavior; its paired `.ALL` remains unchanged and unparsed.
- Original behavior for malformed data. Safe-parser rejection is not asserted
  to reproduce an original error path.
- The M1 placement-record-to-resource identity remains open under `KU-023`.

## Contradictions and negative results

- The on-disk header zeros do not describe consumer-time fields `+0x00` and
  `+0x04`; the caller patches them first.
- Multiple first-level references are relocated, but only the first nonzero
  referenced record is inspected further by this function.
- No editor is exposed because no nested semantic field is demonstrated.

## Result and follow-up

M2.4 is complete at a read-only boundary. M2.5 should use a staged,
hash-guarded whole-file substitution between same-size/same-first-level-layout
plants 04 and 10, keep the paired `.ALL` unchanged, and compare an unchanged
hardware-renderer control. That experiment tests `.ANM` contribution without
inventing a field edit or distributing game bytes.
