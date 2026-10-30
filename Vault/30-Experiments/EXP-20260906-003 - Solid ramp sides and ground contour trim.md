---
type: experiment
id: EXP-20260906-003
date: 2026-09-06
status: test-fixture-corrected-runtime-preview-closed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 43 offline terrain authoring, native PC instruction probes, and isolated Wine preview
question: "Do appended vertical source99 collision cells, paired at render top minus96 like the working box, block lateral movement under the original PC collision code?"
result: "Yes: twenty appended vertical cells block 8/8 native outside approaches and block live; Flik's model partly disappears into the wall with root 267 world units outside the plane (clearance versus draw-order open)"
tags: [re/terrain, re/rendering, re/collision]
updated: 2026-10-29
---

# Solid ramp sides and ground contour trim

## Scope

This note tests whether appended vertical collision cells, paired with the
render surface the same way as the working EXP-004 box, block lateral movement
under the original PC collision code. EXP-20260906-002 is the visual-only
control. No live input, RAM write, debugger or process action occurred during
the offline increment.

Fresh ID allocation found no003 in experiment/report/private roots. Run-index
remains114 directories,7 unreadable,14 uncited and1 dangling citation.

## Matching collision

`terrain_ramp_solid.py` reuses `terrain_play_area.encode_group` and the additive
writer. Twenty new vertical triangle cells form both sides using outward
axis-aligned normals(+/-16384,0,0). Following the working box's pairing, their
upper edge is render top minus96 stored units, and lower edge is the old buried
base plus96. This is side blocking, not guardrails or global X/Z barriers.

All150 existing source99 cells remain active and byte-identical, including the
working connector. Twenty groups grow the payload5164 ->6044 bytes, append at
49084, and move the terminator to49964. Directory223276 ->224156; only the
known directory locator and source99 word count change along with insertion.
All188 other payloads and unknown directory fields are preserved. New cell
offsets, exact vertices, normals and admission windows are in the build report.

## Original ground under the ramp

A census of the original ground around the ramp foot found original render
reference124 covering the target: its face116968 gives east groundY-3068.0814
at(6250,10900) and face117660 gives west groundY-2911.202 at(5750,10900).
Full side-line intersections with explicitly selected original primary124/128
give27 geometric spans with one west seam fromZ3076000/247 to6139592/493,
about0.0922 stored units; the original meshes are not welded there. The
orientation census also retains28 unresolved rotated references, not promoted
to ground or discarded as causal impossibilities. The decorative side trim built
from those contours is not a confirmed rasterization repair.

## Offline original-PC results

Native side blocking: four outside approaches across two sides/two Z levels
cross in the visual-only control and remain outside in the candidate,8/8
declared arm outcomes,5.050443803s. This is lateral blocking only: the two west
candidate final flags are[1,0], so no continuously settled actor claim follows.

The first fixed-axis route gate is **not wholly accepted**. Centre/east lanes
complete up/down/up, both side step-offs land on original ground, and an east
step-off/landing returns via the open foot. West lane5850's third fixed-axis
leg misses the entrance after normal-induced X drift. Keep that failed
criterion. A separate unchanged-control run fails identically at all three
leg-end states: the downhill endpointX183355 is already outside westX184000.
Do not edit collision to compensate for this synthetic steering omission.

A separately declared continuous steering discriminator retains fixed Z+/−900
and downward512 with corrective X clamped to+/−384. All three lanes pass all
three up/down/up legs without resets,9/9,9.596176058s including the control.
These are original collision-coordinator instructions with synthetic motion,
not a full actor/input replay. Native command traversal also passes all124
supported mesh streams. Native DAT relocation preserves both trailing pointers
and the table SHA in0.163415033s. The initial route packet duration is8.819170606s.

Private evidence: `native-side-blocking.json`, `native-ramp-routes.json`,
`native-drift-discriminator.json`, `native-relocation.json` under
`work/experiments/EXP-20260906-003/`.

## Tests

Affected suite at the candidate checkpoint:137 passed,1 failed in0.59s. The
failure was the new synthetic test
`test_ground_profile_reads_both_synthetic_footer_variants`: its setup reversed
an already upward quad, so the reader correctly excluded it. The test-only
fixture-winding correction was applied after approval (see the live check
below). The five-file terrain gate passes72/72 in26.29s, xdist4/loadfile,
repo-local scratch with failed-only retention. No full make check or R2q tests.

Candidate hashes:

- TERRAIN.ALL `288d57396d6de67db0df7904567c2bf2a0a40e4309fff490f9343928dc1075b7`.
- LEVEL.DAT `f6cfa7883a902af5f43362356b7731adf9708ee5164c454b489e266867b048b2`.
- Active mesh `6ac8ba9594349af7e9c97b8d683ed33e3e88b8ec267834266eccc65549b64f33`.

Public build and validation: `reports/terrain/EXP-20260906-003.json`,
`reports/terrain/EXP-20260906-003-validation.json`.

## Live check and wall-clearance observation

The approved test-only fixture-winding correction passed **138 affected tests in
0.56 s**. The candidate launched once after clean post-close/prelaunch audits.
Complete resident sources 99/100 and mesh streams 128/160/213/280 matched the
candidate; scene bound 8560 confirmed. Postlaunch audit's seven processes and
sink are independently accounted, not called a clean no-session audit. Closure
required scoped fallback after Alt+F4; no normal-close-only claim. Runtime
packet: `reports/terrain/EXP-20260906-003-runtime.json`.

**Live result:** side collision works, but walking against a side makes part of Flik's model disappear into/behind the wall. Private screenshot `work/experiments/EXP-20260906-003/preview-01/user-wall-clearance.png`, SHA `8ae8de3d40c3c02b600aa2ca07e0a8ebafd8eeef2ddf34daf100988d9d49c2e7`. Independent captured state has root X=183733 versus west plane X=184000, an outward distance of 267 world units; this is not a measured collider radius or an atomic pairing with the screenshot.

**Open alternatives:** insufficient root/body clearance versus actor/wall draw-order or depth interaction; original-wall parity is unmeasured. Do not generalize this sample into a mesh-wide defect or padding constant.

**Next discriminator:** compare original/authored wall stop intervals and rendering with normal input/read-only RAM. If supported, isolate bounded collision-only padding from render-only inset, then check two-sided approaches, corners, open ramp foot and top return. No new memory-write authorization is implied.

## 2026-09-06 successor: clearance trial

[[EXP-20260906-004 - Wall clearance comparison and offset trial]] preserves this exact fixture as control and creates a separate collision-only48-stored-unit outward-offset copy. Original/render comparisons and finite native gates support the trial; visual success remains pending. This preview (game42212/group41955) was closed with a clean post-close audit. The successor's attempted original-wall navigation is retained as unsuccessful, not a matched live comparison.
