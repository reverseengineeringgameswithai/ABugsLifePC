---
type: session
date: 2026-08-20
agent: Codex
topic: P0A hard-truth correction before authorized runtime
status: completed
tags:
  - session
  - reverse-engineering
  - level01
  - terrain
---

# 2026-08-20 2124 - Codex - P0A hard-truth correction

## Outcome

The user explicitly authorized the exact 521-point passive P0A `/proc`
task-lifecycle collection, with no process-memory read or write. The frozen
ordering gate still required James acceptance before launch. James audited
commit `52d9a0f6db4d98ffa9676d956d406254cb82c281` / tree
`8b271be807f596ac7122636dd4ff53731cf18c26` and returned **REJECT** on nine
reproducible evidence-integrity defects. No game launched and the authorization
was not consumed.

The correction makes `published-unverified` the only intermediate publication
identity and creates a terminal directory only after post-move validation,
manifest closure, and fsync. It validates the full timing grammar on every
rejected sample prefix; narrows title failures; brackets first-seen metadata
with equal task identities; binds exact current asset paths to open
descriptors; records distinct X connection descriptors plus owned Xwayland
identity; names stable, four single lifecycle classes, and mixed results
exactly; refreshes all source/test pins; and reads the final log once.

The first focused correction suite passed 150/150, including the real isolated
Gamescope/Xwayland X11/XTEST fixture. The pre-runtime session audit is clear.
Stage, pending, published-unverified, accepted, and rejected production
identities remain absent. `originals/`, game assets, process memory, debugger,
signals, screenshots, DAT/localizer/candidate state, and R2o were untouched.

James then re-audited exact commit `b24890b` / tree `8ce1cfc3`. He confirmed
the first nine corrections and independently passed 150/150 focused plus
1794/1794 full tests, but returned **REJECT** on five further counterexamples:
timing failures self-invalidated rejected packets; manifest creation followed
the last semantic validation; unresolved metadata could duplicate/mislabel an
initial identity; non-hex 64-character executable digests passed partial
rejection; and the two X sockets lacked peer-process proof.

The second correction separates structural validation from an exact derived
timing rejection, repeats semantic validation after manifest creation and
fsyncs both rename parents, emits one neutral deduplicated unresolved result
with initial/added category lists, requires lowercase hexadecimal digests, and
binds both actual Xlib sockets' `SO_PEERCRED` PID plus `/proc` start ticks to
the retained owned Xwayland identity. The focused suite now passes 158/158,
including the real isolated Gamescope/Xwayland peer-credential fixture. No game
launched and the one live authorization remains unconsumed.

James's third audit of exact commit `c05f167` / tree `d60d88bb` confirmed those
five fixes, matching pins, 158/158 focused tests, absent production identities,
and clean git/session state. He still returned **REJECT** because adjacent task
deltas erased cross-gap identity history. A changed start value after a
one-sample absence was add/remove mixed instead of reuse; missing metadata on
that later identity was categorized differently by the two analyzers; and a
baseline identity that disappeared for one sample and returned was called
short-lived.

The third correction builds compact ordered per-TID identity histories across
all 521 samples. It detects reuse across gaps, partitions metadata by global
first-seen sequence in both analyzers, limits short-lived to a post-baseline
non-reappearing/non-reuse identity, and fails closed on any exact identity that
returns after absence while retaining the precise interval. Six paired
regressions bring the focused suite to 164/164. No game launched and the live
authorization remains unconsumed.

James's fourth audit of exact commit `96e2fdf` / tree `60ab6a3d` confirmed the
complete-history correction, 164/164 focused tests, 1808/1808 full tests,
matching pins, absent production identities, and clean state. He still returned
**REJECT** because both analyzers and the fixture failed to anchor the task
census to the guarded process leader. They accepted process `(10,20)` with
leader `(10,1)`, only an unrelated worker, no tasks, or a reused leader.

The fourth correction requires both per-sample task enumerations to contain the
guarded PID; every stable sample must parse exactly
`(pid,process.start_ticks)`; and no task may predate the process. Only one exact
sample-local identity-read failure for an enumerated leader can omit its parsed
identity, producing unresolved enumeration drift. The fixtures now keep a
permanent leader and exercise lifecycles on worker TIDs. Five adversarial cases
are paired across direct, scientific, and rejected-prefix validators. The
focused suite passes 184/184 and the full repository gate passes 1829/1829. No
game launched and the live authorization remains unconsumed.

James's fifth audit of exact commit `b8e8d44` / tree `5c48cbb4` confirmed the
leader anchor, prior fixes, pins, tests, absent identities, and clean state. He
still returned **REJECT** because the sole permitted leader-omission exception
accepted malformed evidence. Direct analysis accepted missing/extra fields,
non-string, empty, and untyped identity errors; scientific and rejected-prefix
validation also accepted empty error strings.

The fifth correction routes every metadata-error receipt through one shared
validator before omission or early drift return. It requires exact phase
fields, positive identities, nonempty single-line typed text bounded to 4096
characters, a closed exception-type set, and bounded internal `P0AError`
prefixes. Direct/scientific/rejected regressions cover the malformed variants,
while a valid local leader read error still yields unresolved drift. The
analyzer/packet suite passes 201/201 and the separate native X fixture passes
(202 total); the full repository gate passes 1846/1846. No game launched and
the live authorization remains unconsumed.

James's sixth audit of exact commit `a68076f` / tree `10bdcad9` confirmed every
earlier malformed-record form was closed. He still returned **REJECT** because
the shared internal `P0AError` union admitted the metadata-only identity-change
message under the initial `identity` phase, allowing an impossible receipt to
omit the leader in direct, scientific, and rejected validation.

The sixth correction uses exact phase-specific message sets: five fixed
`/proc/stat` parser failures for initial identity, with the one exact post-
metadata identity-change message added only to `new-identity-metadata`.
Direct/scientific/rejected regressions reject the wrong phase and accept the
producing phase. The analyzer/packet suite passes 207/207 and native X passes
separately (208 total); the full repository gate passes 1852/1852. No game
launched and authorization remains unconsumed.

## Next

James accepted the sixth correction at exact `8437c0a` / `53241906`. The one
authorized runtime was then consumed and is documented in
[[2026-08-21 0022 - Codex - P0A pending pre-collection runtime]]. It selected level07, produced no
collection, and remains pending after normal close failed without signal
fallback. No recovery, retry, second passive process, or later diagnostic is
authorized.

## Links

- [[EXP-20260820-005 - R2p task lifecycle diagnostic]]
- [[Decision Log#DEC-187 - Bind P0A internal metadata errors to their producing phase|DEC-187]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Known Unknowns#KU-079 - The render-geometry command grammar (the LEVEL.DAT draw-command stream)|KU-079]]
