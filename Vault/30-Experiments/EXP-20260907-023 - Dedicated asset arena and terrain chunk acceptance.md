---
type: experiment
id: EXP-20260907-023
date: 2026-09-07
created: 2026-09-07
updated: 2026-10-29
status: bounded-runtime-accepted
environment: Wine Gamescope hardware Direct3D, Blender 5.2 Flatpak, offline Unicorn x86
question: Where does the native loader place retained level and model data, what bounds that region, and what minimal edit moves it away from renderer scratch?
result: The native load cursor starts at 0063E998 through exactly two HIGHLOW operands (004634EA, 004672E5) and the space up to engine global 0076F998 is 1249280 bytes; RAW staging still ends at 0076F998 and must not move. Repointing only the two operands to a dedicated region loads all 170 model entries identically in native replay and passes three live arms.
binary_sha256: 431ec953b67bd3233f8fa58e7a22edbfabaeb153e3ee322d760c45f2a44c7d8f
evidence: [EXP-20260907-017, EXP-20260907-019, EXP-20260907-022]
tags: [experiment, terrain/authoring, re/memory, re/rendering]
---

# Dedicated asset arena and terrain chunk acceptance

This experiment addresses the storage dependency that prevented EXP-022 terrain
chunks from passing live acceptance: retained level and model data reaching the
renderer scratch at 0076F9A0.

## Confirmed storage mechanism

Evidence below is under `work/experiments/EXP-20260907-023/` unless otherwise stated.
Static queries use the original PC export with [[Ghidra export structure and caveats]].
Disassembly and PE relocation inspection independently check its results.

- `arena-base-disassembly.txt` and `arena-interior-relocations.json` identify
  exactly two HIGHLOW operands containing 0063E998:004634EA and 004672E5.
  Instructions 004634E4 and 004672E4 initialize the native load cursor. The latter
  feeds stack-local cursor, 005C5964 and reset root 0076F9B0. Ghidra's additional
  propagated references are not additional encoded base operands.
- `loader.c/json`, `raw-loader.c/json`, `terrain-loader.c/json` and
  `character-loader.c/json` show downstream RAW→DAT→terrain→model loading using
  those cursors. RAW file staging still ends at 0076F998; that address is also
  used by scalar engine state. It must not be indiscriminately relocated.
- `load-layout.json` reconstructs EXP-019's retained layout from the observed
  DAT/model roots and original loader rules: 48927 RAW bytes, 593276 DAT bytes,
  367744 TERRAIN bytes, 16692 PLANTTER bytes, and 380232 model/animation bytes.
  Retained data ends at 0079612F, 157591 bytes beyond the next known engine global
  at 0076F998. The space from 0063E998 to that global is 1249280 bytes. This is not
  a measurement of all game RAM or the host's capacity.
- The EXP-022 restored capture's reset root 0076F9B0 is already corrupted to
  EB774000. This supplies another affected occupant besides the confirmed
  MOS.ALL stream and renderer scratch. It does not prove EXP-020's exit cause.

## Minimal relocation proof

A test executable adds a zero-filled read/write, non-executable PE section at
RVA 0047B000, preferred VA 0087B000, capacity 8388608 bytes, and edits only the
two native base operands and required PE header fields. Both existing HIGHLOW
relocations remain intact; file size is unchanged; original RAW staging and
renderer globals stay at their original addresses. The native loader constructs
its own dependent pointers. The edit is checked against critical native
code-window hashes, the original base operands and the complete matching
base-relocation set, and has an exact inverse.

`native-initializer-check.json` executes both initializers at preferred image
base 00400000 and a relocated 10400000 base. Both native cursor roots and the
stack cursor acquire the new section address.

`native-model-load.py` executes the complete original 00445020 model loader.
Only local file reads at 004AE240 and log formatting at 004ADEA0 are substituted.
`model-load-comparison.json` compares all 35 file loads and 170 final shared entries
at old and new addresses; every entry payload matches the native control.
157 match source bytes directly; 13 undergo native preprocessing. The first
strict raw-source assertion rejected entry 21 and was replaced with the paired
native-output comparison, not an exemption from comparison. Two further rejected
checks are retained: a captured gameplay state changes plant load ordering, and
a replay using a new-region pointer with its region omitted temporarily produced
137 entries.

Three live arms used the derived executable in frontmatter with fresh cold
prefixes; all six hardware markers and guarded resident checks pass, with no
live memory write, debugger stop, breakpoint or ptrace:

| Arm | Assets | Result |
| --- | --- | --- |
| preview-01 | Exact 721 EXP-019 stage files; EXE storage change only | 195 repeated checks of all 170 models, 77 distinct Flik pose tables; normal Up and jump input; resident geometry checks pass. |
| preview-02 | Four EXP-022 chunks plus 2097152 inert DAT tail bytes | 3094194 combined DAT/TERRAIN/PLANTTER bytes; 244 complete model checks, 220 distinct pose tables, movement/jump and all four resident chunks pass. |
| preview-03 | Four-chunk build without padding | All four resident chunks pass; 612 complete model checks over 50 seconds, 283 distinct pose tables. |

The large arm's retained region uses 3505561 bytes, with native peak 3506097
including the last file directory (`large-load-budget.json`). This is a storage
stress fixture with unchanged geometry, not a denser-map performance benchmark.
In preview-03, sampled contacts visit all four terrain descriptors 99/178/179/180
with maximum sampled floor gap 117 world units; its traversal inputs overlapped
with user control, so route results are shared-control observations, not
deterministic automated route acceptance.

The reproduced model/scratch overlap is absent in these builds. The region is
finite; no streaming or all-level compatibility claim is made. Measured
rendering/collision costs, denser geometry, wider coordinates and sustained
actor/transition coverage remain open.

Tracked evidence index: `reports/terrain/EXP-20260907-023.json`. Game assets,
captures and derived binaries remain private under work/. No PS1 evidence used.
