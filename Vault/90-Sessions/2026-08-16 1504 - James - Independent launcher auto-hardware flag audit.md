---
type: session
date: 2026-08-16
agent: James
status: complete
tags: [session, workflow/play, implementation/compatibility, re/direct3d, re/audit]
---

# Independent launcher auto-hardware flag audit

## Goal

Adversarially audit, from fresh context, the launcher change at HEAD
`727b37b` that adds an opt-in `--auto-hardware` flag to
`scripts/play-pristine.sh` (a pinned M4 compatibility machine authority) and
return ACCEPT or REJECT. Statically audit the launcher wiring, the M4 re-pin,
and the M4 structure/semantic preservation; do not launch the game (the
transform and runtime behavior are already accepted in EXP-150/151).

## Verdict

**ACCEPT.** Recorded in
[[EXP-20260816-152 - Independent launcher auto-hardware flag audit]].

## What I checked

1. **Changed files** - `git show --stat 727b37b` touches exactly 8 files
   inside the acceptable set (launcher, compatibility.py, new launcher test,
   5 Vault notes). No game bytes; `originals/` untouched.
2. **M4 re-pin** - the single compatibility.py change re-pins the launcher from
   `68c91717…4049977e` to `6ca3c657…41eb690`, which **equals**
   `sha256sum scripts/play-pristine.sh`. `check-m4-compatibility.py` passes
   (v0.2, 5 anchors). `m4-v0.2.json` unchanged by the commit; semantic claims
   (`renderer_selection` manual, `640x480`, `fit`, `nearest`) intact.
3. **Structure by construction** - `_require_launcher_structure` /
   `_require_shell_assignments` code is unmodified; the launcher still has one
   `COMMAND` block with `-w 640 -h 480` and `-S fit -F "$FILTER"`, the exact
   game-dir guard, and exactly one unindented renderer echo (kept verbatim).
   The auto-hardware note is a separate indented block; no second matching echo.
   Retail `EXPECTED_EXE_SHA256` and the `GAME_DIR`/`OUTPUT_*`/`FILTER`
   assignments are unchanged.
4. **Wiring** - hash-gates the retail source, builds/reuses the cache by hash
   `1e1d5099…`, verifies the built hash, runs `wine "$EXE_RUN"` from the retail
   `cd "$GAME_DIR"`. `bash -n` clean; auto-hardware dry-run prints the cached
   patched-exe command from the retail dir (cache hash `1e1d5099…`, fresh
   rebuild reproduced it); plain dry-run prints `wine ./bugs.exe`.
5. **Tests** - `pytest tests/test_play_pristine_launcher.py
   tests/test_auto_hardware_mod.py -q` = 13 passed; launcher tests cover help,
   retail path, cache build + patched run from retail cwd, and cache reuse.
6. **No falsified history** - the commit's `Vault/` diff touches only
   current-state/baseline/candidate/session-index/new session note; historical
   records keep the old pin (still in 15 Vault files; none deleted).
7. **Hygiene** - `git status` clean at HEAD; cache git-ignored and untracked;
   `make check` green (623 tests, Vault lint 435/0, M4 5 anchors, tracked audit
   0).

## Defects

None. The accepted boundary is the opt-in flag with the M4-checked structure
and every semantic claim preserved, only the launcher byte pin re-pinned — the
intended deliberate-change workflow. Runtime markers were out of scope
(already accepted in EXP-150/151).

## Constraints honored

Read-only toward game media and `originals/`; game not launched; nothing
committed or staged. The only writes were rebuilds of the git-ignored
auto-hardware cache under `work/copies/` while exercising the dry-run wiring;
the tree stayed clean.

## Next

Worker reconciles [[Current State]] and related notes after this verdict; no
correction packet is required.
