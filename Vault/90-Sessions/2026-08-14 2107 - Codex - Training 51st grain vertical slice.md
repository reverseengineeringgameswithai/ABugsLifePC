---
type: session
date: 2026-08-14
agent: Codex
status: completed
tags:
  - session
  - milestone/m3
  - gameplay/collectibles
---

# Training 51st grain vertical slice

## Agent

Codex

## Goal

Add one collectible grain to PC Training for a total of 51, investigate the
user-reported black-panel regression, preserve evidence discipline/Obsidian,
leave no stale runtime/agent instances, and return Git to a clean committed
state.

## Files inspected

- exact PC `bugs.exe` and Training `CD/LEVEL07/LEVEL1.DAT` work copies
- Ghidra export plus PC disassembly at `0x00417720`, `0x00439E90`,
  `0x0044BB70`, and `0x00456A90`
- complete/standalone candidate logs, screenshots, and live table dump under
  ignored `work/copies/M3-training-51-grains-full-disc/evidence/`
- committed PS1 blobs at external commit
  `1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51`
- required START HERE chain, cross-port policy, relevant MOCs, roadmap, and
  existing LEVEL DAT implementation/file-format notes

## Experiments inspected

- `EXP-20260812-006`, `EXP-20260812-016`, and `EXP-20260812-020`
- [[EXP-20260814-111 - Training 51st grain collectible vertical slice]]

## Changes made

- Added exact-hash `training_grain_mod.py`, CLI wrapper, and three synthetic
  regression tests.
- Built the ignored 115,076-byte output with 51 selector-`0x14` records.
- Added PC static, runtime, function, file-format, implementation, cross-port,
  roadmap, current-state, decision, unknown, MOC, and user-facing evidence.
- Added the required runtime/worker instance lifecycle policy to the START HERE
  chain.
- Closed eight stale owned Gamescope/reaper pairs, their private sinks, and
  obsolete M6 verifier agents; final scoped audit was empty.

## Conclusions

- **Confirmed:** the exact Training source has 50 selector-`0x14` records;
  selector `0x14` follows the PC grain pickup/counter path.
- **Confirmed:** entry 62 at `(4950,-1301,1127)` initializes and can be the
  only adjacent record consumed while the counter increments `0 -> 1`.
- **Confirmed:** the output has 51 collectible records and reconstructs its
  exact source through the inverse transformation.
- **Confirmed:** the black-panel screenshot was caused by a standalone launch
  missing the required complete `DRIVE:\PC\BUGS` shape, not by the DAT bytes.
- **Unknown:** the retained/HUD counter reaching 51. A PC function clamps the
  counter to 50 and another exact-50 event exists.

## New hypotheses

The smallest follow-up, only if the user requires a visible or completion-
relevant total of 51, is to discriminate the `0x00417720` exact-50 event from
the `0x00439E90` clamp with a controlled 50-to-51 pickup.

## Contradictions discovered

- A visually corrupt menu initially suggested DAT relocation damage. The
  failing log instead recorded missing absolute level-select data; complete-
  tree mapped-drive staging removed the corruption with the same DAT.
- Fifty-one collectible records do not imply a current/HUD value of 51 because
  executable logic clamps the counter at 50. This remains `KU-054` rather than
  being silently folded into the completed record-total claim.

## Tests run

- `PYTHONPATH=reimplementation pytest -q tests/test_training_grain_mod.py`
  — 3 passed.
- exact CLI rebuild and `cmp` against the accepted candidate — passed.
- Python compilation for the module, CLI, and test — passed.
- `make check` — Python doctor passed; Vault 321 notes/0 errors/0 warnings;
  M4 compatibility five anchors valid; 512 tests passed; tracked audit 0;
  diff and staged-diff checks passed.

## Unresolved questions

- `KU-054`: exact-50 event, clamp, HUD, and completion behavior after a 51st
  sequential pickup.
- M3's remaining actor, collision, trigger, camera, progression, and additional
  independent-modification exit gates.

## Recommended next action

If the user wants a displayed 51, execute only the `KU-054` trace/50-to-51
discriminator. Otherwise select the next concrete gameplay edit and its
smallest M3 packet. Do not reopen M2 without new evidence for its separate
causal gate.

## Later correction

[[EXP-20260814-112 - Training 51 counter and tally boundary]] completed this
recommended discriminator. The counter retains 51, the unmodified HUD displays
51, and an exact three-byte end-tally patch preserves the original 50-grain
completion/emblem path while rendering `51/50`. The static cap in
`0x00439E90` was not reached in the controlled Training window, so this
session's Training-specific clamp attribution is withdrawn; the cap's broader
identity remains unknown.

## Git commit if applicable

Committed as one bounded Training-51/M3.1 packet after final review; see the
repository history adjacent to this session note.
