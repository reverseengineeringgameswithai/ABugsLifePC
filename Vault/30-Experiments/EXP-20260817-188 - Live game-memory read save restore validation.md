---
type: experiment
id: EXP-20260817-188
date: 2026-08-17
question: Do game-memory's read, save, and restore verbs work against the running retail PC game, not only the synthetic fixture?
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44, Wine 11 (wow64), Gamescope; the running EXP-20260817-187 berry-throw session
environment_version: wine-11.0; kernel 7.0.11-200.fc44
working_directory: work/copies/BUGS_PC-full-disc/PC/BUGS
configuration: read-only reads plus one explicitly user-authorized, immediately-reverted position write
result: confirmed
addresses:
  - "0x004C1000"
  - "0x00864000"
  - "0x0059D910"
  - "0x00861C84"
file_offsets: []
artifacts:
  - dynamic/wine/RUN-POKE-20260817-170940
  - dynamic/wine/RUN-RESTORE-20260817-170940
tags:
  - re/runtime
  - implementation/tooling
---

# Live game-memory read save restore validation

## Question

Do the `game-memory.py` read (`state`/`peek`), save (`snapshot`), and reload
(`restore`) verbs work against the **running retail PC game**, not only the
synthetic fixture they were built against? See [[Session control plane]].

## Procedure

The target was the already-running EXP-20260817-187 berry-throw session
(PID `57939`, process group `57698`), which this session did not launch and
does not own. The user explicitly authorized the memory writes for this
tooling test only.

1. Read the live game's identity and state (`game-memory.py state`).
2. Parse `/proc/57939/maps` and check whether the `.data` section
   `0x004C1000`–`0x00864000` is one contiguous writable mapping, as the tool's
   default checkpoint region assumes.
3. Read-only snapshot of the full `.data` section (`--no-freeze`).
4. The reload cycle on the 12-byte current-position triple `0x0059D910`:
   frozen `snapshot` → guarded authorized `poke` of X to a marker →
   read back → `restore` → read back.

## Expected

Reads return sane values and a verified retail identity; `.data` maps as one
region; the snapshot captures it; the poke changes X and the restore reverts
it exactly.

## Observed

**Confirmed.**

- **Identity/read.** `state` verified `exe_sha256`
  `97c95ba5572dce63…`, loader `…/wine-preloader`, cwd
  `work/copies/BUGS_PC-full-disc/PC/BUGS`, and read current position
  `(-120108, -29503, 135084)`, internal level `17`, `NextLife=0`. The
  hardcoded global addresses return coherent values from the real process.
- **`.data` layout.** `/proc/57939/maps` shows `0x004C1000-0x00864000` is
  exactly one `rwxp` mapping, ending precisely where the next mapping begins.
  The single-contiguous-`.data` assumption behind the default checkpoint region
  is therefore correct on the real Wine image, not only the fixture. (The
  runtime perms are `rwx`, not the on-disk `rw-`; the Wine loader maps the
  image executable.)
- **Save.** A read-only `snapshot` of `.data` captured 3,813,376 bytes,
  SHA-256 `e04fa9a8b53aee37ed637d6a40523d01961da4ce1a0df6a10d59899c6a381a6b`,
  to a git-ignored file with a header recording pid/exe/level. (Deleted after
  the test; it held game bytes and was transient.)
- **Reload cycle.** X `-120108` → frozen 12-byte snapshot → guarded `poke`
  set X to `1234567` (`--expect-current` matched, write verified) → read back
  `1234567` → `restore` (`verified: true`, `same_process: true`,
  `level_changed: false`) → read back `-120108`, full position
  `(-120108, -29503, 135084)`. Receipts:
  `RUN-POKE-20260817-170940`, `RUN-RESTORE-20260817-170940`.

## Interpretation

The `game-memory` read, save, and restore path works against the real game.
The central design assumption — that all mutable game state the project has
identified lives in one writable `.data` section that can be captured and
written back — is validated live for the first time, and the full
save→change→reload→verify loop reverts a real, observable global exactly.

## Result

**Confirmed** for the `game-memory` memory read/save/restore path on an
existing, same-level, same-process target. This partially retires CAP-010 and
gives CAP-011's in-process checkpoint its first live confirmation.

What this does **not** establish, and remains fixture-only or unproven:

- `game-session` launch, the renderer gate, and carousel navigation; and
  `send-keys` and `wait-for` — none were exercised live.
- Restore of the full 3.8 MB `.data` (only a 12-byte region was written).
- That restoring a **complex running** state resumes gameplay faithfully. The
  target was idle (two reads a second apart were identical, i.e. the logic
  loop was paused, unfocused per [[EXP-20260816-148 - Modified grain-gate thresholds for remaining gates]]);
  only a static position was reverted.
- Any durable, cross-relaunch savestate. That remains CRIU, blocked here by
  `ntsync` (`KU-028`, CAP-011).

## Lifecycle and safety

Writes were explicitly user-authorized for this test. They were performed on a
session this context does not own (EXP-20260817-187's); the single change was
reverted, position was left exactly as found, and the process was left in
state `R` (not SIGSTOPed). No executable, asset, `originals/`, or persistent
configuration was modified. The `SIGSTOP`/`SIGCONT` freeze pair completed on
every snapshot/restore. See [[Environment Status]].

## Follow-up

A clean owned-session arm (CAP-010) that also exercises `game-session` launch,
`send-keys`, `wait-for`, a full-`.data` restore, and a restored *running*
state that continues gameplay.
