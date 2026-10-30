---
type: experiment
id: EXP-20260815-134
date: 2026-08-15
question: Can fresh, explicitly authorized, breakpoint-free Training position writes reproduce the appended-grain and moved-duplicate-letter pickup behaviors required by M3.7?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; Wine 11 Staging; Gamescope; Direct3D 640x480x16; exact ignored PC work copies
environment_version: kernel 7.0.11-200.fc44.x86_64; Wine 11.0 Staging; Gamescope 3.16.25-1.fc44.x86_64; Python 3.14.6; GCC 16.1.1
working_directory: /home/dev/ABLPC
configuration: two fresh retail-executable Training processes; read-only 10 ms process_vm_readv observer; one approved 24-byte current-plus-preceding position write per process; no debugger, breakpoint, register, code, auxiliary, counter, mask, reward, or record write
artifacts:
  - dynamic/wine/EXP-20260815-134-receipt.md
  - work/copies/EXP-20260815-134-approved-training-runtime
addresses:
  - 0x0059D910
  - 0x0059D920
  - 0x0059D960
  - 0x0059D9B0
  - 0x0059D9B1
  - 0x0059D9B2
  - 0x0059A5B0
  - 0x005C595C
result: accepted-authorization-compliant-training-runtime-pair
created: 2026-08-15
updated: 2026-08-15
tags:
  - re/experiment
  - re/dynamic
  - re/gameplay
  - milestone/m3
---

# EXP-20260815-134 - Approval-compliant Training runtime receipts

## Question and corrective scope

Can M3.7 replace the authorization-defective Training portion of the old
runtime packet with one fresh appended-grain pickup and one fresh moved-
duplicate-letter pickup, without changing a recipe, executable, static
conclusion, or milestone gate?

[[EXP-20260815-133 - Independent M3 closure authorization hard-truth audit]]
requires this exact correction. The experiment does not retroactively approve
EXP-111 through EXP-114 and does not reuse their mutated processes.

## Prior authorization

Before either launch, the exact proposed surface was presented in the active
research exchange:

- grain arm: write current and preceding XYZ at
  `0x0059D910/14/18` and `0x0059D920/24/28` to
  `(167776,-34272,38112)`;
- letter arm: write those same six fields to
  `(156800,-59296,48000)`;
- exactly 24 target bytes per fresh process;
- no counter, mask, reward, record, auxiliary-position, register, code, or
  breakpoint change;
- read-only observation and abort-on-mismatch stop rules.

The researcher then directed the worker to continue the reject/correct/audit
ratchet until James accepts and clarified: “the approvals are up to you” and
“Assume yes for me.” This reply followed the exact mutation proposal and is
the explicit prior authorization for these two arms. It delegates mechanical
approval decisions within this bounded work-copy project; it is not treated as
permission to modify originals or widen the mutation surface silently.

## Identity and preconditions

Both arms used retail `bugs.exe`, SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.

| Arm | Training `LEVEL1.DAT` SHA-256 | Live type/count tag | Selected fresh entry |
| --- | --- | ---: | --- |
| appended grain | `20d0f9b143a4fceeb058d5ce81680b3e6317995abc3d5ac4103fc85e79b5fd40` | `0x003F003F` (63) | index 62 `(4950,-1301,1127)`, selector `0x14` |
| duplicate letter | `e9c75bb24ae0d0f4f74d17ea63431195e49b7e5278c089588d9372b8eb8cae7a` | `0x003F0043` (67) | index 63 `(4900,-1853,1500)`, selector `0x10` |

Each fresh log positively records `Native software render mode is FALSE`,
Direct3D render mode, `640x480x16`, `Starting Direct3D renderer`, Training
`level07\level1.dat`, `End InitMainGame`, and `NextLife`. Neither contains
`INITSOFTRENDER`.

The read-only observer initially interpreted the live tag as a standalone
count and refused before mutation. A second letter preflight then correctly
exposed the count-67 encoding. The observer was narrowed to candidate-specific
`0x003F003F`/`0x003F0043` tag expectations. No target write occurred until the
final precondition set passed. These are retained calibration refusals, not
behavior arms.

## Authorized write mechanism

The compiled helper is byte-identical in source to the reviewed EXP-130
teleport primitive; source SHA-256 is
`7cc425b774135cd3a4d631b35589e8e6abf0fcd7d3b00436bb008471a26eb1fb`.
One `process_vm_writev` call supplied two 12-byte remote vectors, current and
preceding XYZ. Both calls returned exactly 24 and immediate readback matched
all six proposed values. Auxiliary `0x0059D960` was not written and retained
the pre-write tuple in the immediate receipts.

No debugger attached. No breakpoint, watchpoint, execution continuation,
register change, signal delivery, counter/mask/reward reset, live-record
restoration, executable patch, or file edit occurred during either process.

## Appended-grain result

The accepted observer began with grain `0`, `NextLife=0`, unconsumed entry 62,
and unconsumed neighbors 0 and 1. After the approved position write:

- entry 62 y changed `-1301 -> 0x80000000`;
- grain byte `0x0059D9B1` changed `0 -> 1`;
- neighboring entry y values remained exactly `-1303` and `-1300` across all
  791 samples;
- mask remained 0 and `NextLife` remained 0 across all samples;
- the terminal sample at 7.995816292 seconds retained the target position and
  accepted state.

This freshly confirms the isolated appended record is collected by retail PC
logic. It does not prove controller reachability to the forced position.

## Duplicate-letter result

The accepted observer began with mask `0`, grain `0`, `NextLife=0`, original
selector-`0x10` entry 50 unconsumed, and duplicate selector-`0x10` entry 63
unconsumed. After the approved position write:

- duplicate entry 63 y changed `-1853 -> 0x80000000`;
- mask byte `0x0059D9B2` changed `0 -> 1`;
- original entry 50 y remained exactly `-1707` across all 791 samples;
- grain remained 0 and `NextLife` remained 0 across all samples;
- the terminal sample at 7.992603017 seconds retained the target position and
  accepted state.

This freshly confirms one moved duplicate letter independently drives its
existing selector mask bit under retail PC logic. It does not re-prove the
other three selectors, repeated completion, or the later `FLIKFLIK` patch;
their retained static/data/recipe evidence is unchanged.

## Survival and cleanup

Both exact `bugs.exe` PIDs remained live after their terminal samples. Each
owned Gamescope process group was then terminated, its retained reaper was
closed, its run-created Wine device helper was closed by exact PID after
graceful termination did not succeed, and its private null sink disappeared.
Wine `Y:` was restored to
`work/copies/BUGS_PC-full-disc`. Final targeted audits found no `bugs.exe`,
Gamescope, coordinate-overlay, input-movie, run-private sink, or screenshot
process from these arms.

## Evidence disposition

**Confirmed:** the two approved breakpoint-free position-write arms reproduce
the exact Training behavior families required by M3.7 with exact hashes,
before/after state, isolation, survival, and cleanup.

**Inferred:** these fresh receipts repair the governance defect in M3 exit gate
1 when combined with the retained PC static/data evidence. Only an independent
closure audit may accept that inference and close M3.

**Unknown/unchanged:** controller-only access to these exact pickup points,
generic collectible/letter tooling, deterministic long gameplay replay, and
all previously retained semantic limits.

## Worker result

At the worker boundary, M3.7 was complete and M3 remained Active pending a
fresh independent James audit of this packet and all four exit gates. M2/M5
remained Deferred and M4/M6 remained Complete.

## Later independent disposition

[[EXP-20260815-135 - Independent M3 ratchet acceptance audit]] rehashes and
parses both raw traces, rebuilds the exercised C helper byte-for-byte,
reproduces the five recipes and all validation gates, and returns `ACCEPT`.
That later audit closes M3 without widening this worker claim.
