---
type: session
date: 2026-08-21
agent: Codex
topic: P0A offline postmortem and consumed-wrapper retirement
status: complete-offline
tags:
  - session
  - reverse-engineering
  - level01
  - terrain
---

# 2026-08-21 0430 - Codex - P0A offline postmortem hardening

## Outcome

Continued entirely offline after P0A-AH-001's pre-collection failure. No game
launch, input, close retry, signal, process-memory access, save-state action,
or `R:` change occurred. The then-recorded seven-process census and private
sink, pending evidence, stage, and mapping were not controlled or changed.

The consumed argument-free wrapper now refuses reuse and no P0B identity or
successor arm exists. Session-audit receipts retain stdout and stderr
separately, hash each independently, and parse only stdout. Runtime provenance
records both X sockets' actual common `gamescope-wl` peer through a minimal
exact `/proc/stat` + cmdline identity and exact owned command. The display is
independently tied to one exact Xwayland launch-stderr marker. The isolated
native fixture confirms the Gamescope peer; focused lifecycle/analyzer/packet/
native-X tests pass 215/215 and the full gate passes 1859/1859 with zero
tracked-file violations.

Static postmortem work also rejects a timing-only level-route patch. On the
Level Select path, retail `0x0043DB83` resets `word [0x00599AF8]` to zero.
Candidate selector `0x00443B40` tests the live Right bit at `0x00443F54`,
increments its local position at `0x00443FB3` without a previous-state edge
test, and writes the selected position at `0x004444D6`. Ghidra and a fresh
bounded retail disassembly agree. The retained 180 ms hold followed by
level07/progression position 10 is consistent with repeated held-state polls,
but does not prove their count or cadence. Known approximately 12 ms dropped
taps make an unverified shorter hold unsafe as a deterministic repair.

The user reports that save states do not currently work. This was not
independently exercised and is recorded as an operational constraint, not
runtime evidence; no save-state route is used.

James rejected first immutable postmortem candidate `932627d` / `4742aa21`.
Strict schemas had admitted JSON booleans as numeric identities, the two socket
receipts were not bound by their complete UID/GID credentials, and peer
chronology plus launcher/game/peer identity collisions were unchecked. The
correction applies exact positive/nonnegative integer domains throughout,
requires one complete peer tuple and distinct chronological identities, and
prevents enumeration drift from masking invalid sample timing. Focused tests
pass 269/269 plus native X (270 total); the full gate passes 1914/1914 with zero
tracked-file violations. Collector/validator SHA-256 is
`71f9099aa2040e8cb141523f9114d38f9b972622b37dc935f513213995d528bd`.

A read-only audit at `2026-08-21T05:35:13-04:00` records no open managed
session, three unattributed helpers (Gamescope, gamescopereaper, winedevice),
and the private sink. Launcher shell `1834769` remains; the game and Xwayland
PIDs are absent. This is a current-state observation without a causal claim;
no process was controlled, closed, signaled, or read through process-memory.

James then rejected exact candidate `740cb07` / `56818bd1`. Float aliases still
passed equality-only numeric fields, owned polls were ignored, direct drift
masked structural sample defects, direct metadata-error partitions were
weaker than packet validation, and missing runtime PID escaped as `KeyError`.
The correction gives both paths one sorted/unique task and error-partition gate,
checks every named numeric alias exactly, and makes malformed metadata/runtime
schemas fail as evidence errors. It passes 297/297 non-native focused tests,
native X (298 total), and 1942/1942 full tests with zero tracked-file
violations. Current collector/validator SHA-256 is
`415fe20a699a3491735c9cbbb8f169da65ee067ef842811125964dc098085e4e`.

## Boundary

P0A-AH-001 remains consumed and pending with zero lifecycle samples. At this
checkpoint the established direct focused `xdotool` route had been overlooked;
the later operational correction is recorded in
[[2026-08-21 0823 - Codex - PC Level01 route reconfirmation and P0B pickup]]. A
passive successor still needs new frozen identities, fresh explicit
authorization, and a new James verdict. This work supplies no
lifecycle, collision, terrain, material, visibility, causality, or retail-
behavior conclusion and authorizes no recovery or retry.

## Links

- [[EXP-20260820-005 - R2p task lifecycle diagnostic]]
- [[PC level roster and numbering]]
- [[Known Unknowns#KU-074 - Live semantics of the level-select carousel position counter|KU-074]]
- [[Decision Log#DEC-189 - Retire the consumed P0A wrapper and correct offline runtime provenance|DEC-189]]
- [[Decision Log#DEC-190 - Require exact integer domains and complete X peer credentials|DEC-190]]
- [[Decision Log#DEC-191 - Share exact task partitions and reject numeric aliases|DEC-191]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
