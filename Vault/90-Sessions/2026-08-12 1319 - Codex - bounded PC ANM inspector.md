---
type: session
date: 2026-08-12
agent: Codex
status: completed
tags:
  - session
  - re/resources
  - re/static
  - re/file-format
  - implementation/parser
---

# Bounded PC ANM inspector

## Agent

Codex

## Goal

Complete roadmap M2.4 by mapping the complete first-level `.ANM` walk at
`0x00444B70`, implementing a lossless bounds-checked inspector, testing
synthetic invalid inputs, and validating multiple exact PC files.

## Files and evidence inspected

- Canonical startup, folder, evidence, naming, roadmap, and implementation
  policies under `Vault/00-System/` and the root/reimplementation READMEs
- Exact-hash PC executable, Ghidra export, and GNU objdump instructions for
  `0x00444B70`, caller `0x00444C40`, loader call `0x00444CD8`, and consumer
  call `0x00444D21`
- Exact user-owned work-copy `CD/PLANTS/*.ANM` files
- Prior resource evidence `EXP-20260812-015` through `EXP-20260812-017`

No runtime was launched or modified. No file under `originals/` was modified.
No PS1 source or findings were consulted.

## Folder placement followed

- Independent parser: `reimplementation/ablpc/anm.py`
- Synthetic regressions: `tests/test_anm.py`
- Exact-address trace: `static/exports/BIN-97c95ba5572dce63/`
- Metadata-only corpus result: `reports/resources/`
- Durable format/function/implementation/experiment findings: `Vault/`

No game-file payload bytes were added to tracked paths.

## Changes made

- Added immutable `AnmFile`, offset/reference dataclasses, and explicit checked
  reads for the bounded first-consumer layout.
- Added `ablpc-mod inspect-anm` and `scan-anm` metadata-only commands.
- Added 16 synthetic ANM tests covering losslessness and invalid boundaries.
- Added `EXP-20260812-017`, [[PC ANM first-level]],
  [[FUNC-97C95BA5572D-00444B70]], [[PC ANM inspector]], and the metadata report.
- Closed M2.4 and framed a same-layout plant 04/10 whole-file substitution as
  M2.5 without exposing an editor.

## Conclusions

- **Confirmed:** `0x00444B70` relocates nonzero first-level offsets, retains
  the first nonzero reference, bounds a signed-word list from its unsigned
  count, and distinguishes `-2`.
- **Confirmed:** the caller patches header words `+0x00` and `+0x04` before the
  consumer, so their on-disk zeros are not runtime constants.
- **Confirmed:** all 11 PC plant `.ANM` files pass the independent inspector;
  the selected four reproduce their prior offsets exactly.
- **Confirmed:** the parser preserves complete input bytes and exposes no
  writer or payload bytes in output.
- **Unknown:** nested semantics, `.ANM` visible role, pair requirements with
  `.ALL`, and the direct M1 placement-resource bridge.

## Contradictions and negative results

- Relocating every nonzero top offset does not mean this function parses every
  referenced record; it follows only the first nonzero reference.
- The original routine's lack of a byte-size argument is not reproduced as
  permissive behavior; the independent inspector rejects unsafe bounds.
- No semantic editor was justified by the bounded layout.

## Tests and checks

- Focused ANM suite: 16 passed.
- Exact PC plant corpus: 11 scanned, zero failures.
- Complete `make check`: 38 tests, Vault lint clean, tracked-file audit clean.
- Git diff and final status checks are recorded in the handoff.

## Recommended next action

Execute [[Project Roadmap#M2.5 — Same-layout ANM replacement validation]] with
separate ignored control/replacement trees and exact hardware-renderer log
gates. Leave `.ALL` unchanged and do not commit game bytes.

## Git commit if applicable

Bounded commit message: `feat: add bounded PC ANM inspector`.
