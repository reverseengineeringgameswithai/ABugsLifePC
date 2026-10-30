# ABLPC agent instructions

This project uses `Vault/` as durable shared research memory. The canonical detailed policy is `Vault/00-System/Agent Operating Manual.md`; do not create a divergent policy here.

Before substantive work, read:

- `Vault/00-System/START HERE.md`
- `Vault/00-System/Current State.md`
- `Vault/00-System/Environment Status.md`

Then read the MOC relevant to the task.

This repository holds the reverse-engineering research only. The author's own
modding project is kept elsewhere; do not add mod design, builds or play
sessions here. Engine facts and modification requirements belong here, written
up as research with their evidence.

`make briefing` prints a generated, bounded orientation (about 4,600 tokens)
with pointers into those notes. It is a map, not an authority, and does not
replace the reading above: verify anything you rely on in the note it cites.
`make budget` reports the current sizes of the mandated set.

Never modify `originals/`. Never commit full decompiler or string dumps of the executable (`ghidra-evidence.json`, `strings.txt`, `rabin2-strings.json`) or game screenshots. Never commit original binaries, game assets, disc images, ROMs, Windows media, memory dumps, or virtual disks. Work on copies under `work/`.

Separate confirmed facts from inference. Every significant reverse-engineering conclusion must reference static evidence, runtime evidence, a file offset, an executable address, or an experiment ID. Prefer two independent evidence forms for important claims.

Do not rename unidentified functions or structure fields merely because a semantic interpretation seems plausible. Prefer names such as:

- `unknown_00418A20`
- `candidate_level_reader`
- `probable_actor_update`

until evidence supports something stronger.

Decompiler output is evidence, not source code. Do not mechanically copy decompiler pseudocode into `reimplementation/`.

For parsers:

- bounds-check every read;
- preserve unknown fields;
- reject impossible offsets/counts;
- test multiple files;
- add regression tests;
- use synthetic fixtures where possible.

Do not silently resolve contradictory evidence. Record the contradiction and propose a discriminating experiment.

Treat the PS1 research repository (conventionally `~/Downloads/ABL`) as an external, read-only PS1 comparative source. Follow `Vault/00-System/Cross-Port Evidence Policy.md`: do not copy or link the repository into ABLPC, cite its commit and relative path, and never promote PS1 evidence into a confirmed PC claim without independent PC evidence.

## Publishing

This repository is public on GitHub. `scripts/git-hooks/private_names.py`
refuses any commit whose files (plain, UTF-16, hex or base64), paths, message
or identities contain a name listed in the local, unpushed
`.git/info/private-names`. It runs at commit time, at push time, and before
this clone's GitHub login is issued, and CI repeats it on every push. Never
bypass it (`--no-verify`), never edit or empty that list, and never copy its
contents into a tracked file. Runtime tools record absolute paths: before
committing new receipts or notes, replace the home-directory prefix with
`/home/dev`, as the existing receipts do. Ask before any force-push or history
rewrite.

## Tooling

Machine-readable contracts: `make harness-caps`, `input-movie-caps`,
`coordinate-caps`, `session-caps`, `memory-caps`, `keys-caps`, `wait-caps`.

- Live sessions: `scripts/game-session.py` (launch/status/level/close/audit),
  `game-memory.py` (peek/state/watch/snapshot, and authorization-gated
  poke/teleport/restore — snapshot/restore are same-process `.data` state
  checkpoints; CRIU is blocked here, see `make criu-check`).
  `scripts/savestate-hotkeys.py` gives in-game save-state hotkeys grabbed
  on the game's nested display (F5 save / F9 load by default),
  `send-keys.py`, `wait-for.py`. These are **fixture-validated only**, except
  `game-memory`'s read/snapshot/poke/restore cycle (live-validated in
  EXP-20260817-188) and the hotkeys' key grab; `game-session` launch and
  navigation, `send-keys` and `wait-for` have never run against the real
  game. Until CAP-010's acceptance arm passes,
  `Vault/10-Environment/PC autonomous game control.md` is the authoritative
  procedure and no tool output is runtime evidence. Any memory write needs
  fresh explicit user authorization per use, plus a compare-before-write guard
  and a receipt.
- Before any launch and after any close, run `make session-audit` and account
  for what it reports.
- Static analysis: `scripts/ghidra-query.py` instead of reading the 7.7 MB
  `ghidra-evidence.json`. Read
  `Vault/20-Research/Ghidra export structure and caveats.md` first — the
  export's `imports` is empty, its `callers` are call-site addresses, and its
  call graph breaks at thunks.
- Evidence: `scripts/run-index.py` (runs cross-referenced against citations),
  `scripts/experiment-draft.py` (an experiment note pre-filled from receipts).
- After correcting a claim, run `scripts/claim-sweep.py pair --old ... --new
  ...` before handing the packet to an audit. A tree carrying both wordings is
  the defect that has cost this project the most audit rounds.

Run `make check` before committing, and `make install-hooks` once so the fast
gates run automatically.

At the end of meaningful work:

- update relevant Vault notes;
- update `Current State.md`;
- update `Known Unknowns.md`;
- record important decisions;
- create a session note;
- update relevant MOCs;
- ensure new conclusions point to their evidence.

## Mission and cross-port boundary

Before substantive reverse-engineering work, read `Vault/00-System/Project Charter.md`. The Windows PC executable and its recorded behavior are authoritative. Keep `~/Downloads/ABL` external; PS1 work may be consulted only for a bounded PC-native unknown, at a recorded commit, and any correspondence remains cross-port inference until verified against PC evidence.
