---
type: session
date: 2026-09-04
agent: Codex
status: diagnosis-complete-user-game-paused
---

# 2026-09-04 2034 - Codex - Paused side-view visibility diagnosis

**Follow-up:** the user authorized the prepared in-place comparison;
[[2026-09-04 2047 - Codex - Paused subdivision verified and restored]] completes
both writes and returns the original mesh to this same paused game. Statements
below about pending authorization describe the earlier diagnostic boundary.

The user reports residual leg fragments after left/right movement against the
zero-offset box and asks to preserve the already-triggered paused state.
[[EXP-20260904-009 - Paused side-view depth interpolation]] investigates that
same game using guarded read-only memory and a native capture, then executes
the original character and static-mesh drawing routines offline on a captured
copy. No live input, write, debugger, signal, restart, close or save-state action.

**Keep paused/open:** game46701/1147812, group46458, display`:2`,
sink`ablpc_mute_46458`. Position`(163024,-102401,509900)` is176 units outside
the box's left plane and on the lower deck. Camera/contact values remain stable
through capture and later preflight.55 readable mappings were saved privately;
this is a sequential memory capture, not an atomic/restorable process state.

The offline static renderer reproduces12 consecutive live-buffer XYZRHW
vertices exactly. Its large face has the wrong relative depth at sampled visible
leg pixels; a ray meets the physical box top first. Subdivision brings emitted
depth much closer to the analytic top and ahead of Flik in most such samples.
The actor buffer match is partial, and the computation does not model the full
GPU. The conclusion is strong evidence for large-face depth interpolation as
a residual cause, not a live changed/restored acceptance result.

Prepared a same-dimensions45-vertex/33-quad candidate using the existing tested
builder. The1,078-byte prefix at`0x006662A7` is the only proposed live change;
collision and object settings stay identical. Saved both exact prefix buffers
and a read-only preflight in EXP-009's `candidate-plan.json`. The proposed
temporary swap/capture/restoration needs explicit authorization for both memory
writes and brief suspensions; none occurred. Preserve this user pose while
awaiting that decision. If the pause menu prevents refresh, do not unpause
without agreement.

EXP-008's stationary one-byte removal/restoration remains valid but is a partial
repair. Updated Current State, Environment, DEC-234, roadmap, KU-079/080,
mesh/authoring notes, experiment/session follow-ups, MOCs and Session Index.
The existing197 focused tests are prior evidence; EXP-009 adds three successful
original-instruction calls and candidate invariants, without new production
code. No full make check, commit, independent audit, R2q or PS1 action.

Closing checks: python-doctor, vault-lint (0 errors; existing budget/metadata
warnings), M4 compatibility, tracked-file audit (0 violations) and diff whitespace
check pass. Claim sweep for the old current-state heading reports old0/new1,
`new_only`. Final guarded state and loaded-data reads still match the paused
fixture. EXP-008's report and provenance-bound comparison helper remain intact.

Report13,366 bytes, SHA-256
`88dc3516d4ce54f6c6a08c6dd889f96e9bce31f9f9b9c3ccaf1b8669fe1c8fe4`.
