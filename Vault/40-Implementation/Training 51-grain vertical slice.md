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

# Training 51-grain vertical slice

## Outcome

[[EXP-20260814-111 - Training 51st grain collectible vertical slice]] accepts
one exact PC Training recipe that raises the type-`0x3F` selector-`0x14` census
from 50 to 51 and proves the new record itself is collectible.
[[EXP-20260814-112 - Training 51 counter and tally boundary]] then proves that
the pickup counter and in-level HUD naturally retain/display 51 and accepts a
separate exact three-byte executable patch for the end tally.

## Asset-free implementation

- `reimplementation/ablpc/training_grain_mod.py` contains the exact-hash recipe.
- `scripts/make-training-51-grains` is the CLI entry point.
- `tests/test_training_grain_mod.py` covers the transformation using an
  independently created synthetic fixture.
- `reimplementation/ablpc/training_grain_counter_mod.py` contains the exact
  retail-executable three-byte tally recipe.
- `scripts/make-training-51-counter-cap` is its work-copy-only CLI.
- `tests/test_training_grain_counter_mod.py` covers exact byte preservation,
  inversion, overlap, and wrong-source rejection without game bytes.

The recipe is locked to source SHA-256
`494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`.
It inserts entry 62 at original offset `0x3E8`, position
`(4950,-1301,1127)`, selector `0x14`; changes table count 62 to 63; relocates
exactly 556 known file-relative fields; reparses; checks 51 selectors; and
requires a byte-exact inverse. The output identity is
`20d0f9b143a4fceeb058d5ce81680b3e6317995abc3d5ac4103fc85e79b5fd40`.

The executable recipe changes file offsets `0x422CB`, `0x422CF`, and
`0x42327`, corresponding to virtual addresses `0x00442ECB`, `0x00442ECF`,
and `0x00442F27`. It raises the end-tally retention cap from 50 to 51 and
changes the completion branch from exactly 50 to unsigned at least 50. The
output is 1,069,056 bytes at SHA-256
`8ececefbe1e5747322bd635830f4125500c087d3769094b79545bd7a7b6a4456`,
and its exact inverse reconstructs the retail executable.

## Staging contract

Build a new output from a user-owned work copy:

```bash
./scripts/make-training-51-grains \
  work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL07/LEVEL1.DAT \
  work/copies/training-51-LEVEL1.DAT

./scripts/make-training-51-counter-cap \
  work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe \
  work/copies/training-51-bugs.exe
```

Copy the complete base tree to a fresh ignored location and replace
`PC/BUGS/CD/LEVEL07/LEVEL1.DAT` and `PC/BUGS/bugs.exe` there. The launch root
must retain the complete `DRIVE:\PC\BUGS` shape. A standalone
DAT/game-directory staging tree is not sufficient: the level selector loads
shared absolute paths such as
`\PC\BUGS\CD\LEVEL00\LEVEL.RAW` and will render corrupt black panels when
that drive shape is absent.

## Safety and compatibility boundary

- Never point output at `originals/` or distribute the generated DAT/tree.
- The CLI refuses source/output identity, existing output, wrong input hash,
  wrong selector census, wrong relocation census, wrong output identity, and
  failed reparse/inverse.
- This is a dedicated exact M3 recipe, not a new generic type-`0x3F` manifest
  operation and not a change to accepted M4 or M6 compatibility authorities.
- The accepted behavior is intentionally `51/50`: the extra grain is a bonus,
  while the original exact-50 pickup event, `/50` goal denominator, and bright
  completion/emblem path remain intact. Changing the emblem art or redefining
  the goal is outside this recipe.
