---
type: session
date: 2026-09-02
agent: Codex
topic: R2q 027 rejection and 028 activation freeze
status: activation-docs-committed-final-clean-tree-james-reaudit-pending
---

# 2026-09-02 0056 - Codex - R2q 027 rejection and 028 activation freeze

## Goal and authority boundary

Continue R2q offline after the consumed R2q-026 cross-mount-namespace
executable-provenance failure. Correct the rule without launching the game or
invoking the restoration/R2q wrapper, preserve immutable predecessors, obtain
James source and activation acceptance, run the full gate, update durable
state, commit cleanly, and submit the exact clean tree to James. No runtime,
mapping, ptrace, process-memory, input, signal, screenshot, or save-state
authority was granted. The retained round-91 stash remains `stash@{0}`, object
`76db1c9ee1ffffce52cea6aee591c24ab6a1c39a`, and was not dropped.

## R2q-027 correction and immutable rejection

R2q-027 hashes/stats the executable through the retained
`/proc/<pid>/root` and compares `/proc/<pid>/maps` device/inode identity only
with that same process-namespace result. Host and process-root bytes, inode,
mode, size, mtime, and ctime must still agree; host-global and process-
namespace device values are recorded separately rather than equated. Focused
runtime regression coverage exercises differing device values and direct-byte
replacement rejection.

James accepted source commit
`ee6c6084897ee08565eb074fcbbfd682215c42e8` / tree
`3815f9413b5f6e5e07b83b347f11c823cdfeef53`. Benchmark-013 is 4,563 bytes /
`0559c257fb955c6cdf9be5546bbd835e8df2c2f4bb1e1e67b5aa100c684a6524`;
final anchor-013 is 1,364 bytes /
`9150244fbad5d5c37338e117b92a8777ec65cb7d46d0787a008b363136c6939a`.
Immutable design-027 is 54,983,457 bytes /
`499e5fda1a13df59f71f9ee6a6ccc202a424b23db00b0543c89c7617cb62f211`,
with 5,966-byte activation manifest
`c3376624af23bb73c0c996da4263915e0a811d36637b87b41049d67af9259ed9`.
James returned `ACCEPT R2Q-027 ACTIVATION`.

The complete design/runtime pytest tranche then reported 486 passed and 30
failed in 4,313.31 seconds. Twenty-eight failures were a cascading
`OSError: [Errno 122] Disk quota exceeded` after completed pytest scratch grew
to 15 GiB. Two failures were genuine frozen-source defects: the mapping test
still asserted `retail-026`/`D2-AH-026`, and the failed-025 regression did not
accept the current v3 `field set mismatch` rejection. The canonical 1,588-byte
receipt is
`work/copies/EXP-20260820-005/evidence/offline/quiet-census-design-027/finalization-rejection.json`,
SHA-256
`8375369c4f0b93e4c3f5861fc4546890ea469dfbc263722e53b453fae185b4fb`.
James returned `REJECT R2Q-027 FINALIZATION`; the design remains immutable and
was never run.

## Fresh R2q-028 source and activation

R2q-028 corrects the two anchored tests and advances all prospective runtime,
stage, publication, and comparison identities to `-028`. James's first source
review rejected omission of 28 never-used R2q-027 paths from the absence
closure. The correction adds the exact 28-path inventory to
`predecessor_absent_paths()`, makes the continuity attempted-path set include
it, and supplies both exact-inventory and per-path appearance-rejection tests.
Predecessor closure v6 binds design-027 and its finalization-rejection receipt.

Measured maximum-shape accounts are 1,048,907,365 and 1,201,329,750 raw bytes,
and 435,449,287 and 492,562,955 zlib9 bytes. Protocol
`ablpc-r2q-one-shot-authority-v10` therefore freezes 1,280 MiB raw and 576 MiB
stored bounds, leaving 140,847,530 raw bytes and 111,416,821 stored bytes above
the measured maxima. James accepted source commit
`68e0714f8f1e8bac6ed4c106ce32c6db8c3aa2ee` / tree
`cda3886ef3194043e7982784c24a4db8bc8e402d`.

Benchmark-014 ran once from that clean source. Its 4,563-byte result is
`83cf0963b2971a9084a7b06dcbf954052504b22f6d01ad13eafdd90ef505d05e`;
the maximum control/comparison times are 24.372802910 / 81.894036244 seconds,
leaving 98.105963756 seconds below the prospective 180-second ceiling. Final
anchor-014 is 1,364 bytes /
`0046689714ac0621f31b8561769162de5faf374b1767bd442f5ba919cbace756`.

The design freezer then ran once. Immutable
`work/copies/EXP-20260820-005/evidence/offline/quiet-census-design-028/design.json`
is 78,066,492 bytes /
`c5840fe90aec93f8d26baf4a71b567cc4576e606ecba47953dffcd75b327e087`;
its 5,966-byte activation manifest is
`fb3e82926581dbaa3c64a7a44320734e22b680c33fe4e950b35a0a788d925fa8`.
Validation returns `offline-r2q-design-frozen-runtime-unauthorized`. James
returned `ACCEPT R2Q-028 ACTIVATION`.

## Full gate and environment

The pre-gate session audit was exactly clear. The full command was
`TMPDIR=/dev/shm/ablpc-r2q-028-make-check make check`, isolating maximum-shape
scratch from the home quota. It passes 3,972/3,972 in 6,102.42 seconds with
zero tracked-file violations. The exact temporary directory reached about
32 GiB and was removed after the successful gate; `/dev/shm` returned to its
prior free state. The post-gate session audit is exactly clear.

No game, emulator, restoration wrapper, R2q wrapper, live census, ptrace,
debug-register, process-memory, signal, input, screenshot, save-state, or
mapping action occurred. `Y:` remains retail inode `9998033`; `R:` remains P0A
inode `9054047`; the retired D1-026 link remains inode `9997058`.

## Scientific disposition and next step

This work establishes an offline, source-authenticated successor and no runtime
science. KU-079, KU-080, and KU-081 remain open: there is no new persistent-
task role, render grammar, terrain, collision, material, visibility,
causality, no-effect, or retail-executable result.

The documentation-inclusive activation commit completed at
`1aa45392ae87dcfc90f5630e25e992d75b05f976` / tree
`8c308ba77982ac1b53214c6c765801b86a1277e4`. James's first final clean-tree
review passed every artifact, strict-validator, predecessor-closure, 28-path
absence, capacity, stash, Git-cleanliness, and session-audit check. He rejected
only the procedural inconsistency that the committed notes still called their
own commit a future step. This bounded docs-only correction leaves only the
exact clean-tree re-audit.

Any R2q-028 D1-then-D2 invocation would be a later, separately authorized
action bound to the exact accepted activation; no such authority exists in
this session.
