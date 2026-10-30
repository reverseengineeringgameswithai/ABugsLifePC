---
type: implementation
status: active
created: 2026-08-14
updated: 2026-08-14
tags:
  - implementation/modding
  - milestone/m3
  - gameplay/collectibles
---

# Training FLIK letter transformations

## Outcome

[[EXP-20260814-113 - Training FLIK letter transformations]] accepts one exact
PC Training demo that duplicates the four existing letter selectors at moved
positions. All four copies initialize and collect independently; the same
implementation surface also supports exact move and remove transformations.

## Asset-free implementation

- `reimplementation/ablpc/training_letter_mod.py` contains the exact recipe
  and its public hash-locked `transform_training_letter_records` primitive.
- `scripts/make-training-duplicate-flik` is the work-copy-only CLI.
- `tests/test_training_letter_mod.py` covers positive/negative table growth,
  move, duplicate, remove, unknown-byte preservation, relocation, inverse,
  and refusal using an independently created synthetic DAT.

The public recipe accepts only Training DAT SHA-256
`20d0f9b143a4fceeb058d5ce81680b3e6317995abc3d5ac4103fc85e79b5fd40`.
It copies selectors `0x10`–`0x13` to `(4900,-50,1500)`,
`(5100,-50,1000)`, `(5000,-50,500)`, and `(4900,-50,0)`, changes type-`0x3F`
count 63 to 67, relocates exactly 556 fields, checks two of every letter
selector plus 51 grains, and requires a byte-exact inverse. Output identity is
`e9c75bb24ae0d0f4f74d17ea63431195e49b7e5278c089588d9372b8eb8cae7a`.

## Usage

```bash
./scripts/make-training-duplicate-flik \
  work/copies/training-51/PC/BUGS/CD/LEVEL07/LEVEL1.DAT \
  work/copies/training-duplicate-flik-LEVEL1.DAT
```

Stage the generated DAT into a fresh complete ignored `DRIVE:\PC\BUGS` tree.
Do not distribute the generated DAT or source content.

## Behavioral boundary

The four selectors feed one persistent bit mask. A duplicate collected after
mask `0x0F` retriggers the existing completion/reward path: runtime changes
byte `0x0059D9B0` from 1 to 2. The data-only recipe intentionally reports that
behavior rather than patching it. A one-shot or redesigned reward requires a
separate executable modification and acceptance packet.

This module is an exact M3 recipe, not a general type-`0x3F` manifest grammar
and not a change to completed M4/M6 compatibility authorities.
