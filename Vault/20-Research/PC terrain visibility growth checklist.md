---
type: reference
status: confirmed-bounded
created: 2026-09-06
updated: 2026-09-06
evidence: [EXP-20260906-001, EXP-20260906-011, EXP-20260906-012]
tags: [terrain/authoring, re/rendering, reference]
---

# PC terrain visibility growth checklist

If an entire ground/foliage mesh disappears at particular positions or angles but collision still supports Flik, check scene visibility before changing collision, blade placement or materials. This symptom was reproduced in [[EXP-20260906-011 - Expanded corner visibility regression]]; it is a diagnostic lead, not proof that every future disappearance has the same cause.

## Authoring rule

Every terrain mesh-growth path must recompute a bound around the **retained scene center**, accounting for the object origin and all vertices. Do not use an enclosing geometric sphere plus arbitrary padding. The PC side-plane comparisons are unnormalised: [[EXP-20260906-001 - PC-compatible ramp visibility bounds]] established the shared `ablpc.terrain_visibility.scene_visibility_radius` helper. At observed640x480/focal320 it uses `ceil(R*sqrt(2))+8`; this is a bounded profile with rounding allowance, not an arbitrary-renderer theorem.

Round geometric radius upward, preserve larger existing bounds, reject signed-word overflow and unsupported rotation/scale. Preserve geometry, material fields, collision, allocation and unrelated unknown bytes. The corrected foliage appender shares this helper with additive terrain authoring; EXP-20260906-012.

## Regression and runtime gates

1. Verify exact staged/resident asset, scene and camera identities. Capture visible -> hidden -> visible through normal input, retaining asynchronous capture limits. Floor-contact flags alone do not prove continuous support.
2. Separate render-data traversal from scene admission. A complete-face-stream pass can coexist with erroneous camera culling; test both.
3. Replay original-PC gate `0x0044D59F` with recorded camera/projection inputs. For EXP-011 the horizontal rejection is `0x0044D677`; that branch is not assumed for a new case. Compare a bound-only offline candidate at the same inputs.
4. Require captured-camera regressions and finite corner/edge/yaw/pitch checks where a target remains inside the viewport. Keep broader camera/profile/performance limits explicit.
5. Load a separate candidate normally and request matched-area user confirmation. Do not label offline success as a live visual fix or reuse prior memory-write authorization.

EXP-011's expanded geometric radius10023 needs bound14183 rather than10087. That changes only file offset8593 within scene160's two-byte bound at8592. Full rebuild equality and preservation are required; this is not permission to hard-code14183 for future geometry.

## Distinguish polygon distance rejection

[[PC scenery render distance]] / [[EXP-20260907-009 - Mushroom render distance diagnosis]]
show two new mushrooms passing the scene gate but emitting zero faces at the
separate mesh depth limit. Growing a scene bound does not change that cutoff.
Use the staged/resident identity and independent admission/emission checks to
discriminate the causes before tuning either control.
