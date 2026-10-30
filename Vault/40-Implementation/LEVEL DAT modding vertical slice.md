---
type: implementation
status: active
created: 2026-08-12
updated: 2026-08-14
tags:
  - implementation/modding
---

# LEVEL DAT modding vertical slice

The first independent implementation is in `reimplementation/ablpc/` with CLI wrapper `scripts/ablpc-mod`.

## Supported now

- inspect the bounded [[PC LEVEL DAT prefix]];
- scan all `LEVEL*.DAT` files below a work tree;
- build a sparse overlay from a JSON manifest;
- copy a base work tree and apply the manifest;
- verify exact source SHA-256 and emit an output receipt;
- edit only a selected primary/secondary record's three candidate-center
  fields through the historical `set-scene-record-position` operation;
- guard and edit the signed word at scene-record `+0x0C` without assigning
  unsupported negative-value semantics;
- inspect positive-count payload-target blocks and scan the bounded masked
  dispatch-`0x49` class across a local corpus;
- rebind a dispatch-`0x49` record only when the source hash, expected old
  target, old block, and new positive-count block all validate.

## Safety boundary

Inputs remain unchanged. Output roots under `originals` or `media` and unsafe relative paths are rejected. Unknown suffix bytes and unknown record fields are preserved verbatim. The manifest schema is deliberately narrow and versioned. It does not allow arbitrary byte patches, negative-count target editing, or payload-target editing for dispatches other than the PC-native `0x49` path bounded in `EXP-20260812-009`.

## Current example

`mods/training-central-flower-cluster-candidate-far.json` changes three first
candidate-center components in the Training DAT. `EXP-20260812-006` confirmed
a joint visible effect. The three
`mods/training-primary-record-{124,125,126}-candidate-far.json` manifests then
isolate those edits under the hardware renderer. `EXP-20260812-008` confirms
that each record controls a distinct visible plant element in the tested
starting camera; `EXP-20260812-011` establishes that the large edit removes
them through visibility selection rather than render translation.

## Guarded target rebind

`mods/training-primary-record-124-target-111e4.json` and
`mods/training-primary-record-125-target-1319c.json` stage reciprocal guarded
rebinds. Synthetic/local staging proves field locality, and
`EXP-20260812-010` confirms both candidates under the original executable's
hardware Direct3D path. Each phase-matched visual difference is confined to
the selected placement region. Target rebinding is therefore a demonstrated
mod operation for the exact Training hash and bounded positive dispatch class;
negative-count targets, other dispatches, and complete object-definition
semantics remain unsupported.

## Candidate center and visibility bound

`mods/training-primary-record-126-field-{04,08}-plus-512.json` isolate two
center components. `EXP-20260812-011` accepts both without visible movement
and records the static switch to payload placement. The offset-named
`set-scene-record-field-0c` operation requires an expected signed value;
`mods/training-primary-record-125-field-0c-zero.json` demonstrates the positive
visibility-bound role in `EXP-20260812-012`. Negative values remain
unsupported semantically even though the operation preserves their signed
representation.

## Cross-file acceptance

`mods/level01-primary-record-261-candidate-far.json` and
`mods/level01-primary-record-261-target-3459c.json` extend exact-hash staging
and original-executable acceptance to `CD/LEVEL01/LEVEL.DAT` in
`EXP-20260812-013`. Both retain exact control frames at the tested starting
camera; the evidence supports safe cross-file editing, not a visible Level 01
placement assignment.

## M1 tooling promotion

[[M1 Tool Support Matrix]] is the canonical support/rejection boundary. The
M1.5 audit filters payload inspection to the demonstrated masked dispatch class,
rejects unknown manifest-root fields and duplicate Windows targets, adds
synthetic regression coverage, and documents the no-game-bytes authoring flow
in `reimplementation/README.md`. Training and Level 01 recipes reproduce their
accepted bytes without another runtime rerun, so M1 is complete.

## M3 exact Training collectible recipe

[[Training 51-grain vertical slice]] is a separate exact-hash operation over
the first type-`0x3F` table. It inserts one selector-`0x14` record, relocates
the remainder of the file according to the PC loader's known fixups, and
requires byte-exact inverse reconstruction. `EXP-20260814-111` confirms normal
Direct3D initialization and an isolated pickup of the inserted record.

This does not widen the M1 scene-record manifest grammar or claim a general
type-`0x3F` editor. The distinct executable counter cap at 50 also prevents a
claim that the HUD/current count reaches 51.
