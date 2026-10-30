---
type: reference
status: active
created: 2026-08-17
updated: 2026-08-17
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
evidence:
  - EXP-20260811-002
tags:
  - re/static
  - reference
  - implementation/tooling
---

# Ghidra export structure and caveats

How `static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json` is actually
shaped, and the five ways a naive reading of it gives a wrong answer.

Produced by `scripts/ghidra/ExportEvidence.java` via
`scripts/ghidra-export.sh`. Generated once on 2026-08-11 and not regenerated
since. Query it with `scripts/ghidra-query.py` rather than by loading it into
a session: it is 7.7 MB on a single line.

## Shape

`{program, functions[1218], strings[1922], imports[0]}`. Each function record
carries `address` (bare 8-hex, no `0x`), `name`, `prototype`, `callers[]`,
`callees[]`, `data_references[]`, and `decompiler` (full pseudocode text).
Image base `0x00400000`.

All counts below were re-derived directly from the file on 2026-08-17 and are
reproducible with `scripts/ghidra-query.py stats`.

## Confirmed caveats

### 1. `imports` is empty

The array is literally `[]`, although the binary imports DDRAW, DINPUT,
DSOUND, GDI32, KERNEL32, OLE32, USER32, and WINMM (see
`reports/ghidra/BIN-97c95ba5572dce63-baseline.md`). The exporter's
external-function pass produced nothing.

Import evidence must therefore come from `static/pe/…/rabin2-imports.json` or
the authored `static/imports/…/import-categories.md`, never from this file.
Imported calls do appear in the graph as **191 `EXTERNAL:<ordinal>` callee
edges (114 distinct)**, which cannot be resolved to API names from this export
alone.

### 2. `callers` holds call-site addresses, not function entries

**4,464 of 4,468** caller references are not the entry address of any
function: they are the addresses of the calling instructions. Treating a
`callers` entry as a function identity is wrong in 99.9% of cases. The owning
function must be resolved by finding the nearest preceding entry, which is an
inference and is labelled as one by `ghidra-query.py callers` (`exact: false`,
cross-checked against the owner's `callees`, 98.5% corroborated).

### 3. The call graph breaks at thunks

There are **486 thunk functions and every one has an empty `callees` array**.
Because callers reach a function through its thunk, a real function can appear
to be called by nobody.

Concretely: `FUN_00432930` — the type-1 reset-placement selector reimplemented
as M5's first admitted module ([[EXP-20260816-153 - M5 entry gate and type-1 reset placement resolver]])
— has **zero** entries in `callers`, while `thunk_FUN_00432930` has one. An
agent asking this export who calls the reset selector gets "nobody", which is
false.

`ghidra-query.py` bridges this by name (`thunk_FUN_<addr>` → `<addr>`) and
labels the edge `thunk_name_bridge` so the inference is never merged with
structured evidence.

### 4. Thunk bodies duplicate their targets

**1,812,088 of 4,663,040 decompiler bytes (38.9%)** are thunk copies of code
that also appears under the real function. A textual search of the decompiler
therefore reports many findings twice, and a "second site" may be the same
code seen through its thunk.

### 5. Names are not unique, and `data_references` operands are not all addresses

One name, `thunk_FUN_0041a1d0`, is carried by three distinct functions;
lookup by name must refuse rather than pick. Some `data_references` operands
are stack forms such as `Stack[-0x…]` rather than addresses.

## Consequence for evidence discipline

This export is a **search surface, not an authority**. A structural claim
taken from it — who calls what, whether something is referenced, how many
sites exist — needs confirmation against `static/pe/…/objdump.txt` or a fresh
disassembly, because of caveats 2, 3, and 4 specifically.

[[Current State Archive]] records at least four audit rounds spent
re-discovering content this file already held, and one counter-correction
establishing that it "mentions every **principal** address, not every
address". Both failure directions — under-crediting and over-crediting — come
from the same cause: it was too large to read and had no query surface.

## Regeneration is cheap

`reports/ghidra/BIN-97c95ba5572dce63-import.log` records full import plus
auto-analysis at **41 seconds** (32.3 s of that in Decompiler Switch
Analysis), and the `-noanalysis` export pass completes in about a second. The
empty `imports` array is therefore a cheap fix in `ExportEvidence.java`
followed by a re-export, not an expensive one. That work is not done here and
no claim in this note depends on it.

## Related

- [[Agent evidence and query tooling]] — `scripts/ghidra-query.py`
- [[Functions MOC]] — the authored function dossiers
- [[Evidence Standard]]
