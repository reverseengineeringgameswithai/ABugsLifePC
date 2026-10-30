---
type: experiment
id: EXP-20260816-152
date: 2026-08-16
question: Does the launcher change at HEAD 727b37b add an opt-in --auto-hardware flag to play-pristine.sh with the M4-checked structure and semantic claims fully preserved, only the byte pin re-pinned, no falsified history, and clean hygiene?
status: accepted
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
modified_binary_sha256: 1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f
environment: Fedora Linux 44; Linux 7.0.11 x86_64; static launcher/M4 audit plus dry-run wiring exercise; no game launch
environment_version: Python 3.14.6; pytest 9.1.1; Git 2.54.0
working_directory: /home/dev/ABLPC
configuration: fresh-context adversarial audit at clean HEAD 727b37bcfabe7fa7f7122253a24a1d98ada1b1b6 (parent 9bff348); read-only toward game media and originals; no target launch, commit, or staging; the only writes were the git-ignored auto-hardware cache under work/copies/
artifacts:
  - scripts/play-pristine.sh
  - reimplementation/ablpc/compatibility.py
  - reimplementation/compatibility/m4-v0.2.json
  - tests/test_play_pristine_launcher.py
  - scripts/make-auto-hardware
addresses: []
file_offsets: []
result: accept-opt-in-auto-hardware-flag-m4-structure-and-semantics-preserved-byte-repin-only
created: 2026-08-16
updated: 2026-08-16
tags: [re/experiment, implementation/launcher, implementation/compatibility, re/direct3d, re/audit]
---

# EXP-20260816-152 - Independent launcher auto-hardware flag audit

## Verdict and authority

**ACCEPT.** This is an independent fresh-context hard-truth audit of the
launcher change at HEAD `727b37bcfabe7fa7f7122253a24a1d98ada1b1b6` (parent
`9bff348`), which adds an opt-in `--auto-hardware` flag to
`scripts/play-pristine.sh`. The launcher is a pinned M4 compatibility machine
authority ([[EXP-20260814-082 - Closed-world machine-authority byte pins]] /
[[EXP-20260814-083 - Independent M4.23 machine-authority-pin hard-truth audit]]),
so M4 integrity was the crux. The underlying transform and runtime behavior
were **not** re-audited here — they are already accepted in
[[EXP-20260816-150 - Automatic Direct3D startup runtime acceptance]] /
[[EXP-20260816-151 - Independent auto-hardware runtime audit]] — and the game
was not launched.

No game process, Wine process, or Gamescope was used. `originals/` and the
retail work copy were not modified; nothing was committed or staged. The only
writes were rebuilds of the git-ignored auto-hardware cache under
`work/copies/auto-hardware/` while exercising the dry-run wiring; the tree
stayed clean.

Every material claim was re-derived from the repository. The change gains an
opt-in flag while the M4-checked structural surface and every semantic claim
are preserved; only the launcher byte pin is re-pinned to the launcher's new
digest — the intended deliberate-change workflow. All seven checks pass.

## Check 1 - Changed files and no game bytes

`git show --stat 727b37b` changes exactly 8 files, all inside the acceptable
set (launcher, compatibility.py, the new launcher test, and Vault notes):

- `scripts/play-pristine.sh`
- `reimplementation/ablpc/compatibility.py`
- `tests/test_play_pristine_launcher.py` (new)
- `Vault/00-System/Current State.md`
- `Vault/10-Environment/Wine Linux Play Baseline.md`
- `Vault/40-Implementation/PC automatic Direct3D startup candidate.md`
- `Vault/90-Sessions/2026-08-16 1451 - Claude - launcher auto-hardware flag.md` (new)
- `Vault/90-Sessions/Session Index.md`

No game bytes, no binaries, nothing under `originals/`.

Result: **PASS.**

## Check 2 - M4 machine-authority re-pin

- The compatibility.py diff is a single line: the
  `scripts/play-pristine.sh` entry in `MACHINE_AUTHORITIES` /
  `EXPECTED_MACHINE_AUTHORITY_SHA256` changes from
  `68c9171749bd7b207a15b4202193ccfddd2661fbb383deb34b1a5a5a4049977e` to
  `6ca3c65750be95b05f3099f414dc67121f95cff84dca64758d97ebf6841eb690`.
- `sha256sum scripts/play-pristine.sh` =
  `6ca3c65750be95b05f3099f414dc67121f95cff84dca64758d97ebf6841eb690` — the new
  pin **equals** the actual current launcher digest.
- `.venv/bin/python scripts/check-m4-compatibility.py` prints
  `M4 compatibility statement valid: ablpc-m4-compatibility-v0.2 (5 hash
  anchors)` and exits 0.
- `git show 727b37b -- reimplementation/compatibility/m4-v0.2.json` is **empty**
  — the M4 v0.2 canonical statement JSON was not changed by this commit.
- The statement's semantic launcher claims are unchanged:
  `renderer_selection` = `manual-down-then-confirm-hardware-acceleration`,
  `gamescope_game_surface` = `640x480`, `scaler` = `fit`,
  `default_filter` = `nearest`, `default_output` = `2560x1440`,
  `executable_anchor` = `pc-executable` (`97c95ba5…`).

Result: **PASS.**

## Check 3 - M4 structure check still satisfied by construction

The structure-check code in `compatibility.py` (`_require_launcher_structure`,
`_require_shell_assignments`) is **not** modified by this commit — only the
pinned digest line changed — so the check passes on its own merits, not by
weakening.

- `_require_launcher_structure`: exactly one `^COMMAND=\(\n…^\)$` block
  (lines 172-179), containing `-w 640 -h 480` (line 174) and `-S fit -F
  "$FILTER"` (line 176); the exact `case "$GAME_DIR/"` guard is present and
  unique (lines 118-121). The renderer echo regex
  `^echo "At the renderer selector, ([^"]+)" >&2$` matches **exactly one**
  unindented line — line 182,
  `echo "At the renderer selector, press Down once, then confirm hardware
  acceleration." >&2` — kept verbatim. The auto-hardware note the worker added
  (lines 184-185) is a separate 4-space-indented `if` block whose text does not
  begin `At the renderer selector,`, so no second matching line exists.
- `_require_shell_assignments`: `EXPECTED_EXE_SHA256` = retail
  `97c95ba5…27b878` (line 5); the `GAME_DIR` assignment list
  (`"$ROOT/work/copies/BUGS_PC-full-disc/PC/BUGS"`, `$2`,
  `$(readlink -f -- "$GAME_DIR")`), `OUTPUT_WIDTH` (`2560`, `${2%%x*}`, `1280`),
  `OUTPUT_HEIGHT` (`1440`, `${2#*x}`, `960`), and `FILTER` (`nearest`, `$2`) are
  all unchanged. The new `AUTO_HARDWARE_EXE_SHA256` / `AUTO_HARDWARE_CACHE`
  variables do not collide with any pinned name (negative-lookbehind matcher;
  neither name is a substring boundary of a checked name).

Result: **PASS.**

## Check 4 - `--auto-hardware` wiring correctness

- The launcher still hash-gates the source `EXE="$GAME_DIR/bugs.exe"` to retail
  `97c95ba5…` (lines 123-130) before any branch.
- With `--auto-hardware` it builds via `scripts/make-auto-hardware "$EXE"
  "$AUTO_HARDWARE_CACHE"` into `work/copies/auto-hardware/bugs.exe` **only if**
  the cache is missing or its hash != `1e1d5099…c8a9c41f` (lines 141-150),
  verifies the built hash (lines 151-155), and sets `EXE_RUN` to that cache
  path (line 156); otherwise `EXE_RUN="./bugs.exe"` (line 136).
- `cd "$GAME_DIR"` (line 211) is still the retail game directory, so retail
  assets and Wine `Y:` are used unchanged (the patch edits only the exe). The
  `COMMAND` runs `wine "$EXE_RUN"` (line 178).
- `bash -n scripts/play-pristine.sh` — syntax OK.
- `./scripts/play-pristine.sh --auto-hardware --windowed --dry-run` prints
  `cd /home/dev/ABLPC/work/copies/BUGS_PC-full-disc/PC/BUGS` and
  `wine /home/dev/ABLPC/work/copies/auto-hardware/bugs.exe`, and the cache
  hashes `1e1d5099…c8a9c41f`. Forcing a rebuild (cache removed) also produced
  `1e1d5099…c8a9c41f`, and the retail source stayed `97c95ba5…`.
- `./scripts/play-pristine.sh --windowed --dry-run` prints `wine ./bugs.exe`.

Result: **PASS.**

## Check 5 - Tests

`pytest tests/test_play_pristine_launcher.py tests/test_auto_hardware_mod.py -q`
= **13 passed** (4 launcher + 9 mod). The launcher tests cover: help documents
`--auto-hardware`; the plain dry-run uses `wine ./bugs.exe` with no
auto-hardware; the auto-hardware dry-run builds the cache to the exact expected
hash, runs the cached patched exe (not `./bugs.exe`), and keeps the cwd at the
retail game dir; and a correct cache is reused (mtime unchanged), not rebuilt.

Result: **PASS.**

## Check 6 - No falsified history

- The commit's `Vault/` diff touches only `Current State.md`,
  `Wine Linux Play Baseline.md`, `PC automatic Direct3D startup candidate.md`,
  the new session note, and `Session Index.md`. It does **not** touch any
  historical audit record (EXP-082/083/098-103 etc.).
- The old pin `68c9171749bd…4049977e` still legitimately appears in 15 Vault
  files (Project Roadmap plus historical EXP/session notes that recorded the
  launcher hash when they ran).
- `git show 727b37b -- Vault/ | grep '^-.*68c9171749bd'` finds **no** deletions
  — the commit removed the old hash from none of those historical records. Only
  the live pin in compatibility.py changed.

Result: **PASS.**

## Check 7 - Hygiene

- `git status --porcelain` is empty at HEAD `727b37b`, and stayed empty after
  the audit's cache rebuilds.
- The cache `work/copies/auto-hardware/bugs.exe` is git-ignored via
  `.gitignore:/work/copies/` (`git check-ignore -v` confirms) and is not
  tracked (`git ls-files work/copies/auto-hardware/` is empty).
- `make check`: Python doctor green, Vault lint **435 notes / 0 errors / 0
  warnings**, M4 statement valid (`ablpc-m4-compatibility-v0.2`, 5 hash
  anchors), **623 tests passed**, tracked-file audit **0 violations**.

Result: **PASS.**

## Defects and recorded limits

None. No defect narrows or blocks the acceptance.

- The audit did not re-verify the six [[START HERE]] runtime markers or launch
  the game; the runtime behavior of the patched build is out of scope here and
  is already accepted at the derived build hash in
  [[EXP-20260816-150 - Automatic Direct3D startup runtime acceptance]] /
  [[EXP-20260816-151 - Independent auto-hardware runtime audit]] (which itself
  scopes the physical-GPU-vs-llvmpipe identity as asserted, not proven).
- The `--auto-hardware` build path relies on `scripts/make-auto-hardware`,
  whose guards were audited in EXP-151; the launcher additionally re-verifies
  the built hash before running.

## Accepted boundary

Accepted: the opt-in `--auto-hardware` flag on `scripts/play-pristine.sh`,
which builds (or reuses by hash) the guarded auto-hardware patched copy at
`work/copies/auto-hardware/bugs.exe` (SHA-256 `1e1d5099…c8a9c41f`) and runs it
from the retail game directory with retail assets and `Y:` unchanged; the
retail source hash gate; and the launcher's M4-checked structure — one
`COMMAND` block with `-w 640 -h 480` / `-S fit -F "$FILTER"`, the exact
game-directory guard, the single unindented renderer-guidance echo kept
verbatim, and the unchanged `EXPECTED_EXE_SHA256` / `GAME_DIR` / `OUTPUT_*` /
`FILTER` assignments. The M4 v0.2 canonical statement and every semantic claim
are unchanged; only the launcher byte pin in `compatibility.py` was re-pinned
to the launcher's new digest — the intended deliberate re-pin, not an M4 scope
change. Default (non-`--auto-hardware`) behavior is unchanged: the retail exe
and the manual Down/confirm procedure with the full six-marker log gate remain
authoritative for the retail hash. The worker reconciles [[Current State]] and
related notes after this verdict.
