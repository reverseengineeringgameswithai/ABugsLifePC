# ABLPC: reverse engineering *A Bug's Life* (PC)

> Every step of this was used with AI. Some things may be inaccurate or false.
> I will not be updating this repo going forward.

This repository is a reproducible, evidence-driven research record for the
Windows PC version of Disney/Pixar's *A Bug's Life* (1998). It documents how the
original executable and its data files work: formats, functions, structures,
subsystems and runtime behaviour, plus what the engine requires, permits or
limits when its files or code are changed. The original executable under
controlled conditions is the behavioural reference; AI output and decompiler
output are hypotheses or evidence, never ground truth by themselves.

It contains no game files. To reproduce the runtime work you need your own copy
of the game (see [Original-file workflow](#original-file-workflow)).

## Scope of this repository

This is the research half of a larger private workspace. It carries:

- the Obsidian research vault (`Vault/`): experiments, function, structure and
  file-format dossiers, subsystem notes, cross-port comparisons, decisions,
  known unknowns and session logs;
- the evidence those notes cite: runtime receipts (`dynamic/`), generated
  reports (`reports/`) and static exports (`static/`);
- the research tooling: bounds-checked parsers and inspectors, the M4
  manifest/overlay toolkit and M6 release layer, the M3/M5 proof recipes,
  harness and evidence scripts, and their synthetic tests.

Deliberately not included:

- **The author's own modding project** (custom levels and features built on
  this research). Engine facts first measured while building it are kept,
  written up as research. Some experiment IDs are cited in plain text without
  a note; those belong to the modding project.
- **Full decompiler, disassembly-adjacent and string dumps** of `bugs.exe`
  (`ghidra-evidence.json`, `strings.txt`, `rabin2-strings.json`) and game
  screenshots. Regenerate the dumps locally from your own copy with
  `scripts/ghidra-export.sh` and `scripts/pe-triage.sh`; `scripts/ghidra-query.py`
  reads the regenerated export.
- **The R2 static-mesh localization harness code.** It is bound to the
  original host (absolute paths, inode and process pins). Its experiment notes
  and receipts are included.

Recorded absolute paths in receipts and notes were normalised to
`/home/dev/ABLPC` for publication. Hashes recorded for files that contain
such paths describe the files as originally captured.

## Start here

1. Read [Vault/00-System/START HERE.md](Vault/00-System/START%20HERE.md).
2. Review [Vault/00-System/Current State.md](Vault/00-System/Current%20State.md) and [Vault/00-System/Environment Status.md](Vault/00-System/Environment%20Status.md).
3. Create the pinned environment (`python3 -m venv .venv && .venv/bin/pip install -r requirements.lock`), then run `make doctor` and `make check`.
4. Select the Map of Content relevant to the task; [Reverse Engineering MOC](Vault/01-MOCs/Reverse%20Engineering%20MOC.md) is the default.

The vault is the durable shared memory for people and agents; conversation
history is disposable. Agents (Codex, Claude Code) start from the repository
root; `AGENTS.md`/`CLAUDE.md` hold their instructions.

The PS1 reverse-engineering repository at `~/Downloads/ABL` is an external comparative source, not a dependency or source of PC ground truth. It is never vendored, linked, or copied wholesale. Cross-port work follows `Vault/00-System/Cross-Port Evidence Policy.md` and requires independent PC confirmation.

## Directory layout

| Path | Purpose |
|---|---|
| `Vault/` | Obsidian vault and durable human/agent research memory |
| `originals/` | Immutable user-owned source material; never committed |
| `media/` | User-owned installation media; never committed |
| `work/copies/` | Experimental copies of originals |
| `work/ghidra/` | Ghidra databases |
| `static/` | Reviewable static-analysis exports |
| `dynamic/` | Runtime evidence and run metadata |
| `research/tasks/` | Bounded evidence packets for agents |
| `scripts/` | Reproducible capture, triage, and note tools |
| `reimplementation/` | Independently written implementation work |
| `tests/` | Synthetic fixtures and regression/golden tests |
| `reports/` | Generated inventories and environment reports |
| `tools/` | Project-local tools; binaries are Git-ignored |

## Environment roles

- **Wine** is the primary Linux modding, compatibility, and trace environment.
- **86Box + Windows 98 SE** is an optional period-correct cross-check, not a release blocker.
- **KVM/libvirt Windows VM** is an optional modern dynamic-debugging environment.
- **PCem** is only a secondary emulator cross-check when 86Box behavior is suspicious.
- **Ghidra** is the primary static-analysis tool; reviewable exports belong in `static/exports/`.

## Common commands

```bash
make doctor
make python-doctor
make vault-lint
make test
make new-experiment QUESTION="What behavior is being tested?"
make hash-originals
make inventory-originals
./scripts/ablpc-mod --help
./scripts/ablpc-mod inspect-anm \
  work/copies/BUGS_PC-full-disc/PC/BUGS/CD/PLANTS/PLANT04.ANM --json
./scripts/ablpc-mod dry-run --help
./scripts/ablpc-mod restore --help
./scripts/census-pc-content.py --help
./scripts/check-m4-compatibility.py
./scripts/ablpc-release --help
./scripts/m6-smoke --help
./scripts/play-pristine.sh --help
```

`make originals-readonly` is an explicit, opt-in operation after ingestion. It never runs automatically.

The modding vertical slice (M1–M6) is documented in [reimplementation/README.md](reimplementation/README.md). It builds only ignored work trees or sparse overlays and never bundles game data. M4.18 independently accepts M4.17's cross-checked current-Linux later-mount order: the reused-lower-ID alias refuses before traversal while covered-stack behavior and every retained baseline survive. This accepts ordinary sparse-overlay removal only at that current-Linux boundary. M4.19 publishes the strict, asset-free historical [M4 v0.1 compatibility statement](reimplementation/compatibility/m4-v0.1.json); M4.20 and M4.22 expose two authority-alignment defects, and M4.23 closes them with exact same-read pins for only the five machine authorities. Independent M4.24 accepts that correction after 10/10 predecessor attacks, 5/5 direct mutations, exactly nine asset-free reads, and every retained gate pass. M4.25 provides a deterministic write-free report for one existing manifest, and independent M4.26 accepts that exact boundary after direct byte reconstruction, write traps, exact snapshots, retained receipts/workflows, and 99/161/349 tests. M4.27's full evidence ledger rejects milestone closure because receipts still require the original manifest and no accepted test joins one tool-created clean-copy install through validation, launch, and removal. M4.28 is worker-complete on strict external-receipt replay into a new sparse root and receipt-authenticated removal without the original manifest; exact M4.29 rejects one checked-parent substitution. M4.30 closes that bypass at the worker boundary, but exact M4.31 rejects its descriptor-release claim. M4.32 corrects exhaustive one-attempt receipt-chain closure, and independent M4.33 accepts it after reproducing the +7/+6 parent defect, passing 28/28 fresh indexed close cases, 161/223/411 tests, six local cycles, five pins, and nine reads. `KU-051` is resolved only at that strict boundary. M4.34 then rejects milestone closure after a same-tree four-route audit: complete staged/forced-copy trees are structurally launcher-ready but dedicated sparse removal rejects their necessary extra game content unchanged, while removable apply/replay trees are not complete launch inputs. M4.35 adds distinct manifest-driven restoration of an authenticated complete staged copy. Independent M4.36 rejects Windows-case-equivalent complete-tree paths; M4.37 corrects them, and independent M4.38 accepts after 36 fresh collision cases, four bind-mounted sibling-order cases, all eight namespace families, the exact full-tree lifecycle, six sparse cycles, five pins/nine reads, and 198/260/448 tests. `KU-052` resolves only for the demonstrated manifest-driven current-Linux lifecycle. M4.39 publishes the strict active [M4 v0.2 compatibility statement](reimplementation/compatibility/m4-v0.2.json) while preserving v0.1 byte-for-byte, the five pins, and exactly nine asset-free reads. Independent M4.40 retains those facts and the restoration boundary but rejects selected-path cross-version acceptance, reordered-object-field acceptance, and an uncaught malformed-ID error; exact suites pass 58/271/459, correcting the stale worker combined count 266. M4.41 closes those regular-file checker failures at the worker boundary, preserves both statement hashes/five pins/nine reads, and passes 71/284/472 suites. Independent M4.42 retains that evidence but rejects selected-path identity because the default active pathname can link to the historical selected file and validate v0.1. M4.43 closes that exact worker boundary with lexical selection, selected regular non-link admission, retained unselected links, and 75/288/476 suites. Independent M4.44 accepts that correction after selected link/nonregular no-read attacks, lexical aliases, unselected exact contracts, complete statement/order/leaf/pin reconstruction, normal nine-read checks, and full ledger reconciliation. M4 is Complete at 9/9 required capabilities and 5/5 exit gates only at the documented asset-free, current-x86_64-Linux boundary. No broader platform, authorship, general dry-run, external-receipt full-tree restoration, whole-tree deletion, package, rollback, transaction, POSIX-metadata, concurrency, or runtime-automation claim is implied, and no successor milestone is activated.

`EXP-20260814-104` supplies a second independent post-closure `ACCEPT` after a
separate 663-assertion path/content/read matrix, exact ledger reconstruction,
and 75/288/476 suites. It preserves the same final-entry-only filesystem
boundary, explicit unsupported list, and no-successor disposition.

## Asset-free toolkit release

M6 adds a separate release layer without widening M4's game-facing claims.
The exact `ablpc-toolkit-v1.0.0` contract, supported hashes, primary Linux
environment, smoke cases, and limitations are in
[reimplementation/M6-RELEASE.md](reimplementation/M6-RELEASE.md) and
[reimplementation/release/m6-v1.0.0.json](reimplementation/release/m6-v1.0.0.json).

Builds require a clean tracked allowlist and produce a deterministic tar plus
SHA-256 sidecar. Installation verifies every archived file and keeps each
version immutable; migration selects the new version while retaining the
prior selection, and rollback atomically selects that verified prior toolkit
without reading or changing game files. Packaged Python entry points disable
bytecode generation so normal tool use does not add files to an installed
version. Install, current, and rollback reject linked release/version roots or
linked/nonregular state before changing selection. They also require canonical
single-link state/package files, exact implicit package-directory topology and
modes, and valid manifests for every installed version, including inactive
retained versions. Canonical install-state schema 2 retains the verified
archive, release-manifest, and source-tree hashes for each installed version,
so rewriting package content together with its in-tree manifest still rejects.
The primary smoke matrix creates only ignored disposable staged work copies,
covers Training, Level 01, and the schema-2 character recipe, launcher-dry-runs
them, restores them exactly, and checks that the source copy did not change.

```bash
./scripts/ablpc-release build --output-dir work/releases/a
./scripts/ablpc-release verify work/releases/a/ablpc-toolkit-v1.0.0.tar
./scripts/m6-smoke \
  --game-root work/copies/BUGS_PC-full-disc/PC/BUGS \
  --prefix work/wine/baseline \
  --report work/m6-smoke-report.json
```

The automated smoke result is launcher readiness, not automated gameplay or a
rendered compatibility claim. Hardware selection and gameplay input remain
manual. Windows 98 and every unlisted platform/version remain explicitly
untested.

The metadata-only PC content census is documented in
[Vault/20-Research/PC Content Census.md](Vault/20-Research/PC%20Content%20Census.md).
Its report records paths, sizes, hashes, groupings, and retained loader-log
matches; it does not embed game-file payload bytes.

## Play the unchanged game on Linux

After preparing the baseline Wine prefix and derived full-disc work copy described in the Vault, run:

```bash
./scripts/play-pristine.sh
```

At the game's first selector, choose **hardware acceleration** (the second option). The selector defaults to software rendering, which starts gameplay at 320×200; the tested Direct3D path renders at 640×480×16. The launcher uses Gamescope's `fit` scaler so the 4:3 image fills the display height without stretching. Its default `nearest` filter keeps pixels crisp; `--filter linear` gives a softer presentation without changing the aspect ratio.

The default 2560×1440 output matches the tested host. Use `--output WIDTHxHEIGHT` on a different display. The launcher verifies the known executable hash and refuses to run a game directory outside `work/copies/`.

## Configure Tunnels and City Entrance grain gates

Build a fresh executable from the exact retail work copy:

```bash
./scripts/make-grain-gates \
  work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe \
  work/copies/bugs-grain-gates.exe \
  --tunnels 1,2,3,4,5,6,7,8,9 \
  --city-entrance 1,2,3
```

Tunnels takes nine resident-table requirements; City Entrance takes three.
Values are limited to `0..50`, and an omitted level retains its retail values.
The builder refuses the wrong executable, linked/out-of-work paths, overwrite,
source-byte drift, or a transform without an exact inverse. The output is a
user-local game-bearing work artifact and must not be committed or
distributed. See [PC grain gate threshold mod](Vault/40-Implementation/PC%20grain%20gate%20threshold%20mod.md)
for the exact supported boundary. The example profile has independently
accepted runtime receipts for Tunnels row 3 (`3` closed, `4` open) and City
gate 0 (`0` closed, `1` open); other gates are not generalized.

## Original-file workflow

Place only user-owned game files in `originals/`. Do not analyze or execute them in place. First run:

```bash
make hash-originals
make inventory-originals
```

Then copy files needed for experiments into `work/copies/`. Generated PE triage belongs under `static/pe/BIN-.../`; runtime runs belong under `dynamic/`; experimental state belongs under `work/`.

## Research method

Every significant conclusion must be marked **Confirmed**, **Inferred**, or **Unknown** and cite an executable address, file offset, static artifact, runtime run ID, or experiment ID. Prefer two independent forms of evidence for important claims. Do not mechanically translate decompiler pseudocode into source code.

## Safety and copyright

Never commit original binaries, assets, disc images, ROMs, Windows media, dumps, or virtual disks. Never patch `originals/`. Debugger and agent-control services must use localhost or host-only networking. Community plugins and arbitrary reverse-engineering MCP servers are not part of this bootstrap.

## Project charter

The durable mission, evidence hierarchy, research phases, repository hygiene rules, and PC-first cross-port policy are defined in `Vault/00-System/Project Charter.md`. Read it before changing research scope or consulting another port.

## Building on this work

This repository is a snapshot and is not maintained. To continue the research,
fork it. Start with [START HERE](Vault/00-System/START%20HERE.md),
[Next Tasks](Vault/00-System/Next%20Tasks.md) and
[Known Unknowns](Vault/70-Known-Unknowns/Known%20Unknowns.md). Findings are tied
to the retail `bugs.exe` with SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`; verify them
against your own legally obtained copy rather than taking the notes on trust.

## License

[MIT](LICENSE), covering this repository's own notes, code and data. You may
fork, copy, modify and redistribute it, including commercially, provided the
copyright and permission notice in `LICENSE` is kept with substantial copies.

Not covered by that license:

- *A Bug's Life* itself. No game files are included. The game, and the short
  excerpts of its text and code quoted here for analysis, remain the property
  of their rights holders.
- `tools/86box/patches/`: modifications of 86Box, distributed under 86Box's
  own license (GNU GPL), not MIT.
- Third-party tools and packages the scripts call (Ghidra, Wine, Gamescope,
  86Box, Blender, and the Python packages in `requirements.lock`). They keep
  their own licenses and are not redistributed here.
