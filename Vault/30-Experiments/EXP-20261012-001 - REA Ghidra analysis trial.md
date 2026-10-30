---
type: experiment
id: EXP-20261012-001
date: 2026-10-12
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44 host under load (load average 17–26 on 16 cores); rea-agents 6.4.0 CLI over Ghidra 12.1.2 and JDK 21.0.12; static only, no game launch or memory access
question: Does REA (github.com/morluto/rea), a Ghidra-backed agent analysis tool, add to ABLPC's existing static tooling for bugs.exe?
result: It works here and matched the existing export's facts (10 of 10 references, same decompiled body) at 60–90 s per CLI query against 45 ms. It shares Ghidra's blind spots; a raw scan found an 11th reference that both missed. Its caller lists do not follow thunks. Optional, not adopted as a core tool
status: complete-bounded
created: 2026-10-12
updated: 2026-10-12
evidence: [EXP-20261012-001]
tags: [experiment/tooling, re/static]
---

# EXP-20261012-001 - REA Ghidra analysis trial

## Question and scope

The user asked whether [REA](https://github.com/morluto/rea) would help the
project keep going, and then approved a trial. REA wraps Hopper, Ghidra or IDA
so an agent can query a binary through MCP or a CLI. The trial tests only its
Ghidra path on the retail executable. It answers two questions from
[[Next Tasks]]: a writer and reader census of a global (section 5.5), and the
last unidentified KU-072 callee. The [[Known Unknowns]] register is the
reference for both. No agent or MCP registration was made, and no game ran.

## Setup

- **Package.** `rea-agents` 6.4.0, the newest of eight releases in seven days
  (three major versions). It was installed with npm `--ignore-scripts` and an
  exact pin into the ignored `work/tools/rea-agents-6.4.0`. The package
  declares no install hooks. Integrity is recorded in
  `reports/rea/EXP-20261012-001/summary.json`.
- **Provider check.** `rea doctor --provider ghidra` accepted
  `tools/ghidra/ghidra_12.1.2_PUBLIC` and `tools/jdk/jdk-21.0.12+8`.
  "Environment not healthy" reflects only the absent agent registration.
- **Target.** A copy of `work/copies/BUGS_PC-disc/bugs.exe` at
  `work/experiments/EXP-20261012-001/target/bugs.exe`, rechecked at the
  retail SHA-256.
- **Comparisons.** The existing export, through `scripts/ghidra-query.py`,
  and an independent capstone decode of every occurrence of the address bytes
  in executable sections.

## Results

### References to `0x0059A5EE`

| Source | Time | Result |
|---|---|---|
| `rea xrefs` | 61 s (fresh import and analysis) | 10 sites: `0x413a96`, `0x41a6d4`, `0x41aa7d`, `0x41b80f`, `0x41b831`, `0x41b86f`, `0x41b876`, `0x41b8ad`, `0x438eb0`, `0x44d472`. Kinds are not listed in this view |
| `ghidra-query xrefs` | 45 ms | The same 10, in six functions, with READ/WRITE kinds |
| Raw capstone scan | under 1 s | **11** sites: the same 10, plus `0x41a992` |

- **Instruction boundaries.** The scan's first pass placed `0x41a6d4` and
  `0x41aa7d` one byte late. Both carry a `66` prefix and are 16-bit stores
  (`mov word ptr [0x59a5ee], ax/cx`). REA's addresses were right.
- **The 11th site.** `0x41a992: 66 89 15 ee a5 59 00` is
  `mov word ptr [0x59a5ee], dx`. It is the tail of a routine that fills
  `0x59a5e0`–`0x59a5ee` (`[0x59a5ec] = 2`, then `ret` at `0x41a99a`).
- **Why both Ghidra views miss it.** Ghidra never made that code into a
  function. `rea function 0x41a992` reports "No procedure exists" (86 s). No
  direct `E8`/`E9` lands in `0x41a940`–`0x41a9cf`, so its entry and callers
  are unknown.

### `0x00403A10` (KU-072)

| Source | Signature | Callers |
|---|---|---|
| Raw disassembly | Reads `[esp+4]` and `[esp+8]`, ends in a plain `ret` after the caller's `add esp`: two stack arguments, caller cleans | — |
| REA (fresh analysis, 92 s) | `__stdcall`, 2 parameters | none: it does not follow thunk `0x401d61` |
| Export | `__fastcall`, 4 parameters | `ghidra-query callers` follows the thunk to `FUN_00417720` (call `0x004181e4`) and `FUN_0041dc60` |

Both decompilers give the same body. It stores the two byte arguments to
`0x0059D9B6` and `0x0059D9B7`, then calls `0x00410A20(0x7D, 0, arg1)`.

## Confirmed, inferred, unknown

- **Confirmed (static, two forms).** `0x0059A5EE` has 11 code references in
  the retail executable: Ghidra's 10, plus a 16-bit store at `0x41a992` in
  code Ghidra does not treat as a function. These are Ghidra references and
  raw decoding.
- **Confirmed (raw disassembly).** `0x00403A10` takes two stack arguments with
  caller cleanup. Neither decompiler's calling convention matches.
- **Inferred.**
  - For this executable, REA's Ghidra path carries the same facts as the
    existing export, because both are Ghidra auto-analysis.
  - An MCP session would avoid the per-command import, but that is not
    measured.
- **Unknown.**
  - The routine containing `0x41a992`: its entry, its callers, and whether it
    runs.
  - What `0x00410A20` does with event `0x7D`.

## Disposition

REA is not adopted as a core tool, and no MCP registration was made
([[Decision Log]] 2026-10-12):

- **No new facts.** It added none here, cost 60–90 s per CLI query, and has
  the export's blind spots.
- **Weaker caller tracing.** It traces callers less well than
  `ghidra-query`, which follows thunks.
- **Wrong bottleneck.** It does not touch the project's main constraint,
  runtime game control (CAP-010).

The pinned install stays in `work/tools/` for a fresh Ghidra re-analysis, or
for an interactive MCP session if a later bulk task (creature identities, for
example) needs one.

The main research result is a method lesson. A census of writers to a global
must include a raw scan of the executable sections, not only Ghidra or REA
cross-references.

## Artifacts

- `reports/rea/EXP-20261012-001/summary.json` (tracked: versions, hashes,
  addresses and timings; no decompiled text).
- `work/experiments/EXP-20261012-001/` (ignored): the full REA JSON outputs,
  the snapshot and the export query.
