---
type: session
date: 2026-08-21
agent: Codex
topic: PC Level01 route reconfirmation and P0B passive-lifecycle pickup
status: live-operational-runtime-offline-p0b-candidate
tags:
  - session
  - reverse-engineering
  - level01
  - terrain
  - collision
---

# 2026-08-21 0823 - Codex - PC Level01 route reconfirmation and P0B pickup

## Outcome

The user corrected the false pickup premise that deterministic Anthill Level01
navigation was unsolved. After a read-only preflight identified the abandoned
P0A runtime, the user explicitly directed an immediate proper PC launch. The
exact recorded P0A leftovers were recovered: `SIGTERM` did not clear process
group `1834769` or winedevice `1834980` within 5.1 seconds, so the exact guarded
targets were sent `SIGKILL`; their private sink disappeared with the runtime.
The next `make session-audit` was exactly clear (zero runtime processes, sinks,
or open sessions). P0A's pending evidence, stage bytes, terminal-path absence,
and `R:` target were not changed.

The PC game was then launched with:

```text
setsid ./scripts/play-pristine.sh --research --windowed --mute --auto-hardware
```

The executed derived PC image was SHA-256
`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`.
The live identities were Gamescope `1978673/33236090`, nested Xwayland
`1978700/33236114` on `:2`, and `bugs.exe` `1978909/33236220` in process group
`1978654`. Owned main XID `14680071` remained `640x480` and PID-bound to the
game.

After the exact `ROUTINE : --- Start LevelSelect ---` log marker and more than
the fixed one-second no-input settle, the direct focused XTEST/`xdotool` route
was applied: `Right` held 180 ms, one-second gap, `Return` held 180 ms. The log
then recorded `Y:\PC\BUGS\cd\level01\level.dat` and `ROUTINE : Start
ClearLoadScreen.` A second focused 180 ms `Return` reached `ROUTINE : End
ClearLoadScreen.`, `ROUTINE : ---End InitMainGame---`, and `ROUTINE :
NextLife.` A compositor capture at `2026-08-21 08:19:16-04:00` is a 640x480,
301,805-byte PNG with SHA-256
`77f6eeffd2c0d1fd2193ab7e5bcd61bd51dae54bbc5a6247359c3303d384f598`;
direct visual inspection shows non-faded Anthill gameplay with Flik present.
The transient PNG remains outside the repository under `/tmp`.

No process-memory read/write, debugger, save state, DAT mutation, or `R:`
change occurred. The live game is intentionally left open for the user; it is
not admitted as P0B evidence and must not be sampled by the successor. Git was
clean after launch.

## Correction to the pickup

This reconfirms the already-established PC route in
[[PC autonomous game control]] and the earlier R2c/R2f runtime arms. It does
not establish the live semantics of carousel counter `0x00599AF8`. P0A's
Level07 result came from replacing the proved direct focused `xdotool` delivery
with its new persistent-X held-state delivery, not from an unsolved Level01
route. A P0B design may reuse the exact proved direct input route before
collection while retaining the no-process-memory boundary; its persistent X
connections should begin only after navigation.

## Boundary

This launch is an operational reconfirmation, not a frozen scientific packet.
It supplies no P0A lifecycle sample and no terrain, collision, material,
visibility, or causal conclusion. P0A-AH-001 remains consumed and pending with
zero samples. P0B requires a fresh immutable protocol/stage/evidence identity,
offline tests, James acceptance, and fresh explicit runtime authorization.

## Recommended next action

Implement and audit an argument-free P0B successor that preserves P0A's exact
521-point passive `/proc` collection and validated packet semantics, never
touches P0A pending bytes, and substitutes only the established pre-collection
PC navigation path and fresh identities.

James returned **ACCEPT AS AN OFFLINE DESIGN BASIS — NOT A PRE-RUNTIME
ACCEPT**. His critical ordering correction preserves the collector's existing
sample-5 title Return. Direct `xdotool` sends only carousel Right and select
Return; after exact Level01/Start ClearLoadScreen, two fresh persistent X
connections open and the 521-point grid begins. The independent worker sends
the sole title Return at sample 5, and ordered gameplay markers are validated
only after the grid.

The implementation must allocate a new protocol/wrapper and fresh stage,
pending, published-unverified, accepted, and rejected identities; authenticate
P0A pending stage/evidence exclusions before and after; use a separate `Y:`
stage without changing P0A's `R:`; reject any dirty pre-audit or adoption of
the currently open game; preserve all `1b61da3` task/error/manifest/fsync
semantics; and retain normal-close-only cleanup. A fresh James verdict and
fresh explicit runtime authorization remain mandatory after implementation.

## P0B offline implementation candidate

The fresh `ablpc-r2p-p0b-passive-lifecycle-v1` implementation now exists only
as offline source. Its argument-free wrapper fails closed with an explicit
`not runtime-authorized` error. It allocates fresh P0B stage, pending,
published-unverified, accepted, and rejected paths under `EXP-20260820-005`,
uses a separate `Y:` stage, and pins complete content manifests for the
existing P0A stage and pending packet before and after any future run. It
rejects existing/dangling/aliased P0B namespaces and cannot adopt the live
operational game because launch remains behind an exact-clear pre-audit.

Navigation is separated from collection. Direct focused `xdotool` is limited
to one 180 ms Right and one 180 ms select Return, with exact one-second settles
and guarded keyup. Any fresh non-Level01 `level.dat` load rejects immediately.
Only after exact Level01 followed by Start ClearLoadScreen may two persistent
X connections open. The unchanged independent worker owns the sole title
Return at sample 5 of the 521-point grid. Ordered, unique End ClearLoadScreen,
End InitMainGame, and NextLife markers must append to the exact pre-title log
prefix after the grid. A precollection close may use the still-live xdotool
route, but the existence of `collection.json` permanently prohibits that
fallback; post-collection close uses only the retained persistent input
connection.

Scientific packets require the gameplay gate. Collection failures may publish
only an exact procedural rejection without that gate; precollection and
post-collection gameplay-gate failures stay pending and make no lifecycle
claim. Cleanup failure also stays pending: there is no signal fallback, drive
restoration, or terminal publication until owned runtime and audit clearance
are exact. At this first-candidate checkpoint the focused analyzer/packet/
native-X suite passed 308/308,
including P0A one-byte mutation, namespace alias, wrong-level-then-forged-
Level01, stale/order/duplicate log, settle/key/focus/chronology, strict JSON
root/schema, symlinked receipt, sample-5 input, and post-collection xdotool
attacks. No P0B runtime is authorized or has occurred.

The first complete repository gate passed 2250/2250 in 662.12 seconds with
zero tracked-file violations. That historical checkpoint became immutable as
commit `2277b75ecf8170fb2e1fc28f9cb24d19c0b8471b`, tree
`cf2f88cb64cca22bd811751318ae8ee8ef2f1b21`, and was sent to James. Its
historical offline SHA-256 identities were collector/validator
`0e585f06...1208`, lifecycle analyzer `c7441293...9fe78`, wrapper
`e4ae7fbf...e3ff`, and launcher `09652411...f6051`.

## First immutable James rejection and successor correction

James returned **REJECT** for exact `2277b75` / `cf2f88c` without launching,
controlling, or reading the live game and without modifying the repository. He
confirmed the P0A exclusions, absent production P0B namespaces, route ordering,
sample-5 Return, 521-point lifecycle logic, normal-close-only cleanup, and
308/308 focused tests. He nevertheless reproduced seven blocker families:

1. the source clone carried a pre-existing 66,230-byte `PC/BUGS/bugs.log`,
   while neither the executor nor validator established a fresh regular file,
   stable path identity, or exact append-only byte chain;
2. wrong-level matching recognized only `Y:` and admitted an `R:` Level02 load
   before a forged-valid `Y:` Level01 chain;
3. the ephemeral xdotool connection identity did not include the exact nested
   display;
4. boolean/float aliases and malformed list roots survived in xdotool focus,
   pre-settle duration, gameplay positions, and optional window timestamps;
5. publication receipts were ignored and the manifest admitted extra fields;
6. direct analysis accepted extra collection/sample/process fields and
   skeletal asset guards, with non-object roots leaking implementation errors;
7. plan/disposition prohibited vocabularies disagreed, save state was absent,
   and the preserved P0A `R:` mapping was not authenticated.

The successor correction handles all seven as one boundary. `_prepare` now
removes and fsyncs the staged log before launch and retains its exact prior
size/hash or exact prior absence. The reader uses `O_NOFOLLOW`, requires a
regular file and stable device/inode/path, decodes exact UTF-8, and carries
byte-count/hash/file identity through every append-only gate and final log.
Level-load recognition is drive- and slash-independent. Xdotool identities are
`xdotool-XTEST-ephemeral-v1@<runtime.x_display>`. One exact shared collection,
sample, process, window, asset, and metadata-error structure runs before every
direct/scientific/rejected outcome. Publication phases admit only ordered
pre/post/manifest states whose canonical bytes equal the derived result and
whose manifest closure is exact. Plan and disposition now use the same
save-state-inclusive prohibited map, and both P0A receipts, the plan, current
filesystem, equality check, and chronology retain the exact `R:` symlink.

New regressions replay every James counterexample, both scientific and
procedural-rejection paths where applicable, plus real staged-log removal,
symlink/non-UTF-8/replaced log files, terminal publication incompleteness, and
direct malformed roots/extra fields. The focused analyzer/packet/native-X
suite passes 351/351. The full repository gate passes 2293/2293 in 663.10
seconds with zero tracked-file violations. No P0B runtime or authorization was
created; the open operational Level01 game remains untouched and inadmissible.
Corrected offline SHA-256 identities are collector/validator
`91cd0ec4...786b`, lifecycle analyzer `c7441293...9fe78`, wrapper
`e4ae7fbf...e3ff`, launcher `09652411...f6051`, primary tests
`dd9c4adb...b0f`, packet-integrity tests `44f66f69...1195`, and native-X tests
`8a1e80de...31b7`. The next audit below then rejected that exact candidate.

## Second immutable James rejection and successor correction

The first correction was frozen as commit
`8b8d19df0dd8d1db76ef26302753add2938039b0`, tree
`e8b58c9f26dea6473648b71017ad0ff5b05f3ede`. James returned **REJECT** after
351/351 focused passes and broad numeric/boolean/object-root sweeps. He
reproduced nine remaining fail-closed defects: the pre-input backslash-only
level guard; incomplete P0A entry/count validation; a later Level02 gameplay
load; duplicate XIDs/multiple focus; Python equality aliases in retained audit
data, the P0A `R:` boolean, and publication results; an exact-key list
connection receipt leaking `AttributeError`; and lexical `..` terminal-root
aliasing. He found no tenth defect in the bounded sweep. No runtime action or
authorization consumption occurred.

The next offline correction shares one any-drive/either-slash parser across
navigation, gameplay, and packet analysis and requires exactly one total
post-LevelSelect Level01 load. It requires exact P0A entry schemas/count/order,
unique XIDs and one retained focus, independently validated retained audit
data, an exact boolean `R:` mapping, canonical result-derived publication
bytes, object connection receipts, and canonical absolute packet roots.
Direct, scientific, rejected, and native-X regressions now pass 396/396.
Collector/validator SHA-256 is
`b50a81d847eb225b25b75f4f5baf6260ecb17b456e6005132be6a219489eb4e5`.
The wrapper remained fail-closed; the live operational Level01 process was not
observed, controlled, closed, or adopted and remained inadmissible. The full
offline gate then passed 2338/2338 in 666.31 seconds with zero tracked-file
violations. This exact checkpoint became commit
`e0fa61a4e634a47e811bbe0a94b161a0aefca06a`, tree
`02550b15d3ed588f87b790f585057d130fc2233e`, and went to James.

## Third immutable James rejection and successor correction

James **REJECTED** exact `e0fa61a` / `02550b15` after independently passing
396/396 focused tests and broad schema sweeps. A list/dict P0A entry `type`
reached dictionary membership before type checking and leaked raw `TypeError`.
Separately, a coherent fresh wrong-level load before the sole LevelSelect
marker was ignored by executor and packet validators, which parsed only the
post-marker suffix.

The successor requires a string entry kind before membership, with direct and
scientific/rejected list/dict regressions. It parses the entire fresh
LevelSelect prefix and requires zero loads before first input, retaining the
sole later Level01 load through final gameplay; executor and both packet paths
have coherent regressions. The focused suite passes 405/405 and source SHA-256
is `347fd5062aff61c7302ced489621fa6b3caec7460b170150f6568969f413e014`.
No runtime/session action or authorization was consumed. The full offline gate
then passed 2347/2347 in 663.90 seconds with zero tracked-file violations. The
clean checkpoint became commit `3c90a6f1e2291f21e756be7c7f339bd2bdbd33e9`,
tree `5fb8ea633f4401e471d29aaced69bb148afe37d5`.

## Immutable offline acceptance

James independently passed the exact 405/405 focused suite, replayed the prior
and adjacent schema, route, lifecycle, publication, cleanup, and claim-ceiling
boundaries, confirmed the P0A 2339/17-entry exclusions and preserved `R:`,
absent P0B namespaces, wrapper exit 2, and clean git, and returned **ACCEPT**
for exact `3c90a6f` / `5fb8ea6`.

This accepted only the offline P0B pre-runtime design. That verdict alone
granted no runtime authority and the wrapper remained unable to launch. The
next section records the later authorization; the open operational game
remained untouched and inadmissible throughout the audit.

## One-shot runtime authorization and blocked preflight

The user then replied `okay continue on`, which authorizes one exact
P0B-AH-001 wrapper process invocation after the James ACCEPT. The one-shot rule
is fail-closed: the first invocation consumes the identity regardless of
pre-plan failure/exit and no retry is permitted. If it creates pending or
terminal evidence, activated source bytes remain pinned because the packet
authenticates them and namespaces block replay. Only a pre-namespace exit
permits retiring the entrypoint, while authorization remains consumed.

`make session-audit` found the previously preserved operational game at
`1978909/33236220`, Gamescope group `1978654`, Xwayland `:2`, and private sink
`ablpc_mute_1978654`. The exact focused normal-close chord did not clear it.
No signal fallback was used, the audit remains dirty, every P0B namespace is
absent, and the authorized invocation was still unconsumed at that checkpoint.

The accepted activation patch changes `run_frozen_p0b()` to construct one
executor with `frozen_config()` and invoke `run()` once. Repository tests are
explicitly monkeypatched before any wrapper call, so a gate cannot launch the
game. The source SHA-256 is
`9e2093bbfa27dd3b4e68ece79ebde296e7977fc14ed9c5d08cf49b4111ea2a5e`.
Focused tests pass 405/405 and the safe full gate passes 2347/2347 in 667.45
seconds with zero tracked-file violations. James independently **ACCEPTED**
exact activation commit `c3ad480f7988870eba3582f8d8d887aae9a50942`, tree
`59acd5d5ace9328a28cf99c1bf3e71fc418370a5`, after passing the exact 405/405
focused suite and verifying test launch isolation, source pins, frozen P0A
exclusions, and clean git. A newly exact-clear preflight plus the frozen
immediate checks remain required before the one real invocation.

## Consumed P0B result and separate recovery pickup

The user subsequently authorized process killing. Exact guarded TERM then
survivor KILL cleared the old operational group and produced a clear audit.
The accepted P0B wrapper was invoked exactly once after every frozen check and
is now consumed. Its complete 521-point collection provisionally found one
persistent added task `2086681/34785536` at sequences 27–520, with no other
lifecycle class or collection error. Collection SHA-256 is
`d8ff0e76...44bc2f`.

Normal Alt+F4 failed to clear new group `2086248`, so the runner used no signal,
exited 2, retained 26 exact pending files, and left `Y:` staged. James accepted
the provisional collection and the pending/fail-closed interpretation only;
there is no terminal P0B packet or terrain/collision claim.

James rejected first recovery implementation `575756d` / `004bf35d` after
reproducing numeric aliases, forged commands, contradictory event histories,
incomplete `/proc` enumeration and immutable-tree validation, stale
per-signal guards, and invalid publication/one-shot failure semantics. No
signal or recovery action occurred. The successor freezes every exact command,
retains fresh guards and complete group censuses, authenticates bounded polls
and complete current invariants, consumes before preflight, preserves stable
failure state, and publishes through a fresh unverified phase. Its module hash
was recorded with its focused/native/full gates. James then rejected exact
`d4de863` for one pending-receipt numeric alias, post-deadline polling, and
both publication rename races. The
next correction uses exact comparison and atomic `RENAME_NOREPLACE`; module
hash is `d1b3e4af...3c38a`, recovery tests pass 48/48, and the non-native set
passes 482/482 plus native X; full `make check` passes 2395/2395 in 672.58
seconds with zero tracked-file violations. At that checkpoint it had not run;
exact commit and James acceptance remained mandatory. No P0B retry or new
runtime authority followed.

## Recovery failure and terminal operator cleanup

James accepted the corrected recovery at exact `fae9b2f` / `a6e9148`. Its
sole invocation sent the authorized group TERM and then failed closed when
still-present exiting processes exposed cleared command lines. It remained
consumed, did not restore `Y:`, and did not publish recovered evidence. The
recovery-pending/recovery-failed trees remain `444b221e...f309e` and
`8e2fb90e...f5d1`.

Between the authenticated pre-recovery and post-TERM states, 160 bytes of
shutdown text were appended to the original P0B `launch.stderr`. Chronology,
content, and retained-FD provenance make attribution to recovery shutdown
consistent, but it remains an inference. The exact historical pre-recovery
packet is `323c958d...451661`; the preserved current packet is 26 files /
`1092fcb9...25f2`, with 11,423-byte log `fb2ba241...eaf5`. Three processes
remained: Gamescope `2086265/34784563`, gamescopereaper
`2086416/34784596`, and winedevice `2086454/34784605`; there was no sink or
open session.

The user-authorized operator cleanup was frozen as exact `4de8b085` /
`666cd92f` after 30/30 operator, 266/266 focused, and 2425/2425 full tests and
James pre-execution **ACCEPT**. Its single invocation sent individual TERM then
fresh-identity-guarded KILL to only those three survivors. Both final audits
are exactly clear, `Y:` is restored to retail, `R:` remains P0A, and the
operator added no later log suffix. James independently authenticated and
**ACCEPTED** the 15-entry terminal envelope, tree `24df2fb7...d65b`.

The final disposition deliberately remains bounded: recovery is
`failed-consumed`, P0B is `pending-cleanup-failed`, the original run is not
relabelled, and no future runtime is authorized. The added task's role and all
terrain/collision/material/render/causal questions remain open.

The first post-cleanup full gate then exposed six state-dependent test
fixtures: they read the now-retail real `Y:` link while constructing synthetic
pre-cleanup/staged invariant snapshots. The fix is test-only: one helper
supplies the staged `Y:` mapping explicitly for those fixtures. The accepted
operator source and every retained evidence byte remain unchanged. Focused
operator validation passes 30/30, and final `make check` passes 2425/2425 in
673.91 seconds with zero tracked-file violations.

James rejected the first closeout commit `49d07ad` / `544ba40` on documentation
only. Five notes had promoted the log suffix's recovery-shutdown attribution
from the terminal receipt's explicit `inference` to causal fact, Environment
omitted the qualifier, and three historical recovery sections still read as
current/unrun. The correction uses the same bounded wording at every append
claim: the 160 bytes are an authenticated state transition, while chronology,
content, and retained-FD provenance make recovery-shutdown attribution
consistent but still inferential. The three older sections are now explicitly
past-tense checkpoint history. Production sources, evidence, result ceiling,
and tests are unchanged.

## Links

- [[EXP-20260820-005 - R2p task lifecycle diagnostic]]
- [[PC autonomous game control]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Known Unknowns#KU-074 - Live semantics of the level-select carousel position counter|KU-074]]
